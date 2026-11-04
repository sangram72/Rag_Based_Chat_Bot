
from langgraph.graph import StateGraph, START, END

from app.graph.state import ChatState
from app.database.chat_history import checkpointer

from app.graph.nodes import (
    retrieve_node,
    check_retrieval_node,
    generate_node,
    validate_node
)


# Decide what happens after citation validation
def validation_router(state):
    if state["is_valid"]:
        return END

    return "generate"


# Create the LangGraph workflow
def create_workflow():

    graph = StateGraph(ChatState)

    # Register nodes
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("check_retrieval", check_retrieval_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)

    # Step 1: Start retrieval
    graph.add_edge(START, "retrieve")

    # Step 2: Check retrieved documents
    graph.add_edge("retrieve", "check_retrieval")

    # Step 3: Decide whether to generate an answer
    graph.add_conditional_edges(
        "check_retrieval",
        lambda state: (
            END if not state["documents"] else "generate"
        ),
        {
            END: END,
            "generate": "generate"
        }
    )

    # Step 4: Generate answer
    graph.add_edge("generate", "validate")

    # Step 5: Validate citations
    graph.add_conditional_edges(
        "validate",
        validation_router,
        {
            END: END,
            "generate": "generate"
        }
    )

    # Compile with SQLite checkpointing
    return graph.compile(checkpointer=checkpointer)
