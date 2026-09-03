import re


def split_into_chunks(text: str, chunk_size: int = 3000) -> list[str]:

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(
            text[i:i + chunk_size]
        )
    return chunks


def get_keywords(question: str) -> list[str]:

    words = re.findall(
        r"\b[a-zA-Z0-9'-]+\b",
        question.lower(),
    )

    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "in",
        "on",
        "to",
        "for",
        "what",
        "which",
        "who",
        "how",
        "does",
        "do",
        "did",
        "used",
        "use",
        "about",
    }

    keywords = []

    for word in words:
        if (
            word not in stop_words
            and len(word) > 2
        ):
            keywords.append(word)
    return keywords


def find_relevant_chunks(text: str, question: str, max_chunks: int = 5) -> list[str]:

    chunks = split_into_chunks(text)
    keywords = get_keywords(question)

    scored_chunks = []

    for chunk in chunks:
        chunk_lower = chunk.lower()

        score = 0

        for keyword in keywords:
            score += chunk_lower.count(
                keyword
            )

        if score > 0:
            scored_chunks.append(
                (score, chunk)
            )

    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    relevant_chunks = [
        chunk
        for score, chunk
        in scored_chunks[:max_chunks]
    ]

    return relevant_chunks