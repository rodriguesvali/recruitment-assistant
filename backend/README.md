# Recruitment Assistant Backend

FastAPI backend for the Recruitment Assistant MVP.

## Run Locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The Angular frontend expects the API at `http://localhost:8000`.

## Endpoints

- `GET /health`
- `POST /api/criteria/extract`
- `POST /api/candidates/preview`
- `POST /api/recommendations/run`
- `POST /api/recommendations/{run_id}/approval`
