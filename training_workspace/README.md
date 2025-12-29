Training workspace - Botrytis Detection
=======================================

This folder contains utilities and scripts to prepare the dataset and train YOLO models.

Quick start
-----------

1) Prepare environment (recommended: same Python venv used for backend):

```powershell
cd training_workspace
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ../backend/requirements.txt
```

2) Repair dataset and generate data.yaml (script):

```powershell
cd training_workspace
python train_yolo.py
```

3) Training

- The `train_yolo.py` script uses `ultralytics.YOLO` and expects `yolov8m.pt` in the folder or available by name.
- Trained weights will be saved in `runs/detect` by default.

Notes
-----
- Prints and logs in these scripts are concise and in English. Comments in the code may be in Spanish.
- Use the notebook `train_yolo_colab_new.ipynb` if you prefer to run on Colab (GPU).
