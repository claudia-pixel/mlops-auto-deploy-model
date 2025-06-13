import os
from dotenv import load_dotenv
import pytest
from app import create_app
from utils.s3_utils import download_from_s3

load_dotenv()  # ✅ Cargar variables del archivo .env

S3_BUCKET = os.getenv("S3_BUCKET_NAME")
IMAGE_KEY = "Datos-prueba/Pug_600.jpg"
LOCAL_IMG_PATH = f"tests/{IMAGE_KEY}"

@pytest.fixture(scope="module")
def client():
    os.makedirs("tests", exist_ok=True)

    if not os.path.exists(LOCAL_IMG_PATH):
        download_from_s3(S3_BUCKET, IMAGE_KEY, LOCAL_IMG_PATH)

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
