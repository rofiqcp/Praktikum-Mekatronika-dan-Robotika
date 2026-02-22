"""
Percobaan 6 – Edge: Anomaly Detector
Berlangganan ke MQTT, menjalankan deteksi anomali Z-score,
dan meneruskan data ke FastAPI backend via HTTP POST.

Algoritma Z-score:
  z = (x - mean) / std
  Jika |z| > threshold (default 2.5) → anomali terdeteksi
  Window: 20 pembacaan terakhir
"""

import json
import time
import threading
import logging
from collections import deque

import numpy as np
import requests
import paho.mqtt.client as mqtt

# ─── Konfigurasi ──────────────────────────────────────────────────────────────
MQTT_BROKER   = "127.0.0.1"
MQTT_PORT     = 1883
MQTT_CLIENT   = "AnomalyDetector-001"
TOPIC_DATA    = "realtime/sensors/data"
TOPIC_ANOMALY = "realtime/alerts/anomaly"

BACKEND_URL   = "http://localhost:8000/api/sensor"

WINDOW_SIZE   = 20
Z_THRESHOLD   = 2.5

# ─── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Sliding window untuk tiap fitur ─────────────────────────────────────────
windows: dict[str, deque] = {
    "temperature": deque(maxlen=WINDOW_SIZE),
    "gas_ppm":     deque(maxlen=WINDOW_SIZE),
    "humidity":    deque(maxlen=WINDOW_SIZE),
}

mqtt_client: mqtt.Client = None  # type: ignore[assignment]


def compute_zscore(window: deque, new_value: float) -> float:
    """Hitung z-score nilai baru terhadap window saat ini."""
    if len(window) < 3:
        # Belum cukup data untuk menghitung statistik
        return 0.0
    arr = np.array(list(window), dtype=float)
    mean = arr.mean()
    std  = arr.std()
    if std < 1e-9:
        return 0.0
    return float((new_value - mean) / std)


def detect_anomalies(payload: dict) -> list[dict]:
    """
    Cek anomali pada temperature, gas_ppm, dan humidity.
    Mengembalikan daftar anomali yang terdeteksi.
    """
    anomalies = []
    for field in ("temperature", "gas_ppm", "humidity"):
        val = payload.get(field)
        if val is None:
            continue
        val = float(val)
        z = compute_zscore(windows[field], val)
        windows[field].append(val)

        if abs(z) > Z_THRESHOLD:
            anomalies.append({
                "field":    field,
                "value":    val,
                "z_score":  round(z, 3),
                "mean":     round(float(np.mean(list(windows[field]))), 3),
                "threshold": Z_THRESHOLD,
            })
    return anomalies


def forward_to_backend(payload: dict) -> bool:
    """Kirim payload ke FastAPI backend via HTTP POST."""
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=5)
        resp.raise_for_status()
        return True
    except requests.RequestException as exc:
        log.warning("HTTP forward gagal: %s", exc)
        return False


def publish_anomaly(device: str, anomalies: list[dict]) -> None:
    """Publikasikan alert anomali ke MQTT broker."""
    if mqtt_client is None:
        return
    alert = {
        "device":    device,
        "alert":     "anomaly_detected",
        "anomalies": anomalies,
        "ts":        int(time.time()),
    }
    payload_str = json.dumps(alert)
    mqtt_client.publish(TOPIC_ANOMALY, payload_str)
    log.warning("Anomali terdeteksi: %s", payload_str)


# ─── MQTT Callbacks ───────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        log.info("Terhubung ke MQTT broker %s:%d", MQTT_BROKER, MQTT_PORT)
        client.subscribe(TOPIC_DATA)
        log.info("Subscribe ke topik: %s", TOPIC_DATA)
    else:
        log.error("Gagal terhubung ke MQTT, kode: %d", rc)


def on_message(client, userdata, msg):
    topic   = msg.topic
    raw_str = msg.payload.decode("utf-8", errors="replace")

    try:
        payload = json.loads(raw_str)
    except json.JSONDecodeError as exc:
        log.warning("JSON parse error pada topik %s: %s", topic, exc)
        return

    log.info("[%s] %s", topic, raw_str)

    # Deteksi anomali
    anomalies = detect_anomalies(payload)
    if anomalies:
        device = payload.get("device", "UNKNOWN")
        publish_anomaly(device, anomalies)

    # Forward ke backend (non-blocking di thread terpisah)
    threading.Thread(
        target=forward_to_backend,
        args=(payload,),
        daemon=True,
    ).start()


def on_disconnect(client, userdata, rc, properties=None):
    log.warning("Terputus dari MQTT (rc=%d). Reconnect otomatis...", rc)


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    global mqtt_client

    log.info("=== Anomaly Detector (Z-score, window=%d, threshold=%.1f) ===",
             WINDOW_SIZE, Z_THRESHOLD)

    mqtt_client = mqtt.Client(
        client_id=MQTT_CLIENT,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    mqtt_client.on_connect    = on_connect
    mqtt_client.on_message    = on_message
    mqtt_client.on_disconnect = on_disconnect

    mqtt_client.reconnect_delay_set(min_delay=1, max_delay=30)
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

    log.info("Menjalankan loop MQTT. Tekan Ctrl+C untuk berhenti.")
    try:
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        log.info("Dihentikan oleh pengguna.")
    finally:
        mqtt_client.disconnect()


if __name__ == "__main__":
    main()
