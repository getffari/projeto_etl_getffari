from io import BytesIO
import pandas as pd
from minio import Minio
from minio.error import S3Error

class MinioBucket:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MinioBucket, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self):
        self.client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin123",
            secure=False
        )

    def upload_to_minio(self, bucket_name, object_name, file_path):
        try:
            self.client.fput_object(bucket_name, object_name, file_path)
            print(f"Arquivo '{object_name}' enviado para o bucket '{bucket_name}' com sucesso!")
        except S3Error as e:
            print(f"Erro ao enviar o arquivo: {e}")

    def list_objects_in_bucket(self, bucket_name):
        try:
            objects = self.client.list_objects(bucket_name)
            for obj in objects:
                print(f"Encontrado objeto: {obj.object_name}")
        except S3Error as e:
            print(f"Erro ao listar objetos: {e}")

    def get_csv_content(self, bucket_name, object_name):
        try:
            response = self.client.get_object(bucket_name, object_name)
            csv_content = pd.read_csv(BytesIO(response.data), delimiter=';', on_bad_lines='warn')
            response.close()
            response.release_conn()
            return csv_content
        except S3Error as e:
            print(f"Erro ao acessar o conteúdo do arquivo: {e}")
            return None
        

