from __future__ import annotations

from fastapi import APIRouter

from app.schemas.recruitment import (
    CandidatePreviewRequest,
    CandidatePreviewResponse,
    CriteriaExtractionRequest,
    EvaluationCriteria,
    HealthResponse,
    RecruiterApproval,
    RecruitmentRunResult,
    WorkflowRequest,
)
from app.services.criteria_service import CriteriaService
from app.services.recruitment_workflow import RecruitmentWorkflowService

router = APIRouter()
criteria_service = CriteriaService()
workflow_service = RecruitmentWorkflowService()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.post("/api/criteria/extract", response_model=EvaluationCriteria)
def extract_criteria(request: CriteriaExtractionRequest) -> EvaluationCriteria:
    return criteria_service.extract(request.job)


@router.post("/api/candidates/preview", response_model=CandidatePreviewResponse)
def preview_candidates(request: CandidatePreviewRequest) -> CandidatePreviewResponse:
    return workflow_service.preview_candidates(request.criteria, request.candidate_source)


@router.post("/api/recommendations/run", response_model=RecruitmentRunResult)
def run_recommendations(request: WorkflowRequest) -> RecruitmentRunResult:
    return workflow_service.run(request)


@router.post("/api/recommendations/{run_id}/approval", response_model=RecruiterApproval)
def record_approval(run_id: str, approval: RecruiterApproval) -> RecruiterApproval:
    return workflow_service.record_approval(run_id, approval)
