"""
Percobaan 2 – Flask Backend
Provides REST API to store and retrieve DHT22 sensor readings from PostgreSQL.
"""

import os
from datetime import datetime, timedelta

import psycopg2
import psycopg2.extras
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# ─── Configuration ────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/iot_db"
)

app = Flask(__name__)
CORS(app)

# ─── Database helpers ─────────────────────────────────────────────────────────
def get_conn():
    """Open a new connection (no pooling – sufficient for practicum scale)."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)

def init_db():
    """Create the sensor_readings table if it does not exist."""
    ddl = """
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id          SERIAL PRIMARY KEY,
        device      VARCHAR(50),
        temperature FLOAT,
        humidity    FLOAT,
        heat_index  FLOAT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_recorded_at ON sensor_readings(recorded_at);
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.post("/api/sensor")
def create_reading():
    """Accept one DHT22 reading from the edge subscriber and persist it."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    device      = data.get("device",      "unknown")
    temperature = data.get("temperature")
    humidity    = data.get("humidity")
    heat_index  = data.get("heat_index")

    if temperature is None or humidity is None:
        return jsonify({"error": "'temperature' and 'humidity' are required"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sensor_readings (device, temperature, humidity, heat_index)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, recorded_at
                    """,
                    (device, temperature, humidity, heat_index),
                )
                row = cur.fetchone()
            conn.commit()
        return jsonify({
            "ok":          True,
            "id":          row["id"],
            "recorded_at": row["recorded_at"].isoformat(),
        })
    except psycopg2.Error as exc:
        app.logger.error("DB insert error: %s", exc)
        return jsonify({"error": "Database error", "detail": str(exc)}), 500


@app.get("/api/sensor")
def get_readings():
    """Return recent sensor readings (default limit=100)."""
    try:
        limit = int(request.args.get("limit", 100))
        limit = max(1, min(limit, 1000))   # clamp to [1, 1000]
    except ValueError:
        return jsonify({"error": "Invalid 'limit' parameter"}), 400

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, device, temperature, humidity, heat_index, recorded_at
                    FROM   sensor_readings
                    ORDER  BY recorded_at DESC
                    LIMIT  %s
                    """,
                    (limit,),
                )
                rows = cur.fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["recorded_at"] = r["recorded_at"].isoformat() if r["recorded_at"] else None
            result.append(r)
        return jsonify(result)
    except psycopg2.Error as exc:
        app.logger.error("DB select error: %s", exc)
        return jsonify({"error": "Database error"}), 500


@app.get("/api/sensor/stats")
def get_stats():
    """Return min/max/avg temperature and humidity over the last 1 hour."""
    since = datetime.utcnow() - timedelta(hours=1)

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        COUNT(*)            AS count,
                        MIN(temperature)    AS temp_min,
                        MAX(temperature)    AS temp_max,
                        AVG(temperature)    AS temp_avg,
                        MIN(humidity)       AS hum_min,
                        MAX(humidity)       AS hum_max,
                        AVG(humidity)       AS hum_avg
                    FROM sensor_readings
                    WHERE recorded_at >= %s
                    """,
                    (since,),
                )
                row = cur.fetchone()

        def fmt(v):
            return round(float(v), 2) if v is not None else None

        return jsonify({
            "period":   "last_1_hour",
            "count":    row["count"],
            "temperature": {
                "min": fmt(row["temp_min"]),
                "max": fmt(row["temp_max"]),
                "avg": fmt(row["temp_avg"]),
            },
            "humidity": {
                "min": fmt(row["hum_min"]),
                "max": fmt(row["hum_max"]),
                "avg": fmt(row["hum_avg"]),
            },
        })
    except psycopg2.Error as exc:
        app.logger.error("DB stats error: %s", exc)
        return jsonify({"error": "Database error"}), 500


# ─── Startup ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        init_db()
        print("[DB] Table sensor_readings ready.")
    except psycopg2.Error as exc:
        print(f"[WARN] Could not initialise DB on startup: {exc}")

    app.run(host="0.0.0.0", port=5000, debug=False)
