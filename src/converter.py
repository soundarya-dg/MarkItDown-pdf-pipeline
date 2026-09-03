from pathlib import Path
from datetime import datetime
import json

from markitdown import MarkItDown

from src.preprocessor import preprocess_markdown
from src.metadata import create_metadata


def convert_pdfs(input_folder: Path, output_folder: Path, metadata_file: Path,) -> None:

    output_folder.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_folder.glob("*.pdf"))
    all_metadata = []

    if not pdf_files:
        print("\nNo PDF files found.")
        return

    markitdown = MarkItDown()

    print(f"\nFound {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:
        try:
            print(f"\nProcessing: {pdf_file.name}")

            result = markitdown.convert(
                pdf_file
            )

            processed_text = preprocess_markdown(
                result.text_content
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d-%H%M%S"
            )

            clean_name = pdf_file.stem.lower()
            clean_name = clean_name.replace(" ", "-")

            while "--" in clean_name:
                clean_name = clean_name.replace("--", "-")

            clean_name = clean_name.strip("-")
            output_filename = (f"{clean_name}-{timestamp}.md")

            output_file = (
                output_folder
                / output_filename
            )

            output_file.write_text(processed_text, encoding="utf-8")

            metadata = create_metadata(pdf_file, output_file, processed_text)
            all_metadata.append(metadata)

            print(f"Saved: {output_filename}")

        except Exception as error:
            all_metadata.append(
                {
                    "filename": pdf_file.name,
                    "status": "failed",
                    "error": str(error),
                }
            )
            print(f"Failed: {pdf_file.name}")
            print(f"Error: {error}")

    metadata_file.parent.mkdir(parents=True, exist_ok=True)
    metadata_file.write_text(
        json.dumps(
            all_metadata,
            indent=4,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"\nMetadata saved to: {metadata_file}")

    print("\nPDF processing complete.")