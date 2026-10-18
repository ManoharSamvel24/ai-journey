import sqlite3
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from src.gemini_client import summarize
from src.db import init_db, log_request
from src.rag import ingest_document, ask_question
from src.db import insert_document

app = FastAPI(title="AI Journey API")
DB_PATH = "app.db"

# 1. Initialize the database when the app starts
@app.on_event("startup")
def startup():
    init_db(DB_PATH)

# 2. Dependency: yields a database connection and closes it automatically
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

class SummarizeRequest(BaseModel):
    doc_id: str | None = None
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    char_count: int

class DocumentUpload(BaseModel):
    doc_id: str
    text: str

class AskRequest(BaseModel):
    doc_id: str
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: list[str]

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(req: SummarizeRequest, db: sqlite3.Connection = Depends(get_db)):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        summary = summarize(req.text)
    except Exception as e:
        raise HTTPException(status_code=502, detail="AI service failed to respond")
        
    # 3. Save the request to the database!
    log_request(db, req.doc_id, req.text, summary, 0, 0)
    db.commit()
        
    return SummarizeResponse(summary=summary, char_count=len(req.text))

# Add this near your other Pydantic models
class ExtractRequest(BaseModel):
    text: str

class ExtractResponse(BaseModel):
    name: str | None
    age: int | None
    city: str | None


# Add this endpoint
@app.post("/extract", response_model=ExtractResponse)
def extract_endpoint(req: ExtractRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        data = extract_info(req.text)
        # Pydantic validates the AI's output here!
        return ExtractResponse(**data) 
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.post("/documents/upload")
def upload_document(req: DocumentUpload, db: sqlite3.Connection = Depends(get_db)):
    insert_document(db, req.doc_id, req.text)
    ingest_document(db, req.doc_id, req.text)
    return {"status": "success", "message": f"Document {req.doc_id} chunked and embedded."}

@app.post("/documents/ask", response_model=AskResponse)
def ask(req: AskRequest, db: sqlite3.Connection = Depends(get_db)):
    result = ask_question(db, req.doc_id, req.question)
    return AskResponse(answer=result["answer"], sources=result["sources"])