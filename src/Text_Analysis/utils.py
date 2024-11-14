import os
import chardet
import pymupdf

def extract_raw_from_file(file_path: str, file_format: str) -> str:
    """
    Extracts raw text from a file. If the file is a PDF, it converts it to text first.
    Supports 'txt' and 'pdf' formats.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} doesn't exist")

    if file_format not in ("txt", "pdf"):
        raise ValueError(f"Invalid file format: {file_format}")

    if file_format == "pdf":
        file_path = _convert_pdf_to_txt(file_path)

    # Detect file encoding and read file content
    file_encoding = _detect_file_encoding(file_path)
    with open(file_path, 'r', encoding=file_encoding, errors='ignore') as f:
        return f.read().lower()

def _convert_pdf_to_txt(file_path: str) -> str:
    """
    Converts a PDF file to a TXT file and returns the path to the TXT file.
    """
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    converted_file_path = os.path.join(temp_dir, os.path.basename(file_path).replace(".pdf", ".txt"))

    with pymupdf.open(file_path) as pdf_file:
        with open(converted_file_path, "wb") as out:
            for page in pdf_file:
                out.write(page.get_text().encode("utf-8"))

    return converted_file_path

def _detect_file_encoding(file_path: str) -> str:
    """
    Detects the encoding of a file and returns the encoding name.
    """
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        return chardet.detect(raw_data)['encoding']