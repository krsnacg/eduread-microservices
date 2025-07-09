from typing import Annotated
from fastapi import APIRouter, Form, File, UploadFile

router = APIRouter()

@router.post("/files/formandfiles/")
async def create_file_formandfiles(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }