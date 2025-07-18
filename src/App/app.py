import streamlit as st
import time
import os
from PIL import Image
import cv2
import numpy as np
import json

# === CONFIG ===
APP_DIR = "data"
FRAME_PATH = os.path.join(APP_DIR, "latest.jpg")
VIOLATION_PATH = os.path.join(APP_DIR, "violations.txt")

# ROI definition from JSON string (replace with file later if needed)
roi_string = '{ "name": "rect", "x": 132, "y": 169, "width": 127, "height": 298 }'
roi_data = json.loads(roi_string)

# Rectangle coordinates
x1 = roi_data["x"]
y1 = roi_data["y"]
x2 = x1 + roi_data["width"]
y2 = y1 + roi_data["height"]

# === STREAMLIT UI ===
st.set_page_config(page_title="Scooper Violation Detection", layout="centered")
st.title("🍕 Pizza Store Scooper Violation Detection")

frame_placeholder = st.empty()
violation_placeholder = st.empty()
debug_placeholder = st.empty()

while True:
    debug_text = f"Looking in: {FRAME_PATH} and {VIOLATION_PATH}\n"

    if os.path.exists(FRAME_PATH):
        try:
            # Read image using OpenCV
            frame = cv2.imread(FRAME_PATH)

            # Convert to RGB and display in Streamlit
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)

            frame_resized = frame.resize((640, 640))
            frame_placeholder.image(frame_resized, caption="Live Stream with ROI", use_container_width=True)

        except Exception as e:
            debug_text += f"Error loading or drawing image: {e}\n"

    if os.path.exists(VIOLATION_PATH):
        try:
            with open(VIOLATION_PATH, "r") as f:
                violations = int(f.read())
                violation_placeholder.markdown(f"### 🚨 Violations Detected: {violations}")
        except Exception as e:
            debug_text += f" Error reading violations.txt: {e}\n"

    debug_placeholder.text(debug_text)
    time.sleep(0.5)
