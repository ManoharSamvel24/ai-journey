from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.gemini_client import summarize

app = FastAPI(title="AI Journey API")


class SummarizeRequest(BaseModel):
    text: str


class SummarizeResponse(BaseModel):
    summary: str
    char_count: int


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(req: SummarizeRequest) -> SummarizeResponse:
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        summary = summarize(req.text)
    except Exception as e:
        # If Gemini fails (timeout, rate limit, etc.), return a clean 502, not a crash
        raise HTTPException(status_code=502, detail="AI service failed to respond")
        
    return SummarizeResponse(summary=summary, char_count=len(req.text))