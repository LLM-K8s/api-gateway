import grpc
import src.grpc_client.Minio_pb2 as Minio_pb2
import src.grpc_client.Minio_pb2_grpc as Minio_pb2_grpc
import src.config as config
import os

settings = config.settings


class MinioGrpcClient:
    def __init__(self):
        os.environ['GRPC_VERBOSITY'] = 'ERROR'
        self.channel = None
        self.stub = None
        self.connect()

    def connect(self):
        server_address = settings.GRPC_SERVER
        try:
            self.channel = grpc.insecure_channel(server_address)
            self.stub = Minio_pb2_grpc.MinioServiceStub(self.channel)
        except Exception as e:
            print(f"Failed to connect to gRPC server: {str(e)}")
            raise

    def close(self):
        if self.channel:
            self.channel.close()

    def list_directory(self, bucket_name, prefix="", recursive=True):
        request = Minio_pb2.ListDirectoryRequest(
            bucket_name=bucket_name,
            prefix=prefix,
            recursive=recursive
        )
        return self.stub.ListDirectory(request)

    def query_file_content(self, bucket_name, object_name):
        request = Minio_pb2.QueryFileContentRequest(
            bucket_name=bucket_name,
            object_name=object_name
        )
        return self.stub.QueryFileContent(request)

    def upload_object(self, bucket_name, object_name, file_content):
        request = Minio_pb2.UploadFileRequest(
            bucket_name=bucket_name,
            object_name=object_name,
            chunk_data=file_content.encode('utf-8')
        )
        return self.stub.UploadFile(iter([request]))

    def delete_object(self, bucket_name, path, recursive=False):
        request = Minio_pb2.DeleteFileOrDirectoryRequest(
            bucket_name=bucket_name,
            path=path,
            recursive=recursive
        )
        return self.stub.DeleteFileOrDirectory(request)


def connect_grpc():
    return MinioGrpcClient()


if __name__ == "__main__":
    client = connect_grpc()
    response = client.delete_object("kploit", "test/ff.txt")
    print(str(response))

    client.close()
