from pydantic import BaseModel


class FileResponse(BaseModel):
    id: int
    reference: str
    url: str
