"""
Agent Tools Registry & LangGraph ToolNode binding.
"""
from langgraph.prebuilt import ToolNode
from src.wpa.tools import ALL_TOOLS, TOOLS_BY_NAME

# Prebuilt LangGraph ToolNode for automatic execution in graphs
tool_node = ToolNode(tools=ALL_TOOLS)

__all__ = ["ALL_TOOLS", "TOOLS_BY_NAME", "tool_node"]
