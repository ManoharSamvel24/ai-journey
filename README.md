# AI Document Assistant (ai-journey)

An end-to-end AI application that allows users to upload documents, chunk them, and ask questions based on the document's content using Retrieval-Augmented Generation (RAG).

## ✨ Features

- **Document Ingestion:** Splits large text into overlapping chunks and generates embeddings.
- **Semantic Search:** Uses Cosine Similarity to find the most relevant context for a user's question.
- **Strict AI Grounding:** The AI answers _only_ from the provided context. If the answer isn't in the document, it strictly refuses with "I don't know".
- **Source Citations:** Returns the exact text chunks used to generate the answer so the user can verify it.
- **Structured Output:** Extracts clean JSON data from unstructured text using Pydantic validation.
- **Interactive UI:** Includes a Streamlit chat interface for a clean user experience.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** SQLite
- **AI Integration:** Google Gemini (Interactions API, Embeddings)
- **Frontend:** Streamlit
- **DevOps:** Docker, Git, Pytest

## 🏗️ Architecture Flow

1. User uploads a document via the API or Streamlit UI.
2. The backend splits the text into overlapping chunks (`src/rag.py`).
3. Chunks are embedded via Gemini and stored in SQLite (`src/db.py`).
4. User asks a question. The question is embedded and compared against chunk embeddings using Cosine Similarity.
5. The top 3 matching chunks are sent to Gemini as context to generate the final answer.

## 🚀 How to Run Locally

**1. Clone the repo and install dependencies:**

```bash
git clone https://github.com/ManoharSamvel24/ai-journey.git
cd ai-journey
pip install -r requirements.txt
```
