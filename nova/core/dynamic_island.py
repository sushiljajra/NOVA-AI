import time
import threading
import tkinter as tk
from tkinter import font as tkfont
from typing import Optional

class DynamicIsland:
    """
    iPhone-style floating Dynamic Island HUD for Windows.
    Appears smoothly at top-center of the screen during wake, listening, thinking, and speaking states.
    """
    def __init__(self):
        self.root = None
        self.canvas = None
        self.is_running = False
        self._thread = None
        self._state = "hidden"  # hidden, wake, thinking, speaking
        self._text = ""
        self._subtext = ""
        self._wave_frame = 0
        self._hide_timer = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_gui, daemon=True)
        self._thread.start()
        # Wait briefly for GUI initialization
        time.sleep(0.3)

    def _run_gui(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)

        # Transparent window background
        TRANS_COLOR = "#010101"
        self.root.config(bg=TRANS_COLOR)
        self.root.wm_attributes("-transparentcolor", TRANS_COLOR)

        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        # Default dimensions
        self.width = 380
        self.height = 46
        self.pos_x = (self.screen_w - self.width) // 2
        self.pos_y = 12

        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=TRANS_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.is_running = True
        self._render_hidden()
        self._tick_animation()
        self.root.mainloop()

    def _draw_capsule(self, x1, y1, x2, y2, radius=22, fill="#0a0a0f", outline="#00e5ff", width=1):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, fill=fill, outline=outline, width=width)

    def _tick_animation(self):
        if not self.root:
            return

        if self._state == "speaking":
            self._wave_frame = (self._wave_frame + 1) % 10
            self._redraw()
        elif self._state == "thinking":
            self._wave_frame = (self._wave_frame + 1) % 8
            self._redraw()

        self.root.after(80, self._tick_animation)

    def _redraw(self):
        if not self.canvas:
            return
        self.canvas.delete("all")

        if self._state == "hidden":
            # Invisible minimal pill or withdrawn
            self.root.withdraw()
            return

        self.root.deiconify()

        # Outer glowing pill
        self._draw_capsule(2, 2, self.width - 2, self.height - 2, radius=21, fill="#08080c", outline="#00e5ff", width=1)

        # Left status indicator
        cy = self.height // 2
        if self._state == "wake":
            # Glowing cyan circle
            self.canvas.create_oval(16, cy - 6, 28, cy + 6, fill="#00e5ff", outline="")
            # Text
            self.canvas.create_text(42, cy, text="NOVA", anchor="w", fill="#00e5ff", font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(92, cy, text="Listening...", anchor="w", fill="#ffffff", font=("Segoe UI", 10))

        elif self._state == "thinking":
            # Animated pulse dots
            colors = ["#00e5ff", "#0088ff", "#0055aa"]
            offset = self._wave_frame % 3
            self.canvas.create_oval(14, cy - 4, 22, cy + 4, fill=colors[(offset) % 3], outline="")
            self.canvas.create_oval(24, cy - 4, 32, cy + 4, fill=colors[(offset + 1) % 3], outline="")
            self.canvas.create_oval(34, cy - 4, 42, cy + 4, fill=colors[(offset + 2) % 3], outline="")

            display_txt = self._text if self._text else "Processing & executing..."
            if len(display_txt) > 36:
                display_txt = display_txt[:36] + "..."
            self.canvas.create_text(52, cy, text=display_txt, anchor="w", fill="#ffffff", font=("Segoe UI", 10))

        elif self._state == "speaking":
            # Mini animated sound wave bars
            heights = [4, 9, 14, 8, 12, 6, 11]
            shift = self._wave_frame
            for i in range(5):
                h = heights[(i + shift) % len(heights)]
                x = 16 + (i * 5)
                self.canvas.create_line(x, cy - h, x, cy + h, fill="#00e5ff", width=2)

            display_txt = self._text if self._text else "Speaking..."
            if len(display_txt) > 36:
                display_txt = display_txt[:36] + "..."
            self.canvas.create_text(52, cy, text=display_txt, anchor="w", fill="#ffffff", font=("Segoe UI", 10))

    def _render_hidden(self):
        self._state = "hidden"
        self._redraw()

    # Public API called from main assistant
    def show_wake(self):
        """Displays the Island in awake state: 'ECLIPSE • Listening...'"""
        self._state = "wake"
        self._text = "Listening..."
        if self._hide_timer:
            self._hide_timer.cancel()
        if self.root:
            self.root.after(0, self._redraw)

    def show_thinking(self, action_name: str = "Processing..."):
        """Displays thinking state with action preview."""
        self._state = "thinking"
        self._text = action_name
        if self._hide_timer:
            self._hide_timer.cancel()
        if self.root:
            self.root.after(0, self._redraw)

    def show_speaking(self, preview_text: str = ""):
        """Displays speaking state with audio waves."""
        self._state = "speaking"
        self._text = preview_text or "Speaking..."
        if self._hide_timer:
            self._hide_timer.cancel()
        if self.root:
            self.root.after(0, self._redraw)

    def dismiss(self, delay: float = 3.5):
        """Hides the dynamic island after delay seconds."""
        def _hide():
            self._state = "hidden"
            if self.root:
                self.root.after(0, self._redraw)

        if self._hide_timer:
            self._hide_timer.cancel()
        self._hide_timer = threading.Timer(delay, _hide)
        self._hide_timer.daemon = True
        self._hide_timer.start()

# Global singleton instance
island = DynamicIsland()

