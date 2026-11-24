"""
File Operation Tools: Safely inspect directories, read text files, and delete files with confirmation checks.
"""
import os
import sys
from pathlib import Path
from langchain_core.tools import tool

try:
    from src.wpa.utils.logger import log
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    from src.wpa.utils.logger import log


@tool
def list_directory_files(directory_path: str = ".") -> str:
    """List the names of files and folders inside a given directory path."""
    try:
        target = Path(directory_path).resolve()
        if not target.exists():
            log(f"Tool executed: list_directory_files('{directory_path}') -> not found")
            return f"Directory '{directory_path}' does not exist."
        if not target.is_dir():
            log(f"Tool executed: list_directory_files('{directory_path}') -> not a directory")
            return f"Path '{directory_path}' is not a directory."

        entries = list(target.iterdir())
        if not entries:
            log(f"Tool executed: list_directory_files('{directory_path}') -> empty")
            return f"Directory '{target.name}' is empty."

        folders = [f"[DIR] {e.name}" for e in entries if e.is_dir()]
        files = [e.name for e in entries if e.is_file()]
        summary = folders[:10] + files[:20]
        output = ", ".join(summary)
        if len(entries) > 30:
            output += f" (and {len(entries) - 30} more items)"
        log(f"Tool executed: list_directory_files('{directory_path}') -> {len(entries)} items")
        return f"Contents of {target.name}: {output}"
    except Exception as e:
        log(f"Tool failed: list_directory_files('{directory_path}') - {str(e)}")
        return f"Error listing directory: {str(e)}"


@tool
def read_text_file(file_path: str, max_lines: int = 15) -> str:
    """Read the first few lines of a plain text or code file."""
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            log(f"Tool executed: read_text_file('{file_path}') -> not found")
            return f"File '{file_path}' does not exist."
        if not path.is_file():
            log(f"Tool executed: read_text_file('{file_path}') -> not a file")
            return f"Path '{file_path}' is a directory, not a file."

        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = [f.readline() for _ in range(max_lines)]

        content = "".join(lines).strip()
        if not content:
            log(f"Tool executed: read_text_file('{file_path}') -> empty file")
            return f"File '{path.name}' is empty."
        log(f"Tool executed: read_text_file('{file_path}') -> {len(lines)} lines read")
        return f"File content of {path.name}:\n{content}"
    except Exception as e:
        log(f"Tool failed: read_text_file('{file_path}') - {str(e)}")
        return f"Error reading file: {str(e)}"


@tool
def delete_file(file_path: str, confirmed: bool = False) -> str:
    """Safely delete a file. Requires confirmed=True to execute, otherwise warns and requests confirmation."""
    try:
        path = Path(file_path).resolve()
        if not path.exists():
            log(f"Tool executed: delete_file('{file_path}') -> not found")
            return f"File '{file_path}' does not exist."

        if not confirmed:
            log(f"Tool warning: delete_file('{file_path}') -> confirmation requested")
            return f"Safety Warning: Are you sure you want to delete '{path.name}'? Please confirm with 'yes'."

        if path.is_file():
            os.remove(path)
            log(f"Tool executed: delete_file('{file_path}') -> deleted successfully")
            return f"File '{path.name}' was deleted."
        elif path.is_dir():
            log(f"Tool refused: delete_file('{file_path}') -> refusal: path is directory")
            return f"Path '{path.name}' is a directory. Refusing to delete directories for safety."
        return "Unknown file type."
    except Exception as e:
        log(f"Tool failed: delete_file('{file_path}') - {str(e)}")
        return f"Error deleting file: {str(e)}"
