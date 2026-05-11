from __future__ import annotations

from dataclasses import dataclass

from app.schemas.recruitment import (
    CandidateEvaluation,
    CandidateProfile,
    EvaluationCriteria,
    RankedRecommendation,
    WorkflowWarning,
)
from app.services.candidate_sources import CandidateSourceService


@dataclass
class ResearchResult:
    candidates: list[CandidateProfile]
    warnings: list[WorkflowWarning]


class ResearcherAgent:
    role = "Researcher Agent"
    goal = "Select and normalize candidate options from approved sources only."

    def __init__(self, candidate_sources: CandidateSourceService | None = None) -> None:
        self.candidate_sources = candidate_sources or CandidateSourceService()

    def run(self, criteria: EvaluationCriteria, candidate_source, max_candidates: int) -> ResearchResult:
        candidates, warnings = self.candidate_sources.load_candidates(criteria, candidate_source, max_candidates)
        return ResearchResult(candidates=candidates, warnings=warnings)


class EvaluatorAgent:
    role = "Evaluator Agent"
    goal = "Evaluate candidates consistently against job-related criteria."

    def run(self, criteria: EvaluationCriteria, candidates: list[CandidateProfile]) -> list[CandidateEvaluation]:
        return [self._evaluate_candidate(criteria, candidate) for candidate in candidates]

    def _evaluate_candidate(self, criteria: EvaluationCriteria, candidate: CandidateProfile) -> CandidateEvaluation:
        required_score, matched_required = self._skill_score(criteria.required_skills, candidate.skills)
        preferred_score, matched_preferred = self._skill_score(criteria.preferred_skills, candidate.skills)
        experience_score = self._experience_score(criteria, candidate)
        seniority_score = self._seniority_score(criteria, candidate)
        location_score = self._location_score(criteria, candidate)
        evidence_score = 70 if "Needs recruiter review" in candidate.skills else 82
        if any("unknown" in item.lower() for item in candidate.missing_data):
            evidence_score -= 8

        overall = round(
            required_score * 0.34
            + preferred_score * 0.12
            + experience_score * 0.22
            + seniority_score * 0.12
            + location_score * 0.08
            + evidence_score * 0.12
        )
        overall = max(0, min(100, overall))
        fit_label = "strong" if overall >= 82 else "moderate" if overall >= 68 else "low"

        strengths = self._strengths(matched_required, matched_preferred, candidate)
        gaps = self._gaps(criteria, matched_required, candidate)
        unknowns = candidate.missing_data or ["Availability unknown"]

        return CandidateEvaluation(
            candidate_id=candidate.candidate_id,
            fit_label=fit_label,
            overall_score=overall,
            component_scores={
                "required_skills": required_score,
                "preferred_skills": preferred_score,
                "experience": experience_score,
                "seniority": seniority_score,
                "location": location_score,
                "evidence_confidence": evidence_score,
            },
            strengths=strengths,
            gaps=gaps,
            unknowns=unknowns,
            rationale=(
                f"{candidate.display_name} was evaluated against the supplied role criteria using approved "
                "candidate data and source labels."
            ),
        )

    @staticmethod
    def _skill_score(criteria_skills: list[str], candidate_skills: list[str]) -> tuple[int, list[str]]:
        if not criteria_skills:
            return 65, []
        normalized_candidate = [skill.lower() for skill in candidate_skills]
        matched = [
            skill
            for skill in criteria_skills
            if any(skill.lower() in candidate_skill or candidate_skill in skill.lower() for candidate_skill in normalized_candidate)
        ]
        return round(len(matched) / len(criteria_skills) * 100), matched

    @staticmethod
    def _experience_score(criteria: EvaluationCriteria, candidate: CandidateProfile) -> int:
        haystack = " ".join([candidate.profile_summary, *candidate.experience]).lower()
        role_terms = [term for term in [criteria.title, *criteria.required_skills, *criteria.preferred_skills] if term]
        matches = sum(1 for term in role_terms if term.lower() in haystack)
        return min(95, 58 + matches * 7)

    @staticmethod
    def _seniority_score(criteria: EvaluationCriteria, candidate: CandidateProfile) -> int:
        if not criteria.seniority:
            return 60
        haystack = " ".join([candidate.profile_summary, *candidate.experience]).lower()
        seniority = criteria.seniority.lower()
        if seniority in haystack:
            return 90
        if "senior" in seniority and any(term in haystack for term in ["lead", "led", "senior", "mentor"]):
            return 84
        return 72

    @staticmethod
    def _location_score(criteria: EvaluationCriteria, candidate: CandidateProfile) -> int:
        if not criteria.location:
            return 70
        required = criteria.location.lower()
        candidate_location = candidate.location.lower()
        if required in candidate_location or candidate_location in required:
            return 100
        if "remote" in required and "remote" in candidate_location:
            return 94
        if candidate.location == "Unknown":
            return 55
        return 68

    @staticmethod
    def _strengths(matched_required: list[str], matched_preferred: list[str], candidate: CandidateProfile) -> list[str]:
        strengths: list[str] = []
        if matched_required:
            strengths.append(f"Matches required skills: {', '.join(matched_required)}.")
        if matched_preferred:
            strengths.append(f"Also shows preferred skills: {', '.join(matched_preferred)}.")
        if candidate.experience:
            strengths.append(candidate.experience[0])
        return strengths or ["Has adjacent experience that should be reviewed by the recruiter."]

    @staticmethod
    def _gaps(criteria: EvaluationCriteria, matched_required: list[str], candidate: CandidateProfile) -> list[str]:
        missing_required = [skill for skill in criteria.required_skills if skill not in matched_required]
        gaps = [f"No direct evidence for required skill: {skill}." for skill in missing_required[:3]]
        if "Needs recruiter review" in candidate.skills:
            gaps.append("Candidate skills could not be reliably extracted from the supplied profile text.")
        return gaps


class RecommenderAgent:
    role = "Recommender Agent"
    goal = "Rank candidates and produce recruiter-reviewable recommendations."

    def run(
        self,
        criteria: EvaluationCriteria,
        candidates: list[CandidateProfile],
        evaluations: list[CandidateEvaluation],
    ) -> list[RankedRecommendation]:
        candidate_by_id = {candidate.candidate_id: candidate for candidate in candidates}
        ranked_evaluations = sorted(evaluations, key=lambda item: item.overall_score, reverse=True)
        recommendations: list[RankedRecommendation] = []

        for rank, evaluation in enumerate(ranked_evaluations, start=1):
            candidate = candidate_by_id[evaluation.candidate_id]
            recommendations.append(
                RankedRecommendation(
                    rank=rank,
                    candidate_id=candidate.candidate_id,
                    display_name=candidate.display_name,
                    fit_label=evaluation.fit_label,
                    overall_score=evaluation.overall_score,
                    recommendation_rationale=self._rationale(criteria, candidate, evaluation),
                    strengths=evaluation.strengths,
                    gaps=evaluation.gaps or ["No material gaps identified from supplied data."],
                    unknowns=evaluation.unknowns,
                    suggested_next_step=self._next_step(evaluation),
                )
            )

        return recommendations

    @staticmethod
    def _rationale(criteria: EvaluationCriteria, candidate: CandidateProfile, evaluation: CandidateEvaluation) -> str:
        return (
            f"{candidate.display_name} is ranked for {criteria.title} based on a {evaluation.fit_label} "
            f"fit score and evidence tied to required criteria."
        )

    @staticmethod
    def _next_step(evaluation: CandidateEvaluation) -> str:
        if evaluation.fit_label == "strong":
            return "Recruiter review, then consider hiring-manager screen."
        if evaluation.fit_label == "moderate":
            return "Recruiter review recommended; clarify gaps before advancing."
        return "Recruiter should review missing evidence before considering next steps."


def build_crewai_blueprint() -> dict[str, object]:
    """Return CrewAI-compatible role metadata without requiring live LLM execution."""
    return {
        "process": "sequential",
        "agents": [
            {"role": ResearcherAgent.role, "goal": ResearcherAgent.goal},
            {"role": EvaluatorAgent.role, "goal": EvaluatorAgent.goal},
            {"role": RecommenderAgent.role, "goal": RecommenderAgent.goal},
        ],
        "tasks": [
            "Normalize approved candidate profiles.",
            "Evaluate candidates against job criteria.",
            "Rank candidates and prepare decision-support recommendations.",
        ],
    }


def build_crewai_crew():
    """Build the CrewAI crew object for environments that enable live agent execution."""
    from crewai import Agent, Crew, Process, Task

    researcher = Agent(
        role=ResearcherAgent.role,
        goal=ResearcherAgent.goal,
        backstory="You normalize approved candidate data and preserve source labels without scraping.",
        verbose=False,
    )
    evaluator = Agent(
        role=EvaluatorAgent.role,
        goal=EvaluatorAgent.goal,
        backstory="You evaluate job-related evidence consistently and mark missing evidence as unknown.",
        verbose=False,
    )
    recommender = Agent(
        role=RecommenderAgent.role,
        goal=RecommenderAgent.goal,
        backstory="You prepare ranked decision-support recommendations that require recruiter approval.",
        verbose=False,
    )

    tasks = [
        Task(
            description="Normalize approved candidate input into structured candidate profiles.",
            expected_output="Candidate profiles with source labels and missing-data notes.",
            agent=researcher,
        ),
        Task(
            description="Score candidates against role criteria and identify strengths, gaps, and unknowns.",
            expected_output="Candidate evaluations with component scores and rationale.",
            agent=evaluator,
        ),
        Task(
            description="Rank evaluated candidates and prepare recruiter-reviewable recommendations.",
            expected_output="Ranked shortlist with rationale, caveats, next steps, and disclosure.",
            agent=recommender,
        ),
    ]
    return Crew(
        agents=[researcher, evaluator, recommender],
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
    )
