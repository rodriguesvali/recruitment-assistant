# AAMAD Rules for Codex

## Core Rules

- Context first: scope and architecture should trace back to PRD, SAD, user stories, or explicit user direction.
- Single responsibility: each persona or delegated task owns a clear module and output artifact.
- Deterministic work: prefer repeatable commands, stable file outputs, and explicit verification.
- Preserve existing conventions: local repo patterns override generic AAMAD defaults.
- No secrets in artifacts: document variable names and configuration shape, never secret values.
- MVP first: implement the smallest approved scope that proves the intended value; document deferrals.

## Persona Contract

- Each persona has declared inputs, outputs, actions, and prohibited actions.
- Read broadly enough to understand the repo, but write only to the task's scoped files and matching artifact unless the user asks otherwise.
- If a required input is missing, record assumptions and open questions before proceeding.

## Task Contract

- Define the expected output path, acceptance criteria, and verification before substantial implementation.
- Keep traceability to PRD, SAD, SFS, user story, issue, or explicit user instruction.
- If a requested task conflicts with the active persona contract, stop and explain the conflict.

## Artifact Rules

- Keep artifacts concise and actionable.
- Each artifact should include Sources, Assumptions, Open Questions, Verification, and Handoff Notes when relevant.
- Record known gaps rather than hiding incomplete work.
- Add an Audit section for generated planning artifacts when useful: date, persona, action, model/tooling notes, and verification.

## Tooling Rules

- Use repository-local commands and existing toolchains first.
- Use network, dependency installation, destructive operations, or deployment only with explicit user approval.
- Prefer structured parsers and existing framework tools over ad hoc text manipulation.

## Failure Policy

- If required inputs are missing, continue only when a reasonable assumption is low risk.
- Record assumptions and open questions.
- Halt and ask the user when the next step would be destructive, high-risk, or impossible to infer safely.
