# QA Plan: Recruitment Assistant

## Scope

Validate the Recruitment Assistant MVP against the approved PRD, Build-phase SAD, and implementation plans. QA covers the guided recruiter workflow, FastAPI endpoints, deterministic Application Crew agents, approved candidate sources, human approval behavior, report disclosure, and error handling.

This QA pass was executed on 2026-05-11 from `/workspace/recruitment-assistant`.

## Sources

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `project-context/2.build/frontend-plan.md`
- `project-context/2.build/backend-plan.md`
- `project-context/2.build/integration-plan.md`
- `backend/app/api/routes.py`
- `backend/app/agents/crew.py`
- `frontend/src/app/app.ts`
- `frontend/src/app/recruitment-api.service.ts`

## Acceptance Criteria

| ID | Criteria | Status |
| --- | --- | --- |
| AC-01 | Recruiter can enter job requirements and extract reviewable criteria. | Passed |
| AC-02 | Criteria checkpoint is preserved before recommendation run. | Passed |
| AC-03 | Only approved candidate sources are used: seeded, pasted, uploaded plain text. | Passed |
| AC-04 | Researcher, Evaluator, and Recommender agents execute sequentially. | Passed |
| AC-05 | Ranked shortlist includes rationale, strengths, gaps, unknowns, confidence/score, and next step. | Passed |
| AC-06 | Report includes AI-assisted decision-support disclosure. | Passed |
| AC-07 | Recruiter approval can be recorded after a run. | Passed with issue |
| AC-08 | Empty or invalid input fails safely with useful validation or warning. | Passed with issue |
| AC-09 | Frontend builds and renders the primary app shell. | Passed |
| AC-10 | Full browser e2e interaction is automated. | Not run |
| AC-11 | Workflow stepper clearly reflects approval as the final human-review state. | Passed |
| AC-12 | Run progress clearly reflects completion after ranked shortlist generation. | Passed |

## Test Scenarios

| ID | Scenario | Expected Result | Actual Result | Status |
| --- | --- | --- | --- | --- |
| TC-API-001 | `GET /health` | Returns `200` with backend status `ok`. | Returned `{"status":"ok","service":"recruitment-assistant-backend"}`. | Passed |
| TC-API-002 | Extract criteria with valid job input. | Returns normalized criteria and skills. | Returned title, description, `Python`, `FastAPI`, preferred skills, and no unexpected errors. | Passed |
| TC-API-003 | Extract criteria with blank job title. | Rejects before crew run. | Returned HTTP `422`. | Passed |
| TC-API-004 | Preview seeded candidates from `backend_engineers`. | Returns approved seeded profiles with source labels. | Returned 4 seeded candidates and no warnings. | Passed |
| TC-API-005 | Preview pasted candidate profiles. | Parses separate candidates and labels source as pasted. | Returned 2 parsed candidates with `pasted-profile` labels. | Passed |
| TC-API-006 | Preview uploaded plain text. | Parses approved text payload and labels source as uploaded. | Returned 1 parsed candidate with `uploaded-text` label. | Passed |
| TC-API-007 | Preview unknown seeded dataset. | Returns no candidates and a controlled warning. | Returned empty list with `UNKNOWN_DATASET`. | Passed |
| TC-API-008 | Run seeded recommendation workflow. | Returns complete run, sorted shortlist, evaluations, report, disclosure, and warnings if needed. | Returned complete run with 3 ranked candidates, sorted scores, disclosure, and `LOW_CONFIDENCE_RESULTS` warning. | Passed |
| TC-API-009 | Record approval for a completed run. | Stores reviewer status and notes. | Returned approved status and reviewer notes. | Passed |
| TC-API-010 | Run with no available candidates. | Completes safely with no shortlist and recovery warning. | Returned empty shortlist with `NO_CANDIDATES`. | Passed |
| TC-AGENT-001 | Researcher Agent with seeded source. | Returns approved candidate profiles only. | Returned 2 candidates when `max_candidates=2`. | Passed |
| TC-AGENT-002 | Evaluator Agent with researcher output. | Produces bounded scores, fit labels, rationale, strengths, gaps, unknowns. | Produced evaluations with `0-100` scores and rationale. | Passed |
| TC-AGENT-003 | Recommender Agent with evaluations. | Ranks by score and returns recommendation fields. | Returned ranks `[1, 2]` in descending score order. | Passed |
| TC-AGENT-004 | CrewAI blueprint. | Defines 3 agents, 3 tasks, sequential process. | Blueprint matched expected structure. | Passed |
| TC-FE-001 | Angular unit tests. | App component tests pass. | `2 passed`. | Passed |
| TC-FE-002 | Angular production build. | Build completes without errors. | Build completed to `frontend/dist/frontend`. | Passed |
| TC-FE-003 | Frontend dev server smoke. | Serves Angular shell. | Served `index.html` with `<app-root>` on `127.0.0.1:4300`. | Passed with issue |
| TC-FE-004 | Save approval after selecting `Approved`. | Approval status updates and the workflow stepper activates the final `Approval` step. | Fixed on 2026-05-18. `activeStep` now returns `5` while approval is pending and `6` once `approval.status` is no longer `pending`; frontend tests cover both states. | Passed |
| TC-FE-005 | Complete recommendation run and review the Run progress panel. | Progress bar reaches 100% and state reads `complete` once the ranked shortlist is available. | Fixed on 2026-05-18. The delayed `recommending` timer is guarded by the current run token and only applies while the run is still `evaluating`; frontend regression coverage verifies status remains `complete` and progress remains `100` after delayed timers flush. | Passed |
| TC-E2E-001 | Live backend HTTP workflow. | Local server handles run and approval over HTTP. | Uvicorn handled health, run, and approval calls successfully. | Passed |

## Execution Log

| Command or Check | Result |
| --- | --- |
| `PYTHONPATH=backend pytest -q backend/tests` | Passed: 2 tests. |
| `npm test -- --watch=false` from `frontend/` | Passed: 1 test file, 2 tests. |
| `npm run build` from `frontend/` | Passed. |
| `npm test -- --watch=false` from `frontend/` after QA-005 fix | Passed: 1 test file, 4 tests. |
| `npm run build` from `frontend/` after QA-005 fix | Passed. |
| `npm test -- --watch=false` from `frontend/` after QA-006 fix | Passed: 1 test file, 5 tests. |
| `npm run build` from `frontend/` after QA-006 fix | Passed. |
| `npm test -- --watch=false` from `frontend/` after QA-001 fix | Passed: 2 test files, 10 tests. |
| `npm run build` from `frontend/` after QA-001 fix | Passed. |
| `npm test -- --watch=false` from `frontend/` after QA-002 fix | Passed: 2 test files, 11 tests. |
| `npm run build` from `frontend/` after QA-002 fix | Passed. |
| Scripted FastAPI and direct agent QA checks | Passed: 16 checks. |
| `PYTHONPATH=backend uvicorn app.main:app --host 127.0.0.1 --port 8000` | Started successfully for live smoke. |
| `curl http://127.0.0.1:8000/health` | Passed. |
| Live `POST /api/recommendations/run` | Passed; returned complete run and ranked shortlist. |
| Live `POST /api/recommendations/{run_id}/approval` | Passed; returned saved approval payload. |
| `npm start -- --host 127.0.0.1 --port 4200` | Could not start because port 4200 was already in use. |
| `npm start -- --host 127.0.0.1 --port 4300` | Started and served Angular shell. |

## Issues Found

| ID | Severity | Area | Finding | Evidence | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| QA-001 | Medium | Frontend/API integration | Frontend API service catches all API errors and falls back to demo results, including backend validation or server failures. This preserves demo usability but can mask real API defects during QA or production-like demos. | Fixed on 2026-05-18. `RecruitmentApiService` now uses demo fallback only for request timeout or status `0` transport failures, while backend HTTP `4xx/5xx` responses are rethrown to Angular subscribers. Covered by focused service tests for network fallback, timeout fallback, validation error propagation, server error propagation, and preserved fallback warning copy. | Keep fallback limited to offline/timeout failures unless an explicit demo-mode flag is added later. | Fixed |
| QA-002 | Low | Frontend/API integration | Frontend included seeded dataset options `frontend_engineers` and `data_analytics`, but backend only ships `backend_engineers`. Selecting the extra options produced an empty preview warning. | Fixed on 2026-05-18. `frontend/src/app/app.ts` now exposes only the backend-supported `backend_engineers` seeded dataset. Covered by a focused frontend regression test in `frontend/src/app/app.spec.ts`. | Keep the seeded dataset selector aligned with backend-supported IDs until additional approved fixtures are added. | Fixed |
| QA-003 | Low | API semantics | Approval endpoint returns success for unknown `run_id` instead of returning `404`. This can make a mistyped or stale run approval look saved. | Fixed on 2026-05-18. `RecruitmentWorkflowService.record_approval` now returns `404` for missing runs, while valid approvals still return and persist the saved payload. Verified with `PYTHONPATH=backend pytest -q backend/tests`. | Keep endpoint semantics strict for stale or mistyped run IDs. | Fixed |
| QA-004 | Low | Local dev integration | Default frontend port `4200` was occupied during QA. The fallback port `4300` is not CORS-whitelisted by the backend, so a browser served from `4300` would not be able to call the live API and would fall back to demo mode. | Frontend dev server had to start on `127.0.0.1:4300`; backend CORS allows `4200` and `5173`, not `4300`. | Keep `4200` free for demos or add documented alternate dev ports to CORS. | Open |
| QA-005 | Medium | Frontend workflow stepper | After selecting `Approved` and clicking `Save approval`, the approval status was saved, but the final workflow step was never activated. The SAD defines approval/report-ready summary as the final human-review state, and the UI stepper includes `Approval` as step 6. | Fixed in `frontend/src/app/app.ts`; `activeStep` now returns `5` for pending approval and `6` after a non-pending approval is recorded. Covered by frontend tests in `frontend/src/app/app.spec.ts`. | Keep the current 6-step UI for MVP. Revisit whether to expand to the SAD's 7-step flow during broader UX refinement. | Fixed |
| QA-006 | Medium | Frontend progress state | The Run progress bar can remain at 86% with label `Recommending` after the ranked shortlist is already rendered, making the completed recommendation run look unfinished. | Fixed in `frontend/src/app/app.ts`; the delayed `recommending` transition now checks the active recommendation run token and current status before updating. Covered by frontend regression test in `frontend/src/app/app.spec.ts` that flushes the delayed timer after a completed workflow and verifies `runStatus` remains `complete` with `progressValue()` at `100`. | Keep the guarded timer behavior for MVP; revisit progress events if backend streaming or async job polling is introduced later. | Fixed |

## Status Tracking

| Work Item | Status | Notes |
| --- | --- | --- |
| Review PRD | Complete | MVP scope, approval requirement, approved data boundaries, and success metrics reviewed. |
| Review SAD | Complete | Sequential Application Crew, FastAPI contracts, error handling, and disclosure reviewed. |
| Review frontend plan | Complete | Angular workflow, fallback mode, and expected endpoints reviewed. |
| Review backend plan | Complete | Endpoint and deterministic crew implementation reviewed. |
| Review integration plan | Complete | Local ports, CORS, run flow, approval flow, and test expectations reviewed. |
| Create QA plan artifact | Complete | This document created at `project-context/2.build/qa-plan.md`. |
| Execute API tests | Complete | Smoke tests plus scripted endpoint coverage passed. |
| Execute Application Crew agent tests | Complete | Researcher, Evaluator, Recommender, and CrewAI blueprint checks passed. |
| Execute frontend checks | Complete | Unit tests, build, and dev-server HTML smoke passed. |
| Execute end-to-end tests | Complete | Live backend HTTP flow passed; browser-click automation not run. |
| Document findings | Complete | Two open findings remain; QA-001, QA-002, QA-005, and QA-006 fixed and verified. |

## Assumptions

- Deterministic backend services are the MVP execution path; live LLM/CrewAI execution is optional and not required for this QA pass.
- Uploaded plain text means approved text content pasted into the API/UI, not multipart PDF/DOCX parsing.
- In-memory run and approval storage is acceptable for the module demo.
- Frontend fallback mode is intentionally supported for demos when the backend is unavailable.

## Open Questions

- Should approval of an unknown `run_id` be considered invalid for the MVP?
- Will additional seeded datasets be added before delivery, after approved fixtures are defined?
- Is browser e2e automation expected for delivery, and if so should Playwright or another runner be added to the repo?

## Verification

Backend, agent, frontend unit, frontend build, and live HTTP checks passed on 2026-05-11. QA-001 was fixed and verified on 2026-05-18 with `npm test -- --watch=false` and `npm run build` from `frontend/`; the frontend suite now covers offline/timeout fallback and HTTP validation/server error propagation in `RecruitmentApiService`. QA-002 was fixed and verified on 2026-05-18 with `npm test -- --watch=false` and `npm run build` from `frontend/`; the frontend suite now includes regression coverage that only backend-supported seeded dataset IDs are exposed. QA-005 was fixed and verified on 2026-05-18 with `npm test -- --watch=false` and `npm run build` from `frontend/`. QA-006 was fixed and verified on 2026-05-18 with `npm test -- --watch=false` and `npm run build` from `frontend/`; the frontend suite now includes regression coverage for the delayed progress-state race. Full browser-click automation was not executed because no browser binary or Playwright dependency is currently available in the workspace.

## Handoff Notes

- MVP is functionally ready for a guided local demo on the default backend `8000` and frontend `4200` ports.
- Before a production-like demo, keep fallback behavior limited to backend-offline or timeout failures so API validation/server defects remain visible.
- Keep the app on CORS-approved frontend ports or update backend CORS for any alternate demo port.
- Add browser e2e coverage for seeded happy path, pasted profiles, uploaded text, empty source, backend-unavailable fallback, and approval capture when the team adds a browser test runner.
