from typing import TypedDict, List, Any
from langgraph.graph import MessagesState


class ChatState(MessagesState):
    question: str
    documents: List[Any]
    answer: str
    citations: List[dict]
    is_valid: bool