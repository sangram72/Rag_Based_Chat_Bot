
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.graph.workflow import create_workflow

router = APIRouter()

# Initialize the LangGraph workflow
workflow = create_workflow()


# Request structure
class ChatRequest(BaseModel):
    question: str
    conversation_id: str


# Chat endpoint
@router.post("/chat")
def chat(request: ChatRequest):

    try:
        # Use conversation ID as LangGraph thread ID
        config = {
            "configurable": {
                "thread_id": request.conversation_id
            }
        }

        # Execute the RAG workflow
        result = workflow.invoke(
            {
                "question": request.question
            },
            config=config
        )

        # Return answer and citations
        return {
            "conversation_id": request.conversation_id,
            "question": request.question,
            "answer": result["answer"],
            "citations": result["citations"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
