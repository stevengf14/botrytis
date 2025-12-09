Backend (FastAPI) - Botrytis Detection
=====================================

Instrucciones básicas para ejecutar el microservicio de inferencia y el
entrenamiento del modelo.

1) Entorno

   - Crear un entorno virtual (recomendado `venv`) y activar.
   - Instalar dependencias:

```powershell
cd botrytis_project\backend
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Dataset

   - Organizar imágenes en `botrytis_project/backend/data/` con estructura:

```
data/
  train/
    healthy/
    botrytis/
  val/
    healthy/
    botrytis/
```

3) Entrenamiento (esqueleto)

   - Ejecutar entrenamiento de muestra:

```powershell
cd botrytis_project\backend\app
python train.py --data-dir ../data --epochs 10 --batch-size 16 --out ../model.pth
```

4) Ejecutar API

```powershell
cd botrytis_project\backend\app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5) Endpoint

- `POST /predict` : subir archivo `file` (form) -> devuelve JSON:

```json
{
  "has_botrytis": true,
  "confidence": 0.87
}
```

Respuesta:
- `has_botrytis` (boolean): `true` si detecta Botrytis, `false` si está sano
- `confidence` (float): valor de 0.0 a 1.0 indicando la confiabilidad de la predicción

Notas:
- `torch` puede ser pesado; si no desea instalarlo en el entorno de inferencia,
  puede usar el `ModelWrapper` en `model.py` que funciona en modo "dummy" basado
  en brillo hasta que cargue un modelo real.
- El heurístico dummy es solo para pruebas tempranas; reemplazar con modelo
  entrenado después de recolectar dataset.
