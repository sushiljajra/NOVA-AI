#!/usr/bin/env python3
"""
E.C.L.I.P.S.E. - Autonomous Desktop Assistant
Phase 1 & 2: Core Brain, Desktop Hands, Multimodal Vision, Memory & Voice
"""

import sys
import os
import threading
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# If running silently in the background via pythonw (no terminal attached), redirect to nova.log
if sys.stdout is None or sys.stderr is None:
    log_file = ROOT_DIR / "nova.log"
    sys.stdout = open(log_file, "a", encoding="utf-8", buffering=1)
    sys.stderr = open(log_file, "a", encoding="utf-8", buffering=1)

from rich.prompt import Prompt
from nova import config
from nova.core.ui import print_banner, print_status, print_jarvis_response, console
from nova.core.agent import GeminiNovaAgent, OpenAINovaAgent
from nova.core.voice import speak, listen_for_command
from nova.core.wake_listener import start_hands_free_session
from nova.tools.system_tools import get_system_vitals
from nova.tools.email_tools import get_daily_briefing

def setup_api_key_if_missing():
    """Prompts the user for an API key if none is found in .env."""
    if config.GEMINI_API_KEY or config.OPENAI_API_KEY or config.GROQ_API_KEY:
        return

    console.print("\n[bold yellow]Attention:[/bold yellow] No API key detected in your environment or [bold].env[/bold] file.")
    console.print("[dim]You can get a free Gemini API key from: [link=https://aistudio.google.com/]https://aistudio.google.com/[/link][/dim]\n")
    
    key = Prompt.ask("[bold cyan]Enter your Gemini API Key[/bold cyan]").strip()
    if not key:
        console.print("[bold red]An API key is required to activate ECLIPSE's neural core. Exiting.[/bold red]")
        sys.exit(1)

    env_path = ROOT_DIR / ".env"
    with open(env_path, "a", encoding="utf-8") as f:
        f.write(f"\nGEMINI_API_KEY={key}\n")
    
    config.GEMINI_API_KEY = key
    config.DEFAULT_PROVIDER = "gemini"
    console.print("[green]✓ Key saved to .env successfully.[/green]\n")

def init_agent():
    setup_api_key_if_missing()

    if config.DEFAULT_PROVIDER == "gemini":
        return GeminiNovaAgent(api_key=config.GEMINI_API_KEY, model=config.DEFAULT_MODEL)
    elif config.DEFAULT_PROVIDER == "openai":
        return OpenAINovaAgent(api_key=config.OPENAI_API_KEY, model=config.DEFAULT_MODEL)
    elif config.DEFAULT_PROVIDER == "groq":
        return OpenAINovaAgent(
            api_key=config.GROQ_API_KEY,
            model=config.DEFAULT_MODEL,
            base_url="https://api.groq.com/openai/v1"
        )
    else:
        raise ValueError(f"Unsupported provider: {config.DEFAULT_PROVIDER}")

def main():
    print_banner()
    agent = init_agent()
    active_m = agent.active_model if hasattr(agent, 'active_model') else config.DEFAULT_MODEL
    print_status(config.DEFAULT_PROVIDER, active_m, config.USER_NAME)

    voice_status = "[green]Enabled[/green]" if config.VOICE_ENABLED else "[dim]Disabled[/dim]"
    console.print(f"[dim cyan]Voice Output: {voice_status} | Type 'wake' for Hands-Free mode, or 'mic' to speak.[/dim cyan]\n")
    console.print(f"[dim cyan]N.O.V.A. is online and ready, {config.USER_NAME}. Type your command, or 'wake', 'briefing', 'vitals', 'clear', or 'exit'.[/dim cyan]\n")

    # If launched with --wake or --voice flag, enter hands-free wake word loop directly
    if "--wake" in sys.argv or "--voice" in sys.argv:
        start_hands_free_session(agent)

    while True:
        try:
            user_input = console.input(f"[bold cyan]You[/bold cyan] [dim]({config.USER_NAME})[/dim] > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit", "bye"):
                farewell = "Powering down systems. Standing by, Sir."
                print_jarvis_response(farewell)
                if config.VOICE_ENABLED:
                    speak(farewell, config.VOICE_NAME)
                break

            if user_input.lower() == "clear":
                console.clear()
                print_banner()
                continue

            if user_input.lower() == "voice on":
                config.VOICE_ENABLED = True
                console.print("[green]✓ Voice output enabled.[/green]")
                speak("Voice feedback activated, Sir.", config.VOICE_NAME)
                continue

            if user_input.lower() == "voice off":
                config.VOICE_ENABLED = False
                console.print("[dim]✓ Voice output muted.[/dim]")
                continue

            if user_input.lower() in ("wake", "handsfree", "continuous"):
                start_hands_free_session(agent)
                continue

            if user_input.lower() in ("mic", "listen", "voice"):
                console.print("[bold cyan]🎤 Listening... (Speak now)[/bold cyan]")
                spoken = listen_for_command()
                if not spoken:
                    console.print("[dim]No speech detected. Returning to keyboard input.[/dim]")
                    continue
                console.print(f"[bold cyan]Heard:[/bold cyan] [white]{spoken}[/white]")
                user_input = spoken

            if user_input.lower() == "vitals":
                vitals = get_system_vitals()
                console.print(vitals)
                continue

            if user_input.lower() == "briefing":
                with console.status("[bold cyan]Compiling executive briefing...[/bold cyan]", spinner="dots"):
                    briefing = get_daily_briefing()
                print_jarvis_response(briefing)
                if config.VOICE_ENABLED:
                    threading.Thread(target=speak, args=(briefing, config.VOICE_NAME), daemon=True).start()
                continue

            with console.status("[bold cyan]N.O.V.A. processing and executing...[/bold cyan]", spinner="dots"):
                response = agent.interact(user_input)

            print_jarvis_response(response)

            # Speak response in background thread if voice is enabled
            if config.VOICE_ENABLED:
                threading.Thread(target=speak, args=(response, config.VOICE_NAME), daemon=True).start()

        except KeyboardInterrupt:
            console.print("\n[dim]Session suspended.[/dim]")
            break
        except Exception as e:
            console.print(f"\n[bold red]System Anomaly:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()

