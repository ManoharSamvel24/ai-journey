import sqlite3


def init_db(path: str) -> None:
    with sqlite3.connect(path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                doc_id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL,
                output_tokens INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
            )
        """)


def insert_document(conn: sqlite3.Connection, doc_id: str, text: str) -> None:
    conn.execute(
        "INSERT INTO documents (doc_id, text) VALUES (?, ?)",
        (doc_id, text),
    )


def get_document(conn: sqlite3.Connection, doc_id: str) -> dict | None:
    row = conn.execute(
        "SELECT doc_id, text, created_at FROM documents WHERE doc_id = ?",
        (doc_id,),
    ).fetchone()
    if row is None:
        return None
    return {"doc_id": row[0], "text": row[1], "created_at": row[2]}


def list_documents(conn: sqlite3.Connection) -> list[dict]:
    rows = conn.execute(
        "SELECT doc_id, text, created_at FROM documents ORDER BY created_at DESC"
    ).fetchall()
    return [{"doc_id": r[0], "text": r[1], "created_at": r[2]} for r in rows]


def log_request(
    conn: sqlite3.Connection,
    doc_id: str | None,
    prompt: str,
    response: str,
    prompt_tokens: int,
    output_tokens: int,
) -> None:
    conn.execute(
        """INSERT INTO requests
           (doc_id, prompt, response, prompt_tokens, output_tokens)
           VALUES (?, ?, ?, ?, ?)""",
        (doc_id, prompt, response, prompt_tokens, output_tokens),
    )


def total_tokens(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        """SELECT COALESCE(SUM(prompt_tokens), 0),
                  COALESCE(SUM(output_tokens), 0)
           FROM requests"""
    ).fetchone()
    return {"prompt_tokens": row[0], "output_tokens": row[1]}