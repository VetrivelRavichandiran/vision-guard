# VisionGuard 👁️🛡️

VisionGuard is a professional Python desktop application for real-time visual ergonomics, eye-closure monitoring, and fatigue prevention using PySide6, OpenCV, and MediaPipe.

> **Disclaimer:** VisionGuard provides non-diagnostic observations about eye closure, viewing posture, and lighting conditions. It is not a diagnostic medical device.

## Features
* **Live Webcam Analytics**: Real-time Eye Aspect Ratio (EAR), blink duration, and PERCLOS calculation.
* **Ergonomic Monitoring**: Head posture (pitch/yaw/roll) and environment lighting analysis.
* **Interactive Screenings**: Tumbling-E visual screening test engine.
* **Data & Reports**: SQLite session history storage and ReportLab PDF report generation.

## Installation & Running

```bash
# Create virtual environment (Python 3.10 to 3.12 recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode
pip install -e .

# Run application
visionguard