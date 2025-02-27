import os

import fitz
from minio import Minio
from nanoid import generate

# Region: Configurations
INPUT_BUCKET_NAME = "media"
OUTPUT_BUCKET_NAME = "output"

MINIO_HOST = os.getenv("MINIO_HOST", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
USE_MINIO_HTTPS = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

minio_client = Minio(
    endpoint=MINIO_HOST,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=USE_MINIO_HTTPS,
)
# EndRegion


def process_pdf_task(data: dict) -> list[str]:
    """Main entry point for PDF processing tasks"""
    input_objects = data.get("input_files", [])
    tool_type = data.get("tool", "")

    if not input_objects:
        raise ValueError("No input files provided")

    # Download all input files first
    local_input_paths = download_objects_from_minio(input_objects)
    output_paths = []

    try:
        if tool_type == "merge":
            result = process_pdf_merge(local_input_paths, output_paths)
        elif tool_type == "split":
            ranges = data.get("ranges", [])
            result = process_pdf_split(local_input_paths[0], ranges, output_paths)
        else:
            raise ValueError(f"Unsupported tool type: {tool_type}")

        return result
    finally:
        # Cleanup all temporary files
        cleanup_files(local_input_paths + output_paths)


def process_pdf_merge(input_paths: list[str], output_paths: list[str]) -> list[str]:
    """Merge multiple PDF files into one"""
    try:
        object_name, output_path = generate_output_path("merged")
        output_paths.append(output_path)

        # Merge PDF logic
        merged_doc = fitz.open()
        for path in input_paths:
            with fitz.open(path) as pdf:
                merged_doc.insert_pdf(pdf)

        merged_doc.save(output_path, garbage=3, deflate=True)
        merged_doc.close()

        # Upload result
        upload_object_to_minio(output_path, object_name)
        return [object_name]
    except Exception as e:
        raise RuntimeError(f"Merging failed: {str(e)}")


def process_pdf_split(
    input_path: str, ranges: list[dict], output_paths: list[str]
) -> list[str]:
    """Split PDF into multiple ranges"""
    if not ranges:
        raise ValueError("No page ranges specified")

    try:
        result_objects = []
        with fitz.open(input_path) as src_doc:
            total_pages = len(src_doc)

            for _, range_spec in enumerate(ranges):
                start = max(1, range_spec.get("start", 1))
                end = min(total_pages, range_spec.get("end", total_pages))

                if start > end:
                    raise ValueError(f"Invalid range {start}-{end}")

                object_name, output_path = generate_output_path(f"split_{start}-{end}")
                output_paths.append(output_path)

                # Extract pages
                new_doc = fitz.open()
                new_doc.insert_pdf(src_doc, from_page=start - 1, to_page=end - 1)
                new_doc.save(output_path, garbage=3, deflate=True)
                new_doc.close()

                # Upload result
                upload_object_to_minio(output_path, object_name)
                result_objects.append(object_name)

        return result_objects
    except Exception as e:
        raise RuntimeError(f"Splitting failed: {str(e)}")


# Region: Helper functions
def generate_output_path(prefix: str) -> tuple[str, str]:
    """Generate unique output path and object name"""
    unique_id = generate(size=10)
    object_name = f"{unique_id}_{prefix}.pdf"
    return object_name, os.path.join(OUTPUT_DIR, object_name)


def download_objects_from_minio(object_names: list[str]) -> list[str]:
    """Download multiple objects from MinIO"""
    local_paths = []
    for obj_name in object_names:
        local_path = os.path.join(TEMP_DIR, obj_name)
        minio_client.fget_object(INPUT_BUCKET_NAME, obj_name, local_path)
        local_paths.append(local_path)
    return local_paths


def upload_object_to_minio(file_path: str, object_name: str) -> None:
    """Upload file to MinIO storage"""
    minio_client.fput_object(
        bucket_name=OUTPUT_BUCKET_NAME,
        object_name=object_name,
        file_path=file_path,
    )


def cleanup_files(paths: list[str]) -> None:
    """Cleanup temporary files"""
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Warning: Failed to delete {path} - {str(e)}")


def initialize_buckets():
    """Ensure required buckets exist"""
    for bucket in [INPUT_BUCKET_NAME, OUTPUT_BUCKET_NAME]:
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)


# Initialize buckets on startup
initialize_buckets()
# EndRegion
