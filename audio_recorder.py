# utils/audio_recorder.py
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import time

RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

def record_audio(duration=5, fs=44100):
    """
    Records audio for a specified duration and saves it as a WAV file.
    Returns the file path.
    """
    file_path = os.path.join(RECORDINGS_DIR, "recorded_audio.wav")

    try:
        print("🎙️ Recording audio...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
        sd.wait()  # Wait until recording is finished

        # Save the recording
        write(file_path, fs, recording)
        time.sleep(1)  # small delay to ensure file is written

        # Check file size before processing
        if os.path.getsize(file_path) < 1500:
            print("⚠️ Audio too short or silent — skipping transcription.")
            return None

        print(f"✅ Audio saved: {file_path}")
        return file_path

    except Exception as e:
        print(f"❌ Error recording audio: {e}")
        return None
