# 🌐 Web App - Scooper Violation Monitoring Dashboard

## Overview
The Web App is a Streamlit-based dashboard that provides real-time monitoring and visualization of the Scooper Violation Detection System. It displays live video feeds, violation alerts, and system status information in an intuitive web interface.

## Features

- **Real-time Video Display**: Shows live processed frames with ROI visualization
- **Violation Alerts**: Displays immediate notifications when violations are detected
- **ROI Visualization**: Overlays region of interest boundaries on video feed
- **Status Monitoring**: Shows system health and connection status
- **Responsive Design**: Clean, modern interface optimized for monitoring stations

## User Interface

### Main Dashboard Components

1. **Video Feed Section**
   - Live video stream with ROI overlay
   - Frame resize for optimal display (640x640)
   - Real-time frame updates

2. **Violation Alert Section**
   - Latest violation information
   - Timestamp and violation details
   - Visual alert indicators

## Configuration

### Application Settings
```python
APP_DIR = "data"                           # Data directory
FRAME_PATH = "data/latest.jpg"             # Latest frame file
VIOLATION_PATH = "data/violations.txt"     # Violation status file

# ROI Configuration (matches detection service)
roi_string = '{ "name": "rect", "x": 132, "y": 169, "width": 127, "height": 298 }'
```

### Streamlit Configuration
```python
st.set_page_config(
    page_title="Scooper Violation Detection",
    layout="centered"
)
```

## Configuration Options

### Display Settings
```python
# Frame display configuration
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 640
REFRESH_INTERVAL = 1.0  # seconds

# ROI visualization
ROI_COLOR = (0, 255, 0)  # Green
ROI_THICKNESS = 2
```

## Data Sources

### Input Files
- **Latest Frame**: `data/latest.jpg` - Current processed video frame
- **Violation Log**: `data/violations.txt` - Real-time violation status
- **Violation Images**: `data/violations/` - Historical violation images

### Data Format
```
# violations.txt format
Violation detected at 2025-01-19 14:30:25 in rect region
```

## User Interface Elements

### Header
```python
st.title("🍕 Pizza Store Scooper Violation Detection")
```

### Video Display
- **Frame Source**: Latest processed frame from detection service
- **ROI Overlay**: Visual rectangle showing monitored region
- **Auto-resize**: Consistent 640x640 display size
- **Refresh Rate**: Real-time updates (approximately 1-2 seconds)

### Violation Alerts
- **Alert Box**: Prominent violation notifications
- **Timestamp**: When the violation occurred
- **Location**: Which ROI detected the violation
- **Status**: Current system state

## Technical Implementation

### Core Loop
```python
while True:
    # Load and display latest frame
    if os.path.exists(FRAME_PATH):
        frame = cv2.imread(FRAME_PATH)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_resized)
    
    # Check for violations
    if os.path.exists(VIOLATION_PATH):
        with open(VIOLATION_PATH, 'r') as f:
            violation_text = f.read()
        violation_placeholder.error(violation_text)
    
    time.sleep(1)  # Refresh rate
```

### Image Processing
- **Color Conversion**: BGR to RGB for Streamlit display
- **Resize**: Maintains aspect ratio while standardizing size
- **ROI Drawing**: Overlays detection region rectangle

## ROI Visualization

### Rectangle Drawing
```python
# ROI coordinates from JSON configuration
x1, y1 = roi_data["x"], roi_data["y"]
x2, y2 = x1 + roi_data["width"], y1 + roi_data["height"]

# Visual overlay on video feed
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
```

### Visual Indicators
- **Green Rectangle**: Normal monitoring region
- **Red Rectangle**: Active violation area (future enhancement)