from app.ingestion.loader import load_document
from app.ingestion.chunker import split_documents

from app.ingestion.embeddings import embedding_model


file_path = "uploaded_documents/company_policy.txt"

documents = load_document(file_path)

chunks = split_documents(documents)

texts = [
    chunk.page_content
    for chunk in chunks
]

embeddings = embedding_model.embed_documents(texts)

print("Total chunks:", len(chunks))

print("Total embeddings:", len(embeddings))

print("Vector dimensions:", len(embeddings[0]))

print("First embedding:", embeddings[0][:10])