Botrytis Detection
---------------------

Integrantes:

<li> Jonathan Santiago Almeida Salas</li>
<li> Steven Andrés Guamán Figueroa</li>
<li> Bryan Steven Vinueza Bustamante</li>
<li> Carlos Eduardo Vaca Cano</li>
<li> Erick Stuart Almeida Chávez</li>

=================================

Este repositorio contiene lo mínimo necesario para ejecutar la API de
detección de Botrytis y la integración con el componente frontend.

Conservado:
- `backend/` — FastAPI app en `backend/app` con `main.py` y `model.py`.
- `frontend/` — documentación y el servicio JS para integrar en la UI.
- `.gitignore` — reglas para no subir datos/weights.

Quitado: documentación duplicada y metadatos de IDE para mantener el
repositorio limpio. Si necesitas los documentos originales, están
consolidados en `QUICK_START.md`.

Quick start (summary)
---------------------
1) Backend (PowerShell):

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2) Frontend (PowerShell):

```powershell
cd frontend
npm install
npm start
```

3) Quick test (optional):

```powershell
curl -F "file=@C:\path\to\image.jpg" http://localhost:8000/analyze
```

Contacto
-------
Si quieres que deje el repo listo para `git push` en una rama `cleanup/minimal`,
puedo preparar el commit y la instrucción para subirlo.
