from datetime import datetime
from db import get_connection
from services.logger import log_event

def exit_vehicle(plate_number, user_id=None):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Find ACTIVE session
        cur.execute("""
            SELECT ps.session_id, ps.slot_id, ps.entry_time
            FROM parking_session ps
            JOIN vehicle v ON ps.vehicle_id = v.vehicle_id
            WHERE v.plate_number = :1
              AND ps.status = 'ACTIVE'
              AND ps.exit_time IS NULL
        """, [plate_number])

        session = cur.fetchone()

        if not session:
            print("❌ No active parking session found for this vehicle")
            return False

        session_id, slot_id, entry_time = session

        # 2. Time calculation
        exit_time = datetime.now()

        duration_seconds = (exit_time - entry_time).total_seconds()
        duration_hours = max(1, duration_seconds / 3600)

        # 3. Fee calculation
        rate_per_hour = 50
        amount = round(duration_hours * rate_per_hour, 2)

        # 4. Update session
        cur.execute("""
            UPDATE parking_session
            SET exit_time = :1,
                status = 'EXITED'
            WHERE session_id = :2
        """, [exit_time, session_id])

        # 5. Payment record
        cur.execute("""
            INSERT INTO payment (session_id, amount, payment_status)
            VALUES (:1, :2, 'UNPAID')
        """, [session_id, amount])

        # 6. Free slot
        cur.execute("""
            UPDATE slot
            SET slot_status = 'FREE'
            WHERE slot_id = :1
        """, [slot_id])

        conn.commit()

        print("🚗 Vehicle exited successfully")
        print(f"💰 Total bill: {amount}")

        # 7. Logging (safe check)
        log_event(user_id if user_id else 0, "EXIT_VEHICLE", f"Plate={plate_number}, Amount={amount}")

        return True

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)

    finally:
        conn.close()