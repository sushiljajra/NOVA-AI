import time
import threading
import datetime
import winsound
import subprocess
from typing import List, Dict, Any

_ACTIVE_TIMERS: List[Dict[str, Any]] = []

def _trigger_alert(title: str, message: str):
    """Triggers an audio beep and Windows visual notification balloon."""
    try:
        # Audio alert
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
        # Windows balloon tip notification
        ps_cmd = f"""
Add-Type -AssemblyName System.Windows.Forms
$b = New-Object System.Windows.Forms.NotifyIcon
$b.Icon = [System.Drawing.SystemIcons]::Information
$b.BalloonTipTitle = "{title}"
$b.BalloonTipText = "{message}"
$b.Visible = $True
$b.ShowBalloonTip(10000)
Start-Sleep -Seconds 10
$b.Dispose()
"""
        subprocess.Popen(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], shell=False)
    except Exception:
        pass

def _timer_worker(seconds: float, label: str):
    time.sleep(seconds)
    _trigger_alert("ECLIPSE Alarm", f"Timer Complete: {label}")
    # Remove from active
    global _ACTIVE_TIMERS
    _ACTIVE_TIMERS = [t for t in _ACTIVE_TIMERS if t.get("label") != label]

def set_timer(minutes: float, label: str = "Timer") -> str:
    """
    Sets a countdown timer for a specified number of minutes. When time expires,
    triggers a Windows desktop notification and sound.
    Example: set_timer(minutes=5, label="Take a break")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("set_timer", {"minutes": minutes, "label": label})

    seconds = minutes * 60
    finish_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    finish_str = finish_time.strftime("%I:%M:%S %p")

    timer_record = {
        "label": label,
        "minutes": minutes,
        "finish_time": finish_str
    }
    _ACTIVE_TIMERS.append(timer_record)

    t = threading.Thread(target=_timer_worker, args=(seconds, label), daemon=True)
    t.start()

    res = f"Timer initialized for {minutes} minute(s) ('{label}'). Alert set for {finish_str}."
    print_tool_result(res)
    return res

def set_reminder(time_str: str, message: str) -> str:
    """
    Sets a reminder for a specific time of day (e.g., '14:30', '5:00 PM', or 'in 20 minutes').
    Triggers visual and audio alerts when due.
    Example: set_reminder(time_str="17:00", message="Submit project deliverables")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("set_reminder", {"time_str": time_str, "message": message})

    # Try parsing time
    now = datetime.datetime.now()
    target_dt = None

    time_str_clean = time_str.strip().lower()
    if "in " in time_str_clean and "min" in time_str_clean:
        try:
            mins = float("".join(c for c in time_str_clean if c.isdigit() or c == "."))
            return set_timer(minutes=mins, label=message)
        except Exception:
            pass

    formats = ["%H:%M", "%I:%M %p", "%I:%M%p", "%I %p"]
    for fmt in formats:
        try:
            parsed = datetime.datetime.strptime(time_str.strip(), fmt)
            target_dt = now.replace(hour=parsed.hour, minute=parsed.minute, second=0)
            if target_dt < now:
                # If time is in the past, assume next day
                target_dt += datetime.timedelta(days=1)
            break
        except ValueError:
            continue

    if not target_dt:
        res = f"Could not parse time '{time_str}'. Please specify as 'HH:MM' (24-hour) or 'I:MM AM/PM' (e.g. '5:30 PM')."
        print_tool_result(res)
        return res

    seconds_delay = (target_dt - now).total_seconds()
    minutes_delay = round(seconds_delay / 60, 1)

    timer_record = {
        "label": message,
        "minutes": minutes_delay,
        "finish_time": target_dt.strftime("%I:%M %p")
    }
    _ACTIVE_TIMERS.append(timer_record)

    t = threading.Thread(target=_timer_worker, args=(seconds_delay, message), daemon=True)
    t.start()

    res = f"Reminder scheduled for {target_dt.strftime('%I:%M %p')} ({minutes_delay} mins from now): '{message}'."
    print_tool_result(res)
    return res

def list_active_reminders() -> str:
    """
    Lists all currently pending timers and reminders.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("list_active_reminders", {})

    if not _ACTIVE_TIMERS:
        res = "No active timers or reminders are currently running."
        print_tool_result(res)
        return res

    lines = [f"{'LABEL':<30} {'TIME REMAINING':<15} {'DUE AT':<15}"]
    lines.append("-" * 60)
    for t in _ACTIVE_TIMERS:
        lines.append(f"{t['label']:<30} {t.get('minutes', 0)} mins{'':<8} {t.get('finish_time', ''):<15}")
    res = "\n".join(lines)
    print_tool_result(res)
    return res

