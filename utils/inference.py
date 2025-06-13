import numpy as np
import onnxruntime as ort
from PIL import Image
import torchvision.transforms as transforms

MODEL_PATH = "src/model.onnx"  # Ruta por defecto (ajústala si es necesario)

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convierte una imagen PIL a un tensor NumPy normalizado compatible con ONNX"""
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),  # C -> H x W x C
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    tensor = transform(image).unsqueeze(0)  # Agrega batch dimension
    return tensor.numpy()

def load_model(model_path: str = MODEL_PATH) -> ort.InferenceSession:
    """Carga un modelo ONNX y devuelve una sesión de inferencia"""
    return ort.InferenceSession(model_path)

def predict(session: ort.InferenceSession, input_tensor: np.ndarray) -> np.ndarray:
    """Realiza una inferencia con el modelo ONNX"""
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: input_tensor})
    return output[0]  # logits
