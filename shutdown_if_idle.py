# import subprocess
# from datetime import datetime, timedelta

# LOG_PATH = "/root/rakshit_chatbot_backend/server.log"  # Your backend logs user interaction here
# IDLE_LIMIT = timedelta(minutes=5)

# def get_last_activity_time():
#     try:
#         with open(LOG_PATH, "r") as f:
#             lines = f.readlines()
#             for line in reversed(lines):
#                 if "POST /chat" in line:
#                     timestamp = line.split()[0]
#                     return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")  # Adjust format if needed
#     except Exception as e:
#         print(f"Error reading log: {e}")
#     return None

# def get_system_uptime():
#     output = subprocess.check_output("uptime -s", shell=True).decode().strip()
#     return datetime.strptime(output, "%Y-%m-%d %H:%M:%S")

# def main():
#     now = datetime.utcnow()
#     uptime = get_system_uptime()
    
#     if now - uptime < IDLE_LIMIT:
#         print("⏳ Server just started. Skipping shutdown.")
#         return

#     last_active = get_last_activity_time()
#     if last_active is None or (now - last_active) > IDLE_LIMIT:
#         print("💤 No activity. Shutting down...")
#         subprocess.run("shutdown now", shell=True)
#     else:
#         print("✅ User recently active. Not shutting down.")

# if __name__ == "__main__":
#     main()


from datetime import datetime, timedelta
from pathlib import Path
import os

IDLE_THRESHOLD_MINUTES = 5
PING_LOG = "/root/rakshit_chatbot_backend/last_ping.txt"
DEBUG_LOG = "/root/shutdown_debug.txt"

def log_debug(message):
    with open(DEBUG_LOG, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def get_last_active_time():
    try:
        with open(PING_LOG, "r") as f:
            lines = f.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip()
            return datetime.strptime(last_line, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        log_debug(f"❌ Error reading ping file: {e}")
        return None

def should_shutdown():
    last_active = get_last_active_time()
    now = datetime.now()

    if last_active:
        idle_time = now - last_active
        log_debug(f"Last active at: {last_active} | Idle: {idle_time}")
        return idle_time > timedelta(minutes=IDLE_THRESHOLD_MINUTES)
    else:
        log_debug("No valid last ping found.")
        return True

if should_shutdown():
    log_debug("💤 Server is idle. Triggering shutdown.")
    os.system("shutdown now")
else:
    log_debug("✅ Server is active. No shutdown.")
