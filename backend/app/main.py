from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import os
from ultralytics import YOLO

app = FastAPI(title="Botrytis Detection API")

# Allow all origins for development
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Model path (relative to `backend/app`)
MODEL_PATH = os.path.join("..", "model", "best.pt")
model = None

@app.on_event("startup")
async def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = YOLO(MODEL_PATH)
        print(f"Model loaded: {MODEL_PATH}")
    else:
        print(f"WARNING: Model not found at {MODEL_PATH}. API cannot perform predictions.")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded on server.")

    try:
        contents = await file.read()
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Inference (conf=0.4 to filter low-confidence detections)
    results = model.predict(pil_img, conf=0.4)
    result = results[0]

    detections = []
    has_botrytis = False

    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        cls_name = result.names[cls_id]

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

    # Response logic
    if not detections:
        status_global = "no_flower_detected"
        message = "No flowers detected in the image."
    elif has_botrytis:
        status_global = "infected"
        message = "ALERT: Botrytis detected in the rose."
    else:
        status_global = "uninfected"
        message = "No signs of Botrytis detected in the rose."

    return JSONResponse(content={
        "status": status_global,
        "message": message,
        "total_detections": len(detections),
        "detections": detections
    })