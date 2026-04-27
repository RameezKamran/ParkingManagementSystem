from db import get_connection

# ==================================================
# 📊 BASIC DASHBOARD STATS
# ==================================================
def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM vehicle")
    vehicles = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM parking_session WHERE status = 'ACTIVE'")
    active = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM slot WHERE slot_status = 'OCCUPIED'")
    occupied = cur.fetchone()[0]

    cur.execute("SELECT NVL(SUM(amount), 0) FROM payment")
    revenue = cur.fetchone()[0]

    conn.close()

    return {
        "vehicles": vehicles,
        "active": active,
        "occupied": occupied,
        "revenue": revenue
    }


# ==================================================
# 🧾 RECENT ACTIVITY (JOIN)
# ==================================================
def get_recent_activity():
    conn = get_connection()

    import pandas as pd

    df = pd.read_sql("""
        SELECT v.plate_number,
               s.slot_id,
               ps.entry_time,
               ps.exit_time,
               ps.status
        FROM parking_session ps
        JOIN vehicle v ON ps.vehicle_id = v.vehicle_id
        JOIN slot s ON ps.slot_id = s.slot_id
        ORDER BY ps.entry_time DESC
    """, conn)

    conn.close()
    return df


# ==================================================
# 💰 REVENUE TREND
# ==================================================
def get_daily_revenue():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT TO_CHAR(TRUNC(ps.entry_time), 'YYYY-MM-DD'), NVL(SUM(p.amount), 0)
        FROM parking_session ps
        LEFT JOIN payment p ON ps.session_id = p.session_id
        GROUP BY TRUNC(ps.entry_time)
        ORDER BY TRUNC(ps.entry_time)
    """)

    data = cur.fetchall()
    conn.close()
    return data


# ==================================================
# 🅿️ OCCUPANCY TREND
# ==================================================
def get_daily_occupancy():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT TO_CHAR(TRUNC(entry_time), 'YYYY-MM-DD'), COUNT(*)
        FROM parking_session
        GROUP BY TRUNC(entry_time)
        ORDER BY TRUNC(entry_time)
    """)

    data = cur.fetchall()
    conn.close()
    return data


# ==================================================
# 🧠 SLOT UTILIZATION (DBMS AGGREGATION)
# ==================================================
def get_slot_utilization():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM slot")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM slot WHERE slot_status = 'OCCUPIED'")
    occupied = cur.fetchone()[0]

    conn.close()
    return occupied, total


# ==================================================
# 📊 STATUS DISTRIBUTION (GROUP BY)
# ==================================================
def get_status_distribution():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM parking_session
        GROUP BY status
    """)

    data = cur.fetchall()
    conn.close()
    return data


# ==================================================
# 🕒 PEAK HOURS (TIME ANALYTICS)
# ==================================================
def get_peak_hours():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT EXTRACT(HOUR FROM entry_time), COUNT(*)
        FROM parking_session
        GROUP BY EXTRACT(HOUR FROM entry_time)
        ORDER BY EXTRACT(HOUR FROM entry_time)
    """)

    data = cur.fetchall()
    conn.close()
    return data


# ==================================================
# 📈 CUMULATIVE (DP / PREFIX SUM)
# ==================================================
def get_cumulative(data):
    dates = []
    revenue = []
    cumulative = []

    total = 0

    for d, r in data:
        dates.append(str(d))
        revenue.append(r)
        total += r
        cumulative.append(total)

    return dates, revenue, cumulative


# ==================================================
# ⏱️ AVERAGE PARKING DURATION
# ==================================================
def get_avg_duration():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT AVG((exit_time - entry_time) * 24)
        FROM parking_session
        WHERE exit_time IS NOT NULL
    """)

    avg = cur.fetchone()[0]
    conn.close()

    return avg or 0


def get_vehicle_type_stats():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT vehicle_type, COUNT(*)
        FROM vehicle
        GROUP BY vehicle_type
    """)

    data = cur.fetchall()
    conn.close()
    return data