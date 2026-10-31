# 📘 N.O.V.A. — Complete Setup & Operator Manual
> **Neural Optical Voice & Autonomous Assistant**  
> An Iron Man-inspired autonomous desktop assistant with real-time computer control, multimodal screen vision, dynamic GUI grounding, permanent memory, and hands-free wake-word detection.

---

## 📋 Table of Contents
1. [Prerequisites](#-prerequisites)
2. [Quick Installation](#-quick-installation)
3. [Configuration (.env)](#-configuration-env)
4. [Operation Modes](#-operation-modes)
5. [Complete Command Reference](#-complete-command-reference)
6. [Autonomous Protocols](#-autonomous-protocols)
7. [Architecture & Subsystems](#-architecture--subsystems)
8. [Troubleshooting & FAQs](#-troubleshooting--faqs)

---

## 🛠️ Prerequisites

* **Operating System:** Windows 10 or Windows 11 (64-bit).
* **Python:** Python 3.10, 3.11, 3.12, or 3.13.
* **Hardware:** A working microphone (for hands-free wake-word mode) and audio output/speakers.
* **API Key:** A free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/) (or Groq / OpenAI).

---

## 🚀 Quick Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/sushiljajra/NOVA-AI.git
cd NOVA-AI
```

### Step 2: Create a Virtual Environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Open `.env` and paste your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
NOVA_USER_NAME=Sir
NOVA_MODEL=gemini-3.5-flash-lite
NOVA_VOICE=en-GB-RyanNeural
```

---

## 🎮 Operation Modes

N.O.V.A. supports **three convenient execution modes**:

### Mode 1: Hands-Free Voice Assistant (Recommended)
Double-click [`nova_voice.bat`](file:///d:/Projects/Eclipse/nova_voice.bat) or run:
```powershell
.\.venv\Scripts\python.exe run_nova.py --wake
```
* Sits ambiently listening on your microphone.
* Say **`"Nova"`** or **`"Hey Nova"`** from across the room.
* The floating **iPhone-style Dynamic Island HUD** will expand at the top of your screen.
* Supports **Continuous Follow-Up Mode**: After N.O.V.A. answers, you have a 5-second window to ask follow-up questions without repeating the wake word.

### Mode 2: Interactive Terminal Interface
Double-click [`nova.bat`](file:///d:/Projects/Eclipse/nova.bat) or run:
```powershell
.\.venv\Scripts\python.exe run_nova.py
```
* Type commands directly into the terminal or type `wake` to switch to voice mode.
* Type `mic` to speak a one-off voice command.
* Type `briefing` to compile your morning executive intelligence report.

### Mode 3: Silent 24/7 Windows Background Mode (Auto-Boot)
* Double-click [`install_autostart.bat`](file:///d:/Projects/Eclipse/install_autostart.bat) once.
* N.O.V.A. is registered into your Windows Startup folder (`NOVA_Assistant.vbs`).
* Every time you turn on your laptop, N.O.V.A. automatically boots silently in the background with **zero terminal windows**.
* To pause or stop background listening anytime, run [`stop_nova.bat`](file:///d:/Projects/Eclipse/stop_nova.bat).

---

## 💬 Complete Command Reference

| Category | Example Commands | What N.O.V.A. Does |
| :--- | :--- | :--- |
| **📱 WhatsApp & Contacts** | *"Remember Papa's number as +91 XXXXX XXXXX"*<br>*"Send 'Hello from Nova' to Papa on WhatsApp"* | Resolves contact, opens WhatsApp Web, types message, and auto-dispatches by pressing Enter. |
| **👁️ Screen Vision & Grounding** | *"Look at my screen and tell me what is open."*<br>*"Click on the green Submit button."*<br>*"Click the YouTube play icon."* | Captures screen, uses multimodal AI vision to find 2D coordinates, and clicks UI elements dynamically. |
| **🪟 Window Management** | *"Focus Chrome."*<br>*"Snap this window to the left."*<br>*"Minimize all windows."*<br>*"Close Notepad."* | Brings apps to foreground, splits screen, minimizes, or closes application windows. |
| **🎵 Media & Volume** | *"Turn the volume up by 10 percent."*<br>*"Mute audio."*<br>*"Play relaxing Lo-Fi beats on YouTube."* | Direct Win32 hardware virtual-key audio control and browser media playback. |
| **⏰ Alarms & Timers** | *"Remind me to check the oven in 25 minutes."*<br>*"Set an alarm for 5:30 PM."*<br>*"Show my active reminders."* | Dispatches background thread timers with audio chimes and native Windows desktop notifications. |
| **🧠 Long-Term Memory** | *"Remember that my favorite editor is VS Code."*<br>*"Save a note: WiFi password is NovaNet123."*<br>*"Recall my WiFi password."* | Persists user preferences and notes into local SQLite database across restarts. |
| **💻 System Telemetry** | *"Check my PC vitals."*<br>*"What processes are eating my RAM?"*<br>*"Open Chrome."* | Reports CPU load, available RAM, disk space, battery status, and process consumption. |
| **📁 File System** | *"Find all PDFs downloaded in the last 48 hours."*<br>*"Read this script and summarize it."* | Searches files recursively, reads text, and inspects directories. |
| **🌐 Web Intelligence** | *"Search the web for latest tech headlines."*<br>*"Open GitHub in my browser."* | Real-time DuckDuckGo searches and browser navigation. |

---

## 🛡️ Autonomous Protocols

Just like Tony Stark commanding *"JARVIS, initiate House Party Protocol"*, N.O.V.A. comes equipped with pre-programmed multi-step autonomous routines:

* **`"Nova, initiate Protocol Dev"`**: Automatically launches VS Code, opens GitHub in browser, and starts Lo-Fi study beats on YouTube.
* **`"Nova, initiate Protocol Maintenance"`**: Purges Windows temporary caches, inspects active processes, and checks system vitals.
* **`"Nova, initiate Protocol Focus"`**: Dims system audio and arms a 45-minute Pomodoro focus block with audio/desktop alert.
* **`"Nova, initiate Protocol Night"`**: Dims master audio, clears clipboard, and checks pending reminders for tomorrow.

### Create Your Own Protocols On the Fly:
You can create custom protocols simply by telling N.O.V.A.:
> *"Nova, create a new protocol called Gaming that opens Discord and turns the volume up."*

---

## 🏗️ Architecture & Subsystems

```
nova/
├── config.py              # Configuration & persona instructions
├── core/
│   ├── agent.py           # Autonomous tool execution loop with model fallback
│   ├── dynamic_island.py  # Floating iPhone-style Dynamic Island Tkinter HUD
│   ├── safety.py          # Safety interceptor for destructive shell commands
│   ├── ui.py              # Terminal UI & formatting
│   ├── voice.py           # Neural Edge-TTS + SpeechRecognition STT
│   └── wake_listener.py   # Ultra-low latency ambient wake-word detector
└── tools/
    ├── code_tools.py      # Dynamic Python scratchpad code runner
    ├── contact_tools.py   # Persistent contact book manager
    ├── email_tools.py     # Email sender & daily executive briefing compiler
    ├── file_tools.py      # Filesystem read/write/search
    ├── gui_tools.py       # Mouse click, keyboard typing, hotkeys, screenshot
    ├── media_tools.py     # Win32 hardware volume & YouTube launcher
    ├── memory_tools.py    # SQLite permanent semantic memory bank
    ├── protocol_tools.py  # Autonomous multi-step macro protocols
    ├── reminder_tools.py  # Background timers & Windows notifications
    ├── system_tools.py    # Shell commands, PC vitals, process manager
    ├── vision_tools.py    # Multimodal screen perception & visual click grounding
    ├── web_tools.py       # DuckDuckGo search & browser launcher
    ├── whatsapp_tools.py  # Adaptive WhatsApp Web auto-sender
    └── window_tools.py    # Window listing, snapping, focusing, and closing
```

---

## ❓ Troubleshooting & FAQs

### 1. N.O.V.A. is not waking up when I speak
* Ensure your microphone is plugged in and set as the default recording device in Windows Sound Settings.
* Speak clearly near your microphone: *"Nova"* or *"Hey Nova"*.
* If running in a noisy room, launch [`nova_voice.bat`](file:///d:/Projects/Eclipse/nova_voice.bat) in interactive mode to check microphone calibration output.

### 2. How to change the voice persona?
Open `.env` and set `NOVA_VOICE` to any Microsoft Edge Neural Voice:
* `en-GB-RyanNeural` (Default: Sophisticated British AI)
* `en-US-ChristopherNeural` (American tech assistant)
* `en-US-GuyNeural` (Casual American male)
* `en-AU-WilliamNeural` (Australian English)

### 3. How do I pause or uninstall auto-boot?
* Run [`stop_nova.bat`](file:///d:/Projects/Eclipse/stop_nova.bat) to stop running background processes.
* Run [`uninstall_autostart.bat`](file:///d:/Projects/Eclipse/uninstall_autostart.bat) to remove N.O.V.A. from Windows Startup.
