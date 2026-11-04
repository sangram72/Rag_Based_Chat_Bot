import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

connection = sqlite3.connect(
    "chat_history.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(connection)

checkpointer.setup()