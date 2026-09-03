import re


def preprocess_markdown(text: str) -> str:
    # Remove standalone page numbers
    text = re.sub(
        r"(?m)^\s*\d{1,3}\s*$",
        "",
        text,
    )

    # Join words split across lines with hyphens
    # Example: "en-\ndow" -> "endow"
    text = re.sub(
        r"([A-Za-z])-\n([a-z])",
        r"\1\2",
        text,
    )

    # Remove spaces and tabs at the end of lines
    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text,
    )

    # Normalize repeated spaces while preserving tables
    lines = []

    for line in text.splitlines():
        if line.strip().startswith("|"):
            lines.append(line)
        else:
            line = re.sub(
                r"[ \t]{2,}",
                " ",
                line,
            )
            lines.append(line)

    text = "\n".join(lines)

    # Reduce excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()