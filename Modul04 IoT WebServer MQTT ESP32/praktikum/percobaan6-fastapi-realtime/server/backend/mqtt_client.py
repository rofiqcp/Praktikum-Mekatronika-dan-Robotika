# Percobaan 6 – Backend: MQTT Client (asyncio dengan paho-mqtt)
# Berlangganan ke topik MQTT dan menyiarkan data ke WebSocket.

import asyncio
import json
import logging
from datetime import datetime

import paho.mqtt.client as mqtt

from database import get_sensor_collection, get_alert_collection

log = logging.getLogger(__name__)

MQTT_BROKER    = "127.0.0.1"
MQTT_PORT      = 1883
TOPIC_SENSORS  = "realtime/sensors/data"
TOPIC_ALERTS   = "realtime/alerts/#"

# Referensi ke set WebSocket aktif (diisi oleh main.py)
active_websockets: set = set()

_loop: asyncio.AbstractEventLoop | None = None


def _broadcast(data: dict) -> None:
    """Kirim data ke semua WebSocket yang terhubung (thread-safe)."""
    if not active_websockets or _loop is None:
        return
    payload = json.dumps(data, default=str)
    for ws in list(active_websockets):
        asyncio.run_coroutine_threadsafe(_safe_send(ws, payload), _loop)


async def _safe_send(ws, payload: str) -> None:
    try:
        await ws.send_text(payload)
    except Exception:
        active_websockets.discard(ws)


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        log.info("[MQTT] Terhubung ke broker %s:%d", MQTT_BROKER, MQTT_PORT)
        client.subscribe(TOPIC_SENSORS)
        client.subscribe(TOPIC_ALERTS)
        log.info("[MQTT] Subscribe: %s, %s", TOPIC_SENSORS, TOPIC_ALERTS)
    else:
        log.error("[MQTT] Gagal terhubung, kode: %d", rc)


def on_message(client, userdata, msg):
    topic   = msg.topic
    raw_str = msg.payload.decode("utf-8", errors="replace")

    try:
        payload = json.loads(raw_str)
    except json.JSONDecodeError:
        log.warning("[MQTT] Bukan JSON valid dari topik %s", topic)
        return

    payload["timestamp"] = datetime.utcnow().isoformat()

    if topic == TOPIC_SENSORS:
        payload["_type"] = "sensor"
        _save_sensor(payload)
    else:
        payload["_type"] = "alert"
        _save_alert(payload)

    _broadcast(payload)


def _save_sensor(payload: dict) -> None:
    if _loop:
        asyncio.run_coroutine_threadsafe(_async_save_sensor(payload), _loop)


def _save_alert(payload: dict) -> None:
    if _loop:
        asyncio.run_coroutine_threadsafe(_async_save_alert(payload), _loop)


async def _async_save_sensor(payload: dict) -> None:
    try:
        await get_sensor_collection().insert_one(payload)
    except Exception as exc:
        log.warning("[DB] Gagal simpan sensor: %s", exc)


async def _async_save_alert(payload: dict) -> None:
    try:
        await get_alert_collection().insert_one(payload)
    except Exception as exc:
        log.warning("[DB] Gagal simpan alert: %s", exc)


def on_disconnect(client, userdata, rc, properties=None):
    log.warning("[MQTT] Terputus (rc=%d). Reconnect otomatis...", rc)


def start_mqtt_background(loop: asyncio.AbstractEventLoop) -> None:
    """Mulai klien MQTT di thread daemon terpisah."""
    global _loop
    _loop = loop

    client = mqtt.Client(
        client_id="FastAPI-Backend-001",
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )
    client.on_connect    = on_connect
    client.on_message    = on_message
    client.on_disconnect = on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    import threading

    def _run():
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            client.loop_forever()
        except Exception as exc:
            log.error("[MQTT] Thread error: %s", exc)

    t = threading.Thread(target=_run, daemon=True, name="mqtt-client")
    t.start()
    log.info("[MQTT] Thread dimulai.")
