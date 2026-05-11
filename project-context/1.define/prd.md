# Product Requirements Document: Recruitment Assistant

## Product Overview

The Recruitment Assistant is an AI-powered multi-agent application that helps recruiters find, evaluate, and rank candidates based on job requirements. It is inspired by the CrewAI recruitment example and adapts that pattern into a focused mini-project with three application agents: a Researcher Agent, an Evaluator Agent, and a Recommender Agent.

The assistant takes a job requirement as input, searches or sources candidate information from approved inputs, evaluates candidates against the role criteria, and returns ranked candidate recommendations with concise reasoning.

### Core Value Proposition

Recruiters can move from a job requirement to a ranked candidate shortlist faster, with more consistent evaluation logic and clearer recommendations for hiring managers.

The product provides value by:

- Reducing manual candidate sourcing and screening effort.
- Applying job criteria consistently across candidates.
- Producing ranked candidate recommendations with fit rationale.
- Helping hiring managers quickly understand which candidates are strongest and why.
- Keeping recruiter review, edits, overrides, and approval in the workflow before recommendations are shared.
- Demonstrating a practical CrewAI multi-agent workflow for recruitment.

## Goals And Success Metrics

### Product Goals

- Help recruiters find qualified candidates quickly.
- Improve consistency of candidate evaluation against job criteria.
- Provide ranked recommendations that hiring managers can review.
- Keep the mini-project scope focused enough for implementation in Module 06.
- Preserve human review; the assistant recommends candidates but does not make hiring decisions.

### Success Metrics

| Metric | Target For Mini-Project | Why It Matters |
| --- | --- | --- |
| Time to source candidates | Generate an initial candidate list within 2 minutes for seeded or approved candidate data. | Shows time savings compared with manual sourcing. |
| Candidate match accuracy | At least 80% of recommendations judged relevant in seeded test scenarios. | Shows the evaluator is matching candidates to job criteria. |
| Recruiter satisfaction | Recruiter rates output 4 out of 5 or higher in review/testing. | Confirms recommendations are useful and understandable. |
| Recommendation explainability | 100% of ranked candidates include a short rationale tied to job criteria. | Makes output reviewable by recruiter and hiring manager. |
| End-to-end completion | 95% successful runs in controlled test cases. | Confirms the mini-project workflow is reliable enough to demonstrate. |

## Business Value And ROI

The MVP should demonstrate measurable business value through recruiter productivity, recommendation quality, and hiring-manager trust. The mini-project does not need a full financial model, but it should make the value hypothesis testable.

### Business Outcomes

| Business outcome | Product metric | MVP target | Business rationale |
| --- | --- | --- | --- |
| Reduce recruiter time spent on first-pass sourcing and screening | Time to ranked shortlist | Ranked shortlist produced in under 15 minutes after candidate data is available; seeded data workflow under 2 minutes. | Frees recruiter time for human review, stakeholder alignment, and candidate engagement. |
| Reduce repetitive candidate writeup effort | Report readiness | 100% of ranked candidates include rationale, strengths, gaps, unknowns, confidence, and suggested next step. | Reduces manual documentation work and improves consistency of hiring-manager handoffs. |
| Improve consistency of candidate evaluation | Candidate match accuracy and evidence quality | At least 80% of recommendations judged relevant in seeded test scenarios, with 0 unsupported candidate facts in QA fixtures. | Makes comparisons more repeatable and reduces subjective or unsupported evaluation notes. |
| Improve hiring-manager confidence | Hiring-manager usefulness or recruiter proxy rating | Report or recommendation output rated 4 out of 5 or higher in review/testing. | Increases trust in recruiter recommendations and shortens review conversations. |
| Protect against automation risk | Human approval and AI-assisted disclosure | 100% of final recommendations require recruiter review and include AI-assisted disclosure. | Keeps the system positioned as decision support, not autonomous selection. |

### Value Hypotheses

- Time savings: recruiters should spend materially less time creating an initial shortlist and candidate summary when approved candidate data is available.
- Cost reduction: reduced manual screening and writeup time should lower effort per role run, especially for repeated or high-volume roles.
- Quality improvement: consistent criteria, evidence labels, and unknown handling should improve the clarity and defensibility of recommendations.
- Trust improvement: hiring managers should receive clearer ranked recommendations with visible strengths, gaps, caveats, and next steps.

### ROI Model For MVP Validation

The MVP ROI model should be calculated with simple operational assumptions:

`Estimated value = (manual shortlist time - assisted shortlist time) x recruiter hourly cost x number of role runs`

`Net ROI = estimated value - implementation and operating cost`

Baseline assumptions to validate:

- Manual first-pass shortlist preparation for a role with up to 10 candidates may take 60 to 120 minutes, including review and writeup.
- Assisted shortlist preparation should take under 15 minutes after candidate data is available.
- The MVP should show at least 50% time reduction for first-pass shortlist and report preparation in controlled testing.
- ROI is only defensible if time savings are achieved while maintaining recommendation relevance, source-backed rationale, and recruiter approval.

### Business Acceptance Criteria

- Recruiter can produce a reviewed shortlist faster than the baseline manual process in seeded test scenarios.
- At least 80% of recommendations are judged relevant by reviewer or fixture expectations.
- 100% of material candidate claims are source-backed, labeled as inference, or marked unknown.
- 100% of final recommendations require recruiter approval before use.
- Hiring-manager-ready output is clear enough to reduce rewrite effort in review/testing.

## Strategic Fit And Scope Rationale

The Recruitment Assistant fits an organization that wants to improve recruiting productivity while adopting AI in a controlled, explainable, human-reviewed way. For the current mini-project, the strategy is to prove a focused assisted-shortlist workflow before expanding into integrations, communications, or production compliance capabilities.

### Assumed Organizational Goals

- Increase recruiter productivity by reducing first-pass screening and candidate writeup effort.
- Improve consistency and explainability of candidate recommendations.
- Give hiring managers clearer, faster-to-review shortlists.
- Demonstrate a practical CrewAI multi-agent workflow with visible intermediate outputs.
- Preserve human oversight, approved data boundaries, and responsible AI positioning.

### MVP Strategy

The MVP should prove that a recruiter can move from job requirements and approved candidate data to a reviewed, explainable, ranked shortlist faster than the manual baseline. The product should prioritize depth and trust in this core workflow over broad recruiting platform coverage.

Strategic priorities:

- Make the end-to-end shortlist workflow work reliably with seeded or approved candidate data.
- Keep the recruiter in control through criteria review, candidate review, and final approval.
- Produce output that is useful to both recruiters and hiring managers.
- Measure time savings, recommendation relevance, evidence quality, and review usefulness.
- Avoid high-risk automation before the product proves value and receives legal or HR review.

### Scope Tiers

MVP must-have:

- Guided job requirement input.
- Required field validation and ambiguous requirement handling.
- Seeded, pasted, uploaded text, or otherwise approved candidate data source.
- Researcher, Evaluator, and Recommender agent workflow.
- Ranked shortlist with rationale, strengths, gaps, unknowns, confidence, and suggested next step.
- Recruiter review and approval before recommendations are used.
- AI-assisted disclosure and neutral, job-related candidate language.
- Core error handling for empty inputs, no candidates, malformed output, timeouts, unapproved sources, and low-confidence results.

MVP nice-to-have:

- Editable extracted criteria in the frontend.
- Editable recommendation notes or override controls in the frontend.
- Persistent run history or audit trail.
- Uploaded file parsing beyond plain text.
- Markdown, PDF, DOCX, or ATS-ready export formatting.
- Recruiter-adjustable score weights.

Future or explicitly out of scope for current mini-project:

- Full ATS integration.
- Automatic email, LinkedIn, SMS, or outreach sending.
- Direct candidate communication.
- Production-grade compliance workflows or bias audit certification.
- Advanced analytics and reporting.
- Interview scheduling, offer management, onboarding, payroll, or HRIS integration.
- Autonomous candidate rejection, advancement, or hiring decisions.

### Out-Of-Scope Rationale

The current out-of-scope items are appropriate because they carry higher business, legal, integration, and operational risk than the MVP needs to prove value. The project should avoid full ATS integration, automated outreach, autonomous hiring actions, and production compliance claims until the core workflow demonstrates measurable productivity and quality gains.

### Scope Guardrails

- Do not expand into candidate communication until recruiter-reviewed draft quality, disclosure language, and compliance expectations are defined.
- Do not implement autonomous candidate decisions; the system remains decision support.
- Do not depend on unauthorized scraping or unsupported data collection.
- Do not require ATS integration for the MVP to function.
- Do not treat persistent audit logging as a hard blocker for the mini-project if run output or handoff notes can represent review decisions.

## Risks, Constraints, And Compliance

The MVP should keep technical and business risk proportional to the mini-project timeline. The safest path is to prove the core workflow with seeded or approved plain-text candidate data before adding complex uploads, integrations, automation, or production compliance commitments.

### Technical Constraints

- Candidate data source: MVP should prioritize seeded data, pasted profiles, uploaded plain text, or explicitly approved APIs.
- File handling: PDF, DOCX, and CSV parsing are nice-to-have unless explicitly approved for the current module.
- Persistence: full database-backed run history and audit logs are nice-to-have for the mini-project; run output or handoff notes may represent review and approval decisions.
- Integrations: ATS, email, LinkedIn, SMS, calendar, HRIS, and payroll integrations are out of scope.
- Runtime reliability: agent/model timeouts and malformed outputs must fail safely with controlled messages and preserved user inputs where possible.
- Model output quality: agent outputs must be structured enough for frontend presentation and QA validation.

### Business Constraints

- Business timeline: MVP scope should fit the current module/demo timeline and avoid features that require procurement, vendor approval, or long security review.
- Operating cost: model, hosting, storage, and third-party API costs should remain low enough for controlled testing; ROI is not validated until operating cost assumptions are known.
- Stakeholder availability: recruiter, hiring-manager, HR, legal, or compliance reviewers may be needed to validate personas, baseline time, disclosure language, and real-candidate pilot readiness.
- Data availability: business value testing depends on representative seeded data or approved candidate data that reflects target roles.
- Adoption risk: recruiter workflow changes should remain lightweight, because high-friction review or approval steps may reduce usage even if model output is strong.

### Compliance And Regulatory Considerations

The MVP is not production compliance certified. If the system is used with real candidates or in real hiring workflows, legal and HR review is required before pilot or launch.

Key considerations:

- Candidate data privacy, retention, access control, and deletion expectations.
- Approved sourcing boundaries and third-party terms of service.
- Avoiding protected attributes and unsupported sensitive data in scoring.
- Automated Employment Decision Tool obligations in applicable jurisdictions.
- Bias, fairness, and adverse impact review before production use.
- Candidate or employee notice requirements where applicable.
- Auditability of generated recommendations, recruiter edits, overrides, approvals, and exports.
- AI-assisted disclosure language in UI and reports.

### Risk Matrix

| Risk | Business impact | Mitigation |
| --- | --- | --- |
| MVP does not reduce time to shortlist | Weak ROI, low recruiter adoption, and limited stakeholder support. | Measure manual baseline, target at least 50% time reduction, and keep workflow focused on must-have scope. |
| Recommendations are not relevant enough | Recruiters lose trust and need to redo the work manually. | Use seeded QA fixtures, require 80% relevance target, and preserve recruiter review/approval. |
| Candidate claims are unsupported or hallucinated | Reputational, compliance, and trust risk. | Require source-backed rationale, inference labels, unknown handling, and QA checks for unsupported facts. |
| Output is not explainable to hiring managers | Recommendations are rejected or require heavy rewrite. | Require strengths, gaps, unknowns, confidence, rationale, and report-ready summary. |
| Workflow fails or times out frequently | Demo credibility and user confidence decline. | Handle timeouts, malformed outputs, and empty states with controlled errors and retry paths. |
| System appears to make autonomous hiring decisions | Legal/compliance risk and stakeholder resistance. | Require human approval, AI-assisted disclosure, and decision-support language throughout the workflow. |
| Candidate language is subjective or inappropriate | Brand, fairness, and candidate-trust risk. | Enforce neutral, job-related, evidence-based tone and QA language review. |
| Operating costs exceed expected value | ROI becomes weak even if the workflow functions. | Track model/runtime cost assumptions and compare them against measured recruiter time savings. |
| Stakeholders are unavailable for validation | Personas, baseline assumptions, and disclosure language remain unproven. | Identify pilot reviewers early and keep unvalidated items in open questions. |
| Scope expands into integrations or compliance prematurely | Timeline risk and reduced chance of completing core MVP. | Keep ATS, outreach, production compliance, and advanced exports out of scope until core value is proven. |

### Business Decision Gates

- Continue MVP build if seeded or approved-data workflow can produce a ranked shortlist within the target timeframe.
- Rework product scope if reviewer-rated recommendation relevance falls below 80% in controlled scenarios.
- Block real-candidate pilot until approved data sources, retention expectations, disclosure language, and legal/HR review are complete.
- Do not expand into ATS integration, outreach, or production compliance until the core workflow meets time savings, evidence quality, and recruiter-review targets.
- Do not treat ROI as validated until manual baseline time, recruiter cost assumptions, and role-run volume are confirmed with target stakeholders.

## User Personas

### Primary Persona: Recruiter

The recruiter needs to find qualified candidates quickly and produce an initial shortlist for a role.

Needs:

- Enter or paste job requirements.
- Source candidate options from approved data.
- Evaluate candidate fit without manually reading every profile in depth.
- See why each candidate is recommended.
- Review criteria, evidence, scores, gaps, and unknowns before using recommendations.
- Override or approve AI-assisted recommendations before sharing.
- Share ranked recommendations with a hiring manager.

Pain points:

- Manual candidate sourcing is time-consuming.
- Candidate data is often inconsistent or spread across sources.
- Comparing candidates manually can be subjective.
- Writing candidate summaries and recommendations is repetitive.

Success outcome:

- The recruiter receives a ranked shortlist with clear rationale and can decide which candidates to review further.
- The recruiter remains in control of final recommendations through review, edits, overrides, and approval.

### Secondary Persona: Hiring Manager

The hiring manager needs ranked candidate recommendations that are easy to review and tied to the job requirements.

Needs:

- Understand candidate strengths and gaps.
- Review a ranked shortlist rather than raw candidate data.
- See concise recommendation rationale.
- Provide feedback to the recruiter.

Pain points:

- Candidate notes are often inconsistent.
- Recommendations may not clearly map to role criteria.
- Reviewing a large candidate pool takes too much time.

Success outcome:

- The hiring manager can quickly identify the strongest candidates to interview or discuss.

### Future Stakeholder Persona: HR Or Talent Operations Lead

The HR or talent operations lead needs repeatable, governed recruiting workflows that can scale across roles and recruiters.

Needs:

- Consistent evaluation criteria across similar roles.
- Clear audit trail of generated recommendations, recruiter edits, overrides, and approvals.
- Confidence that candidate data is handled through approved sources.
- Reports that support oversight without replacing recruiter judgment.

Pain points:

- Recruiting quality can vary across teams and roles.
- AI-assisted hiring tools may create compliance, fairness, privacy, or auditability concerns.
- High-volume recruiting makes it difficult to maintain consistent documentation.

Success outcome:

- The HR or talent operations lead can understand how recommendations were produced and confirm that the workflow preserves human review and approved data boundaries.

## User Interaction Model

The MVP should provide a guided recruiter workflow, not only a backend/API flow. The interface may be implemented as a compact web UI or chat-like guided flow, but it must make the recruiter checkpoints explicit.

### Job Requirement Input

Recruiters should input job requirements through a guided form with a free-text job description area and optional structured fields. A chat-like wrapper may be used, but the underlying interaction should still capture clear fields for downstream agents.

Minimum MVP input fields:

- Job title.
- Job description or role summary.
- Required skills.
- Preferred skills.
- Seniority level, if known.
- Location, remote, hybrid, or onsite constraints, if known.
- Candidate source selection, such as seeded dataset, pasted profiles, uploaded text, or approved source.

Input behavior:

- Job title and job description are required for the MVP.
- Required skills and preferred skills may be manually entered or extracted from the job description.
- The system should show extracted criteria before candidate evaluation starts.
- The recruiter should be able to confirm criteria before continuing.
- If criteria editing is not implemented in the first UI, the system must still show the extracted criteria and include a clear review checkpoint.

Primary interaction steps:

1. Recruiter enters or pastes job requirements, including title, description, required skills, preferred skills, and location or remote constraints when available.
2. System extracts or receives role criteria and shows them for recruiter review.
3. Recruiter confirms candidate input source, such as seeded data, pasted candidate profiles, uploaded text, or another approved source.
4. Researcher Agent returns candidate options with profile summaries, source labels, and missing data notes.
5. Recruiter reviews the candidate list before evaluation continues when candidate data is user-provided or ambiguous.
6. Evaluator Agent evaluates candidates against the reviewed criteria and labels strengths, gaps, confidence, and unknowns.
7. Recommender Agent ranks candidates and produces a concise shortlist with rationale and suggested next steps.
8. Recruiter reviews, edits, overrides, or approves the final shortlist before sharing with a hiring manager.

### Recommendation Presentation

Recommendations should be presented in layers so recruiters can scan quickly and inspect evidence when needed.

Primary presentation layers:

- Ranked shortlist: compact list of candidates ordered by fit, with rank, fit label or score, short rationale, confidence, and suggested next step.
- Candidate detail view: expanded candidate view with strengths, gaps, unknowns, source labels, evidence confidence, and criterion-by-criterion assessment.
- Hiring-manager report: concise approved summary that includes the ranked shortlist, rationale, caveats, and AI-assisted disclosure.

Minimum MVP output format:

- Candidate rank or fit label.
- Candidate name or identifier.
- Short profile summary.
- Strengths tied to job criteria.
- Gaps or risks tied to job criteria.
- Unknown or missing information.
- Evidence confidence.
- Concise recommendation rationale.
- Suggested next step.
- AI-assisted disclosure and recruiter-review requirement.

### Ambiguous Requirement Handling

The system should treat ambiguous role requirements as a recruiter-review moment, not as a silent inference.

Examples of ambiguity:

- Seniority is missing or inconsistent.
- Required and preferred skills are mixed together.
- Location or work arrangement is missing.
- Criteria are too broad, such as "good engineer" or "strong communicator."
- Job description conflicts with structured fields.
- The role description is too short to support reliable evaluation.

Expected behavior:

- The system identifies ambiguous criteria and labels them as inferred, low confidence, or needs review.
- The system asks the recruiter to confirm or clarify blocking ambiguity before evaluation when possible.
- If the MVP cannot support interactive clarification, the system may continue only with visible caveats in the criteria review, evaluation output, and final recommendation.
- The Evaluator Agent must not penalize candidates for criteria that are unknown, ambiguous, or not job-related.
- The final shortlist must identify material assumptions that affected ranking.

### Error And Edge Case Handling

Errors should be recoverable and written in recruiter-friendly language. The system should preserve user-entered job and candidate data where possible.

Required MVP edge cases:

| Scenario | Expected behavior |
| --- | --- |
| Empty job title or description | Block workflow and ask recruiter to provide the missing required field. |
| Very short or vague job description | Show low-confidence criteria and ask for clarification or confirmation before evaluation. |
| No candidates found | Explain that no candidate options were found and suggest refining criteria or adding candidate data. |
| Candidate profile lacks evidence | Mark missing details as unknown and avoid unsupported claims. |
| Candidate source is not approved | Block sourcing from that source and ask the recruiter to use seeded, pasted, uploaded, or approved data. |
| Agent or model timeout | Show a retryable error and preserve submitted inputs. |
| Malformed agent output | Show a controlled failure message and avoid displaying partial unsupported recommendations. |
| All candidates have low confidence | Present results as low-confidence, explain why, and require recruiter review before approval. |
| Conflicting criteria | Flag the conflict and require recruiter confirmation or visible caveat before evaluation. |
| Sensitive or unsupported data appears in input | Warn the recruiter and avoid using unsupported sensitive attributes in scoring. |

## Brand And Voice

The Recruitment Assistant should represent the product as a professional, transparent, and recruiter-controlled decision-support tool. Agent outputs should sound helpful and evidence-based, not authoritative or judgmental.

### Brand Experience Principles

- Human-in-the-loop: the product supports recruiter judgment and does not make autonomous hiring decisions.
- Evidence-first: material claims about candidates should be tied to supplied candidate data, source labels, or explicit unknowns.
- Job-related: evaluations should focus on role criteria, skills, experience, constraints, and evidence quality.
- Respectful toward candidates: candidate descriptions should be neutral, fair, and professional.
- Privacy-aware: candidate data should be treated as sensitive and sourced only from approved inputs.
- Transparent about uncertainty: missing, ambiguous, inferred, or low-confidence information should be labeled clearly.

### Agent Tone Guidelines

All application agents should use a tone that is:

- Professional and concise.
- Consultative rather than directive.
- Neutral and non-judgmental.
- Clear about confidence, caveats, and unknowns.
- Focused on recruiter next steps.
- Suitable for recruiter and hiring-manager review.

Agents should avoid:

- Presenting recommendations as final hiring decisions.
- Using subjective labels such as "bad fit," "weak candidate," "poor culture fit," or "top talent" without job-related evidence.
- Inferring personal traits, protected attributes, compensation expectations, availability, or intent unless supplied by approved candidate data.
- Making claims that are not supported by the candidate profile or approved source.
- Using overly casual, promotional, or sales-like language in evaluation outputs.

### Candidate Representation Guidelines

The MVP does not include direct candidate communication. Agents should not send emails, LinkedIn messages, SMS, or other outreach to candidates.

Any candidate-facing content in future releases must be draft-only until reviewed and approved by a recruiter. Candidate descriptions in reports should:

- Refer to candidates by name or identifier without unnecessary personal details.
- Describe fit in relation to job criteria rather than personal worth.
- Use terms such as "strong evidence," "partial evidence," "gap," "unknown," and "requires recruiter review."
- Avoid language that implies rejection, advancement, or employment eligibility decisions.

### Recommended Disclosure Language

The exact legal copy remains an open question, but MVP outputs should include a short disclosure similar to:

"These recommendations are AI-assisted decision support based on the supplied job criteria and candidate data. A recruiter must review and approve all recommendations before they are used in a hiring process."

## Core Features

### CF1: Candidate Search Based On Job Requirements

The assistant uses job requirements to identify or retrieve candidate options from approved sources.

Mini-project implementation options:

- Seeded candidate dataset.
- User-provided candidate list.
- Uploaded candidate profile text.
- Approved search/API tool if available.

Acceptance criteria:

- Given a job requirement, when the search step runs, then the system returns candidate options relevant to the role.
- Given candidate data is sourced, then the system stores or displays candidate name, profile summary, relevant skills, and source.
- Given no candidates are found, then the system returns a clear message and suggests refining job criteria or adding candidate data.

### CF2: Automated Candidate Evaluation

The assistant evaluates each candidate against the job criteria.

Evaluation dimensions:

- Required skills match.
- Relevant experience.
- Seniority alignment.
- Domain or industry relevance.
- Location or work constraints, if provided.
- Evidence confidence.

Acceptance criteria:

- Given a candidate and job criteria, when evaluation runs, then the system produces a fit assessment.
- Each assessment includes strengths, gaps, and a concise rationale.
- The system should mark unknown information as unknown rather than inventing candidate facts.

### CF3: Ranked Candidate Recommendations

The assistant ranks evaluated candidates and provides recommendations.

Acceptance criteria:

- Given multiple evaluated candidates, when recommendation runs, then candidates are sorted by fit.
- Each ranked candidate includes score or rank, rationale, strengths, gaps, and suggested next step.
- The output makes clear that recommendations are AI-assisted and require recruiter review.

### CF4: Recruiter Review, Override, And Approval

The assistant keeps the recruiter in control before recommendations are shared or exported.

Acceptance criteria:

- Given extracted role criteria, when they are displayed to the recruiter, then the recruiter can review them before evaluation.
- Given evaluated candidates, when results are displayed, then strengths, gaps, unknowns, and evidence confidence are visible.
- Given ranked recommendations, when the recruiter reviews them, then the recruiter can approve, reject, or override recommendation notes before sharing.
- Given an override or approval, then the system records the human decision in the run output or handoff notes.
- Given final output, then it states that recommendations are AI-assisted decision support and not an autonomous hiring decision.

### CF5: Job Posting System Integration

Integration with job posting systems is optional for this mini-project.

Possible future integration behavior:

- Import job requirements from a job posting system.
- Export ranked recommendations back to a recruiting workflow.
- Sync job title, description, requirements, and location.

Mini-project acceptance criteria:

- If implemented, integration should be read-only or export-only.
- If not implemented, the product should still work through manual job requirement input.

## Application Crew Definition

The application crew is the AI agent team responsible for the recruitment assistant workflow.

### Researcher Agent

Role: Searches and sources candidates.

Goal:

- Find candidate options that may match the provided job requirements.

Inputs:

- Job title.
- Job description.
- Required skills.
- Preferred skills.
- Location or remote constraints.
- Candidate data sources or seeded dataset.

Outputs:

- Candidate list.
- Candidate profile summaries.
- Source references or source labels.
- Missing data notes.

Responsibilities:

- Interpret the job requirements.
- Search approved sources or seeded data for possible candidates.
- Return candidates with enough information for evaluation.
- Avoid unauthorized scraping or unsupported data collection.

### Evaluator Agent

Role: Evaluates candidates against job criteria.

Goal:

- Assess each candidate's fit for the role using consistent criteria.

Inputs:

- Job criteria.
- Candidate profiles from the Researcher Agent.

Outputs:

- Candidate fit assessments.
- Strengths and gaps.
- Component scores or qualitative fit ratings.
- Evidence confidence.

Responsibilities:

- Compare each candidate against required and preferred criteria.
- Identify strong matches and missing information.
- Avoid making unsupported claims.
- Produce evaluation output that a recruiter can review.

### Recommender Agent

Role: Provides ranked recommendations.

Goal:

- Turn candidate evaluations into a prioritized shortlist for recruiter and hiring manager review.

Inputs:

- Candidate evaluations from the Evaluator Agent.
- Job criteria.

Outputs:

- Ranked candidate shortlist.
- Recommendation rationale.
- Suggested next steps.
- Hiring-manager-friendly summary.

Responsibilities:

- Rank candidates by overall fit.
- Explain why top candidates are recommended.
- Highlight caveats and unknowns.
- Present output as decision support, not a final hiring decision.

## Development Crew Mapping

The development crew maps AAMAD project personas to the modules and responsibilities needed to build the mini-project.

### Product Manager

Owner: Current Define phase.

Responsibilities:

- Define product scope and value proposition.
- Produce MRD and PRD.
- Clarify personas, core features, success metrics, and out-of-scope items.
- Maintain open questions for stakeholder review.

Current artifacts:

- `project-context/1.define/mrd.md`
- `project-context/1.define/prd.md`
- `project-context/1.define/open-questions.md`

### System Architect

Owner: Module 06 architecture work.

Responsibilities:

- Define the system architecture for the recruitment assistant.
- Map the Researcher, Evaluator, and Recommender agents into backend components.
- Specify data flow, storage, API boundaries, and runtime assumptions.
- Update the SAD when architecture decisions are made.

Expected artifact:

- `project-context/1.define/sad.md`

### Project Manager

Owner: Build-phase setup and work sequencing.

Responsibilities:

- Scaffold the project environment and implementation directories.
- Confirm Build-phase prerequisites, dependency manifests, and environment variables.
- Sequence frontend, backend, integration, and QA workstreams.
- Maintain setup and handoff notes so implementation agents can work from the approved PRD scope.

Expected artifact:

- Updates to `project-context/2.build/setup.md`.

### Backend Engineer

Owner: Module 06 backend implementation.

Responsibilities:

- Implement the application crew workflow.
- Build candidate sourcing/search logic using seeded or approved data.
- Implement candidate evaluation and ranking endpoints/services.
- Persist or return intermediate outputs needed for review.
- Add backend tests for core workflow behavior.

Expected artifacts:

- Backend code and tests.
- Updates to `project-context/2.build/backend.md`.

### Frontend Engineer

Owner: Module 06 frontend implementation for the guided MVP user flow.

Responsibilities:

- Implement the guided recruiter workflow for job input, candidate source selection, criteria review, and recommendation review.
- Present ranked shortlist, candidate detail, confidence, caveats, and report-ready summary in a recruiter-friendly format.
- Make human review and approval checkpoints visible.
- Preserve brand and voice guidelines in UI copy and generated-output presentation.
- Document frontend decisions and verification results.

Expected artifact:

- Updates to `project-context/2.build/frontend.md`.

### Integration Engineer

Owner: Module 06 integration work.

Responsibilities:

- Connect frontend or caller workflow to backend recruitment assistant APIs.
- Ensure job requirement input flows into the Researcher Agent.
- Ensure candidate evaluations flow into the Recommender Agent.
- Validate end-to-end flow from job input to recruiter-approved ranked recommendations.
- Document integration decisions and smoke test results.

Expected artifact:

- Updates to `project-context/2.build/integration.md`.

### QA Engineer

Owner: Module 06 validation and regression coverage.

Responsibilities:

- Validate the end-to-end flow from job requirement input to recruiter-approved recommendations.
- Test required inputs, ambiguous requirements, edge cases, safe failure behavior, and approved-source boundaries.
- Verify that candidate claims are source-backed, labeled as inference, or marked unknown.
- Verify that generated recommendations use neutral, job-related, evidence-based language.
- Document QA scenarios, results, known gaps, and residual risks.

Expected artifact:

- Updates to `project-context/2.build/qa.md`.

## Out Of Scope For This Mini-Project

The following capabilities are intentionally out of scope:

- Full ATS integration.
- Candidate communication automation.
- Automatic email, LinkedIn, SMS, or outreach sending.
- Advanced analytics and reporting.
- Bias audit certification.
- Production-grade compliance workflows.
- Background checks.
- Interview scheduling.
- Offer management.
- Onboarding.
- Payroll or HRIS integration.
- Autonomous candidate rejection, advancement, or hiring decisions.

## Functional Requirements

### FR1: Job Requirement Input

The user can provide job requirements as free text or structured fields.

Acceptance criteria:

- The system accepts a job title and job description.
- The system extracts or receives required skills and preferred skills.
- The workflow cannot proceed if the job requirement is empty.

### FR2: Candidate Search Or Source Step

The system uses job requirements to source candidate options.

Acceptance criteria:

- The Researcher Agent returns a candidate list from approved data.
- The candidate list includes enough information for evaluation.
- The system handles empty results gracefully.

### FR3: Candidate Evaluation Step

The system evaluates candidates against job criteria.

Acceptance criteria:

- The Evaluator Agent produces an assessment for each candidate.
- Each assessment includes strengths, gaps, and fit rationale.
- Unknown or missing information is labeled clearly.

### FR4: Recommendation Step

The system ranks candidates based on evaluation output.

Acceptance criteria:

- The Recommender Agent returns a ranked shortlist.
- Each recommendation includes rationale and suggested next step.
- The output states that recruiter review is required.

### FR5: Recruiter Review And Approval Step

The user can review AI-assisted outputs before final recommendations are shared.

Acceptance criteria:

- The system exposes extracted role criteria for review before or alongside evaluation.
- The system exposes candidate strengths, gaps, unknowns, and evidence confidence.
- The system allows the recruiter to approve the final shortlist in the MVP output.
- If edit or override controls are implemented in the UI, the final output preserves the recruiter-edited version.
- If full edit controls are not implemented, the output must still include a clear approval/review checkpoint and handoff notes for manual edits.

### FR6: Optional Job Posting Integration

The system may optionally import job requirements from or export results to a job posting workflow.

Acceptance criteria:

- The core workflow works without this integration.
- If implemented, integration does not block manual input.

### FR7: Ambiguity, Error, And Edge Case Handling

The system handles unclear requirements, missing data, invalid sources, and agent failures without producing unsupported recommendations.

Acceptance criteria:

- Given ambiguous job requirements, when criteria are extracted, then ambiguous criteria are labeled for recruiter review.
- Given conflicting role criteria, when the workflow runs, then the system flags the conflict before or alongside evaluation.
- Given missing candidate evidence, when evaluation runs, then missing facts are marked as unknown.
- Given an unapproved candidate source, when sourcing is requested, then the workflow blocks that source and explains acceptable alternatives.
- Given an agent timeout or malformed output, when the workflow fails, then the system returns a controlled error message and preserves submitted inputs where possible.
- Given low-confidence results across all candidates, when recommendations are presented, then the output clearly states that confidence is low and requires recruiter review before approval.

### FR8: Brand Voice And Candidate Representation

The system communicates recommendations in a professional, evidence-based, recruiter-controlled voice.

Acceptance criteria:

- Given any agent output, when candidate fit is described, then language is neutral, job-related, and evidence-based.
- Given a recommendation, when the output is shown, then it avoids presenting the AI as the final hiring decision-maker.
- Given missing or inferred information, when the output is shown, then uncertainty is labeled instead of stated as fact.
- Given a candidate has gaps, when they are described, then the output frames gaps against role criteria rather than personal judgment.
- Given final output, when it is shared or report-ready, then it includes an AI-assisted decision-support disclosure and recruiter-review requirement.
- Given the MVP workflow, when candidate communication would be needed, then the system does not send outreach and keeps any future candidate-facing content draft-only.

## Non-Functional Requirements

### Usability

- The workflow should be understandable to a recruiter without technical knowledge.
- The MVP should support a guided frontend or chat-like interaction for role input, candidate source selection, and result review.
- Candidate recommendations should be concise and easy to scan.
- The system should show enough rationale for a hiring manager to understand the ranking.
- The system should make recruiter checkpoints visible instead of presenting the crew workflow as an opaque automated run.
- Error and ambiguity messages should explain what happened, why it matters, and what the recruiter can do next.

### Brand And Voice Quality

- Agent outputs should be professional, concise, neutral, and evidence-based.
- Candidate descriptions should be respectful and focused on role criteria.
- The system should consistently communicate that outputs are AI-assisted and require recruiter review.
- The system should avoid unsupported subjective language and claims about candidate personal traits.

### Reliability

- The workflow should handle missing candidates, incomplete candidate data, and empty job requirements.
- Failures should return actionable error messages.
- The system should preserve user inputs when possible.

### Security And Data Boundaries

- Candidate data should be treated as sensitive.
- The mini-project should avoid unauthorized scraping.
- API keys or model credentials must not be exposed to the frontend.

### Performance

- The mini-project should return a ranked shortlist within a reasonable demo timeframe.
- Target end-to-end time for seeded data: under 2 minutes.

## Recommended MVP Flow

1. User enters job requirements.
2. System validates required fields and flags vague, conflicting, or incomplete requirements.
3. System extracts or receives role criteria and shows them for recruiter review.
4. User confirms candidate source from seeded, pasted, uploaded, or otherwise approved data.
5. Researcher Agent finds or selects candidate options from approved data.
6. User reviews the candidate list when source data is user-provided or ambiguous.
7. Evaluator Agent evaluates each candidate against reviewed criteria.
8. Recommender Agent ranks candidates and produces rationale.
9. System presents a ranked shortlist with expandable candidate detail and report-ready summary.
10. User reviews, edits or overrides where supported, and approves ranked recommendations before sharing.

## Sources

- CrewAI Docs, "CrewAI Examples," lists Recruitment as "Candidate sourcing and evaluation": https://docs.crewai.com/en/examples/example
- CrewAI Examples GitHub repository: https://github.com/crewAIInc/crewAI-examples
- CrewAI recruitment example README and setup notes: https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment
- CrewAI recruitment agents configuration: https://raw.githubusercontent.com/crewAIInc/crewAI-examples/main/crews/recruitment/src/recruitment/config/agents.yaml
- CrewAI recruitment tasks configuration: https://raw.githubusercontent.com/crewAIInc/crewAI-examples/main/crews/recruitment/src/recruitment/config/tasks.yaml

## Assumptions

- This PRD describes a mini-project, not a full production recruiting platform.
- Candidate data will come from seeded data, user-provided data, uploads, or approved APIs.
- The first implementation can work without ATS or job posting integration.
- The ranked shortlist is advisory and requires recruiter review.
- The MVP includes a guided frontend or chat-like user flow, even if the backend remains the primary implementation focus.
- Full audit logging may be represented in run output or handoff notes for the mini-project if persistent storage is not implemented.
- Module 06 will cover architecture, frontend, backend, integration, and QA work.

## Key Open Questions

The canonical open-question log lives in `project-context/1.define/open-questions.md`. The PRD tracks only the questions most likely to affect scope, business validation, architecture, or release readiness.

### Product And Strategy

- Which organizational goal is primary for this project: internal productivity, CrewAI technical showcase, commercial MVP validation, or responsible AI governance pilot?
- Who is the first pilot audience and which stakeholders will validate personas, terminology, baseline time, output usefulness, and disclosure language?
- Which MVP nice-to-have items should be pulled into scope only if time remains?

### Data, Compliance, And Governance

- Will Module 06 use seeded candidate data, live search, uploaded profiles, or a combination?
- Which candidate data sources, file formats, retention expectations, and source-reference formats are approved for MVP or pilot use?
- Which compliance or regulatory requirements apply if real candidate data is used in testing or pilot workflows?
- What legal or HR-reviewed AI-assisted disclosure language should appear in the UI and final report?

### Implementation And UX

- Should candidate ranking use numeric scores, qualitative labels, or both?
- What candidate fields are required for the first backend implementation?
- Should the first frontend implement editable criteria and recommendation notes, or only review/approval checkpoints?
- Which clarification questions should be mandatory before evaluation versus represented as caveats?

### Business Validation

- What is the actual manual baseline time for first-pass shortlist and report preparation for target pilot users?
- What recruiter hourly cost, operating cost, and minimum improvement threshold should be used for ROI modeling?
- Which success metric failures should block pilot expansion versus trigger iteration within the mini-project?

## Verification

- PRD revised on May 11, 2026 to match requested mini-project coverage.
- Scope now emphasizes product overview, goals/metrics, personas, core features, application crew, development crew mapping, and out-of-scope items.
- Requirements preserve human review and approved data-source boundaries.
- UX alignment review completed on May 11, 2026.
- PRD now defines a guided interaction model, recruiter review checkpoints, minimum recommendation output format, and HR/talent operations as a future stakeholder persona.
- Interaction design review completed on May 11, 2026.
- PRD now defines job requirement input fields, layered recommendation presentation, ambiguous requirement handling, and required error/edge case behavior.
- Brand and voice review completed on May 11, 2026.
- PRD now defines brand experience principles, agent tone guidelines, candidate representation rules, and MVP disclosure language.
- Business value alignment review completed on May 11, 2026.
- PRD now defines business outcomes, value hypotheses, MVP ROI model, baseline assumptions, and business acceptance criteria.
- Strategic fit review completed on May 11, 2026.
- PRD now defines assumed organizational goals, MVP strategy, scope tiers, out-of-scope rationale, and scope guardrails.
- Risk and constraints review completed on May 11, 2026.
- PRD now defines technical constraints, compliance considerations, risk matrix, and business decision gates.
- Cohesion and organization review completed on May 11, 2026.
- PRD now has consolidated open questions, aligned development crew handoffs, and a single review summary table.

### Review Summary

| Review area | PRD status | Remaining validation |
| --- | --- | --- |
| UX alignment | Complete for PRD | Validate personas and terminology with real recruiters, hiring managers, or HR/talent operations stakeholders. |
| Interaction design | Complete for PRD | Confirm which clarification questions require blocking user input versus visible caveats. |
| Brand and voice | Complete for PRD | Replace generic MVP voice guidelines with organization-approved wording when available. |
| Business value | Partially complete | Validate manual baseline time, recruiter cost, operating cost, role-run volume, and minimum ROI threshold. |
| Strategic fit | Partially complete | Confirm the primary organizational goal and protect must-have scope from nice-to-have expansion. |
| Risks, constraints, and compliance | Complete for PRD | Legal/HR review is required before using real candidate data or real hiring workflows. |

## Handoff Notes

- Product Manager has completed the Define-phase PRD revision.
- System Architect should use this PRD to produce Module 06 architecture.
- Backend Engineer should implement the Researcher, Evaluator, and Recommender workflow using approved or seeded data.
- Frontend Engineer should implement a guided recruiter flow with visible checkpoints for role criteria, candidate source, evaluation review, and recommendation approval.
- Integration Engineer should verify the end-to-end path from job input to recruiter-approved ranked recommendations.
- QA Engineer should validate required input handling, ambiguous criteria handling, approved-source boundaries, low-confidence outputs, and controlled failure behavior.
- QA Engineer should also validate that generated recommendations use neutral, evidence-based, job-related language and include the AI-assisted disclosure.
- Product Manager should validate manual baseline time, recruiter cost assumptions, and minimum ROI threshold with target pilot stakeholders.
- Product Manager should confirm the primary organizational goal and protect MVP must-have scope from nice-to-have expansion unless time remains.
- System Architect and QA Engineer should treat timeout handling, malformed output handling, source-backed rationale, and safe failure behavior as required MVP safeguards.
- Product Manager should block real-candidate pilot use until legal/HR review, approved data source rules, retention expectations, and disclosure language are confirmed.
- Product Manager should validate operating cost assumptions and stakeholder availability before treating ROI or strategic alignment as fully confirmed.
