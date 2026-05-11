# Frontend

## Scope

Build the MVP recruiter-facing web interface with Angular + PrimeNG. The frontend supports guided job input, criteria review, approved candidate source selection, candidate preview, recommendation review, detail inspection, explicit approval capture, and report preview.

## Inputs

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- `project-context/2.build/frontend-plan.md`
- AAMAD Frontend Engineer persona lens from `.codex/aamad/personas.md`

## Changes

- Created Angular app in `frontend/`.
- Added PrimeNG, PrimeIcons, PrimeUI theme package, and Angular animations.
- Added typed recruitment workflow contracts in `frontend/src/app/recruitment.models.ts`.
- Added `RecruitmentApiService` in `frontend/src/app/recruitment-api.service.ts` for:
  - `GET /health`
  - `POST /api/criteria/extract`
  - `POST /api/candidates/preview`
  - `POST /api/recommendations/run`
  - `POST /api/recommendations/{run_id}/approval`
- Implemented local deterministic fallback data when backend endpoints are unavailable.
- Replaced generated Angular starter UI with a responsive PrimeNG workflow in `frontend/src/app/app.html`, `app.ts`, and `app.css`.
- Updated build budgets in `frontend/angular.json` for the selected PrimeNG UI stack.
- Updated generated unit test expectations for the recruitment assistant app.

## Verification

- Passed: `npm run build` from `frontend/`.
- Passed: `npm test -- --watch=false` from `frontend/`.

## Decisions

- Implemented a single-page guided workflow rather than separate routes to keep the MVP compact.
- Supported `seeded` and `pasted` candidate sources first; `uploaded` is visible but deferred until backend parser support exists.
- Used a backend-availability check and fallback results so the frontend remains demoable before FastAPI implementation is complete.
- Kept model calls and secrets out of frontend code; all real AI workflow execution is expected to happen through the backend.

## Handoff Notes

- Integration should validate the backend response shapes against `recruitment.models.ts`.
- Backend CORS should allow the Angular dev origin, usually `http://localhost:4200`.
- The fallback mode should remain useful for demos but should be labeled clearly when the backend is unavailable.
- QA should add browser/e2e coverage for validation, seeded happy path, pasted profile flow, detail drawer, and approval save.

## Known Gaps

- Backend endpoints are not implemented in this repo state, so live integration has not been verified.
- Uploaded plain-text parsing is deferred.
- No persistent run history UI is included.
- Final disclosure language should be reviewed by HR/legal before real candidate use.
