from datetime import datetime, timedelta
from pathlib import Path
import os

IDLE_LIMIT = timedelta(minutes=5)
PING_FILE = "last_ping.txt"

def should_shutdown():
    try:
        timestamp = Path(PING_FILE).read_text().strip()
        last_time = datetime.fromisoformat(timestamp)
        now = datetime.utcnow()

        if now - last_time > IDLE_LIMIT:
            print(f"🛑 Server idle for > {IDLE_LIMIT}. Shutting down...")
            return True
        else:
            print("✅ Server still active.")
            return False
    except Exception as e:
        print(f"⚠️ Failed to read ping file: {e}")
        return True  # assume idle if no ping file

if should_shutdown():
    os.system("shutdown now")
