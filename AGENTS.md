# AAMAD Agent Framework

This project uses the AAMAD framework for multi-agent development.
See the full agent definitions in the IDE-specific directories.

## Agent Personas
- **@product-mgr** — Product Manager: Orchestrates product vision and requirements
- **@system.arch** — System Architect: Produces SAD and SFS documents
- **@project.mgr** — Project Manager: Scaffolds project and environment
- **@frontend.eng** — Frontend Developer: Builds MVP chat interface
- **@backend.eng** — Backend Developer: Builds CrewAI backend
- **@integration.eng** — Integration Engineer: Connects frontend and backend
- **@qa.eng** — QA Engineer: Validates MVP functionality

## Workflow
1. **Define** (Phase 1): @product-mgr → Market Research → PRD → @system.arch → SAD
2. **Build** (Phase 2): @project.mgr → @frontend.eng / @backend.eng → @integration.eng → @qa.eng
3. **Deliver** (Phase 3): DevOps deployment

## Rules
All development follows AAMAD core rules. See project-context/ for artifacts.

## Agent Definitions
See the IDE-specific directories for agent definitions:

- `.cursor/agents/` for Cursor
- `.github/agents/` for VS Code / GitHub Copilot
- `.claude/agents/` for Claude Code

<!-- AAMAD-CODEX:START -->
## AAMAD Workflow for Codex

Use AAMAD (AI-Assisted Multi-Agent Application Development) as the project operating model for Codex work. This repository is configured for Codex-native execution, not Cursor agents.

### Phases

1. Define: clarify goal, users, scope, constraints, acceptance criteria, risks, and open questions before coding.
2. Build: implement in scoped modules with clear ownership, verification, and handoff notes.
3. Deliver: verify release readiness, deployment assumptions, operations, access, monitoring, and rollback concerns.

### Context Artifacts

- Store planning and handoff artifacts in `project-context/`.
- Treat `project-context/1.define/prd.md` and `project-context/1.define/sad.md` as the approved source for scope and architecture once reviewed.
- Update the relevant phase artifact when decisions change.
- Record unresolved assumptions and questions in `project-context/1.define/open-questions.md`.
- Use `.codex/aamad/` for AAMAD orchestration, persona, prompt, rule, adapter, epic, and template reference material.
- Start from `.codex/aamad/orchestrator.md` when deciding which AAMAD phase or persona lens applies.

### Codex Multi-Agent Mapping

- The main Codex agent owns orchestration, repo inspection, user communication, final integration, and verification.
- Use Codex subagents only when the user explicitly asks for delegation, subagents, or parallel agent work.
- Map AAMAD personas to Codex subagents as follows when delegation is authorized:
  - Product Manager and System Architect: `explorer` for discovery, requirements, architecture questions, and artifact review.
  - Project Manager, Frontend Engineer, Backend Engineer, Integration Engineer, QA Engineer, and DevOps Engineer: `worker` for bounded implementation or verification tasks with disjoint file ownership.
- Give each worker explicit ownership, tell it the codebase may have other active edits, and require it to list changed files in its final response.
- Keep blocking critical-path work local unless parallel delegation can progress without blocking the next step.

### Agent Personas

- Product Manager: discovery, MRD/PRD, success metrics, and acceptance criteria.
- System Architect: SAD, constraints, interfaces, risks, and technical decisions.
- Project Manager: task slicing, setup, sequencing, and handoffs.
- Frontend Engineer: UI implementation and frontend verification when applicable.
- Backend Engineer: APIs, data, services, and backend verification when applicable.
- Integration Engineer: cross-component wiring and smoke tests.
- QA Engineer: test plan, regression checks, and known gaps.
- DevOps Engineer: deployment, runtime config, access, monitoring, and rollback notes.

### Execution Rules

- Preserve existing repo conventions over generic AAMAD defaults.
- Work in small modules with explicit acceptance criteria.
- Write or update the relevant artifact after each phase.
- Ask for human approval before major scope changes, destructive actions, dependency changes, or deployment.
- Prefer deterministic verification: tests, linters, type checks, smoke tests, screenshots, or logs as appropriate.
- End substantial AAMAD artifacts with Sources, Assumptions, Open Questions, Verification, and Handoff Notes when relevant.
<!-- AAMAD-CODEX:END -->
