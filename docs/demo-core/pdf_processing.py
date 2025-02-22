import os
from typing import List, Tuple

import fitz


def merge(input_files: List[str], output_file: str) -> bool:
    try:
        new_file = fitz.open()
        for file in input_files:
            with fitz.open(file) as mfile:
                new_file.insert_pdf(mfile)
        new_file.save(output_file, garbage=3, deflate=True)
        new_file.close()
        return True
    except Exception as e:
        print(f"Error merging PDFs: {str(e)}")
        return False


def split_pdf_ranges(
    input_file: str, output_folder: str, ranges: List[Tuple[int, int]]
) -> bool:
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        ifile = fitz.open(input_file)
        for _, (start, end) in enumerate(ranges, 1):
            output_path = os.path.join(output_folder, f"split_{start}_{end}.pdf")
            new_file = fitz.open()
            new_file.insert_pdf(ifile, from_page=start - 1, to_page=end - 1)
            new_file.save(output_path, garbage=3, deflate=True)
            new_file.close()
        ifile.close()
        return True
    except Exception as e:
        print(f"Error spliting PDFs: {str(e)}")
        return False


if __name__ == "__main__":
    paths = ["Pdf1.pdf", "Pdf2.pdf"]
    output_file = "output.pdf"
    merge(paths, output_file)
    output_dir = "output_pdfs"
    pages_to_split = [(1, 5), (10, 15), (20, 25)]
    split_pdf_ranges(paths[0], output_dir, pages_to_split)
