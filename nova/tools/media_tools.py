import ctypes
import webbrowser
import urllib.parse
from typing import Dict, Any

# Windows Virtual-Key Codes for Media & Hardware Control
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

def _send_vk(vk_code: int):
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY, 0)
    ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)

def control_media(action: str, steps: int = 5) -> str:
    """
    Controls computer audio and media playback.
    Actions supported:
    - 'volume_up': Increases system volume (can specify steps, e.g. 5)
    - 'volume_down': Decreases system volume
    - 'mute': Toggles mute / unmute
    - 'play_pause': Toggles play/pause for Spotify, YouTube, or background media
    - 'next_track': Skips to next song/video
    - 'prev_track': Skips to previous song/video
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("control_media", {"action": action, "steps": steps})

    act = action.strip().lower()
    try:
        if act in ("volume_up", "volup", "increase_volume"):
            for _ in range(steps):
                _send_vk(VK_VOLUME_UP)
            res = f"Increased volume by {steps * 2}%."
        elif act in ("volume_down", "voldown", "decrease_volume"):
            for _ in range(steps):
                _send_vk(VK_VOLUME_DOWN)
            res = f"Decreased volume by {steps * 2}%."
        elif act in ("mute", "unmute", "toggle_mute"):
            _send_vk(VK_VOLUME_MUTE)
            res = "Toggled system mute."
        elif act in ("play_pause", "play", "pause", "toggle_play"):
            _send_vk(VK_MEDIA_PLAY_PAUSE)
            res = "Dispatched media play/pause signal."
        elif act in ("next_track", "next", "skip"):
            _send_vk(VK_MEDIA_NEXT_TRACK)
            res = "Dispatched next track signal."
        elif act in ("prev_track", "previous", "back"):
            _send_vk(VK_MEDIA_PREV_TRACK)
            res = "Dispatched previous track signal."
        else:
            res = f"Unknown media action '{action}'. Supported: volume_up, volume_down, mute, play_pause, next_track, prev_track."
        
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error executing media action '{action}': {str(e)}"
        print_tool_result(err)
        return err

def play_on_youtube(query: str) -> str:
    """
    Searches YouTube and opens the results/video in the default browser.
    Example: play_on_youtube(query="lofi hip hop radio")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    print_tool_call("play_on_youtube", {"query": query})

    try:
        encoded = urllib.parse.quote(query)
        url = f"https://www.youtube.com/results?search_query={encoded}"
        webbrowser.open(url)
        res = f"Opened YouTube search for '{query}' in browser."
        print_tool_result(res)
        return res
    except Exception as e:
        err = f"Error opening YouTube: {str(e)}"
        print_tool_result(err)
        return err

