# AAMAD Codex Workflow

## Purpose

This repository uses AAMAD as a Codex-native operating model. AAMAD structures work into Define, Build, and Deliver phases while Codex handles orchestration, implementation, verification, and optional delegated subagent work.

## Define

- Clarify the user goal, users, constraints, scope, non-goals, acceptance criteria, and risks.
- Produce or update `project-context/1.define/mrd.md`, `prd.md`, `sad.md`, and `open-questions.md` as needed.
- Use `project-context/1.define/context-summary.md` to summarize approved context for later Build sessions.
- Produce `project-context/1.define/sfs/<feature-id>.md` when a feature needs a tighter functional specification.
- Do not move into broad implementation until the relevant Define artifacts are sufficient for the requested change.

## Build

- Split implementation into bounded modules with explicit ownership.
- Keep the immediate critical path in the main Codex thread.
- When the user explicitly authorizes subagents, delegate independent sidecar tasks to Codex `explorer` or `worker` agents.
- Require every implementation slice to update its matching artifact under `project-context/2.build/`.
- Use `.codex/aamad/epics-index.md` to map Setup, Frontend, Backend, Integration, and QA work to outputs.

## Deliver

- Verify the integrated system with deterministic checks.
- Document release, deployment, operations, access, monitoring, rollback, and remaining risk under `project-context/3.deliver/`.
- Ask for human approval before deployment or other high-impact operations.

## Handoff

- Write handoff notes when changing phases, pausing work, or handing work to another session or authorized subagent.
- Include current state, changed files, verification, known gaps, and next action.
