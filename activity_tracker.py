from datetime import datetime

# Global variable to track last activity
last_activity = datetime.now()

def update_last_activity():
    """Call this function to update the timestamp when a user interacts."""
    global last_activity
    last_activity = datetime.now()

def get_last_activity():
    """Returns the datetime of last known user interaction."""
    return last_activity
