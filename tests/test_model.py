import os
from dotenv import load_dotenv
import pytest
from app import create_app
from utils.s3_utils import download_from_s3

# Cargar variables de entorno desde .env o GitHub Actions
load_dotenv()

# Configuración de variables
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
IMAGE_KEY = "Datos-prueba/Pug_600.jpg"
MODEL_KEY = os.getenv("S3_MODEL_KEY", "densenet121_Opset17.onnx")
LOCAL_IMG_PATH = f"tests/{IMAGE_KEY}"
LOCAL_MODEL_PATH = "onnx_models/densenet121_Opset17.onnx"

@pytest.fixture(scope="module")
def client():
    os.makedirs("tests/Datos-prueba", exist_ok=True)
    os.makedirs("onnx_models", exist_ok=True)

    # Descargar imagen de prueba si no existe
    if not os.path.exists(LOCAL_IMG_PATH):
        download_from_s3(S3_BUCKET, IMAGE_KEY, LOCAL_IMG_PATH)

    # Descargar modelo ONNX si no existe
    if not os.path.exists(LOCAL_MODEL_PATH):
        download_from_s3(S3_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)

    # Crear la app Flask
    app = create_app()
    app.testing = True
    return app.test_client()

def test_index_post_with_image(client):
    assert os.path.exists(LOCAL_IMG_PATH)
    with open(LOCAL_IMG_PATH, "rb") as img_file:
        data = {
            "image": (img_file, IMAGE_KEY)
        }
        response = client.post("/", content_type="multipart/form-data", data=data)

    assert response.status_code == 200
    assert b"label" in response.data or b"Desconocido" in response.data
