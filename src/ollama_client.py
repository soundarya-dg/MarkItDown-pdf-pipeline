import ollama

from src.retriever import find_relevant_chunks


def start_qa(markdown_text: str) -> None:

    print("\nDocument Q&A ready.")
    print("Ask a question about the selected document.")
    print("Type 'exit' to stop.")

    while True:
        question = input(
            "\nEnter your question: "
        ).strip()

        if question.lower() == "exit":
            print("\nSession ended.")
            break

        if not question:
            print("Please enter a question.")
            continue

        relevant_chunks = (
            find_relevant_chunks(
                markdown_text,
                question,
            )
        )

        if not relevant_chunks:
            print("\nAnswer:")
            print("The answer is not available in this document.")
            continue

        context = "\n\n".join(
            relevant_chunks
        )

        prompt = f"""
You are answering questions about the uploaded document.

Use only the document content provided below to answer the user's question.

If the answer cannot be found in the provided content, respond exactly:
"The answer is not available in this document."

Do not invent, assume, or use outside knowledge.
Keep the answer clear and concise.

DOCUMENT CONTENT:
{context}

QUESTION:
{question}
"""

        try:
            print("\nSearching the document...")

            response = ollama.chat(
                model="qwen3:4b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            answer = response["message"]["content"]

            print("\nAnswer:")
            print(answer)

        except Exception as error:
            print("\nOllama request failed.")
            print(f"Error: {error}")