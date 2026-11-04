from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

def load_document(file_path):

    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)

    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)

    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")

    else:
        raise ValueError("Unsupported file format")

    return loader.load()