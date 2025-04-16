from datetime import datetime, timedelta
from activity_tracker import get_last_activity
import os

IDLE_THRESHOLD_MINUTES = 5
DEBUG_LOG = "/root/shutdown_debug.txt"

def log_debug(message):
    with open(DEBUG_LOG, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def should_shutdown():
    try:
        last_active = get_last_activity()
        if not last_active:
            log_debug("⚠️ No last activity timestamp found.")
            return True

        now = datetime.now()
        idle_time = now - last_active
        log_debug(f"🕒 Last activity: {last_active} | Idle: {idle_time}")

        return idle_time > timedelta(minutes=IDLE_THRESHOLD_MINUTES)

    except Exception as e:
        log_debug(f"❌ Error in shutdown logic: {e}")
        return True

if should_shutdown():
    log_debug("💤 Server is idle. Triggering shutdown.")
    os.system("shutdown now")
else:
    log_debug("✅ Server is active. No shutdown.")
