# JOBSHEET MODUL 05: KOMUNIKASI MODBUS PLC DENGAN EDGE DEVICE DAN SERVER IoT

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 05 – IoT PLC AI Modbus  
**Platform:** Schneider TM221 / Omron CP2E, ESP32 (PlatformIO), MiniPC Python  
**Pertemuan:** 9–10 (2 × 2 SKS)  
**Tanggal:** ___________________  
**Nama Kelompok:** ___________________  
**Anggota:**

| No | Nama | NIM |
|----|------|-----|
| 1  |      |     |
| 2  |      |     |
| 3  |      |     |
| 4  |      |     |

---

## A. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menjelaskan konsep protokol Modbus RTU dan Modbus TCP serta perbedaannya
2. Mengkonfigurasi PLC Schneider TM221 atau Omron CP2E sebagai Modbus slave
3. Mengimplementasikan komunikasi Modbus RTU antara PLC dan MiniPC menggunakan Python (pymodbus)
4. Mengimplementasikan komunikasi Modbus RTU antara PLC dan ESP32 menggunakan PlatformIO
5. Mengimplementasikan komunikasi Modbus TCP antara PLC dan edge device
6. Mengirimkan data real-time dari PLC ke server melalui protokol MQTT
7. Mengirimkan data dari PLC ke server melalui REST API (HTTP POST)
8. Memvisualisasikan data PLC pada dashboard IoT (Node-RED / Grafana)
9. Membangun sistem gateway IoT industri yang terintegrasi

---

## B. KOMPETENSI YANG DICAPAI (CPMK)

| Kode | CPMK | Indikator Pencapaian |
|------|------|---------------------|
| **CPMK-1** | Mampu mengkonfigurasi PLC sebagai Modbus slave (RTU & TCP) | Konfigurasi EMEB/CX-Programmer, Slave ID, parameter serial |
| **CPMK-2** | Mampu membangun komunikasi Modbus dengan Python | Baca/tulis holding register dan coil via pymodbus |
| **CPMK-3** | Mampu membangun komunikasi Modbus dengan ESP32 | Program PlatformIO membaca dan menulis register PLC |
| **CPMK-4** | Mampu mengintegrasikan data PLC ke MQTT | Publish JSON data PLC ke MQTT broker |
| **CPMK-5** | Mampu mengintegrasikan data PLC ke REST API | HTTP POST data PLC ke FastAPI/Flask server |
| **CPMK-6** | Mampu memvisualisasikan data PLC pada dashboard | Dashboard Node-RED atau Grafana menampilkan data real-time |

---

## C. ALAT DAN BAHAN

### C.1 Perangkat Keras

| No | Perangkat | Spesifikasi | Jumlah |
|----|-----------|------------|--------|
| 1 | **PLC** | Schneider TM221CE24R **atau** Omron CP2E-N60DT | 1 unit |
| 2 | **MiniPC / Laptop** | OS Linux Ubuntu 20.04+ / Windows 10 | 1 unit |
| 3 | **ESP32** | ESP32 Dev Module / DOIT ESP32 DevKit | 1 unit |
| 4 | **Konverter USB-RS485** | CH340/FT232RL + MAX485 | 1 unit |
| 5 | **Modul RS-485** | MAX485 atau SP3485 | 1 unit |
| 6 | **Kabel RS-485** | Twisted pair (A+, B-, GND) | 1 set |
| 7 | **Switch Ethernet** | Unmanaged 4/8 port | 1 unit |
| 8 | **Kabel UTP** | Cat5e RJ45 straight | 2 pcs |
| 9 | **Push Button** | Normaly Open 24V | 2 pcs |
| 10 | **Lampu Indikator** | LED 24V / Pilot Lamp | 2 pcs |
| 11 | **Catu Daya** | 24VDC 2A untuk PLC dan I/O | 1 unit |
| 12 | **Breadboard + Jumper** | Untuk rangkaian ESP32 | 1 set |

### C.2 Perangkat Lunak

| No | Software | Platform | Fungsi | Link |
|----|---------|----------|--------|------|
| 1 | **EcoStruxure Machine Expert – Basic** | Windows | Pemrograman PLC Schneider TM221 | se.com/download |
| 2 | **CX-Programmer** | Windows | Pemrograman PLC Omron CP2E | ia.omron.com |
| 3 | **VS Code + PlatformIO** | Win/Linux/Mac | Pemrograman ESP32 | code.visualstudio.com |
| 4 | **Python 3.9+** | Win/Linux/Mac | Script edge device MiniPC | python.org |
| 5 | **Mosquitto** | Linux/Windows | MQTT Broker | mosquitto.org |
| 6 | **Node-RED** | Linux/Windows | IoT Dashboard | nodered.org |
| 7 | **Modbus Poll** | Windows | Test & debug Modbus | modbustools.com |
| 8 | **MQTT Explorer** | Win/Linux/Mac | Monitor MQTT topics | mqtt-explorer.com |

### C.3 Library Python (requirements.txt)

```
pymodbus>=3.0.0
pyserial>=3.5
paho-mqtt>=1.6.1
requests>=2.28.0
fastapi>=0.95.0
uvicorn>=0.22.0
python-dotenv>=0.19.0
```

Instalasi:
```bash
pip install -r requirements.txt
```

### C.4 Library ESP32 (PlatformIO)

```ini
lib_deps =
    emelianov/modbus-esp8266@^4.1.0
    knolleary/PubSubClient@^2.8
    bblanchon/ArduinoJson@^6.21.3
```

---

## D. DASAR TEORI SINGKAT

### D.1 Protokol Modbus

Modbus adalah protokol komunikasi master-slave yang dikembangkan pada 1979. Terdapat dua varian utama yang digunakan dalam praktikum ini:

- **Modbus RTU:** komunikasi serial via RS-485, frame berisi Slave ID + Function Code + Data + CRC
- **Modbus TCP:** komunikasi via Ethernet/IP, port 502, menggunakan MBAP header

### D.2 Register Map Modbus

| Tipe | Alamat | Akses | Keterangan |
|------|--------|-------|-----------|
| Coil | 0–65535 | R/W | Bit output (Boolean) |
| Discrete Input | 0–65535 | R | Bit input (Boolean) |
| Input Register | 0–65535 | R | Word 16-bit input |
| Holding Register | 0–65535 | R/W | Word 16-bit R/W |

### D.3 Pemetaan Memori TM221

- `%MW0–%MW999` → Holding Register 0–999
- `%Q0.0–%Q0.9` → Coil 2048–2057 (output relay)
- `%I0.0–%I0.13` → Discrete Input 0–13
- `%IW0.0` → Input Register 256 (analog input 0)

### D.4 Pemetaan Memori CP2E

- `DM0000–DM9999` → Holding Register 0–9999
- `CIO 000.00–099.15` → Coil 0–1599

---

## E. LANGKAH KERJA

---

### SESI 1: KONFIGURASI DAN PENGUJIAN PLC

---

#### LANGKAH 1: Persiapan Hardware

**Estimasi waktu: 20 menit**

1. Rangkai catu daya 24VDC untuk PLC
2. Hubungkan push button ke input I0.0 dan I0.1 PLC
3. Hubungkan lampu indikator ke output Q0.0 dan Q0.1 PLC
4. Untuk komunikasi RTU: sambungkan kabel RS-485 (A+, B-, GND) dari port SL1 PLC ke konverter USB-RS485
5. Untuk komunikasi TCP: sambungkan kabel UTP RJ45 dari port Ethernet PLC ke switch
6. Sambungkan MiniPC dan ESP32 ke switch yang sama

**Diagram wiring RS-485:**
```
PLC SL1 (A) ──────────── USB-RS485 (A+)
PLC SL1 (B) ──────────── USB-RS485 (B-)
PLC GND     ──────────── USB-RS485 (GND)
```

**Checkpoint ✅:** Semua koneksi fisik sudah benar, PLC menyala (LED POWER hijau)

---

#### LANGKAH 2: Pemrograman PLC Schneider TM221

**Estimasi waktu: 30 menit**

1. Buka **EcoStruxure Machine Expert – Basic (EMEB)**
2. Buat project baru: **File > New Project** → Nama: `ModbusGateway_[NamaKelompok]`
3. Pilih PLC: **TM221CE24R**

**Konfigurasi Serial Modbus RTU Slave:**
4. Klik **TM221CE24R** di panel kiri → tab **Configuration**
5. Pilih **Serial Line** → **SL1**
6. Atur parameter:
   - Protocol: **Modbus Slave**
   - Slave Address: **1**
   - Baud Rate: **9600**
   - Data Bits: 8, Parity: None, Stop Bits: 1

**Konfigurasi Ethernet Modbus TCP:**
7. **Configuration** → **Ethernet**
8. IP Mode: **Fixed**
9. IP Address: **192.168.1.10**
10. Subnet: **255.255.255.0**

**Program Ladder:**
11. Buat **New Program** → nama: `Main`
12. Buat Rung 1: kontrol lampu Q0.0 dari tombol I0.0 (latch) dan I0.1 (unlatch)
13. Buat Rung 2: salin nilai AI (`%IW0.0`) ke memory word (`%MW0`)
14. Buat Rung 3: salin nilai counter otomatis ke `%MW1` (gunakan `%MW1 = %MW1 + 1`)
15. **Build** (F7) → tidak ada error
16. **Download** ke PLC → **Run**

**Checkpoint ✅:** PLC berjalan (LED RUN hijau), indikator I/O sesuai tombol

---

#### LANGKAH 3: Pemrograman PLC Omron CP2E (Alternatif)

**Estimasi waktu: 30 menit**

1. Buka **CX-Programmer**
2. Buat project baru → pilih CPU: **CP2E-N60DT-D**
3. Klik kanan CPU → **Properties** → **Built-in I/O Settings** → **Serial Port**
4. Atur:
   - Protocol: **Modbus RTU Slave**
   - Node No: **1**
   - Baud Rate: 9600, Data Bits: 8, Parity: None, Stop Bits: 1

**Program:**
5. Rung 1: `LD I:000.00 / AND NOT I:000.01 / OUT Q:100.00`
6. Rung 2: `LD P_On / MOV AI:000 DM:0000` (salin analog ke DM0)
7. Download → PLC Run

**Checkpoint ✅:** PLC CP2E berjalan, dapat dikontrol dari CX-Programmer

---

### SESI 2: KOMUNIKASI MODBUS DENGAN PYTHON (MINIPC)

---

#### LANGKAH 4: Setup Python Environment

**Estimasi waktu: 15 menit**

```bash
# Buat virtual environment
python3 -m venv venv_modbus
source venv_modbus/bin/activate   # Linux
# atau: venv_modbus\Scripts\activate   # Windows

# Install library
pip install pymodbus pyserial paho-mqtt requests fastapi uvicorn

# Verifikasi port USB-RS485 (Linux)
ls /dev/ttyUSB*
# atau Windows: Device Manager → Ports (COMx)
```

**Checkpoint ✅:** Library terinstall, port USB terdeteksi

---

#### LANGKAH 5: Tes Komunikasi Modbus RTU (Python)

**Estimasi waktu: 30 menit**

Buat file `test_modbus_rtu.py`:

```python
from pymodbus.client import ModbusSerialClient
import time

PORT = "/dev/ttyUSB0"  # Sesuaikan dengan sistem Anda

client = ModbusSerialClient(
    port=PORT, baudrate=9600,
    bytesize=8, parity='N', stopbits=1, timeout=2
)

print("Menghubungkan ke PLC...")
if client.connect():
    print("Terhubung!")
    for i in range(5):
        rr = client.read_holding_registers(address=0, count=5, slave=1)
        if not rr.isError():
            print(f"[{i}] MW0={rr.registers[0]}, MW1={rr.registers[1]}, "
                  f"MW2={rr.registers[2]}, MW3={rr.registers[3]}, MW4={rr.registers[4]}")
        else:
            print(f"Error baca register: {rr}")

        di = client.read_coils(address=2048, count=4, slave=1)
        if not di.isError():
            print(f"    Output Q0.0={di.bits[0]}, Q0.1={di.bits[1]}")
        time.sleep(1)

    # Tulis nilai ke MW5
    wr = client.write_register(address=5, value=9999, slave=1)
    print(f"Tulis MW5=9999: {wr}")

    # Aktifkan/matikan Q0.0
    client.write_coil(address=2048, value=True, slave=1)
    print("Q0.0 diaktifkan")
    time.sleep(2)
    client.write_coil(address=2048, value=False, slave=1)
    print("Q0.0 dimatikan")

    client.close()
else:
    print("Gagal terhubung. Cek PORT dan kabel RS-485")
```

Jalankan:
```bash
python test_modbus_rtu.py
```

**Catat hasil pada Tabel Pengamatan F.1**

**Checkpoint ✅:** Data register terbaca, Q0.0 dapat dikontrol dari Python

---

#### LANGKAH 6: Tes Komunikasi Modbus TCP (Python)

**Estimasi waktu: 20 menit**

Buat file `test_modbus_tcp.py`:

```python
from pymodbus.client import ModbusTcpClient
import time

PLC_IP = "192.168.1.10"

client = ModbusTcpClient(host=PLC_IP, port=502, timeout=3)

if client.connect():
    print(f"Terhubung ke PLC via Modbus TCP ({PLC_IP}:502)")
    for i in range(5):
        rr = client.read_holding_registers(address=0, count=5, slave=1)
        if not rr.isError():
            print(f"[{i}] Registers: {rr.registers}")
        time.sleep(1)
    client.close()
else:
    print("Gagal terhubung. Cek IP PLC dan koneksi jaringan")
```

**Catat hasil pada Tabel Pengamatan F.2**

---

### SESI 3: KOMUNIKASI MODBUS DENGAN ESP32 (PLATFORMIO)

---

#### LANGKAH 7: Setup Project PlatformIO

**Estimasi waktu: 15 menit**

1. Buka **VS Code** → klik ikon **PlatformIO**
2. PlatformIO Home → **New Project**
   - Name: `ModbusESP32_[NamaKelompok]`
   - Board: **Espressif ESP32 Dev Module**
   - Framework: **Arduino**
3. Edit `platformio.ini`:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
    emelianov/modbus-esp8266@^4.1.0
    knolleary/PubSubClient@^2.8
    bblanchon/ArduinoJson@^6.21.3
monitor_speed = 115200
upload_speed = 921600
```

**Wiring ESP32-MAX485:**
```
ESP32 GPIO17 (TX2) ──► MAX485 DI
ESP32 GPIO16 (RX2) ◄── MAX485 RO
ESP32 GPIO4        ──► MAX485 DE
ESP32 GPIO4        ──► MAX485 RE
MAX485 A(+)        ──── Bus RS-485 A(+)
MAX485 B(-)        ──── Bus RS-485 B(-)
```

---

#### LANGKAH 8: Program ESP32 Modbus RTU Master

**Estimasi waktu: 30 menit**

Buat file `src/main.cpp`:

```cpp
#include <Arduino.h>
#include <ModbusRTU.h>

#define RXD2    16
#define TXD2    17
#define DE_RE    4
#define SLAVE_ID 1

ModbusRTU mb;
uint16_t regData[10];
bool coilData[8];
bool dataReady = false;

bool cbReadRegs(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        dataReady = true;
        Serial.print("Registers: ");
        for (int i = 0; i < 10; i++) {
            Serial.printf("MW%d=%d ", i, regData[i]);
        }
        Serial.println();
    } else {
        Serial.printf("Modbus Error: 0x%02X\n", event);
    }
    return true;
}

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
    mb.begin(&Serial2, DE_RE);
    mb.master();
    Serial.println("=== ESP32 Modbus RTU Master ===");
    Serial.println("Siap baca PLC...");
}

void loop() {
    if (!mb.slave()) {
        mb.readHreg(SLAVE_ID, 0, regData, 10, cbReadRegs);
    }
    mb.task();
    delay(1000);
}
```

Build dan upload:
```
PlatformIO: Build → Upload → Monitor (115200 baud)
```

**Catat hasil pada Tabel Pengamatan F.3**

**Checkpoint ✅:** Serial monitor menampilkan nilai register PLC secara berkala

---

### SESI 4: PENGIRIMAN DATA KE SERVER

---

#### LANGKAH 9: Setup MQTT Broker (Mosquitto)

**Estimasi waktu: 20 menit**

```bash
# Install Mosquitto (Linux)
sudo apt update && sudo apt install -y mosquitto mosquitto-clients
sudo systemctl start mosquitto && sudo systemctl enable mosquitto

# Verifikasi berjalan
sudo systemctl status mosquitto

# Test di terminal terpisah:
# Terminal 1 (subscriber):
mosquitto_sub -h localhost -t "plc/#" -v

# Terminal 2 (publisher test):
mosquitto_pub -h localhost -t "plc/test" -m '{"test": 123}'
```

**Windows:** Download installer dari mosquitto.org, jalankan sebagai service.

**Checkpoint ✅:** Subscriber menerima pesan dari publisher test

---

#### LANGKAH 10: Gateway Modbus RTU → MQTT (Python)

**Estimasi waktu: 30 menit**

Buat file `gateway_mqtt.py`:

```python
#!/usr/bin/env python3
"""PLC Modbus RTU → MQTT Gateway"""
import time, json, logging
from pymodbus.client import ModbusSerialClient
import paho.mqtt.client as mqtt

PORT = "/dev/ttyUSB0"
SLAVE = 1
MQTT_HOST = "localhost"
MQTT_TOPIC = "plc/data"
INTERVAL = 1.0

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

modbus = ModbusSerialClient(port=PORT, baudrate=9600,
                             bytesize=8, parity='N', stopbits=1, timeout=1)
mq = mqtt.Client("plc_gateway")

def on_connect(c, u, f, rc):
    log.info("MQTT %s" % ("OK" if rc==0 else f"Error {rc}"))

mq.on_connect = on_connect
mq.connect(MQTT_HOST, 1883, 60)
mq.loop_start()
modbus.connect()

log.info("Gateway berjalan... Ctrl+C untuk berhenti")
try:
    while True:
        rr = modbus.read_holding_registers(address=0, count=10, slave=SLAVE)
        rc = modbus.read_coils(address=2048, count=10, slave=SLAVE)
        ri = modbus.read_input_registers(address=256, count=2, slave=SLAVE)

        if not rr.isError():
            payload = {
                "timestamp": time.time(),
                "plc_id": SLAVE,
                "registers": rr.registers,
                "outputs": list(rc.bits[:10]) if not rc.isError() else [],
                "analog": ri.registers if not ri.isError() else []
            }
            mq.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
            log.info(f"Published: regs={rr.registers[:3]}...")
        else:
            log.warning(f"Modbus error: {rr}")

        time.sleep(INTERVAL)
except KeyboardInterrupt:
    log.info("Dihentikan")
finally:
    modbus.close()
    mq.loop_stop()
    mq.disconnect()
```

Jalankan di dua terminal:
```bash
# Terminal 1: subscriber monitor
mosquitto_sub -t "plc/data" -v

# Terminal 2: gateway
python gateway_mqtt.py
```

**Catat hasil pada Tabel Pengamatan F.4**

**Checkpoint ✅:** Data PLC terlihat di subscriber MQTT setiap 1 detik

---

#### LANGKAH 11: Buat REST API Server (Python FastAPI)

**Estimasi waktu: 25 menit**

Buat file `api_server.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3, time, json

app = FastAPI(title="PLC IoT Gateway API v1.0")

def init_db():
    conn = sqlite3.connect("plc_data.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL NOT NULL,
        plc_id INTEGER NOT NULL,
        registers TEXT,
        outputs TEXT,
        analog TEXT
    )''')
    conn.commit(); conn.close()

init_db()

class PLCData(BaseModel):
    plc_id: int
    registers: List[int] = []
    outputs: List[bool] = []
    analog: List[int] = []

@app.post("/api/v1/plc/data")
async def receive_data(data: PLCData):
    conn = sqlite3.connect("plc_data.db")
    conn.execute(
        "INSERT INTO readings (timestamp, plc_id, registers, outputs, analog) VALUES (?,?,?,?,?)",
        (time.time(), data.plc_id, json.dumps(data.registers),
         json.dumps(data.outputs), json.dumps(data.analog))
    )
    conn.commit(); conn.close()
    return {"status": "ok", "plc_id": data.plc_id, "registers": len(data.registers)}

@app.get("/api/v1/plc/{plc_id}/latest")
async def get_latest(plc_id: int):
    conn = sqlite3.connect("plc_data.db")
    row = conn.execute(
        "SELECT timestamp, plc_id, registers, outputs, analog FROM readings "
        "WHERE plc_id=? ORDER BY timestamp DESC LIMIT 1", (plc_id,)
    ).fetchone()
    conn.close()
    if row:
        return {"timestamp": row[0], "plc_id": row[1],
                "registers": json.loads(row[2]), "outputs": json.loads(row[3])}
    return {"error": "Data tidak ditemukan"}

@app.get("/api/v1/plc/{plc_id}/history")
async def get_history(plc_id: int, limit: int = 20):
    conn = sqlite3.connect("plc_data.db")
    rows = conn.execute(
        "SELECT timestamp, registers FROM readings WHERE plc_id=? "
        "ORDER BY timestamp DESC LIMIT ?", (plc_id, limit)
    ).fetchall()
    conn.close()
    return {"plc_id": plc_id, "count": len(rows),
            "data": [{"t": r[0], "r": json.loads(r[1])} for r in rows]}
```

Jalankan:
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
# Buka: http://localhost:8000/docs (Swagger UI)
```

**Catat hasil pada Tabel Pengamatan F.5**

**Checkpoint ✅:** API berjalan, Swagger UI dapat diakses, POST dan GET berhasil

---

#### LANGKAH 12: Gateway Modbus → REST API (Python)

**Estimasi waktu: 15 menit**

Buat file `gateway_rest.py`:

```python
import time, json, logging, requests
from pymodbus.client import ModbusSerialClient

PORT = "/dev/ttyUSB0"
SLAVE = 1
API_URL = "http://localhost:8000/api/v1/plc/data"

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = ModbusSerialClient(port=PORT, baudrate=9600,
                             bytesize=8, parity='N', stopbits=1, timeout=1)
client.connect()

while True:
    rr = client.read_holding_registers(address=0, count=10, slave=SLAVE)
    rc = client.read_coils(address=2048, count=10, slave=SLAVE)

    if not rr.isError():
        payload = {
            "plc_id": SLAVE,
            "registers": rr.registers,
            "outputs": [bool(b) for b in rc.bits[:10]] if not rc.isError() else []
        }
        try:
            resp = requests.post(API_URL, json=payload, timeout=5)
            log.info(f"REST: {resp.status_code} - {resp.json()}")
        except requests.exceptions.ConnectionError:
            log.warning("API server tidak dapat dijangkau, data tidak terkirim")

    time.sleep(2)
```

**Catat hasil pada Tabel Pengamatan F.5**

---

#### LANGKAH 13: Dashboard Node-RED

**Estimasi waktu: 30 menit**

1. Install dan jalankan Node-RED:
```bash
node-red
# Buka: http://localhost:1880
```

2. Install dashboard nodes: **Menu** (☰) → **Manage Palette** → Install: `node-red-dashboard`

3. Buat flow MQTT → Dashboard:
   - Drag **MQTT in** node → Server: localhost, Topic: `plc/data`
   - Drag **JSON** node (parse payload)
   - Drag **Function** node:
     ```javascript
     // Ekstrak nilai dari payload
     var data = msg.payload;
     msg.payload = data.registers[0];  // Tampilkan MW0
     return msg;
     ```
   - Drag **Gauge** node → Label: "MW0", Range: 0–4095
   - Drag **Chart** node → Label: "Tren MW0", Duration: 60 detik

4. Klik **Deploy** → buka `http://localhost:1880/ui`

**Screenshot dashboard dan lampirkan**

**Checkpoint ✅:** Dashboard menampilkan nilai MW0 secara real-time

---

## F. TABEL PENGAMATAN DAN DATA

### F.1 Hasil Komunikasi Modbus RTU (Python – MiniPC)

| No | Iterasi | MW0 | MW1 | MW2 | MW3 | MW4 | Q0.0 | Q0.1 | Keterangan |
|----|---------|-----|-----|-----|-----|-----|------|------|-----------|
| 1 | 1 | | | | | | | | |
| 2 | 2 | | | | | | | | |
| 3 | 3 | | | | | | | | |
| 4 | 4 | | | | | | | | |
| 5 | 5 | | | | | | | | |

**Latency rata-rata:** ________ ms  
**Error count:** ________

---

### F.2 Hasil Komunikasi Modbus TCP (Python – MiniPC)

| No | Iterasi | Registers [0–4] | Waktu Respons (ms) | Status |
|----|---------|----------------|-------------------|--------|
| 1 | 1 | | | |
| 2 | 2 | | | |
| 3 | 3 | | | |
| 4 | 4 | | | |
| 5 | 5 | | | |

**Perbandingan RTU vs TCP:** ______________________

---

### F.3 Hasil Komunikasi Modbus (ESP32 – PlatformIO)

| No | Iterasi | Register [0–9] | Error? | Keterangan |
|----|---------|---------------|--------|-----------|
| 1 | 1 | | | |
| 2 | 2 | | | |
| 3 | 3 | | | |
| 4 | 4 | | | |
| 5 | 5 | | | |

---

### F.4 Hasil Pengiriman Data ke MQTT

| No | Timestamp | Topic | Payload (singkat) | QoS | Diterima? |
|----|-----------|-------|------------------|-----|-----------|
| 1 | | plc/data | | 1 | |
| 2 | | plc/data | | 1 | |
| 3 | | plc/data | | 1 | |

**MQTT Broker:** ________________  
**Rata-rata interval pengiriman:** ________ detik

---

### F.5 Hasil Pengiriman ke REST API

| No | Method | Endpoint | Payload | Status Code | Response |
|----|--------|----------|---------|------------|---------|
| 1 | POST | /api/v1/plc/data | {plc_id:1,...} | | |
| 2 | GET | /api/v1/plc/1/latest | – | | |
| 3 | GET | /api/v1/plc/1/history | – | | |

---

### F.6 Konfigurasi yang Digunakan

| Parameter | Nilai |
|-----------|-------|
| PLC yang digunakan | Schneider TM221 / Omron CP2E |
| Slave ID PLC | |
| Baud Rate (RTU) | |
| IP PLC (TCP) | |
| Port USB-RS485 (MiniPC) | |
| IP MiniPC | |
| IP ESP32 | |
| IP MQTT Broker | |
| MQTT Topic | |
| REST API Port | |

---

## G. PERTANYAAN ANALISIS

1. **Jelaskan** perbedaan antara Modbus RTU dan Modbus TCP dari sisi physical layer, kecepatan, jarak, dan jumlah perangkat yang didukung. Kapan sebaiknya menggunakan masing-masing?

   **Jawaban:**
   _______________________________________________

2. **Bandingkan** waktu respons Modbus RTU vs Modbus TCP yang Anda ukur pada praktikum ini. Faktor apa yang menyebabkan perbedaan tersebut?

   **Jawaban:**
   _______________________________________________

3. **Jelaskan** alasan menggunakan resistor terminasi 120Ω pada kedua ujung bus RS-485. Apa yang akan terjadi jika resistor terminasi tidak dipasang?

   **Jawaban:**
   _______________________________________________

4. **Bandingkan** pengiriman data menggunakan MQTT vs REST API. Protokol mana yang lebih cocok untuk sistem monitoring real-time? Berikan alasannya secara teknis.

   **Jawaban:**
   _______________________________________________

5. **Analisa** potensi masalah keamanan pada sistem yang Anda bangun di praktikum ini. Sebutkan minimal 3 celah keamanan dan cara mengatasinya.

   **Jawaban:**
   _______________________________________________

6. **Rancanglah** arsitektur sistem IoT untuk pabrik dengan 10 PLC berbeda merek (5 Schneider dan 5 Omron), dengan 1 server pusat. Protokol apa yang dipilih dan mengapa?

   **Jawaban:**
   _______________________________________________

---

## H. KESIMPULAN

Tuliskan kesimpulan praktikum dalam 5–6 poin:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
4. _______________________________________________
5. _______________________________________________
6. _______________________________________________

---

## I. LAMPIRAN (Screenshot Wajib)

- [ ] Screenshot EMEB/CX-Programmer: konfigurasi Modbus Slave dan program Ladder
- [ ] Screenshot terminal Python: output pembacaan Modbus RTU berhasil
- [ ] Screenshot terminal Python: output pembacaan Modbus TCP berhasil
- [ ] Screenshot Serial Monitor PlatformIO: ESP32 membaca register PLC
- [ ] Screenshot Mosquitto: subscriber menerima data dari gateway
- [ ] Screenshot MQTT Explorer: data di topic `plc/data`
- [ ] Screenshot Swagger UI FastAPI: endpoint POST dan GET
- [ ] Screenshot terminal: HTTP POST berhasil (status 200)
- [ ] Screenshot Node-RED: flow MQTT → Dashboard
- [ ] Screenshot Node-RED UI Dashboard: gauge/chart menampilkan data PLC real-time
- [ ] Screenshot PLC panel: indikator I/O saat dikendalikan dari Python/ESP32

---

## J. REFERENSI

1. Modbus Organization. *Modbus Application Protocol Specification V1.1b3*. https://modbus.org
2. Schneider Electric. *EcoStruxure Machine Expert – Basic User Guide*. https://www.se.com
3. Omron. *CP2E Series CPU Unit Operation Manual*. https://www.ia.omron.com
4. pymodbus Documentation. https://pymodbus.readthedocs.io/en/latest/
5. emelianov. *modbus-esp8266 Library for Arduino*. https://github.com/emelianov/modbus-esp8266
6. Eclipse Mosquitto. *An Open Source MQTT Broker*. https://mosquitto.org
7. FastAPI. *Modern, fast web framework for building APIs with Python 3.9+*. https://fastapi.tiangolo.com
8. Node-RED. *Low-code programming for event-driven applications*. https://nodered.org
9. PlatformIO. *Professional collaborative platform for embedded development*. https://platformio.org
10. Texas Instruments. *RS-485 Application Note SLLA272C*. https://www.ti.com

---

*Jobsheet ini merupakan dokumen resmi praktikum. Isi dengan lengkap dan jujur.*  
*Nilai ditentukan berdasarkan kelengkapan jobsheet, keberhasilan percobaan, kualitas analisis, dan pemahaman teknis.*

**Tanda Tangan Dosen/Asisten:** ___________________  
**Tanggal:** ___________________
