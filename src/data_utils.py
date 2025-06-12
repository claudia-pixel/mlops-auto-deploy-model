import boto3
from datetime import datetime

def append_prediction_to_s3(bucket: str, key: str, prediction: str):
    s3 = boto3.client('s3')
    local_path = "/tmp/temp_log.txt"
    try:
        s3.download_file(bucket, key, local_path)
    except s3.exceptions.NoSuchKey:
        open(local_path, "w").close()

    with open(local_path, "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}: {prediction}\n")

    s3.upload_file(local_path, bucket, key)
