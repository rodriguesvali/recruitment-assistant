# Monitoring Plan: Recruitment Assistant

## Purpose

Define basic Deliver-phase monitoring and logging for the Recruitment Assistant MVP so local/demo operators can see backend health, API activity, Application Crew execution, errors, and CrewAI AOP/AMP traces without adding persistent infrastructure.

## What To Monitor

| Area | Signals | Current Implementation |
| --- | --- | --- |
| Application lifecycle | Backend startup, shutdown, runtime environment, log level, CrewAI tracing flag | `backend/app/main.py` logs `application.startup` and `application.shutdown`. |
| API requests | Method, path, status code, duration, client host, request correlation ID | FastAPI middleware in `backend/app/main.py` logs `api.request.start`, `api.request.complete`, and `api.request.error`. |
| Application Crew execution | Run start, run completion, run failure, elapsed time, candidate count, evaluation count, shortlist count, warning count | `backend/app/services/recruitment_workflow.py` logs `application_crew.run.*`. |
| Agent steps | Researcher, Evaluator, and Recommender start/completion counts | `backend/app/services/recruitment_workflow.py` logs `application_crew.agent.start` and `application_crew.agent.complete`. |
| Candidate preview | Candidate source type, max candidates, candidate count, warning count, duration | `RecruitmentWorkflowService.preview_candidates()` logs preview start/completion/error. |
| Recruiter approval | Approval saved or missing run ID | `RecruitmentWorkflowService.record_approval()` logs approval completion and not-found warnings. |
| Errors and exceptions | Unhandled request exceptions, workflow exceptions, stack traces | Middleware and workflow service use `logger.exception(...)` for stack traces. |
| CrewAI traces | Live CrewAI task/agent execution, LLM calls, task timeline, token/cost metrics where available | `backend/app/agents/crew.py` sets `tracing=crewai_tracing_enabled()` when building a live CrewAI Crew. |

## Log Levels And Format

| Level | Use |
| --- | --- |
| `INFO` | Startup/shutdown, API request start/completion, workflow start/completion, agent step start/completion, approval completion. |
| `WARNING` | Expected operational issues that do not crash the service, such as approval for an unknown run ID. |
| `ERROR` | Request or workflow exceptions that raise stack traces. |
| `DEBUG` | Reserved for local troubleshooting; do not log secrets, full job descriptions, or full candidate profiles. |

Default format is structured JSON to stdout:

```json
{
  "timestamp": "2026-05-25T00:00:00+00:00",
  "level": "INFO",
  "logger": "app.main",
  "message": "api.request.complete",
  "request_id": "request-correlation-id",
  "method": "POST",
  "path": "/api/recommendations/run",
  "status_code": 200,
  "duration_ms": 42.3
}
```

Set `LOG_FORMAT=text` for local human-readable logs. Keep `LOG_FORMAT=json` for Docker demos and production-like validation.

## Where Logs Are Stored

Logs are written to process stdout/stderr.

| Runtime | Storage Location |
| --- | --- |
| Docker Compose | Docker container log driver for the `backend` service. |
| Local `uvicorn` | Terminal output from `scripts/start-backend.sh` or the `uvicorn` command. |
| Future cloud runtime | Platform log collector, such as CloudWatch, Azure Monitor, GCP Cloud Logging, or a centralized OpenTelemetry/log pipeline. |

No database or file-backed log retention is implemented for the MVP.

## How To View Logs

Docker Compose:

```bash
docker compose logs -f backend
docker compose logs --tail=100 backend
```

Local backend:

```bash
LOG_LEVEL=INFO LOG_FORMAT=json scripts/start-backend.sh
```

Filter examples:

```bash
docker compose logs backend | grep application_crew.run
docker compose logs backend | grep api.request.error
```

## CrewAI AOP/AMP Tracing Setup

CrewAI tracing is configured for the live Application Crew builder in `backend/app/agents/crew.py`:

```python
Crew(..., tracing=crewai_tracing_enabled())
```

Tracing is enabled by default in Docker and `.env.example`:

```bash
CREWAI_TRACING_ENABLED=true
CREWAI_TELEMETRY_OPT_OUT=false
```

Authentication and dashboard access:

1. Create or use a CrewAI AOP/AMP account at `https://app.crewai.com`.
2. Authenticate the local or demo host:

   ```bash
   crewai login
   ```

3. Enable trace collection consent for the local user:

   ```bash
   crewai traces enable
   CREWAI_TRACING_ENABLED=true crewai traces status
   ```

4. Start the backend with `CREWAI_TRACING_ENABLED=true`.
5. Set `RECRUITMENT_EXECUTION_MODE=crewai_live` and execute `POST /api/recommendations/run` to call `Crew.kickoff()` from the backend.
6. Open `https://app.crewai.com`, navigate to the project dashboard, and select the Traces tab.

CrewAI documentation states that traces show agent/task execution details, LLM calls, execution timelines, token/cost metrics, and errors. If traces do not appear, verify `crewai login`, `crewai traces enable`, `CREWAI_TRACING_ENABLED=true`, and that a live CrewAI Crew was actually executed with `Crew.kickoff()`.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOG_LEVEL` | `INFO` | Controls backend application logging verbosity. |
| `LOG_FORMAT` | `json` | Controls backend log formatter: `json` or `text`. |
| `RECRUITMENT_EXECUTION_MODE` | `deterministic` | Set to `crewai_live` to route recommendation runs through CrewAI `kickoff()`. |
| `CREWAI_TRACING_ENABLED` | `true` | Enables CrewAI tracing for live CrewAI Crew objects. |
| `CREWAI_TELEMETRY_OPT_OUT` | `false` | Allows CrewAI tracing/telemetry for the monitored demo path. |
| `APP_ENV` | `development` locally, `docker` in Compose | Identifies the runtime environment in startup logs. |

## Status Tracking

| Item | Status | Notes |
| --- | --- | --- |
| Review deployment plan | Complete | Reviewed `project-context/3.deliver/deployment-plan.md` and updated monitoring-related environment variables. |
| Add application startup logging | Complete | Startup/shutdown logs are emitted from FastAPI lifespan hooks. |
| Add API request/response logging | Complete | Middleware logs request start, completion, status code, duration, and errors with `x-request-id`. |
| Add Application Crew execution logging | Complete | Workflow service logs run lifecycle, deterministic agent steps, preview, and approval actions. |
| Add error and exception logging | Complete | Middleware and workflow service log exceptions with stack traces. |
| Enable CrewAI tracing configuration | Complete | Live CrewAI Crew builder passes `tracing=crewai_tracing_enabled()` and environment defaults enable tracing. |
| Integrate CrewAI kickoff in backend | Complete | `/api/recommendations/run` calls `Crew.kickoff()` when `RECRUITMENT_EXECUTION_MODE=crewai_live`; deterministic mode remains the default fallback. |
| Set up CrewAI AOP/AMP authentication | Complete | Operator ran `crewai login` in the dev container. |
| Enable CrewAI trace collection consent | Complete | `crewai traces enable` succeeded; `CREWAI_TRACING_ENABLED=true crewai traces status` reports `Overall Status: ENABLED`. |
| Document dashboard trace viewing | Complete | See CrewAI AOP/AMP tracing setup above. |
| Verify backend tests | Complete | `PYTHONPATH=backend pytest -q backend/tests` passed with 5 tests on 2026-05-25. |
| Verify request log smoke | Complete | TestClient `/health` request emitted startup, request start/complete, and shutdown JSON logs with `x-request-id=monitoring-smoke`. |
| Verify CrewAI CLI availability | Complete | `crewai --version` returned `crewai, version 1.14.2`; interactive login still requires an operator. |
| Verify CrewAI tracing config | Complete | `build_crewai_crew()` returned a Crew with `tracing=True` when `CREWAI_TRACING_ENABLED=true`. |
| Verify live kickoff smoke | Blocked By LLM Credential/Model | Backend reached `application_crew.kickoff.start`, built a traced Crew, and attempted Google GenAI. The provider returned errors indicating the configured API key/model is not accepted. |
| Verify Docker logs | Blocked In Workspace | Docker CLI was previously unavailable in this workspace; validate with `docker compose logs -f backend` in a Docker-enabled environment. |

## Sources

- `project-context/3.deliver/deployment-plan.md`
- `project-context/2.build/sad.md`
- `backend/app/main.py`
- `backend/app/services/recruitment_workflow.py`
- `backend/app/agents/crew.py`
- CrewAI tracing documentation: `https://docs.crewai.com/en/observability/tracing`
- CrewAI AOP traces documentation: `https://docs.crewai.com/en/enterprise/features/traces`

## Assumptions

- The Deliver target remains a local/demo Docker Compose deployment.
- Logs should not include secrets, full job descriptions, full candidate profiles, or recruiter notes.
- The current API path remains deterministic; live CrewAI tracing is configured and ready but only emits dashboard traces when a live CrewAI Crew is executed.
- Docker/container log retention is handled outside the application.

## Open Questions

- What retention period and access policy should apply before real candidate data is processed?
- Should production logs be shipped to a centralized platform, and if so which one?
- Should future persistent audit logs store recruiter approvals separately from application logs?
- Should alert thresholds be defined for error rate, p95 latency, and failed recommendation runs before a pilot?

## Verification

Recommended checks:

```bash
PYTHONPATH=backend pytest -q backend/tests
LOG_LEVEL=INFO LOG_FORMAT=json PYTHONPATH=backend python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
curl http://127.0.0.1:8000/health
```

For Docker-enabled environments:

```bash
docker compose build
docker compose up -d
docker compose logs -f backend
```

Expected backend logs include `application.startup`, `api.request.start`, `api.request.complete`, and `application_crew.run.complete` after a seeded recommendation run.

Executed in this workspace on 2026-05-25:

- `PYTHONPATH=backend pytest -q backend/tests`: passed with 5 tests.
- `PYTHONPATH=backend python - <<'PY' ... TestClient('/health') ... PY`: passed and returned `x-request-id: monitoring-smoke`.
- `python -m compileall -q backend/app`: passed.
- `crewai --version`: returned `crewai, version 1.14.2`.
- `crewai traces enable`: succeeded.
- `CREWAI_TRACING_ENABLED=true crewai traces status`: reported `Overall Status: ENABLED`.
- `CREWAI_TRACING_ENABLED=true PYTHONPATH=backend python - <<'PY' ... build_crewai_crew() ... PY`: returned a `Crew` with `tracing=True`.
- Live `/api/recommendations/run` with `RECRUITMENT_EXECUTION_MODE=crewai_live`: reached `Crew.kickoff()` and emitted CrewAI trace messaging, but Google GenAI returned provider errors for the configured key/model. Replace the local `GOOGLE_API_KEY` and confirm `CREWAI_MODEL` is available to the key before rerunning.

## Handoff Notes

- Use `x-request-id` from API responses to correlate request logs.
- Keep log payloads metadata-only unless legal/HR explicitly approves logging candidate or job details.
- Run `crewai login` wherever live CrewAI execution happens; containerized production-like environments may need a non-interactive credential strategy before real deployment.
- Add centralized log retention, alerting, and audit persistence before processing real candidate data.
