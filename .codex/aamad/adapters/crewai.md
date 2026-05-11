# CrewAI Adapter Notes

Use this only when the application being built uses CrewAI. This file does not configure Cursor or run CrewAI by itself.

## Guidance

- Keep CrewAI agent and task configuration externalized when the project pattern supports it.
- Declare model/provider, tools, memory, retries, and execution limits explicitly in project code or config.
- Prefer deterministic, sequential flows for MVP work unless the SAD justifies parallel or hierarchical crews.
- Log prompt, task, and output traces to project artifacts when useful, without exposing secrets.
- Validate output headings or schemas before writing final artifacts.

## Safety

- Do not hardcode API keys.
- Keep memory scoped to the project when enabled.
- Document tool whitelists and runtime configuration in build or operations artifacts.
