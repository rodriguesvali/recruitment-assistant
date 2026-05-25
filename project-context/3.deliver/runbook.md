# Runbook: Recruitment Assistant

## Purpose

This runbook explains how to install, configure, run, monitor, troubleshoot, stop, restart, and health-check the Recruitment Assistant MVP.

Primary audience: an operator, reviewer, or engineer who has not worked on the project before.

Primary deployment target: Docker Compose on a local workstation or demo VM.

This MVP is not production-ready for real hiring workflows. Use seeded or explicitly approved candidate data only. Real candidate data requires legal/HR approval, access controls, retention decisions, and audit requirements before pilot or launch.

## Application Overview

The Recruitment Assistant is an AI-assisted recruiter workflow that turns job requirements and approved candidate data into a ranked shortlist with rationale, strengths, gaps, unknowns, confidence signals, suggested next steps, and an AI-assisted disclosure.

The application has two services:

| Service | Runtime | Default URL | Purpose |
| --- | --- | --- | --- |
| Backend | Python 3.12, FastAPI, Uvicorn | `http://localhost:8000` | API, criteria extraction, candidate preview, recommendation workflow, approvals, logs, health check |
| Frontend | Angular production build served by nginx | `http://localhost:4200` | Recruiter-facing UI for entering jobs, reviewing candidates, running recommendations, and approving results |

The backend supports the MVP Researcher -> Evaluator -> Recommender flow:

1. Validate or extract job criteria.
2. Load candidates from an approved source.
3. Evaluate candidates against the criteria.
4. Rank and summarize candidate recommendations.
5. Require recruiter review and approval before use.

Default execution mode is deterministic and does not require live LLM credentials. Optional live CrewAI execution is available with `RECRUITMENT_EXECUTION_MODE=crewai_live`, a valid provider key, and CrewAI tracing setup.

## Prerequisites And Dependencies

### Docker Runtime

Use this path for normal demo operation.

- Git checkout of this repository.
- Docker Engine with Docker Compose v2.
- Host ports `4200` and `8000` available, or alternate port values in `.env`.
- Optional `.env` copied from `.env.example`.

### Local Development Runtime

Use this path when running without Docker.

- Python 3.11 or newer. The Docker image uses Python 3.12.
- Node.js 20 or newer. The frontend Docker build uses Node 24.
- npm with `frontend/package-lock.json`.
- Backend dependencies from `backend/requirements.txt`.

### Optional Live CrewAI Runtime

Only needed when testing live CrewAI execution and trace collection.

- CrewAI CLI installed in the environment.
- `crewai login` completed on the host where live execution runs.
- `crewai traces enable` completed if trace collection is desired.
- Valid `GOOGLE_API_KEY` and a `CREWAI_MODEL` available to that key.

## Installation

### Docker Compose Installation

From the repository root:

```bash
cp .env.example .env
docker compose build
```

For the deterministic MVP demo path, leave `GOOGLE_API_KEY` empty.

### Local Backend Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Local Frontend Installation

```bash
cd frontend
npm ci
```

## Configuration

Configuration is read from environment variables. For Docker Compose, put local values in `.env`. Do not commit `.env` or secrets.

| Variable | Default | Required | Used By | Notes |
| --- | --- | --- | --- | --- |
| `APP_NAME` | `Recruitment Assistant` | No | Local env | Human-readable app name. |
| `APP_ENV` | `development` locally, `docker` in Compose | No | Backend | Appears in startup logs. |
| `BACKEND_PORT` | `8000` | No | Compose and scripts | Host port for the backend. The container still listens on `8000`. |
| `FRONTEND_PORT` | `4200` | No | Compose and scripts | Host port for the frontend. The frontend container listens on `80`. |
| `BACKEND_HOST` | `0.0.0.0` | No | Local script | Host binding for `scripts/start-backend.sh`. |
| `FRONTEND_HOST` | `0.0.0.0` | No | Local script | Host binding for `scripts/start-frontend.sh`. |
| `LOG_LEVEL` | `INFO` | No | Backend | Use `DEBUG` only for local troubleshooting. |
| `LOG_FORMAT` | `json` | No | Backend | Use `json` for Docker logs and `text` for local readability. |
| `RECRUITMENT_EXECUTION_MODE` | `deterministic` | No | Backend | Set to `crewai_live` to call `Crew.kickoff()`. |
| `CREWAI_TRACING_ENABLED` | `true` | No | Backend live CrewAI | Enables tracing on live CrewAI crews. |
| `CREWAI_TELEMETRY_OPT_OUT` | `false` | No | CrewAI | Set to `true` only when tracing/telemetry must be disabled. |
| `CREWAI_MODEL` | `gemini-3.1-pro-preview` | No for deterministic mode | Live CrewAI | Must be valid for the configured provider/key when live mode is enabled. |
| `CREWAI_PROVIDER` | `google` | No for deterministic mode | Live CrewAI | Provider marker for future/live CrewAI configuration. |
| `GOOGLE_API_KEY` | empty | No for deterministic mode | Live CrewAI | Required only for live CrewAI execution with Google GenAI. |

Current runtime constraints:

- The frontend expects the backend at `http://localhost:8000`.
- Backend CORS allows documented local frontend origins, including `http://localhost:4200`.
- Recommendation runs and approvals are stored in backend memory only.
- Restarting the backend clears in-memory run and approval state.
- No database, migration, or seed SQL is required for the current MVP.

## Run The Application

### Start With Docker Compose

```bash
docker compose up -d
```

Open:

- Frontend: `http://localhost:4200`
- Backend health: `http://localhost:8000/health`
- Backend OpenAPI docs: `http://localhost:8000/docs`

### Start Locally Without Docker

Use two terminals from the repository root.

Terminal 1:

```bash
scripts/start-backend.sh
```

Terminal 2:

```bash
scripts/start-frontend.sh
```

Or start both together:

```bash
scripts/start-dev.sh
```

The combined script stops both child processes when it exits.

## Seeded Demo Procedure

Use this path to verify the core MVP workflow without live LLM credentials.

1. Start the application.
2. Open `http://localhost:4200`.
3. Enter a backend or full-stack role requirement.
4. Confirm extracted criteria in the UI.
5. Select seeded candidate data.
6. Use dataset `backend_engineers`.
7. Run recommendations.
8. Review ranked candidates, rationale, strengths, gaps, unknowns, and disclosure.
9. Save recruiter approval or notes.

API smoke test:

```bash
curl -s http://localhost:8000/health
```

Expected response:

```json
{"status":"ok","service":"recruitment-assistant-backend"}
```

Seeded recommendation API smoke:

```bash
curl -s http://localhost:8000/api/recommendations/run \
  -H 'Content-Type: application/json' \
  -d '{
    "job": {
      "title": "Backend Engineer",
      "description": "Build Python FastAPI services for a recruiter-facing AI workflow.",
      "required_skills": ["Python", "FastAPI"],
      "preferred_skills": ["CrewAI", "PostgreSQL"],
      "seniority": "Senior",
      "location": "Remote"
    },
    "criteria": {
      "title": "Backend Engineer",
      "description": "Build Python FastAPI services for a recruiter-facing AI workflow.",
      "required_skills": ["Python", "FastAPI"],
      "preferred_skills": ["CrewAI", "PostgreSQL"],
      "seniority": "Senior",
      "location": "Remote",
      "ambiguities": [],
      "confirmed_by_recruiter": true
    },
    "candidate_source": {
      "type": "seeded",
      "dataset_id": "backend_engineers"
    },
    "options": {
      "max_candidates": 3,
      "score_style": "numeric_and_label",
      "require_recruiter_checkpoints": true
    }
  }'
```

Expected result:

- HTTP 200.
- `status` is `complete`.
- `ranked_shortlist` is not empty.
- `report.disclosure` is present.
- `approval.status` starts as `pending`.

## Health Checks

### Backend Health

```bash
curl -i http://localhost:8000/health
```

Expected:

- HTTP 200.
- JSON body with `status: ok`.
- Response header includes `x-request-id`.

### Frontend Health

```bash
curl -i http://localhost:4200/healthz
```

Expected:

- HTTP 200.
- Body `ok`.

### Docker Service Health

```bash
docker compose ps
```

Expected:

- `backend` is running and healthy.
- `frontend` is running and healthy.

If a service is unhealthy, inspect logs before restarting.

## Monitor And View Logs

Logs are written to stdout/stderr. In Docker, use Docker container logs. No file-backed or database-backed log retention is implemented in the MVP.

Follow backend logs:

```bash
docker compose logs -f backend
```

Show recent backend logs:

```bash
docker compose logs --tail=100 backend
```

Follow frontend/nginx logs:

```bash
docker compose logs -f frontend
```

Filter useful backend events:

```bash
docker compose logs backend | grep api.request
docker compose logs backend | grep application_crew.run
docker compose logs backend | grep application_crew.agent
docker compose logs backend | grep api.request.error
```

Important backend log events:

| Event | Meaning |
| --- | --- |
| `application.startup` | Backend started and emitted environment metadata. |
| `application.shutdown` | Backend shut down cleanly. |
| `api.request.start` | API request received. |
| `api.request.complete` | API request completed with status and duration. |
| `api.request.error` | Unhandled request exception. |
| `application_crew.preview.start` | Candidate preview started. |
| `application_crew.preview.complete` | Candidate preview completed. |
| `application_crew.run.start` | Recommendation run started. |
| `application_crew.agent.start` | Researcher, Evaluator, or Recommender step started. |
| `application_crew.agent.complete` | Agent step completed. |
| `application_crew.run.complete` | Recommendation run completed. |
| `application_crew.run.error` | Recommendation workflow failed. |
| `approval.record.complete` | Recruiter approval was saved in memory. |
| `approval.record.not_found` | Approval was attempted for an unknown or expired run ID. |

Use the `x-request-id` response header to correlate one API response with backend logs. Keep logs metadata-only; do not add secrets, full job descriptions, full candidate profiles, or recruiter notes to logs without explicit approval.

## CrewAI Tracing

CrewAI AOP/AMP tracing applies only to live CrewAI execution. Deterministic mode does not emit live CrewAI dashboard traces because it does not call `Crew.kickoff()`.

Enable live mode locally:

```bash
crewai login
crewai traces enable
CREWAI_TRACING_ENABLED=true crewai traces status
```

Set `.env`:

```bash
RECRUITMENT_EXECUTION_MODE=crewai_live
CREWAI_TRACING_ENABLED=true
CREWAI_TELEMETRY_OPT_OUT=false
GOOGLE_API_KEY=your_valid_key
CREWAI_MODEL=your_available_model
```

Restart the backend and run a recommendation. Then open `https://app.crewai.com` and inspect the Traces tab.

If traces do not appear:

- Confirm `crewai login` succeeded on the execution host.
- Confirm `crewai traces enable` succeeded.
- Confirm `CREWAI_TRACING_ENABLED=true`.
- Confirm `RECRUITMENT_EXECUTION_MODE=crewai_live`.
- Confirm the backend reached `application_crew.kickoff.start`.
- Confirm the LLM provider key and model are valid.

## Stop And Restart

### Docker Compose

Stop:

```bash
docker compose down
```

Restart all services:

```bash
docker compose restart
```

Restart one service:

```bash
docker compose restart backend
docker compose restart frontend
```

Rebuild after code or dependency changes:

```bash
docker compose build
docker compose up -d
```

Clean rebuild:

```bash
docker compose build --no-cache
docker compose up -d
```

### Local Runtime

- Press `Ctrl+C` in each terminal running `scripts/start-backend.sh` or `scripts/start-frontend.sh`.
- If using `scripts/start-dev.sh`, press `Ctrl+C` once; the script terminates both child processes.
- Restart by running the same script again.

Remember: backend restarts clear in-memory run and approval state.

## Common Issues And Troubleshooting

| Symptom | Likely Cause | What To Do |
| --- | --- | --- |
| `docker: command not found` | Docker is not installed or not on `PATH`. | Install Docker Engine/Desktop or use the local development runtime. |
| `port is already allocated` for `8000` or `4200` | Another process is using the port. | Stop the other process or set `BACKEND_PORT`/`FRONTEND_PORT` in `.env`, then restart. |
| Frontend loads but API calls fail | Backend is not running, backend is on a different port, or CORS origin is not allowed. | Check `curl http://localhost:8000/health`, backend logs, and that the frontend is served from an allowed local origin. |
| Backend container is unhealthy | Backend failed startup or `/health` is unreachable. | Run `docker compose logs --tail=100 backend`, fix configuration, then `docker compose restart backend`. |
| Frontend container is unhealthy | nginx failed or `/healthz` is unreachable. | Run `docker compose logs --tail=100 frontend`, rebuild if static assets are missing. |
| Recommendation returns no candidates | Unknown seeded dataset or empty pasted/uploaded candidate text. | Use seeded dataset `backend_engineers` or provide non-empty candidate text. |
| Recommendation returns low-confidence warnings | Candidate profiles lack enough evidence for the criteria. | Review warnings, add better candidate data, or treat output as requiring more recruiter review. |
| `POST /api/recommendations/run` returns 502 in live mode | CrewAI kickoff failed, usually provider credentials or model access. | Confirm `GOOGLE_API_KEY`, `CREWAI_MODEL`, `CREWAI_PROVIDER`, and CrewAI login/tracing status. Use deterministic mode if live LLM is not needed. |
| Approval returns 404 | Run ID is missing, wrong, or was lost after backend restart. | Rerun recommendations and approve the new `run_id`. |
| Logs are hard to read locally | JSON logs are optimized for containers. | Start backend with `LOG_FORMAT=text` for local debugging. |
| `npm ci` fails | Node/npm version mismatch or corrupted install. | Use Node 20+ and rerun `npm ci` from `frontend/`. |
| Python import errors locally | Virtual environment or `PYTHONPATH` is missing. | Use `scripts/start-backend.sh`, or set `PYTHONPATH=backend` before running tests or Uvicorn. |

## Rollback

Use rollback when a new change breaks the local/demo deployment.

1. Stop the stack:

   ```bash
   docker compose down
   ```

2. Return to the previous known-good Git commit or tag.

3. Rebuild and restart:

   ```bash
   docker compose build --no-cache
   docker compose up -d
   ```

4. Verify:

   ```bash
   curl http://localhost:8000/health
   curl http://localhost:4200/healthz
   ```

5. Run the seeded demo procedure.

No database rollback is required in the current MVP because runtime state is in memory. Any in-progress runs or approvals are lost after rollback.

## Verification Checklist

Run these checks before a demo or handoff:

- `docker compose build` succeeds in a Docker-enabled environment.
- `docker compose up -d` starts both services.
- `docker compose ps` shows healthy backend and frontend services.
- `curl http://localhost:8000/health` returns backend status `ok`.
- `curl http://localhost:4200/healthz` returns `ok`.
- Frontend opens at `http://localhost:4200`.
- Backend OpenAPI docs open at `http://localhost:8000/docs`.
- Seeded dataset `backend_engineers` produces a non-empty ranked shortlist.
- Recommendation output includes rationale, strengths, gaps, unknowns, suggested next steps, and disclosure.
- Recruiter approval can be saved before backend restart.
- `docker compose logs backend` shows request and workflow completion logs.

Non-container checks:

```bash
PYTHONPATH=backend pytest -q backend/tests
cd frontend && npm run build
```

## Operational Guardrails

- Treat all candidate data as sensitive.
- Use seeded or explicitly approved candidate data only.
- Do not use unauthorized scraping or unsupported sources.
- Do not position output as an autonomous hiring decision.
- Keep recruiter review and approval in the workflow.
- Do not process real candidate data until legal/HR, privacy, retention, access control, monitoring, and audit requirements are approved.
- Keep `.env` local and out of version control.
- Do not log API keys, secrets, full candidate profiles, full job descriptions, or recruiter notes unless explicitly approved.

## Sources

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `project-context/3.deliver/deployment-plan.md`
- `project-context/3.deliver/monitoring-plan.md`
- `backend/README.md`
- `backend/app/api/routes.py`
- `backend/app/main.py`
- `backend/app/services/candidate_sources.py`
- `backend/app/services/recruitment_workflow.py`
- `docker-compose.yml`
- `Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- `.env.example`

## Assumptions

- Docker Compose remains the primary Deliver-phase runtime.
- The MVP is for local/demo use, not production hiring decisions.
- Deterministic execution is the normal demo path.
- Live CrewAI execution is optional and depends on valid external credentials.
- In-memory run and approval storage is acceptable for the current MVP.
- The requested `.cursor/templates/runbook-template.md` was not present in this repository, so this runbook follows the requested sections and the established AAMAD Deliver artifact structure.

## Open Questions

- Should the frontend API base URL become runtime-configurable before any non-local deployment?
- Which cloud target should be prepared if this moves beyond a local/demo VM?
- What log retention, access control, and audit policy should apply before real candidate data is processed?
- Should persistent run history and approval audit records be implemented before a production-like pilot?
- Should alert thresholds be defined for error rate, p95 latency, failed recommendation runs, and CrewAI provider failures?

## Handoff Notes

- Start with deterministic mode for reliable demos.
- Use live CrewAI mode only when provider credentials and tracing setup have been verified.
- Backend restarts clear run and approval state.
- Use `x-request-id` to correlate user-reported failures with logs.
- Validate Docker commands in a Docker-enabled environment; Docker was previously unavailable in this workspace during deployment-plan verification.
