FROM python:3.13-slim

WORKDIR /app

# Copy requirements first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY src/ ./src/

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]