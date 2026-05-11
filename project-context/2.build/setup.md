# Setup

## Scope

Record local Build-phase setup decisions and verification notes for the recruitment assistant MVP.

## Inputs

- `project-context/1.define/prd.md`
- `project-context/2.build/sad.md`
- Frontend implementation in `frontend/`
- Backend implementation in `backend/`

## Changes

- Frontend scaffold added under `frontend/` with Angular 21.
- Frontend dependencies added through `frontend/package.json`: PrimeNG, PrimeIcons, PrimeUI themes, and Angular animations.
- Backend scaffold added under `backend/` with FastAPI and deterministic recruitment workflow services.
- Root launch scripts added:
  - `scripts/start-backend.sh`
  - `scripts/start-frontend.sh`
  - `scripts/start-dev.sh`
- VS Code launchers added:
  - `.vscode/tasks.json`
  - `.vscode/launch.json`

## Verification

- Frontend build verified with `npm run build`.
- Frontend unit tests verified with `npm test -- --watch=false`.
- Backend tests verified with `PYTHONPATH=backend pytest -q backend/tests`.
- Live backend health verified at `http://localhost:8000/health`.

## Decisions

- Use `npm start` from `frontend/` for local Angular dev server.
- Frontend expects backend API at `http://localhost:8000` and falls back to demo data when unavailable.
- Use `./scripts/start-backend.sh` for FastAPI local execution.
- Use `./scripts/start-frontend.sh` for Angular local execution.
- Use `./scripts/start-dev.sh` or the VS Code compound launcher for full-stack local execution.
- Runtime ports are configurable with `BACKEND_PORT`, `BACKEND_HOST`, `FRONTEND_PORT`, and `FRONTEND_HOST`.

## Handoff Notes

- Backend and frontend local launchers are ready for QA and demo use.
- VS Code users can run tasks or the compound debug configuration without manually changing directories.

## Known Gaps

- The frontend API URL is still a local service constant and should become environment-driven before deployed demos.
