# Backend Implementation Plan

## Scope

Implement the Recruitment Assistant backend for the MVP using a FastAPI API surface and a sequential Application Crew with Researcher, Evaluator, and Recommender responsibilities. The backend will support approved candidate inputs only: seeded data, pasted profiles, and uploaded plain text.

## Application Crew Implementation

- Researcher Agent: normalize approved candidate sources into candidate profiles with source labels and missing-data notes.
- Evaluator Agent: score candidates against required skills, preferred skills, experience, seniority, location, and evidence confidence.
- Recommender Agent: rank evaluated candidates and generate decision-support recommendations with disclosure language.
- CrewAI integration: include CrewAI agent/task configuration and an adapter-friendly crew module. MVP execution uses deterministic business logic so local demos and tests do not require an LLM API key.

## API Endpoints

- `GET /health`: health check for frontend availability checks.
- `POST /api/criteria/extract`: validate and normalize job requirements into reviewable criteria.
- `POST /api/candidates/preview`: return candidate profiles from approved seeded, pasted, or uploaded sources.
- `POST /api/recommendations/run`: execute the sequential Application Crew workflow and return structured recommendations.
- `POST /api/recommendations/{run_id}/approval`: record recruiter approval status and notes in memory for the MVP.

## Business Logic Components

- Criteria service: validates required fields, extracts ambiguities, and preserves recruiter-provided criteria.
- Candidate source service: searches seeded candidates, parses pasted profiles, parses uploaded plain text, and blocks unsupported sources.
- Recruitment workflow service: orchestrates Researcher, Evaluator, and Recommender steps, handles warnings, and stores run approvals.
- Report service: creates report-ready Markdown and required AI-assisted disclosure.
- Schemas: Pydantic models matching the Angular frontend contract.

## Implementation Approach

1. Create backend package structure under `backend/app/`.
2. Add Pydantic schemas and FastAPI routes matching frontend models.
3. Add deterministic candidate sourcing, evaluation, recommendation, and report services.
4. Add CrewAI agent/task definitions and YAML descriptors for the three-agent application crew.
5. Add dependency manifest and README run notes.
6. Verify by importing the app and exercising endpoints with FastAPI `TestClient` where dependencies are available.

## Status Tracking

| Item | Status | Notes |
| --- | --- | --- |
| Review PRD | Complete | Used `project-context/1.define/prd.md` for MVP scope and guardrails. |
| Review SAD | Complete | Used `project-context/2.build/sad.md` for FastAPI, schemas, and sequential crew shape. |
| Backend plan artifact | Complete | Initial implementation plan created before code changes and updated after verification. |
| Backend package scaffold | Complete | Added `backend/app` modules, `backend/requirements.txt`, backend README, and smoke tests. |
| Application Crew | Complete | Implemented Researcher, Evaluator, Recommender classes plus CrewAI YAML descriptors and a CrewAI `Crew` factory. |
| API endpoints | Complete | Implemented health, criteria, candidates, recommendations, and approval routes. |
| Verification | Complete | `PYTHONPATH=backend pytest -q backend/tests` passed; CrewAI factory created 3 agents and 3 tasks. |

## Assumptions

- MVP can use deterministic execution for local reliability while representing the required CrewAI agent roles in code.
- Full persistent audit logging is out of scope; in-memory approval and run storage is acceptable for the mini-project.
- Real candidate use still requires legal/HR approval and approved data handling outside this backend scaffold.

## Open Questions

- Whether live CrewAI LLM execution should be enabled for demos that have model credentials available.
- Whether uploaded text should remain inline JSON for MVP or later move to multipart file upload.

## Verification

- `PYTHONPATH=backend pytest -q backend/tests` passed with 2 tests.
- `PYTHONPATH=backend python - <<'PY' ... build_crewai_crew() ... PY` confirmed a CrewAI `Crew` with 3 agents and 3 tasks.

## Handoff Notes

- Frontend expects backend at `http://localhost:8000`.
- CORS should allow the Angular development server.
- Run locally with `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
