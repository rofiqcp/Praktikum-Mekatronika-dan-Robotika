#!/usr/bin/env python3
"""Percobaan 08: REST API Server untuk data PLC (FastAPI + SQLite)"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3, json, time

app = FastAPI(title="PLC IoT Gateway API", version="1.0.0")
DB_FILE = "plc_api.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS plc_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        received_at REAL NOT NULL, plc_id INTEGER NOT NULL,
        registers TEXT, outputs TEXT, analog TEXT)''')
    conn.commit(); conn.close()


init_db()


class PLCPayload(BaseModel):
    plc_id:    int
    registers: List[int]      = []
    outputs:   List[bool]     = []
    analog:    List[int]      = []
    meta:      Optional[dict] = None


@app.get("/", response_class=HTMLResponse)
def root():
    return ("<h2>PLC IoT API</h2><a href='/docs'>Swagger UI</a>")


@app.post("/api/v1/plc/data")
async def receive_data(payload: PLCPayload):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO plc_data (received_at,plc_id,registers,outputs,analog) VALUES (?,?,?,?,?)",
        (time.time(), payload.plc_id,
         json.dumps(payload.registers),
         json.dumps([bool(o) for o in payload.outputs]),
         json.dumps(payload.analog))
    )
    conn.commit(); conn.close()
    return {"status": "ok", "plc_id": payload.plc_id,
            "registers": len(payload.registers), "server_ts": time.time()}


@app.get("/api/v1/plc/{plc_id}/latest")
async def get_latest(plc_id: int):
    conn = sqlite3.connect(DB_FILE)
    row = conn.execute(
        "SELECT received_at,plc_id,registers,outputs,analog FROM plc_data "
        "WHERE plc_id=? ORDER BY received_at DESC LIMIT 1", (plc_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail=f"Data PLC {plc_id} tidak ditemukan")
    return {"plc_id": row[1], "received_at": row[0],
            "registers": json.loads(row[2]), "outputs": json.loads(row[3])}


@app.get("/api/v1/plc/{plc_id}/history")
async def get_history(plc_id: int, limit: int = 20):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT received_at,registers FROM plc_data WHERE plc_id=? "
        "ORDER BY received_at DESC LIMIT ?", (plc_id, min(limit, 1000))
    ).fetchall()
    conn.close()
    return {"plc_id": plc_id, "count": len(rows),
            "data": [{"ts": r[0], "registers": json.loads(r[1])} for r in rows]}


@app.get("/api/v1/stats")
async def get_stats():
    conn = sqlite3.connect(DB_FILE)
    total = conn.execute("SELECT COUNT(*) FROM plc_data").fetchone()[0]
    latest = conn.execute("SELECT MAX(received_at) FROM plc_data").fetchone()[0]
    plcs = conn.execute(
        "SELECT plc_id, COUNT(*) FROM plc_data GROUP BY plc_id").fetchall()
    conn.close()
    return {"total_records": total, "latest_ts": latest,
            "plc_summary": [{"plc_id": p[0], "count": p[1]} for p in plcs]}
