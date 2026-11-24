"""
Application & Browser Tools: Launch desktop apps, close processes, and open websites.
"""
import os
import sys
from pathlib import Path
import subprocess
import webbrowser
import psutil
from langchain_core.tools import tool

try:
    from src.wpa.utils.logger import log
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    from src.wpa.utils.logger import log

# Common application aliases to executable commands
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "task manager": "taskmgr.exe",
    "taskmgr": "taskmgr.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "settings": "start ms-settings:",
    "terminal": "wt.exe",
    "cmd": "cmd.exe",
    "powershell": "powershell.exe",
    "chrome": "start chrome",
    "edge": "start msedge",
    "vs code": "code",
    "vscode": "code",
    "spotify": "start spotify:",
}

WEBSITE_SHORTCUTS = {
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "reddit": "https://www.reddit.com",
    "stackoverflow": "https://stackoverflow.com",
}


@tool
def open_application(app_name: str) -> str:
    """Launch a Windows desktop application by name (e.g. 'notepad', 'calculator', 'chrome', 'settings', 'task manager')."""
    clean_name = app_name.strip().lower()
    cmd = APP_COMMANDS.get(clean_name, clean_name)
    try:
        subprocess.Popen(cmd, shell=True)
        log(f"Tool executed: open_application('{app_name}')")
        return f"Launched {app_name}."
    except Exception as e:
        log(f"Tool failed: open_application('{app_name}') - {str(e)}")
        return f"Failed to open {app_name}: {str(e)}"


@tool
def close_application(app_name: str) -> str:
    """Close a running Windows application by process or executable name (e.g., 'notepad', 'calc', 'chrome')."""
    clean_name = app_name.strip().lower()
    terminated_count = 0
    try:
        for proc in psutil.process_iter(['name', 'exe']):
            p_name = (proc.info['name'] or '').lower()
            if clean_name in p_name:
                proc.terminate()
                terminated_count += 1
        if terminated_count > 0:
            log(f"Tool executed: close_application('{app_name}') -> closed {terminated_count} instance(s)")
            return f"Closed {terminated_count} instance(s) of {app_name}."
        log(f"Tool executed: close_application('{app_name}') -> no running process found")
        return f"No running process found matching '{app_name}'."
    except Exception as e:
        log(f"Tool failed: close_application('{app_name}') - {str(e)}")
        return f"Error closing {app_name}: {str(e)}"


@tool
def open_website(target: str) -> str:
    """Open a website or web application in the default browser. Accepts names like 'youtube', 'github', or direct URLs."""
    clean_target = target.strip().lower()
    url = WEBSITE_SHORTCUTS.get(clean_target, target.strip())
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"https://{url}"
    try:
        webbrowser.open(url)
        log(f"Tool executed: open_website('{clean_target}') -> {url}")
        return f"Opened {clean_target} in browser."
    except Exception as e:
        log(f"Tool failed: open_website('{clean_target}') - {str(e)}")
        return f"Failed to open {target}: {str(e)}"


# ---------------------------------------------------------
# Test Case Execution
# ---------------------------------------------------------
def test_open_notepad():
    """Unit test to verify that open_application launches Notepad."""
    import time
    print("\n--- Running Test: Open Notepad Application ---")
    result = open_application.invoke({"app_name": "notepad"})
    print(f"Tool Result: {result}")

    # Assertions
    assert isinstance(result, str), "Expected string output from open_application"
    assert "notepad" in result.lower(), "Expected launch confirmation message"

    # Give Windows a moment to spawn the process and verify
    time.sleep(1.0)
    notepad_running = any("notepad" in (p.info["name"] or "").lower() for p in psutil.process_iter(["name"]))
    assert notepad_running, "Notepad process should be actively running in Windows"
    print("Process Check: Notepad process confirmed running in Windows task list!")
    print("Test Passed: Notepad launched successfully!\n")


if __name__ == "__main__":
    test_open_notepad()

