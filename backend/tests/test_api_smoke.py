from types import SimpleNamespace

from fastapi.testclient import TestClient

import app.services.recruitment_workflow as recruitment_workflow
from app.main import app
from app.api.routes import workflow_service
from app.schemas.recruitment import CandidateEvaluation, CrewAIRecommendationOutput, RankedRecommendation


client = TestClient(app)


def recommendation_request() -> dict:
    return {
        "job": {
            "title": "Backend Engineer",
            "description": "Build Python FastAPI services for a recruiter-facing AI workflow.",
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["CrewAI", "PostgreSQL"],
            "seniority": "Senior",
            "location": "Remote",
        },
        "candidate_source": {"type": "seeded", "dataset_id": "backend_engineers"},
        "criteria": {
            "title": "Backend Engineer",
            "description": "Build Python FastAPI services for a recruiter-facing AI workflow.",
            "required_skills": ["Python", "FastAPI"],
            "preferred_skills": ["CrewAI", "PostgreSQL"],
            "seniority": "Senior",
            "location": "Remote",
            "ambiguities": [],
            "confirmed_by_recruiter": True,
        },
        "options": {
            "max_candidates": 3,
            "score_style": "numeric_and_label",
            "require_recruiter_checkpoints": True,
        },
    }


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cors_allows_documented_frontend_fallback_port() -> None:
    response = client.options(
        "/health",
        headers={
            "Origin": "http://127.0.0.1:4300",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:4300"


def test_run_recommendations_seeded() -> None:
    response = client.post("/api/recommendations/run", json=recommendation_request())

    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "complete"
    assert payload["criteria"]["confirmed_by_recruiter"] is True
    assert payload["ranked_shortlist"]
    assert payload["report"]["disclosure"]


def test_run_recommendations_uses_crewai_kickoff_when_live_mode_enabled(monkeypatch) -> None:
    kickoff_inputs: dict = {}

    live_output = CrewAIRecommendationOutput(
        evaluations=[
            CandidateEvaluation(
                candidate_id="cand_001",
                fit_label="strong",
                overall_score=91,
                component_scores={"required_skills": 95},
                strengths=["Strong Python and FastAPI evidence."],
                gaps=[],
                unknowns=["Compensation expectations unknown"],
                rationale="Live CrewAI evaluation rationale.",
            )
        ],
        ranked_shortlist=[
            RankedRecommendation(
                rank=1,
                candidate_id="cand_001",
                display_name="Avery Chen",
                fit_label="strong",
                overall_score=91,
                recommendation_rationale="Live CrewAI recommendation rationale.",
                strengths=["Strong Python and FastAPI evidence."],
                gaps=["No material gaps identified from supplied data."],
                unknowns=["Compensation expectations unknown"],
                suggested_next_step="Recruiter review, then consider hiring-manager screen.",
            )
        ],
    )

    class FakeCrew:
        def kickoff(self, inputs):
            kickoff_inputs.update(inputs)
            return SimpleNamespace(pydantic=live_output)

    monkeypatch.setenv("RECRUITMENT_EXECUTION_MODE", "crewai_live")
    monkeypatch.setattr(recruitment_workflow, "build_crewai_crew", lambda: FakeCrew())

    response = client.post("/api/recommendations/run", json=recommendation_request())

    payload = response.json()
    assert response.status_code == 200
    assert payload["ranked_shortlist"][0]["recommendation_rationale"] == "Live CrewAI recommendation rationale."
    assert "criteria_json" in kickoff_inputs
    assert "candidates_json" in kickoff_inputs


def test_run_recommendations_live_mode_returns_502_when_kickoff_fails(monkeypatch) -> None:
    class FailingCrew:
        def kickoff(self, inputs):
            raise RuntimeError("provider failed")

    monkeypatch.setenv("RECRUITMENT_EXECUTION_MODE", "crewai_live")
    monkeypatch.setattr(recruitment_workflow, "build_crewai_crew", lambda: FailingCrew())

    response = client.post("/api/recommendations/run", json=recommendation_request())

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "CrewAI live execution failed. Check LLM credentials, model access, and CrewAI tracing status."
    )


def test_record_approval_unknown_run_returns_404() -> None:
    response = client.post(
        "/api/recommendations/run_missing_approval/approval",
        json={"status": "approved", "reviewer_notes": "Looks good."},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Recommendation run not found."


def test_record_approval_valid_run_returns_and_persists_payload() -> None:
    run_response = client.post("/api/recommendations/run", json=recommendation_request())
    run_id = run_response.json()["run_id"]
    approval_payload = {"status": "approved", "reviewer_notes": "Ready for recruiter follow-up."}

    approval_response = client.post(f"/api/recommendations/{run_id}/approval", json=approval_payload)

    assert approval_response.status_code == 200
    assert approval_response.json() == approval_payload
    assert workflow_service._runs[run_id].approval.model_dump(mode="json") == approval_payload
