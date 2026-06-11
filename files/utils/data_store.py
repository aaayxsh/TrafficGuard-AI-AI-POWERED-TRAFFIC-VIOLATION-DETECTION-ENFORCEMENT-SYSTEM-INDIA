import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

VIOLATION_TYPES = ["Over-Speeding", "Signal Jump", "No Helmet", "Wrong Side", "No Seat Belt", "Illegal Parking"]
LOCATIONS = [
    "NH-24 Ghaziabad", "Sector-18 Noida", "Rajnagar Intersection",
    "DND Flyway", "Expressway Toll Plaza", "Connaught Place Jn.",
    "Karol Bagh Signal", "NH-58 Meerut Road"
]
STATES = ["UP", "DL", "MH", "HR", "RJ", "GJ", "KA", "TN"]
FINE_MAP = {
    "Over-Speeding": 2000, "Signal Jump": 5000,
    "No Helmet": 1000, "Wrong Side": 5000,
    "No Seat Belt": 1000, "Illegal Parking": 500
}
STATUSES = ["Pending", "Paid", "Disputed"]

def _generate_plate():
    return f"{random.choice(STATES)}{random.randint(10,99)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000,9999)}"

def _seed_data(n=80):
    rows = []
    now = datetime.now()
    for _ in range(n):
        vtype = random.choice(VIOLATION_TYPES)
        rows.append({
            "timestamp": (now - timedelta(minutes=random.randint(0, 20160))).strftime("%Y-%m-%d %H:%M:%S"),
            "plate": _generate_plate(),
            "violation_type": vtype,
            "location": random.choice(LOCATIONS),
            "speed": random.randint(60, 185) if vtype == "Over-Speeding" else random.randint(20, 80),
            "fine": FINE_MAP[vtype],
            "confidence": round(random.uniform(0.82, 0.99), 2),
            "status": random.choices(STATUSES, weights=[60, 30, 10])[0],
        })
    return pd.DataFrame(rows)

def get_violations_df() -> pd.DataFrame:
    if "violations_df" not in st.session_state:
        st.session_state.violations_df = _seed_data(80)
    return st.session_state.violations_df

def add_violation(record: dict):
    df = get_violations_df()
    new_row = pd.DataFrame([record])
    st.session_state.violations_df = pd.concat([df, new_row], ignore_index=True)
