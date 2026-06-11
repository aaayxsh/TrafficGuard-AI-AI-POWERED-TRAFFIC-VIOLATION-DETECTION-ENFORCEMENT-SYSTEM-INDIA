"""
Detection Engine — Simulation Layer
In production, replace with real YOLOv8 inference + DeepSORT tracking + ANPR OCR.
"""
import random
from datetime import datetime

VIOLATION_TYPES = ["Over-Speeding", "Signal Jump", "No Helmet", "Wrong Side", "No Seat Belt", "Illegal Parking"]

def simulate_frame_detection(frame_idx: int) -> dict | None:
    """
    Simulates one 'batch of frames' processed by the AI pipeline.
    Returns a violation dict if detected, else None.
    """
    if random.random() < 0.40:  # ~40% detection rate per batch
        vtype = random.choice(VIOLATION_TYPES)
        return {
            "violation_type": vtype,
            "confidence": round(random.uniform(0.82, 0.99), 3),
            "bbox": [random.randint(100,400), random.randint(100,300),
                     random.randint(400,700), random.randint(300,500)],
            "track_id": random.randint(1, 50),
            "speed": random.randint(60, 185) if vtype == "Over-Speeding" else random.randint(20, 80),
            "plate_text": None,  # ANPR fills this after crop
            "frame_idx": frame_idx,
            "timestamp": datetime.now().isoformat(),
        }
    return None


def extract_plate_anpr(crop_image) -> str:
    """
    Simulates ANPR/OCR plate extraction.
    In production: use PaddleOCR or EasyOCR on the license plate crop.
    """
    states = ["UP", "DL", "MH", "HR", "RJ"]
    return f"{random.choice(states)}{random.randint(10,99)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000,9999)}"


def apply_rule_engine(detection: dict, speed_limit: int = 80) -> dict:
    """
    Applies rule-based logic on top of ML detections.
    Returns augmented detection with 'confirmed_violation' flag.
    """
    detection = detection.copy()
    vtype = detection.get("violation_type")

    if vtype == "Over-Speeding":
        detection["confirmed"] = detection.get("speed", 0) > speed_limit
    elif vtype == "Signal Jump":
        # Would check signal_state == "red" and vehicle crossed stop line
        detection["confirmed"] = True
    elif vtype == "No Helmet":
        detection["confirmed"] = detection.get("confidence", 0) > 0.85
    else:
        detection["confirmed"] = detection.get("confidence", 0) > 0.80

    return detection
