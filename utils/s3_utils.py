import boto3
import os

def download_from_s3(bucket, key, dest):
    if os.path.exists(dest):
        print(f"✅ Ya existe: {dest}")
        return

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f"⬇️ Descargando desde s3://{bucket}/{key}")
    s3 = boto3.client("s3")
    try:
        s3.download_file(bucket, key, dest)
        print(f"✅ Descargado en {dest}")
    except s3.exceptions.NoSuchKey:
        print(f"❌ El archivo '{key}' no existe en el bucket '{bucket}'")
    except Exception as e:
        print(f"❌ Error al descargar desde S3: {e}")

