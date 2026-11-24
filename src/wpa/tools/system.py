"""
System Tools: Master volume control, battery monitoring, system metrics, workstation locking.
"""
import ctypes
import sys
from pathlib import Path
import psutil
from langchain_core.tools import tool
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

try:
    from src.wpa.utils.logger import log
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[3]))
    from src.wpa.utils.logger import log


@tool
def set_volume(level: int) -> str:
    """Set the Windows master volume. Level must be an integer between 0 and 100."""
    try:
        level = max(0, min(100, int(level)))
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        log(f"Tool executed: set_volume({level}%)")
        return f"Volume set to {level} percent."
    except Exception as e:
        log(f"Tool failed: set_volume({level}%) - {str(e)}")
        return f"Error setting volume: {str(e)}"


@tool
def get_volume() -> str:
    """Get the current Windows master volume level and mute status."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        current_scalar = volume.GetMasterVolumeLevelScalar()
        percent = int(round(current_scalar * 100))
        is_muted = volume.GetMute()
        mute_status = "muted" if is_muted else "unmuted"
        log(f"Tool executed: get_volume -> {percent}% ({mute_status})")
        return f"Current volume is {percent} percent ({mute_status})."
    except Exception as e:
        log(f"Tool failed: get_volume - {str(e)}")
        return f"Error reading volume: {str(e)}"


@tool
def get_battery_status() -> str:
    """Check the laptop battery percentage and whether the charger is connected."""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            log("Tool executed: get_battery_status -> No battery detected")
            return "No battery detected on this system."
        percent = int(battery.percent)
        status = "plugged in and charging" if battery.power_plugged else "discharging on battery"
        time_left = ""
        if not battery.power_plugged and battery.secsleft > 0 and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
            hours = battery.secsleft // 3600
            mins = (battery.secsleft % 3600) // 60
            time_left = f", approximately {hours}h {mins}m remaining"
        log(f"Tool executed: get_battery_status -> {percent}% ({status})")
        return f"Battery is at {percent} percent ({status}{time_left})."
    except Exception as e:
        log(f"Tool failed: get_battery_status - {str(e)}")
        return f"Error checking battery: {str(e)}"


@tool
def get_system_stats() -> str:
    """Get current CPU utilization and RAM memory usage."""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()
        used_gb = round((memory.total - memory.available) / (1024 ** 3), 1)
        total_gb = round(memory.total / (1024 ** 3), 1)
        log(f"Tool executed: get_system_stats -> CPU {cpu}%, RAM {memory.percent}%")
        return f"CPU usage is at {cpu} percent. Memory usage is {memory.percent} percent ({used_gb} GB used of {total_gb} GB)."
    except Exception as e:
        log(f"Tool failed: get_system_stats - {str(e)}")
        return f"Error reading system metrics: {str(e)}"


@tool
def lock_workstation() -> str:
    """Lock the Windows desktop session immediately for security."""
    try:
        ctypes.windll.user32.LockWorkStation()
        log("Tool executed: lock_workstation")
        return "Workstation locked successfully."
    except Exception as e:
        log(f"Tool failed: lock_workstation - {str(e)}")
        return f"Error locking workstation: {str(e)}"


# ---------------------------------------------------------
# Test Case Execution
# ---------------------------------------------------------
def test_battery_percentage():
    """Unit test to verify that get_battery_status executes and returns valid information."""
    print("\n--- Running Test: Battery Percentage Check ---")
    result = get_battery_status.invoke({})
    print(f"Tool Result: {result}")

    # Assertions
    assert isinstance(result, str), "Expected string output from battery tool"
    assert len(result) > 0, "Tool returned an empty string"
    assert "percent" in result or "No battery" in result, "Output should contain battery percentage or status"
    print("Test Passed: Battery percentage check verified successfully!\n")


if __name__ == "__main__":
    test_battery_percentage()
