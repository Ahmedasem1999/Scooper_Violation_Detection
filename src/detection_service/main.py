from ultralytics import YOLO
import pika
import base64
import json
import cv2
import numpy as np
import os
import time
from datetime import datetime
import csv

"""
Scooper Violation Detection Service
This service reads frames from a video stream, detects violations using a YOLO model,
and logs violations with images and metadata.
"""

# === CONFIG ===
model = YOLO("src/model/best.pt")
QUEUE = "frames"
OUTPUT_DIR = "data"
VIOLATION_IMG_DIR = os.path.join(OUTPUT_DIR, "violations")
LOG_FILE = os.path.join(OUTPUT_DIR, "violations_log.csv")

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")

# Create directories if not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VIOLATION_IMG_DIR, exist_ok=True)

# RabbitMQ Connection
while True:
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        channel = conn.channel()
        channel.queue_declare(queue=QUEUE)
        break
    except pika.exceptions.AMQPConnectionError:
        print("Waiting for RabbitMQ...")
        time.sleep(2)

# === ROI: Rectangle Definition ===
ROI_RECT = {
    "name": "rect",
    "x": 132,
    "y": 169,
    "width": 127,
    "height": 298
}

# Vertical split position
SPLIT_RATIO = 0.52

# Compute bounding box corners
x1 = ROI_RECT["x"]
y1 = ROI_RECT["y"]
x2 = x1 + ROI_RECT["width"]
y2 = y1 + ROI_RECT["height"]

# Calculate the split line x-coordinate
split_x = x1 + int(ROI_RECT["width"] * SPLIT_RATIO)

def is_inside_upper_roi(x, y):
    """Check if point is in the upper region (left of the split line)"""
    return x1 <= x <= split_x and y1 <= y <= y2

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        frame_data = base64.b64decode(data["frame"])
        frame = cv2.imdecode(np.frombuffer(frame_data, np.uint8), 1)

        # Resize for model input and consistent output
        frame_resized = cv2.resize(frame, (640, 640))
        results = model(frame_resized)

        violations = 0
        result = results[0]

        if result.boxes is not None:
            for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                x1_box, y1_box, x2_box, y2_box = map(int, box)
                label = model.names[int(cls)]

                if label == "use-hand":
                    cx = (x1_box + x2_box) // 2
                    cy = (y1_box + y2_box) // 2

                    # Check if the center is in the upper region (left of split line)
                    if is_inside_upper_roi(cx, cy):
                        violations += 1

                        # Draw red box for violation
                        cv2.rectcv2angle(frame_resized, (x1_box, y1_box), (x2_box, y2_box), (0, 0, 255), 2)
                        cv2.putText(frame_resized, "VIOLATION", (x1_box, y1_box - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                        # Save violation image with timestamp
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        violation_frame_path = os.path.join(
                            VIOLATION_IMG_DIR, f"violation_{timestamp}.jpg")
                        cv2.imwrite(violation_frame_path, frame_resized)

                        # Append to CSV log
                        log_fields = ['timestamp', 'frame_path', 'label', 'bbox']
                        file_exists = os.path.exists(LOG_FILE)
                        with open(LOG_FILE, 'a', newline='') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=log_fields)
                            if not file_exists:
                                writer.writeheader()
                            writer.writerow({
                                'timestamp': timestamp,
                                'frame_path': violation_frame_path,
                                'label': label,
                                'bbox': f"[{x1_box},{y1_box},{x2_box},{y2_box}]"
                            })

        # Draw ROI box in green
        cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Draw the italicized split line
        tilt_angle = -4 
        tilt_pixels = int((y2 - y1) * np.tan(np.radians(tilt_angle)))  # Calculate horizontal offset
        cv2.line(frame_resized, (split_x, y1), (split_x + tilt_pixels, y2), (255, 0, 0), 2)
        
        # Save current frame for Streamlit UI
        cv2.imwrite(os.path.join(OUTPUT_DIR, "latest.jpg"), frame_resized)

        # Write current violation count
        with open(os.path.join(OUTPUT_DIR, "violations.txt"), "w") as f:
            f.write(str(violations))

    except Exception as e:
        print(f"[Detection Error] {e}")

channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)
print("[Detection] Waiting for frames...")
channel.start_consuming()