import logging
import os
from datetime import datetime

# Create logs directory if not exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configure logging
logging.basicConfig(
    filename="logs/parking_logs.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def log_event(user_id, action, details=""):
    """
    Logs system events for parking management system.
    
    Args:
        user_id (int): ID of admin/user performing action
        action (str): Action type (PARK, EXIT, LOGIN, etc.)
        details (str): Extra info like plate number, slot id, etc.
    """

    message = f"USER_ID={user_id} | ACTION={action} | DETAILS={details}"
    logging.info(message)