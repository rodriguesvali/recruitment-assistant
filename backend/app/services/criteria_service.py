from __future__ import annotations

from fastapi import HTTPException, status

from app.schemas.recruitment import EvaluationCriteria, JobRequirement


class CriteriaService:
    """Validates and normalizes recruiter-provided job criteria."""

    def extract(self, job: JobRequirement) -> EvaluationCriteria:
        title = job.title.strip()
        description = job.description.strip()

        if not title:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Job title is required.",
            )
        if not description:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Job description is required.",
            )

        ambiguities: list[str] = []
        if not job.required_skills:
            ambiguities.append("No required skills were supplied. Add must-have criteria before using real candidates.")
        if not job.seniority.strip():
            ambiguities.append("Seniority is not specified, so level alignment may be lower confidence.")
        if not job.location.strip():
            ambiguities.append("Location or work arrangement is not specified.")
        if len(description.split()) < 12:
            ambiguities.append("Job description is brief; evaluation may rely heavily on listed skills.")

        return EvaluationCriteria(
            title=title,
            description=description,
            required_skills=self._unique(job.required_skills),
            preferred_skills=self._unique(job.preferred_skills),
            seniority=job.seniority.strip(),
            location=job.location.strip(),
            ambiguities=ambiguities,
            confirmed_by_recruiter=False,
        )

    @staticmethod
    def _unique(items: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            normalized = item.strip()
            key = normalized.lower()
            if normalized and key not in seen:
                seen.add(key)
                result.append(normalized)
        return result
