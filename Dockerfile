FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
COPY src/ src/                        
COPY onnx_models/ onnx_models/
COPY utils/ utils/
COPY templates/ templates/ 

CMD ["python", "app.py"]
