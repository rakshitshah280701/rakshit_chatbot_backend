from datetime import datetime, timedelta
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
            for line in reversed(lines):
                line = line.strip()
                try:
                    return datetime.strptime(line, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    continue  # Skip malformed lines
    except Exception as e:
        log_debug(f"❌ Error reading ping file: {e}")
    return None

def should_shutdown():
    now = datetime.now()
    last_active = get_last_active_time()

    if last_active:
        idle_time = now - last_active
        log_debug(f"✔️ Last active at: {last_active} | Idle: {idle_time}")
        return idle_time > timedelta(minutes=IDLE_THRESHOLD_MINUTES)
    else:
        log_debug("❌ No valid last ping found.")
        return True

if should_shutdown():
    log_debug("💤 Server is idle. Triggering shutdown.")
    os.system("shutdown now")
else:
    log_debug("✅ Server is active. No shutdown.")
