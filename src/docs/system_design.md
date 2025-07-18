# 🍕 Scooper Violation Detection System

## 1. System Description
The Scooper Violation Detection System is designed to monitor food handling practices in pizza stores using video feeds and detect hygiene violations, specifically:

- **Pizza Handling**
- **Using a Scooper (Allowed)**
- **Using Hands Directly (Violation)**

The system utilizes a YOLOv8-based object detection model and applies custom logic to evaluate whether the detected behavior occurs in a critical region of interest (ROI). It automatically logs violations, saves annotated images, and writes summary stats for UI display.

---

## 2. Key Features
- **Real-Time Detection** of hygiene violations.
- **Region-Based Violation Logic** using split-ROI strategy.
- **Image Logging and CSV Logging** for every detected violation.
- **Modular Message-Driven Architecture** using RabbitMQ.
- **Streamlit-Compatible Output** for UI integration.

---

## 3. ROI-Based Violation Logic

The ROI is defined as a rectangular area in the video frame that covers the pizza preparation zone. This region is **vertically split** into two subregions:

- **Left (Upper) Region**: Critical zone — violations here are counted.
- **Right (Lower) Region**: Non-critical zone — violations here are ignored.

### 💡 Custom Violation Rule:

> If a `use-hand` action is detected **inside the upper (left) region** of the ROI, it is considered a hygiene violation and logged accordingly. If the same action occurs in the lower (right) region, it is ignored.

### 📐 Diagram:
```mermaid
flowchart TD
    A[Full ROI Rectangle]
    A --> B[Left Region: Critical Zone]
    A --> C[Right Region: Non-Critical Zone]

    B -- "use-hand Detected" --> D[Log Violation]
    C -- "use-hand Detected" --> E[Ignore Violation]
