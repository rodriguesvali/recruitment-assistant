from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from app.agents.crew import EvaluatorAgent, RecommenderAgent, ResearcherAgent
from app.schemas.recruitment import (
    CandidatePreviewResponse,
    CandidateSource,
    EvaluationCriteria,
    RecruiterApproval,
    RecruitmentRunResult,
    RunStatus,
    WorkflowRequest,
    WorkflowWarning,
)
from app.services.criteria_service import CriteriaService
from app.services.report_service import ReportService


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
        research = self.researcher.run(criteria, candidate_source, max_candidates)
        return CandidatePreviewResponse(candidates=research.candidates, warnings=research.warnings)

    def run(self, request: WorkflowRequest) -> RecruitmentRunResult:
        criteria = request.criteria or self.criteria_service.extract(request.job)
        warnings: list[WorkflowWarning] = []
        warnings.extend(
            WorkflowWarning(code="CRITERIA_AMBIGUITY", message=ambiguity) for ambiguity in criteria.ambiguities
        )

        research = self.researcher.run(criteria, request.candidate_source, request.options.max_candidates)
        warnings.extend(research.warnings)

        if not research.candidates:
            result = self._empty_result(criteria, warnings)
            self._runs[result.run_id] = result
            return result

        evaluations = self.evaluator.run(criteria, research.candidates)
        shortlist = self.recommender.run(criteria, research.candidates, evaluations)
        report = self.report_service.create_report(criteria, shortlist)

        if any(item.overall_score < 68 for item in evaluations):
            warnings.append(
                WorkflowWarning(
                    code="LOW_CONFIDENCE_RESULTS",
                    message="One or more candidates have low or incomplete evidence and require recruiter review.",
                )
            )

        result = RecruitmentRunResult(
            run_id=self._run_id(),
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
        return result

    def record_approval(self, run_id: str, approval: RecruiterApproval) -> RecruiterApproval:
        existing = self._runs.get(run_id)
        if existing:
            existing.approval = approval
            self._runs[run_id] = existing
        return approval

    def _empty_result(self, criteria: EvaluationCriteria, warnings: list[WorkflowWarning]) -> RecruitmentRunResult:
        warnings.append(
            WorkflowWarning(
                code="NO_CANDIDATES",
                message="No approved candidate profiles were available for evaluation.",
            )
        )
        report = self.report_service.create_report(criteria, [])
        return RecruitmentRunResult(
            run_id=self._run_id(),
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
