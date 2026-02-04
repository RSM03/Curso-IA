import os
import json
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

PDF_DIR = "BOE"
STORE_DIR = "rag_store"
os.makedirs(STORE_DIR, exist_ok=True)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def chunk_text(text, size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

documents = []
metadatas = []

for pdf_file in os.listdir(PDF_DIR):
    if not pdf_file.lower().endswith(".pdf"):
        continue

    reader = PdfReader(os.path.join(PDF_DIR, pdf_file))

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text or len(text.strip()) < 50:
            continue

        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "source": pdf_file,
                "page": page_num + 1,
                "chunk_id": i
            })

print(f"Total chunks generados: {len(documents)}")

# Embeddings
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = embedder.encode(documents, convert_to_numpy=True, show_progress_bar=True)

# Índice FAISS
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

faiss.write_index(index, os.path.join(STORE_DIR, "index.faiss"))

# Guardar textos y metadatos
with open(os.path.join(STORE_DIR, "chunks.json"), "w", encoding="utf-8") as f:
    json.dump(
        [{"text": d, "meta": m} for d, m in zip(documents, metadatas)],
        f,
        ensure_ascii=False,
        indent=2
    )

print("Ingesta completada correctamente.")