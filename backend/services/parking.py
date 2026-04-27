from db import get_connection
from services.logger import log_event

def park_vehicle(plate_number, vehicle_type, user_id):
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. CHECK VEHICLE
        cur.execute("""
            SELECT vehicle_id 
            FROM vehicle 
            WHERE plate_number = :1
        """, [plate_number])

        existing = cur.fetchone()

        if existing:
            vehicle_id = existing[0]
        else:
            vehicle_id_var = cur.var(int)

            cur.execute("""
                INSERT INTO vehicle (plate_number, vehicle_type)
                VALUES (:1, :2)
                RETURNING vehicle_id INTO :3
            """, [plate_number, vehicle_type, vehicle_id_var])

            vehicle_id = vehicle_id_var.getvalue()[0]

        # 2. CHECK ACTIVE SESSION
        cur.execute("""
            SELECT 1 
            FROM parking_session
            WHERE vehicle_id = :1 
            AND status = 'ACTIVE'
            AND exit_time IS NULL
        """, [vehicle_id])

        if cur.fetchone():
            return "ALREADY_PARKED"

        # 3. FIND SLOT
        cur.execute("""
            SELECT slot_id 
            FROM slot 
            WHERE TRIM(UPPER(slot_status)) = 'FREE'
            AND TRIM(UPPER(slot_type)) = UPPER(:1)
            AND ROWNUM = 1
        """, [vehicle_type])

        slot = cur.fetchone()

        if not slot:
            return "NO_SLOT"

        slot_id = slot[0]

        # 4. INSERT SESSION
        cur.execute("""
            INSERT INTO parking_session 
            (vehicle_id, slot_id, status, created_by)
            VALUES (:1, :2, 'ACTIVE', :3)
        """, [vehicle_id, slot_id, user_id])

        # 5. UPDATE SLOT
        cur.execute("""
            UPDATE slot
            SET slot_status = 'OCCUPIED'
            WHERE slot_id = :1
        """, [slot_id])

        conn.commit()

        log_event(user_id, "PARK_VEHICLE", f"Plate={plate_number}, Slot={slot_id}")

        return "SUCCESS"

    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return "ERROR"

    finally:
        conn.close()
        
        
def is_vehicle_parked(plate_number):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 1
            FROM parking_session ps
            JOIN vehicle v ON ps.vehicle_id = v.vehicle_id
            WHERE v.plate_number = :1
            AND ps.status = 'ACTIVE'
            AND ps.exit_time IS NULL
        """, [plate_number])

        result = cur.fetchone()
        return True if result else False

    finally:
        conn.close()