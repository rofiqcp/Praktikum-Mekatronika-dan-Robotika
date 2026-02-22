#!/usr/bin/env python3
"""
Percobaan 09: MQTT Subscriber → InfluxDB Writer untuk Grafana
"""
import json, time, logging
import paho.mqtt.client as mqtt

MQTT_HOST  = "localhost"
MQTT_TOPIC = "plc/line1/data"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("influx_writer")

# Coba import influxdb, jika tidak ada tampilkan pesan instalasi
try:
    from influxdb import InfluxDBClient
    influx = InfluxDBClient(host='localhost', port=8086, database='plc_iot')
    log.info("InfluxDB client siap")
    USE_INFLUX = True
except ImportError:
    log.warning("Library 'influxdb' tidak terinstall. Jalankan: pip install influxdb")
    log.warning("Script akan berjalan dalam mode fallback (print ke konsol). Data TIDAK disimpan ke InfluxDB.")
    USE_INFLUX = False


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        regs = data.get('registers', [])
        outs = data.get('outputs', [])
        ts_ns = int(data.get('timestamp', time.time()) * 1e9)

        if USE_INFLUX:
            points = []
            for i, val in enumerate(regs):
                points.append({
                    "measurement": "plc_register",
                    "tags": {"plc_id": str(data.get('plc_id', 1)),
                             "register": f"MW{i}"},
                    "time": ts_ns,
                    "fields": {"value": int(val)}
                })
            for i, val in enumerate(outs):
                points.append({
                    "measurement": "plc_output",
                    "tags": {"plc_id": str(data.get('plc_id', 1)),
                             "output": f"Q0.{i}"},
                    "time": ts_ns,
                    "fields": {"value": int(val)}
                })
            influx.write_points(points)
            log.info(f"InfluxDB: {len(points)} points written (ts={ts_ns})")
        else:
            # Fallback: tampilkan data
            log.info(f"Data PLC{data.get('plc_id')}: regs={regs[:4]}, outs={outs}")

    except Exception as e:
        log.error(f"Error proses pesan: {e}")


c = mqtt.Client(client_id="influx_writer")
c.on_message = on_message
c.connect(MQTT_HOST, 1883, 60)
c.subscribe(MQTT_TOPIC, qos=1)
log.info(f"Mendengarkan MQTT topic: {MQTT_TOPIC}")
log.info("Tekan Ctrl+C untuk berhenti")
try:
    c.loop_forever()
except KeyboardInterrupt:
    log.info("Dihentikan")
