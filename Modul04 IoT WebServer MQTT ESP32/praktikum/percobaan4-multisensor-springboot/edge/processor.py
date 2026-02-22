#!/usr/bin/env python3
"""
Percobaan 4 - Edge Processor
Subscribes to MQTT sensor data, applies data processing
(unit conversion, outlier detection, moving average),
enriches data, and forwards to Spring Boot backend via HTTP POST.
Logs all readings and prints dashboard summaries every 60 seconds.
"""

import json
import logging
import sys
import threading
import time
from collections import deque
from logging.handlers import RotatingFileHandler

import numpy as np
import paho.mqtt.client as mqtt
import requests

# ─── Configuration ────────────────────────────────────────────────────────────
MQTT_BROKER    = "localhost"
MQTT_PORT      = 1883
MQTT_CLIENT    = "EdgeProcessor"
TOPIC_DATA     = "sensors/multi/data"
TOPIC_CONFIG   = "sensors/multi/config"

BACKEND_URL    = "http://localhost:8080/api/sensors"
LOCATION       = "Lab Mekatronika - Ruang B204"
SUMMARY_INTERVAL_S = 60

# ─── Moving Average Window Size ───────────────────────────────────────────────
MA_WINDOW = 5

# Outlier thresholds (min, max) for each sensor
OUTLIER_LIMITS = {
    "temperature":   (-10.0, 80.0),
    "humidity":      (0.0,   100.0),
    "light":         (0,     100),
    "soil_moisture": (0,     100),
    "battery":       (2.5,   4.3),
}

# ─── Logging Setup ────────────────────────────────────────────────────────────
log_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = RotatingFileHandler(
    "edge_processor.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
)
file_handler.setFormatter(log_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)

logger = logging.getLogger("EdgeProcessor")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# ─── Moving Average Buffers ───────────────────────────────────────────────────
ma_buffers: dict[str, deque] = {
    "temperature":   deque(maxlen=MA_WINDOW),
    "humidity":      deque(maxlen=MA_WINDOW),
    "light":         deque(maxlen=MA_WINDOW),
    "soil_moisture": deque(maxlen=MA_WINDOW),
    "battery":       deque(maxlen=MA_WINDOW),
}

# ─── Statistics Accumulator ──────────────────────────────────────────────────
readings_buffer: list[dict] = []
last_summary_time = time.time()
total_received  = 0
total_forwarded = 0
total_outliers  = 0


# ─── Outlier Detection ────────────────────────────────────────────────────────
def is_outlier(field: str, value: float) -> bool:
    if field not in OUTLIER_LIMITS:
        return False
    lo, hi = OUTLIER_LIMITS[field]
    return not (lo <= value <= hi)


# ─── Moving Average ───────────────────────────────────────────────────────────
def moving_average(field: str, value: float) -> float:
    ma_buffers[field].append(value)
    return float(np.mean(list(ma_buffers[field])))


# ─── Unit Conversion ─────────────────────────────────────────────────────────
def celsius_to_fahrenheit(c: float) -> float:
    return round(c * 9.0 / 5.0 + 32.0, 1)


# ─── Process a Single Reading ─────────────────────────────────────────────────
def process_reading(raw: dict) -> dict | None:
    global total_outliers

    outlier_fields = []
    for field in ("temperature", "humidity", "light", "soil_moisture", "battery"):
        val = raw.get(field)
        if val is not None and is_outlier(field, float(val)):
            outlier_fields.append(field)
            logger.warning(f"[OUTLIER] {field}={val} out of range {OUTLIER_LIMITS[field]}")
            total_outliers += 1

    if outlier_fields:
        logger.warning(f"[SKIP] Reading discarded due to outliers: {outlier_fields}")
        return None

    # Moving average smoothing
    temp_smooth  = moving_average("temperature",   float(raw["temperature"]))
    hum_smooth   = moving_average("humidity",      float(raw["humidity"]))
    light_smooth = moving_average("light",         float(raw["light"]))
    soil_smooth  = moving_average("soil_moisture", float(raw["soil_moisture"]))
    batt_smooth  = moving_average("battery",       float(raw["battery"]))

    enriched = {
        "device":           raw.get("device", "ESP32-MULTI"),
        "temperature":      round(temp_smooth,  1),
        "temperatureF":     celsius_to_fahrenheit(temp_smooth),
        "humidity":         round(hum_smooth,   1),
        "light":            round(light_smooth),
        "soilMoisture":     round(soil_smooth),
        "battery":          round(batt_smooth,  2),
        "location":         LOCATION,
        "rawTimestamp":     raw.get("ts", 0),
    }
    return enriched


# ─── Forward to Spring Boot Backend ──────────────────────────────────────────
def forward_to_backend(data: dict) -> bool:
    global total_forwarded
    try:
        resp = requests.post(BACKEND_URL, json=data, timeout=5)
        if resp.status_code in (200, 201):
            total_forwarded += 1
            logger.info(f"[HTTP] Forwarded to backend → {resp.status_code}")
            return True
        else:
            logger.error(f"[HTTP] Backend returned {resp.status_code}: {resp.text[:120]}")
    except requests.exceptions.ConnectionError:
        logger.warning("[HTTP] Backend not reachable (Spring Boot may be starting)")
    except Exception as e:
        logger.error(f"[HTTP] Error: {e}")
    return False


# ─── Print Dashboard Summary ─────────────────────────────────────────────────
def print_summary():
    global readings_buffer, last_summary_time
    now = time.time()
    if now - last_summary_time < SUMMARY_INTERVAL_S or not readings_buffer:
        return

    temps  = [r["temperature"]  for r in readings_buffer]
    hums   = [r["humidity"]     for r in readings_buffer]
    lights = [r["light"]        for r in readings_buffer]
    soils  = [r["soilMoisture"] for r in readings_buffer]

    print("\n" + "═" * 60)
    print(f"  DASHBOARD SUMMARY  (last {SUMMARY_INTERVAL_S}s)")
    print("═" * 60)
    print(f"  Readings received : {total_received}")
    print(f"  Forwarded to API  : {total_forwarded}")
    print(f"  Outliers discarded: {total_outliers}")
    print(f"  {'Metric':<18} {'Min':>7} {'Max':>7} {'Avg':>7}")
    print(f"  {'-'*46}")
    print(f"  {'Temperature (°C)':<18} {min(temps):>7.1f} {max(temps):>7.1f} {np.mean(temps):>7.1f}")
    print(f"  {'Humidity (%)':<18} {min(hums):>7.1f} {max(hums):>7.1f} {np.mean(hums):>7.1f}")
    print(f"  {'Light (%)':<18} {min(lights):>7.0f} {max(lights):>7.0f} {np.mean(lights):>7.0f}")
    print(f"  {'Soil Moisture (%)':<18} {min(soils):>7.0f} {max(soils):>7.0f} {np.mean(soils):>7.0f}")
    print("═" * 60 + "\n")

    readings_buffer   = []
    last_summary_time = now


# ─── MQTT Callbacks ───────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logger.info(f"[MQTT] Connected to broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(TOPIC_DATA)
        logger.info(f"[MQTT] Subscribed to: {TOPIC_DATA}")
    else:
        logger.error(f"[MQTT] Connection failed rc={rc}")


def on_message(client, userdata, msg):
    global total_received
    total_received += 1

    try:
        raw = json.loads(msg.payload.decode())
        logger.info(f"[MQTT] Raw: {json.dumps(raw)}")
    except json.JSONDecodeError as e:
        logger.error(f"[MQTT] JSON decode error: {e}")
        return

    processed = process_reading(raw)
    if processed is None:
        return

    readings_buffer.append(processed)
    logger.info(f"[PROC] Processed: temp={processed['temperature']}°C "
                f"hum={processed['humidity']}% "
                f"light={processed['light']}% "
                f"soil={processed['soilMoisture']}%")

    forward_to_backend(processed)
    print_summary()


def on_disconnect(client, userdata, rc, properties=None):
    logger.warning(f"[MQTT] Disconnected (rc={rc})")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    logger.info("=== Percobaan 4 Edge Processor ===")
    logger.info(f"MQTT Broker : {MQTT_BROKER}:{MQTT_PORT}")
    logger.info(f"Backend URL : {BACKEND_URL}")
    logger.info(f"Location    : {LOCATION}")
    logger.info(f"MA Window   : {MA_WINDOW} readings")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT)
    client.on_connect    = on_connect
    client.on_message    = on_message
    client.on_disconnect = on_disconnect

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    except Exception as e:
        logger.error(f"[MQTT] Cannot connect: {e}")
        sys.exit(1)

    logger.info("Edge processor running. Press Ctrl+C to stop.")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down edge processor.")
        client.disconnect()


if __name__ == "__main__":
    main()
