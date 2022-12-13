import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.common.data.models import File
from app.common.exceptions.app_exceptions import NotFoundException
from app.modules.file.file_dtos import FileResponse
from app.modules.file.file_mappings import file_to_file_response


def upload_file(db: Session, file_upload: UploadFile) -> FileResponse:
    url = upload_file_to_bucket(file_upload)

    file = File(
        reference=str(uuid.uuid4()),
        url=url
    )

    db.add(file)
    db.commit()
    db.refresh(file)

    return file_to_file_response(file)


def upload_file_to_bucket(file_upload) -> str:
    pass


def get_file_by_reference(db: Session, reference: str) -> File:
    file = db.query(File).filter(File.reference == reference).first()

    if not file:
        raise NotFoundException(message=f"File with reference: {reference} does not exist")

    return file
