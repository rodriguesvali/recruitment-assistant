from __future__ import annotations

import json
import logging
import os
from datetime import UTC, datetime
from time import perf_counter
from typing import Any
from uuid import uuid4

from fastapi import HTTPException, status
from pydantic import ValidationError

from app.agents.crew import EvaluatorAgent, RecommenderAgent, ResearcherAgent, build_crewai_crew
from app.schemas.recruitment import (
    CandidatePreviewResponse,
    CandidateProfile,
    CandidateSource,
    CrewAIRecommendationOutput,
    EvaluationCriteria,
    RecruiterApproval,
    RecruitmentRunResult,
    RunStatus,
    WorkflowRequest,
    WorkflowWarning,
)
from app.services.criteria_service import CriteriaService
from app.services.report_service import ReportService

logger = logging.getLogger(__name__)


def crewai_live_execution_enabled() -> bool:
    return os.getenv("RECRUITMENT_EXECUTION_MODE", "deterministic").lower() in {
        "crewai_live",
        "crewai",
        "live",
    }


class RecruitmentWorkflowService:
    def __init__(self) -> None:
        self.criteria_service = CriteriaService()
        self.researcher = ResearcherAgent()
        self.evaluator = EvaluatorAgent()
        self.recommender = RecommenderAgent()
        self.report_service = ReportService()
        self._runs: dict[str, RecruitmentRunResult] = {}

    def preview_candidates(
        self, criteria: EvaluationCriteria, candidate_source: CandidateSource, max_candidates: int = 6
    ) -> CandidatePreviewResponse:
        started_at = perf_counter()
        logger.info(
            "application_crew.preview.start",
            extra={"candidate_source_type": candidate_source.type.value, "max_candidates": max_candidates},
        )
        try:
            research = self.researcher.run(criteria, candidate_source, max_candidates)
        except Exception:
            logger.exception(
                "application_crew.preview.error",
                extra={"candidate_source_type": candidate_source.type.value, "max_candidates": max_candidates},
            )
            raise

        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        logger.info(
            "application_crew.preview.complete",
            extra={
                "candidate_source_type": candidate_source.type.value,
                "candidate_count": len(research.candidates),
                "warning_count": len(research.warnings),
                "duration_ms": duration_ms,
            },
        )
        return CandidatePreviewResponse(candidates=research.candidates, warnings=research.warnings)

    def run(self, request: WorkflowRequest) -> RecruitmentRunResult:
        run_id = self._run_id()
        started_at = perf_counter()
        logger.info(
            "application_crew.run.start",
            extra={
                "run_id": run_id,
                "candidate_source_type": request.candidate_source.type.value,
                "max_candidates": request.options.max_candidates,
            },
        )

        try:
            criteria = request.criteria or self.criteria_service.extract(request.job)
            warnings: list[WorkflowWarning] = []
            warnings.extend(
                WorkflowWarning(code="CRITERIA_AMBIGUITY", message=ambiguity) for ambiguity in criteria.ambiguities
            )

            logger.info("application_crew.agent.start", extra={"run_id": run_id, "agent": "researcher"})
            research = self.researcher.run(criteria, request.candidate_source, request.options.max_candidates)
            logger.info(
                "application_crew.agent.complete",
                extra={
                    "run_id": run_id,
                    "agent": "researcher",
                    "candidate_count": len(research.candidates),
                    "warning_count": len(research.warnings),
                },
            )
            warnings.extend(research.warnings)

            if not research.candidates:
                result = self._empty_result(criteria, warnings, run_id)
                self._runs[result.run_id] = result
                duration_ms = round((perf_counter() - started_at) * 1000, 2)
                logger.info(
                    "application_crew.run.complete",
                    extra={
                        "run_id": result.run_id,
                        "status": result.status.value,
                        "candidate_count": 0,
                        "evaluation_count": 0,
                        "shortlist_count": 0,
                        "warning_count": len(result.warnings),
                        "duration_ms": duration_ms,
                    },
                )
                return result

            if crewai_live_execution_enabled():
                output = self._run_live_crewai(run_id, criteria, research.candidates)
                warnings.extend(output.warnings)
                report = self.report_service.create_report(criteria, output.ranked_shortlist)
                result = RecruitmentRunResult(
                    run_id=run_id,
                    status=RunStatus.complete,
                    criteria=criteria,
                    candidates=research.candidates,
                    evaluations=output.evaluations,
                    ranked_shortlist=output.ranked_shortlist,
                    report=report,
                    warnings=warnings,
                    approval=RecruiterApproval(),
                )
                self._runs[result.run_id] = result
                duration_ms = round((perf_counter() - started_at) * 1000, 2)
                logger.info(
                    "application_crew.run.complete",
                    extra={
                        "run_id": result.run_id,
                        "status": result.status.value,
                        "execution_mode": "crewai_live",
                        "candidate_count": len(result.candidates),
                        "evaluation_count": len(result.evaluations),
                        "shortlist_count": len(result.ranked_shortlist),
                        "warning_count": len(result.warnings),
                        "duration_ms": duration_ms,
                    },
                )
                return result

            logger.info(
                "application_crew.agent.start",
                extra={"run_id": run_id, "agent": "evaluator", "candidate_count": len(research.candidates)},
            )
            evaluations = self.evaluator.run(criteria, research.candidates)
            logger.info(
                "application_crew.agent.complete",
                extra={"run_id": run_id, "agent": "evaluator", "evaluation_count": len(evaluations)},
            )

            logger.info(
                "application_crew.agent.start",
                extra={"run_id": run_id, "agent": "recommender", "evaluation_count": len(evaluations)},
            )
            shortlist = self.recommender.run(criteria, research.candidates, evaluations)
            logger.info(
                "application_crew.agent.complete",
                extra={"run_id": run_id, "agent": "recommender", "shortlist_count": len(shortlist)},
            )
            report = self.report_service.create_report(criteria, shortlist)

            if any(item.overall_score < 68 for item in evaluations):
                warnings.append(
                    WorkflowWarning(
                        code="LOW_CONFIDENCE_RESULTS",
                        message="One or more candidates have low or incomplete evidence and require recruiter review.",
                    )
                )

            result = RecruitmentRunResult(
                run_id=run_id,
                status=RunStatus.complete,
                criteria=criteria,
                candidates=research.candidates,
                evaluations=evaluations,
                ranked_shortlist=shortlist,
                report=report,
                warnings=warnings,
                approval=RecruiterApproval(),
            )
            self._runs[result.run_id] = result
            duration_ms = round((perf_counter() - started_at) * 1000, 2)
            logger.info(
                "application_crew.run.complete",
                extra={
                    "run_id": result.run_id,
                    "status": result.status.value,
                    "candidate_count": len(result.candidates),
                    "evaluation_count": len(result.evaluations),
                    "shortlist_count": len(result.ranked_shortlist),
                    "warning_count": len(result.warnings),
                    "duration_ms": duration_ms,
                },
            )
            return result
        except Exception:
            duration_ms = round((perf_counter() - started_at) * 1000, 2)
            logger.exception(
                "application_crew.run.error",
                extra={
                    "run_id": run_id,
                    "candidate_source_type": request.candidate_source.type.value,
                    "duration_ms": duration_ms,
                },
            )
            raise

    def _run_live_crewai(
        self, run_id: str, criteria: EvaluationCriteria, candidates: list[CandidateProfile]
    ) -> CrewAIRecommendationOutput:
        started_at = perf_counter()
        logger.info(
            "application_crew.kickoff.start",
            extra={
                "run_id": run_id,
                "candidate_count": len(candidates),
                "execution_mode": "crewai_live",
            },
        )
        crew = build_crewai_crew()
        try:
            crew_output = crew.kickoff(
                inputs={
                    "criteria_json": criteria.model_dump_json(),
                    "candidates_json": json.dumps([candidate.model_dump(mode="json") for candidate in candidates]),
                }
            )
            output = self._parse_crewai_output(crew_output)
        except Exception:
            duration_ms = round((perf_counter() - started_at) * 1000, 2)
            logger.exception(
                "application_crew.kickoff.error",
                extra={"run_id": run_id, "duration_ms": duration_ms},
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="CrewAI live execution failed. Check LLM credentials, model access, and CrewAI tracing status.",
            )

        duration_ms = round((perf_counter() - started_at) * 1000, 2)
        logger.info(
            "application_crew.kickoff.complete",
            extra={
                "run_id": run_id,
                "evaluation_count": len(output.evaluations),
                "shortlist_count": len(output.ranked_shortlist),
                "warning_count": len(output.warnings),
                "duration_ms": duration_ms,
            },
        )
        return output

    @staticmethod
    def _parse_crewai_output(crew_output: Any) -> CrewAIRecommendationOutput:
        pydantic_output = getattr(crew_output, "pydantic", None)
        if isinstance(pydantic_output, CrewAIRecommendationOutput):
            return pydantic_output
        if pydantic_output is not None:
            return CrewAIRecommendationOutput.model_validate(pydantic_output)

        json_dict = getattr(crew_output, "json_dict", None)
        if json_dict:
            return CrewAIRecommendationOutput.model_validate(json_dict)

        raw = getattr(crew_output, "raw", None) or str(crew_output)
        try:
            return CrewAIRecommendationOutput.model_validate_json(raw)
        except ValidationError as exc:
            raise ValueError("CrewAI kickoff did not return a valid recommendation payload.") from exc

    def record_approval(self, run_id: str, approval: RecruiterApproval) -> RecruiterApproval:
        existing = self._runs.get(run_id)
        if not existing:
            logger.warning("approval.record.not_found", extra={"run_id": run_id})
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation run not found.")

        existing.approval = approval
        self._runs[run_id] = existing
        logger.info("approval.record.complete", extra={"run_id": run_id, "approval_status": approval.status.value})
        return approval

    def _empty_result(
        self, criteria: EvaluationCriteria, warnings: list[WorkflowWarning], run_id: str | None = None
    ) -> RecruitmentRunResult:
        warnings.append(
            WorkflowWarning(
                code="NO_CANDIDATES",
                message="No approved candidate profiles were available for evaluation.",
            )
        )
        report = self.report_service.create_report(criteria, [])
        return RecruitmentRunResult(
            run_id=run_id or self._run_id(),
            status=RunStatus.complete,
            criteria=criteria,
            candidates=[],
            evaluations=[],
            ranked_shortlist=[],
            report=report,
            warnings=warnings,
            approval=RecruiterApproval(),
        )

    @staticmethod
    def _run_id() -> str:
        stamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
        return f"run_{stamp}_{uuid4().hex[:8]}"
