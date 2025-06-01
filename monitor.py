import os
import psutil
import requests
import json
from datetime import datetime, timezone

# Skapa dashboard-mapp om den inte finns
os.makedirs("dashboard", exist_ok=True)

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

# Skapa dataobjekt
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

# Skicka Slack-meddelande – korrekt formaterat med headers och data
if slack_url:
    headers = {'Content-Type': 'application/json'}
    payload = {
        "text": f"📢 TEST från monitor.py\nCPU: {cpu}%\nMEM: {mem}%\nSTATUS: {status}\nTID: {timestamp}"
    }
    response = requests.post(slack_url, headers=headers, data=json.dumps(payload))
    print("🔗 Slack-respons:", response.status_code)
else:
    print("🚫 Slack Webhook URL saknas – kontrollera miljövariabeln")

# Visa i terminal
print(json.dumps(data, indent=2))
