from __future__ import annotations

import re

from fastapi import HTTPException, status

from app.schemas.recruitment import CandidateProfile, CandidateSource, EvaluationCriteria, SourceType, WorkflowWarning


SEED_CANDIDATES: dict[str, list[CandidateProfile]] = {
    "backend_engineers": [
        CandidateProfile(
            candidate_id="cand_001",
            display_name="Avery Chen",
            profile_summary="Backend engineer with Python, FastAPI, API design, and agent workflow experience.",
            skills=["Python", "FastAPI", "PostgreSQL", "CrewAI", "API design"],
            experience=["Built production APIs", "Designed LLM workflow services", "Owned backend reliability work"],
            location="Remote US",
            source_labels=["seeded-data:backend_engineers"],
            missing_data=["Compensation expectations unknown"],
        ),
        CandidateProfile(
            candidate_id="cand_002",
            display_name="Jordan Patel",
            profile_summary="Full-stack engineer with Angular, TypeScript, Python services, and recruiting platform integrations.",
            skills=["Angular", "TypeScript", "Python", "FastAPI", "ATS integrations"],
            experience=["Built recruiter dashboards", "Integrated HR tooling APIs", "Created candidate review workflows"],
            location="Hybrid NYC",
            source_labels=["seeded-data:backend_engineers"],
            missing_data=["Remote availability unknown"],
        ),
        CandidateProfile(
            candidate_id="cand_003",
            display_name="Morgan Rivera",
            profile_summary="Data-oriented engineer with strong evaluation, scoring, and reporting experience.",
            skills=["Python", "Data pipelines", "Evaluation design", "SQL", "Reporting"],
            experience=["Built scoring pipelines", "Created explainability reports", "Supported hiring analytics"],
            location="Remote",
            source_labels=["seeded-data:backend_engineers"],
            missing_data=["CrewAI experience unknown"],
        ),
        CandidateProfile(
            candidate_id="cand_004",
            display_name="Samira Okafor",
            profile_summary="Senior platform engineer focused on distributed systems, observability, and secure service design.",
            skills=["Python", "Kubernetes", "Observability", "PostgreSQL", "Security"],
            experience=["Led backend platform migrations", "Improved API reliability", "Mentored backend engineers"],
            location="Remote Canada",
            source_labels=["seeded-data:backend_engineers"],
            missing_data=["CrewAI experience unknown", "US work authorization unknown"],
        ),
    ]
}

KNOWN_SKILLS = [
    "Python",
    "FastAPI",
    "Flask",
    "CrewAI",
    "Angular",
    "TypeScript",
    "JavaScript",
    "SQL",
    "PostgreSQL",
    "API design",
    "ATS integrations",
    "Data pipelines",
    "Evaluation design",
    "Kubernetes",
    "Observability",
    "Security",
]


class CandidateSourceService:
    """Loads candidate profiles from approved MVP sources only."""

    def load_candidates(
        self, criteria: EvaluationCriteria, source: CandidateSource, max_candidates: int = 6
    ) -> tuple[list[CandidateProfile], list[WorkflowWarning]]:
        if source.type == SourceType.seeded:
            return self._seeded_candidates(source, max_candidates)
        if source.type == SourceType.pasted:
            return self._parse_text(source.pasted_profiles or "", "pasted-profile", max_candidates)
        if source.type == SourceType.uploaded:
            return self._parse_text(source.uploaded_text or "", "uploaded-text", max_candidates)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported candidate source type.")

    def _seeded_candidates(
        self, source: CandidateSource, max_candidates: int
    ) -> tuple[list[CandidateProfile], list[WorkflowWarning]]:
        dataset_id = source.dataset_id or "backend_engineers"
        candidates = SEED_CANDIDATES.get(dataset_id)
        if not candidates:
            return [], [
                WorkflowWarning(
                    code="UNKNOWN_DATASET",
                    message=f"No seeded candidate dataset named '{dataset_id}' was found.",
                )
            ]
        return candidates[:max_candidates], []

    def _parse_text(
        self, text: str, source_label: str, max_candidates: int
    ) -> tuple[list[CandidateProfile], list[WorkflowWarning]]:
        if not text.strip():
            return [], [
                WorkflowWarning(
                    code="EMPTY_CANDIDATE_SOURCE",
                    message="No candidate text was supplied for the selected source.",
                )
            ]

        blocks = [block.strip() for block in re.split(r"\n\s*\n+", text.strip()) if block.strip()]
        candidates = [self._candidate_from_block(block, index + 1, source_label) for index, block in enumerate(blocks)]
        return candidates[:max_candidates], []

    def _candidate_from_block(self, block: str, index: int, source_label: str) -> CandidateProfile:
        lines = [line.strip(" -\t") for line in block.splitlines() if line.strip()]
        first_line = lines[0] if lines else f"Candidate {index}"
        display_name = re.sub(r"[:|-].*$", "", first_line).strip() or f"Candidate {index}"
        summary = " ".join(lines)[:300]
        lower_block = block.lower()
        skills = [skill for skill in KNOWN_SKILLS if skill.lower() in lower_block]
        location = self._extract_labeled_value(lines, "location") or "Unknown"

        return CandidateProfile(
            candidate_id=f"{source_label.replace('-', '_')}_{index}",
            display_name=display_name,
            profile_summary=summary,
            skills=skills or ["Needs recruiter review"],
            experience=self._extract_experience(lines),
            location=location,
            source_labels=[source_label],
            missing_data=["Availability unknown", "Compensation expectations unknown"],
        )

    @staticmethod
    def _extract_labeled_value(lines: list[str], label: str) -> str | None:
        prefix = f"{label}:"
        for line in lines:
            if line.lower().startswith(prefix):
                return line.split(":", 1)[1].strip() or None
        return None

    @staticmethod
    def _extract_experience(lines: list[str]) -> list[str]:
        experience = [line for line in lines if any(term in line.lower() for term in ["built", "led", "created", "managed"])]
        return experience[:3] or ["Experience inferred from recruiter-provided profile text."]
