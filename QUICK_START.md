Guía Rápida - Botrytis Detection (Frontend + Backend)
=====================================================

Descripción
-----------
Sistema completo para detectar Botrytis en rosas usando Deep Learning.
- Backend: FastAPI + PyTorch (microservicio)
- Frontend: React con componente de carga/análisis de imágenes

Estructura
----------
```
botrytis_project/
├── backend/
│   ├── app/
│   │   ├── main.py       (API FastAPI)
│   │   ├── model.py      (Wrapper del modelo PyTorch)
│   │   ├── train.py      (Script de entrenamiento)
│   │   └── schemas.py
│   ├── data/             (Dataset - crear después)
│   │   ├── train/
│   │   └── val/
│   ├── model.pth         (Modelo entrenado - generar con train.py)
│   ├── requirements.txt
│   ├── test_api.py       (Script de prueba)
│   └── README.md
├── frontend/
│   └── README.md
└── README.md

svision_front/           (Proyecto React existente)
├── src/
│   ├── components/
│   │   └── BotrytisDetection/
│   │       ├── BotrytisDetection.jsx
│   │       └── BotrytisDetection.css
│   ├── services/
│   │   └── botrytisService.js
│   └── App.js            (Ruta agregada)
├── .env.example
└── .env                  (Crear a partir de .env.example)
```

Uso Rápido
==========

OPCIÓN 1: Prueba local (sin modelo entrenado, usando heurístico dummy)
----------------------------------------------------------------------

1. Backend (Terminal 1)
   
   cd botrytis_project\backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

2. Frontend (Terminal 2)
   
   cd svision_front
   copy .env.example .env        # Windows PowerShell: copy (o cp)
   npm install                   # Primera vez
   npm start
   
   El navegador abrirá http://localhost:3000/

3. Probar
   
   - Ir a http://localhost:3000/botrytis-detection
   - Cargar una imagen (cualquier .jpg, .png, etc.)
   - Clic en "Analizar Imagen"
   - Ver resultado: "Rosa Sana" o "Botrytis Detectada" con % de confianza

4. Test API (Terminal 3, opcional)
   
   cd botrytis_project\backend
   .\.venv\Scripts\Activate.ps1
   pip install requests
   python test_api.py --api-url http://localhost:8000


OPCIÓN 2: Entrenamiento con Dataset Real
------------------------------------------

1. Preparar dataset
   
   Crear estructura en botrytis_project/backend/data/:
   
   data/
   ├── train/
   │   ├── healthy/     (imágenes de rosas sanas)
   │   └── botrytis/    (imágenes con Botrytis)
   └── val/
       ├── healthy/
       └── botrytis/
   
   Mínimo recomendado: 50-100 imágenes por clase, distribuidas 80% train, 20% val.

2. Ejecutar entrenamiento
   
   cd botrytis_project\backend\app
   .\.venv\Scripts\Activate.ps1
   
   python train.py \
     --data-dir ../data \
     --epochs 20 \
     --batch-size 16 \
     --lr 1e-4 \
     --out ../model.pth
   
   Esto genera botrytis_project/backend/model.pth

3. Usar modelo en Backend
   
   El backend cargará automáticamente model.pth si existe.
   Reinicia el servidor FastAPI para cargar el nuevo modelo.

4. Frontend usará automáticamente el nuevo modelo
   
   No requiere cambios; simplemente usará model.pth.


Configuración Avanzada
======================

Cambiar URL del Backend (si no está en localhost:8000)
-------------------------------------------------------

1. Editar .env en svision_front/:
   
   REACT_APP_BOTRYTIS_API_URL=http://192.168.1.100:8000

2. Reiniciar npm start


CORS (Cross-Origin)
-------------------

Backend permite CORS desde cualquier origen en desarrollo.
Para producción, cambiar en backend/app/main.py:

   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://tudominio.com"],  # En lugar de ["*"]
       ...
   )


Solución de Problemas
====================

Error: "No se puede conectar a localhost:8000"
   → Verificar que Backend está corriendo: uvicorn main:app --reload

Error: "CORS Error / No se puede enviar imagen"
   → Backend podría no tener CORS configurado
   → Revisar que main.py tiene CORSMiddleware

Error: "Modelo no encontrado"
   → Usar heurístico dummy primero (obra sin model.pth)
   → Entrenar con train.py para generar model.pth

Error: "CUDA out of memory"
   → Reducir --batch-size en train.py
   → O usar CPU: agregar --device cpu al train.py (modificar)

Error: "npm start no funciona"
   → Ejecutar npm install primero
   → Verificar Node.js/npm instalados: node -v


Estructura de Respuesta API
===========================

POST /predict

Request:
  - Multipart form-data con campo "file" (imagen)

Response (200 OK):
  {
    "has_botrytis": true,
    "confidence": 0.87
  }

Response (400 Bad Request):
  {
    "detail": "Invalid image file"
  }


Próximos Pasos
==============

1. Recolectar dataset de rosas (saludables + Botrytis)
   - Fuentes: Hugging Face, Roboflow, capturas propias
   - Mínimo inicial: 200-500 imágenes balanceadas

2. Entrenar modelo con tu dataset real

3. Evaluar métricas (Accuracy, F1, Confusion Matrix)

4. Despliegue en producción
   - Docker + docker-compose
   - Cloud (AWS, GCP, Heroku, etc.)

5. Agregar funcionalidades
   - Logging y estadísticas de uso
   - Batch processing
   - Video en tiempo real (fase 2)


Referencia Rápida - Comandos
=============================

Backend Setup:
  cd botrytis_project/backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt

Correr Backend:
  cd botrytis_project/backend/app
  .\.venv\Scripts\Activate.ps1
  uvicorn main:app --reload --host 0.0.0.0 --port 8000

Correr Frontend:
  cd svision_front
  npm install
  npm start

Test API:
  python botrytis_project/backend/test_api.py

Entrenar Modelo:
  python botrytis_project/backend/app/train.py --data-dir ../data --epochs 20

