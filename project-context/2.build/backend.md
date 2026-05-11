# Backend

## Scope

Implemented the Recruitment Assistant MVP backend with FastAPI endpoints and a sequential Application Crew for approved-data candidate sourcing, evaluation, and recommendations.

## Inputs

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `frontend/src/app/recruitment-api.service.ts`
- `frontend/src/app/recruitment.models.ts`

## Changes

- Added backend package under `backend/app/`.
- Added Pydantic schemas matching the Angular frontend contract.
- Added `CriteriaService`, `CandidateSourceService`, `RecruitmentWorkflowService`, and `ReportService`.
- Added Researcher, Evaluator, and Recommender agent classes plus CrewAI YAML descriptors and CrewAI crew factory.
- Added FastAPI routes:
  - `GET /health`
  - `POST /api/criteria/extract`
  - `POST /api/candidates/preview`
  - `POST /api/recommendations/run`
  - `POST /api/recommendations/{run_id}/approval`
- Added `backend/requirements.txt`, `backend/README.md`, and API smoke tests.

## Verification

- `PYTHONPATH=backend pytest -q backend/tests` passed.
- CrewAI crew factory import/build check passed with 3 agents and 3 tasks.

## Decisions

- MVP endpoints use deterministic backend-owned business logic for reliable local demos and tests.
- CrewAI agent/task definitions are present and can be used for future live LLM execution without changing frontend API contracts.
- Approval tracking is in memory for the mini-project.

## Handoff Notes

- Start the backend with `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
- The frontend is already configured for `http://localhost:8000`.
- Seeded dataset currently available: `backend_engineers`.

## Known Gaps

- In-memory run and approval storage will reset when the process restarts.
- Live CrewAI kickoff is not enabled by API routes yet; routes use deterministic services to avoid model credential requirements.
- Uploaded candidate data is accepted as plain text in JSON, not multipart file upload.
