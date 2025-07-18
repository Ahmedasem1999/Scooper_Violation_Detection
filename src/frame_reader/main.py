import cv2
import pika
import base64
import json
import time
import os

"""
Here you can pass the the video py passing it's lochation or using url or camera index.
"""

VIDEO_PATH = "Test_Data/2.mp4"
QUEUE = "frames"

rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")

# Connect to RabbitMQ
while True:
    try:
        conn = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        channel = conn.channel()
        break
    except pika.exceptions.AMQPConnectionError:
        print("Waiting for RabbitMQ...")
        time.sleep(2)

channel.queue_declare(queue=QUEUE)

cap = cv2.VideoCapture(VIDEO_PATH)

# Read video frames until it ends
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Video finished. Exiting...")
        break
    _, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer).decode('utf-8')
    payload = json.dumps({"frame": encoded_frame})
    channel.basic_publish(exchange='', routing_key=QUEUE, body=payload)
    time.sleep(0.1)

cap.release()
conn.close()
