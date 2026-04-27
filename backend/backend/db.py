import oracledb

def get_connection():
    conn = oracledb.connect(
        user="parking_db",
        password="pass123",
        dsn="localhost/XEPDB1"
    )
    return conn