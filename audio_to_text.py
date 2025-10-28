# utils/audio_to_text.py
import torch
from transformers import pipeline
import os

# Load model only once (Whisper for local speech recognition)
print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")
device = 0 if torch.cuda.is_available() else -1
asr = pipeline("automatic-speech-recognition", model="openai/whisper-base", device=device)

def audio_to_text(audio_path):
    """
    Converts an audio (.wav) file into transcribed text.
    Returns recognized text or error message if audio invalid.
    """
    if not audio_path or not os.path.exists(audio_path):
        print("⚠️ No valid audio file provided.")
        return "No audio file found."

    try:
        print(f"🧩 Processing audio: {audio_path}")
        result = asr(audio_path)

        # Whisper sometimes returns text with timestamps — clean it
        text = result.get("text", "").strip()
        if not text:
            print("⚠️ No speech detected in the audio.")
            return "No clear speech detected."

        print("✅ Audio successfully transcribed.")
        return text

    except Exception as e:
        print(f"❌ Error processing audio: {e}")
        return "Error processing audio."
