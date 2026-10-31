import os
import sys
import asyncio
import tempfile
import ctypes
import re
from pathlib import Path
import edge_tts

# Default JARVIS-style British voice
DEFAULT_VOICE = os.getenv("ECLIPSE_VOICE", "en-GB-RyanNeural")
TTS_ENGINE = os.getenv("ECLIPSE_TTS_ENGINE", "edge").lower()  # "edge" or "sapi"

def _clean_text_for_speech(text: str) -> str:
    """Strips markdown and extracts the first 1-2 concise sentences for ultra-fast audio response."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove markdown links
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    # Remove headers, bullets, asterisks, brackets
    text = re.sub(r'[*#_~>|\-•\(\)]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Extract first 2 sentences for crisp, instant JARVIS audio
    sentences = re.split(r'(?<=[.!?])\s+', text)
    concise = " ".join(sentences[:2]).strip()
    if len(concise) > 180:
        concise = concise[:180].rsplit(" ", 1)[0] + "."
    return concise or text[:120]

async def _synthesize_edge_speech(text: str, output_path: str, voice: str):
    communicate = edge_tts.Communicate(text, voice, rate="+15%")  # +15% speed for brisk, modern AI response
    await communicate.save(output_path)

def _speak_sapi(text: str):
    """Zero-latency offline Windows SAPI TTS."""
    try:
        import win32com.client
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Rate = 1
        speaker.Speak(text)
    except Exception:
        # Fallback to PowerShell speech
        import subprocess
        escaped = text.replace('"', '`"')
        subprocess.run(["powershell", "-c", f"Add-Type -AssemblyName System.Speech; `$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; `$s.Rate = 1; `$s.Speak(\"{escaped}\")"], check=False)

def speak(text: str, voice: str = DEFAULT_VOICE):
    """
    Synthesizes and speaks text out loud at accelerated speed.
    """
    clean = _clean_text_for_speech(text)
    if not clean:
        return

    if TTS_ENGINE == "sapi":
        _speak_sapi(clean)
        return

    # Edge TTS (Fast generation of 1-2 crisp sentences)
    temp_mp3 = Path(tempfile.gettempdir()) / "nova_speech.mp3"
    try:
        asyncio.run(_synthesize_edge_speech(clean, str(temp_mp3), voice))

        winmm = ctypes.windll.winmm
        winmm.mciSendStringW(f'open "{temp_mp3}" type mpegvideo alias nova_audio', None, 0, None)
        winmm.mciSendStringW('play nova_audio wait', None, 0, None)
        winmm.mciSendStringW('close nova_audio', None, 0, None)

        if temp_mp3.exists():
            try:
                temp_mp3.unlink()
            except Exception:
                pass
    except Exception:
        pass

# Shared fast speech recognizer
_SHARED_RECOGNIZER = None

def _get_fast_recognizer():
    global _SHARED_RECOGNIZER
    if _SHARED_RECOGNIZER is None:
        import speech_recognition as sr
        _SHARED_RECOGNIZER = sr.Recognizer()
        _SHARED_RECOGNIZER.energy_threshold = 280
        _SHARED_RECOGNIZER.dynamic_energy_threshold = False
        _SHARED_RECOGNIZER.pause_threshold = 0.4
        _SHARED_RECOGNIZER.non_speaking_duration = 0.2
    return _SHARED_RECOGNIZER

def listen_for_command() -> str:
    """
    Fast listener with sub-second silence cut-off.
    """
    try:
        import speech_recognition as sr
        r = _get_fast_recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=4, phrase_time_limit=8)
        text = r.recognize_google(audio)
        return text.strip()
    except Exception:
        return ""

def listen_for_followup(timeout: int = 4) -> str:
    """
    Fast follow-up listener.
    """
    try:
        import speech_recognition as sr
        r = _get_fast_recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=8)
        text = r.recognize_google(audio)
        return text.strip()
    except Exception:
        return ""

