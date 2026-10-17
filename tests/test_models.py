import pytest
from pydantic import ValidationError

from src.models import Document


def test_valid_document():
    doc = Document(doc_id="d1", text="hello")
    assert doc.doc_id == "d1"
    assert doc.text == "hello"
    assert doc.tags == []


def test_empty_doc_id_raises():
    with pytest.raises(ValidationError):
        Document(doc_id="", text="hello")


def test_created_at_autopopulates():
    doc = Document(doc_id="d1", text="hello")
    assert doc.created_at is not None