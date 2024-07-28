from fastapi import APIRouter, HTTPException, Body
from src.api import schemas
from src.domain.minio import MinioService
from typing import Optional

router = APIRouter()
minio_service = MinioService()


@router.get("/list/{bucket_name}", response_model=schemas.ListDirectoryResponse)
async def list_directory(bucket_name: str, prefix: Optional[str] = "", recursive: Optional[bool] = True):
    try:
        request = schemas.ListDirectoryRequest(
            bucket_name=bucket_name, prefix=prefix, recursive=recursive)
        return minio_service.list_directory(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/query/{bucket_name}", response_model=schemas.QueryFileContentResponse)
async def query_file_content(bucket_name: str, object_name: str):
    try:
        request = schemas.QueryFileContentRequest(
            bucket_name=bucket_name, object_name=object_name)
        return minio_service.query_file_content(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload/{bucket_name}", response_model=schemas.UploadFileResponse)
async def upload_text(
    bucket_name: str,
    object_name: str,
    text_content: Optional[str] = Body(default="", media_type="text/plain")
):
    try:
        request = schemas.UploadFileRequest(
            bucket_name=bucket_name, object_name=object_name, file_content=text_content)
        return minio_service.upload_file(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{bucket_name}", response_model=schemas.DeleteFileResponse)
async def delete_file(bucket_name: str, path: str, recursive: Optional[bool] = False):
    try:
        request = schemas.DeleteFileRequest(
            bucket_name=bucket_name, path=path, recursive=recursive)
        return minio_service.delete_file(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
