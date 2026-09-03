from pathlib import Path


def create_metadata(pdf_file: Path, markdown_file: Path, markdown_text: str) -> dict:

    return {
        "filename": pdf_file.name,
        "markdown_filename": markdown_file.name,
        "file_size_bytes": pdf_file.stat().st_size,
        "character_count": len(markdown_text),
        "word_count": len(markdown_text.split()),
        "status": "success",
    }