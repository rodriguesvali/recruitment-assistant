# AAMAD Codex Orchestrator

## Purpose

Use this as the routing guide for AAMAD work in Codex. The main Codex agent owns orchestration, user communication, final integration, and verification. Persona files are operating contracts; they do not require separate agents unless the user explicitly authorizes multi-agent work.

## Routing

1. Inspect `project-context/` and existing repo instructions.
2. Identify the active phase: Define, Build, Deliver, or Handoff.
3. Select the matching persona lens from `.codex/aamad/personas/`.
4. Load only the references needed for the task:
   - Define: `prompts/define-phase.md`, templates, Product Manager, System Architect.
   - Build: `epics-index.md`, Project Manager, Frontend, Backend, Integration, QA.
   - Deliver: DevOps, QA, release and operations artifacts.
   - Delegation: `delegation.md` only when the user authorizes subagents.
5. Update the relevant artifact in `project-context/` before ending substantial work.

## Gates

- Do not move from Define to broad Build without explicit user approval or a narrow user-scoped task.
- Do not install dependencies, perform destructive actions, or deploy without explicit approval.
- If scope, architecture, or acceptance criteria are missing, record assumptions and open questions before implementing.

## Outputs

- Define outputs live in `project-context/1.define/`.
- Build outputs live in `project-context/2.build/`.
- Deliver outputs live in `project-context/3.deliver/`.
- Cross-session notes live in `project-context/handoffs/`.
