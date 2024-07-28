from src.api import schemas
from typing import List
import src.grpc_client.minio as minio


class MinioService:
    def __init__(self):
        self.client = minio.connect_grpc()

    def __del__(self):
        self.client.close()

    def list_directory(self, request: schemas.ListDirectoryRequest) -> schemas.ListDirectoryResponse:
        try:
            response = self.client.list_directory(
                bucket_name=request.bucket_name,
                prefix=request.prefix,
                recursive=request.recursive
            )
            files = [
                schemas.FileInfo(
                    name=file.name,
                    size=file.size,
                    last_modified=file.last_modified
                ) for file in response.files
            ]
            return schemas.ListDirectoryResponse(files=files)
        except Exception as e:
            raise Exception(f"Failed to list directory: {str(e)}")

    def query_file_content(self, request: schemas.QueryFileContentRequest) -> schemas.QueryFileContentResponse:
        try:
            response = self.client.query_file_content(
                bucket_name=request.bucket_name,
                object_name=request.object_name
            )
            return schemas.QueryFileContentResponse(
                file_content=response.content
            )
        except Exception as e:
            return Exception(f"Failed to query file content: {str(e)}")

    def upload_file(self, request: schemas.UploadFileRequest) -> schemas.UploadFileResponse:
        try:
            response = self.client.upload_object(
                bucket_name=request.bucket_name,
                object_name=request.object_name,
                file_content=request.file_content
            )
            return schemas.UploadFileResponse(
                success=response.success,
                message=response.message
            )
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")

    def delete_file(self, request: schemas.DeleteFileRequest) -> schemas.DeleteFileResponse:
        try:
            response = self.client.delete_object(
                bucket_name=request.bucket_name,
                path=request.path,
                recursive=request.recursive
            )
            return schemas.DeleteFileResponse(
                success=response.success,
                message=response.message
            )
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")
