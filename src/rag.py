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