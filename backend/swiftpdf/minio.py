from datetime import timedelta

from django.conf import settings
from minio import Minio

minio_client = Minio(
    endpoint=settings.MINIO_HOST,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.USE_MINIO_HTTPS,
)

bucket_name = settings.MINIO_BUCKET_NAME


def get_put_url(filename: str, expire: int = 5) -> str:
    found = minio_client.bucket_exists(bucket_name)
    if not found:
        minio_client.make_bucket(bucket_name)
    return minio_client.presigned_put_object(
        bucket_name, filename, expires=timedelta(minutes=expire)
    )
