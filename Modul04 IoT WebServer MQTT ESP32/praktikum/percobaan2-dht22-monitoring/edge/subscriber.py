#!/usr/bin/env python3
"""
Percobaan 2 – Edge subscriber
Subscribes to 'sensor/dht22/data', saves to CSV, POSTs to Flask backend,
and prints rolling min/max/avg stats over the last 10 readings.
"""

import json
import os
import csv
import time
from collections import deque
from datetime import datetime

import paho.mqtt.client as mqtt
import requests

# ─── Configuration ────────────────────────────────────────────────────────────
MQTT_BROKER   = "192.168.1.100"
MQTT_PORT     = 1883
MQTT_TOPIC    = "sensor/dht22/data"
BACKEND_URL   = "http://localhost:5000/api/sensor"
CSV_DIR       = "data"
CSV_FILE      = os.path.join(CSV_DIR, "sensor_log.csv")
STATS_WINDOW  = 10          # number of readings for rolling stats
RECONNECT_DELAY = 5

# Rolling buffer for temperature stats
temp_window = deque(maxlen=STATS_WINDOW)

# ─── CSV helpers ──────────────────────────────────────────────────────────────
CSV_HEADERS = ["timestamp", "device", "temperature", "humidity", "heat_index"]

def ensure_csv():
    """Create data/ directory and CSV with headers if they don't exist."""
    os.makedirs(CSV_DIR, exist_ok=True)
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            csv.writer(f).writerow(CSV_HEADERS)
        print(f"[CSV] Created {CSV_FILE}")

def append_csv(row: dict):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writerow(row)

# ─── Stats helper ─────────────────────────────────────────────────────────────
def print_stats():
    if not temp_window:
        return
    t_min = min(temp_window)
    t_max = max(temp_window)
    t_avg = sum(temp_window) / len(temp_window)
    n     = len(temp_window)
    print(f"  ┌─ Stats (last {n} readings) ─────────────────────────")
    print(f"  │ Temp min={t_min:.1f}°C  max={t_max:.1f}°C  avg={t_avg:.2f}°C")
    print(f"  └─────────────────────────────────────────────────────")

# ─── MQTT callbacks ───────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Subscribed to '{MQTT_TOPIC}'")
    else:
        print(f"[MQTT] Connection failed (rc={rc})")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[MQTT] Disconnected (rc={rc}). Reconnecting in {RECONNECT_DELAY}s …")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── Parse ─────────────────────────────────────────────────────────────────
    try:
        data = json.loads(msg.payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"[ERROR] Bad payload: {exc}")
        return

    device     = data.get("device",      "unknown")
    temperature = float(data.get("temperature", 0))
    humidity    = float(data.get("humidity",    0))
    heat_index  = float(data.get("heat_index",  0))

    # ── Console output ────────────────────────────────────────────────────────
    print(
        f"[{timestamp}] {device:16s}  "
        f"T={temperature:5.1f}°C  "
        f"H={humidity:5.1f}%  "
        f"HI={heat_index:5.1f}°C"
    )

    # ── Rolling stats ─────────────────────────────────────────────────────────
    temp_window.append(temperature)
    print_stats()

    # ── Save to CSV ───────────────────────────────────────────────────────────
    csv_row = {
        "timestamp":   timestamp,
        "device":      device,
        "temperature": temperature,
        "humidity":    humidity,
        "heat_index":  heat_index,
    }
    try:
        append_csv(csv_row)
    except OSError as exc:
        print(f"  [WARN] CSV write failed: {exc}")

    # ── POST to backend ───────────────────────────────────────────────────────
    payload = {
        "device":      device,
        "temperature": temperature,
        "humidity":    humidity,
        "heat_index":  heat_index,
    }
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            print(f"  → Backend OK (HTTP {resp.status_code})")
        else:
            print(f"  → Backend HTTP {resp.status_code}: {resp.text[:80]}")
    except requests.exceptions.ConnectionError:
        print(f"  → [WARN] Backend unreachable ({BACKEND_URL})")
    except requests.exceptions.Timeout:
        print("  → [WARN] Backend request timed out")
    except requests.exceptions.RequestException as exc:
        print(f"  → [ERROR] {exc}")

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    ensure_csv()

    print("=== Percobaan 2 – DHT22 Edge Subscriber ===")
    print(f"Broker : {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Topic  : {MQTT_TOPIC}")
    print(f"CSV    : {os.path.abspath(CSV_FILE)}")
    print(f"Backend: {BACKEND_URL}")
    print("─" * 60)

    client = mqtt.Client(client_id="edge-dht22-subscriber")
    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect
    client.on_message    = on_message

    client.reconnect_delay_set(min_delay=RECONNECT_DELAY, max_delay=30)

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    except OSError as exc:
        print(f"[ERROR] Cannot connect to broker: {exc}")
        return

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
