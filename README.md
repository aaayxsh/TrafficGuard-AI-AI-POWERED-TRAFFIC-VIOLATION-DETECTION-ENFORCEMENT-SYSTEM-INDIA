# 🚦 TrafficGuard AI — Road Safety Violation Detection System

**AI-powered traffic violation detection & enforcement product built on Streamlit.**

Research Paper: *Road Safety: Tracking Traffic Violations in India Using AI*  
Sharda University, Dept. of Engineering & Technology, Greater Noida — 2025

---

## 🚀 Quick Start

```bash
# 1. Clone / extract the project
cd traffic_violation_system

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open browser at: **http://localhost:8501**

---

## 📁 Project Structure

```
traffic_violation_system/
├── app.py                      # Main Streamlit entry point + sidebar nav
├── requirements.txt
├── README.md
├── pages/
│   ├── dashboard.py            # KPI metrics + live charts + recent violations
│   ├── detection.py            # Live detection (upload / RTSP / demo sim)
│   ├── violations.py           # Filterable violations log + CSV export
│   ├── challan.py              # E-Challan generator (lookup + manual)
│   ├── analytics.py            # Full analytics: trends, heatmaps, model metrics
│   └── about.py                # Architecture, tech stack, references
└── utils/
    ├── data_store.py           # Session-state data management + seed data
    └── detection_engine.py     # Detection/tracking/ANPR simulation layer
```

---

## 🧠 AI Pipeline (Production)

```
CCTV Feed (RTSP/Video)
    ↓
Frame Extraction (OpenCV @ 30fps)
    ↓
Preprocessing (Noise, Brightness, Resize 640×640)
    ↓
YOLOv8 Object Detection (Vehicles, Helmets, Signals)
    ↓
Deep SORT Multi-Object Tracking (Vehicle ID across frames)
    ↓
Feature Extraction (Speed, Lane, Helmet, Signal State)
    ↓
Rule Engine (speed > limit | signal=red+cross | no helmet | wrong lane)
    ↓
ANPR / PaddleOCR (License plate crop → text)
    ↓
Violation Confirmed → DB Storage → E-Challan → Real-time Alert
    ↓
Analytics Dashboard
```

---

## 🔌 Connecting Real CCTV / Video

In `pages/detection.py`, replace the simulation section with:

```python
import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # or your fine-tuned weights

cap = cv2.VideoCapture("rtsp://user:pass@192.168.1.100:554/stream")
# or: cap = cv2.VideoCapture("path/to/video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    results = model(frame)
    # → pass to Deep SORT tracker
    # → apply rule engine
    # → run ANPR on plate crops
    # → log violations
```

---

## 🚨 Violations Detected

| Violation | Detection Method | Fine | Section |
|-----------|-----------------|------|---------|
| Over-Speeding | Virtual line time-delta | ₹2,000 | MV Act 183 |
| Signal Jump | Signal state + stop-line | ₹5,000 | MV Act 177 |
| No Helmet | Head-region CNN classifier | ₹1,000 | MV Act 129 |
| Wrong Side Driving | Lane direction vectors | ₹5,000 | MV Act 184 |
| No Seat Belt | Upper torso keypoints | ₹1,000 | MV Act 194B |
| Illegal Parking | Zone map + dwell time | ₹500 | MV Act 177 |

---

## 👥 Team

- **Ayush** — 2023420888.ayush@ug.sharda.ac.in  
- **Akhilesh Chaudhary** — 2023416222.akhilesh@ug.sharda.ac.in  
- **Mohammad Asim** (Supervisor) — er.mohdasim@gmail.com
