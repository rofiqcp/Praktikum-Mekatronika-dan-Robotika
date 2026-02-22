#!/usr/bin/env python3
"""
Percobaan 10: Gateway IoT Terintegrasi
PLC Modbus RTU → MQTT + REST API + Anomaly Detection (Z-score)
"""

import time, json, logging, sqlite3
from collections import deque
import requests
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusSerialClient

PORT          = "/dev/ttyUSB0"
SLAVE_ID      = 1
MQTT_HOST     = "localhost"
MQTT_PORT     = 1883
API_URL       = "http://localhost:8000/api/v1/plc/data"
POLL_INTERVAL = 1.0

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("integrated_gw")


class AnomalyDetector:
    def __init__(self, window=20, z_thr=3.0):
        self.window = deque(maxlen=window)
        self.z_thr  = z_thr

    def update(self, v):
        self.window.append(v)

    def is_anomaly(self, v):
        if len(self.window) < 5:
            return False
        mean = sum(self.window) / len(self.window)
        std  = (sum((x - mean) ** 2 for x in self.window) / len(self.window)) ** 0.5
        return std > 0 and abs(v - mean) / std > self.z_thr

    @property
    def baseline(self):
        return round(sum(self.window) / len(self.window), 1) if self.window else 0


class IntegratedGateway:
    def __init__(self):
        self.modbus = ModbusSerialClient(port=PORT, baudrate=9600,
                                          parity='N', stopbits=1, bytesize=8, timeout=1)
        self.mq = mqtt.Client(client_id="integrated_gw")
        self.mq.on_connect = lambda c, u, f, rc: log.info(
            f"MQTT {'OK' if rc==0 else f'Error rc={rc}'}")
        self.mq.reconnect_delay_set(min_delay=1, max_delay=30)
        self.detectors = [AnomalyDetector() for _ in range(10)]
        self.stats = {'poll': 0, 'mqtt': 0, 'rest': 0, 'anomaly': 0, 'errors': 0}
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect("gateway_buffer.db")
        conn.execute('''CREATE TABLE IF NOT EXISTS buffer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL, data TEXT, sent INTEGER DEFAULT 0)''')
        conn.commit(); conn.close()

    def connect(self):
        if not self.modbus.connect():
            log.error(f"Gagal Modbus RTU ke {PORT}")
            return False
        try:
            self.mq.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            self.mq.loop_start()
        except Exception as e:
            log.warning(f"MQTT tidak tersedia: {e}")
        log.info("Gateway terhubung")
        return True

    def baca_plc(self):
        rr = self.modbus.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
        if rr.isError():
            self.stats['errors'] += 1
            return None
        rc = self.modbus.read_coils(address=2048, count=4, slave=SLAVE_ID)
        ri = self.modbus.read_input_registers(address=256, count=2, slave=SLAVE_ID)
        return {
            "timestamp": time.time(), "plc_id": SLAVE_ID,
            "registers": rr.registers,
            "outputs":   [bool(b) for b in rc.bits[:4]] if not rc.isError() else [],
            "analog":    ri.registers if not ri.isError() else []
        }

    def cek_anomali(self, data):
        anomalies = []
        for i, val in enumerate(data.get('registers', [])):
            self.detectors[i].update(val)
            if self.detectors[i].is_anomaly(val):
                anomalies.append({"reg": i, "val": val, "base": self.detectors[i].baseline})
        return anomalies

    def publish_mqtt(self, data):
        r = self.mq.publish("plc/line1/data", json.dumps(data), qos=1)
        if r.rc == 0:
            self.stats['mqtt'] += 1

    def post_rest(self, data):
        try:
            resp = requests.post(API_URL, json=data, timeout=3)
            if resp.status_code == 200:
                self.stats['rest'] += 1
        except Exception:
            pass

    def buffer(self, data):
        conn = sqlite3.connect("gateway_buffer.db")
        conn.execute("INSERT INTO buffer (timestamp,data,sent) VALUES (?,?,0)",
                     (data['timestamp'], json.dumps(data)))
        conn.commit(); conn.close()

    def run(self):
        if not self.connect():
            return
        log.info("=== Gateway Terintegrasi berjalan === Ctrl+C untuk berhenti")
        t_stats = time.time()
        try:
            while True:
                data = self.baca_plc()
                if data:
                    self.stats['poll'] += 1
                    self.buffer(data)
                    self.publish_mqtt(data)
                    self.post_rest(data)
                    for a in self.cek_anomali(data):
                        self.stats['anomaly'] += 1
                        log.warning(f"ANOMALI MW{a['reg']}={a['val']} (base={a['base']})")
                        self.mq.publish("plc/line1/alarm",
                                        json.dumps({"ts": time.time(), "anomaly": a}), qos=2)
                if time.time() - t_stats > 10:
                    log.info(f"Stats: {self.stats}")
                    t_stats = time.time()
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            log.info(f"Dihentikan. Final stats: {self.stats}")
        finally:
            self.modbus.close()
            self.mq.loop_stop()
            self.mq.disconnect()


if __name__ == "__main__":
    IntegratedGateway().run()
