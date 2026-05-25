from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SourceType(str, Enum):
    seeded = "seeded"
    pasted = "pasted"
    uploaded = "uploaded"


class RunStatus(str, Enum):
    idle = "idle"
    validating = "validating"
    researching = "researching"
    evaluating = "evaluating"
    recommending = "recommending"
    complete = "complete"
    failed = "failed"


class ApprovalStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    needs_edits = "needs_edits"


class JobRequirement(BaseModel):
    title: str = ""
    description: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    seniority: str = ""
    location: str = ""

    @field_validator("required_skills", "preferred_skills", mode="before")
    @classmethod
    def normalize_skill_list(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []


class CriteriaExtractionRequest(BaseModel):
    job: JobRequirement


class EvaluationCriteria(JobRequirement):
    ambiguities: list[str] = Field(default_factory=list)
    confirmed_by_recruiter: bool = False


class CandidateSource(BaseModel):
    type: SourceType
    dataset_id: str | None = None
    pasted_profiles: str | None = None
    uploaded_text: str | None = None


class WorkflowWarning(BaseModel):
    code: str
    message: str


class CandidateProfile(BaseModel):
    candidate_id: str
    display_name: str
    profile_summary: str
    skills: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    location: str = "Unknown"
    source_labels: list[str] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)


class CandidatePreviewRequest(BaseModel):
    criteria: EvaluationCriteria
    candidate_source: CandidateSource


class CandidatePreviewResponse(BaseModel):
    candidates: list[CandidateProfile]
    warnings: list[WorkflowWarning] = Field(default_factory=list)


class CandidateEvaluation(BaseModel):
    candidate_id: str
    fit_label: Literal["strong", "moderate", "low"]
    overall_score: int = Field(ge=0, le=100)
    component_scores: dict[str, int] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    rationale: str


class RankedRecommendation(BaseModel):
    rank: int
    candidate_id: str
    display_name: str
    fit_label: Literal["strong", "moderate", "low"]
    overall_score: int = Field(ge=0, le=100)
    recommendation_rationale: str
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    suggested_next_step: str


class RecruiterApproval(BaseModel):
    status: ApprovalStatus = ApprovalStatus.pending
    reviewer_notes: str | None = None


class WorkflowOptions(BaseModel):
    max_candidates: int = Field(default=6, ge=1, le=20)
    score_style: Literal["numeric_and_label"] = "numeric_and_label"
    require_recruiter_checkpoints: bool = True


class WorkflowRequest(BaseModel):
    job: JobRequirement
    criteria: EvaluationCriteria | None = None
    candidate_source: CandidateSource
    options: WorkflowOptions = Field(default_factory=WorkflowOptions)


class RecommendationReport(BaseModel):
    summary_markdown: str
    disclosure: str


class RecruitmentRunResult(BaseModel):
    run_id: str
    status: RunStatus
    criteria: EvaluationCriteria
    candidates: list[CandidateProfile]
    evaluations: list[CandidateEvaluation]
    ranked_shortlist: list[RankedRecommendation]
    report: RecommendationReport
    warnings: list[WorkflowWarning] = Field(default_factory=list)
    approval: RecruiterApproval = Field(default_factory=RecruiterApproval)


class CrewAIRecommendationOutput(BaseModel):
    evaluations: list[CandidateEvaluation]
    ranked_shortlist: list[RankedRecommendation]
    warnings: list[WorkflowWarning] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "recruitment-assistant-backend"
