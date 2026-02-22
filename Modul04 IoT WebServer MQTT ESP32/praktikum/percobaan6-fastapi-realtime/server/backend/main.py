# Percobaan 6 – Backend: FastAPI Application
# Real-time dashboard backend dengan WebSocket, MongoDB, dan MQTT.

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from database import get_sensor_collection, get_alert_collection, init_indexes
from models import SensorReading, Alert
from mqtt_client import active_websockets, start_mqtt_background

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

app = FastAPI(
    title="IoT Real-Time Dashboard API",
    description="Percobaan 6 – FastAPI + WebSocket + MongoDB",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Startup ──────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    await init_indexes()
    loop = asyncio.get_event_loop()
    start_mqtt_background(loop)
    log.info("FastAPI startup selesai.")


# ─── WebSocket /ws ────────────────────────────────────────────────────────────
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    active_websockets.add(ws)
    log.info("WebSocket terhubung. Total: %d", len(active_websockets))
    try:
        while True:
            # Terima pesan ping dari klien agar koneksi tetap hidup
            data = await ws.receive_text()
            if data == "ping":
                await ws.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        pass
    finally:
        active_websockets.discard(ws)
        log.info("WebSocket terputus. Total: %d", len(active_websockets))


# ─── POST /api/sensor ─────────────────────────────────────────────────────────
@app.post("/api/sensor", status_code=201)
async def receive_sensor(reading: SensorReading):
    """Terima data sensor dari edge (anomaly_detector.py atau langsung)."""
    doc = reading.model_dump()
    doc["timestamp"] = datetime.utcnow()
    doc["_type"] = "sensor"

    result = await get_sensor_collection().insert_one(doc)
    doc["_id"] = str(result.inserted_id)

    # Siarkan ke semua WebSocket
    broadcast_payload = json.dumps(doc, default=str)
    for ws in list(active_websockets):
        try:
            await ws.send_text(broadcast_payload)
        except Exception:
            active_websockets.discard(ws)

    return {"id": doc["_id"], "status": "saved"}


# ─── GET /api/sensors?limit=50 ────────────────────────────────────────────────
@app.get("/api/sensors")
async def get_sensors(limit: int = Query(default=50, ge=1, le=200)):
    """Ambil pembacaan sensor terbaru dari MongoDB."""
    cursor = get_sensor_collection().find(
        {}, {"_id": 0}
    ).sort("timestamp", -1).limit(limit)
    readings = await cursor.to_list(length=limit)
    return readings


# ─── GET /api/alerts?limit=20 ─────────────────────────────────────────────────
@app.get("/api/alerts")
async def get_alerts(limit: int = Query(default=20, ge=1, le=100)):
    """Ambil alert terbaru dari MongoDB."""
    cursor = get_alert_collection().find(
        {}, {"_id": 0}
    ).sort("timestamp", -1).limit(limit)
    alerts = await cursor.to_list(length=limit)
    return alerts


# ─── GET /api/stats ───────────────────────────────────────────────────────────
@app.get("/api/stats")
async def get_stats():
    """Statistik agregat dari 100 pembacaan terakhir."""
    cursor = get_sensor_collection().find(
        {}, {"_id": 0, "temperature": 1, "humidity": 1, "gas_ppm": 1}
    ).sort("timestamp", -1).limit(100)
    docs = await cursor.to_list(length=100)

    if not docs:
        return {"count": 0, "message": "Belum ada data."}

    temps = [d["temperature"] for d in docs if "temperature" in d]
    hums  = [d["humidity"]    for d in docs if "humidity"    in d]
    gases = [d["gas_ppm"]     for d in docs if "gas_ppm"     in d]

    def safe_stats(values: list[float]) -> dict:
        if not values:
            return {}
        return {
            "min":  round(min(values), 2),
            "max":  round(max(values), 2),
            "avg":  round(sum(values) / len(values), 2),
            "last": round(values[0], 2),
        }

    return {
        "count":       len(docs),
        "temperature": safe_stats(temps),
        "humidity":    safe_stats(hums),
        "gas_ppm":     safe_stats(gases),
        "ws_clients":  len(active_websockets),
    }


# ─── Health ───────────────────────────────────────────────────────────────────
@app.get("/")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}
