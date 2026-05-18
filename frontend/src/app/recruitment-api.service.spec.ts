import { HttpErrorResponse, provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { vi } from 'vitest';
import { RecruitmentApiService } from './recruitment-api.service';
import {
  CandidateSource,
  EvaluationCriteria,
  JobRequirement,
  RecruiterApproval,
  WorkflowRequest,
} from './recruitment.models';

describe('RecruitmentApiService', () => {
  let service: RecruitmentApiService;
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RecruitmentApiService, provideHttpClient(), provideHttpClientTesting()],
    });

    service = TestBed.inject(RecruitmentApiService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    http.verify({ ignoreCancelled: true });
    vi.useRealTimers();
  });

  it('uses demo fallback when the backend is unreachable before an HTTP response', async () => {
    vi.useFakeTimers();
    let result: EvaluationCriteria | undefined;

    service.extractCriteria(createJob()).subscribe((criteria) => {
      result = criteria;
    });

    const request = http.expectOne('http://localhost:8000/api/criteria/extract');
    request.error(new ProgressEvent('error'), { status: 0, statusText: 'Unknown Error' });
    await vi.advanceTimersByTimeAsync(350);

    expect(result?.title).toBe('Backend Engineer');
    expect(result?.confirmed_by_recruiter).toBe(false);
  });

  it('uses demo fallback when the backend request times out before an HTTP response', async () => {
    vi.useFakeTimers();
    let result: RecruiterApproval | undefined;
    const approval: RecruiterApproval = {
      status: 'approved',
      reviewer_notes: 'Looks good.',
    };

    service.recordApproval('run-1', approval).subscribe((savedApproval) => {
      result = savedApproval;
    });

    http.expectOne('http://localhost:8000/api/recommendations/run-1/approval');
    await vi.advanceTimersByTimeAsync(10250);

    expect(result).toEqual(approval);
  });

  it('propagates backend validation errors instead of converting them to fallback criteria', () => {
    let error: HttpErrorResponse | undefined;

    service.extractCriteria(createJob()).subscribe({
      error: (raisedError: HttpErrorResponse) => {
        error = raisedError;
      },
    });

    const request = http.expectOne('http://localhost:8000/api/criteria/extract');
    request.flush(
      { detail: 'title is required' },
      { status: 422, statusText: 'Unprocessable Entity' },
    );

    expect(error?.status).toBe(422);
    expect(error?.error).toEqual({ detail: 'title is required' });
  });

  it('propagates backend server errors instead of converting them to fallback recommendations', () => {
    let error: HttpErrorResponse | undefined;

    service.runRecommendations(createWorkflowRequest(), []).subscribe({
      error: (raisedError: HttpErrorResponse) => {
        error = raisedError;
      },
    });

    const request = http.expectOne('http://localhost:8000/api/recommendations/run');
    request.flush(
      { detail: 'workflow failed' },
      { status: 500, statusText: 'Internal Server Error' },
    );

    expect(error?.status).toBe(500);
    expect(error?.error).toEqual({ detail: 'workflow failed' });
  });

  it('keeps the current candidate preview fallback message for legitimate fallback', async () => {
    vi.useFakeTimers();
    let result: { warnings: { message: string }[] } | undefined;

    service.previewCandidates(createCriteria(), createSource()).subscribe((response) => {
      result = response;
    });

    const request = http.expectOne('http://localhost:8000/api/candidates/preview');
    request.error(new ProgressEvent('error'), { status: 0, statusText: 'Unknown Error' });
    await vi.advanceTimersByTimeAsync(450);

    expect(result?.warnings[0].message).toBe(
      'Backend API was unavailable, so deterministic local candidate preview is shown.',
    );
  });
});

function createJob(): JobRequirement {
  return {
    title: 'Backend Engineer',
    description: 'Build APIs and reliable recruiting workflows.',
    required_skills: ['Python', 'FastAPI'],
    preferred_skills: ['CrewAI'],
    seniority: 'Mid-level',
    location: 'Remote US',
  };
}

function createCriteria(): EvaluationCriteria {
  return {
    ...createJob(),
    ambiguities: [],
    confirmed_by_recruiter: true,
  };
}

function createSource(): CandidateSource {
  return {
    type: 'seeded',
    dataset_id: 'backend_engineers',
  };
}

function createWorkflowRequest(): WorkflowRequest {
  return {
    job: createJob(),
    criteria: createCriteria(),
    candidate_source: createSource(),
    options: {
      max_candidates: 3,
      score_style: 'numeric_and_label',
      require_recruiter_checkpoints: true,
    },
  };
}
