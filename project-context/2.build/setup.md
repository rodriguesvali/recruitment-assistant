# Setup

## Scope

Record local Build-phase setup decisions and verification notes for the recruitment assistant MVP.

## Inputs

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- Frontend implementation in `frontend/`

## Changes

- Frontend scaffold added under `frontend/` with Angular 21.
- Frontend dependencies added through `frontend/package.json`: PrimeNG, PrimeIcons, PrimeUI themes, and Angular animations.

## Verification

- Frontend build verified with `npm run build`.
- Frontend unit tests verified with `npm test -- --watch=false`.

## Decisions

- Use `npm start` from `frontend/` for local Angular dev server.
- Frontend expects backend API at `http://localhost:8000` and falls back to demo data when unavailable.

## Handoff Notes

- Backend setup remains to be completed separately.
- Integration should confirm CORS between Angular dev server and FastAPI backend.

## Known Gaps

- No backend dependency manifest or runtime command has been verified in this frontend workstream.
