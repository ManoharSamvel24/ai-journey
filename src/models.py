from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Document(BaseModel):
    doc_id: str = Field(min_length=1, max_length=50)
    text: str = Field(min_length=1)
    tags: list[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))