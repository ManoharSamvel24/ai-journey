import pytest
from src.rag import cosine_similarity
from src.rag import chunk_text

def test_chunk_text_basic():
    text = "abcdefghij" # 10 chars
    # chunk_size 5, overlap 2
    # chunk 1: abcde (0 to 5)
    # chunk 2: defgh (3 to 8)
    # chunk 3: ghij  (6 to 10)
    chunks = chunk_text(text, chunk_size=5, overlap=2)
    assert chunks == ["abcde", "defgh", "ghij"]

def test_chunk_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("hello", chunk_size=5, overlap=5)

def test_cosine_similarity_identical():
    vec1 = [1.0, 2.0, 3.0]
    vec2 = [1.0, 2.0, 3.0]
    assert cosine_similarity(vec1, vec2) == pytest.approx(1.0)

def test_cosine_similarity_orthogonal():
    vec1 = [1.0, 0.0]
    vec2 = [0.0, 1.0]
    assert cosine_similarity(vec1, vec2) == pytest.approx(0.0)

def test_cosine_similarity_zero_vector():
    assert cosine_similarity([0.0, 0.0], [1.0, 2.0]) == 0.0