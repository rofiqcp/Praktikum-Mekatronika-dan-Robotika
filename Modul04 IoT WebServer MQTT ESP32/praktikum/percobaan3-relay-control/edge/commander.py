#!/usr/bin/env python3
"""
Percobaan 3 - Edge Commander
MQTT CLI interface untuk mengontrol Relay/LED di ESP32.
Menerima status dari ESP32, meneruskan ke backend Node.js via HTTP POST.
"""

import json
import sys
import threading
import time
import paho.mqtt.client as mqtt
import requests

# ─── Configuration ────────────────────────────────────────────────────────────
MQTT_BROKER   = "localhost"
MQTT_PORT     = 1883
MQTT_CLIENT   = "EdgeCommander"

TOPIC_SET    = "control/relay/set"
TOPIC_STATUS = "control/relay/status"
TOPIC_ALL_OFF = "control/all/off"

BACKEND_URL  = "http://localhost:3001/api/status"

# ─── Device number mapping for CLI ────────────────────────────────────────────
DEVICE_MAP = {
    "relay1": 1,
    "relay2": 2,
    "led1":   3,
    "led2":   4,
}

latest_status = {}
_mqtt_client  = None

# ─── MQTT Callbacks ───────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[MQTT] Connected to broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(TOPIC_STATUS)
        print(f"[MQTT] Subscribed to: {TOPIC_STATUS}")
    else:
        print(f"[MQTT] Connection failed with code {rc}")


def on_message(client, userdata, msg):
    global latest_status
    try:
        payload = json.loads(msg.payload.decode())
        latest_status = payload
        ts = time.strftime("%H:%M:%S")
        print(
            f"\n[STATUS {ts}] "
            f"relay1={payload.get('relay1','?')} "
            f"relay2={payload.get('relay2','?')} "
            f"led1={payload.get('led1','?')} "
            f"led2={payload.get('led2','?')} "
            f"uptime={payload.get('uptime','?')}s"
        )
        forward_to_backend(payload)
        print("cmd> ", end="", flush=True)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON decode: {e}")


def on_disconnect(client, userdata, rc, properties=None):
    print(f"\n[MQTT] Disconnected (rc={rc}). Will auto-reconnect...")


# ─── HTTP Forward to Backend ─────────────────────────────────────────────────
def forward_to_backend(status: dict):
    try:
        resp = requests.post(BACKEND_URL, json=status, timeout=2)
        if resp.status_code not in (200, 201):
            print(f"[HTTP] Backend returned {resp.status_code}")
    except requests.exceptions.ConnectionError:
        pass  # Backend may not be running; silently skip
    except Exception as e:
        print(f"[HTTP] Error: {e}")


# ─── Publish Helper ───────────────────────────────────────────────────────────
def send_command(device: str, state: str):
    """Send {relay, state} JSON to control/relay/set."""
    device_lower = device.lower()
    if device_lower not in DEVICE_MAP:
        print(f"[CLI] Unknown device '{device}'. Valid: {list(DEVICE_MAP.keys())}")
        return
    payload = json.dumps({"relay": DEVICE_MAP[device_lower], "state": state.upper()})
    _mqtt_client.publish(TOPIC_SET, payload)
    print(f"[CLI] Sent: {payload}")


def send_all_off():
    """Publish to control/all/off."""
    _mqtt_client.publish(TOPIC_ALL_OFF, json.dumps({"command": "all_off"}))
    print("[CLI] Sent: ALL OFF")


# ─── Print Help ───────────────────────────────────────────────────────────────
def print_help():
    print("""
╔══════════════════════════════════════════════════════╗
║       Percobaan 3 - Edge Commander (MQTT CLI)        ║
╠══════════════════════════════════════════════════════╣
║  Commands:                                           ║
║    relay1 on   / relay1 off                          ║
║    relay2 on   / relay2 off                          ║
║    led1 on     / led1 off                            ║
║    led2 on     / led2 off                            ║
║    all off                (emergency all-off)        ║
║    status                 (show latest status)       ║
║    help                   (show this message)        ║
║    quit / exit            (exit program)             ║
╚══════════════════════════════════════════════════════╝
""")


# ─── MQTT Thread ─────────────────────────────────────────────────────────────
def mqtt_thread_fn():
    global _mqtt_client
    _mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT)
    _mqtt_client.on_connect    = on_connect
    _mqtt_client.on_message    = on_message
    _mqtt_client.on_disconnect = on_disconnect

    try:
        _mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    except Exception as e:
        print(f"[MQTT] Cannot connect to broker: {e}")
        sys.exit(1)

    _mqtt_client.loop_forever()


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=== Percobaan 3 Edge Commander ===")
    print(f"Broker: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"Backend: {BACKEND_URL}")

    t = threading.Thread(target=mqtt_thread_fn, daemon=True)
    t.start()

    # Wait until MQTT connects
    time.sleep(1.5)
    print_help()

    while True:
        try:
            print("cmd> ", end="", flush=True)
            line = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[CLI] Exiting...")
            break

        if not line:
            continue

        parts = line.lower().split()

        if parts[0] in ("quit", "exit"):
            print("[CLI] Goodbye!")
            break

        elif parts[0] == "help":
            print_help()

        elif parts[0] == "status":
            if latest_status:
                print(json.dumps(latest_status, indent=2))
            else:
                print("[CLI] No status received yet.")

        elif parts[0] == "all" and len(parts) >= 2 and parts[1] == "off":
            send_all_off()

        elif len(parts) == 2 and parts[0] in DEVICE_MAP and parts[1] in ("on", "off"):
            send_command(parts[0], parts[1])

        else:
            print(f"[CLI] Unknown command: '{line}'. Type 'help' for usage.")


if __name__ == "__main__":
    main()
