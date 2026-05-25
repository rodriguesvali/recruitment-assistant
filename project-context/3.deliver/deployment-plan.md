# Deployment Plan: Recruitment Assistant

## Purpose

Prepare the Recruitment Assistant MVP for a repeatable Deliver-phase deployment that supports local demos and production-like validation without expanding beyond the approved PRD and Build-phase SAD.

## Deployment Approach

Primary approach: Docker Compose on a local workstation or demo VM.

The MVP is best deployed as two containers:

| Service | Runtime | Port | Purpose |
| --- | --- | --- | --- |
| `backend` | Python 3.12 + FastAPI/Uvicorn | `8000` | JSON API, deterministic Researcher/Evaluator/Recommender workflow, in-memory run approvals |
| `frontend` | Angular production build served by nginx | `4200` host to container `80` | Recruiter workflow UI |

This matches the Build-phase architecture while keeping deployment low-risk. A full cloud deployment is deferred until the team resolves persistent storage, runtime configuration, access control, and legal/HR approval for real candidate data.

## Required Dependencies And Environment Setup

Local Docker deployment requires:

- Docker Engine with Compose v2.
- Git checkout of this repository.
- Optional `.env` file copied from `.env.example` if model credentials or local overrides are needed.
- Open host ports `4200` and `8000`, or alternate `FRONTEND_PORT` and `BACKEND_PORT` values.

Local non-Docker development remains supported with:

- Python 3.11 or newer.
- Node.js 20 or newer; the devcontainer uses Node 24.
- npm using `frontend/package-lock.json`.
- Backend dependencies from `backend/requirements.txt`.

## Configuration Requirements

| Variable | Default | Required | Notes |
| --- | --- | --- | --- |
| `APP_ENV` | `docker` in Compose | No | Used to identify container runtime. |
| `BACKEND_PORT` | `8000` | No | Host port mapped to backend container port `8000`. |
| `FRONTEND_PORT` | `4200` | No | Host port mapped to frontend container port `80`. |
| `LOG_LEVEL` | `INFO` | No | Backend application log verbosity. |
| `LOG_FORMAT` | `json` | No | Backend log format; `json` is preferred for container logs, `text` is available for local debugging. |
| `RECRUITMENT_EXECUTION_MODE` | `deterministic` | No | Uses local deterministic agents by default. Set to `crewai_live` to make `/api/recommendations/run` execute `Crew.kickoff()` and emit CrewAI trace batches. |
| `CREWAI_TRACING_ENABLED` | `true` | No | Enables CrewAI AOP/AMP tracing for live Application Crew execution. Requires `crewai login` before traces appear in the dashboard. |
| `CREWAI_TELEMETRY_OPT_OUT` | `false` | No | Allows CrewAI tracing/telemetry for the requested monitored demo path. Set to `true` only when tracing must be disabled. |
| `GOOGLE_API_KEY` | empty | No for MVP | Deterministic API path does not require live LLM credentials. Required only if future live CrewAI execution is enabled. |
| `CREWAI_MODEL` | `gemini-3.1-pro-preview` | No for MVP | Present for future live CrewAI configuration. |
| `CREWAI_PROVIDER` | `google` | No for MVP | Present for future live CrewAI configuration. |

Current constraints:

- The frontend API base URL is currently built as `http://localhost:8000`, so the Docker demo maps backend port `8000` on the same host.
- Backend CORS allows the documented local frontend origins, including `http://localhost:4200`.
- The current backend uses in-memory run and approval storage, so no database is provisioned for this version.
- No database schema, migrations, or seed SQL are required for the current deterministic MVP runtime.
- PostgreSQL or another persistent store can be added later when the backend implements persisted run history and audit records.
- Real candidate data use requires legal/HR review, approved data handling, retention decisions, and access controls.

## Deployment Steps

1. Prepare configuration:

   ```bash
   cp .env.example .env
   ```

   Leave `GOOGLE_API_KEY` empty for the deterministic MVP demo path.

2. Build images:

   ```bash
   docker compose build
   ```

3. Start the stack:

   ```bash
   docker compose up -d
   ```

4. Verify health:

   ```bash
   docker compose ps
   curl http://localhost:8000/health
   curl http://localhost:4200/healthz
   ```

5. Open the application:

   - Frontend: `http://localhost:4200`
   - Backend OpenAPI docs: `http://localhost:8000/docs`

6. Run a seeded demo:

   - Enter a backend or full-stack role requirement.
   - Confirm criteria.
   - Select seeded dataset `backend_engineers`.
   - Run recommendations.
   - Review ranked candidates and save recruiter approval.

7. Stop the stack:

   ```bash
   docker compose down
   ```

## Rollback Procedures

Local rollback:

1. Stop the current stack:

   ```bash
   docker compose down
   ```

2. Return to the previous known-good Git commit or tag.

3. Rebuild and restart:

   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

4. Re-run health checks and the seeded recommendation smoke test.

Operational notes:

- No database migration rollback is required for the current MVP because runtime state is in memory.
- Any in-progress approvals are lost on backend restart; users should rerun the workflow after rollback.
- If a failed frontend image is the only issue, the backend can stay running while the frontend image is rebuilt.

## Status Tracking

| Item | Status | Notes |
| --- | --- | --- |
| Review PRD | Complete | Reviewed `project-context/1.define/prd.md`; deployment remains decision-support only and local/demo focused. |
| Review Build SAD | Complete | Reviewed `project-context/2.build/sad.md`; deployment matches Angular frontend plus FastAPI backend. |
| Review Build artifacts | Complete | Reviewed setup, backend, frontend, integration, QA, and architecture Build artifacts. |
| Select deployment approach | Complete | Chose Docker Compose local/demo deployment as the primary Deliver path. |
| Add backend Dockerfile | Complete | Root `Dockerfile` builds the FastAPI service and exposes `/health`. |
| Add frontend Dockerfile | Complete | `frontend/Dockerfile` builds Angular and serves static assets with nginx. |
| Add Compose config | Complete | `docker-compose.yml` runs backend and frontend with health checks. |
| Remove unused PostgreSQL provisioning | Complete | Removed PostgreSQL from deployment and devcontainer because the current backend does not consume a database. |
| Add Docker ignore rules | Complete | `.dockerignore` excludes local envs, build outputs, node modules, and secrets. |
| Verify Compose/config build | Blocked | Docker CLI is not installed in this workspace; `docker compose config` returned `docker: command not found`. |
| Verify backend tests | Complete | `PYTHONPATH=backend pytest -q backend/tests` passed with 5 tests. |
| Verify frontend build | Complete | `npm run build` from `frontend/` passed. |
| Add monitoring and logging plan | Complete | Added `project-context/3.deliver/monitoring-plan.md` with logging, viewing, tracing, and status details. |
| Enable CrewAI AOP/AMP trace collection | Complete | Operator ran `crewai login`; `crewai traces enable` succeeded; `CREWAI_TRACING_ENABLED=true crewai traces status` reports enabled. |
| Cloud deployment decision | Deferred | Requires runtime API URL externalization, access controls, persistence, monitoring, and legal/HR review. |

## Sources

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `project-context/2.build/setup.md`
- `project-context/2.build/backend.md`
- `project-context/2.build/frontend.md`
- `project-context/2.build/integration-plan.md`
- `project-context/2.build/qa-plan.md`
- `.devcontainer/Dockerfile`
- `.devcontainer/docker-compose.yml`

## Assumptions

- The first Deliver target is a local or demo VM deployment, not a production hiring workflow.
- Deterministic backend services remain the MVP execution path.
- Docker Compose is acceptable for this delivery milestone.
- The current host can expose ports `4200` and `8000`.
- Database-backed persistence is intentionally excluded from this version until the backend implements it.

## Open Questions

- Should the frontend API base URL be made runtime-configurable before any non-local deployment?
- Which cloud target, if any, should be prepared after local Docker validation?
- What retention, access control, and audit requirements apply before real candidate data is used?
- Should persistent run history be implemented before a production-like pilot?
- If persistence is approved later, should the backend use PostgreSQL with SQLAlchemy/SQLModel and migrations?

## Verification

Container verification is blocked in this workspace because Docker is not installed:

- `docker compose config` could not run: `docker: command not found`.

Run these checks in a Docker-enabled environment:

- `docker compose build`
- `docker compose up -d`
- `curl http://localhost:8000/health`
- `curl http://localhost:4200/healthz`
- Seeded recommendation smoke test through the UI or API.

Available non-container verification passed on 2026-05-18:

- `PYTHONPATH=backend pytest -q backend/tests`: passed with 5 tests.
- `npm run build` from `frontend/`: passed.

## Handoff Notes

- Use this plan for Deliver-phase local/demo packaging.
- Keep `.env` local and out of version control.
- Do not position this deployment as production-ready for real candidate workflows until compliance, persistence, access, monitoring, and rollback requirements are approved.
- A separate backend implementation task is required before runs, approvals, or audit records are persisted in any database.
