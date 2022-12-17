import uuid

import boto3
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.data.models import File
from app.common.domain.config import S3_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from app.common.exceptions.app_exceptions import NotFoundException
from app.modules.file.file_dtos import FileResponse
from app.modules.file.file_mappings import file_to_file_response


def upload_file(db: Session, file_upload: UploadFile) -> FileResponse:
    reference = str(uuid.uuid4())
    url = upload_file_to_bucket(reference, file_upload)

    file = File(
        reference=reference,
        url=url
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    return file_to_file_response(file)


def upload_file_to_bucket(reference: str, file_upload: UploadFile) -> str:
    s3 = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_fileobj(file_upload.file, reference)

    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{reference}"


def get_file_by_reference(db: Session, reference: str) -> File:
    file = db.query(File).filter(File.reference == reference).first()

    if not file:
        raise NotFoundException(message=f"File with reference: {reference} does not exist")

    return file
