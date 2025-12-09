from PIL import Image
import numpy as np
import os

class ModelWrapper:
    """Wrapper that attempts to load a PyTorch model if available.

    If PyTorch is not installed or a model file is not provided, the wrapper
    falls back to a simple heuristic (mean brightness) so the API can be
    exercised during early stages.
    """
    def __init__(self):
        self.model = None
        self.torch = None
        try:
            import torch
            self.torch = torch
        except Exception:
            self.torch = None

    def load_model(self, path: str):
        if not self.torch:
            raise RuntimeError("PyTorch not available in this environment")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file not found: {path}")
        # Example: user-saved a scripted or state_dict model. Loading logic
        # may need adaption depending how train.py saves the model.
        self.model = self.torch.load(path, map_location=self.torch.device('cpu'))
        self.model.eval()

    def predict(self, image: Image.Image):
        """Return (label, confidence). If a torch model is loaded, use it.

        Otherwise use a brightness heuristic as a placeholder.
        """
        if self.model and self.torch:
            import torchvision.transforms as T
            transform = T.Compose([
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            x = transform(image).unsqueeze(0)
            with self.torch.no_grad():
                out = self.model(x)
                probs = self.torch.nn.functional.softmax(out, dim=1).cpu().numpy()[0]
                idx = int(probs.argmax())
                label = 'botrytis' if idx == 1 else 'healthy'
                confidence = float(probs[idx])
                return label, confidence

        # Dummy heuristic: use mean brightness
        arr = np.array(image).astype(np.float32) / 255.0
        mean = arr.mean()
        # threshold chosen empirically as placeholder
        if mean < 0.55:
            return 'botrytis', 0.6
        else:
            return 'healthy', 0.7
