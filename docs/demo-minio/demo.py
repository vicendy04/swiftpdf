import os

from client import client
from minio.error import S3Error

bucket_name = "python-test-bucket"
object_name = "uploaded-test-file.txt"


def upload():
    source_file = "tmp/test-file.txt"
    if not os.path.exists(source_file):
        print(f"File {source_file} is not exist")
        return

    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    client.fput_object(
        bucket_name,
        object_name,
        source_file,
    )

    print(
        source_file,
        "successfully uploaded as object",
        object_name,
        "to bucket",
        bucket_name,
    )

    print("List of files in bucket:")
    objects = client.list_objects(bucket_name)
    for obj in objects:
        print(obj.object_name)


def download():
    file_name = "static/downloaded_test_file.txt"
    client.fget_object(bucket_name, object_name, file_name)
    print(f"Downloaded {object_name} to {file_name}.")


if __name__ == "__main__":
    try:
        upload()
        download()
    except S3Error as exc:
        print("error occurred.", exc)
