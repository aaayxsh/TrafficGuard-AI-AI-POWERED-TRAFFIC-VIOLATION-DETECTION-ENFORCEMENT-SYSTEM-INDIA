import streamlit as st
import time
import random
from datetime import datetime
from utils.detection_engine import simulate_frame_detection
from utils.data_store import add_violation

VIOLATION_TYPES = ["Over-Speeding", "Signal Jump", "No Helmet", "Wrong Side", "No Seat Belt", "Illegal Parking"]
LOCATIONS = [
    "NH-24 Ghaziabad", "Sector-18 Noida", "Rajnagar Intersection",
    "DND Flyway", "Expressway Toll Plaza", "Connaught Place Jn.",
    "Karol Bagh Signal", "NH-58 Meerut Road"
]

def generate_plate():
    states = ["UP", "DL", "MH", "HR", "RJ", "GJ", "KA", "TN"]
    return f"{random.choice(states)}{random.randint(10,99)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000,9999)}"

def fine_for(vtype):
    fines = {
        "Over-Speeding": 2000, "Signal Jump": 5000,
        "No Helmet": 1000, "Wrong Side": 5000,
        "No Seat Belt": 1000, "Illegal Parking": 500
    }
    return fines.get(vtype, 1000)

def show():
    st.markdown("<div class='main-header'>🎥 Live Violation Detection</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>REAL-TIME AI ANALYSIS · YOLOv8 + DEEP SORT + ANPR</div>", unsafe_allow_html=True)

    # ── Camera Config ─────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        source = st.selectbox("📷 Camera / Input Source", [
            "Upload Video File", "RTSP Stream (Live CCTV)",
            "Webcam (Local)", "Demo Simulation Mode"
        ])
    with col2:
        location = st.selectbox("📍 Camera Location", LOCATIONS)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        start = st.button("▶ Start Detection")

    st.markdown("---")

    if source == "Upload Video File":
        uploaded = st.file_uploader("Upload Traffic Video", type=["mp4", "avi", "mov", "mkv"])
        if uploaded:
            st.video(uploaded)
            st.info("⚡ In production, this video would be processed frame-by-frame through YOLOv8 for violation detection.")
        else:
            _show_placeholder_camera()

    elif source == "RTSP Stream (Live CCTV)":
        rtsp = st.text_input("Enter RTSP URL", placeholder="rtsp://username:password@192.168.1.100:554/stream")
        if rtsp:
            st.info(f"📡 Connecting to: `{rtsp}`")
            st.warning("RTSP streams require OpenCV backend running on server. Use Demo Mode in this environment.")
        _show_placeholder_camera()

    elif source == "Webcam (Local)":
        st.warning("⚠️ Webcam access requires browser permissions and local deployment.")
        _show_placeholder_camera()

    else:  # Demo Simulation
        _run_demo_simulation(location, start)


def _show_placeholder_camera():
    st.markdown("""
    <div style='background: #0d1117; border: 2px dashed #333; border-radius: 12px;
                height: 320px; display: flex; flex-direction: column;
                align-items: center; justify-content: center; color: #444; margin: 1rem 0;'>
        <div style='font-size: 3rem;'>📷</div>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1.2rem; margin-top: 0.5rem;'>Camera Feed</div>
        <div style='font-size: 0.8rem; margin-top: 0.3rem;'>No active stream</div>
    </div>
    """, unsafe_allow_html=True)


def _run_demo_simulation(location, start):
    st.markdown("""
    <div style='background: linear-gradient(135deg,#0d1117,#1a1a2e); border: 1px solid #FF4B2B33;
                border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;'>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1rem; color: #FF4B2B; margin-bottom: 0.5rem;'>
            ⚙️ DEMO SIMULATION MODE
        </div>
        <div style='font-size: 0.85rem; color: #999;'>
            Simulates the AI detection pipeline (YOLOv8 → SORT → ANPR → Rule Engine → E-Challan).
            In production, connect real CCTV feeds via RTSP or video upload.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI Pipeline Visual
    st.markdown("### 🔄 AI Detection Pipeline")
    steps = [
        ("1. Frame Capture", "CCTV feed → Frame extraction @ 30fps", "#FF4B2B"),
        ("2. Preprocessing", "Noise removal · Brightness normalization · Resize to 640×640", "#FF7043"),
        ("3. YOLOv8 Detection", "Vehicle · Helmet · Traffic Signal object detection", "#FFA500"),
        ("4. Deep SORT Tracking", "Multi-object tracking across frames · Vehicle ID assignment", "#FFD700"),
        ("5. Rule Engine", "Speed check · Signal state · Helmet presence · Lane direction", "#66BB6A"),
        ("6. ANPR / OCR", "License plate crop → PaddleOCR → Number plate extraction", "#6495ED"),
        ("7. E-Challan", "Violation logged → Fine computed → Challan generated → Alert sent", "#AB47BC"),
    ]
    cols = st.columns(7)
    for col, (title, desc, color) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style='background:#111; border: 1px solid {color}44; border-radius:8px;
                        padding:0.7rem 0.5rem; text-align:center; height:120px;'>
                <div style='color:{color}; font-family:Rajdhani,sans-serif; font-size:0.85rem; font-weight:700;'>{title}</div>
                <div style='font-size:0.7rem; color:#777; margin-top:0.4rem; line-height:1.3;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if start:
        st.markdown("### 🚨 Live Detection Feed")
        feed_placeholder = st.empty()
        detection_placeholder = st.empty()
        log_placeholder = st.empty()

        detections_log = []

        for i in range(20):
            # Simulate a detection event
            detected = random.random() > 0.35  # 65% chance of violation per "frame batch"

            with feed_placeholder.container():
                _render_fake_camera_feed(i, detected)

            if detected:
                vtype = random.choice(VIOLATION_TYPES)
                plate = generate_plate()
                speed = random.randint(60, 180) if vtype == "Over-Speeding" else random.randint(20, 80)
                confidence = round(random.uniform(0.82, 0.99), 2)
                fine = fine_for(vtype)
                ts = datetime.now().strftime("%H:%M:%S")

                # Save to store
                add_violation({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "plate": plate,
                    "violation_type": vtype,
                    "location": location,
                    "speed": speed,
                    "fine": fine,
                    "confidence": confidence,
                    "status": "Pending"
                })

                detections_log.insert(0, (ts, plate, vtype, speed, confidence, fine))
                detections_log = detections_log[:8]

                with detection_placeholder.container():
                    st.success(f"🚨 **VIOLATION DETECTED** — `{plate}` — **{vtype}** — Confidence: {confidence*100:.0f}%")

            with log_placeholder.container():
                if detections_log:
                    st.markdown("**📋 Session Detection Log**")
                    for ts, plate, vtype, speed, conf, fine in detections_log:
                        cols = st.columns([1, 1.5, 2, 1, 1, 1])
                        cols[0].markdown(f"<span style='color:#666;font-size:0.82rem;'>{ts}</span>", unsafe_allow_html=True)
                        cols[1].markdown(f"<span style='color:#FF4B2B;font-family:monospace;font-weight:700;'>{plate}</span>", unsafe_allow_html=True)
                        cols[2].markdown(f"<span style='font-size:0.85rem;'>{vtype}</span>", unsafe_allow_html=True)
                        cols[3].markdown(f"<span style='font-size:0.82rem;'>{speed} km/h</span>", unsafe_allow_html=True)
                        cols[4].markdown(f"<span style='color:#66BB6A;font-size:0.82rem;'>{conf*100:.0f}%</span>", unsafe_allow_html=True)
                        cols[5].markdown(f"<span style='color:#FFD700;font-weight:700;'>₹{fine}</span>", unsafe_allow_html=True)

            time.sleep(0.6)

        st.balloons()
        st.success("✅ Demo simulation complete! Check Violations Log and E-Challan tabs.")
    else:
        st.info("👆 Click **▶ Start Detection** to begin the demo simulation.")


def _render_fake_camera_feed(frame_idx, detected):
    color = "#FF4B2B" if detected else "#333"
    label = "⚠ VIOLATION" if detected else "● MONITORING"
    lcolor = "#FF4B2B" if detected else "#66BB6A"
    st.markdown(f"""
    <div style='background: #070d14; border: 2px solid {color}; border-radius: 12px;
                height: 200px; display: flex; flex-direction: column;
                align-items: center; justify-content: center; position: relative;
                transition: border-color 0.3s;'>
        <div style='font-size: 2.5rem;'>🛣️</div>
        <div style='font-family: monospace; font-size: 0.8rem; color: #444; margin-top: 0.5rem;'>
            FRAME #{frame_idx*30 + random.randint(1,30):06d} · 1920×1080 · 30fps
        </div>
        <div style='position:absolute; top:10px; left:12px; font-size:0.7rem;
                    color:{lcolor}; font-family:Rajdhani,sans-serif; font-weight:700;'>
            {label}
        </div>
        <div style='position:absolute; top:10px; right:12px; font-size:0.7rem; color:#444; font-family:monospace;'>
            YOLOv8 · DeepSORT · ANPR
        </div>
        <div style='position:absolute; bottom:10px; right:12px; font-size:0.7rem; color:#333; font-family:monospace;'>
            {datetime.now().strftime('%H:%M:%S.%f')[:12]}
        </div>
    </div>
    """, unsafe_allow_html=True)
