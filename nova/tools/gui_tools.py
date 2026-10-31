import os
import time
from pathlib import Path
import pyautogui
import pyperclip

# Enable safety pause
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def press_hotkey(keys: str) -> str:
    """
    Simulates pressing a keyboard hotkey combination or special key on your computer.
    Examples:
    - 'ctrl+c', 'ctrl+v', 'ctrl+z', 'ctrl+s', 'ctrl+w', 'ctrl+t'
    - 'alt+tab', 'alt+f4', 'win+d' (minimize all), 'win+e' (open explorer)
    - 'enter', 'space', 'esc', 'backspace', 'tab', 'f5'
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("press_hotkey", {"keys": keys})

    try:
        parts = [k.strip().lower() for k in keys.split("+")]
        if len(parts) == 1:
            pyautogui.press(parts[0])
        else:
            pyautogui.hotkey(*parts)
        res = f"Simulated hotkey sequence: '{keys}'."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error pressing hotkey '{keys}': {str(e)}"
        print_tool_result(err)
        return err

def type_text(text: str, press_enter: bool = False) -> str:
    """
    Simulates typing text on the keyboard into whatever window or text field is currently focused.
    If press_enter is True, presses the Enter key immediately after typing.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("type_text", {"text": text, "press_enter": press_enter})

    try:
        # Using pyperclip + paste for full unicode/emoji support without typing bugs
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        if press_enter:
            time.sleep(0.2)
            pyautogui.press("enter")
        res = f"Typed text into active window ({len(text)} characters, enter={press_enter})."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error typing text: {str(e)}"
        print_tool_result(err)
        return err

def click_mouse(x: int = -1, y: int = -1, clicks: int = 1, button: str = "left") -> str:
    """
    Clicks the mouse at coordinate (x, y) on the screen.
    If x and y are -1, clicks at the current cursor position.
    button can be 'left', 'right', or 'middle'.
    clicks can be 1 (single click) or 2 (double click).
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("click_mouse", {"x": x, "y": y, "clicks": clicks, "button": button})

    try:
        if x >= 0 and y >= 0:
            pyautogui.click(x=x, y=y, clicks=clicks, button=button)
            res = f"Clicked mouse at ({x}, {y}) [button={button}, clicks={clicks}]."
        else:
            pyautogui.click(clicks=clicks, button=button)
            pos = pyautogui.position()
            res = f"Clicked mouse at current position ({pos.x}, {pos.y}) [button={button}, clicks={clicks}]."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error clicking mouse: {str(e)}"
        print_tool_result(err)
        return err

def scroll_screen(amount: int = -300) -> str:
    """
    Scrolls the mouse wheel. Negative values scroll down (e.g., -300), positive values scroll up (e.g., 300).
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("scroll_screen", {"amount": amount})

    try:
        pyautogui.scroll(amount)
        direction = "down" if amount < 0 else "up"
        res = f"Scrolled screen {direction} by {abs(amount)} units."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error scrolling: {str(e)}"
        print_tool_result(err)
        return err

def take_screenshot(filename: str = "screenshot.png") -> str:
    """
    Captures a full screenshot of the computer monitor and saves it to disk.
    Returns the file path and screen dimensions.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    from nova.tools.vision_tools import _capture_screen_bytes
    print_tool_call("take_screenshot", {"filename": filename})

    try:
        out_path = Path(__file__).resolve().parent.parent.parent / filename
        png_data = _capture_screen_bytes()
        with open(out_path, "wb") as f:
            f.write(png_data)
        res = f"Screenshot captured successfully: {out_path} ({len(png_data) // 1024} KB)."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error capturing screenshot: {str(e)}"
        print_tool_result(err)
        return err

def get_clipboard() -> str:
    """
    Retrieves the current text from the computer's clipboard.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("get_clipboard", {})

    try:
        content = pyperclip.paste()
        res = f"Clipboard content ({len(content)} chars): {content[:200]}"
        print_tool_result(res)
        return content or "[Clipboard is empty]"
    except Exception as e:
        err = f"Error reading clipboard: {str(e)}"
        print_tool_result(err)
        return err

def set_clipboard(text: str) -> str:
    """
    Copies text to the computer's clipboard.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("set_clipboard", {"text": text[:50]})

    try:
        pyperclip.copy(text)
        res = f"Copied {len(text)} characters to clipboard."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error copying to clipboard: {str(e)}"
        print_tool_result(err)
        return err

