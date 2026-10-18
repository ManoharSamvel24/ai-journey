import sqlite3


def docs_with_request_counts(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT d.doc_id,
               d.text,
               COUNT(r.id) AS request_count
        FROM documents d
        LEFT JOIN requests r ON r.doc_id = d.doc_id
        GROUP BY d.doc_id
        ORDER BY request_count DESC
    """).fetchall()
    return [
        {"doc_id": r[0], "text": r[1], "request_count": r[2]}
        for r in rows
    ]


def most_expensive_documents(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute("""
        SELECT d.doc_id,
               COALESCE(SUM(r.prompt_tokens + r.output_tokens), 0) AS total_tokens
        FROM documents d
        LEFT JOIN requests r ON r.doc_id = d.doc_id
        GROUP BY d.doc_id
        ORDER BY total_tokens DESC
    """).fetchall()
    return [{"doc_id": r[0], "total_tokens": r[1]} for r in rows]