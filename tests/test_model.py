from src.model_loader import load_model_from_s3
import os

def test_model_loading():
    session = load_model_from_s3(
        bucket=os.getenv("MODEL_BUCKET"),
        key=os.getenv("MODEL_KEY")
    )
    assert session is not None
    assert session.get_inputs()
