import fitz  # PyMuPDF for PDFs
import os
import json
def extract_text_from_file(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return "\n".join(page.get_text() for page in doc)
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file type")

def chunk_text(text: str, chunk_size=500) -> list:
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]
def save_chunks_to_json(chunks: list, filename: str, output_dir="src/data/chunks"):
    os.makedirs(output_dir, exist_ok=True)
    base_filename = os.path.splitext(filename)[0]
    output_path = os.path.join(output_dir, f"{base_filename}_chunks.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    return output_path
