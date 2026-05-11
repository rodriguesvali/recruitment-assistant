# Context Summary

## Approved Scope

- Define-phase artifacts for a recruitment assistant application based on the CrewAI recruitment example.
- MVP concept: recruiter-controlled AI copilot that turns job requirements and approved candidate data into explainable shortlists, outreach drafts, and recruiter-ready reports.
- The product supports human review and recommendation workflows; it does not make final hiring decisions.
- MVP inputs are manual entry, upload/import, seed data, or compliant connectors/APIs only.

## Key Decisions

- Use the Product Manager lens for MRD and PRD creation.
- Use the CrewAI recruitment example as the workflow reference; for this mini-project, simplify the application crew to Researcher, Evaluator, and Recommender agents.
- Do not carry forward the example's cookie-based LinkedIn automation into product scope.
- Prioritize explainability, source traceability, human approval, and audit logging in MVP requirements.
- Full ATS integration, candidate communication automation, and advanced analytics/reporting are out of scope for the mini-project.
- MRD is organized around problem statement, target users, market opportunity, and competitive landscape per stakeholder direction.
- PRD is organized around product overview, goals/metrics, user personas, core features, application crew definition, development crew mapping, and mini-project out-of-scope boundaries.

## Constraints

- Candidate data must come from manual entry, upload, seed data, or compliant connectors/APIs.
- AI scoring must be positioned as decision support, not autonomous selection.
- Compliance-sensitive requirements must be reviewed before production hiring use.
- Define artifacts should remain the source of scope until reviewed and approved.

## Acceptance Criteria

- MRD identifies the recruitment problem, target users, market opportunity, competitive landscape, multi-agent differentiation, market requirements, risks, metrics, sources, assumptions, open questions, verification, and handoff notes.
- PRD defines product overview, core value proposition, success metrics, recruiter and hiring manager personas, core features, application crew definition, Module 06 development crew mapping, out-of-scope items, functional requirements, sources, assumptions, open questions, verification, and handoff notes.
- Open questions are captured for stakeholder review before broad Build phase work.

## Open Questions

- First pilot audience and buyer persona are not yet confirmed.
- Approved candidate data sources and upload formats are not yet confirmed.
- Target jurisdictions, notices, audit needs, and data retention policy are not yet confirmed.
- Export format and ATS integration needs are not yet confirmed.

## Handoff Notes

- System Architect should next review `project-context/1.define/prd.md` and produce/update `project-context/1.define/sad.md`.
- Build phase should wait for user approval or a narrow implementation request.
- Backend implementation should use CrewAI orchestration with persisted intermediate outputs and avoid unauthorized scraping.
