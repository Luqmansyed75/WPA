import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
RECORD_SECONDS = 4  # Duration of recording in seconds


class VoiceRecorder:
    def __init__(self, model_size: str = "base.en"):
        print("[Voice] Loading Whisper model...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.last_query = ""
        self.history = []
        print("[Voice] Ready.\n")

    def record_and_transcribe(self, duration: int = RECORD_SECONDS) -> str:
        """Waits for ENTER, records audio for specified seconds, and transcribes it."""
        input("Press [ENTER] to start speaking...")
        print(f"🎙️  Recording for {duration} seconds... Speak now!")

        # Record from microphone
        audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="float32")
        sd.wait()
        audio = audio.flatten()

        print("⚡ Transcribing...")
        segments, _ = self.model.transcribe(audio, beam_size=1)
        query = " ".join([seg.text.strip() for seg in segments]).strip()

        # Store results
        self.last_query = query
        if query:
            self.history.append(query)
            print(f"✅ Stored Query: \"{query}\"\n")
        else:
            print("⚠️  No speech recognized.\n")

        return query


if __name__ == "__main__":
    recorder = VoiceRecorder()
    try:
        while True:
            query = recorder.record_and_transcribe()
    except KeyboardInterrupt:
        print("\nStopped.")
