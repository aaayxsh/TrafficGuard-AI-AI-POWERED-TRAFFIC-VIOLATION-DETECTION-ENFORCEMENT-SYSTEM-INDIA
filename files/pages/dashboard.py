import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
from utils.data_store import get_violations_df

def show():
    st.markdown("<div class='main-header'>🚦 TrafficGuard AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>AI-POWERED TRAFFIC VIOLATION DETECTION & ENFORCEMENT SYSTEM · INDIA</div>", unsafe_allow_html=True)

    # ── KPI Metrics ─────────────────────────────────────────────────────────
    df = get_violations_df()
    today = datetime.now().date()
    today_df = df[pd.to_datetime(df["timestamp"]).dt.date == today]

    col1, col2, col3, col4, col5 = st.columns(5)
    metrics = [
        ("Total Violations", len(df), "🚨"),
        ("Today's Violations", len(today_df), "📅"),
        ("Challans Issued", int(len(df) * 0.87), "📄"),
        ("High-Risk Zones", 7, "⚠️"),
        ("Active Cameras", 24, "📷"),
    ]
    for col, (label, val, icon) in zip([col1, col2, col3, col4, col5], metrics):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:1.8rem'>{icon}</div>
                <div class='metric-value'>{val:,}</div>
                <div class='metric-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts Row ───────────────────────────────────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📈 Violations Over Last 14 Days")
        dates = [today - timedelta(days=i) for i in range(13, -1, -1)]
        counts = [random.randint(18, 75) for _ in dates]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=counts,
            mode='lines+markers',
            line=dict(color='#FF4B2B', width=2.5),
            marker=dict(size=6, color='#FF416C'),
            fill='tozeroy',
            fillcolor='rgba(255,75,43,0.08)'
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#aaa', size=11),
            xaxis=dict(gridcolor='#222', showgrid=True),
            yaxis=dict(gridcolor='#222', showgrid=True),
            margin=dict(l=10, r=10, t=10, b=10),
            height=260
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("🍕 Violation Types")
        vtype_counts = df["violation_type"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=vtype_counts.index,
            values=vtype_counts.values,
            hole=0.55,
            marker=dict(colors=['#FF4B2B','#FF7043','#FFA500','#FFD700','#6495ED','#66BB6A']),
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#aaa', size=11),
            showlegend=True,
            legend=dict(font=dict(size=10), bgcolor='rgba(0,0,0,0)'),
            margin=dict(l=0, r=0, t=10, b=10),
            height=260
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Recent Violations Table ───────────────────────────────────────────────
    st.subheader("🕒 Recent Violations")
    recent = df.sort_values("timestamp", ascending=False).head(8).reset_index(drop=True)
    
    badge_colors = {
        "Over-Speeding": "badge-red",
        "Signal Jump": "badge-orange",
        "No Helmet": "badge-yellow",
        "Wrong Side": "badge-red",
        "No Seat Belt": "badge-yellow",
        "Illegal Parking": "badge-blue",
    }

    # Render styled table
    header_cols = st.columns([1.5, 1.5, 2, 2, 1.5, 1])
    for col, h in zip(header_cols, ["Timestamp", "Plate No.", "Violation", "Location", "Speed", "Fine (₹)"]):
        col.markdown(f"<span style='color:#666; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em;'>{h}</span>", unsafe_allow_html=True)

    for _, row in recent.iterrows():
        r = st.columns([1.5, 1.5, 2, 2, 1.5, 1])
        r[0].markdown(f"<span style='font-size:0.85rem; color:#aaa;'>{row['timestamp']}</span>", unsafe_allow_html=True)
        r[1].markdown(f"<span style='font-family:monospace; color:#FF4B2B; font-weight:700;'>{row['plate']}</span>", unsafe_allow_html=True)
        bc = badge_colors.get(row['violation_type'], 'badge-blue')
        r[2].markdown(f"<span class='violation-badge {bc}'>{row['violation_type']}</span>", unsafe_allow_html=True)
        r[3].markdown(f"<span style='font-size:0.85rem;'>{row['location']}</span>", unsafe_allow_html=True)
        spd = row.get('speed', '-')
        r[4].markdown(f"<span style='font-size:0.85rem;'>{spd} km/h</span>", unsafe_allow_html=True)
        r[5].markdown(f"<span style='color:#66BB6A; font-weight:700;'>₹{row['fine']}</span>", unsafe_allow_html=True)

    # ── Live Alerts ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🔴 Live Alerts")
    alerts = [
        "🚨 Over-speeding detected at NH-24 Ghaziabad — MH12AB3456 — 142 km/h",
        "⛑️ No helmet violation at Rajnagar Intersection — UP14XY7890",
        "🚦 Signal jump at Sector-18 Noida — DL8CAB1234 — Camera #07",
        "🅿️ Illegal parking on Expressway Service Road — HR26BC9012",
    ]
    for a in alerts:
        st.markdown(f"<div class='alert-box'>{a}</div>", unsafe_allow_html=True)
