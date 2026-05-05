import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import time

# ============================
# 🔗 IMPORT FIX
# ============================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import run_system

# ============================
# 📄 PAGE CONFIG
# ============================
st.set_page_config(page_title="Email Automation", layout="wide")

# ============================
# 🎨 CSS (SAAS LEVEL LOOK)
# ============================
st.markdown("""
<style>
body { background-color: #f5f7fa; }
h1 { color: #2c3e50; }

.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 220px;
    font-size: 16px;
    border: none;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ============================
# 📂 NAVIGATION
# ============================
st.sidebar.title("📂 Email System")
page = st.sidebar.selectbox("Navigate", ["Dashboard", "Data Preview"])

# ============================
# 📊 DASHBOARD
# ============================
if page == "Dashboard":

    st.title("📧 Email Automation & Reminder System")
    st.markdown("### 🟢 System Status: READY")

    mode = st.sidebar.radio("Mode", ["Dry Run", "Send Emails"])
    auto_run = st.toggle("🔁 Live Scheduler (60 sec)")

    if "data" not in st.session_state:
        st.session_state["data"] = None

    def execute():
        df = run_system(mode == "Dry Run")
        st.session_state["data"] = df

    if st.button("▶ Run Automation"):
        with st.spinner("Processing Emails..."):
            execute()
            st.success("Emails Processed Successfully!")

    if auto_run:
        st.info("Auto scheduler running...")
        time.sleep(60)
        execute()
        st.rerun()

    # ============================
    # 📊 RESULTS
    # ============================
    if st.session_state["data"] is not None:

        df = st.session_state["data"]

        total = len(df)
        success = df["status"].astype(str).str.contains("SENT").sum()
        failed = df["status"].astype(str).str.contains("FAILED").sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("📨 Total Emails", total)
        col2.metric("✅ Success", success)
        col3.metric("❌ Failed", failed)

        st.subheader("📊 Status Distribution")
        st.plotly_chart(px.pie(df, names="status"), use_container_width=True)

        st.subheader("📈 Email Trend")
        df["time"] = pd.to_datetime(df["time"])
        trend = df.groupby(df["time"].dt.floor("min")).size().reset_index(name="count")
        st.plotly_chart(px.line(trend, x="time", y="count"), use_container_width=True)

        # ============================
        # 📄 TABLE (FIXED - NO APPLYMAP)
        # ============================
        st.subheader("📄 Detailed Report")

        def style_status(val):
            if "SENT" in str(val):
                return "background-color: #d4edda"
            elif "FAILED" in str(val):
                return "background-color: #f8d7da"
            return "background-color: #fff3cd"

        styled_df = df.style.map(lambda v: style_status(v) if v == v else "")
        st.dataframe(df)

    # ============================
    # 🧾 LOG VIEWER (FIXED PATH)
    # ============================
    st.subheader("🧾 Logs")

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log_file = os.path.join(BASE_DIR, "logs", "email.log")

    st.write("📍 Log Path:", log_file)

    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            logs = f.readlines()

        if logs:
            st.text_area("System Logs", "".join(logs[-100:]), height=300)
        else:
            st.warning("No logs yet. Run automation first.")
    else:
        st.error("Log file not found")

# ============================
# 📁 DATA PAGE
# ============================
elif page == "Data Preview":

    st.title("📁 Data Preview")

    try:
        st.subheader("👤 Contacts")
        st.dataframe(pd.read_csv("data/contacts.csv"))
    except:
        st.warning("contacts.csv missing")

    try:
        st.subheader("⏰ Reminders")
        st.dataframe(pd.read_csv("data/reminders.csv"))
    except:
        st.warning("reminders.csv missing")