"""
Clipboard Tools: Read and copy text to the Windows system clipboard.
"""
import sys
from pathlib import Path
import pyperclip
from langchain_core.tools import tool

try:
    from src.wpa.utils.logger import log
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    from src.wpa.utils.logger import log


@tool
def get_clipboard_content() -> str:
    """Read and return the current plain text stored in the Windows clipboard."""
    try:
        content = pyperclip.paste()
        if not content:
            log("Tool executed: get_clipboard_content -> empty")
            return "The clipboard is currently empty."
        preview = content[:300]
        if len(content) > 300:
            preview += f"... [truncated {len(content) - 300} characters]"
        log(f"Tool executed: get_clipboard_content -> {len(content)} chars read")
        return f"Clipboard content: {preview}"
    except Exception as e:
        log(f"Tool failed: get_clipboard_content - {str(e)}")
        return f"Error reading clipboard: {str(e)}"


@tool
def set_clipboard_content(text: str) -> str:
    """Copy given text into the Windows clipboard."""
    try:
        pyperclip.copy(text)
        preview = text[:50] + ("..." if len(text) > 50 else "")
        log(f"Tool executed: set_clipboard_content -> '{preview}'")
        return "Copied text to clipboard."
    except Exception as e:
        log(f"Tool failed: set_clipboard_content - {str(e)}")
        return f"Error copying to clipboard: {str(e)}"
