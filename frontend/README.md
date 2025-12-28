Frontend Integration - Botrytis Detection
=========================================

Quick start
-----------

1) Install and run the frontend:

```powershell
cd frontend
npm install   # first time only
npm start
```

2) Open in browser:

- http://localhost:3000/

Configuration
-------------
- The frontend expects the backend API at `REACT_APP_BOTRYTIS_API_URL` (env var). Default: `http://localhost:8000`.
- The frontend calls `POST /analyze` with form field `file` and maps the response into `{ has_botrytis, confidence, found_flower }` for the UI.

If you want me to include a simple e2e test script that posts a sample image to the backend, I can add it.
