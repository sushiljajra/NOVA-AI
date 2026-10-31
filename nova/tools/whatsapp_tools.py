import time
import urllib.parse
import webbrowser
import threading
from typing import Optional
from nova.tools.contact_tools import _load_contacts

def _focus_window_and_press_enter():
    """Focuses the browser or WhatsApp window and simulates pressing Enter."""
    try:
        import pyautogui
        import pygetwindow as gw

        # Find any matching WhatsApp or browser windows
        target_win = None
        for keyword in ["WhatsApp", "Chrome", "Brave", "Edge", "Firefox"]:
            matches = gw.getWindowsWithTitle(keyword)
            if matches:
                target_win = matches[0]
                break

        if target_win:
            try:
                if target_win.isMinimized:
                    target_win.restore()
                target_win.activate()
                time.sleep(0.3)
            except Exception:
                pass

        # Press Enter to send the message
        pyautogui.press("enter")
    except Exception:
        pass

def _auto_dispatch_enter(initial_delay: int = 10, attempts: int = 4, interval: int = 4):
    """
    Waits for WhatsApp Web to connect and load the chat, then activates the window
    and dispatches Enter across multiple intervals to ensure delivery regardless
    of network or load latency.
    """
    time.sleep(initial_delay)
    for _ in range(attempts):
        _focus_window_and_press_enter()
        time.sleep(interval)

def send_whatsapp_message(target: str, message: str, auto_send: bool = True) -> str:
    """
    Sends a WhatsApp message to a contact name (e.g., 'Papa', 'Mom') or direct phone number.
    If target is a name, ECLIPSE resolves their phone number from the contacts memory.
    If auto_send is True, ECLIPSE automatically focuses the window and dispatches the message.
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("send_whatsapp_message", {"target": target, "message": message, "auto_send": auto_send})

    contacts = _load_contacts()
    query = target.strip().lower()
    phone_number = ""
    display_target = target

    # 1. Resolve contact if target is a name
    if query in contacts:
        phone_number = contacts[query].get("phone", "")
        display_target = contacts[query].get("display_name", target)
    else:
        # Check partial or relationship match
        for k, v in contacts.items():
            if query in k or query in v.get("relationship", "").lower():
                phone_number = v.get("phone", "")
                display_target = v.get("display_name", target)
                break

    # If not in contacts, check if target contains phone number digits
    if not phone_number:
        digits = "".join(filter(str.isdigit, target))
        if len(digits) >= 10:
            phone_number = digits
        else:
            msg = f"Error: Contact '{target}' is not saved in contacts memory and no valid phone number was provided. Please save the contact first using save_contact."
            print_tool_result(msg)
            return msg

    # Format phone number for WhatsApp URL (digits only, no '+' or leading zeros)
    clean_digits = "".join(filter(str.isdigit, phone_number))
    # If 10 digits without country code, default to India (+91)
    if len(clean_digits) == 10:
        clean_digits = "91" + clean_digits

    encoded_msg = urllib.parse.quote(message)
    whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_digits}&text={encoded_msg}"

    # Open WhatsApp in browser
    webbrowser.open(whatsapp_url)

    if auto_send:
        # Launch background adaptive dispatcher
        threading.Thread(target=_auto_dispatch_enter, args=(10, 4, 4), daemon=True).start()
        status = f"Opening WhatsApp chat for {display_target} (+{clean_digits}) with message: '{message}'. ECLIPSE is actively focusing the window and will dispatch the send command as soon as the chat finishes loading."
    else:
        status = f"Opened WhatsApp chat for {display_target} (+{clean_digits}) with pre-filled message '{message}'. Ready for your review."

    print_tool_result(status)
    return status

