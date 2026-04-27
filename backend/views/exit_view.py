import streamlit as st
from services.exit import exit_vehicle  # Agar aapka logic exit service mein hai

def show_exit_ui():  # Is naam ka hona zaroori hai
    st.header("Exit Vehicle")
    plate = st.text_input("Enter Plate Number to Exit")

    if st.button("Exit Vehicle"):
        if plate:
            success = exit_vehicle(plate)

        if success:
            st.success(f"Vehicle {plate} exited!")
        else:
            st.error("No active parking session found!")
    else:
        st.error("Please enter plate number.")