#!/usr/bin/env python3
"""Percobaan 06: MQTT Subscriber — Simpan data PLC ke SQLite"""

import json, sqlite3, time, logging
import paho.mqtt.client as mqtt

MQTT_HOST  = "localhost"
MQTT_TOPIC = "plc/#"
DB_FILE    = "plc_history.db"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("subscriber")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS plc_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL, plc_id INTEGER NOT NULL,
        line TEXT, registers TEXT, outputs TEXT, analog TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS alarms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL, alarm_type TEXT,
        alarm_value REAL, threshold REAL)''')
    conn.commit(); conn.close()
    log.info(f"Database '{DB_FILE}' siap")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        if "alarm" in msg.topic:
            conn = sqlite3.connect(DB_FILE)
            alarm = payload.get("alarm", {})
            conn.execute(
                "INSERT INTO alarms (timestamp,alarm_type,alarm_value,threshold) VALUES (?,?,?,?)",
                (payload.get("timestamp", time.time()),
                 alarm.get("type"), alarm.get("value", 0), alarm.get("threshold", 0))
            )
            conn.commit(); conn.close()
            log.warning(f"ALARM: {alarm}")
        else:
            conn = sqlite3.connect(DB_FILE)
            conn.execute(
                "INSERT INTO plc_readings (timestamp,plc_id,line,registers,outputs,analog) "
                "VALUES (?,?,?,?,?,?)",
                (payload.get("timestamp", time.time()), payload.get("plc_id", 0),
                 payload.get("line", ""),
                 json.dumps(payload.get("registers", [])),
                 json.dumps(payload.get("outputs", [])),
                 json.dumps(payload.get("analog", [])))
            )
            conn.commit(); conn.close()
            log.info(f"Disimpan: PLC{payload.get('plc_id')} regs={payload.get('registers',[])[:3]}")
    except Exception as e:
        log.error(f"Error: {e}")


def main():
    init_db()
    client = mqtt.Client(client_id="db_subscriber")
    client.on_message = on_message
    client.connect(MQTT_HOST, 1883, 60)
    client.subscribe(MQTT_TOPIC, qos=1)
    log.info(f"Mendengarkan topic: {MQTT_TOPIC}")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log.info("Subscriber dihentikan")


if __name__ == "__main__":
    main()
