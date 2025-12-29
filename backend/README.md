Backend (FastAPI) - Botrytis Detection
=====================================

Quick start
-----------

1) Create and activate Python virtualenv, then install dependencies:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Run the API (development):

```powershell
cd backend\app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3) Endpoint

- `POST /analyze` — form field `file` (image) -> JSON response:

Example response:

```json
{
  "status": "infected",           
  "message": "ALERT: Botrytis detected in the rose.",
  "total_detections": 1,
  "detections": [
    {"box": [x1,y1,x2,y2], "label": "botrytis_rose", "confidence": 0.87, "is_infected": true}
  ]
}
```

Notes
-----
- Model path: `backend/model/best.pt`. The API attempts to load this file at startup.
- CORS is enabled for development (`*`).
- If you need a lightweight test mode without `torch`, use the training workspace tools or a mock wrapper.

If you want, I can add a minimal `test_api.py` script to automate a quick POST test.
