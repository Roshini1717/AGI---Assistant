import os
import glob

def clean_old_recordings(folder="recordings", keep_last=5):
    files = sorted(glob.glob(f"{folder}/*"), key=os.path.getmtime)
    for f in files[:-keep_last]:
        os.remove(f)
        print(f"Deleted old file: {f}")
