# PERCOBAAN 09: DASHBOARD IoT – NODE-RED + GRAFANA

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Visualisasi data PLC real-time menggunakan Node-RED dan Grafana  
**Platform:** MiniPC + Node-RED + Grafana + MQTT + InfluxDB  
**Estimasi Waktu:** 120 menit

---

## A. TUJUAN

1. Membangun dashboard IoT real-time menggunakan Node-RED
2. Mengkonfigurasi aliran data dari MQTT ke Node-RED Dashboard
3. Menginstalasi dan mengkonfigurasi Grafana + InfluxDB untuk data time-series
4. Membuat panel monitoring dengan gauge, chart, dan alert

---

## B. INSTALASI

### B.1 Node-RED

```bash
# Install Node.js (minimal v14)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Node-RED
sudo npm install -g --unsafe-perm node-red

# Jalankan Node-RED
node-red
# Buka browser: http://localhost:1880
```

**Install Dashboard Plugin:**
1. Buka Node-RED: `http://localhost:1880`
2. Menu (☰) → **Manage Palette** → tab Install
3. Search: `node-red-dashboard` → klik **Install**
4. Tunggu selesai → klik **Close**

### B.2 InfluxDB + Grafana (Opsional — untuk data time-series)

```bash
# InfluxDB
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/ubuntu focal stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update && sudo apt install -y influxdb
sudo systemctl start influxdb && sudo systemctl enable influxdb

# Buat database
influx -execute "CREATE DATABASE plc_iot"

# Grafana
sudo apt install -y grafana
sudo systemctl start grafana-server && sudo systemctl enable grafana-server
# Buka: http://localhost:3000 (admin/admin)
```

---

## C. FLOW NODE-RED

### C.1 Flow MQTT → Dashboard

Buat flow berikut di Node-RED editor:

**Nodes yang diperlukan:**
```
[mqtt in]  ──► [json]  ──► [function: ekstrak MW0]  ──► [ui_gauge]
                       ──► [function: ekstrak regs]  ──► [ui_chart]
                       ──► [function: cek alarm]    ──► [ui_notification]
```

**Konfigurasi MQTT in node:**
- Server: localhost:1883
- Topic: `plc/line1/data`
- Output: String

**Function node – Ekstrak MW0:**
```javascript
// Ekstrak nilai MW0 (AI0) dan konversi ke tegangan
var data = msg.payload;
var mw0 = data.registers ? data.registers[0] : 0;
var voltage = (mw0 / 4095.0) * 10.0;  // Konversi ADC ke tegangan 0-10V
msg.payload = parseFloat(voltage.toFixed(2));
msg.topic = "Tegangan AI0 (V)";
return msg;
```

**Function node – Counter dan Status:**
```javascript
var data = msg.payload;
var counter = data.registers ? data.registers[1] : 0;
var motor = data.outputs ? data.outputs[0] : false;

// Set warna LED berdasarkan status
msg.payload = motor;
msg.topic = "Motor Status";
return msg;
```

**Function node – Cek Alarm:**
```javascript
var data = msg.payload;
var regs = data.registers || [];
var alarm = null;

if (regs[0] > 3000) {
    alarm = "⚠️ AI0 TINGGI: " + regs[0];
}
if (regs[0] < 100) {
    alarm = "⚠️ AI0 RENDAH: " + regs[0];
}

if (alarm) {
    msg.payload = alarm;
    return msg;
}
return null;  // Tidak ada alarm → tidak lanjut ke node berikut
```

**Konfigurasi UI Gauge:**
- Label: Tegangan AI0
- Value Format: `{{value}} V`
- Range: 0 – 10
- Sectors: 0-3 (green), 3-7 (yellow), 7-10 (red)

**Konfigurasi UI Chart:**
- Label: Tren MW0
- Type: Line chart
- Duration: 5 menit
- Legend: true

### C.2 Export Flow JSON

Simpan flow ini ke file `nodered_flow_percobaan09.json` untuk import ulang:

```json
[{"id":"mqtt_plc","type":"mqtt in","topic":"plc/line1/data",
  "broker":"localhost","port":"1883","qos":"1","x":100,"y":100,"wires":[["json_node"]]},
 {"id":"json_node","type":"json","x":280,"y":100,"wires":[["fn_mw0","fn_status"]]},
 {"id":"fn_mw0","type":"function","name":"Ekstrak MW0",
  "func":"var d=msg.payload;var v=(d.registers?d.registers[0]:0)/4095.0*10;msg.payload=parseFloat(v.toFixed(2));return msg;",
  "x":480,"y":80,"wires":[["gauge_ai0","chart_ai0"]]},
 {"id":"fn_status","type":"function","name":"Status Output",
  "func":"var d=msg.payload;msg.payload=d.outputs?d.outputs[0]:false;return msg;",
  "x":480,"y":130,"wires":[["led_motor"]]}]
```

---

## D. KONFIGURASI GRAFANA (JIKA MENGGUNAKAN INFLUXDB)

### D.1 Script Python – Tulis ke InfluxDB

**`percobaan09_influx_writer.py`:**

```python
#!/usr/bin/env python3
"""
Percobaan 09: MQTT Subscriber → InfluxDB Writer
"""
import json, time, logging
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

MQTT_HOST  = "localhost"
MQTT_TOPIC = "plc/line1/data"

influx = InfluxDBClient(host='localhost', port=8086, database='plc_iot')

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        regs = data.get('registers', [])
        outs = data.get('outputs', [])

        points = []
        for i, val in enumerate(regs):
            points.append({
                "measurement": "plc_register",
                "tags": {"plc_id": str(data.get('plc_id', 1)),
                         "register": f"MW{i}"},
                "time": int(data.get('timestamp', time.time()) * 1e9),
                "fields": {"value": val}
            })
        for i, val in enumerate(outs):
            points.append({
                "measurement": "plc_output",
                "tags": {"plc_id": str(data.get('plc_id', 1)),
                         "output": f"Q0.{i}"},
                "time": int(data.get('timestamp', time.time()) * 1e9),
                "fields": {"value": int(val)}
            })

        influx.write_points(points)
        logging.info(f"InfluxDB: {len(points)} points written")
    except Exception as e:
        logging.error(f"Error: {e}")

logging.basicConfig(level=logging.INFO)
c = mqtt.Client()
c.on_message = on_message
c.connect(MQTT_HOST, 1883, 60)
c.subscribe(MQTT_TOPIC, qos=1)
logging.info("InfluxDB writer berjalan...")
c.loop_forever()
```

### D.2 Konfigurasi Dashboard Grafana

1. Buka Grafana: `http://localhost:3000`
2. **Configuration** → **Data Sources** → **Add data source** → **InfluxDB**
3. URL: `http://localhost:8086`, Database: `plc_iot`
4. **Create** → **Dashboard** → **Add new panel**
5. Query:
   ```sql
   SELECT mean("value") FROM "plc_register"
   WHERE "register" = 'MW0' AND time > now() - 1h
   GROUP BY time(10s)
   ```
6. Visualization: Time series
7. Panel title: "MW0 – Analog Input 0"

---

## E. LANGKAH PERCOBAAN

1. Pastikan gateway MQTT (Percobaan 06) sudah berjalan
2. Jalankan Node-RED: `node-red`
3. Import flow dan konfigurasi sesuai instruksi di atas
4. Deploy flow → buka dashboard `http://localhost:1880/ui`
5. Amati gauge dan chart menampilkan data real-time dari PLC
6. Ubah nilai AI0 PLC (putar potensiometer) — amati perubahan di dashboard
7. (Opsional) Jalankan `percobaan09_influx_writer.py` dan konfigurasi Grafana

---

## F. TABEL PENGAMATAN

| Waktu | MW0 (ADC) | Tegangan (V) | Motor | Dashboard Update? | Latency (s) |
|-------|-----------|-------------|-------|------------------|------------|
| | | | | | |
| | | | | | |
| | | | | | |

**Dashboard digunakan:** ☐ Node-RED ☐ Grafana ☐ Keduanya  
**Latency rata-rata MQTT → Dashboard:** ________ detik

---

## G. PERTANYAAN ANALISIS

1. Jelaskan kelebihan Node-RED dibanding membuat web dashboard manual (HTML/CSS/JS).

2. Mengapa InfluxDB lebih cocok untuk data time-series IoT dibanding PostgreSQL atau SQLite?

3. Bagaimana Anda mengkonfigurasi alert di Grafana agar mengirim notifikasi email/Telegram saat nilai MW0 melebihi threshold?
