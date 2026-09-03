from pathlib import Path

from src.converter import convert_pdfs
from src.ollama_client import start_qa


INPUT_FOLDER = Path("input_data")
MARKDOWN_FOLDER = Path("results/markdown")
METADATA_FILE = Path("results/metadata.json")


def select_document():
    markdown_files = sorted(
        MARKDOWN_FOLDER.glob("*.md")
    )

    if not markdown_files:
        print("\nNo converted documents found.")
        print("Convert the PDF files first.")
        return None

    print("\nConverted documents:")

    for index, file in enumerate(markdown_files, start=1):
        print(f"{index}. {file.name}")

    while True:
        choice = input(
            "\nSelect a document number: "
        ).strip()

        if not choice.isdigit():
            print("Please enter a valid number.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(markdown_files):
            return markdown_files[choice - 1]
        print("Please select a number from the list.")


def explore_document():
    markdown_file = select_document()

    if markdown_file is None:
        return

    markdown_text = markdown_file.read_text(encoding="utf-8")

    print(f"\nSelected: {markdown_file.name}")

    start_qa(markdown_text)


def main():
    print("\nConvert PDFs to Markdown and explore them with local AI.")

    while True:
        print("\nChoose an option:")
        print("1. Convert PDFs from input_data")
        print("2. Explore a converted document")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            convert_pdfs(
                INPUT_FOLDER,
                MARKDOWN_FOLDER,
                METADATA_FILE,
            )

        elif choice == "2":
            explore_document()

        elif choice == "3":
            print("\nApplication closed.")
            break

        else:
            print("\nPlease choose 1, 2, or 3.")


if __name__ == "__main__":
    main()