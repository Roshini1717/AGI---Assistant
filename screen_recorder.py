# utils/screen_recorder.py
import pyautogui
import cv2
import numpy as np
import time
import os
from datetime import datetime

# ==============================
# 📁 Directory Setup
# ==============================
RECORDINGS_DIR = "recordings"
SCREENSHOT_DIR = os.path.join(RECORDINGS_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ==============================
# 🖼️ Single Screenshot
# ==============================
def capture_screenshot():
    """
    Capture a single screenshot and save it with timestamp.
    Returns the saved file path.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        print(f"📸 Screenshot saved: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ Error capturing screenshot: {e}")
        return None


# ==============================
# 🖼️ Screenshot Sequence
# ==============================
def record_screenshots(duration=5, interval=1):
    """
    Capture multiple screenshots over 'duration' seconds.
    """
    print("📸 Starting screenshot sequence...")
    start_time = time.time()
    count = 1

    try:
        while (time.time() - start_time) < duration:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(SCREENSHOT_DIR, f"screenshot_{count:03d}_{timestamp}.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"🖼️ Screenshot saved: {filename}")
            count += 1
            time.sleep(interval)

        print("✅ Screenshot sequence completed!")
    except Exception as e:
        print(f"❌ Error during screenshot recording: {e}")


# ==============================
# 🎥 Screen Video Recording
# ==============================
def record_screen(duration=5, fps=10):
    """
    Record the screen for a given duration (in seconds) and save as .avi video.
    Returns the output video file path.
    """
    print("🎥 Starting screen recording...")
    try:
        screen_size = pyautogui.size()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(RECORDINGS_DIR, f"screen_capture_{timestamp}.avi")

        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, fps, screen_size)

        start_time = time.time()
        frame_count = 0

        while (time.time() - start_time) < duration:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            frame_count += 1

        out.release()
        print(f"✅ Screen recording saved ({frame_count} frames): {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Error recording screen: {e}")
        return None
