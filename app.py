import os
import json
import numpy as np
from PIL import Image
from flask import Flask, request, render_template
import onnxruntime as ort
from utils.s3_utils import download_from_s3

# Configuración
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_MODEL_KEY = os.getenv("S3_MODEL_KEY")
MODEL_PATH = "onnx_models/densenet121_Opset17.onnx"
LABELS_PATH = "src/imagenet1000_clsidx_to_labels.json"
RESULT_PATH = "results/prediction.json"

def create_app():
    app = Flask(__name__)

    # Descargar modelo si no existe
    download_from_s3(S3_BUCKET, S3_MODEL_KEY, MODEL_PATH)

    # Cargar etiquetas
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        class_labels = json.load(f)

    # Cargar modelo ONNX
    ort_session = ort.InferenceSession(MODEL_PATH)

    def preprocess(img):
        img = img.resize((224, 224)).convert("RGB")
        arr = np.array(img).astype(np.float32) / 255.0
        arr = np.transpose(arr, (2, 0, 1))[np.newaxis, :]
        return arr

    @app.route("/", methods=["GET", "POST"])
    def index():
        prediction = None
        label = None
        if request.method == "POST":
            img = Image.open(request.files["image"].stream)
            input_tensor = preprocess(img)
            ort_inputs = {ort_session.get_inputs()[0].name: input_tensor}
            ort_outs = ort_session.run(None, ort_inputs)

            pred_class = int(np.argmax(ort_outs[0]))
            label = class_labels.get(str(pred_class), "Desconocido")

            prediction = {"class_index": pred_class, "label": label}

            os.makedirs("results", exist_ok=True)
            with open(RESULT_PATH, "w", encoding="utf-8") as f:
                json.dump(prediction, f, indent=2, ensure_ascii=False)

        return render_template("index.html", prediction=prediction)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)


      