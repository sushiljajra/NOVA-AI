# N.O.V.A. (Neural Optical Voice & Autonomous Assistant)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python Version" />
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge&logo=windows" alt="Platform" />
  <img src="https://img.shields.io/badge/Model-Gemini%20Flash%20%7C%20OpenAI%20%7C%20Groq-8A2BE2?style=for-the-badge" alt="AI Brain" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

> An Iron Man-inspired autonomous desktop assistant engineered with **real-time computer control**, **iPhone-style Dynamic Island HUD**, **multimodal screen vision**, **permanent SQLite memory**, **WhatsApp automation**, and **hands-free ambient wake-word detection**.

---

## ⚡ What Makes N.O.V.A. Unique?

* **🎙️ Ultra-Low Latency Ambient Wake-Word:** Say *"Nova"* or *"Hey Nova"* from across the room. Detects and awakens in **~1 second** with continuous conversational follow-up.
* **🏝️ Floating Dynamic Island HUD:** Sleek, borderless iPhone-style capsule that expands at the top-center of your screen, displaying real-time audio waveforms, listening pulses, and tool telemetry.
* **👁️ Multimodal Visual Click Grounding:** Don't have API access to an app? N.O.V.A. looks at your monitor screenshot, computes normalized 2D coordinates for any requested button/icon, and clicks it dynamically.
* **🛡️ Iron Man Autonomous Protocols:** Execute named multi-step macro routines like `Protocol Dev`, `Protocol Maintenance`, `Protocol Focus`, and `Protocol Night`.
* **📱 Full Desktop & WhatsApp Automation:** Manage contacts, draft and auto-dispatch WhatsApp messages, control Win32 hardware volume, and organize windows.
* **🧠 Permanent Long-Term Memory:** Remembers your preferences, habits, and notes across sessions via a local SQLite database.

---

## 🛠️ Complete Subsystems (45 Tools)

```
        ┌──────────────────────────────────────────────────────────┐
        │            N.O.V.A. NEURAL EXECUTIVE CORE                │
        └───────┬───────────────────┬───────────────────┬──────────┘
                │                   │                   │
      ┌─────────▼─────────┐ ┌───────▼─────────┐ ┌───────▼──────────┐
      │   SENSES & HUD    │ │   EXECUTION     │ │     STORAGE      │
      ├───────────────────┤ ├─────────────────┤ ├──────────────────┤
      │ • Dynamic Island  │ │ • 45 OS Tools   │ │ • SQLite Memory  │
      │ • Ambient Wake    │ │ • Protocols     │ │ • Contacts Book  │
      │ • Neural TTS      │ │ • Shell Runner  │ │ • Macro Store    │
      │ • Vision Grounding│ │ • WhatsApp Auto │ │ • Settings (.env)│
      └───────────────────┘ └─────────────────┘ └──────────────────┘
```

---

## 🚀 Quick Start Guide

Detailed step-by-step installation instructions can be found in **[INSTRUCTIONS.md](INSTRUCTIONS.md)**.

### 1. Clone & Install
```bash
git clone https://github.com/sushiljajra/NOVA-AI.git
cd NOVA-AI
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Key
Copy `.env.example` to `.env` and paste your free Google Gemini API key:
```env
GEMINI_API_KEY=your_key_here
NOVA_USER_NAME=Sir
NOVA_MODEL=gemini-3.5-flash-lite
NOVA_VOICE=en-GB-RyanNeural
```

### 3. Launch
* **Hands-Free Voice Mode:** Double-click [`nova_voice.bat`](nova_voice.bat) (or run `python run_nova.py --wake`).
* **Interactive CLI Mode:** Double-click [`nova.bat`](nova.bat) (or run `python run_nova.py`).
* **Silent 24/7 Auto-Start on Boot:** Double-click [`install_autostart.bat`](install_autostart.bat).

---

## 💡 Example Voice & Text Commands

* **Hands-Free Voice:** *"Nova, what are my PC vitals?"*
* **Visual Computer-Use:** *"Nova, look at my screen and click on the search bar."*
* **Messaging:** *"Save Papa's number as +91... and send hello to Papa on WhatsApp."*
* **Autonomous Routines:** *"Nova, initiate Protocol Dev."*
* **Media & Audio:** *"Play Lo-Fi chill beats on YouTube and turn the volume up."*
* **Window Control:** *"Focus Chrome and snap this window to the left."*
* **Memory Recall:** *"Remember that my server IP is 192.168.1.50"*, followed by *"What is my server IP?"*

---

## 📄 License
Distributed under the MIT License. Built for autonomous desktop interaction.
