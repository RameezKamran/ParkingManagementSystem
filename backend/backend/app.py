import streamlit as st
from views.parking_view import show_parking_ui
from views.exit_view import show_exit_ui
from views.dashboard_view import show_dashboard_ui
from services.auth import login, signup

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Parking System",
    page_icon="🚗",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
    <h1 style='text-align:center; color:#4CAF50;'>🚗 Smart Parking System</h1>
    <p style='text-align:center;'>Data-powered Parking Management Dashboard</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- LOGIN / SIGNUP ----------------
if not st.session_state.logged_in:

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🔐 Login / Signup")

        menu = st.radio("Choose Action", ["Login", "Signup"])

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if menu == "Signup":
            if st.button("Create Account"):
                if signup(username, password):
                    st.success("Account Created Successfully!")
                else:
                    st.error("Signup Failed")

        else:
            if st.button("Login"):
                result = login(username, password)

                if result == "NOT_FOUND":
                    st.error("User does not exist")

                elif result == "WRONG_PASSWORD":
                    st.error("Invalid password")

                elif result == "ERROR":
                    st.error("System error occurred")

                else:
                    user_id, username = result

                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.rerun()

    with col2:
        st.info("""
        ### Features:
        - 🚗 Smart Parking Allocation  
        - 📊 Real-time Dashboard  
        - 💰 Billing System  
        - 🔐 Multi-user Access  
        """)

# ---------------- MAIN APP ----------------
else:

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.markdown(f"### 👋 Welcome, {st.session_state.username}")
        st.markdown("---")

        menu = st.radio(
            "Navigation",
            ["📊 Dashboard", "🚗 Park Vehicle", "🚪 Exit Vehicle"]
        )

        st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()

    # ---------------- DASHBOARD ----------------
    if menu == "📊 Dashboard":
        show_dashboard_ui()

    # ---------------- PARK ----------------
    elif menu == "🚗 Park Vehicle":
        show_parking_ui()
    # ---------------- EXIT ----------------
    elif menu == "🚪 Exit Vehicle":
        show_exit_ui()