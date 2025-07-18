# 🍕 Scooper Violation Detection System

## Overview
The **Scooper Violation Detection System** is a real-time computer vision solution designed to monitor hygiene protocol compliance in pizza stores. The system detects whether workers use a scooper when handling protein-based ingredients from designated Regions of Interest (ROIs). Any violation—such as directly grabbing ingredients by hand—is automatically flagged, logged, and displayed in a user-friendly interface.

## Features

- **Real-time Video Processing**: Processes video streams frame by frame
- **YOLO-based Detection**: Uses custom trained YOLO model for scooper violation detection
- **ROI Monitoring**: Monitors specific regions of interest in the video feed
- **Microservice Architecture**: Modular design with separate services for different functionalities
- **Message Queue Communication**: Uses RabbitMQ for reliable inter-service communication
- **Violation Logging**: Automatically saves violation images and logs to CSV
- **Web Dashboard**: Interactive Streamlit dashboard for real-time monitoring
- **Docker Support**: Containerized deployment with Docker Compose

## System Architecture

The system consists of three main services:

1. **Frame Reader Service** (`src/frame_reader/`): Reads video frames and publishes them to RabbitMQ
2. **Detection Service** (`src/detection_service/`): Processes frames using YOLO model and detects violations
3. **Web App** (`src/App/`): Streamlit dashboard for real-time monitoring and visualization

## Prerequisites

### Python Environment
- Python 3.10 or higher

### System Dependencies
- Docker and Docker Compose (for containerized deployment)
- RabbitMQ (if running without Docker)

## Installation

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd Scooper_Violation_Detection
```

2. **Build and run with Docker Compose**
```bash
docker-compose up --build
```


## Usage

### Running the System

1. **Start the services in order:**

```bash
# Terminal 1: Start Frame Reader
python src/frame_reader/main.py

# Terminal 2: Start Detection Service
python src/detection_service/main.py

# Terminal 3: Start Web Dashboard
streamlit run src/App/app.py
```

2. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`
   - Monitor real-time video feed and violation alerts

### Configuration

- **Video Source**: Edit `VIDEO_PATH` in `src/frame_reader/main.py`
- **ROI Settings**: Modify ROI coordinates in detection service configuration
- **Model Path**: Update YOLO model path in `src/detection_service/main.py`

## Data Structure

```
data/
├── latest.jpg              # Latest processed frame
├── violations_log.csv      # CSV log of all violations
├── violations.txt          # Text log for real-time monitoring
└── violations/            # Directory containing violation images
    ├── violation_2025-01-19_14-30-25.jpg
    └── ...
```

## Service Documentation

For detailed information about each service:

- [Frame Reader Service](docs/services/frame_reader_service.md)
- [Detection Service](docs/services/detection_service.md)
- [Web App Service](docs/services/web_app_service.md)

## Development

### Project Structure
```
src/
├── App/                   # Streamlit web dashboard
├── detection_service/     # YOLO-based detection service
├── frame_reader/         # Video frame processing service
├── model/               # YOLO model files

```
