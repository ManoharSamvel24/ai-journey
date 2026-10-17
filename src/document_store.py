import json
import logging
import os

logger = logging.getLogger(__name__)


class DocumentNotFound(Exception):
    pass


class DocumentStore:
    def __init__(self, path: str) -> None:
        self.path = path
        self.data: dict[str, str] = {}

    def __enter__(self) -> "DocumentStore":
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.data = json.load(f)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        with open(self.path, "w") as f:
            json.dump(self.data, f)

    def add(self, doc_id: str, text: str) -> None:
        self.data[doc_id] = text
        logger.info("Added %s", doc_id)

    def get(self, doc_id: str) -> str:
        self._ensure_exists(doc_id)
        return self.data[doc_id]

    def list_all(self) -> list[str]:
        return list(self.data.keys())

    def delete(self, doc_id: str) -> None:
        self._ensure_exists(doc_id)
        del self.data[doc_id]
        logger.info("Deleted %s", doc_id)

    def _ensure_exists(self, doc_id: str) -> None:
        if doc_id not in self.data:
            raise DocumentNotFound(doc_id)