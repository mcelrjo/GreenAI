from fastapi import APIRouter, BackgroundTasks
import boto3
import os
from app.services.embedding_service import extract_text_from_pdf, embed_and_store

router_s3 = APIRouter()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

@router_s3.post("/admin/process-s3-pdf")
def process_s3_pdf(background_tasks: BackgroundTasks, s3_key: str, source_id: str):
    temp_path = f"/tmp/{s3_key.replace('/', '_')}"
    s3.download_file(S3_BUCKET_NAME, s3_key, temp_path)

    # Schedule processing in background
    background_tasks.add_task(process_pdf_background, temp_path, source_id)

    return {"status": "S3 PDF received and processing started", "source_id": source_id, "s3_key": s3_key}

def process_pdf_background(temp_path: str, source_id: str):
    text = extract_text_from_pdf(temp_path)
    embed_and_store(text, source_id)
