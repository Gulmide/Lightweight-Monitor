import os
import psutil
import requests
import json
from datetime import datetime, timezone

# Hämta aktuell CPU- och minnesanvändning
cpu = psutil.cpu_percent()
mem = psutil.virtual_memory().percent

# Läs tröskelvärden från miljövariabler eller använd default
cpu_limit = float(os.getenv("THRESHOLD_CPU", 80))
mem_limit = float(os.getenv("THRESHOLD_MEM", 75))
slack_url = os.getenv("SLACK_WEBHOOK_URL")

# Bestäm status
status = "OK"
if cpu > cpu_limit or mem > mem_limit:
    status = "ALERT"
    payload = {
        "text": f"🚨 LARM!\nCPU: {cpu}%\nMinne: {mem}%\nTid: {datetime.now(timezone.utc).isoformat()}"
    }
    if slack_url:
        requests.post(slack_url, json=payload)

# Skapa dataobjekt
data = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "cpu": cpu,
    "mem": mem,
    "status": status
}

with open("dashboard/data.json", "w") as f:
    json.dump(data, f, indent=2)

# Lägg till i historikfil
history_path = "dashboard/history.json"
if os.path.exists(history_path):
    with open(history_path, "r") as f:
        history = json.load(f)
else:
    history = []

history.append(data)

# Spara max 50 senaste poster
history = history[-50:]

with open(history_path, "w") as f:
    json.dump(history, f, indent=2)

# Visa i terminal
print(json.dumps(data, indent=2))

