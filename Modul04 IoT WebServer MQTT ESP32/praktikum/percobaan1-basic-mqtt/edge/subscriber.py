#!/usr/bin/env python3
"""
Percobaan 1 – Edge subscriber
Subscribes to 'praktikum/esp32/hello', parses JSON, and forwards to Node.js backend.
"""

import json
import time
import paho.mqtt.client as mqtt
import requests

# ─── Configuration ────────────────────────────────────────────────────────────
MQTT_BROKER   = "192.168.1.100"
MQTT_PORT     = 1883
MQTT_TOPIC    = "praktikum/esp32/hello"
BACKEND_URL   = "http://localhost:3000/api/data"
RECONNECT_DELAY = 5          # seconds between reconnection attempts


# ─── MQTT callbacks ───────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connected to broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Subscribed to '{MQTT_TOPIC}'")
    else:
        print(f"[MQTT] Connection failed with code {rc}")


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[MQTT] Unexpected disconnect (rc={rc}). Reconnecting in {RECONNECT_DELAY}s …")


def on_message(client, userdata, msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # ── Parse JSON ────────────────────────────────────────────────────────────
    try:
        data = json.loads(msg.payload.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"[ERROR] Failed to parse payload: {exc}")
        return

    device  = data.get("device",  "unknown")
    uptime  = data.get("uptime",  0)
    counter = data.get("counter", 0)
    message = data.get("message", "")

    # ── Pretty-print ──────────────────────────────────────────────────────────
    print(
        f"[{timestamp}] device={device!r:16s} "
        f"uptime={uptime:6d}s  "
        f"counter={counter:5d}  "
        f"msg={message!r}"
    )

    # ── Forward to backend ────────────────────────────────────────────────────
    payload = {
        "device":  device,
        "uptime":  uptime,
        "counter": counter,
        "message": message,
    }
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=5)
        if resp.status_code == 200:
            print(f"  → Backend OK (HTTP {resp.status_code})")
        else:
            print(f"  → Backend returned HTTP {resp.status_code}: {resp.text[:80]}")
    except requests.exceptions.ConnectionError:
        print(f"  → [WARN] Backend unreachable ({BACKEND_URL}). Data not stored.")
    except requests.exceptions.Timeout:
        print("  → [WARN] Backend request timed out.")
    except requests.exceptions.RequestException as exc:
        print(f"  → [ERROR] Request failed: {exc}")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=== Percobaan 1 – Edge Subscriber ===")
    print(f"Broker : {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Topic  : {MQTT_TOPIC}")
    print(f"Backend: {BACKEND_URL}")
    print("─" * 60)

    client = mqtt.Client(client_id="edge-subscriber-p1")
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
