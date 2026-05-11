# AAMAD Adapter Registry

## Purpose

AAMAD can describe work independently of the execution environment. In this repository, the default adapter is `codex`.

## Selection

- Default: `codex`.
- Optional implementation framework adapters may be documented under `.codex/aamad/adapters/`.
- If an environment variable such as `AAMAD_ADAPTER` exists, record its value in architecture or build artifacts, but do not let it override explicit user instructions.

## Adapter Contract

Each adapter should define:

- Persona/task mapping.
- Allowed tools and execution controls.
- Logging and audit expectations.
- Output validation expectations.
- Failure policy.

## Available Adapters

- `codex`: main Codex orchestration with optional explorer/worker subagents.
- `crewai`: optional implementation-framework guidance when the project itself uses CrewAI.
