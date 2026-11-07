
from langgraph.graph import StateGraph, START, END

from app.graph.state import ChatState
from app.database.chat_history import checkpointer

from app.graph.nodes import (
    retrieve_node,
    check_retrieval_node,
    generate_node,
    validate_node
)


MAX_GENERATION_ATTEMPTS = 2


def validation_router(state):

    # Stop when citations are valid.
    if state.get("is_valid", False):
        return END

    # Prevent endless regeneration.
    if state.get("generation_attempts", 0) >= MAX_GENERATION_ATTEMPTS:
        return END

    # Retry once if citations are invalid.
    return "generate"


def create_workflow():

    graph = StateGraph(ChatState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("check_retrieval", check_retrieval_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)

    graph.add_edge(START, "retrieve")

    graph.add_edge("retrieve", "check_retrieval")

    graph.add_conditional_edges(
        "check_retrieval",
        lambda state: (
            END if not state.get("documents") else "generate"
        ),
        {
            END: END,
            "generate": "generate"
        }
    )

    graph.add_edge("generate", "validate")

    graph.add_conditional_edges(
        "validate",
        validation_router,
        {
            END: END,
            "generate": "generate"
        }
    )

    return graph.compile(
        checkpointer=checkpointer
    )
