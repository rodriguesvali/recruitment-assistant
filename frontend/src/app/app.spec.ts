import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { App } from './app';
import { RecruitmentApiService } from './recruitment-api.service';
import { RecruitmentRunResult } from './recruitment.models';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [
        {
          provide: RecruitmentApiService,
          useValue: {
            checkBackend: () => of(false)
          }
        }
      ]
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render title', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('AI-assisted shortlist review');
  });

  it('keeps the workflow on Run while approval is pending', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    app.runResult.set(createRunResult('pending'));

    expect(app.activeStep()).toBe(5);
  });

  it('activates Approval after approval is recorded', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;

    app.runResult.set(createRunResult('approved'));

    expect(app.activeStep()).toBe(6);
  });
});

function createRunResult(status: RecruitmentRunResult['approval']['status']): RecruitmentRunResult {
  return {
    run_id: 'run-1',
    status: 'complete',
    criteria: {
      title: 'Backend Engineer',
      description: 'Build APIs and reliable recruiting workflows.',
      required_skills: ['Python'],
      preferred_skills: ['Angular'],
      seniority: 'Mid-level',
      location: 'Remote',
      ambiguities: [],
      confirmed_by_recruiter: true
    },
    candidates: [],
    evaluations: [],
    ranked_shortlist: [],
    report: {
      summary_markdown: 'Ready for recruiter review.',
      disclosure: 'AI-assisted recommendation.'
    },
    warnings: [],
    approval: {
      status,
      reviewer_notes: null
    }
  };
}
