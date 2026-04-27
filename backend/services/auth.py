import hashlib
from db import get_connection
from services.logger import log_event

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(username, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        hashed = hash_password(password)

        cur.execute("""
            INSERT INTO users (username, password, role)
            VALUES (:1, :2, 'ADMIN')
        """, [username, hashed])

        conn.commit()
        log_event(None, "SIGNUP", f"Username={username}")
        return True

    except Exception as e:
        conn.rollback()
        print("Signup error:", e)
        return False

    finally:
        conn.close()


def login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        hashed = hash_password(password)

        # 1. check user exists
        cur.execute("""
            SELECT user_id, password 
            FROM users
            WHERE username = :1
        """, [username])

        user = cur.fetchone()

        if not user:
            return "NOT_FOUND"

        user_id, db_password = user

        # 2. check password
        if db_password != hashed:
            return "WRONG_PASSWORD"

        return user_id, username

    except Exception as e:
        print("Login error:", e)
        return "ERROR"

    finally:
        conn.close()