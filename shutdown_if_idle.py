import subprocess
from datetime import datetime, timedelta

LOG_PATH = "/root/rakshit_chatbot_backend/server.log"  # Your backend logs user interaction here
IDLE_LIMIT = timedelta(minutes=5)

def get_last_activity_time():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
            for line in reversed(lines):
                if "POST /chat" in line:
                    timestamp = line.split()[0]
                    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")  # Adjust format if needed
    except Exception as e:
        print(f"Error reading log: {e}")
    return None

def get_system_uptime():
    output = subprocess.check_output("uptime -s", shell=True).decode().strip()
    return datetime.strptime(output, "%Y-%m-%d %H:%M:%S")

def main():
    now = datetime.utcnow()
    uptime = get_system_uptime()
    
    if now - uptime < IDLE_LIMIT:
        print("⏳ Server just started. Skipping shutdown.")
        return

    last_active = get_last_activity_time()
    if last_active is None or (now - last_active) > IDLE_LIMIT:
        print("💤 No activity. Shutting down...")
        subprocess.run("shutdown now", shell=True)
    else:
        print("✅ User recently active. Not shutting down.")

if __name__ == "__main__":
    main()
