export type SourceType = 'seeded' | 'pasted' | 'uploaded';
export type RunStatus = 'idle' | 'validating' | 'researching' | 'evaluating' | 'recommending' | 'complete' | 'failed';
export type ApprovalStatus = 'pending' | 'approved' | 'rejected' | 'needs_edits';

export interface JobRequirement {
  title: string;
  description: string;
  required_skills: string[];
  preferred_skills: string[];
  seniority: string;
  location: string;
}

export interface EvaluationCriteria extends JobRequirement {
  ambiguities: string[];
  confirmed_by_recruiter: boolean;
}

export interface CandidateSource {
  type: SourceType;
  dataset_id?: string | null;
  pasted_profiles?: string | null;
  uploaded_text?: string | null;
}

export interface WorkflowWarning {
  code: string;
  message: string;
}

export interface CandidateProfile {
  candidate_id: string;
  display_name: string;
  profile_summary: string;
  skills: string[];
  experience: string[];
  location: string;
  source_labels: string[];
  missing_data: string[];
}

export interface CandidateEvaluation {
  candidate_id: string;
  fit_label: 'strong' | 'moderate' | 'low';
  overall_score: number;
  component_scores: Record<string, number>;
  strengths: string[];
  gaps: string[];
  unknowns: string[];
  rationale: string;
}

export interface RankedRecommendation {
  rank: number;
  candidate_id: string;
  display_name: string;
  fit_label: 'strong' | 'moderate' | 'low';
  overall_score: number;
  recommendation_rationale: string;
  strengths: string[];
  gaps: string[];
  unknowns: string[];
  suggested_next_step: string;
}

export interface RecruiterApproval {
  status: ApprovalStatus;
  reviewer_notes: string | null;
}

export interface RecruitmentRunResult {
  run_id: string;
  status: RunStatus;
  criteria: EvaluationCriteria;
  candidates: CandidateProfile[];
  evaluations: CandidateEvaluation[];
  ranked_shortlist: RankedRecommendation[];
  report: {
    summary_markdown: string;
    disclosure: string;
  };
  warnings: WorkflowWarning[];
  approval: RecruiterApproval;
}

export interface WorkflowRequest {
  job: JobRequirement;
  criteria?: EvaluationCriteria;
  candidate_source: CandidateSource;
  options: {
    max_candidates: number;
    score_style: 'numeric_and_label';
    require_recruiter_checkpoints: boolean;
  };
}

export interface CandidatePreviewResponse {
  candidates: CandidateProfile[];
  warnings: WorkflowWarning[];
}
