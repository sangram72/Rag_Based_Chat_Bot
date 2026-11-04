from app.ingestion.loader import load_document
from app.ingestion.chunker import split_documents


file_path = "uploaded_documents/company_policy.txt"

documents = load_document(file_path)

chunks = split_documents(documents)

print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks):

    print(f"\nChunk {index + 1}")
    print(chunk.page_content)

    print("Metadata:", chunk.metadata)