"""
Agent State Schema for LangGraph.
"""
from typing import Annotated, Optional, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State passed between nodes in the WPA LangGraph agent."""

    # Raw voice/user query
    query: str

    # Message history with automatic appending reducer
    messages: Annotated[list[BaseMessage], add_messages]

    # Classified intent (e.g. 'tool', 'general_chat', 'unknown')
    intent: Optional[str]

    # Raw execution result from a tool
    tool_output: Optional[str]

    # Final response to be returned or spoken by pyttsx3
    response: Optional[str]
