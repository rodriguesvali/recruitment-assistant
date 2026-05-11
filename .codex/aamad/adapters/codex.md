# Codex Adapter

## Mapping

- Main Codex agent: orchestration, repo inspection, critical-path work, final integration, final verification.
- `explorer`: authorized read-only discovery, requirements review, architecture review, test strategy.
- `worker`: authorized bounded implementation or verification with disjoint file ownership.

## Controls

- Use subagents only when the user explicitly asks for delegation, subagents, or parallel agent work.
- Keep blocking work local.
- Assign explicit ownership and required outputs to every worker.
- Review and integrate worker results before final response.

## Audit

For substantial work, update the matching `project-context/` artifact with changed files, verification, known gaps, and handoff notes.
