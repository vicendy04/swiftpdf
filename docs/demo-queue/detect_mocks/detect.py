import os
import random
import shutil
import time


def faces(image_path):
    """
    Mock face detection function that simulates processing time
    and returns either the original image or a "processed" version

    Args:
        image_path: Path to the temporary image file to process

    Returns:
        str: Path to the result file (either new processed file or original)
    """
    # Simulate processing time
    process_time = random.uniform(0.5, 2.0)
    time.sleep(process_time)

    # 30% chance to "detect" faces
    if random.random() < 0.3:
        print("[WORKER] Faces detected!")
        # Create a new temp file for processed result
        base, ext = os.path.splitext(image_path)
        result_path = f"{base}_processed{ext}"

        # Copy temp file to create processed version
        shutil.copy2(image_path, result_path)
        return result_path
    else:
        print("[WORKER] No faces detected, returning original")
        # For no detection, we'll create a copy anyway to maintain consistent behavior
        result_path = f"{image_path}_result"
        shutil.copy2(image_path, result_path)
        print(f"[WORKER] Created result at: {result_path}")
        return result_path
