from pydantic import BaseModel
from typing import List, Optional


class MinioOperation(BaseModel):
    bucket_name: str
    object_name: str
    operation_type: str


class FileInfo(BaseModel):
    name: str
    size: int
    last_modified: str


class ListDirectoryRequest(BaseModel):
    bucket_name: str
    prefix: Optional[str] = ""
    recursive: Optional[bool] = True


class ListDirectoryResponse(BaseModel):
    files: List[FileInfo]


class QueryFileContentRequest(BaseModel):
    bucket_name: str
    object_name: str


class QueryFileContentResponse(BaseModel):
    file_content: str


class UploadFileRequest(BaseModel):
    bucket_name: str
    object_name: str
    file_content: Optional[str] = ""


class UploadFileResponse(BaseModel):
    success: bool
    message: str


class DeleteFileRequest(BaseModel):
    bucket_name: str
    path: str
    recursive: Optional[bool] = False


class DeleteFileResponse(BaseModel):
    success: bool
    message: str
