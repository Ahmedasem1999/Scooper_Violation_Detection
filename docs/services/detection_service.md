# 🔍 Detection Service

## Overview
The Detection Service is the core component of the Scooper Violation Detection System. It processes video frames using a custom-trained YOLO model to detect violations of hygiene protocols, specifically monitoring whether workers use scooper tools when handling protein ingredients within designated regions of interest (ROIs).

## Features

- **YOLO-based Detection**: Uses Ultralytics YOLO for real-time object detection
- **Custom Model**: Trained specifically for scooper violation detection
- **ROI Monitoring**: Analyzes violations only within specified regions
- **Automatic Logging**: Saves violation images and metadata to files and CSV
- **Real-time Processing**: Processes frames from RabbitMQ queue continuously
- **Violation Tracking**: Maintains logs with timestamps and violation details

## Architecture

```
RabbitMQ Queue → Frame Processing → YOLO Detection → ROI Analysis → Violation Logging
```

## Configuration

### Environment Variables
- `RABBITMQ_HOST`: RabbitMQ server hostname (default: `localhost`)

### Key Configuration Parameters
```python
model = YOLO("src/model/best.pt")  # YOLO model path
QUEUE = "frames"                    # Input queue name
OUTPUT_DIR = "data"                 # Output directory
VIOLATION_IMG_DIR = "data/violations"  # Violation images directory
LOG_FILE = "data/violations_log.csv"   # CSV log file

# ROI Definition
ROI_RECT = {
    "name": "rect",
    "x": 132,           # Top-left X coordinate
    "y": 169,           # Top-left Y coordinate
    "width": 127,       # Rectangle width
    "height": 298       # Rectangle height
}
```

## Model Information

### YOLO Model
- **Model File**: `src/model/best.pt`
- **Framework**: Ultralytics YOLO
- **Classes**: Custom trained for scooper violation detection
- **Input Size**: Configurable (default: 640x640)

### Detection Classes
The model is trained to detect:
- Workers/hands in ROI
- Scooper tools
- Direct hand contact with ingredients (violations)

## ROI (Region of Interest)

### Rectangle ROI
The system monitors a rectangular region defined by:
- **Position**: (x, y) coordinates of top-left corner
- **Dimensions**: Width and height in pixels
- **Purpose**: Focus detection on ingredient handling areas

### ROI Configuration
```python
# Example ROI configuration for ingredient station
ROI_RECT = {
    "name": "rect",
    "x": 132,       # Pixel coordinates
    "y": 169,
    "width": 127,
    "height": 298
}
```

### Line-Based Violation Detection
The system implements a sophisticated line-based detection mechanism within the ROI rectangle:

- **Detection Line**: A horizontal line is defined within the ROI rectangle
- **Above Line**: Violations detected above this line are considered **valid violations**
- **Below Line**: Violations detected below this line are **ignored/not considered as violations**
- **Purpose**: This line-based approach helps filter out false positives and focuses on the critical ingredient handling zone

```python
# Line-based detection configuration
DETECTION_LINE_Y = roi_data["y"] + (roi_data["height"] * 0.6)  # 60% down from top
# Only violations above this Y-coordinate are considered valid
```

## Violation Detection Logic

### Detection Process
1. **Frame Decoding**: Converts base64 frame to OpenCV format
2. **YOLO Inference**: Runs detection on the frame
3. **ROI Filtering**: Checks if violations occur within ROI
4. **Violation Assessment**: Determines if detected objects constitute a violation
5. **Logging**: Records violations with timestamps and images

### Violation Criteria
A violation is detected when:
- Human hand/worker is detected in ROI
- No scooper tool is detected in the same region
- Confidence threshold is met for both detections
- **Line Position Check**: The detected violation occurs **above** the detection line within the ROI
  - Violations above the line = **Valid violations** (logged and reported)
  - Violations below the line = **Ignored** (not considered violations)

## Output Data

### Violation Images
- **Location**: `data/violations/`
- **Format**: `violation_YYYY-MM-DD_HH-MM-SS.jpg`
- **Content**: Original frame with detection annotations

### CSV Log Format
```csv
timestamp,violation_type,roi_name,image_path,confidence
2025-01-19 14:30:25,scooper_violation,rect,violations/violation_2025-01-19_14-30-25.jpg,0.85
```

### Real-time Status
- **File**: `data/violations.txt`
- **Content**: Latest violation information for UI display

## Message Processing

### Input Message Format
```json
{
    "frame": "base64_encoded_image_data"
}
```

### Processing Pipeline
1. **Queue Consumption**: Reads frames from RabbitMQ
2. **Image Decoding**: Converts base64 to numpy array
3. **Model Inference**: Processes frame through YOLO model
4. **Result Analysis**: Evaluates detections against violation criteria
5. **Output Generation**: Saves results and updates status files

## Usage

### Standalone Execution
```bash
python src/detection_service/main.py
```

### Docker Execution
```bash
docker-compose up detection_service
```

### Development Mode
```bash
# With debug output
PYTHONPATH=. python src/detection_service/main.py
```

## Dependencies

### Core Libraries
- `ultralytics`: YOLO model framework
- `opencv-python`: Image processing
- `pika`: RabbitMQ client
- `numpy`: Numerical computations

### Additional Libraries
- `datetime`: Timestamp handling
- `csv`: Log file management
- `base64`: Image encoding/decoding
- `json`: Message parsing

For system-wide documentation, see the [main README](../../README.md).