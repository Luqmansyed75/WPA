"""
Session-based Logger Utility for WPA.
Creates a separate, dedicated log file for each run session.
Format: [YYYY-MM-DD HH:MM:SS] <text>
"""
from datetime import datetime
from pathlib import Path

# Resolve logs directory at the project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOGS_DIR = PROJECT_ROOT / "logs"

# Timestamp generated once at the start of each run/process
_SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
_CURRENT_LOG_FILE = LOGS_DIR / f"run_{_SESSION_ID}.log"


def start_new_session() -> Path:
    """Explicitly starts a new logging session file for the current process."""
    global _SESSION_ID, _CURRENT_LOG_FILE
    _SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
    _CURRENT_LOG_FILE = LOGS_DIR / f"run_{_SESSION_ID}.log"
    return _CURRENT_LOG_FILE


def get_current_log_file() -> Path:
    """Returns the path to the current run's log file."""
    return _CURRENT_LOG_FILE


def log(text: str) -> str:
    """
    Stores only the current time and the mentioned text into this run's separate log file.

    Format:
        [YYYY-MM-DD HH:MM:SS] <text>
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {text}\n"

    with open(_CURRENT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    return entry.strip()


if __name__ == "__main__":
    saved_entry = log("Testing separate run logging.")
    print(f"Recorded entry: {saved_entry}")
    print(f"Created run log file: {_CURRENT_LOG_FILE}")
