import os

import boto3
from django.conf import settings


class S3Service:
    def __init__(self):
        s3_resource = boto3.Session().resource('s3')
        self._signatures_bucket = s3_resource.Bucket(settings.AWS_SIGNATURES_BUCKET_NAME)
        self._user_files_bucket = s3_resource.Bucket(settings.AWS_USER_FILES_BUCKET_NAME)

    def upload_user_file(self, file_path: str) -> str:
        return self._upload_file(self._user_files_bucket, file_path)

    def upload_signature(self, file_path: str) -> str:
        return self._upload_file(self._signatures_bucket, file_path)

    def _upload_file(self, bucket, file_path: str) -> str:
        assert bucket in (self._signatures_bucket, self._user_files_bucket)

        key = os.path.basename(file_path)
        file_obj = bucket.Object(key=key)
        file_obj.upload_file(file_path)

        return key
