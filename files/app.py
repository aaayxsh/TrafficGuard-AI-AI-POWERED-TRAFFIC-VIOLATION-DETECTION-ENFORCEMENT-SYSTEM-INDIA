import streamlit as st

st.set_page_config(
    page_title="TrafficGuard AI",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FF4B2B, #FF416C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
    }

    .sub-header {
        text-align: center;
        color: #888;
        font-size: 0.95rem;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }

    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(255,75,43,0.1);
    }

    .metric-value {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #FF4B2B;
    }

    .metric-label {
        font-size: 0.8rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.2rem;
    }

    .violation-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-red { background: rgba(255,75,43,0.15); color: #FF4B2B; border: 1px solid #FF4B2B; }
    .badge-orange { background: rgba(255,165,0,0.15); color: #FFA500; border: 1px solid #FFA500; }
    .badge-yellow { background: rgba(255,215,0,0.15); color: #FFD700; border: 1px solid #FFD700; }
    .badge-blue { background: rgba(100,149,237,0.15); color: #6495ED; border: 1px solid #6495ED; }

    .stButton>button {
        background: linear-gradient(135deg, #FF4B2B, #FF416C);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        letter-spacing: 0.05em;
        transition: all 0.2s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,75,43,0.4);
    }

    div[data-testid="stSidebarNav"] { display: none; }

    .sidebar-nav-btn {
        width: 100%;
        text-align: left;
        padding: 0.6rem 1rem;
        margin: 0.2rem 0;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        font-weight: 500;
        transition: background 0.2s;
    }

    .challan-box {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border: 1px solid #FF4B2B;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Rajdhani', sans-serif;
    }

    .challan-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FF4B2B;
        text-align: center;
        letter-spacing: 0.1em;
        border-bottom: 1px solid #FF4B2B33;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.9rem;
    }

    .info-key { color: #aaa; }
    .info-val { color: #fff; font-weight: 600; }

    .alert-box {
        background: rgba(255,75,43,0.1);
        border-left: 4px solid #FF4B2B;
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #eee;
    }

    .pipeline-step {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #0f3460;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }

    .pipeline-step-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #FF4B2B;
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-family: Rajdhani, sans-serif; font-size: 1.8rem; font-weight: 700;
                    background: linear-gradient(135deg, #FF4B2B, #FF416C);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🚦 TrafficGuard AI
        </div>
        <div style='font-size: 0.75rem; color: #666; letter-spacing: 0.1em; margin-top: 0.3rem;'>
            ROAD SAFETY ENFORCEMENT SYSTEM
        </div>
    </div>
    <hr style='border-color: #222; margin: 0.5rem 0 1rem;'>
    """, unsafe_allow_html=True)

    pages = {
        "🏠 Dashboard": "dashboard",
        "🎥 Live Detection": "detection",
        "📋 Violations Log": "violations",
        "📄 E-Challan Generator": "challan",
        "📊 Analytics": "analytics",
        "ℹ️ About / How It Works": "about",
    }

    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    for label, key in pages.items():
        is_active = st.session_state.page == key
        btn_style = (
            "background: linear-gradient(135deg,#FF4B2B22,#FF416C22); "
            "color: #FF4B2B; border: 1px solid #FF4B2B44;"
            if is_active else
            "background: transparent; color: #ccc; border: 1px solid transparent;"
        )
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("<hr style='border-color:#222; margin-top:1rem;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem; color:#444; text-align:center;'>Sharda University · PBL Project 2025<br>Dept. of Engineering & Technology</div>", unsafe_allow_html=True)


# Page Router
page = st.session_state.page

if page == "dashboard":
    from pages import dashboard; dashboard.show()
elif page == "detection":
    from pages import detection; detection.show()
elif page == "violations":
    from pages import violations; violations.show()
elif page == "challan":
    from pages import challan; challan.show()
elif page == "analytics":
    from pages import analytics; analytics.show()
elif page == "about":
    from pages import about; about.show()
