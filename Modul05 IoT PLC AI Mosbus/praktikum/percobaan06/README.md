# PERCOBAAN 06: GATEWAY MODBUS RTU → MQTT (PYTHON MINIPC)

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** Mengirim data PLC ke MQTT Broker menggunakan Python  
**Platform:** MiniPC Python + Mosquitto MQTT + PLC TM221/CP2E  
**Estimasi Waktu:** 90 menit

---

## A. TUJUAN

1. Memahami konsep MQTT (broker, publisher, subscriber, topic, QoS)
2. Menginstalasi dan mengkonfigurasi Mosquitto MQTT Broker
3. Membangun gateway PLC Modbus RTU → MQTT menggunakan Python
4. Menyimpan data PLC ke database SQLite melalui MQTT subscriber
5. Memonitor data PLC real-time menggunakan MQTT Explorer

---

## B. SETUP MQTT BROKER (MOSQUITTO)

```bash
# Install Mosquitto di Linux (Ubuntu/Debian/Raspberry Pi OS)
sudo apt update && sudo apt install -y mosquitto mosquitto-clients

# Start dan enable service
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Verifikasi status
sudo systemctl status mosquitto

# Konfigurasi (buka file config)
sudo nano /etc/mosquitto/mosquitto.conf
```

**Isi file `/etc/mosquitto/mosquitto.conf`:**
```
listener 1883
allow_anonymous true
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
```

```bash
# Restart setelah edit config
sudo systemctl restart mosquitto

# Test: buka dua terminal
# Terminal 1 (subscriber):
mosquitto_sub -h localhost -t "plc/#" -v

# Terminal 2 (publisher):
mosquitto_pub -h localhost -t "plc/test" -m '{"hello":"world"}'
```

---

## C. PROGRAM PYTHON – GATEWAY

**`percobaan06_gateway_mqtt.py`:**

```python
#!/usr/bin/env python3
"""
Percobaan 06: Gateway Modbus RTU → MQTT
PLC TM221/CP2E → MiniPC Python → Mosquitto MQTT Broker
"""

import time
import json
import logging
from pymodbus.client import ModbusSerialClient
import paho.mqtt.client as mqtt

# ============================================================
# KONFIGURASI
# ============================================================
PORT         = "/dev/ttyUSB0"
BAUDRATE     = 9600
SLAVE_ID     = 1
MQTT_HOST    = "localhost"
MQTT_PORT    = 1883
MQTT_TOPIC   = "plc/line1/data"
TOPIC_ALARM  = "plc/line1/alarm"
POLL_INTERVAL = 1.0
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
log = logging.getLogger("gateway")

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("MQTT Broker terhubung")
    else:
        log.error(f"MQTT error rc={rc}")

def on_disconnect(client, userdata, rc):
    log.warning("MQTT terputus, akan reconnect otomatis...")

def on_publish(client, userdata, mid):
    log.debug(f"MQTT published mid={mid}")

# Inisialisasi Modbus
modbus = ModbusSerialClient(
    port=PORT, baudrate=BAUDRATE,
    parity='N', stopbits=1, bytesize=8, timeout=1
)

# Inisialisasi MQTT
mq = mqtt.Client(client_id="plc_gateway_rtu", clean_session=True)
mq.on_connect    = on_connect
mq.on_disconnect = on_disconnect
mq.on_publish    = on_publish
mq.reconnect_delay_set(min_delay=1, max_delay=30)


def baca_plc():
    """Baca semua data dari PLC, kembalikan dict atau None jika error"""
    data = {}

    rr = modbus.read_holding_registers(address=0, count=10, slave=SLAVE_ID)
    if not rr.isError():
        data['registers'] = rr.registers
    else:
        log.warning(f"Gagal baca HR: {rr}")
        return None

    rc = modbus.read_coils(address=2048, count=4, slave=SLAVE_ID)
    if not rc.isError():
        data['outputs'] = [bool(b) for b in rc.bits[:4]]
    else:
        data['outputs'] = []

    ri = modbus.read_input_registers(address=256, count=2, slave=SLAVE_ID)
    if not ri.isError():
        data['analog'] = ri.registers
    else:
        data['analog'] = []

    return data


def cek_alarm(data):
    """Cek kondisi alarm berdasarkan nilai register"""
    alarms = []
    regs = data.get('registers', [])

    # Alarm jika MW0 (AI0) > 3000 (threshold ~7.3V)
    if len(regs) > 0 and regs[0] > 3000:
        alarms.append({"type": "HIGH_AI0", "value": regs[0], "threshold": 3000})

    # Alarm jika MW1 (counter) berhenti naik — PLC mungkin tidak berjalan
    # (implementasi sederhana)

    return alarms


def buat_payload(data):
    """Buat JSON payload untuk MQTT"""
    return {
        "timestamp": time.time(),
        "plc_id": SLAVE_ID,
        "line": "line1",
        "registers": data.get('registers', []),
        "outputs": data.get('outputs', []),
        "analog": data.get('analog', [])
    }


def main():
    log.info("=== PLC MQTT Gateway dimulai ===")

    # Connect Modbus
    if not modbus.connect():
        log.error(f"Gagal connect Modbus RTU ke {PORT}")
        return
    log.info(f"Modbus RTU terhubung ke {PORT} (Slave {SLAVE_ID})")

    # Connect MQTT
    try:
        mq.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
    except Exception as e:
        log.error(f"Gagal connect MQTT: {e}")
        modbus.close()
        return
    mq.loop_start()

    log.info(f"Mengirim data ke MQTT topic: {MQTT_TOPIC}")
    log.info("Tekan Ctrl+C untuk berhenti")

    pesan_count = 0
    error_count = 0

    try:
        while True:
            data = baca_plc()
            if data:
                payload = buat_payload(data)
                result = mq.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
                if result.rc == 0:
                    pesan_count += 1
                    log.info(f"[{pesan_count}] Published: regs={data['registers'][:4]}...")
                else:
                    log.warning(f"Publish gagal: rc={result.rc}")

                # Cek dan publish alarm jika ada
                alarms = cek_alarm(data)
                for alarm in alarms:
                    mq.publish(
                        TOPIC_ALARM,
                        json.dumps({"timestamp": time.time(), "alarm": alarm}),
                        qos=2
                    )
                    log.warning(f"ALARM: {alarm}")

            else:
                error_count += 1
                log.error(f"Gagal baca PLC (total error: {error_count})")

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        log.info(f"\nDihentikan. Total pesan: {pesan_count}, Error: {error_count}")
    finally:
        modbus.close()
        mq.loop_stop()
        mq.disconnect()
        log.info("Gateway berhenti")


if __name__ == "__main__":
    main()
```

**`percobaan06_subscriber_db.py` – Simpan data ke SQLite:**

```python
#!/usr/bin/env python3
"""
Percobaan 06: MQTT Subscriber yang menyimpan data ke SQLite
"""

import json
import sqlite3
import time
import logging
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
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp     REAL    NOT NULL,
        plc_id        INTEGER NOT NULL,
        line          TEXT,
        registers     TEXT,
        outputs       TEXT,
        analog        TEXT
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS alarms (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp     REAL    NOT NULL,
        alarm_type    TEXT,
        alarm_value   REAL,
        threshold     REAL
    )''')
    conn.commit()
    conn.close()
    log.info(f"Database '{DB_FILE}' siap")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        topic   = msg.topic

        if "alarm" in topic:
            # Simpan alarm
            conn = sqlite3.connect(DB_FILE)
            alarm = payload.get("alarm", {})
            conn.execute(
                "INSERT INTO alarms (timestamp, alarm_type, alarm_value, threshold) VALUES (?,?,?,?)",
                (payload.get("timestamp", time.time()),
                 alarm.get("type", "UNKNOWN"),
                 alarm.get("value", 0),
                 alarm.get("threshold", 0))
            )
            conn.commit()
            conn.close()
            log.warning(f"ALARM disimpan: {alarm}")

        else:
            # Simpan data sensor
            conn = sqlite3.connect(DB_FILE)
            conn.execute(
                "INSERT INTO plc_readings (timestamp,plc_id,line,registers,outputs,analog) "
                "VALUES (?,?,?,?,?,?)",
                (
                    payload.get("timestamp", time.time()),
                    payload.get("plc_id", 0),
                    payload.get("line", ""),
                    json.dumps(payload.get("registers", [])),
                    json.dumps(payload.get("outputs", [])),
                    json.dumps(payload.get("analog", []))
                )
            )
            conn.commit()
            conn.close()
            regs = payload.get("registers", [])
            log.info(f"Disimpan: PLC{payload.get('plc_id')} regs={regs[:3]}...")

    except Exception as e:
        log.error(f"Error proses pesan: {e}")


def main():
    init_db()
    client = mqtt.Client(client_id="db_subscriber")
    client.on_message = on_message
    client.connect(MQTT_HOST, 1883, 60)
    client.subscribe(MQTT_TOPIC, qos=1)
    log.info(f"Subscriber berjalan, mendengarkan topic: {MQTT_TOPIC}")
    log.info("Tekan Ctrl+C untuk berhenti")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        log.info("Subscriber dihentikan")


if __name__ == "__main__":
    main()
```

---

## D. LANGKAH PERCOBAAN

1. Install Mosquitto dan verifikasi berjalan
2. Buka 3 terminal:
   - Terminal 1: `mosquitto_sub -t "plc/#" -v` (monitor semua topic)
   - Terminal 2: `python percobaan06_subscriber_db.py` (simpan ke DB)
   - Terminal 3: `python percobaan06_gateway_mqtt.py` (gateway)
3. Amati data mengalir dari PLC → Gateway → Subscriber
4. Buka MQTT Explorer, sambungkan ke `localhost:1883`, lihat tree topic `plc/`
5. Ubah nilai potentiometer pada AI0 PLC — amati perubahan di subscriber

---

## E. TABEL PENGAMATAN

| Iterasi | Topic | Payload (singkat) | QoS | Diterima Subscriber? |
|---------|-------|------------------|-----|---------------------|
| 1 | plc/line1/data | {regs:[...],...} | 1 | |
| 2 | plc/line1/data | | 1 | |
| 3 | plc/line1/data | | 1 | |

**Rata-rata interval:** ________ detik  
**MQTT Broker:** ________ (IP/hostname)  
**Total pesan dalam 60 detik:** ________  
**Total disimpan ke database:** ________

---

## F. PERTANYAAN ANALISIS

1. Jelaskan perbedaan QoS 0, 1, dan 2 pada MQTT. Mana yang paling tepat untuk data sensor PLC? Berikan alasan teknis.

2. Apa fungsi `mq.loop_start()` dibanding `mq.loop_forever()`? Kapan masing-masing digunakan?

3. Apa yang terjadi jika MQTT Broker tidak bisa dijangkau? Bagaimana Anda menangani data loss pada edge device?
