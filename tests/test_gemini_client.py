import pytest

from src.gemini_client import summarize, usage_info


@pytest.mark.integration
def test_summarize():
    result = summarize("Python is a programming language. It is used widely.")
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.integration
def test_usage_info():
    info = usage_info("Say hello")
    assert info["prompt_tokens"] > 0
    assert info["output_tokens"] > 0