import io
import re
import json
import time
from pathlib import Path
from typing import Optional
import pyautogui

def _capture_screen_bytes() -> bytes:
    """Captures the screen and returns PNG bytes using mss with PIL fallback."""
    try:
        import mss
        import mss.tools
        with mss.mss() as sct:
            monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
            sct_img = sct.grab(monitor)
            png_bytes = mss.tools.to_png(sct_img.rgb, sct_img.size)
            return png_bytes
    except Exception:
        pass

    try:
        from PIL import ImageGrab
        im = ImageGrab.grab()
        buf = io.BytesIO()
        im.save(buf, format="PNG")
        return buf.getvalue()
    except Exception as e:
        raise RuntimeError(f"Could not capture desktop screen: {str(e)}")

def analyze_screen(query: str = "Describe what is currently visible on my screen, identify active windows, and read any prominent text, code, or error messages.") -> str:
    """
    Takes a real-time screenshot of the user's computer screen and uses multimodal AI vision
    to analyze, read text, troubleshoot error messages, or inspect web pages and diagrams.
    Example: analyze_screen(query="What error is this Python terminal showing?")
    """
    from nova.core.ui import print_tool_call, print_tool_result, print_warning
    from nova.config import GEMINI_API_KEY
    print_tool_call("analyze_screen", {"query": query})

    try:
        image_bytes = _capture_screen_bytes()

        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        vision_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-flash-latest"]
        
        last_err = None
        for model_name in vision_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                        query
                    ]
                )
                res = response.text or "I examined your screen, Sir, but could not detect distinct details."
                print_tool_result(res)
                return res
            except Exception as e:
                last_err = e
                continue

        err_msg = f"Error during screen analysis: {str(last_err)}"
        print_tool_result(err_msg)
        return err_msg

    except Exception as e:
        err = f"Failed to capture or analyze screen: {str(e)}"
        print_tool_result(err)
        return err

def click_ui_element(element_description: str, clicks: int = 1, button: str = "left") -> str:
    """
    Finds any button, icon, tab, link, or text element visually on your screen and clicks it!
    Uses multimodal visual coordinate grounding (no hardcoded coordinates needed).
    Examples:
    - click_ui_element(element_description="The green Submit button")
    - click_ui_element(element_description="The YouTube play icon")
    - click_ui_element(element_description="The search bar at the top")
    - click_ui_element(element_description="Close tab icon on Chrome")
    """
    from nova.core.ui import print_tool_call, print_tool_result
    from nova.config import GEMINI_API_KEY
    print_tool_call("click_ui_element", {"element_description": element_description, "clicks": clicks})

    try:
        image_bytes = _capture_screen_bytes()
        screen_w, screen_h = pyautogui.size()

        prompt = f"""
Look at this desktop screenshot. Your task is to locate the UI element: "{element_description}".
Return ONLY a valid JSON object with normalized coordinates scaled from 0 to 1000 for the center of this element:
{{"x": integer, "y": integer}}
If the element is not found on the screen, return:
{{"error": "Element not visible"}}
Do not include any other markdown formatting or text outside the JSON.
"""

        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        vision_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash"]

        raw_text = ""
        for model_name in vision_models:
            try:
                resp = client.models.generate_content(
                    model=model_name,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
                        prompt
                    ]
                )
                raw_text = resp.text or ""
                if "x" in raw_text and "y" in raw_text:
                    break
            except Exception:
                continue

        # Extract JSON from model output
        match = re.search(r'\{[^{}]*\}', raw_text)
        if not match:
            res = f"Could not visually pinpoint '{element_description}' on screen."
            print_tool_result(res)
            return res

        coords = json.loads(match.group(0))
        if "error" in coords:
            res = f"Element '{element_description}' is not currently visible on the screen."
            print_tool_result(res)
            return res

        norm_x = int(coords["x"])
        norm_y = int(coords["y"])

        # Convert normalized 0-1000 to actual monitor pixels
        actual_x = int((norm_x / 1000.0) * screen_w)
        actual_y = int((norm_y / 1000.0) * screen_h)

        # Move mouse smoothly to element and click
        pyautogui.moveTo(actual_x, actual_y, duration=0.4)
        pyautogui.click(x=actual_x, y=actual_y, clicks=clicks, button=button)

        res = f"Located and clicked '{element_description}' at screen position ({actual_x}, {actual_y})."
        print_tool_result(res)
        return res

    except Exception as e:
        err = f"Error during visual click: {str(e)}"
        print_tool_result(err)
        return err

