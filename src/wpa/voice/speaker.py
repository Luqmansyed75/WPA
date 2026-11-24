"""
Text-to-Speech (TTS) Speaker for WPA using pyttsx3.
"""
import pyttsx3


class Speaker:
    def __init__(self, rate: int = 175, volume: float = 1.0):
        """Initialize offline pyttsx3 TTS engine."""
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

    def speak(self, text: str):
        """Speak the given text aloud through default speakers."""
        if not text or not text.strip():
            return
        print(f"🔊 [Speaking]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()


# Global speaker instance
speaker = Speaker()

__all__ = ["Speaker", "speaker"]
