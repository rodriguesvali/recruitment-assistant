from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import workflow_service


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
