import os
import json
import random
import requests
from datetime import datetime, timezone

# Skapa dashboard-mapp om den inte finns
os.makedirs("dashboard", exist_ok=True)

# Simulera CPU och minnesanvändning
cpu = random.uniform(60, 95)
mem = random.uniform(60, 90)
status = "ALERT" if cpu > 80 or mem > 75 else "OK"
timestamp = datetime.now(timezone.utc).isoformat()

data = {
    "timestamp": timestamp,
    "cpu": cpu,
    "mem": mem,
    "status": status
}

# Skriv till dashboard/data.json
with open("dashboard/data.json", "w") as f:
    json.dump(data, f, indent=2)

# Lägg till i historik
history_path = "dashboard/history.json"
if os.path.exists(history_path):
    with open(history_path, "r") as f:
        history = json.load(f)
else:
    history = []

history.append(data)
history = history[-50:]

with open(history_path, "w") as f:
    json.dump(history, f, indent=2)

# Skicka Slack-larm om ALERT
slack_url = os.getenv("SLACK_WEBHOOK_URL")
if status == "ALERT" and slack_url:
    headers = {'Content-Type': 'application/json'}
    payload = {
        "text": f"🚨 Simulerat larm från simulate.py\nCPU: {cpu:.1f}%\nMEM: {mem:.1f}%\nSTATUS: {status}\nTID: {timestamp}"
    }
    response = requests.post(slack_url, headers=headers, data=json.dumps(payload))
    print("🔗 Slack-respons:", response.status_code)

# Skriv till terminalen
print("💾 Simulerad datapost sparad:")
print(json.dumps(data, indent=2))
