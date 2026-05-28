# Release Notes

## Version 1.0.0 - Initial Release

Initial local/demo release of the Recruitment Assistant MVP. This release completes the AAMAD Define, Build, and Deliver phases for a recruiter decision-support workflow using an Angular frontend, FastAPI backend, deterministic application crew services, optional live CrewAI execution, Docker Compose deployment configuration, structured logging, monitoring guidance, runbook, execution results, and lessons learned.

### Features

- Guided recruiter workflow for entering job title, description, required skills, preferred skills, seniority, and location or remote constraints.
- Evaluation criteria extraction and review checkpoint before candidate recommendations are generated.
- Candidate source support for seeded candidate data, pasted profiles, uploaded text, and approved-source style inputs.
- Deterministic Researcher Agent path that selects and normalizes candidates from approved inputs only.
- Deterministic Evaluator Agent path that compares candidates against job-related criteria and marks missing evidence as unknown.
- Deterministic Recommender Agent path that ranks candidates and produces recruiter-reviewable recommendations.
- Ranked shortlist with fit labels, numeric scores, rationale, strengths, gaps, unknowns, and suggested next steps.
- Hiring-manager-ready report summary with AI-assisted decision-support disclosure.
- Recruiter approval capture for recommendation runs.
- Safe handling for empty or incomplete candidate inputs, ambiguous criteria, low-confidence results, and missing data fields.
- FastAPI JSON API for health checks, criteria extraction, candidate preview, recommendation execution, and approval capture.
- Angular + PrimeNG frontend for the primary recruiter workflow.
- Structured backend logging for startup, shutdown, API requests, workflow execution, agent steps, approvals, and errors.
- Optional live CrewAI execution mode with CrewAI tracing configuration.
- Docker Compose deployment configuration for local workstation or demo VM operation.
- Operator runbook, monitoring plan, deployment plan, execution results, and lessons learned artifacts.

### Deployment

- Deployment method: Docker Compose on a local workstation or demo VM.
- Services:
  - `backend`: FastAPI/Uvicorn service built from the root `Dockerfile`, exposed on host port `8000` by default.
  - `frontend`: Angular production build served by nginx from `frontend/Dockerfile`, exposed on host port `4200` by default.
- Runtime configuration is provided through `.env`, copied from `.env.example`.
- Deterministic mode is the default release path and does not require LLM credentials.
- Optional live CrewAI mode requires valid provider credentials, model access, `RECRUITMENT_EXECUTION_MODE=crewai_live`, CrewAI login, and trace configuration.

How to deploy:

```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose ps
curl http://localhost:8000/health
curl http://localhost:4200/healthz
```

Open:

- Frontend: `http://localhost:4200`
- Backend OpenAPI docs: `http://localhost:8000/docs`

Use seeded dataset `backend_engineers` for the standard release smoke test. Stop the stack with:

```bash
docker compose down
```

### Known Issues

- Docker CLI is not installed in the current workspace, so container build/start/health verification must be run in a Docker-enabled environment.
- Recommendation runs and approvals are stored in backend memory only and are lost when the backend restarts.
- The frontend API base URL is currently built as `http://localhost:8000`; non-local deployments require runtime API URL externalization.
- Uploaded candidate data is accepted as plain text in JSON, not as multipart file upload with document parsing.
- Browser-click end-to-end automation is not installed; current verification covers backend API tests, frontend unit tests/build, and API smoke flow.
- Real candidate data use is not approved for this MVP without legal/HR review, retention policy, access controls, and audit requirements.
- Deterministic mode is the reliable default. Live CrewAI execution depends on external provider credentials, available model access, CrewAI login, and tracing setup.
- Persistent audit logging, database-backed run history, centralized log retention, alerting, and production access controls are not implemented in this release.

### Next Steps

- Run Docker Compose build, startup, health checks, and seeded recommendation smoke test in a Docker-enabled environment.
- Externalize frontend API base URL configuration before non-local or cloud deployment.
- Add browser end-to-end automation for seeded happy path, pasted profiles, uploaded text, backend-unavailable fallback, and approval capture.
- Add persistent run history and approval audit records before any production-like pilot.
- Define retention, access control, monitoring, alerting, and audit policies before processing real candidate data.
- Add centralized log collection and alert thresholds for error rate, latency, failed recommendation runs, and provider failures.
- Decide on a cloud target if the project moves beyond local/demo VM deployment.
- Add multipart upload and document parsing if resume file ingestion becomes in scope.
- Validate MVP workflow, terminology, output usefulness, and disclosure language with recruiters, hiring managers, or HR/talent operations stakeholders.

