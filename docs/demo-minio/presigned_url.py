from datetime import timedelta

from client import client

bucket_name = "python-test-bucket"
object_name = "uploaded-test-file.txt"

url_get = client.presigned_get_object(
    bucket_name, object_name, expires=timedelta(hours=1)
)
print(f"Presigned URL: {url_get}")
url_put = client.presigned_put_object(
    bucket_name, "uploaded_file.txt", expires=timedelta(hours=1)
)
print(f"curl -X PUT -T file.txt '{url_put}'")
