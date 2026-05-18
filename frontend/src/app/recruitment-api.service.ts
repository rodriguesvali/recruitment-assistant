import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, TimeoutError, catchError, delay, map, of, throwError, timeout } from 'rxjs';
import {
  CandidateEvaluation,
  CandidateProfile,
  CandidatePreviewResponse,
  CandidateSource,
  EvaluationCriteria,
  JobRequirement,
  RecruiterApproval,
  RankedRecommendation,
  RecruitmentRunResult,
  WorkflowRequest
} from './recruitment.models';

const API_BASE_URL = 'http://localhost:8000';
const DISCLOSURE =
  'These recommendations are AI-assisted decision support based on the supplied job criteria and candidate data. A recruiter must review and approve all recommendations before they are used in a hiring process.';

@Injectable({ providedIn: 'root' })
export class RecruitmentApiService {
  private readonly http = inject(HttpClient);

  checkBackend(): Observable<boolean> {
    return this.http.get(`${API_BASE_URL}/health`).pipe(
      timeout(1500),
      map(() => true),
      catchError(() => of(false))
    );
  }

  extractCriteria(job: JobRequirement): Observable<EvaluationCriteria> {
    return this.http.post<EvaluationCriteria>(`${API_BASE_URL}/api/criteria/extract`, { job }).pipe(
      timeout(10000),
      catchError((error) => this.fallbackForOfflineOnly(error, of(this.createFallbackCriteria(job)).pipe(delay(350))))
    );
  }

  previewCandidates(criteria: EvaluationCriteria, source: CandidateSource): Observable<CandidatePreviewResponse> {
    return this.http
      .post<CandidatePreviewResponse>(`${API_BASE_URL}/api/candidates/preview`, {
        criteria,
        candidate_source: source
      })
      .pipe(
        timeout(10000),
        map((response) => ({
          candidates: response.candidates ?? [],
          warnings: response.warnings ?? []
        })),
        catchError((error) =>
          this.fallbackForOfflineOnly(
            error,
            of({
              candidates: this.createFallbackCandidates(source),
              warnings: [
                {
                  code: 'DEMO_FALLBACK',
                  message: 'Backend API was unavailable, so deterministic local candidate preview is shown.'
                }
              ]
            }).pipe(delay(450))
          )
        )
      );
  }

  runRecommendations(request: WorkflowRequest, candidates: CandidateProfile[]): Observable<RecruitmentRunResult> {
    return this.http.post<RecruitmentRunResult>(`${API_BASE_URL}/api/recommendations/run`, request).pipe(
      timeout(130000),
      catchError((error) =>
        this.fallbackForOfflineOnly(error, of(this.createFallbackRun(request, candidates)).pipe(delay(900)))
      )
    );
  }

  recordApproval(runId: string, approval: RecruiterApproval): Observable<RecruiterApproval> {
    return this.http.post<RecruiterApproval>(`${API_BASE_URL}/api/recommendations/${runId}/approval`, approval).pipe(
      timeout(10000),
      catchError((error) => this.fallbackForOfflineOnly(error, of(approval).pipe(delay(250))))
    );
  }

  private fallbackForOfflineOnly<T>(error: unknown, fallback: Observable<T>): Observable<T> {
    if (error instanceof TimeoutError || (error instanceof HttpErrorResponse && error.status === 0)) {
      return fallback;
    }

    return throwError(() => error);
  }

  private createFallbackCriteria(job: JobRequirement): EvaluationCriteria {
    const ambiguities: string[] = [];

    if (job.required_skills.length === 0) {
      ambiguities.push('No required skills were supplied. Add must-have criteria before using real candidates.');
    }

    if (!job.seniority.trim()) {
      ambiguities.push('Seniority is not specified, so candidate level alignment may be lower confidence.');
    }

    if (!job.location.trim()) {
      ambiguities.push('Location or work arrangement is not specified.');
    }

    return {
      ...job,
      ambiguities,
      confirmed_by_recruiter: false
    };
  }

  private createFallbackCandidates(source: CandidateSource): CandidateProfile[] {
    const textProfiles =
      source.type === 'pasted' ? source.pasted_profiles : source.type === 'uploaded' ? source.uploaded_text : null;

    if (textProfiles?.trim()) {
      const sourceLabel = source.type === 'uploaded' ? 'uploaded-text' : 'pasted-profile';

      return textProfiles
        .split(/\n\s*\n/)
        .filter(Boolean)
        .slice(0, 6)
        .map((profile, index) => {
          const firstLine = profile.split('\n').find(Boolean)?.trim() || `Pasted Candidate ${index + 1}`;

          return {
            candidate_id: `pasted_${index + 1}`,
            display_name: firstLine.replace(/[:|-].*$/, '').trim() || `Pasted Candidate ${index + 1}`,
            profile_summary: profile.trim().slice(0, 220),
            skills: this.extractCandidateSkills(profile),
            experience: ['Experience inferred from recruiter-provided profile text.'],
            location: 'Unknown',
            source_labels: [sourceLabel],
            missing_data: ['Availability unknown', 'Compensation expectations unknown']
          };
        });
    }

    return [
      {
        candidate_id: 'cand_001',
        display_name: 'Avery Chen',
        profile_summary: 'Backend engineer with Python, FastAPI, API design, and agent workflow experience.',
        skills: ['Python', 'FastAPI', 'PostgreSQL', 'CrewAI', 'API design'],
        experience: ['Built production APIs', 'Designed LLM workflow services', 'Owned backend reliability work'],
        location: 'Remote US',
        source_labels: [`seeded-data:${source.dataset_id || 'backend_engineers'}`],
        missing_data: ['Compensation expectations unknown']
      },
      {
        candidate_id: 'cand_002',
        display_name: 'Jordan Patel',
        profile_summary: 'Full-stack engineer with Angular, TypeScript, Python services, and recruiting platform integrations.',
        skills: ['Angular', 'TypeScript', 'Python', 'FastAPI', 'ATS integrations'],
        experience: ['Built recruiter dashboards', 'Integrated HR tooling APIs', 'Created candidate review workflows'],
        location: 'Hybrid NYC',
        source_labels: [`seeded-data:${source.dataset_id || 'backend_engineers'}`],
        missing_data: ['Remote availability unknown']
      },
      {
        candidate_id: 'cand_003',
        display_name: 'Morgan Rivera',
        profile_summary: 'Data-oriented engineer with strong evaluation, scoring, and reporting experience.',
        skills: ['Python', 'Data pipelines', 'Evaluation design', 'SQL', 'Reporting'],
        experience: ['Built scoring pipelines', 'Created explainability reports', 'Supported hiring analytics'],
        location: 'Remote',
        source_labels: [`seeded-data:${source.dataset_id || 'backend_engineers'}`],
        missing_data: ['CrewAI experience unknown']
      }
    ];
  }

  private createFallbackRun(request: WorkflowRequest, candidates: CandidateProfile[]): RecruitmentRunResult {
    const criteria = this.createFallbackCriteria(request.job);
    const profiles = candidates.length ? candidates : this.createFallbackCandidates(request.candidate_source);
    const requiredSkills = request.job.required_skills.map((skill) => skill.toLowerCase());

    const evaluations: CandidateEvaluation[] = profiles.map((candidate) => {
      const candidateSkills = candidate.skills.map((skill) => skill.toLowerCase());
      const matchedRequired = requiredSkills.filter((skill) =>
        candidateSkills.some((candidateSkill) => candidateSkill.includes(skill) || skill.includes(candidateSkill))
      );
      const requiredRatio = requiredSkills.length ? matchedRequired.length / requiredSkills.length : 0.55;
      const preferredMatches = request.job.preferred_skills.filter((skill) =>
        candidateSkills.some((candidateSkill) => candidateSkill.includes(skill.toLowerCase()))
      ).length;
      const score = Math.min(96, Math.round(58 + requiredRatio * 28 + preferredMatches * 4));
      const fitLabel: CandidateEvaluation['fit_label'] = score >= 82 ? 'strong' : score >= 68 ? 'moderate' : 'low';

      return {
        candidate_id: candidate.candidate_id,
        fit_label: fitLabel,
        overall_score: score,
        component_scores: {
          required_skills: Math.round(requiredRatio * 100),
          preferred_skills: Math.min(100, preferredMatches * 35),
          experience: score - 4,
          seniority: request.job.seniority ? 80 : 60,
          location: candidate.location.toLowerCase().includes('remote') || !request.job.location ? 90 : 70,
          evidence_confidence: candidate.source_labels.includes('pasted-profile') ? 68 : 78
        },
        strengths: matchedRequired.length
          ? [`Matches required skills: ${matchedRequired.join(', ')}.`]
          : ['Has adjacent experience, but required skill evidence needs recruiter review.'],
        gaps: matchedRequired.length < requiredSkills.length ? ['Some required skills are not directly evidenced.'] : [],
        unknowns: candidate.missing_data,
        rationale: `${candidate.display_name} was scored using supplied job criteria and approved candidate data.`
      };
    });

    const ranked: RankedRecommendation[] = evaluations
      .slice()
      .sort((a, b) => b.overall_score - a.overall_score)
      .map((evaluation, index) => {
        const candidate = profiles.find((profile) => profile.candidate_id === evaluation.candidate_id)!;

        return {
          rank: index + 1,
          candidate_id: candidate.candidate_id,
          display_name: candidate.display_name,
          fit_label: evaluation.fit_label,
          overall_score: evaluation.overall_score,
          recommendation_rationale: evaluation.rationale,
          strengths: evaluation.strengths,
          gaps: evaluation.gaps.length ? evaluation.gaps : ['No material gaps identified from supplied data.'],
          unknowns: evaluation.unknowns.length ? evaluation.unknowns : ['Availability unknown'],
          suggested_next_step:
            evaluation.fit_label === 'strong'
              ? 'Recruiter review, then consider hiring-manager screen.'
              : 'Recruiter review recommended before advancing this candidate.'
        };
      });

    return {
      run_id: `demo_${Date.now()}`,
      status: 'complete',
      criteria,
      candidates: profiles,
      evaluations,
      ranked_shortlist: ranked,
      report: {
        summary_markdown: `Shortlist generated for ${request.job.title || 'the open role'} with ${ranked.length} candidates. Review strengths, gaps, unknowns, and approval notes before sharing.`,
        disclosure: DISCLOSURE
      },
      warnings: [
        {
          code: 'DEMO_FALLBACK',
          message: 'Backend API was unavailable, so deterministic local demo results are shown.'
        }
      ],
      approval: {
        status: 'pending',
        reviewer_notes: null
      }
    };
  }

  private extractCandidateSkills(profile: string): string[] {
    const knownSkills = ['Python', 'FastAPI', 'Angular', 'TypeScript', 'CrewAI', 'SQL', 'PostgreSQL', 'API design'];
    const lowerProfile = profile.toLowerCase();
    const matches = knownSkills.filter((skill) => lowerProfile.includes(skill.toLowerCase()));

    return matches.length ? matches : ['Needs recruiter review'];
  }
}
