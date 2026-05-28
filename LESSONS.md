# Lessons Learned

## Project: Recruitment Assistant

### What Went Well
- The project reached the expected end-to-end result without major blockers.
- The AAMAD sequence helped move from definition to build and delivery in an organized way.
- The agents produced the main artifacts needed for each phase with enough context to continue the workflow.
- The application workflow executed successfully and generated candidate recommendations as expected.
- Issues encountered during the process were manageable and did not prevent completion of the mini-project.

### Challenges Encountered
- Organizing the development cycle according to the AAMAD methodology required discipline to follow the Define, Build, and Deliver sequence instead of jumping directly into implementation.
- Working with Python and CrewAI required additional learning because these technologies were outside my primary background.
- Configuring tracing through `app.crewai.com` required understanding CrewAI login, trace enablement, runtime configuration, and how to validate trace output during execution.

### Key Insights

#### Define Phase
- Agentic Architect: prepared the project context and ensured the work started with AAMAD artifacts before coding.
- Product Manager: produced the MRD with problem, users, market opportunity, and business context.
- Product Manager: produced the PRD with product overview, goals, success metrics, scope, features, and constraints.
- Product Manager: defined the Application Crew: Researcher, Evaluator, and Recommender agents.
- Product Manager: mapped the Development Crew personas that will build the solution in later phases.
- Agentic Architect: reviewed the PRD with the Experience hat to validate user flow, interaction design, and edge cases.
- Agentic Architect: reviewed the PRD with the Business hat to validate business value, metrics, scope, and risks.
- Product Manager: revised and finalized the PRD based on Agentic Architect feedback.
- Product Manager: generated the README from the finalized PRD.
- Agentic Architect: validated the Define Phase handoff before moving to Build.

#### Build Phase
- Agentic Architect: configured environment variables and orchestrated the Development Crew using independent sessions, branches, and quality gates.
- System Architect: produced the SAD and architecture plan from the PRD, defining components, technology choices, and integration points.
- Agentic Architect: reviewed and approved the SAD with the Technical hat before implementation continued.
- Frontend Engineer: produced the frontend plan and implemented the UI components, user flows, and API interaction points.
- Agentic Architect: reviewed the frontend plan and implementation for usability, maintainability, and PRD alignment.
- Backend Engineer: produced the backend plan and implemented the Application Crew, API endpoints, and business logic.
- Agentic Architect: reviewed the backend implementation for architecture alignment, error handling, and environment configuration.
- Integration Engineer: produced the integration plan and connected frontend, backend, configuration, and end-to-end data flow.
- Agentic Architect: reviewed integration to confirm API communication, data flow, and cross-boundary error handling.
- QA Engineer: produced the QA plan, executed end-to-end tests, tested agents, APIs, frontend behavior, and documented issues.
- Agentic Architect: reviewed all Build artifacts, confirmed tests and commits, updated documentation, and prepared the project for Deliver.

#### Deliver Phase
- DevOps Engineer: produced the deployment plan with deployment approach, dependencies, configuration, steps, and rollback procedures.
- Agentic Architect: reviewed the deployment plan with the Technical hat for readiness, completeness, and fit for the mini-project.
- DevOps Engineer: added monitoring and logging for startup, agent execution, API activity, errors, and exceptions.
- DevOps Engineer: enabled and documented CrewAI tracing for Application Crew observability.
- Agentic Architect: reviewed monitoring, logging, trace setup, and operational visibility.
- DevOps Engineer: produced the runbook with installation, configuration, run, monitor, troubleshoot, stop, restart, and health-check procedures.
- Agentic Architect: reviewed the runbook to confirm someone new to the project could operate the application.
- Agentic Architect: ran the application end-to-end, monitored execution, and verified that the Application Crew produced recommendations.
- Agentic Architect: captured execution results with input, timing, agent status, output, logs, issues, and observations.
- Agentic Architect: documented lessons learned from Define, Build, Deliver, AAMAD, and the Agentic Architect role.
- Agentic Architect: reviewed all Deliver artifacts, updated documentation, created release notes, and confirmed readiness for final handoff.

### AAMAD Framework Observations
- Agents, instructions, and prompts define focused responsibilities, reducing context drift between product, architecture, implementation, integration, QA, and delivery work.
- Persona-specific prompts help each agent use only the context relevant to its role, which improves consistency and avoids mixing concerns too early.
- Shared instructions act as guardrails for scope, artifacts, quality gates, and handoffs across the full AAMAD workflow.
- The `project-context/` folder is the project memory: it stores decisions, requirements, plans, verification notes, and delivery evidence in a durable place.
- Organizing `project-context/` by phase keeps context chronological and auditable: `1.define/`, `2.build/`, and `3.deliver/`.
- The framework works best when every persona reads from and writes back to `project-context/`, keeping implementation aligned with approved artifacts.

### Agentic Architect Reflections
- The Agentic Architect is the human accountable for directing teams of AI agents, not just a passive user of automation.
- This role manages context, assigns responsibilities, reviews outputs, and decides when work is ready to move to the next phase.
- Human judgment is essential to balance technical feasibility, user experience, business value, and operational risk.
- AI agents can produce artifacts and code quickly, but the Agentic Architect must validate quality, consistency, scope, and assumptions.
- The strongest value of the role is orchestration: knowing which persona to invoke, what context to provide, what output to expect, and how to integrate the result.
- The Agentic Architect remains responsible for final decisions, especially when agent outputs affect people, compliance, safety, or product direction.

### Recommendations for Future Projects
- Adapt AAMAD artifacts to the actual technology stack instead of filling templates generically.
- Keep PRD, SAD, plans, runbooks, and QA artifacts aligned with the real frontend, backend, runtime, APIs, and deployment model.
- Review each template section and remove, defer, or customize items that do not apply to the project scope.
- Document technology-specific decisions early, such as framework choices, API contracts, execution mode, environment variables, and observability tools.
- Make functional requirements concrete enough to guide implementation, testing, and delivery without leaving major interpretation gaps.
- Update artifacts whenever technical or functional decisions change so `project-context/` remains a reliable source of truth.

### Skills Developed
- Reviewing agent-generated MRD and PRD artifacts for product clarity, scope, metrics, and user value.
- Reviewing architecture artifacts for technical coherence, constraints, interfaces, risks, and implementation readiness.
- Reviewing frontend, backend, integration, QA, deployment, monitoring, and runbook artifacts against the approved project context.
- Checking whether each artifact uses the right level of detail for its phase and avoids generic template filling.
- Identifying gaps, assumptions, contradictions, and missing handoff information across artifacts.
- Validating that agent outputs remain aligned with business goals, technical reality, user experience, and delivery needs.
