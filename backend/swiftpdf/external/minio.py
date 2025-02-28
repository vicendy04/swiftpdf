from datetime import timedelta

from django.conf import settings
from minio import Minio

INPUT_BUCKET_NAME = settings.INPUT_BUCKET_NAME
OUTPUT_BUCKET_NAME = settings.OUTPUT_BUCKET_NAME

minio_client = Minio(
    endpoint=settings.MINIO_HOST,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.USE_MINIO_HTTPS,
)


def get_put_url(filename: str, expire: int = 5) -> str:
    return minio_client.presigned_put_object(
        INPUT_BUCKET_NAME, filename, expires=timedelta(minutes=expire)
    )


def get_get_url(filename: str, expire: int = 5) -> str:
    return minio_client.presigned_get_object(
        OUTPUT_BUCKET_NAME, filename, expires=timedelta(minutes=expire)
    )


def initialize_buckets():
    for bucket in [INPUT_BUCKET_NAME, OUTPUT_BUCKET_NAME]:
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)
