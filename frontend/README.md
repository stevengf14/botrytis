# 💻 Botrytis Detection - Frontend UI

This directory contains the React.js frontend for the Botrytis Detection System, featuring a responsive dark-mode architecture.

## 🚀 Quick Start

1. **Install Dependencies**
   ```powershell
   cd frontend
   npm install
   ```

2. **Run the Application**
   ```powershell
   npm start
   ```

3. Open your browser at `http://localhost:3000/`

## ⚙️ Configuration
- The frontend expects the backend API at `REACT_APP_BOTRYTIS_API_URL` (or defaults to `http://localhost:8000` via Axios config).
- The web app posts image blobs to the `/analyze` endpoint and renders the resulting bounding boxes onto a canvas overlap.

---
**Authors:** Steven Andrés Guamán Figueroa & Jonathan Santiago Almeida Salas
