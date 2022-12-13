from app.common.data.models import File
from app.modules.file.file_dtos import FileResponse


def file_to_file_response(file: File) -> FileResponse:

    result = FileResponse(
        id=file.id,
        reference=file.reference,
        url=file.url
    )

    return result
