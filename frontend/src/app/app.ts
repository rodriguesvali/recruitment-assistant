import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { KeyValuePipe } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { CheckboxModule } from 'primeng/checkbox';
import { DrawerModule } from 'primeng/drawer';
import { InputNumberModule } from 'primeng/inputnumber';
import { InputTextModule } from 'primeng/inputtext';
import { MessageModule } from 'primeng/message';
import { ProgressBarModule } from 'primeng/progressbar';
import { RadioButtonModule } from 'primeng/radiobutton';
import { SelectModule } from 'primeng/select';
import { TableModule } from 'primeng/table';
import { TabsModule } from 'primeng/tabs';
import { TagModule } from 'primeng/tag';
import { TextareaModule } from 'primeng/textarea';
import { TooltipModule } from 'primeng/tooltip';
import {
  ApprovalStatus,
  CandidateProfile,
  CandidateSource,
  EvaluationCriteria,
  JobRequirement,
  RankedRecommendation,
  RecruitmentRunResult,
  RunStatus,
  WorkflowRequest
} from './recruitment.models';
import { RecruitmentApiService } from './recruitment-api.service';

@Component({
  selector: 'app-root',
  imports: [
    ReactiveFormsModule,
    KeyValuePipe,
    ButtonModule,
    CardModule,
    CheckboxModule,
    DrawerModule,
    InputNumberModule,
    InputTextModule,
    MessageModule,
    ProgressBarModule,
    RadioButtonModule,
    SelectModule,
    TableModule,
    TabsModule,
    TagModule,
    TextareaModule,
    TooltipModule
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly api = inject(RecruitmentApiService);
  private recommendationRunId = 0;

  readonly backendOnline = signal<boolean | null>(null);
  readonly criteria = signal<EvaluationCriteria | null>(null);
  readonly candidates = signal<CandidateProfile[]>([]);
  readonly previewWarnings = signal<string[]>([]);
  readonly runResult = signal<RecruitmentRunResult | null>(null);
  readonly runStatus = signal<RunStatus>('idle');
  readonly selectedCandidate = signal<CandidateProfile | null>(null);
  readonly selectedRecommendation = signal<RankedRecommendation | null>(null);
  readonly detailOpen = signal(false);
  readonly errorMessage = signal('');

  readonly sourceTypes = [
    { label: 'Seeded dataset', value: 'seeded' },
    { label: 'Pasted profiles', value: 'pasted' },
    { label: 'Uploaded text', value: 'uploaded' }
  ];

  readonly datasetOptions = [
    { label: 'Backend engineers', value: 'backend_engineers' }
  ];

  readonly seniorityOptions = [
    { label: 'Entry-level', value: 'Entry-level' },
    { label: 'Mid-level', value: 'Mid-level' },
    { label: 'Senior', value: 'Senior' },
    { label: 'Staff+', value: 'Staff+' }
  ];

  readonly approvalOptions: { label: string; value: ApprovalStatus }[] = [
    { label: 'Approved', value: 'approved' },
    { label: 'Needs edits', value: 'needs_edits' },
    { label: 'Rejected', value: 'rejected' }
  ];

  readonly jobForm = this.fb.nonNullable.group({
    title: ['Backend Engineer', [Validators.required, Validators.minLength(3)]],
    description: [
      'Build APIs and AI-assisted recruiting workflows. The role requires clean service design, structured outputs, and reliable integrations.',
      [Validators.required, Validators.minLength(30)]
    ],
    requiredSkills: ['Python, FastAPI, API design', Validators.required],
    preferredSkills: ['CrewAI, PostgreSQL, Angular'],
    seniority: ['Mid-level', Validators.required],
    location: ['Remote US'],
    maxCandidates: [5, [Validators.required, Validators.min(1), Validators.max(10)]]
  });

  readonly sourceForm = this.fb.nonNullable.group({
    type: ['seeded', Validators.required],
    datasetId: ['backend_engineers'],
    pastedProfiles: [
      'Avery Chen: Python, FastAPI, CrewAI, PostgreSQL. Built API services and LLM workflow tools.\n\nJordan Patel: Angular, TypeScript, Python, FastAPI. Built recruiter dashboards and ATS integrations.'
    ],
    uploadedText: ['']
  });

  readonly reviewForm = this.fb.nonNullable.group({
    criteriaConfirmed: [false, Validators.requiredTrue]
  });

  readonly approvalForm = this.fb.nonNullable.group({
    status: ['needs_edits' as ApprovalStatus, Validators.required],
    reviewerNotes: ['']
  });

  readonly progressValue = computed(() => {
    const status = this.runStatus();
    const statusProgress: Record<RunStatus, number> = {
      idle: 0,
      validating: 18,
      researching: 40,
      evaluating: 66,
      recommending: 86,
      complete: 100,
      failed: 100
    };

    return statusProgress[status];
  });

  readonly activeStep = computed(() => {
    const result = this.runResult();

    if (result) {
      return result.approval.status === 'pending' ? 5 : 6;
    }

    if (this.candidates().length) {
      return 4;
    }

    if (this.criteria()) {
      return 2;
    }

    return 1;
  });

  ngOnInit(): void {
    this.api.checkBackend().subscribe((online) => this.backendOnline.set(online));
  }

  get sourceType(): string {
    return this.sourceForm.controls.type.value;
  }

  get selectedEvaluation() {
    const recommendation = this.selectedRecommendation();

    if (!recommendation) {
      return null;
    }

    return this.runResult()?.evaluations.find((evaluation) => evaluation.candidate_id === recommendation.candidate_id) ?? null;
  }

  buildJob(): JobRequirement {
    const value = this.jobForm.getRawValue();

    return {
      title: value.title.trim(),
      description: value.description.trim(),
      required_skills: this.toList(value.requiredSkills),
      preferred_skills: this.toList(value.preferredSkills),
      seniority: value.seniority,
      location: value.location.trim()
    };
  }

  buildSource(): CandidateSource {
    const value = this.sourceForm.getRawValue();

    return {
      type: value.type as CandidateSource['type'],
      dataset_id: value.type === 'seeded' ? value.datasetId : null,
      pasted_profiles: value.type === 'pasted' ? value.pastedProfiles : null,
      uploaded_text: value.type === 'uploaded' ? value.uploadedText : null
    };
  }

  extractCriteria(): void {
    this.errorMessage.set('');

    if (this.jobForm.invalid) {
      this.jobForm.markAllAsTouched();
      this.errorMessage.set('Add a role title, useful description, and required skills before reviewing criteria.');
      return;
    }

    this.runStatus.set('validating');
    this.api.extractCriteria(this.buildJob()).subscribe({
      next: (criteria) => {
        this.criteria.set(criteria);
        this.candidates.set([]);
        this.previewWarnings.set([]);
        this.runResult.set(null);
        this.reviewForm.controls.criteriaConfirmed.setValue(criteria.ambiguities.length === 0);
        this.runStatus.set('idle');
        this.scrollToSection('criteria-review');
      },
      error: () => this.fail('Criteria extraction failed. Check the backend or revise the job input.')
    });
  }

  previewCandidates(): void {
    const criteria = this.criteria();

    if (!criteria) {
      this.errorMessage.set('Review and confirm criteria before previewing candidates.');
      return;
    }

    if (this.reviewForm.invalid) {
      this.reviewForm.markAllAsTouched();
      this.errorMessage.set('Confirm the criteria checkpoint before candidate preview.');
      return;
    }

    this.errorMessage.set('');
    this.previewWarnings.set([]);
    this.runStatus.set('researching');
    this.api.previewCandidates({ ...criteria, confirmed_by_recruiter: true }, this.buildSource()).subscribe({
      next: (response) => {
        this.candidates.set(response.candidates);
        this.previewWarnings.set(response.warnings.map((warning) => warning.message));
        this.runResult.set(null);
        this.runStatus.set('idle');
        this.scrollToSection(response.candidates.length ? 'candidate-preview' : 'candidate-source-warnings');
      },
      error: () => this.fail('Candidate preview failed. Try seeded data or revise pasted profiles.')
    });
  }

  runWorkflow(): void {
    const criteria = this.criteria();

    if (!criteria || this.candidates().length === 0) {
      this.errorMessage.set('Complete criteria review and candidate preview before running recommendations.');
      return;
    }

    const request: WorkflowRequest = {
      job: this.buildJob(),
      criteria: { ...criteria, confirmed_by_recruiter: true },
      candidate_source: this.buildSource(),
      options: {
        max_candidates: this.jobForm.controls.maxCandidates.value,
        score_style: 'numeric_and_label',
        require_recruiter_checkpoints: true
      }
    };

    const runId = ++this.recommendationRunId;

    this.errorMessage.set('');
    this.runStatus.set('evaluating');
    window.setTimeout(() => {
      if (this.recommendationRunId === runId && this.runStatus() === 'evaluating') {
        this.runStatus.set('recommending');
      }
    }, 450);

    this.api.runRecommendations(request, this.candidates()).subscribe({
      next: (result) => {
        this.runResult.set(result);
        this.approvalForm.patchValue({
          status: result.approval.status === 'pending' ? 'needs_edits' : result.approval.status,
          reviewerNotes: result.approval.reviewer_notes ?? ''
        });
        this.runStatus.set('complete');
        this.scrollToSection('ranked-shortlist');
      },
      error: () => this.fail('Recommendation workflow failed. Preserve your inputs and retry.')
    });
  }

  openDetails(recommendation: RankedRecommendation): void {
    const candidate =
      this.runResult()?.candidates.find((profile) => profile.candidate_id === recommendation.candidate_id) ?? null;
    this.selectedCandidate.set(candidate);
    this.selectedRecommendation.set(recommendation);
    this.detailOpen.set(true);
  }

  recordApproval(): void {
    const result = this.runResult();

    if (!result) {
      return;
    }

    const approval = {
      status: this.approvalForm.controls.status.value,
      reviewer_notes: this.approvalForm.controls.reviewerNotes.value.trim() || null
    };

    this.api.recordApproval(result.run_id, approval).subscribe((savedApproval) => {
      this.runResult.set({
        ...result,
        approval: savedApproval
      });
    });
  }

  severityForFit(fit: string): 'success' | 'info' | 'warn' | 'danger' {
    if (fit === 'strong') {
      return 'success';
    }

    if (fit === 'moderate') {
      return 'info';
    }

    return 'warn';
  }

  approvalSeverity(status: ApprovalStatus): 'success' | 'info' | 'warn' | 'danger' {
    const severities: Record<ApprovalStatus, 'success' | 'info' | 'warn' | 'danger'> = {
      approved: 'success',
      needs_edits: 'warn',
      rejected: 'danger',
      pending: 'info'
    };

    return severities[status];
  }

  private fail(message: string): void {
    this.recommendationRunId++;
    this.runStatus.set('failed');
    this.errorMessage.set(message);
  }

  private scrollToSection(id: string): void {
    window.setTimeout(() => {
      document.getElementById(id)?.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }, 0);
  }

  private toList(value: string): string[] {
    return value
      .split(',')
      .map((item) => item.trim())
      .filter(Boolean);
  }
}
