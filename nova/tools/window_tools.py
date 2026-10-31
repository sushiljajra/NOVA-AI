import time
import ctypes
import pyautogui
import pygetwindow as gw
from typing import List, Dict, Any

user32 = ctypes.windll.user32

def list_open_windows() -> str:
    """
    Lists all currently open, visible application windows on the desktop.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("list_open_windows", {})

    try:
        windows = [w for w in gw.getAllWindows() if w.title and w.title.strip()]
        # Filter out tiny or empty utility handles
        visible = [w for w in windows if w.width > 150 and w.height > 100]

        if not visible:
            res = "No prominent open windows detected on the desktop."
            print_tool_result(res)
            return res

        lines = [f"{'TITLE':<45} {'DIMENSIONS':<15} {'STATE'}"]
        lines.append("-" * 75)
        for w in visible[:15]:
            state = "Minimized" if w.isMinimized else ("Maximized" if w.isMaximized else "Normal")
            lines.append(f"{w.title[:43]:<45} {f'{w.width}x{w.height}':<15} {state}")
        res = "\n".join(lines)
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error listing windows: {str(e)}"
        print_tool_result(err)
        return err

def focus_window(title_keyword: str) -> str:
    """
    Brings an open window to the active foreground by its title or app name (e.g., 'Chrome', 'Notepad', 'VS Code').
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("focus_window", {"title_keyword": title_keyword})

    try:
        matches = [w for w in gw.getAllWindows() if title_keyword.lower() in w.title.lower()]
        if not matches:
            res = f"No open window found matching '{title_keyword}'."
            print_tool_result(res)
            return res

        target = matches[0]
        if target.isMinimized:
            target.restore()
        target.activate()
        time.sleep(0.3)
        res = f"Brought window '{target.title}' to the foreground."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error focusing window '{title_keyword}': {str(e)}"
        print_tool_result(err)
        return err

def minimize_window(title_keyword: str = "") -> str:
    """
    Minimizes a specific window by title keyword, or minimizes all windows if title_keyword is empty ('win+d').
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("minimize_window", {"title_keyword": title_keyword})

    try:
        if not title_keyword or title_keyword.lower() in ("all", "desktop", "all windows"):
            pyautogui.hotkey("win", "d")
            res = "Minimized all desktop windows."
            print_tool_result(res)
            return res

        matches = [w for w in gw.getAllWindows() if title_keyword.lower() in w.title.lower()]
        if not matches:
            res = f"No window found matching '{title_keyword}'."
            print_tool_result(res)
            return res

        target = matches[0]
        target.minimize()
        res = f"Minimized window '{target.title}'."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error minimizing window: {str(e)}"
        print_tool_result(err)
        return err

def maximize_window(title_keyword: str) -> str:
    """
    Maximizes a specific window to full screen by title keyword.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("maximize_window", {"title_keyword": title_keyword})

    try:
        matches = [w for w in gw.getAllWindows() if title_keyword.lower() in w.title.lower()]
        if not matches:
            res = f"No window found matching '{title_keyword}'."
            print_tool_result(res)
            return res

        target = matches[0]
        target.maximize()
        res = f"Maximized window '{target.title}'."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error maximizing window: {str(e)}"
        print_tool_result(err)
        return err

def close_window(title_keyword: str) -> str:
    """
    Closes a window by title keyword gracefully.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("close_window", {"title_keyword": title_keyword})

    try:
        matches = [w for w in gw.getAllWindows() if title_keyword.lower() in w.title.lower()]
        if not matches:
            res = f"No window found matching '{title_keyword}'."
            print_tool_result(res)
            return res

        target = matches[0]
        target.close()
        res = f"Closed window '{target.title}'."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error closing window: {str(e)}"
        print_tool_result(err)
        return err

def snap_window(direction: str = "left") -> str:
    """
    Snaps the currently active window using Windows Snap Assist.
    Directions: 'left', 'right', 'up' (maximize), 'down' (minimize/restore).
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("snap_window", {"direction": direction})

    d = direction.lower().strip()
    valid_dirs = {"left": "left", "right": "right", "up": "up", "down": "down"}
    key = valid_dirs.get(d, "left")

    try:
        pyautogui.hotkey("win", key)
        res = f"Snapped active window to {key}."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error snapping window: {str(e)}"
        print_tool_result(err)
        return err

