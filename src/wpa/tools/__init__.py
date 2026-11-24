"""
Tools Package for Windows Productivity Agent (WPA).
Exports all LangChain @tool objects into a centralized registry.
"""
from .system import (
    set_volume,
    get_volume,
    get_battery_status,
    get_system_stats,
    lock_workstation,
)
from .app_launcher import (
    open_application,
    close_application,
    open_website,
)
from .clipboard import (
    get_clipboard_content,
    set_clipboard_content,
)
from .files import (
    list_directory_files,
    read_text_file,
    delete_file,
)

# Complete registry of offline system tools
ALL_TOOLS = [
    # System & Audio
    set_volume,
    get_volume,
    get_battery_status,
    get_system_stats,
    lock_workstation,
    # Apps & Websites
    open_application,
    close_application,
    open_website,
    # Clipboard
    get_clipboard_content,
    set_clipboard_content,
    # Files
    list_directory_files,
    read_text_file,
    delete_file,
]

# Fast name-based lookup dictionary
TOOLS_BY_NAME = {t.name: t for t in ALL_TOOLS}

__all__ = [
    "ALL_TOOLS",
    "TOOLS_BY_NAME",
    "set_volume",
    "get_volume",
    "get_battery_status",
    "get_system_stats",
    "lock_workstation",
    "open_application",
    "close_application",
    "open_website",
    "get_clipboard_content",
    "set_clipboard_content",
    "list_directory_files",
    "read_text_file",
    "delete_file",
]
