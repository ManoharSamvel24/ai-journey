import sqlite3

import pytest

from src.db import (
    get_document,
    init_db,
    insert_document,
    list_documents,
    log_request,
    total_tokens,
)


@pytest.fixture
def conn(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    c = sqlite3.connect(db_path)
    yield c
    c.close()


def test_insert_and_get(conn):
    insert_document(conn, "d1", "hello")
    doc = get_document(conn, "d1")
    assert doc is not None
    assert doc["text"] == "hello"


def test_get_missing_returns_none(conn):
    assert get_document(conn, "nope") is None


def test_list_documents_order(conn):
    insert_document(conn, "d1", "a")
    insert_document(conn, "d2", "b")
    docs = list_documents(conn)
    assert len(docs) == 2


def test_log_request_and_sum(conn):
    insert_document(conn, "d1", "hello")
    log_request(conn, "d1", "p1", "r1", 10, 20)
    log_request(conn, "d1", "p2", "r2", 5, 8)
    totals = total_tokens(conn)
    assert totals["prompt_tokens"] == 15
    assert totals["output_tokens"] == 28