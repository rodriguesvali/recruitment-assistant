from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_recommendations_seeded() -> None:
    response = client.post(
        "/api/recommendations/run",
        json={
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
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["status"] == "complete"
    assert payload["criteria"]["confirmed_by_recruiter"] is True
    assert payload["ranked_shortlist"]
    assert payload["report"]["disclosure"]
