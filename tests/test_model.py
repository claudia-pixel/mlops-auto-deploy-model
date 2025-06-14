import os
from dotenv import load_dotenv
import pytest
from app import create_app
from utils.s3_utils import download_from_s3

load_dotenv()  # Cargar variables desde .env o GitHub Actions

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
IMAGE_KEY = "Datos-prueba/Pug_600.jpg"
MODEL_KEY = os.getenv("S3_MODEL_KEY")  # Ej: "densenet121_Opset17.onnx"

LOCAL_IMG_PATH = f"tests/{IMAGE_KEY}"
LOCAL_MODEL_PATH = f"onnx_models/{MODEL_KEY}"

@pytest.fixture(scope="module")
def client():
    # Asegura carpetas necesarias
    os.makedirs(os.path.dirname(LOCAL_IMG_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(LOCAL_MODEL_PATH), exist_ok=True)

    # Descargar imagen si no existe
    if not os.path.exists(LOCAL_IMG_PATH):
        print(f"⬇️ Descargando imagen desde s3://{S3_BUCKET}/{IMAGE_KEY}")
        download_from_s3(S3_BUCKET, IMAGE_KEY, LOCAL_IMG_PATH)

    # Descargar modelo si no existe
    if not os.path.exists(LOCAL_MODEL_PATH):
        print(f"⬇️ Descargando modelo desde s3://{S3_BUCKET}/{MODEL_KEY}")
        download_from_s3(S3_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)

    # ✅ Verificar modelo descargado
    if not os.path.exists(LOCAL_MODEL_PATH) or os.path.getsize(LOCAL_MODEL_PATH) < 5000:
        print(f"❌ Modelo dañado o muy pequeño: {LOCAL_MODEL_PATH}")
        try:
            with open(LOCAL_MODEL_PATH, "r", errors="ignore") as f:
                print("Contenido parcial del modelo (texto):")
                print(f.read(300))
        except Exception as e:
            print(f"No se pudo leer como texto: {e}")
        raise RuntimeError("⚠️ El modelo ONNX está corrupto o incompleto.")

    # Crear app Flask
    app = create_app()
    app.testing = True
    return app.test_client()

def test_index_post_with_image(client):
    assert os.path.exists(LOCAL_IMG_PATH), "La imagen de prueba no existe"
    with open(LOCAL_IMG_PATH, "rb") as img_file:
        data = {
            "image": (img_file, IMAGE_KEY)
        }
        response = client.post("/", content_type="multipart/form-data", data=data)

    assert response.status_code == 200
    assert b"label" in response.data or b"Desconocido" in response.data
