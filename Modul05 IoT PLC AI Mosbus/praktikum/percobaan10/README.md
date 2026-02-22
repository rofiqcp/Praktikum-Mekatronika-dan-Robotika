# PERCOBAAN 10: SISTEM GATEWAY IoT TERINTEGRASI – MODBUS + MQTT + REST + DASHBOARD + AI

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Integrasi penuh: PLC → Edge Device → Server → Dashboard + Deteksi Anomali AI  
**Platform:** PLC TM221/CP2E + ESP32 + MiniPC Python + MQTT + REST + Grafana + AI  
**Estimasi Waktu:** 120 menit

---

## A. TUJUAN

1. Mengintegrasikan semua komponen dari percobaan 1–9 dalam satu sistem end-to-end
2. Menjalankan gateway Python yang mengirim data ke MQTT dan REST API sekaligus
3. Mengintegrasikan data dari PLC (via MiniPC) dan ESP32 (sensor tambahan)
4. Mengimplementasikan deteksi anomali sederhana menggunakan Z-score (statistik sederhana tanpa sklearn)
5. Menampilkan seluruh data di dashboard Node-RED/Grafana

---

## B. ARSITEKTUR SISTEM TERINTEGRASI

```
┌─────────────────────────────────────────────────────────────┐
│                    LAPANGAN                                  │
│                                                             │
│  PLC TM221/CP2E ──RS-485──► MiniPC Python                  │
│        │                         │                          │
│        │ Ethernet                │ MQTT Publish             │
│        └──────────┐              │ REST POST                │
│                   │              │ AI Anomaly Detection      │
│  ESP32 ──WiFi─────┘              │                          │
│  (sensor node)    │              │                          │
│                   │ MQTT Sub     │                          │
└───────────────────┼──────────────┼──────────────────────────┘
                    │              │
         ┌──────────▼──────────────▼──────────┐
         │            SERVER                   │
         │                                     │
         │  Mosquitto MQTT Broker              │
         │  FastAPI REST API                   │
         │  SQLite / InfluxDB Database         │
         │  Node-RED / Grafana Dashboard       │
         └────────────────────────────────────┘
```

---

## C. PROGRAM UTAMA – GATEWAY TERINTEGRASI

**`percobaan10_integrated_gateway.py`:**

```python
#!/usr/bin/env python3
"""
Percobaan 10: Gateway IoT Terintegrasi
PLC Modbus RTU → MQTT + REST API + Anomaly Detection
"""

import time
import json
import logging
import threading
import sqlite3
from collections import deque

import requests
import paho.mqtt.client as mqtt
from pymodbus.client import ModbusSerialClient

# ============================================================
# KONFIGURASI
# ============================================================
PORT         = "/dev/ttyUSB0"
SLAVE_ID     = 1
MQTT_HOST    = "localhost"
MQTT_PORT    = 1883
API_URL      = "http://localhost:8000/api/v1/plc/data"
POLL_INTERVAL = 1.0
AI_WINDOW     = 20      # Ukuran window untuk deteksi anomali
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
log = logging.getLogger("integrated_gw")


class AnomalyDetector:
    """Deteksi anomali sederhana menggunakan Z-score (tanpa sklearn)"""

    def __init__(self, window_size=20, z_threshold=3.0):
        self.window   = deque(maxlen=window_size)
        self.threshold = z_threshold

    def update(self, value):
        self.window.append(value)

    def is_anomaly(self, value):
        if len(self.window) < 5:
            return False  # Butuh data cukup dulu
        mean = sum(self.window) / len(self.window)
        variance = sum((x - mean) ** 2 for x in self.window) / len(self.window)
        std = variance ** 0.5
        if std == 0:
            return False
        z_score = abs(value - mean) / std
        return z_score > self.threshold

    @property
    def baseline(self):
        if not self.window:
            return 0
        return sum(self.window) / len(self.window)


class IntegratedGateway:

    def __init__(self):
        # Modbus
        self.modbus = ModbusSerialClient(
            port=PORT, baudrate=9600,
            parity='N', stopbits=1, bytesize=8, timeout=1
        )
        # MQTT
        self.mq = mqtt.Client(client_id="integrated_gw")
        self.mq.on_connect = lambda c, u, f, rc: log.info(
            f"MQTT {'OK' if rc==0 else f'Error rc={rc}'}"
        )
        self.mq.reconnect_delay_set(min_delay=1, max_delay=30)

        # Anomaly detectors per register
        self.detectors = [AnomalyDetector() for _ in range(10)]

        # Statistik
        self.stats = {
            'poll_count': 0, 'mqtt_pub': 0, 'rest_post': 0,
            'anomalies': 0, 'errors': 0
        }

        # Database lokal untuk buffering
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect("gateway_buffer.db")
        conn.execute('''CREATE TABLE IF NOT EXISTS buffer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL, data TEXT, sent INTEGER DEFAULT 0)''')
        conn.commit(); conn.close()

    def connect(self):
        if not self.modbus.connect():
            log.error(f"Gagal connect Modbus RTU ke {PORT}")
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
            "timestamp": time.time(),
            "plc_id":    SLAVE_ID,
            "registers": rr.registers,
            "outputs":   [bool(b) for b in rc.bits[:4]] if not rc.isError() else [],
            "analog":    ri.registers if not ri.isError() else []
        }

    def deteksi_anomali(self, data):
        """Deteksi anomali pada setiap register"""
        anomalies = []
        regs = data.get('registers', [])
        for i, val in enumerate(regs):
            self.detectors[i].update(val)
            if self.detectors[i].is_anomaly(val):
                anomalies.append({
                    "register": i,
                    "value":    val,
                    "baseline": round(self.detectors[i].baseline, 1)
                })
        return anomalies

    def publish_mqtt(self, data):
        payload = json.dumps(data)
        result  = self.mq.publish("plc/line1/data", payload, qos=1)
        if result.rc == 0:
            self.stats['mqtt_pub'] += 1

    def post_rest(self, data):
        try:
            resp = requests.post(API_URL, json=data, timeout=3)
            if resp.status_code == 200:
                self.stats['rest_post'] += 1
        except Exception:
            pass  # Simpan ke buffer lokal jika gagal

    def buffer_data(self, data):
        """Simpan ke SQLite sebagai buffer lokal"""
        conn = sqlite3.connect("gateway_buffer.db")
        conn.execute("INSERT INTO buffer (timestamp, data, sent) VALUES (?,?,0)",
                     (data['timestamp'], json.dumps(data)))
        conn.commit(); conn.close()

    def print_stats(self):
        log.info(
            f"Stats: poll={self.stats['poll_count']} "
            f"mqtt={self.stats['mqtt_pub']} "
            f"rest={self.stats['rest_post']} "
            f"anomali={self.stats['anomalies']} "
            f"error={self.stats['errors']}"
        )

    def run(self):
        if not self.connect():
            return

        log.info("=== Gateway Terintegrasi berjalan ===")
        log.info("Ctrl+C untuk berhenti")

        last_stats = time.time()

        try:
            while True:
                data = self.baca_plc()
                if data:
                    self.stats['poll_count'] += 1

                    # 1. Buffering lokal
                    self.buffer_data(data)

                    # 2. Publish ke MQTT (async)
                    self.publish_mqtt(data)

                    # 3. POST ke REST API
                    self.post_rest(data)

                    # 4. Deteksi anomali
                    anomalies = self.deteksi_anomali(data)
                    if anomalies:
                        self.stats['anomalies'] += len(anomalies)
                        for a in anomalies:
                            log.warning(f"ANOMALI: MW{a['register']}={a['value']} "
                                        f"(baseline={a['baseline']})")
                            self.mq.publish(
                                "plc/line1/alarm",
                                json.dumps({"timestamp": time.time(), "anomaly": a}),
                                qos=2
                            )

                    # Log setiap 10 detik
                    if time.time() - last_stats > 10:
                        self.print_stats()
                        last_stats = time.time()

                time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            log.info("\nGateway dihentikan")
            self.print_stats()
        finally:
            self.modbus.close()
            self.mq.loop_stop()
            self.mq.disconnect()


if __name__ == "__main__":
    gw = IntegratedGateway()
    gw.run()
```

---

## D. PROGRAM ESP32 – SENSOR NODE

**Lihat file `src/main.cpp` di direktori ini.**

ESP32 berperan sebagai sensor node tambahan yang mengirim data ke MQTT broker secara independen.

---

## E. LANGKAH PERCOBAAN

1. Pastikan semua komponen dari Percobaan 1–9 sudah dikonfigurasi
2. Jalankan Mosquitto MQTT Broker
3. Jalankan FastAPI Server: `uvicorn percobaan08_api_server:app --port 8000`
4. Jalankan Node-RED dan deploy flow
5. Jalankan gateway terintegrasi: `python percobaan10_integrated_gateway.py`
6. Upload program ESP32 sensor node
7. Amati dashboard Node-RED menampilkan data dari dua sumber (PLC via MiniPC + ESP32)
8. Simulasikan anomali: ubah nilai AI PLC secara drastis (jauh dari baseline)
9. Amati alert anomali di MQTT Explorer dan dashboard
10. Verifikasi data tersimpan di database lokal (`gateway_buffer.db`)

---

## F. TABEL PENGAMATAN

| Parameter | Nilai |
|-----------|-------|
| Total poll dalam 60 detik | |
| Total MQTT publish berhasil | |
| Total REST POST berhasil | |
| Total anomali terdeteksi | |
| Total error Modbus | |
| Jumlah record di buffer DB | |
| Dashboard update interval | |
| ESP32 MQTT publish rate | |

---

## G. ANALISIS SISTEM TERINTEGRASI

Isi berdasarkan hasil percobaan:

| Aspek | Hasil | Catatan |
|-------|-------|---------|
| Keandalan Modbus RTU | ___% sukses | |
| Keandalan MQTT publish | ___% sukses | |
| Keandalan REST POST | ___% sukses | |
| Latensi PLC → Dashboard | ___ detik | |
| Akurasi anomaly detection | | |

---

## H. PERTANYAAN ANALISIS

1. **Sistem end-to-end:** Identifikasi semua titik kegagalan (SPOF - Single Point of Failure) dalam arsitektur sistem yang Anda bangun. Bagaimana meningkatkan keandalan masing-masing?

2. **Skalabilitas:** Jika sistem ini harus menangani 100 PLC berbeda, komponen mana yang perlu di-upgrade/diganti? Berikan estimasi spesifikasi hardware yang dibutuhkan.

3. **AI/Anomaly Detection:** Jelaskan keterbatasan metode Z-score untuk deteksi anomali pada data proses industri. Metode apa yang lebih baik untuk data time-series industri?

4. **Edge vs Cloud:** Kapan lebih baik memproses data di edge device (MiniPC/ESP32) dibanding mengirim semua raw data ke cloud untuk diproses?

5. **Keamanan:** Identifikasi minimal 3 celah keamanan pada sistem yang Anda bangun dan berikan solusi konkret untuk masing-masing.

---

## I. REFERENSI

- pymodbus: https://pymodbus.readthedocs.io
- paho-mqtt: https://pypi.org/project/paho-mqtt/
- FastAPI: https://fastapi.tiangolo.com
- Node-RED: https://nodered.org
- Grafana: https://grafana.com
- Isolation Forest: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html
- Modbus Specification: https://modbus.org
