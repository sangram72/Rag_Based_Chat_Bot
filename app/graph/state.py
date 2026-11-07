from typing import TypedDict, List, Any
from langgraph.graph import MessagesState






class ChatState(MessagesState):
    question: str
    documents: list
    answer: str
    citations: list
    is_valid: bool
    generation_attempts: int


   