import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard import (
    get_daily_revenue,
    get_daily_occupancy,
    get_slot_utilization,
    get_status_distribution,
    get_peak_hours,
    get_vehicle_type_stats
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Parking Dashboard", layout="wide")

TEXT = "#1F2937"

GREEN = "#00C853"
RED = "#FF5252"
BLUE = "#2196F3"
ORANGE = "#FFB300"
PURPLE = "#7C4DFF"
CYAN = "#00ACC1"


def show_dashboard_ui():

    st.title("📊 Parking Dashboard")

    # ---------------- DATA ----------------
    rev_data = get_daily_revenue()
    occ_data = get_daily_occupancy()

    # ---------------- KPI ----------------
    st.subheader("📌 Key Metrics")

    total_revenue = sum([x[1] for x in rev_data]) if rev_data else 0
    total_cars = sum([x[1] for x in occ_data]) if occ_data else 0
    avg_cars = (total_cars / len(occ_data)) if occ_data else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Revenue", round(total_revenue, 2))
    col2.metric("🚗 Total Vehicles", total_cars)
    col3.metric("📊 Avg Daily Cars", round(avg_cars, 2))

    st.divider()

    # ---------------- SLOT UTILIZATION ----------------
    occupied, total = get_slot_utilization()
    util = (occupied / total * 100) if total else 0

    st.metric("🅿️ Slot Utilization", f"{util:.2f}%")

    st.divider()

    st.subheader("📊 Advanced Insights")

    col1, col2 = st.columns(2)

    # ==================================================
    # STATUS DISTRIBUTION (PIE)
    # ==================================================
    with col1:
        st.subheader("🚗 Status Distribution")

        data = get_status_distribution()

        if data:
            df = pd.DataFrame(data, columns=["Status", "Count"])

            fig = px.pie(
                df,
                names="Status",
                values="Count",
                color="Status",
                color_discrete_map={
                    "ACTIVE": GREEN,
                    "EXITED": RED
                }
            )

            fig.update_traces(
                textinfo="percent+label",
                textfont=dict(color=TEXT),
                marker={"line": {"color":"white", "width":2}}
            )

            fig.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font = {'color' : TEXT}
            )

            st.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # PEAK HOURS (BAR)
    # ==================================================
    with col2:
        st.subheader("🕒 Peak Hours")

        data = get_peak_hours()

        if data:
            df = pd.DataFrame(data, columns=["Hour", "Vehicles"])

            fig = px.bar(
                df,
                x="Hour",
                y="Vehicles",
                text="Vehicles",
                color_discrete_sequence=[CYAN]
            )

            fig.update_traces(textposition="outside")

            fig.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font={'color':TEXT}
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==================================================
    # VEHICLE TYPE PIE
    # ==================================================
    st.subheader("🚗 Vehicle Type Demand")

    data = get_vehicle_type_stats()

    if data:
        df = pd.DataFrame(data, columns=["Type", "Count"])

        fig = px.pie(
            df,
            names="Type",
            values="Count",
            color_discrete_sequence=[BLUE, GREEN, ORANGE]
        )

        fig.update_traces(
            textinfo="percent+label",
            textfont= {'color':TEXT},
            marker= {'line' : {'color' : "white", 'width' : 2}}
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font= {'color':TEXT}
        )

        st.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # REVENUE PER DAY (FIXED)
    # ==================================================
    with col1:
        st.subheader("💰 Revenue per Day")

        if rev_data:
            df = pd.DataFrame(rev_data, columns=["Date", "Revenue"])

            # ✅ FIX: remove datetime completely
            df["Date"] = df["Date"].astype(str)

            df = df.groupby("Date")["Revenue"].sum().reset_index()

            fig = px.bar(
                df,
                x="Date",
                y="Revenue",
                text="Revenue",
                color_discrete_sequence=[GREEN]
            )

            fig.update_traces(textposition="outside")

            fig.update_xaxes(type="category")

            fig.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font={'color':TEXT}
            )

            st.plotly_chart(fig, use_container_width=True)

    # ==================================================
    # OCCUPANCY TREND (FIXED)
    # ==================================================
    with col2:
        st.subheader("🅿️ Occupancy Trend")

        if occ_data:
            df = pd.DataFrame(occ_data, columns=["Date", "Cars"])

            # ✅ FIX: force string
            df["Date"] = df["Date"].astype(str)

            df = df.sort_values("Date")

            fig = px.line(
                df,
                x="Date",
                y="Cars",
                markers=True,
                color_discrete_sequence=[BLUE]
            )

            fig.update_traces(line= {'width' : 3})

            fig.update_xaxes(type="category")

            fig.update_layout(
                paper_bgcolor="white",
                plot_bgcolor="white",
                font={'color':TEXT}
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==================================================
    # CUMULATIVE REVENUE (FIXED)
    # ==================================================
    st.subheader("📈 Revenue Growth (Cumulative)")

    if rev_data:
        df = pd.DataFrame(rev_data, columns=["Date", "Revenue"])

        # ✅ FIX
        df["Date"] = df["Date"].astype(str)
        df = df.sort_values("Date")

        df["Cumulative"] = df["Revenue"].cumsum()

        fig = px.line(
            df,
            x="Date",
            y="Cumulative",
            markers=True,
            color_discrete_sequence=[PURPLE]
        )

        fig.update_traces(line={'width':3})

        fig.update_xaxes(type="category")

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            font={'color':TEXT}
        )

        st.plotly_chart(fig, use_container_width=True)