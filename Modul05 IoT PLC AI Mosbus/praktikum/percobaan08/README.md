# PERCOBAAN 08: GATEWAY MODBUS → REST API (PYTHON MINIPC)

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Mengirim data PLC ke REST API Server menggunakan HTTP POST  
**Platform:** MiniPC Python + FastAPI Server + PLC TM221/CP2E  
**Estimasi Waktu:** 90 menit

---

## A. TUJUAN

1. Membangun REST API sederhana untuk menerima data dari edge device menggunakan FastAPI
2. Mengirim data PLC ke server via HTTP POST dari Python
3. Mengakses data terbaru dan riwayat data melalui HTTP GET
4. Memahami perbedaan MQTT vs REST untuk pengiriman data IoT

---

## B. PROGRAM MINIPC PYTHON

### B.1 REST API Server (FastAPI)

**`percobaan08_api_server.py`:**

```python
#!/usr/bin/env python3
"""
Percobaan 08: REST API Server untuk menerima data PLC
Framework: FastAPI + Uvicorn + SQLite
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import json
import time

app = FastAPI(
    title="PLC IoT Gateway API",
    description="API untuk menerima dan menyimpan data dari PLC via edge device",
    version="1.0.0"
)

DB_FILE = "plc_api.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS plc_data (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        received_at REAL    NOT NULL,
        plc_id    INTEGER NOT NULL,
        registers TEXT,
        outputs   TEXT,
        analog    TEXT,
        meta      TEXT
    )''')
    conn.commit()
    conn.close()


init_db()


class PLCPayload(BaseModel):
    plc_id:    int
    registers: List[int]         = []
    outputs:   List[bool]        = []
    analog:    List[int]         = []
    meta:      Optional[dict]    = None


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2>PLC IoT Gateway API</h2>
    <p><a href="/docs">Swagger UI</a> | <a href="/redoc">ReDoc</a></p>
    <ul>
      <li>POST /api/v1/plc/data</li>
      <li>GET  /api/v1/plc/{plc_id}/latest</li>
      <li>GET  /api/v1/plc/{plc_id}/history?limit=20</li>
      <li>GET  /api/v1/stats</li>
    </ul>
    """


@app.post("/api/v1/plc/data", summary="Terima data dari edge device")
async def receive_data(payload: PLCPayload):
    """Terima data PLC dari edge device (MiniPC atau ESP32)"""
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO plc_data (received_at,plc_id,registers,outputs,analog,meta) "
        "VALUES (?,?,?,?,?,?)",
        (
            time.time(),
            payload.plc_id,
            json.dumps(payload.registers),
            json.dumps([bool(o) for o in payload.outputs]),
            json.dumps(payload.analog),
            json.dumps(payload.meta) if payload.meta else None
        )
    )
    conn.commit()
    conn.close()
    return {
        "status":    "ok",
        "plc_id":    payload.plc_id,
        "registers": len(payload.registers),
        "server_ts": time.time()
    }


@app.get("/api/v1/plc/{plc_id}/latest", summary="Data terbaru dari PLC")
async def get_latest(plc_id: int):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute(
        "SELECT received_at,plc_id,registers,outputs,analog "
        "FROM plc_data WHERE plc_id=? ORDER BY received_at DESC LIMIT 1",
        (plc_id,)
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail=f"Data PLC {plc_id} tidak ditemukan")

    return {
        "plc_id":     row[1],
        "received_at": row[0],
        "registers":  json.loads(row[2]),
        "outputs":    json.loads(row[3]),
        "analog":     json.loads(row[4])
    }


@app.get("/api/v1/plc/{plc_id}/history", summary="Riwayat data PLC")
async def get_history(plc_id: int, limit: int = 20):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT received_at,registers FROM plc_data WHERE plc_id=? "
        "ORDER BY received_at DESC LIMIT ?",
        (plc_id, min(limit, 1000))
    ).fetchall()
    conn.close()
    return {
        "plc_id": plc_id,
        "count":  len(rows),
        "data":   [{"ts": r[0], "registers": json.loads(r[1])} for r in rows]
    }


@app.get("/api/v1/stats", summary="Statistik server")
async def get_stats():
    conn = sqlite3.connect(DB_FILE)
    total = conn.execute("SELECT COUNT(*) FROM plc_data").fetchone()[0]
    latest_ts = conn.execute("SELECT MAX(received_at) FROM plc_data").fetchone()[0]
    plcs = conn.execute(
        "SELECT plc_id, COUNT(*) FROM plc_data GROUP BY plc_id"
    ).fetchall()
    conn.close()
    return {
        "total_records": total,
        "latest_ts":     latest_ts,
        "plc_summary":   [{"plc_id": p[0], "count": p[1]} for p in plcs]
    }
```

Jalankan:
```bash
uvicorn percobaan08_api_server:app --host 0.0.0.0 --port 8000 --reload
# Buka Swagger UI: http://localhost:8000/docs
```

### B.2 Gateway Modbus → REST

**`percobaan08_gateway_rest.py`:**

```python
#!/usr/bin/env python3
"""Percobaan 08: Gateway Modbus RTU → REST API"""

import time
import logging
import requests
from pymodbus.client import ModbusSerialClient

PORT     = "/dev/ttyUSB0"
SLAVE_ID = 1
API_URL  = "http://localhost:8000/api/v1/plc/data"
INTERVAL = 2.0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("rest_gateway")

modbus = ModbusSerialClient(port=PORT, baudrate=9600,
                             parity='N', stopbits=1, bytesize=8, timeout=1)
modbus.connect()

while True:
    rr = modbus.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
    rc = modbus.read_coils(address=2048, count=4, slave=SLAVE_ID)

    if not rr.isError():
        payload = {
            "plc_id":    SLAVE_ID,
            "registers": rr.registers,
            "outputs":   [bool(b) for b in rc.bits[:4]] if not rc.isError() else []
        }
        try:
            resp = requests.post(API_URL, json=payload, timeout=5)
            log.info(f"POST {resp.status_code}: {resp.json()}")
        except requests.exceptions.ConnectionError:
            log.warning("API server tidak terjangkau")
        except requests.exceptions.Timeout:
            log.warning("Request timeout")
    else:
        log.error(f"Modbus error: {rr}")

    time.sleep(INTERVAL)
```

---

## C. LANGKAH PERCOBAAN

1. Jalankan API server: `uvicorn percobaan08_api_server:app --host 0.0.0.0 --port 8000`
2. Buka Swagger UI: `http://localhost:8000/docs`
3. Test manual endpoint POST via Swagger UI (isi body JSON)
4. Jalankan gateway: `python percobaan08_gateway_rest.py`
5. Refresh endpoint GET latest dan history di Swagger UI
6. Uji endpoint stats

---

## D. TABEL PENGAMATAN

| No | Method | Endpoint | Status | Waktu (ms) | Keterangan |
|----|--------|----------|--------|-----------|-----------|
| 1 | POST | /api/v1/plc/data | | | |
| 2 | GET | /api/v1/plc/1/latest | | | |
| 3 | GET | /api/v1/plc/1/history | | | |
| 4 | GET | /api/v1/stats | | | |
| 5 | POST | /api/v1/plc/data | | | |

**Total data tersimpan setelah 60 detik:** ________  
**Rata-rata waktu POST:** ________ ms

---

## E. PERTANYAAN ANALISIS

1. Bandingkan overhead HTTP (header, payload, response) vs MQTT. Mengapa MQTT lebih ringan untuk IoT?

2. Jelaskan kelebihan menggunakan Pydantic BaseModel pada FastAPI dibanding menerima raw JSON.

3. Apa kelemahan menggunakan SQLite untuk sistem produksi dengan ratusan PLC? Database apa yang lebih cocok dan mengapa?
