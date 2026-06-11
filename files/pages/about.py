import streamlit as st

def show():
    st.markdown("<div class='main-header'>ℹ️ About TrafficGuard AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>RESEARCH PROJECT · SHARDA UNIVERSITY · DEPT. OF ENGINEERING & TECHNOLOGY</div>", unsafe_allow_html=True)

    # Project info
    st.markdown("""
    <div style='background: linear-gradient(135deg,#1a1a2e,#16213e); border:1px solid #0f3460;
                border-radius:12px; padding:1.5rem; margin-bottom:1.5rem;'>
        <div style='font-family:Rajdhani,sans-serif; font-size:1.4rem; font-weight:700; color:#FF4B2B; margin-bottom:0.5rem;'>
            Road Safety: Tracking Traffic Violations in India Using AI
        </div>
        <div style='font-size:0.9rem; color:#aaa; line-height:1.7;'>
            An AI-powered automated system to detect, log and enforce traffic violations in real-time
            using deep learning (YOLOv8), multi-object tracking (Deep SORT), and Automatic Number Plate
            Recognition (ANPR/OCR). The system generates automated e-challans, sends real-time alerts
            and provides actionable analytics to traffic authorities.
        </div>
        <div style='margin-top:1rem; font-size:0.82rem; color:#666;'>
            Authors: Ayush · Akhilesh Chaudhary · Mohammad Asim (Supervisor)<br>
            Greater Noida, Uttar Pradesh, India — 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pipeline
    st.subheader("🔄 System Architecture & Pipeline")
    steps = [
        ("📷", "Data Collection", "High-resolution CCTV cameras at toll plazas, intersections, accident-prone zones. Captures day/night, peak/off-peak, multi-vehicle type footage."),
        ("🔗", "Data Fusion", "Temporal fusion across frames + vehicle-signal state fusion + Deep SORT tracking to maintain vehicle identity across the video."),
        ("🛠️", "Preprocessing", "Noise removal (OpenCV), brightness/contrast normalization, frame resize to 640×640, shadow removal to improve detection robustness."),
        ("🔍", "Feature Extraction", "Vehicle bounding boxes, helmet region crops, speed displacement vectors, lane marking detection, direction vectors."),
        ("🧠", "Model Training", "YOLOv8 for real-time object detection · CNN/ResNet for classification · Deep SORT for tracking · Random Forest/Gradient Boosting for decision reliability."),
        ("📏", "Rule Engine", "Speed > limit → Over-speeding | Signal = red & vehicle crosses → Signal jump | No helmet on two-wheeler | Wrong lane direction → Wrong side driving"),
        ("✅", "Validation", "Ground-truth annotated videos, Precision/Recall/F1 metrics, false positive/negative analysis, model retraining loop."),
        ("⚡", "Integration", "Centralized DB storage → ANPR OCR plate extraction → E-Challan generation → Real-time alerts → Analytics dashboard"),
    ]
    for i, (icon, title, desc) in enumerate(steps):
        col_num, col_content = st.columns([0.3, 9.7])
        col_num.markdown(f"<div style='background:#FF4B2B; color:#fff; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.75rem; margin-top:0.5rem;'>{i+1}</div>", unsafe_allow_html=True)
        with col_content:
            st.markdown(f"""
            <div class='pipeline-step'>
                <div class='pipeline-step-title'>{icon} {title}</div>
                <div style='font-size:0.85rem; color:#aaa; line-height:1.5;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tech Stack
    st.markdown("---")
    st.subheader("🛠️ Technology Stack")
    techs = [
        ("🧠 YOLOv8", "Ultralytics", "Real-time object detection"),
        ("🔍 Deep SORT", "Object Tracking", "Multi-frame vehicle tracking"),
        ("🔤 PaddleOCR", "ANPR", "License plate text extraction"),
        ("📊 OpenCV", "Computer Vision", "Frame processing & analysis"),
        ("🌲 Random Forest", "Scikit-learn", "Violation classification"),
        ("🚀 Streamlit", "Frontend", "Dashboard & product UI"),
        ("🗄️ SQLite/DB", "Storage", "Violation records & challans"),
        ("📡 RTSP", "Streaming", "Live CCTV feed integration"),
    ]
    cols = st.columns(4)
    for i, (name, cat, desc) in enumerate(techs):
        with cols[i % 4]:
            st.markdown(f"""
            <div style='background:#111; border:1px solid #1a1a2e; border-radius:10px;
                        padding:1rem; margin:0.4rem 0; text-align:center;'>
                <div style='font-size:1.6rem; margin-bottom:0.3rem;'>{name.split()[0]}</div>
                <div style='font-family:Rajdhani,sans-serif; font-weight:700; color:#FF4B2B; font-size:0.95rem;'>{name.split(" ",1)[1]}</div>
                <div style='font-size:0.75rem; color:#666; margin-top:0.2rem;'>{cat} · {desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # Violations Detected
    st.markdown("---")
    st.subheader("🚨 Violations Detected")
    violations = [
        ("🔴", "Over-Speeding", "Speed exceeds road limit. Detected via virtual line crossing time delta.", "₹2,000", "MV Act Sec. 183"),
        ("🟠", "Signal Jump", "Vehicle crosses stop-line on red. Traffic signal state fused with detection.", "₹5,000", "MV Act Sec. 177"),
        ("🟡", "No Helmet", "Rider on two-wheeler without helmet. Head region CNN classifier.", "₹1,000", "MV Act Sec. 129"),
        ("🔴", "Wrong Side Driving", "Vehicle direction ≠ lane direction. Lane marking + direction vectors.", "₹5,000", "MV Act Sec. 184"),
        ("🟡", "No Seat Belt", "Driver/passenger without seat belt. Upper torso keypoint analysis.", "₹1,000", "MV Act Sec. 194B"),
        ("🔵", "Illegal Parking", "Stationary vehicle in no-parking zone. Zone map + dwell time.", "₹500", "MV Act Sec. 177"),
    ]
    for dot, name, how, fine, section in violations:
        col_a, col_b, col_c, col_d = st.columns([0.3, 2.5, 4, 2])
        col_a.markdown(f"<div style='font-size:1.2rem; margin-top:0.4rem;'>{dot}</div>", unsafe_allow_html=True)
        col_b.markdown(f"<span style='font-family:Rajdhani,sans-serif; font-weight:700; font-size:1rem; color:#eee;'>{name}</span>", unsafe_allow_html=True)
        col_c.markdown(f"<span style='font-size:0.83rem; color:#888;'>{how}</span>", unsafe_allow_html=True)
        col_d.markdown(f"<span style='color:#66BB6A; font-weight:700;'>{fine}</span> <span style='color:#444; font-size:0.78rem;'>· {section}</span>", unsafe_allow_html=True)

    # References
    st.markdown("---")
    st.subheader("📚 Key References")
    refs = [
        "Robles-Serrano et al., 2021 — Traffic Accident Detection Using CNN (IEEE Access)",
        "Alzate et al., 2025 — Real-Time Traffic Violation Detection Using YOLOv8",
        "Wen et al., 2020 — UA-DETRAC Benchmark (IEEE Trans. Intelligent Transportation)",
        "Yadav & Singh, 2025 — Helmet Detection Using YOLO for Traffic Enforcement",
        "Jangam et al., 2025 — Integrated Helmet Detection & ANPR Using Deep Learning",
        "ITRVD Survey Group, 2024 — Review of Intelligent Traffic Violation Detection (IEEE Access)",
    ]
    for r in refs:
        st.markdown(f"<div style='font-size:0.83rem; color:#666; padding:0.25rem 0; border-bottom:1px solid #111;'>• {r}</div>", unsafe_allow_html=True)
