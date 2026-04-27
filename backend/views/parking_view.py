import streamlit as st
from services.parking import park_vehicle


def show_parking_ui():

    st.header("🚗 Park Vehicle")

    vehicle_type = st.selectbox(
        "Select Vehicle Type",
        ["CAR", "BIKE", "BUS"]
    )

    plate = st.text_input("Enter Plate Number")

    if st.button("Park Vehicle"):

        if not plate or not plate.strip():
            st.error("Please enter plate number")
            return

        user_id = st.session_state.user_id
        result = park_vehicle(plate.strip().upper(), vehicle_type, user_id)

        if result == "ALREADY_PARKED":
            st.error("This vehicle is already parked")

        elif result == "NO_SLOT":
            st.error("No free slot available for this vehicle type")

        elif result == "SUCCESS":
            st.success(f"Vehicle {plate} parked successfully!")
            
        else:
            st.error("⚠️ System error occurred")