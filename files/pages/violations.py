import streamlit as st
import pandas as pd
from utils.data_store import get_violations_df

BADGE = {
    "Over-Speeding": "badge-red",
    "Signal Jump": "badge-orange",
    "No Helmet": "badge-yellow",
    "Wrong Side": "badge-red",
    "No Seat Belt": "badge-yellow",
    "Illegal Parking": "badge-blue",
}

def show():
    st.markdown("<div class='main-header'>📋 Violations Log</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>COMPLETE VIOLATION RECORDS WITH SEARCH & FILTER</div>", unsafe_allow_html=True)

    df = get_violations_df()

    # ── Filters ───────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    with col1:
        search_plate = st.text_input("🔍 Search by Plate", placeholder="e.g. UP14")
    with col2:
        vtype_filter = st.multiselect("Violation Type", options=df["violation_type"].unique().tolist(),
                                       default=df["violation_type"].unique().tolist())
    with col3:
        location_filter = st.multiselect("Location", options=df["location"].unique().tolist(),
                                          default=df["location"].unique().tolist())
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset Filters"):
            st.rerun()

    # Apply filters
    filtered = df.copy()
    if search_plate:
        filtered = filtered[filtered["plate"].str.contains(search_plate.upper(), na=False)]
    if vtype_filter:
        filtered = filtered[filtered["violation_type"].isin(vtype_filter)]
    if location_filter:
        filtered = filtered[filtered["location"].isin(location_filter)]

    filtered = filtered.sort_values("timestamp", ascending=False).reset_index(drop=True)

    st.markdown(f"<div style='color:#666; font-size:0.85rem; margin-bottom:1rem;'>Showing <b style='color:#FF4B2B;'>{len(filtered)}</b> of {len(df)} records</div>", unsafe_allow_html=True)

    # ── Table ─────────────────────────────────────────────────────────────────
    headers = ["#", "Timestamp", "Plate No.", "Violation Type", "Location", "Speed", "Fine (₹)", "Confidence", "Status"]
    widths = [0.4, 1.5, 1.3, 1.8, 2, 1, 0.8, 1, 1]

    hcols = st.columns(widths)
    for col, h in zip(hcols, headers):
        col.markdown(f"<span style='color:#555; font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;'>{h}</span>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a1a1a; margin:0.3rem 0;'>", unsafe_allow_html=True)

    for i, row in filtered.head(50).iterrows():
        rcols = st.columns(widths)
        rcols[0].markdown(f"<span style='color:#444; font-size:0.82rem;'>{i+1}</span>", unsafe_allow_html=True)
        rcols[1].markdown(f"<span style='font-size:0.82rem; color:#aaa;'>{row['timestamp']}</span>", unsafe_allow_html=True)
        rcols[2].markdown(f"<span style='font-family:monospace; color:#FF4B2B; font-weight:700; font-size:0.9rem;'>{row['plate']}</span>", unsafe_allow_html=True)
        bc = BADGE.get(row['violation_type'], 'badge-blue')
        rcols[3].markdown(f"<span class='violation-badge {bc}'>{row['violation_type']}</span>", unsafe_allow_html=True)
        rcols[4].markdown(f"<span style='font-size:0.82rem;'>{row['location']}</span>", unsafe_allow_html=True)
        rcols[5].markdown(f"<span style='font-size:0.82rem;'>{row.get('speed', '-')} km/h</span>", unsafe_allow_html=True)
        rcols[6].markdown(f"<span style='color:#66BB6A; font-weight:700;'>₹{row['fine']}</span>", unsafe_allow_html=True)
        conf_val = row.get('confidence', 0.92)
        rcols[7].markdown(f"<span style='font-size:0.82rem; color:#6495ED;'>{float(conf_val)*100:.0f}%</span>", unsafe_allow_html=True)
        status = row.get('status', 'Pending')
        sc = "#66BB6A" if status == "Paid" else "#FFA500" if status == "Pending" else "#FF4B2B"
        rcols[8].markdown(f"<span style='color:{sc}; font-size:0.82rem; font-weight:600;'>{status}</span>", unsafe_allow_html=True)

        st.markdown("<div style='border-bottom: 1px solid #111; margin: 0.15rem 0;'></div>", unsafe_allow_html=True)

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    csv = filtered.to_csv(index=False)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv,
        file_name="traffic_violations_export.csv",
        mime="text/csv",
        use_container_width=False
    )
