
from langchain_chroma import Chroma

from app.ingestion.embeddings import embedding_model


vector_store = Chroma(
    collection_name="company_documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


def save_documents(chunks, filename, document_id, document_type, person=None):

    for chunk in chunks:
        chunk.metadata["filename"] = filename
        chunk.metadata["document_id"] = document_id
        chunk.metadata["document_type"] = document_type
        chunk.metadata["person"] = person or ""

    # Replace existing chunks belonging to this document.
    vector_store.delete(
        where={"document_id": document_id}
    )

    vector_store.add_documents(chunks)


def get_uploaded_documents(document_type=None):

    search_filter = None

    if document_type:
        search_filter = {
            "document_type": document_type
        }

    result = vector_store.get(
        where=search_filter,
        include=["metadatas"]
    )

    return result.get("metadatas", [])


def search_documents(question, document_type=None, document_id=None, k=4):

    search_filter = None

    if document_id:
        search_filter = {
            "document_id": document_id
        }

    elif document_type:
        search_filter = {
            "document_type": document_type
        }

    return vector_store.similarity_search_with_score(
        question,
        k=k,
        filter=search_filter
    )
