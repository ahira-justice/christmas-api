from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session

from app.common.auth.bearer import BearerAuth
from app.common.data.dtos import ValidationErrorResponse, ErrorResponse
from app.common.domain.constants import FILES_URL
from app.common.domain.database import get_db
from app.modules.file import file_service
from app.modules.file.file_dtos import FileResponse

controller = APIRouter(
    prefix=FILES_URL,
    tags=["Files"]
)


@controller.post(
    path="",
    dependencies=[Depends(BearerAuth())],
    status_code=200,
    responses={
        200: {"model": FileResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        422: {"model": ValidationErrorResponse}
    }
)
async def upload_file(
        file: UploadFile,
        db: Session = Depends(get_db)
):
    """Upload file"""
    return file_service.upload_file(db, file)
