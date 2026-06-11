import streamlit as st
import random
from datetime import datetime
from utils.data_store import get_violations_df

FINE_SCHEDULE = {
    "Over-Speeding":  {"fine": 2000, "section": "MV Act Sec. 183", "points": 2},
    "Signal Jump":    {"fine": 5000, "section": "MV Act Sec. 177", "points": 3},
    "No Helmet":      {"fine": 1000, "section": "MV Act Sec. 129", "points": 1},
    "Wrong Side":     {"fine": 5000, "section": "MV Act Sec. 184", "points": 3},
    "No Seat Belt":   {"fine": 1000, "section": "MV Act Sec. 194B", "points": 1},
    "Illegal Parking":{"fine": 500,  "section": "MV Act Sec. 177", "points": 0},
}

def show():
    st.markdown("<div class='main-header'>📄 E-Challan Generator</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>AUTOMATED FINE GENERATION · MOTOR VEHICLES ACT 2019</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔎 Lookup by Plate", "✏️ Manual Entry"])

    with tab1:
        _lookup_tab()

    with tab2:
        _manual_tab()


def _lookup_tab():
    df = get_violations_df()
    col1, col2 = st.columns([3, 1])
    with col1:
        plate_input = st.text_input("Enter Vehicle Registration Number", placeholder="e.g. UP14AB1234").upper().strip()
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔎 Find Violations")

    if search_btn and plate_input:
        matches = df[df["plate"].str.upper() == plate_input]
        if matches.empty:
            st.warning(f"No violations found for plate **{plate_input}**")
        else:
            st.success(f"Found **{len(matches)}** violation(s) for `{plate_input}`")
            for _, row in matches.iterrows():
                _render_challan(row["plate"], row["violation_type"], row["location"],
                                row["timestamp"], row.get("speed", "-"), row.get("confidence", 0.92))
    elif search_btn:
        st.error("Please enter a vehicle plate number.")


def _manual_tab():
    st.markdown("#### Enter Violation Details Manually")
    col1, col2 = st.columns(2)
    with col1:
        plate = st.text_input("Vehicle Plate Number", placeholder="MH12AB3456").upper()
        vtype = st.selectbox("Violation Type", list(FINE_SCHEDULE.keys()))
        speed = st.number_input("Recorded Speed (km/h)", min_value=0, max_value=300, value=0)
    with col2:
        location = st.text_input("Location", placeholder="NH-24, Ghaziabad")
        cam_id = st.text_input("Camera ID", placeholder="CAM-007")
        officer = st.text_input("Issuing Authority", placeholder="Traffic Control Room, Noida")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📄 Generate E-Challan", use_container_width=False):
        if plate and location:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _render_challan(plate, vtype, location, ts, speed, 0.99, cam_id, officer)
        else:
            st.error("Please fill in at least Plate Number and Location.")


def _render_challan(plate, vtype, location, timestamp, speed, confidence, cam_id=None, officer=None):
    info = FINE_SCHEDULE.get(vtype, {"fine": 1000, "section": "MV Act", "points": 1})
    challan_id = f"ECH{random.randint(100000, 999999)}"
    due_date = "Within 30 days"

    st.markdown(f"""
    <div class='challan-box'>
        <div class='challan-title'>⚖️ E-CHALLAN — TRAFFIC VIOLATION NOTICE</div>

        <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin-bottom:1rem;'>
            <div>
                <div style='color:#666; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Challan ID</div>
                <div style='color:#FF4B2B; font-weight:700; font-size:1.1rem;'>{challan_id}</div>
            </div>
            <div>
                <div style='color:#666; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>Issued On</div>
                <div style='color:#fff; font-weight:600;'>{timestamp}</div>
            </div>
        </div>

        <div class='info-row'><span class='info-key'>Vehicle Plate</span><span class='info-val' style='color:#FF4B2B;'>{plate}</span></div>
        <div class='info-row'><span class='info-key'>Violation</span><span class='info-val'>{vtype}</span></div>
        <div class='info-row'><span class='info-key'>Legal Section</span><span class='info-val'>{info["section"]}</span></div>
        <div class='info-row'><span class='info-key'>Location</span><span class='info-val'>{location}</span></div>
        <div class='info-row'><span class='info-key'>Recorded Speed</span><span class='info-val'>{speed} km/h</span></div>
        <div class='info-row'><span class='info-key'>Detection Confidence</span><span class='info-val'>{float(confidence)*100:.0f}%</span></div>
        <div class='info-row'><span class='info-key'>Camera ID</span><span class='info-val'>{cam_id or "CAM-AUTO"}</span></div>
        <div class='info-row'><span class='info-key'>Issuing Authority</span><span class='info-val'>{officer or "AI Enforcement System"}</span></div>
        <div class='info-row'><span class='info-key'>Demerit Points</span><span class='info-val'>{info["points"]} point(s)</span></div>

        <div style='margin-top:1rem; background:rgba(255,75,43,0.08); border:1px solid #FF4B2B44;
                    border-radius:8px; padding:1rem; text-align:center;'>
            <div style='color:#aaa; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.1em;'>Fine Amount</div>
            <div style='color:#FF4B2B; font-size:2.5rem; font-weight:700;'>₹{info["fine"]:,}</div>
            <div style='color:#666; font-size:0.8rem;'>Due: {due_date}</div>
        </div>

        <div style='margin-top:1rem; color:#555; font-size:0.75rem; text-align:center;'>
            Pay online at <span style='color:#6495ED;'>echallan.parivahan.gov.in</span> · 
            Disputes to be raised within 7 days · AI-generated under Motor Vehicles Act 2019
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        challan_text = f"""E-CHALLAN — {challan_id}
Plate: {plate} | Violation: {vtype}
Fine: Rs.{info['fine']} | Location: {location}
Date: {timestamp} | Section: {info['section']}
Pay at: echallan.parivahan.gov.in"""
        st.download_button("⬇️ Download Challan (.txt)", challan_text,
                           file_name=f"challan_{challan_id}.txt", use_container_width=True)
    with col2:
        st.button("📧 Send to Vehicle Owner (SMS/Email)", use_container_width=True, key=f"send_{challan_id}")
