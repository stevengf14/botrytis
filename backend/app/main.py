from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from PIL import ImageDraw, ImageFont
import io
import os
import numpy as np

from .model import ModelWrapper

app = FastAPI(title="Botrytis Detection API")

# Allow CORS for local development (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load classifier wrapper (may operate in dummy mode if no model file)
model = ModelWrapper()
try:
    model.load_model(os.environ.get("CLASSIFIER_MODEL_PATH", "../model.pth"))
except Exception:
    # If no model found or load fails, ModelWrapper will operate in dummy mode
    pass

# Try to load YOLO for flower detection if ultralytics is available
YOLO_AVAILABLE = False
yolo = None
try:
    from ultralytics import YOLO
    # Allow overriding path via env var; default to yolov8n (small) if not provided
    yolo_weights = os.environ.get("YOLO_WEIGHTS", "yolov8n.pt")
    # Only instantiate YOLO if the weights file is present locally. This avoids
    # automatic download at startup and keeps the repository clean. To enable
    # YOLO pass the path via `YOLO_WEIGHTS` env var and ensure the file exists.
    if os.path.exists(yolo_weights):
        try:
            yolo = YOLO(yolo_weights)
            YOLO_AVAILABLE = True
        except Exception:
            # Could not load weights — continue but mark YOLO unavailable
            yolo = None
            YOLO_AVAILABLE = False
    else:
        # Weights not present; YOLO will not be used.
        yolo = None
        YOLO_AVAILABLE = False
except Exception:
    YOLO_AVAILABLE = False


def detect_flower_pil(pil_image: Image.Image):
    """
    Run YOLO detection on a PIL image and return the largest flower bbox (x1,y1,x2,y2)
    and the detection confidence. If YOLO is not available, return None.
    """
    if not YOLO_AVAILABLE or yolo is None:
        return None

    # Convert PIL to BGR numpy array for OpenCV/YOLO
    img_rgb = np.array(pil_image)
    img_bgr = img_rgb[:, :, ::-1]

    try:
        results = yolo(img_bgr)
    except Exception:
        return None

    boxes = []
    for r in results:
        # r.boxes.data: each row [x1, y1, x2, y2, conf, cls]
        data = getattr(r, 'boxes').data.tolist() if getattr(r, 'boxes', None) is not None else []
        names = getattr(r, 'names', {}) if getattr(r, 'names', None) is not None else {}
        for row in data:
            x1, y1, x2, y2, conf, cls = row
            cls = int(cls)
            cls_name = names.get(cls, str(cls))
            # Accept detection if class name contains 'flower' or 'plant' (best-effort)
            if isinstance(cls_name, str) and ("flower" in cls_name.lower() or "plant" in cls_name.lower()):
                boxes.append((int(x1), int(y1), int(x2), int(y2), float(conf)))
            else:
                # If model has only one class or unknown names, also accept high-confidence detections
                if float(conf) >= 0.5:
                    boxes.append((int(x1), int(y1), int(x2), int(y2), float(conf)))

    if not boxes:
        return None

    # Return largest box by area
    boxes_sorted = sorted(boxes, key=lambda b: (b[2]-b[0])*(b[3]-b[1]), reverse=True)
    x1, y1, x2, y2, conf = boxes_sorted[0]
    return (x1, y1, x2, y2, conf)


def detect_flower_raw(pil_image: Image.Image):
    """Return full list of YOLO detections (class id, name, box, confidence).

    Returns empty list if YOLO is unavailable or no detections.
    """
    if not YOLO_AVAILABLE or yolo is None:
        return []

    img_rgb = np.array(pil_image)
    img_bgr = img_rgb[:, :, ::-1]

    try:
        results = yolo(img_bgr)
    except Exception:
        return []

    detections = []
    for r in results:
        data = getattr(r, 'boxes').data.tolist() if getattr(r, 'boxes', None) is not None else []
        names = getattr(r, 'names', {}) if getattr(r, 'names', None) is not None else {}
        for row in data:
            x1, y1, x2, y2, conf, cls = row
            cls = int(cls)
            cls_name = names.get(cls, str(cls))
            detections.append({
                'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2),
                'conf': float(conf), 'class_id': cls, 'class_name': cls_name
            })

    return detections


def draw_detections_on_image(pil_image: Image.Image, detections: list):
    """Return a copy of PIL image with detections drawn (boxes + labels)."""
    img = pil_image.copy()
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    for d in detections:
        x1, y1, x2, y2 = d['x1'], d['y1'], d['x2'], d['y2']
        conf = d.get('conf', 0)
        name = str(d.get('class_name', d.get('class_id', '')))
        color = (255, 0, 0)
        draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
        label = f"{name} {conf:.2f}"
        text_size = draw.textsize(label, font=font) if font else (0, 0)
        draw.rectangle([x1, y1 - text_size[1] - 4, x1 + text_size[0] + 4, y1], fill=color)
        draw.text((x1 + 2, y1 - text_size[1] - 2), label, fill=(255, 255, 255), font=font)

    return img


@app.post("/analyze")
async def analyze(file: UploadFile = File(...), debug: bool = False):
    """
    Endpoint that first detects a flower in the submitted image using YOLO (if available),
    crops the detected flower region and then classifies disease with the classifier model.

    Response JSON:
      - found_flower: bool
      - flower_confidence: float (0-1) or null
      - disease_label: string or null
      - disease_confidence: float (0-1) or null
      - message: optional text
    """
    contents = await file.read()
    try:
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Detect flower via YOLO (best-effort). If not available, proceed to classification on whole image.
    bbox = detect_flower_pil(pil_img)
    raw_detections = []
    if debug and YOLO_AVAILABLE:
        # collect raw detections for debugging purposes
        raw_detections = detect_flower_raw(pil_img)
    if bbox is None:
        # No flower detected (or YOLO not available). If YOLO unavailable, we still try classify whole image.
        if not YOLO_AVAILABLE:
            # Note: classifier expects a flower crop; using whole image as fallback
            label, confidence = model.predict(pil_img)
            return JSONResponse(content={
                "found_flower": None,
                "flower_confidence": None,
                "disease_label": label,
                "disease_confidence": float(confidence),
                "message": "YOLO not available or no flower detected; classification run on full image as fallback.",
                "yolo_available": YOLO_AVAILABLE,
                "yolo_detections": raw_detections
            })
        else:
            return JSONResponse(content={
                "found_flower": False,
                "flower_confidence": 0.0,
                "disease_label": None,
                "disease_confidence": None,
                "message": "No flower detected in the image.",
                "yolo_available": YOLO_AVAILABLE,
                "yolo_detections": raw_detections
            })

    x1, y1, x2, y2, fconf = bbox
    # Crop and convert to PIL for classifier
    img_np = np.array(pil_img)
    crop_np = img_np[y1:y2, x1:x2]
    if crop_np.size == 0:
        return JSONResponse(content={
            "found_flower": True,
            "flower_confidence": float(fconf),
            "disease_label": None,
            "disease_confidence": None,
            "message": "Detected bbox produced empty crop."
        })

    crop_pil = Image.fromarray(crop_np)
    label, confidence = model.predict(crop_pil)

    return JSONResponse(content={
        "found_flower": True,
        "flower_confidence": float(fconf),
        "disease_label": label,
        "disease_confidence": float(confidence),
        "yolo_available": YOLO_AVAILABLE,
        "yolo_detections": (raw_detections if debug else [])
    })


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Backward-compatible single-image predict (runs classifier on whole image)."""
    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    label, confidence = model.predict(img)
    has_botrytis = label == 'botrytis'
    return JSONResponse(content={"has_botrytis": has_botrytis, "confidence": float(confidence)})


@app.post("/debug_detect")
async def debug_detect(file: UploadFile = File(...), min_conf: float = 0.1, draw: bool = False):
    """
    Debug endpoint: run YOLO detection with a lower confidence threshold and
    return raw detections. Optionally return a base64 image with boxes drawn.

    Query params:
      - min_conf: float between 0 and 1 (default 0.1)
      - draw: bool (if true returns `image_base64` with boxes)
    """
    contents = await file.read()
    try:
        pil_img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    if not YOLO_AVAILABLE or yolo is None:
        return JSONResponse(content={
            "yolo_available": False,
            "yolo_detections": [],
            "message": "YOLO not available on server."
        })

    # Run YOLO with adjusted confidence threshold if supported by ultralytics
    try:
        results = yolo(np.array(pil_img)[:, :, ::-1], conf=min_conf)
    except TypeError:
        # older ultralytics versions may accept kwargs differently
        try:
            results = yolo(np.array(pil_img)[:, :, ::-1])
        except Exception as e:
            return JSONResponse(content={"error": f"YOLO run failed: {e}"}, status_code=500)

    detections = []
    for r in results:
        data = getattr(r, 'boxes').data.tolist() if getattr(r, 'boxes', None) is not None else []
        names = getattr(r, 'names', {}) if getattr(r, 'names', None) is not None else {}
        for row in data:
            x1, y1, x2, y2, conf, cls = row
            cls = int(cls)
            cls_name = names.get(cls, str(cls))
            detections.append({
                'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2),
                'conf': float(conf), 'class_id': cls, 'class_name': cls_name
            })

    resp = {
        "yolo_available": True,
        "yolo_detections": detections,
        "min_conf": float(min_conf)
    }

    if draw and detections:
        drawn = draw_detections_on_image(pil_img, detections)
        import base64
        buffered = io.BytesIO()
        drawn.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode('ascii')
        resp['image_base64'] = img_b64

    return JSONResponse(content=resp)
