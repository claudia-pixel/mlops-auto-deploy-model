import boto3
import tempfile
import onnxruntime as ort

def load_model_from_s3(bucket: str, key: str) -> ort.InferenceSession:
    s3 = boto3.client("s3")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".onnx") as tmp:
        s3.download_file(bucket, key, tmp.name)
        print(f"Modelo descargado en {tmp.name}")
        session = ort.InferenceSession(tmp.name)
    return session
