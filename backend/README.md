# ⚙️ Botrytis Detection - Backend API

This directory contains the FastAPI backend for the Botrytis Detection System.

## 🚀 Quick Start

1. **Environment Setup**
   Create and activate a Python virtual environment, then install dependencies:
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Run the API (Development)**
   ```powershell
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📡 Endpoints
- `POST /analyze` — Expects a form `file` (image).
  **Example Response:**
  ```json
  {
    "status": "infected",           
    "message": "ALERT: Botrytis detected in the rose.",
    "total_detections": 1,
    "detections": [
      {"box": [10, 20, 100, 200], "label": "botrytis_rose", "confidence": 0.87, "is_infected": true}
    ]
  }
  ```

## 📝 Notes
- **Model path:** `backend/model/best.pt`. The API loads this model weights file at startup via Ultralytics YOLO.
- CORS is enabled for development across all origins (`*`).

---
**Authors:** Steven Andrés Guamán Figueroa & Jonathan Santiago Almeida Salas
