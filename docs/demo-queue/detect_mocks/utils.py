import mimetypes
import os
import tempfile


def write_temp_file(content, content_type):
    """Write binary content to a temporary file"""
    ext = mimetypes.guess_extension(content_type) or ".tmp"
    fd, path = tempfile.mkstemp(suffix=ext)
    with os.fdopen(fd, "wb") as temp:
        temp.write(content)
    return path


def read_image(filepath):
    """Read image file contents"""
    try:
        with open(filepath, "rb") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"[ERROR] Image file not found: {filepath}")
        raise


def mime_type(filepath):
    """Get MIME type for a file"""
    mime = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
    return mime


def get_images():
    """Return list of test image files from the images directory"""
    # Get the directory containing this file
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(current_dir, "images")

    # Check if images directory exists
    if not os.path.exists(images_dir):
        print(f"[ERROR] Images directory not found: {images_dir}")
        print("[INFO] Creating images directory...")
        os.makedirs(images_dir)

    # Get all jpg and png files in the images directory
    images = []
    for filename in os.listdir(images_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            images.append(os.path.join(images_dir, filename))

    if not images:
        print("[WARNING] No images found in images directory!")
    else:
        print(f"[UTILS] Found {len(images)} images to process: {', '.join(images)}")

    return images


def display_image(content, content_type):
    """Mock function to display an image"""
    print("-" * 50)
