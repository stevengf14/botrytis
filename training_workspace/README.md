# 🧠 Botrytis Detection - Training Workspace

Utilities and scripts to prepare the YOLO image dataset and train the YOLOv8 object detection model for Botrytis cinerea.

## 🚀 Quick Start

1. **Prepare Environment**
   It's recommended to use the same Python environment as the backend:
   ```powershell
   cd training_workspace
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r ../backend/requirements.txt
   ```

2. **Dataset Preparation**
   Execute the dataset distribution script to automatically generate `data.yaml` and the corresponding 80/20 train/validation splits.
   ```powershell
   python train_yolo.py
   ```

3. **Training**
   - The `train_yolo.py` script utilizes `ultralytics.YOLO` (`yolov8m.pt`).
   - Trained model weights are subsequently output to the `runs/detect/` folder.

## 📝 Colab GPU Automation
- For faster GPU acceleration during training epochs, use the provided `train_yolo_colab.ipynb` notebook directly on Google Colab.

---
**Authors:** Steven Andrés Guamán Figueroa & Jonathan Santiago Almeida Salas
