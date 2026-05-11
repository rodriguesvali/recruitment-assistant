# AAMAD Epics Index

| Epic | Persona | Primary Artifact | Typical Inputs | Invocation Cue |
| --- | --- | --- | --- | --- |
| Discovery | Product Manager | `project-context/1.define/mrd.md` | user idea, research, market notes | define market |
| Requirements | Product Manager | `project-context/1.define/prd.md` | MRD, user goals, constraints | define product |
| Architecture | System Architect | `project-context/1.define/sad.md` | PRD, repo, constraints | create architecture |
| Feature Spec | System Architect | `project-context/1.define/sfs/<feature-id>.md` | PRD/SAD, user story | create SFS |
| Setup | Project Manager | `project-context/2.build/setup.md` | PRD/SAD, repo inspection | setup project |
| Frontend | Frontend Engineer | `project-context/2.build/frontend.md` | PRD/SAD/setup | build UI |
| Backend | Backend Engineer | `project-context/2.build/backend.md` | PRD/SAD/setup | build backend |
| Integration | Integration Engineer | `project-context/2.build/integration.md` | frontend/backend/setup | integrate flow |
| QA | QA Engineer | `project-context/2.build/qa.md` | build artifacts, acceptance criteria | verify |
| Release | DevOps Engineer | `project-context/3.deliver/release.md` | QA, deployment assumptions | prepare release |

## Rules

- Update this index when the project adds meaningful epics.
- Keep epic ownership clear and avoid mixing unrelated implementation slices.
- Record future work as deferred scope, not hidden failure.
