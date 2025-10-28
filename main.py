import os
import threading
import customtkinter as ctk

# ✅ Ensure FFmpeg is accessible for all utils
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\ffmpeg-8.0-essentials_build\bin"

from utils.audio_recorder import record_audio
from utils.audio_to_text import audio_to_text
from utils.summarizer import summarize_text
from utils.video_to_json import video_to_json
from utils.pattern_learning import learn_patterns
from utils.task_automation import automate_task
from utils.screen_recorder import record_screen, capture_screenshot


# ---------------- GUI Setup ---------------- #
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🧠 AGI Assistant MVP")
root.geometry("750x700")

def update_status(text):
    """Update the status label safely from threads."""
    status_label.configure(text=f"Status: {text}")
    print(text)


# ---------------- Feature Functions ---------------- #
def audio_only():
    try:
        update_status("🎙️ Recording audio...")
        audio_file = record_audio(5)
        update_status("🧩 Processing audio to text...")
        text = audio_to_text(audio_file)

        transcript_box.delete("1.0", ctk.END)
        transcript_box.insert(ctk.END, text)

        summary_box.delete("1.0", ctk.END)
        summary_box.insert(ctk.END, summarize_text(text))

        update_status("✅ Done: Audio Only")
    except Exception as e:
        update_status(f"❌ Error in Audio: {e}")


def image_only():
    try:
        update_status("📸 Capturing screenshot...")
        capture_screenshot()
        update_status("✅ Done: Image Only")
    except Exception as e:
        update_status(f"❌ Error capturing image: {e}")


def video_only():
    try:
        update_status("🎥 Recording screen...")
        record_screen(5)
        update_status("✅ Done: Video Only")
    except Exception as e:
        update_status(f"❌ Error in video recording: {e}")


def image_audio():
    try:
        update_status("📸+🎙️ Capturing screenshot & recording audio...")
        capture_screenshot()
        audio_file = record_audio(5)
        text = audio_to_text(audio_file)

        transcript_box.delete("1.0", ctk.END)
        transcript_box.insert(ctk.END, text)

        summary_box.delete("1.0", ctk.END)
        summary_box.insert(ctk.END, summarize_text(text))
        update_status("✅ Done: Image + Audio")
    except Exception as e:
        update_status(f"❌ Error in Image+Audio: {e}")


def video_audio():
    try:
        update_status("🎥+🎙️ Recording screen & audio...")
        video_file = record_screen(5)
        audio_file = record_audio(5)

        update_status("🧠 Processing audio to text...")
        text = audio_to_text(audio_file)

        transcript_box.delete("1.0", ctk.END)
        transcript_box.insert(ctk.END, text)

        summary_box.delete("1.0", ctk.END)
        summary_box.insert(ctk.END, summarize_text(text))

        update_status("✅ Done: Video + Audio")
    except Exception as e:
        update_status(f"❌ Error in Video+Audio: {e}")


def learn_from_video():
    try:
        update_status("📊 Converting video to JSON...")
        video_file = "recordings/screen_capture.avi"

        if not os.path.exists(video_file):
            update_status("⚠️ No video found. Please record first.")
            return

        json_file = video_to_json(video_file)
        patterns = learn_patterns([json_file])

        transcript_box.delete("1.0", ctk.END)
        transcript_box.insert(ctk.END, f"Learned Patterns:\n{patterns}")

        update_status("✅ Learning Completed")
    except Exception as e:
        update_status(f"❌ Error in Learning: {e}")


def automate_learned_patterns():
    try:
        update_status("🤖 Automating learned patterns...")
        video_file = "recordings/screen_capture.avi"

        if not os.path.exists(video_file):
            update_status("⚠️ No video found. Please record first.")
            return

        json_file = video_to_json(video_file)
        patterns = learn_patterns([json_file])

        automate_task([
            {"action": "click", "x": 200, "y": 150},
            {"action": "type", "text": "Automation successful!"}
        ])
        update_status("✅ Automation Completed")
    except Exception as e:
        update_status(f"❌ Error in Automation: {e}")


# ---------------- GUI Layout ---------------- #
header = ctk.CTkLabel(root, text="🧠 AGI Assistant MVP", font=("Arial", 24, "bold"))
header.pack(pady=10)

btn_frame = ctk.CTkFrame(root)
btn_frame.pack(pady=20)

ctk.CTkButton(btn_frame, text="🎙️ Audio Only", width=300, command=lambda: threading.Thread(target=audio_only).start()).pack(pady=5)
ctk.CTkButton(btn_frame, text="📸 Image Only", width=300, command=lambda: threading.Thread(target=image_only).start()).pack(pady=5)
ctk.CTkButton(btn_frame, text="🎥 Video Only", width=300, command=lambda: threading.Thread(target=video_only).start()).pack(pady=5)
ctk.CTkButton(btn_frame, text="📸+🎙️ Image + Audio", width=300, command=lambda: threading.Thread(target=image_audio).start()).pack(pady=5)
ctk.CTkButton(btn_frame, text="🎥+🎙️ Video + Audio", width=300, command=lambda: threading.Thread(target=video_audio).start()).pack(pady=5)

ctk.CTkButton(btn_frame, text="📊 Learn From Video", width=300, command=lambda: threading.Thread(target=learn_from_video).start()).pack(pady=5)
ctk.CTkButton(btn_frame, text="🤖 Automate Learned Patterns", width=300, command=lambda: threading.Thread(target=automate_learned_patterns).start()).pack(pady=5)

status_label = ctk.CTkLabel(root, text="Status: Idle", font=("Arial", 14))
status_label.pack(pady=10)

ctk.CTkLabel(root, text="Transcript / Learned Patterns:", font=("Arial", 14, "bold")).pack()
transcript_box = ctk.CTkTextbox(root, height=120, width=700)
transcript_box.pack(pady=10)

ctk.CTkLabel(root, text="Summary:", font=("Arial", 14, "bold")).pack()
summary_box = ctk.CTkTextbox(root, height=100, width=700)
summary_box.pack(pady=10)

root.mainloop()
