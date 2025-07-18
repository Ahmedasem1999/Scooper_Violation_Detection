# 📹 Frame Reader Service

## Overview
The Frame Reader Service is responsible for capturing video frames from various sources (video files, cameras, or streams) and publishing them to a RabbitMQ message queue for processing by downstream services.

## Features

- **Multiple Input Sources**: Supports video files, camera feeds, and streaming URLs
- **Message Queue Integration**: Publishes frames to RabbitMQ for reliable message delivery
- **Base64 Encoding**: Encodes frames for efficient transmission over message queues
- **Error Handling**: Robust error handling for video source issues
- **Configurable Frame Rate**: Adjustable frame processing rate

## Configuration

### Environment Variables
- `RABBITMQ_HOST`: RabbitMQ server hostname (default: `localhost`)

### Configuration in Code
```python
VIDEO_PATH = "Test_Data/2.mp4"  # Video file path
QUEUE = "frames"                # RabbitMQ queue name
```

## Input Sources

### Video File
```python
VIDEO_PATH = "Test_Data/your_video.mp4"
```

## Usage

### Standalone Execution
```bash
python src/frame_reader/main.py
```

### Docker Execution
```bash
docker-compose up frame_reader
```

## Dependencies

- `opencv-python`: Video capture and frame processing
- `pika`: RabbitMQ client library
- `base64`: Frame encoding
- `json`: Message serialization

## Flow Diagram

```
Video Source → Frame Capture → Base64 Encoding → RabbitMQ Queue → Detection Service
```

## Integration

This service integrates with:
- **Detection Service**: Consumes published frames
- **RabbitMQ**: Message broker for frame distribution
- **Docker Compose**: Container orchestration

For system-wide documentation, see the [main README](../../README.md).