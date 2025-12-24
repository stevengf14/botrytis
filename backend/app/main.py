from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
from ultralytics import YOLO

app = FastAPI(title="Botrytis Detection API")

# Configurar CORS (Permitir todo por ahora) 
# TODO: Configurar adecuadamente para producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta donde se espera el modelo entrenado
# NOTA: Copiar best.pt aquí después de entrenar
MODEL_PATH = os.path.join("..\model", "best.pt")
model = None

@app.on_event("startup")
async def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = YOLO(MODEL_PATH)
        print(f"Modelo cargado: {MODEL_PATH}")
    else:
        print(f"ALERTA: No se encontró {MODEL_PATH}. La API no podrá predecir.")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado en el servidor.")

    # 1. Leer imagen
    try:
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Archivo de imagen inválido")

    # 2. Inferencia (conf=0.4 descarta predicciones débiles)
    results = model.predict(pil_img, conf=0.4)
    result = results[0]

    detections = []
    has_botrytis = False

    # 3. Procesar cajas detectadas
    for box in result.boxes:
        # Coordenadas
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        # Confianza (0.0 a 1.0)
        conf = float(box.conf[0])
        # Clase ID y Nombre
        cls_id = int(box.cls[0])
        cls_name = result.names[cls_id]

        # Lógica de negocio
        is_infected = False
        if cls_name == 'botrytis_rose':
            has_botrytis = True
            is_infected = True

        detections.append({
            "box": [int(x1), int(y1), int(x2), int(y2)],
            "label": cls_name,
            "confidence": round(conf, 2),
            "is_infected": is_infected
        })

    # 4. Respuesta final resumida
    # TODO: mejorar la logica de mensajes, 100% de confiabilidad tambien cuando la rosa es sana,
    # no solo cuando hay botrytis
    # la confiabilidad depende de la confianza de las cajas detectadas
    if not detections:
        status_global = "no_flower_detected"
        message = "No se detectaron rosas en la imagen."
    elif has_botrytis:
        status_global = "infected"
        message = "ALERTA: Se detectó Botrytis en la rosa."
    else:
        status_global = "healthy"
        message = "La rosa parece sana."

    return JSONResponse(content={
        "status": status_global,
        "message": message,
        "total_detections": len(detections),
        "detections": detections
    })