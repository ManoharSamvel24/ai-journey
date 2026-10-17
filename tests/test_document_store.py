import pytest

from src.document_store import DocumentStore, DocumentNotFound


def test_add_and_get(tmp_path):
    path = tmp_path / "docs.json"
    with DocumentStore(str(path)) as store:
        store.add("d1", "hello")
        assert store.get("d1") == "hello"


def test_get_missing_raises(tmp_path):
    path = tmp_path / "docs.json"
    with DocumentStore(str(path)) as store:
        with pytest.raises(DocumentNotFound):
            store.get("nope")


def test_delete(tmp_path):
    path = tmp_path / "docs.json"
    with DocumentStore(str(path)) as store:
        store.add("d1", "hello")
        store.delete("d1")
        with pytest.raises(DocumentNotFound):
            store.get("d1")


def test_persists_across_contexts(tmp_path):
    path = tmp_path / "docs.json"
    with DocumentStore(str(path)) as store:
        store.add("d1", "hello")

    with DocumentStore(str(path)) as store:
        assert store.get("d1") == "hello"