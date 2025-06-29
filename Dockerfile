FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY src/ src/                        
COPY utils/ utils/
COPY templates/ templates/ 

CMD ["python", "app.py"]