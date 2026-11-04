from langchain_chroma import Chroma

from app.ingestion.embeddings import embedding_model


vector_store = Chroma(
    collection_name="company_documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


def save_documents(chunks):

    vector_store.add_documents(chunks)


def search_documents(question):

    results = vector_store.similarity_search_with_score(
        question,
        k=4
    )

    return results