# Market Requirements Document: Recruitment Assistant

## Executive Summary

The Recruitment Assistant is an AI-powered multi-agent application that helps recruiting teams turn job requirements and approved candidate data into explainable candidate recommendations, outreach drafts, and recruiter-ready reports.

The product is based on the CrewAI recruitment example, which demonstrates a workflow with candidate research, candidate matching/scoring, outreach strategy, and reporting agents. The market version should preserve that multi-agent workflow while adding recruiter control, source traceability, human review, and compliance-aware product boundaries.

Recommended positioning: **a recruiter-controlled AI assistant that reduces manual candidate sourcing and evaluation work while improving the consistency, explainability, and scalability of candidate recommendations.**

## Problem Statement

### What Problem Does The Recruitment Assistant Solve?

Recruiters and hiring teams need to identify qualified candidates, evaluate fit, prepare outreach, and communicate recommendations to hiring managers. Today, this work is often manual and fragmented across job descriptions, resumes, profile pages, spreadsheets, ATS notes, email drafts, and hiring manager feedback.

The Recruitment Assistant solves this by providing a structured AI workflow that:

- Converts job requirements into clear evaluation criteria.
- Summarizes candidate profiles from approved data sources.
- Compares candidates against role requirements.
- Produces explainable fit scores and rationale.
- Drafts outreach strategies and messages.
- Generates hiring-manager-ready candidate reports.

The product does not replace recruiter judgment. It helps recruiters move faster while keeping humans responsible for review, edits, approvals, and final decisions.

### Why Manual Candidate Sourcing And Evaluation Is Inefficient

Manual recruitment workflows are inefficient because they require repeated context switching, subjective comparison, and time-consuming documentation.

Key inefficiencies include:

- **Unstructured role intake:** Job descriptions often mix responsibilities, must-have skills, nice-to-have skills, seniority expectations, location constraints, and hiring manager preferences in free text.
- **Fragmented candidate data:** Candidate information may live in resumes, ATS records, LinkedIn profiles, spreadsheets, referrals, recruiter notes, and email threads.
- **Slow profile review:** Recruiters must manually scan each profile, identify relevant evidence, and compare candidates against the role.
- **Inconsistent evaluation:** Different recruiters or hiring managers may weigh the same criteria differently unless a rubric is explicit.
- **Repetitive writeups:** Candidate summaries, score justifications, outreach messages, and hiring manager reports are often rewritten for every role.
- **Limited scalability:** High-volume roles make it difficult to maintain consistent, evidence-backed review quality across many candidates.
- **Weak traceability:** Manual notes may not clearly show why a candidate was recommended or what source evidence supported the recommendation.

These issues increase time-to-shortlist, reduce recommendation consistency, and make it harder for hiring managers to trust candidate recommendations.

## Target Users

### Recruiters Who Need To Find And Evaluate Candidates

Recruiters and sourcers are the primary users. They need to move from role requirements to a candidate shortlist quickly while maintaining quality and defensibility.

Core needs:

- Extract clear role criteria from job descriptions.
- Review candidate profiles faster.
- Compare candidates against consistent criteria.
- See evidence-backed rationale for each recommendation.
- Draft personalized outreach without starting from a blank page.
- Export candidate reports for hiring manager review.

Success outcome:

- A recruiter can produce a reviewed, explainable shortlist and outreach plan in minutes after candidate data is available.

### Hiring Managers Who Need Candidate Recommendations

Hiring managers need concise, credible recommendations that explain why candidates are worth interviewing.

Core needs:

- Understand how candidates map to role requirements.
- See strengths, gaps, caveats, and unknowns.
- Provide feedback on criteria and fit.
- Avoid reviewing inconsistent or overly generic candidate notes.

Success outcome:

- A hiring manager can quickly understand the recommendation rationale and decide which candidates to interview.

### HR Teams Managing High-Volume Recruitment

HR and talent acquisition teams managing high-volume hiring need repeatable, scalable workflows that keep candidate evaluation consistent.

Core needs:

- Standardize candidate evaluation across recruiters and roles.
- Reduce repetitive sourcing, screening preparation, and report-writing work.
- Maintain human review and audit trails.
- Support governance for AI-assisted hiring workflows.
- Scale candidate review without losing evidence quality.

Success outcome:

- HR teams can process more candidate profiles with more consistent review quality and clearer oversight.

## Market Opportunity

### Time Savings In Candidate Sourcing

Recruiting teams spend significant time converting job requirements into search criteria, reviewing candidate profiles, writing summaries, and preparing reports. AI can reduce this repetitive work by automating first-draft analysis and documentation.

The Recruitment Assistant creates time savings by:

- Structuring role criteria automatically.
- Summarizing candidate profiles.
- Highlighting relevant skills and experience.
- Identifying missing information.
- Drafting outreach and report content.
- Reusing a consistent workflow across roles.

Target MVP metric:

- Median time to reviewed shortlist under 15 minutes after candidate data is available.

### Improved Candidate Matching Accuracy

Manual evaluation can be inconsistent because criteria are often implicit or unevenly applied. An AI-powered workflow can improve matching quality by making the rubric explicit and applying it consistently across candidates.

The product improves candidate matching by:

- Separating required criteria from preferred criteria.
- Scoring candidates by visible components such as required skills, relevant experience, seniority alignment, domain fit, location/work constraints, and evidence confidence.
- Explaining each score with source-backed rationale.
- Marking unknowns instead of inventing candidate facts.
- Allowing recruiters to override scores and record human judgment.

Target MVP metrics:

- At least 80% of candidate rationales rated useful and source-backed by pilot recruiters.
- 0 unsupported candidate facts in seeded QA reports.
- 100% of material recommendation claims mapped to evidence, inference, or unknown labels.

### Scalability For High-Volume Recruitment

High-volume recruiting requires repeatable workflows that can evaluate many candidates without sacrificing consistency. Manual processes are difficult to scale because each additional candidate adds review, comparison, documentation, and communication overhead.

The Recruitment Assistant supports scalability by:

- Applying the same approved rubric to all candidates in a role.
- Producing consistent summaries and score rationales.
- Generating standardized reports.
- Persisting run history and intermediate agent outputs.
- Supporting future CSV, ATS, and approved sourcing integrations.
- Keeping humans in the approval loop while reducing repetitive analysis.

Target MVP metric:

- Successful end-to-end completion rate of 95% or higher in controlled testing for roles with up to 10 candidates.

## Competitive Landscape

### Existing ATS Platforms

Applicant Tracking Systems such as Greenhouse, Lever, Ashby, Workday, and SmartRecruiters help teams manage job postings, applications, candidate stages, interview workflows, and hiring records. Many ATS products are adding AI features for job descriptions, resume review, candidate communication, or workflow automation.

Strengths:

- System of record for recruiting workflows.
- Existing customer adoption.
- Candidate pipeline and compliance records.
- Integrations with job boards, calendars, and HR systems.

Limitations for this opportunity:

- AI features may be embedded inside broader ATS workflows rather than focused on transparent candidate evaluation.
- Smaller teams may not have the budget or implementation maturity for enterprise ATS platforms.
- Candidate rationale can still be inconsistent if recruiters manually write notes.
- Multi-agent reasoning and intermediate outputs are often hidden from users.

Opportunity:

- Position the Recruitment Assistant as a focused copilot that can generate explainable shortlists and reports, then integrate with ATS systems later.

### Manual Recruitment Processes

Many teams still rely on spreadsheets, recruiter notes, Boolean searches, resume folders, email drafts, and hiring manager calls.

Strengths:

- Flexible and familiar.
- Low tooling cost.
- Easy to adapt to unusual roles.
- Human judgment remains central.

Limitations:

- Slow candidate review and documentation.
- Inconsistent evaluation across recruiters.
- Hard to scale for high-volume roles.
- Limited auditability and source traceability.
- Repetitive outreach and report writing.

Opportunity:

- Preserve recruiter control while automating the repetitive work that makes manual processes slow.

### How An AI-Powered Multi-Agent System Differs

An AI-powered multi-agent system differs from both ATS-native automation and manual processes because it decomposes recruitment assistance into specialized, inspectable tasks.

The CrewAI-inspired workflow maps to four agent responsibilities:

- **Candidate Research / Criteria Agent:** Structures role requirements and summarizes approved candidate data.
- **Matcher and Scorer Agent:** Compares candidates against the rubric and explains fit.
- **Outreach Strategist Agent:** Drafts outreach strategy and candidate-specific message templates.
- **Reporter Agent:** Produces the final recruiter or hiring manager report.

Differentiators:

- **Specialized agents:** Each agent handles a defined part of the recruiting workflow.
- **Explainability:** Candidate scores include component rationale, evidence, caveats, and confidence.
- **Human-in-the-loop:** Recruiters review, edit, override, and approve recommendations.
- **Source traceability:** Material claims should map to candidate data, recruiter notes, inference labels, or unknowns.
- **Workflow scalability:** The same structured process can be reused across roles and candidate pools.
- **Production-safe boundaries:** The product should avoid unauthorized scraping and should not make final hiring decisions.

## Market Requirements

### MR1: Structured Role Criteria

The product must turn free-text job requirements into editable criteria and an approved evaluation rubric.

### MR2: Candidate Data From Approved Sources

The product must support manual entry, upload/import, seed data, or compliant connectors/APIs. It must not depend on unauthorized scraping or cookie-based account automation.

### MR3: Explainable Candidate Matching

The product must rank candidates using visible component scores, source-backed rationale, confidence, caveats, and unknowns.

### MR4: Recruiter Control

The product must allow recruiters to review, edit, override, and approve AI-generated summaries, scores, outreach drafts, and reports.

### MR5: Hiring Manager Reporting

The product must generate a concise report that explains candidate recommendations, evidence, strengths, gaps, outreach plan, and next steps.

### MR6: High-Volume Repeatability

The product must support repeatable workflows that can scale from small candidate lists to larger high-volume recruiting scenarios in future releases.

### MR7: Governance And Auditability

The product must record generated outputs, user edits, overrides, approvals, and exports so HR teams can review how recommendations were produced.

## Recommended MVP

1. Guided role intake with free-text paste and structured fields.
2. Criteria extraction with recruiter editing.
3. Candidate manual entry and upload/import from approved files.
4. Candidate summaries grounded in supplied data.
5. Explainable ranking with component scores, confidence, caveats, and reviewer overrides.
6. Outreach strategy and editable message drafts.
7. Recruiter-ready markdown report.
8. Basic run history and audit trail.

## Risks And Mitigations

| Risk | Severity | Mitigation |
| --- | --- | --- |
| AI scoring is perceived as final automated selection. | High | Position as decision support, require human approval, include AI-assisted disclosure. |
| Candidate facts are hallucinated or unsupported. | High | Require source-backed rationale, confidence labels, unknown handling, and seeded QA tests. |
| Unauthorized sourcing violates platform terms or privacy expectations. | High | Use only approved inputs and block cookie-based scraping or unsupported automation. |
| Recruiters over-rely on total scores. | Medium | Show component scores, evidence, caveats, and require review before export. |
| ATS vendors add similar AI features. | Medium | Differentiate on focused workflow, multi-agent transparency, and report quality. |
| High-volume workflows expose quality gaps. | Medium | Start with controlled candidate limits, measure completion/rationale quality, expand after validation. |

## Success Metrics

- Median time to reviewed shortlist under 15 minutes after candidate data is available.
- At least 80% of candidate rationales rated useful and source-backed by pilot recruiters.
- At least 60% of outreach drafts accepted with minor edits.
- Hiring manager report usefulness rating averages 4 out of 5 or higher.
- 100% of exported recommendations have explicit human approval.
- 0 unsupported candidate facts in seeded QA reports.
- 95% end-to-end run completion rate in controlled MVP testing.

## Sources

- CrewAI Docs, "CrewAI Examples," lists Recruitment as "Candidate sourcing and evaluation": https://docs.crewai.com/en/examples/example
- CrewAI Examples GitHub repository, official example collection and project patterns: https://github.com/crewAIInc/crewAI-examples
- CrewAI recruitment example README and setup notes: https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment
- CrewAI recruitment agents configuration: https://raw.githubusercontent.com/crewAIInc/crewAI-examples/main/crews/recruitment/src/recruitment/config/agents.yaml
- CrewAI recruitment tasks configuration: https://raw.githubusercontent.com/crewAIInc/crewAI-examples/main/crews/recruitment/src/recruitment/config/tasks.yaml
- LinkedIn, "The Future of Recruiting 2025": https://business.linkedin.com/talent-solutions/resources/future-of-recruiting
- SHRM, "The Role of AI in HR Continues to Expand": https://www.shrm.org/topics-tools/research/2025-talent-trends/ai-in-hr
- SHRM, "Candidate Ghosting and Employer Competition Are Fueling Talent Shortages": https://www.shrm.org/about/press-room/candidate--ghosting--and-employer-competition-are-fueling-talent
- NYC Department of Consumer and Worker Protection, Automated Employment Decision Tools: https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page
- U.S. EEOC, Employment Tests and Selection Procedures: https://www.eeoc.gov/laws/guidance/employment-tests-and-selection-procedures

## Assumptions

- Initial product is a web application with a guided/chat-like frontend and CrewAI-powered backend.
- Initial users are recruiters, hiring managers, and HR teams managing manual or high-volume recruiting workflows.
- Candidate data for MVP comes from manual entry, uploads, seed data, or compliant connectors/APIs.
- The MVP supports recommendation assistance and report generation, not autonomous selection.
- First release is English-language and United States-oriented unless stakeholders specify otherwise.

## Open Questions

- Which user segment is the first pilot: recruiters, hiring managers, HR high-volume teams, staffing agencies, or CrewAI evaluators?
- Which candidate data sources and file formats are approved for MVP?
- What candidate volume should the MVP support in one role run?
- Should reports export as markdown only for MVP, or also PDF/DOCX?
- Should recruiters customize score weights per role in MVP or later?
- What exact HR/legal disclosure language should appear in reports and UI?

## Verification

- MRD revised on May 11, 2026 to match requested coverage: problem statement, target users, market opportunity, and competitive landscape.
- CrewAI workflow claims are based on official CrewAI docs and the official CrewAI examples repository.
- Product recommendations are framed as assumptions pending stakeholder and legal review.

## Handoff Notes

- PRD should remain aligned with this MRD's focus on time savings, improved matching accuracy, and high-volume scalability.
- System Architect should review data-source boundaries, auditability, and whether scoring creates regulated automated decision-tool obligations.
- Backend Engineer should preserve the multi-agent workflow while avoiding unauthorized scraping.
- Frontend Engineer should emphasize recruiter review, evidence visibility, and hiring-manager-friendly recommendations.
