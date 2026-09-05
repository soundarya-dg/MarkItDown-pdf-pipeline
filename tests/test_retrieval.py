from src.retriever import find_relevant_chunks


def test_retrieves_benchmark_section():
    text = """
# Model Overview
The model is designed for reasoning, coding, and multilingual tasks.

# Architecture
The model uses a Mixture-of-Experts architecture with a subset
of parameters activated for each token.

# Evaluation
The model is evaluated on benchmarks including AIME,
LiveCodeBench, GPQA, and CodeForces.

# Training
The training process combines large-scale pretraining
with post-training for reasoning and instruction following.
"""

    chunks = find_relevant_chunks(
        text,
        "Which benchmarks are used for evaluation?",
        max_chunks=2,
    )

    assert chunks
    assert any(
        "AIME" in chunk
        and "LiveCodeBench" in chunk
        for chunk in chunks
    )


def test_returns_no_chunks_for_unrelated_question():
    text = """
The document describes model architecture, training methods and benchmark evaluation.
"""

    chunks = find_relevant_chunks(
        text,
        "What hardware was used for deployment?",
    )

    assert chunks == []
