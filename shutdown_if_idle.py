import subprocess
from datetime import datetime, timedelta, timezone

DEBUG_LOG = "/root/shutdown_log.txt"
IDLE_THRESHOLD_MINUTES = 5

def log_debug(msg):
    with open(DEBUG_LOG, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

def get_active_connections():
    try:
        output = subprocess.check_output("ss -Htn sport = :443", shell=True).decode()
        return [line for line in output.strip().split("\n") if line]
    except Exception as e:
        log_debug(f"❌ Failed to get active connections: {e}")
        return []

def get_uptime():
    output = subprocess.check_output("uptime -s", shell=True).decode().strip()
    return datetime.strptime(output, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

def main():
    now = datetime.now(timezone.utc)
    uptime = get_uptime()
    if now - uptime < timedelta(minutes=IDLE_THRESHOLD_MINUTES):
        log_debug("⏳ Server just started. Skipping shutdown.")
        return

    connections = get_active_connections()
    if not connections:
        log_debug("💤 No active users. Triggering shutdown.")
        subprocess.run("shutdown now", shell=True)
    else:
        log_debug(f"✅ {len(connections)} active HTTPS connections. No shutdown.")

if __name__ == "__main__":
    main()
