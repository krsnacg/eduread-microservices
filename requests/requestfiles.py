from typing import Annotated

from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


### Using UploadFile has several advantages over bytes:

    # You don't have to use File() in the default value of the parameter.
    # It uses a "spooled" file:
    #     A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
    # This means that it will work well for large files like images, videos, large binaries, etc. without consuming all the memory.
    # You can get metadata from the uploaded file.
    # It has a file-like async interface.
    # It exposes an actual Python SpooledTemporaryFile object that you can pass directly to other libraries that expect a file-like object.

@router.post("/files/upload/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


### OPTIONAL FILE UPLOAD ###

@router.post("/files/upload_optional/")
async def create_upload_file_optional(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    return {"filename": file.filename}


### UploadFile with Additional Metadata ###

@router.post("/files/upload_with_metadata/")
async def create_file_with_metadata(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}

@router.post("/files/uploadfile_with_metadata/")
async def create_upload_file_with_metadata(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    return {"filename": file.filename, "content_type": file.content_type}

### MULTIPLE FILES UPLOAD ###

@router.post("/files/upload_multiple/")
async def create_files_multiple(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}

@router.post("/files/upload_multiple_files/")
async def create_upload_files_multiple(file: list[UploadFile]):
    return {"filenames": [f.filename for f in file]}