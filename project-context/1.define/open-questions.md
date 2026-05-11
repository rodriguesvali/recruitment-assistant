# Open Questions

## Product and Market

- Who is the first pilot audience: internal recruiting team, staffing agency, startup hiring team, or CrewAI demo/evaluation users?
- Which real recruiters, hiring managers, or HR/talent operations stakeholders will validate that the PRD personas match actual workflows and terminology?
- What is the primary buyer: recruiter, talent acquisition leader, agency owner, founder, or technical evaluator?
- Which role types should the MVP optimize for first, such as software engineering, sales, operations, or general professional hiring?
- Should the product be positioned primarily as a production recruiting tool, an internal recruiting copilot, or a CrewAI showcase application for technical buyers?
- What is the actual manual baseline time for first-pass shortlist and report preparation for target pilot users?
- What recruiter hourly cost or loaded cost assumption should be used for ROI modeling?
- What minimum time reduction, quality improvement, or cost reduction threshold is required to justify continued investment after the mini-project?
- Which organizational goal is primary for this project: internal productivity, CrewAI technical showcase, commercial MVP validation, or responsible AI governance pilot?
- Which MVP nice-to-have items should be pulled into scope only if time remains?
- What business timeline should constrain the MVP build, demo, or pilot readiness expectations?
- Which success metric failures should block pilot expansion versus trigger iteration within the mini-project?
- What operating cost assumptions should be used for model, hosting, storage, or third-party API usage?
- Which stakeholders are available to validate personas, baseline time, output usefulness, and disclosure language?

## Data and Integrations

- Which candidate data sources are approved for MVP and pilot use?
- Which file formats should candidate upload support first: PDF, DOCX, TXT, CSV, or all four?
- Should the product integrate with an ATS in the MVP, or export reports for manual ATS entry?
- What candidate data retention policy should apply to uploaded resumes, generated scores, and run logs?
- Should candidate source references be stored as full extracted text, short snippets, document offsets, or metadata links only?

## Compliance and Governance

- Which jurisdictions must be supported or explicitly excluded for the first pilot?
- What legal/compliance review is required before using candidate scoring in a real hiring workflow?
- Which compliance or regulatory requirements apply if real candidate data is used in testing or pilot workflows?
- What candidate or employee notices are required if the tool is used with real candidates?
- What level of audit logging is required for customer trust and regulatory review?
- What exact UI and report disclosure language should communicate AI assistance and human review responsibility?
- Should score categories avoid subjective dimensions such as "culture fit" unless explicitly defined by job-related criteria?

## Product Decisions

- Should the MVP produce markdown only, PDF exports, DOCX exports, or ATS-ready notes?
- What scoring rubric should be approved as the default?
- Should recruiters be able to customize score weights per role?
- Should outreach remain draft-only in MVP, or should later releases send messages through email/ATS integrations?
- Should a candidate require explicit approval before appearing anywhere in the report, or only before being labeled recommended?

## Verification

- What seeded role and candidate examples should QA use as canonical acceptance fixtures?
- What threshold defines an acceptable source-backed rationale?
- What hallucination/error rate is acceptable before pilot release?
- Which failure modes must be tested first: model timeout, malformed model output, unsupported upload, missing candidate evidence, or audit-log write failure?
