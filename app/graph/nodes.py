from app.rag.retriever import retrieve_documents
from app.rag.generator import generate_answer
from app.rag.citations import (
    extract_citations,
    validate_citations
)
from langchain_core.messages import HumanMessage, AIMessage

def retrieve_node(state):
    documents = retrieve_documents(state["question"])

    return {
        "documents": documents
    }

def check_retrieval_node(state):
    if not state["documents"]:
        return {
            "answer": "I could not find sufficient information in the provided documents.",
            "citations": [],
            "is_valid": True
        }

    return {}





def generate_node(state):
    question = state["question"]
    documents = state["documents"]

    answer = generate_answer(
        question,
        documents,
        state.get("messages", [])
    )

    citations = extract_citations(documents)

    return {
        "answer": answer,
        "citations": citations,
        "messages": [
            HumanMessage(content=question),
            AIMessage(content=answer)
        ]
    }


def validate_node(state):

    is_valid = validate_citations(
        state["answer"],
        state["citations"]
    )

    return {
        "is_valid": is_valid
    }