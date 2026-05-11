# Integration Plan: Recruitment Assistant

## Scope

Integrate the Angular + PrimeNG recruiter interface with the FastAPI recruitment backend so a recruiter can move from job input to criteria review, candidate preview, ranked recommendations, approval capture, and report preview using approved candidate data only.

## Sources

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `project-context/2.build/frontend-plan.md`
- `project-context/2.build/backend-plan.md`
- `frontend/src/app/recruitment-api.service.ts`
- `backend/app/api/routes.py`

## Frontend-Backend Integration

| Flow | Frontend component/state | Backend endpoint | Status | Notes |
| --- | --- | --- | --- | --- |
| Backend availability | `RecruitmentApiService.checkBackend()` | `GET /health` | Complete | UI shows backend online or demo fallback. |
| Criteria extraction | `extractCriteria()` | `POST /api/criteria/extract` | Complete | Returns normalized `EvaluationCriteria` and ambiguity warnings. |
| Criteria checkpoint | `reviewForm.criteriaConfirmed` | Included in workflow `criteria` payload | Complete | Confirmed criteria now travels into the run request and response. |
| Candidate preview | `previewCandidates()` | `POST /api/candidates/preview` | Complete | Returns candidate profiles and source warnings. |
| Recommendation run | `runWorkflow()` | `POST /api/recommendations/run` | Complete | Runs Researcher, Evaluator, and Recommender sequence through backend workflow service. |
| Approval capture | `recordApproval()` | `POST /api/recommendations/{run_id}/approval` | Complete | Saves MVP in-memory approval status and reviewer notes. |
| Report preview | `runResult.report` | Workflow response | Complete | Shows report summary and required AI-assisted disclosure. |

## API Connection Setup

- Default API base URL: `http://localhost:8000`.
- Backend CORS allows Angular dev origins:
  - `http://localhost:4200`
  - `http://127.0.0.1:4200`
  - `http://localhost:5173`
  - `http://127.0.0.1:5173`
- Backend local run command: `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
- Frontend local run command: `cd frontend && npm start`.
- Root launchers:
  - Backend: `./scripts/start-backend.sh`
  - Frontend: `./scripts/start-frontend.sh`
  - Full stack: `./scripts/start-dev.sh`
- VS Code launchers:
  - Task `Backend: FastAPI`
  - Task `Frontend: Angular`
  - Task `Full stack: Frontend + Backend`
  - Debug compound `Full stack: Frontend + Backend`
- Frontend falls back to deterministic local demo data if API calls fail, preserving demo usability while making backend availability visible.

## External Service Integrations

No external ATS, email, LinkedIn, SMS, calendar, HRIS, payroll, or scraping integrations are enabled for the MVP.

Approved MVP candidate sources:

- Seeded backend datasets.
- Recruiter-pasted candidate profile text.
- Uploaded plain text represented as approved text content in the API payload.

CrewAI role metadata and optional crew factory are present, but the current integrated MVP uses deterministic backend execution so local verification does not require LLM credentials.

## Configuration Needed

| Area | Current configuration | Status |
| --- | --- | --- |
| Backend dependencies | `backend/requirements.txt` | Complete |
| Frontend dependencies | `frontend/package-lock.json` | Complete |
| API URL | Frontend service constant set to `http://localhost:8000` | Complete for local MVP |
| CORS | FastAPI middleware configured for local frontend ports | Complete |
| Launch scripts | Root scripts for backend, frontend, and full-stack execution | Complete |
| VS Code launchers | Tasks and debug compound for local execution | Complete |
| Secrets | None required for deterministic MVP | Complete |
| Persistence | In-memory run and approval storage | Complete for mini-project |

## Testing Approach

1. Backend API smoke tests with FastAPI `TestClient`.
2. Frontend unit tests through Angular/Vitest.
3. Frontend production build check.
4. Manual or scripted local smoke test with backend server running:
   - Health check succeeds.
   - Criteria extraction returns reviewable criteria.
   - Candidate preview returns approved-source profiles.
   - Recommendation run returns ranked shortlist, report disclosure, and `confirmed_by_recruiter`.
   - Approval endpoint records reviewer decision.
5. QA follow-up should add browser e2e coverage for seeded, pasted, uploaded-text, empty-source, and backend-unavailable fallback paths.

## Status Tracking

| Task | Status | Notes |
| --- | --- | --- |
| Review PRD | Complete | MVP scope, approved data sources, and human approval requirements identified. |
| Review SAD | Complete | FastAPI, sequential workflow, schemas, and error handling reviewed. |
| Review frontend plan | Complete | Angular + PrimeNG flow and endpoint expectations reviewed. |
| Review backend plan | Complete | Endpoint and workflow implementation approach reviewed. |
| Create integration plan | Complete | This artifact created in `project-context/2.build/integration-plan.md`. |
| Align API contracts | Complete | Frontend and backend models share endpoint names and snake_case payload contracts. |
| Wire criteria checkpoint into run | Complete | `WorkflowRequest.criteria` added and sent from frontend after recruiter confirmation. |
| Wire candidate preview warnings | Complete | Frontend now preserves and displays backend preview warnings. |
| Wire uploaded plain text | Complete | Frontend sends `uploaded_text` to existing backend parser. |
| Add launchers | Complete | Added root scripts and VS Code task/debug launchers for backend, frontend, and full-stack execution. |
| Verify backend | Complete | `PYTHONPATH=backend pytest -q backend/tests` passed. |
| Verify frontend tests | Complete | `npm test -- --watch=false` passed. |
| Verify frontend build | Complete | `npm run build` passed. |
| End-to-end local server smoke | Complete | Restarted backend on `8000` with the updated code and exercised the live HTTP flow. |

## Assumptions

- The MVP can use deterministic scoring and recommendation logic while keeping CrewAI agent roles represented in the backend.
- `uploaded_text` is approved text content supplied by the recruiter or UI, not automatic PDF/DOCX parsing.
- In-memory run storage is sufficient for this module demo and is not production audit logging.
- Frontend demo fallback is acceptable when the backend is offline, as long as the UI clearly marks fallback mode.

## Open Questions

- Should the API base URL become environment-driven before delivery, or is the local constant acceptable for the module demo?
- Should frontend expose seeded dataset discovery from the backend instead of maintaining a static dataset option list?
- What legal/HR-approved disclosure text should replace the MVP placeholder before real candidate use?

## Verification

- Backend: `PYTHONPATH=backend pytest -q backend/tests`
- Frontend tests: `npm test -- --watch=false`
- Frontend build: `npm run build`
- Live HTTP smoke: `POST /api/recommendations/run` preserved `confirmed_by_recruiter: true`, returned a ranked shortlist and disclosure, `POST /api/recommendations/{run_id}/approval` saved approval notes, and `POST /api/candidates/preview` parsed uploaded plain text.

## Handoff Notes

- Integration is ready for QA browser smoke testing against the local backend.
- QA should validate that recruiter confirmation appears in the final run response and that approval state updates after saving.
- DevOps should document environment-specific API URL handling before any deployed demo beyond localhost.
