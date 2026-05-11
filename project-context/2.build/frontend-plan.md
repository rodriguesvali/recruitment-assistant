# Frontend Plan: Recruitment Assistant

## Scope

Build a simple Angular + PrimeNG web interface for the MVP recruiter workflow described in the PRD and Build-phase SAD. The UI will support guided job input, criteria review, approved candidate source selection, candidate preview, recommendation review, explicit recruiter approval, and a report preview with AI-assisted disclosure.

## Sources

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `.codex/aamad/orchestrator.md`
- `.codex/aamad/personas.md`

## UI Components To Build

| Component | Status | Notes |
| --- | --- | --- |
| App shell and workflow stepper | Complete | Responsive workflow strip and backend/demo status tags. |
| `JobRequirementForm` section | Complete | Captures title, description, skills, seniority, location, and max candidate count. |
| `CriteriaReviewPanel` section | Complete | Shows normalized criteria, ambiguity warnings, and recruiter confirmation. |
| `CandidateSourcePanel` section | Complete | Supports seeded and pasted approved candidate source inputs. Uploaded text is clearly deferred. |
| `CandidateListPanel` section | Complete | Shows candidate preview with source labels, skills, and missing data. |
| `RunProgressPanel` section | Complete | Shows validation, research, evaluation, recommendation, completion, and error states. |
| `RankedShortlistPanel` section | Complete | Shows ranked candidates with score, fit label, and detail access. |
| `CandidateDetailDrawer` section | Complete | Opens a detail drawer for rationale, strengths, gaps, unknowns, component scores, and source labels. |
| `ApprovalPanel` section | Complete | Captures approve/reject/needs-edits state and reviewer notes. |
| `ReportPreview` section | Complete | Shows hiring-manager-ready summary and AI-assisted disclosure. |

## User Interaction Flows

1. Recruiter enters job requirements and validates required fields.
2. UI calls criteria extraction when backend is available, or performs local normalization for demo mode.
3. Recruiter reviews criteria and acknowledges any ambiguity warnings.
4. Recruiter selects an approved candidate source: seeded dataset or pasted profiles.
5. UI calls candidate preview when backend is available, or creates a demo preview from local sample/pasted data.
6. Recruiter runs the recommendation workflow.
7. UI calls the full workflow endpoint when backend is available, or generates deterministic demo recommendations.
8. Recruiter opens candidate details, reviews rationale, strengths, gaps, unknowns, and confidence.
9. Recruiter records approval, rejection, or needs-edits notes.
10. UI calls the approval endpoint when a run ID exists, and updates the report preview state.

## API Integration Points

| Endpoint | Frontend Use | Status |
| --- | --- | --- |
| `GET /health` | Detect backend availability for live vs demo mode. | Implemented |
| `POST /api/criteria/extract` | Validate job input and return reviewable criteria. | Implemented with fallback |
| `POST /api/candidates/preview` | Validate approved source and show candidates before running. | Implemented with fallback |
| `POST /api/recommendations/run` | Run Researcher -> Evaluator -> Recommender workflow. | Implemented with fallback |
| `POST /api/recommendations/{run_id}/approval` | Record recruiter approval or override notes. | Implemented with fallback |
| `GET /api/recommendations/{run_id}` | Future run reload/history support. | Deferred |

Default local backend URL: `http://localhost:8000`.

## Implementation Approach

- Scaffold a standalone Angular app in `frontend/`.
- Use PrimeNG components for forms, buttons, tags, progress, tables, drawer, cards, messages, tabs, and selectors.
- Use Angular reactive forms for validation and controlled workflow state.
- Create typed frontend models matching the SAD API contract.
- Create an API service with graceful fallback to local demo data while the backend is not implemented.
- Keep secrets out of frontend code; all AI/model work remains backend-only.
- Use responsive CSS with dense, operational UI layout rather than a marketing landing page.
- Ensure the final report includes the AI-assisted decision-support disclosure and explicit recruiter approval controls.

## Status Tracking

| Task | Status | Notes |
| --- | --- | --- |
| Review PRD and SAD | Complete | MVP flow, API contracts, and governance requirements identified. |
| Create frontend plan artifact | Complete | Created before implementation and updated after verification. |
| Scaffold Angular + PrimeNG app | Complete | Implemented under `frontend/`. |
| Build typed models and API service | Complete | Includes backend calls and demo fallback. |
| Build guided recruiter interface | Complete | Single-screen workflow with sections and detail drawer. |
| Add responsive styling and accessibility states | Complete | Required labels, visible validation, non-color-only status tags and messages. |
| Verify build | Complete | `npm run build` passed. |
| Update frontend build artifact | Complete | `frontend.md` updated with implementation notes. |

## Assumptions

- Backend endpoints may not exist yet, so the frontend can operate in demo fallback mode.
- Seeded and pasted sources are the first supported MVP candidate source types.
- Uploaded plain text is represented as future/deferred until backend parsing exists.
- Numeric score plus qualitative fit label are acceptable because the SAD response contract includes both.

## Open Questions

- Which seeded dataset IDs will the backend expose beyond `backend_engineers`?
- Will criteria extraction require an explicit backend checkpoint before candidate preview, or can the first UI implementation normalize locally when offline?
- What exact legal/HR-approved disclosure language should replace the MVP placeholder before real candidate use?

## Verification

- `npm run build` from `frontend/` passed on 2026-05-11.
- `npm test -- --watch=false` from `frontend/` passed on 2026-05-11.
- Manual browser smoke check is pending user/local review; dev server can run with `npm start`.

## Handoff Notes

- Integration engineer should replace or confirm the fallback mode once backend endpoints are implemented.
- QA engineer should add e2e checks for empty inputs, seeded happy path, pasted profiles, backend unavailable fallback, and explicit approval capture.

## Audit

- Date: 2026-05-11
- Persona lens: Frontend Engineer
- Action: Planned and implemented Angular + PrimeNG MVP frontend.
- Tooling notes: Angular 21, PrimeNG 21, local API fallback service, production budget adjusted for PrimeNG bundle size.
