from datetime import timedelta

from django.conf import settings
from minio import Minio

BUCKET_NAME = settings.MINIO_BUCKET_NAME

minio_client = Minio(
    endpoint=settings.MINIO_HOST,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.USE_MINIO_HTTPS,
)


def get_put_url(filename: str, expire: int = 5) -> str:
    found = minio_client.bucket_exists(BUCKET_NAME)
    if not found:
        minio_client.make_bucket(BUCKET_NAME)
    return minio_client.presigned_put_object(
        BUCKET_NAME, filename, expires=timedelta(minutes=expire)
    )
