# import subprocess
# from datetime import datetime, timedelta, timezone

# DEBUG_LOG = "/root/shutdown_log.txt"
# IDLE_THRESHOLD_MINUTES = 5

# def log_debug(msg):
#     with open(DEBUG_LOG, "a") as f:
#         f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

# def get_active_connections():
#     try:
#         output = subprocess.check_output("ss -Htn sport = :8000", shell=True).decode()

#         return [line for line in output.strip().split("\n") if line]
#     except Exception as e:
#         log_debug(f"❌ Failed to get active connections: {e}")
#         return []

# def get_uptime():
#     output = subprocess.check_output("uptime -s", shell=True).decode().strip()
#     return datetime.strptime(output, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

# def main():
#     now = datetime.now(timezone.utc)
#     uptime = get_uptime()
#     if now - uptime < timedelta(minutes=IDLE_THRESHOLD_MINUTES):
#         log_debug("⏳ Server just started. Skipping shutdown.")
#         return

#     connections = get_active_connections()
#     if not connections:
#         log_debug("💤 No active users. Triggering shutdown.")
#         subprocess.run("shutdown now", shell=True)
#     else:
#         log_debug(f"✅ {len(connections)} active HTTPS connections. No shutdown.")

# if __name__ == "__main__":
#     main()


from datetime import datetime, timedelta
from pathlib import Path
import os

ACTIVITY_FILE = "/root/.activity"
DEBUG_LOG = "/root/shutdown_debug.txt"
IDLE_THRESHOLD_MINUTES = 5  # Shutdown if idle for this many minutes

def log_debug(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_msg = f"{timestamp} - {message}"
    print(full_msg)
    with open(DEBUG_LOG, "a") as f:
        f.write(f"{timestamp} - {message}\n")

def should_shutdown():
    activity_path = Path(ACTIVITY_FILE)

    # Case 1: File does not exist — assume idle
    if not activity_path.exists():
        log_debug("❌ Activity file missing. Assuming idle.")
        return True

    last_active = datetime.fromtimestamp(activity_path.stat().st_mtime)
    now = datetime.now()

    idle_duration = now - last_active
    log_debug(f"🕓 Last activity: {last_active} | Idle: {idle_duration}")

    return idle_duration > timedelta(minutes=IDLE_THRESHOLD_MINUTES)

# Skip shutdown right after boot
UPTIME_SECONDS_FILE = "/proc/uptime"
try:
    with open(UPTIME_SECONDS_FILE, "r") as f:
        uptime_seconds = float(f.readline().split()[0])
except Exception:
    uptime_seconds = 0

if uptime_seconds < 300:
    log_debug("⏳ Server just started. Skipping shutdown.")
else:
    if should_shutdown():
        log_debug("💤 No active users. Triggering shutdown.")
        os.system("shutdown now")
    else:
        log_debug("✅ Active user detected. No shutdown.")
