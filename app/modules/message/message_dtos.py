from typing import Optional

from pydantic import BaseModel, validator

from app.modules.file import file_validator
from app.modules.file.file_dtos import FileResponse


class MessageResponse(BaseModel):
    id: int
    description: Optional[str]
    recording: FileResponse


class MessageCreateRequest(BaseModel):
    description: str
    recording_reference: str

    @validator("recording_reference")
    def recording_reference_is_valid(cls, recording_reference):
        if not file_validator.is_valid_reference(recording_reference):
            raise ValueError("Invalid recording_reference")

        return recording_reference
