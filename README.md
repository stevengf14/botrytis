Botrytis Detection
---------------------

Team Members:

<li> Jonathan Santiago Almeida Salas</li>
<li> Steven Andrés Guamán Figueroa</li>
<li> Bryan Steven Vinueza Bustamante</li>
<li> Carlos Eduardo Vaca Cano</li>
<li> Erick Stuart Almeida Chávez</li>

=================================

This repository contains the minimum requirements to run the Botrytis detection API and its integration with the frontend component.

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