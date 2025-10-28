# utils/video_to_json.py
import cv2
import os
import json
import numpy as np
from datetime import datetime

# -----------------------------
# Convert recorded video into JSON summary
# -----------------------------
def video_to_json(video_path):
    """
    Extracts frames from the recorded video and analyzes simple UI changes
    (e.g., motion, color changes) to generate a lightweight JSON summary.
    """

    if not os.path.exists(video_path):
        print(f"⚠️ Video file not found: {video_path}")
        return None

    print(f"🎞️ Processing video for JSON: {video_path}")

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    summary = {
        "video_file": video_path,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fps": fps,
        "total_frames": frame_count,
        "actions_detected": []
    }

    prev_frame = None
    action_id = 1
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        movement = np.sum(thresh) / 255

        # Detect motion threshold (change between frames)
        if movement > 5000:  
            summary["actions_detected"].append({
                "id": action_id,
                "frame": frame_idx,
                "activity": f"User action detected (motion {int(movement)})"
            })
            action_id += 1

        prev_frame = gray
        frame_idx += 1

    cap.release()

    # Save JSON file
    json_dir = os.path.join("recordings", "json")
    os.makedirs(json_dir, exist_ok=True)
    json_path = os.path.join(json_dir, os.path.basename(video_path) + ".json")

    with open(json_path, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"✅ Video JSON saved: {json_path}")
    return json_path


# Example usage:
# video_to_json("recordings/screen_capture.avi")
