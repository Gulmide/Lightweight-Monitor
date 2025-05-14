import random, json
from datetime import datetime, timezone

data = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "cpu": random.uniform(10, 95),
    "mem": random.uniform(20, 90),
    "status": "ALERT" if random.random() < 0.4 else "OK"
}

with open("dashboard/data.json", "w") as f:
    json.dump(data, f, indent=2)

# History-append
history_path = "dashboard/history.json"
try:
    with open(history_path, "r") as f:
        history = json.load(f)
except:
    history = []

history.append(data)
history = history[-50:]

with open(history_path, "w") as f:
    json.dump(history, f, indent=2)

print("Skapade testpost:", data)
