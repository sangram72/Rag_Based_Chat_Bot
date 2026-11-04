
from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as documents_router

app = FastAPI(
    title="Local RAG Chatbot",
    description="RAG chatbot with document citations and chat history",
    version="1.0.0"
)

# Register chat API
app.include_router(chat_router, prefix="/api")

# Register document upload API
app.include_router(documents_router, prefix="/api")


@app.get("/")
def home():
    return {
        "message": "RAG Chatbot API is running!"
    }
