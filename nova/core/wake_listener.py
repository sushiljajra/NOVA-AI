import time
import winsound
import speech_recognition as sr
from nova.core.voice import speak, listen_for_command, listen_for_followup
from nova.core.ui import console, print_jarvis_response
from nova.core.dynamic_island import island
from nova import config

WAKE_WORDS = ["nova", "hey nova", "hi nova", "ok nova", "hello nova", "eclipse", "hey eclipse"]

def play_wake_chime():
    """Plays a futuristic ascending two-tone sci-fi chime upon waking up."""
    try:
        winsound.Beep(950, 80)
        winsound.Beep(1550, 130)
    except Exception:
        pass

def play_sleep_chime():
    """Plays a soft descending chime when returning to background standby."""
    try:
        winsound.Beep(1300, 70)
        winsound.Beep(850, 90)
    except Exception:
        pass

def extract_command_after_wake_word(text: str) -> str:
    """If user said 'Eclipse open Chrome', extracts 'open Chrome'."""
    lower = text.lower().strip()
    for w in sorted(WAKE_WORDS, key=len, reverse=True):
        if w in lower:
            idx = lower.find(w) + len(w)
            cmd = lower[idx:].strip(" ,.!?")
            return cmd
    return ""

def listen_for_wake_word_once(recognizer: sr.Recognizer, mic: sr.Microphone, timeout: int = 3) -> str:
    """Listens in rapid 2-second chunks to detect ambient wake word with zero lag."""
    try:
        with mic as source:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=2.0)
        text = recognizer.recognize_google(audio).lower()
        return text
    except Exception:
        return ""

def start_hands_free_session(agent):
    """
    Runs a continuous hands-free voice loop with conversational follow-up memory and Dynamic Island HUD.
    Say 'Eclipse' or 'Hey Eclipse' to wake up.
    """
    # Start the floating iPhone-style Dynamic Island
    island.start()

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 280
    recognizer.dynamic_energy_threshold = False
    recognizer.pause_threshold = 0.3
    recognizer.non_speaking_duration = 0.15
    mic = sr.Microphone()

    console.print("\n[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]")
    console.print("[bold cyan]║  🎙️  N.O.V.A.: HANDS-FREE CONVERSATIONAL VOICE MODE           ║[/bold cyan]")
    console.print("[bold cyan]║  • Wake Word: '[bold white]Nova[/bold white]' or '[bold white]Hey Nova[/bold white]'                             ║[/bold cyan]")
    console.print("[bold cyan]║  • Continuous Follow-up: Ask follow-ups without repeating wake║[/bold cyan]")
    console.print("[bold cyan]║  • British Neural AI Speech enabled                           ║[/bold cyan]")
    console.print("[bold cyan]║  • Press Ctrl+C to return to keyboard input                  ║[/bold cyan]")
    console.print("[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]\n")

    # Ambient noise calibration
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        console.print("[green]✓ Ready. Listening for 'Nova'...[/green]\n")

    while True:
        try:
            detected = listen_for_wake_word_once(recognizer, mic, timeout=5)
            if not detected:
                continue

            has_wake_word = any(w in detected for w in WAKE_WORDS)

            if has_wake_word:
                play_wake_chime()
                island.show_wake()
                console.print(f"[bold cyan]⚡ Wake Word Detected:[/bold cyan] [yellow]'{detected}'[/yellow]")

                # Check if command was included in the same phrase (e.g. "Eclipse check PC vitals")
                cmd = extract_command_after_wake_word(detected)

                if not cmd:
                    console.print("[bold cyan]N.O.V.A.:[/bold cyan] [italic]Yes, Sir? Listening...[/italic]")
                    speak("Yes, Sir?", config.VOICE_NAME)
                    cmd = listen_for_command()

                if not cmd:
                    console.print("[dim]No command detected. Returning to standby.[/dim]\n")
                    play_sleep_chime()
                    island.dismiss(delay=0.5)
                    continue

                # Multi-turn Conversational Loop (Continuous Follow-Up)
                while cmd:
                    console.print(f"[bold cyan]Operator >[/bold cyan] [bold white]{cmd}[/bold white]")
                    island.show_thinking(f"Thinking: {cmd[:30]}...")

                    with console.status("[bold cyan]E.C.L.I.P.S.E. processing and executing...[/bold cyan]", spinner="dots"):
                        response = agent.interact(cmd)

                    print_jarvis_response(response)
                    island.show_speaking(response[:36])
                    speak(response, config.VOICE_NAME)

                    # Listen for follow-up question for 5 seconds without needing wake-word
                    console.print("[dim cyan]✦ Listening for follow-up... (or stay silent to standby)[/dim cyan]")
                    island.show_wake()
                    followup = listen_for_followup(timeout=5)

                    if followup:
                        # Check if user said goodbye or thank you
                        if followup.lower() in ("thank you", "thanks", "bye", "goodbye", "sleep", "dismissed"):
                            farewell = "Always at your service, Sir."
                            print_jarvis_response(farewell)
                            island.show_speaking(farewell)
                            speak(farewell, config.VOICE_NAME)
                            cmd = ""
                        else:
                            console.print(f"[bold cyan]Follow-up heard:[/bold cyan] [white]'{followup}'[/white]")
                            cmd = followup
                    else:
                        cmd = ""

                play_sleep_chime()
                island.dismiss(delay=1.5)
                console.print("\n[dim green]Standing by for 'Eclipse'...[/dim green]\n")

        except KeyboardInterrupt:
            console.print("\n[dim]Hands-free mode paused. Returning to terminal.[/dim]")
            break
        except Exception:
            time.sleep(0.5)

