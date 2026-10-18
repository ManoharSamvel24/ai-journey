import pytest
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