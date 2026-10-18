import math
import json
import sqlite3
from src.gemini_client import get_embeddings, _client, MODEL

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
        
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        
        # If this chunk reached the end of the text, stop looping
        if end >= len(text):
            break
            
        start += chunk_size - overlap
        
    return chunks


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot_product = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def ingest_document(conn: sqlite3.Connection, doc_id: str, text: str) -> None:
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    
    for chunk, emb in zip(chunks, embeddings):
        conn.execute(
            "INSERT INTO chunks (doc_id, text, embedding) VALUES (?, ?, ?)",
            (doc_id, chunk, json.dumps(emb))
        )
    conn.commit()

def ask_question(conn: sqlite3.Connection, doc_id: str, question: str) -> dict:
    # 1. Embed the question
    q_emb = get_embeddings([question])[0]
    
    # 2. Fetch all chunks for this document
    rows = conn.execute("SELECT text, embedding FROM chunks WHERE doc_id = ?", (doc_id,)).fetchall()
    if not rows:
        return {"answer": "I don't know", "sources": []}
        
    # 3. Calculate similarity
    scored_chunks = []
    for text, emb_json in rows:
        emb = json.loads(emb_json)
        score = cosine_similarity(q_emb, emb)
        scored_chunks.append((score, text))
        
    # 4. Get top 3 matching chunks
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [text for score, text in scored_chunks[:3]]
    
    # 5. Build prompt and ask AI
    context = "\n\n---\n\n".join(top_chunks)
    prompt = f"""
    Answer the question based ONLY on the following context.
    If the answer is not in the context, you MUST say exactly "I don't know".
    
    Context:
    {context}
    
    Question: {question}
    """
    
    interaction = _client.interactions.create(model=MODEL, input=prompt)
    
    return {
        "answer": interaction.output_text,
        "sources": top_chunks
    }