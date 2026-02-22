# MATERI MODUL 05: KOMUNIKASI MODBUS PLC DENGAN EDGE DEVICE DAN SERVER IoT

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 05 – IoT PLC AI Modbus  
**Platform:** Schneider TM221 / Omron CP2E, ESP32 (PlatformIO), MiniPC (Python)  
**Estimasi Waktu Belajar:** 8–10 Jam

---

## DAFTAR ISI

1. [Pendahuluan – Otomasi Industri dan IoT](#1-pendahuluan)
2. [Protokol Modbus – Konsep dan Standar](#2-protokol-modbus)
3. [Modbus RTU – Komunikasi Serial RS-485](#3-modbus-rtu)
4. [Modbus TCP – Komunikasi Ethernet/IP](#4-modbus-tcp)
5. [PLC Schneider TM221 – Arsitektur dan Konfigurasi](#5-plc-schneider-tm221)
6. [PLC Omron CP2E – Arsitektur dan Konfigurasi](#6-plc-omron-cp2e)
7. [Edge Device: MiniPC dengan Python (pymodbus)](#7-edge-device-minipc-python)
8. [Edge Device: ESP32 dengan PlatformIO (ModbusMaster)](#8-edge-device-esp32)
9. [Arsitektur Pengiriman Data ke Server](#9-arsitektur-server)
10. [MQTT Broker – Protokol Pub/Sub untuk IoT](#10-mqtt)
11. [REST API – HTTP untuk IoT](#11-rest-api)
12. [Dashboard dan Visualisasi Data](#12-dashboard)
13. [Keamanan Sistem IoT Industri](#13-keamanan)
14. [Integrasi AI pada Sistem IoT PLC](#14-ai-integrasi)
15. [Referensi](#15-referensi)

---

## 1. PENDAHULUAN – OTOMASI INDUSTRI DAN IoT

### 1.1 Latar Belakang

Industri manufaktur modern saat ini bertransformasi menuju konsep **Industri 4.0**, di mana perangkat fisik (mesin, PLC, sensor) terhubung ke jaringan digital dan mampu bertukar informasi secara real-time. Dalam konteks ini, **Programmable Logic Controller (PLC)** yang selama ini menjadi tulang punggung otomasi pabrik perlu diintegrasikan ke dalam ekosistem **Industrial IoT (IIoT)**.

Tantangan utama integrasi ini adalah:
- PLC menggunakan protokol industri proprietary atau standar lama (Modbus, Profibus, dll.)
- Server cloud dan aplikasi modern menggunakan protokol internet (MQTT, HTTP/REST, WebSocket)
- Diperlukan **edge device** sebagai jembatan penerjemah protokol

### 1.2 Peran Edge Device

**Edge Device** adalah perangkat komputasi yang ditempatkan di lapangan (dekat PLC) untuk:

| Fungsi | Keterangan |
|--------|-----------|
| **Protocol Bridge** | Menerjemahkan Modbus ke MQTT/REST/OPC-UA |
| **Data Preprocessing** | Filter, agregasi, kalkulasi data lokal |
| **Local Control** | Logika kontrol cadangan saat koneksi server putus |
| **Edge AI** | Inferensi model AI langsung di lapangan |
| **Data Buffering** | Menyimpan data sementara saat internet putus |

Dalam praktikum ini, edge device yang digunakan:
- **MiniPC (Raspberry Pi / PC x86)** dengan Python
- **ESP32** dengan PlatformIO

### 1.3 Arsitektur Sistem Keseluruhan

```
┌─────────────────────────────────────────────────────┐
│                  LAPANGAN (Field)                    │
│                                                     │
│  ┌──────────┐  RS-485/    ┌──────────┐             │
│  │ PLC      │◄──Ethernet──►│ Edge     │             │
│  │ TM221 /  │  (Modbus   │ Device   │             │
│  │ CP2E     │  RTU/TCP)  │ MiniPC/  │             │
│  └──────────┘             │ ESP32    │             │
│       │                   └────┬─────┘             │
│  ┌────▼─────┐                  │ WiFi/LAN/4G       │
│  │ Sensor/  │                  │                   │
│  │ Actuator │                  │                   │
│  └──────────┘                  │                   │
└───────────────────────────────┼─────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │      CLOUD / SERVER   │
                    │                       │
                    │  ┌─────────────────┐  │
                    │  │  MQTT Broker    │  │
                    │  │  (Mosquitto/    │  │
                    │  │   HiveMQ)       │  │
                    │  └─────────────────┘  │
                    │  ┌─────────────────┐  │
                    │  │  REST API       │  │
                    │  │  (Flask/FastAPI)│  │
                    │  └─────────────────┘  │
                    │  ┌─────────────────┐  │
                    │  │  Database       │  │
                    │  │  (InfluxDB/     │  │
                    │  │   PostgreSQL)   │  │
                    │  └─────────────────┘  │
                    │  ┌─────────────────┐  │
                    │  │  Dashboard      │  │
                    │  │  (Grafana/      │  │
                    │  │   Node-RED)     │  │
                    │  └─────────────────┘  │
                    └───────────────────────┘
```

---

## 2. PROTOKOL MODBUS – KONSEP DAN STANDAR

### 2.1 Sejarah dan Standar

**Modbus** adalah protokol komunikasi serial yang dikembangkan oleh **Modicon** (sekarang bagian dari Schneider Electric) pada tahun **1979**. Meskipun usianya lebih dari 40 tahun, Modbus tetap menjadi salah satu protokol otomasi industri yang paling banyak digunakan karena:
- **Sederhana** dan mudah diimplementasikan
- **Open standard** – tidak ada biaya lisensi
- **Kompatibel luas** – hampir semua PLC, inverter, sensor mendukungnya
- **Robust** – stabil di lingkungan industri berinterferensi tinggi

Standar resmi: **MODBUS Application Protocol Specification V1.1b3** (modbus.org)

### 2.2 Model Data Modbus

Modbus mendefinisikan 4 jenis tabel data pada slave device:

| Tabel | Jenis Data | Akses | Alamat Register | Kode Fungsi |
|-------|-----------|-------|----------------|-------------|
| **Coil** | Boolean (1-bit) | Read/Write | 00001–09999 | FC01, FC05, FC15 |
| **Discrete Input** | Boolean (1-bit) | Read Only | 10001–19999 | FC02 |
| **Input Register** | 16-bit word | Read Only | 30001–39999 | FC04 |
| **Holding Register** | 16-bit word | Read/Write | 40001–49999 | FC03, FC06, FC16 |

> **Catatan:** Dalam PLC modern, alamat register Modbus dikonfigurasi lewat software pemrograman PLC (SoMachine/EcoStruxure untuk Schneider, CX-Programmer untuk Omron).

### 2.3 Function Codes yang Paling Sering Digunakan

| FC | Nama | Keterangan |
|----|------|-----------|
| **01** | Read Coils | Membaca status output digital (bit) |
| **02** | Read Discrete Inputs | Membaca status input digital (bit) |
| **03** | Read Holding Registers | Membaca nilai register (word 16-bit) |
| **04** | Read Input Registers | Membaca nilai register input (word 16-bit) |
| **05** | Write Single Coil | Menulis satu bit output |
| **06** | Write Single Register | Menulis satu register |
| **15** | Write Multiple Coils | Menulis beberapa bit output |
| **16** | Write Multiple Registers | Menulis beberapa register |

### 2.4 Format Frame Modbus

**Modbus RTU Frame:**
```
┌──────────┬──────────┬──────────┬──────────────────┬──────────┐
│ Slave ID │ Function │  Data    │   Data Bytes     │  CRC     │
│ (1 byte) │  Code    │ Address  │  (variabel)      │ (2 byte) │
│          │ (1 byte) │ (2 byte) │                  │          │
└──────────┴──────────┴──────────┴──────────────────┴──────────┘
```

**Modbus TCP Frame:**
```
┌──────────────────┬──────────┬──────────┬──────────────────────┐
│  MBAP Header     │ Protocol │  Length  │   PDU (FC + Data)    │
│  Transaction ID  │ ID (0x00)│ (2 byte) │                      │
│  (2 byte)        │ (2 byte) │          │                      │
└──────────────────┴──────────┴──────────┴──────────────────────┘
```

### 2.5 Master-Slave Architecture

Modbus menggunakan arsitektur **Master-Slave (Request-Response)**:
- **Master** (Edge Device: MiniPC/ESP32) memulai komunikasi dengan mengirim permintaan
- **Slave** (PLC) menunggu dan merespons permintaan
- Dalam satu jaringan RTU: **1 master, maksimal 247 slave** (alamat 1–247)
- Dalam Modbus TCP: dapat ada beberapa master secara paralel

---

## 3. MODBUS RTU – KOMUNIKASI SERIAL RS-485

### 3.1 Physical Layer RS-485

**RS-485** (juga dikenal sebagai EIA-485) adalah standar komunikasi serial diferensial yang digunakan sebagai physical layer Modbus RTU.

**Karakteristik RS-485:**

| Parameter | Nilai |
|-----------|-------|
| Tipe sinyal | Differential (A+, B-) |
| Tegangan sinyal | ±200 mV (minimum) hingga ±6V |
| Jarak transmisi maksimal | 1200 meter (pada 100 kbps) |
| Kecepatan data | 300 bps – 10 Mbps |
| Jumlah perangkat | Maksimal 32 unit (standar), hingga 256 dengan repeater |
| Topologi | Bus/multi-drop |
| Terminasi | 120 Ω di kedua ujung bus |

**Wiring RS-485:**
```
Master        Slave 1       Slave 2       Slave N
(MiniPC/ESP32) (PLC TM221) (PLC CP2E)
    │               │             │             │
    ├── A(+) ───────┼─────────────┼─────────────┤
    ├── B(-) ───────┼─────────────┼─────────────┤
    └── GND ────────┴─────────────┴─────────────┘
[120Ω]                                      [120Ω]
```

### 3.2 Parameter Komunikasi Serial

Parameter yang harus **identik** antara master dan semua slave:

| Parameter | Nilai Umum |
|-----------|-----------|
| Baud Rate | 9600, 19200, 38400, 115200 |
| Data Bits | 8 (standar Modbus RTU) |
| Stop Bits | 1 atau 2 |
| Parity | None, Even, atau Odd |

> **Contoh:** 9600-8-N-1 = 9600 bps, 8 data bits, No parity, 1 stop bit

### 3.3 Konverter RS-485 untuk Edge Device

**Untuk MiniPC (USB ke RS-485):**
- Chip: CH340G, CP2102, FT232RL + MAX485
- Driver: otomatis di Linux (`/dev/ttyUSB0`), Windows (`COMx`)
- Contoh modul: USB-RS485-WE-1800-BT (FTDI)

**Untuk ESP32 (GPIO ke RS-485):**
- IC: MAX485, SP3485, SN75176
- Koneksi: TX ke DI, RX ke RO, GPIO ke DE+RE (direction control)
- UART ESP32 yang digunakan: UART2 (GPIO16-RX, GPIO17-TX)

```
ESP32             MAX485
GPIO17 (TX) ─────► DI
GPIO16 (RX) ◄───── RO
GPIO4 (DE/RE) ───► DE
                └──► RE (DE dan RE dihubungkan ke GPIO yang sama)
                    A(+) ─────► ke Bus RS-485
                    B(-) ─────► ke Bus RS-485
```

---

## 4. MODBUS TCP – KOMUNIKASI ETHERNET/IP

### 4.1 Konsep Modbus TCP

**Modbus TCP** mengenkapsulasi PDU Modbus standar dalam paket TCP/IP. Karakteristiknya:
- Port default: **502**
- Tidak ada CRC (digantikan oleh error detection TCP)
- Mendukung **multiple connections** secara simultan
- Jarak tidak terbatas (tergantung infrastruktur jaringan)
- Latensi lebih tinggi dibanding RTU (karena overhead TCP)

### 4.2 MBAP Header

```
┌────────────────┬──────────────┬──────────┬────────────┐
│ Transaction ID │ Protocol ID  │  Length  │  Unit ID   │
│   (2 byte)     │  (2 byte)    │ (2 byte) │  (1 byte)  │
│  auto-increment│  selalu 0x00 │  jumlah  │  Slave ID  │
└────────────────┴──────────────┴──────────┴────────────┘
```

### 4.3 Konfigurasi Jaringan

**Topologi standar:**
```
Router/Switch
    │
    ├── PLC TM221 (IP: 192.168.1.10)
    ├── PLC CP2E  (IP: 192.168.1.11)
    └── MiniPC/ESP32 (IP: 192.168.1.20)
```

---

## 5. PLC SCHNEIDER TM221 – ARSITEKTUR DAN KONFIGURASI

### 5.1 Gambaran Umum TM221

**Schneider Electric Modicon M221** (TM221) adalah PLC compact yang banyak digunakan di industri kecil–menengah.

**Spesifikasi Utama TM221CE24R:**

| Spesifikasi | Nilai |
|-------------|-------|
| CPU | 32-bit |
| Program Memory | 256 KB |
| Data Memory | 64 KB |
| Digital Input | 14 × 24VDC |
| Digital Output | 10 × Relay (2A) |
| Analog Input | 2 × 0–10V (built-in) |
| Ethernet | 1 × RJ45 (10/100 Mbps) |
| Serial | 1 × RS-485 (SL1) |
| Modbus RTU | Slave dan Master |
| Modbus TCP | Slave |
| Software | EcoStruxure Machine Expert – Basic (EMEB) |

### 5.2 Port Serial RS-485 pada TM221

TM221 memiliki port serial **SL1** (Serial Line 1) yang mendukung Modbus RTU Slave/Master.

**Konfigurasi SL1 di EcoStruxure Machine Expert – Basic:**
1. Buka EMEB → Panel kiri klik **TM221CE24R** → tab **Configuration**
2. Pilih **Serial Line** → **SL1**
3. Protocol = **Modbus Slave**
4. Baud Rate: 9600
5. Parity: None, Stop Bits: 1
6. Slave Address: 1

### 5.3 Konfigurasi Modbus TCP pada TM221

TM221 mendukung Modbus TCP sebagai **slave** via port Ethernet:
1. EMEB → **Configuration** → **Ethernet**
2. IP Address: 192.168.1.10 (static)
3. Subnet Mask: 255.255.255.0
4. Modbus TCP aktif otomatis pada port 502

### 5.4 Pemetaan Memori Modbus TM221

| Objek PLC | Modbus Address | Keterangan |
|-----------|---------------|-----------|
| `%M0–%M999` | Coil 0–999 | Memory bits |
| `%Q0.0–%Q0.9` | Coil 2048–2057 | Output relay 0–9 |
| `%I0.0–%I0.13` | Discrete Input 0–13 | Input digital 0–13 |
| `%MW0–%MW999` | Holding Register 0–999 | Memory words |
| `%IW0.0` | Input Register 256 | Analog input 0 (0–4095) |
| `%IW0.1` | Input Register 257 | Analog input 1 (0–4095) |

### 5.5 Contoh Program PLC TM221 – Ladder Diagram

```
Rung 1: Start/Stop Motor
|  %I0.0  |   %I0.1  |              |  %Q0.0  |
+--[ ]----+--[/]-----+----( )------+
  START_BTN  STOP_BTN                MOTOR_OUT

Rung 2: Salin nilai AI ke MW
|  P_On  |                     |  %MW0   |
+--[ ]---+---[MOV %IW0.0]------+
                                 Nilai Analog AI0

Rung 3: Timer otomatis
|  %Q0.0  |   TON T0   |             |  %Q0.1  |
+--[ ]----+---PT:5000ms+----( )------+
  MOTOR_ON  ELAPSED_T              LAMP_IND
```

---

## 6. PLC OMRON CP2E – ARSITEKTUR DAN KONFIGURASI

### 6.1 Gambaran Umum CP2E

**Omron CP2E** adalah PLC compact generasi terbaru dari Omron yang mendukung komunikasi industri modern.

**Spesifikasi Utama CP2E-N60DT-D:**

| Spesifikasi | Nilai |
|-------------|-------|
| CPU | 32-bit |
| Program Capacity | 10 K steps |
| Data Memory | 32 K words |
| Digital Input | 36 × 24VDC |
| Digital Output | 24 × Transistor NPN/PNP |
| Built-in RS-232C | 1 port |
| Ethernet (suffix E) | 1 × RJ45 |
| Modbus RTU | Slave dan Master (via FB) |
| Modbus TCP | Slave dan Master |
| Software | CX-Programmer (v9.x) |

### 6.2 Konfigurasi Modbus RTU pada CP2E

1. Buka **CX-Programmer** → klik kanan CPU → **Properties**
2. Tab **Built-in I/O Settings** → **Serial Port**
3. Protocol: **Modbus RTU Slave**
4. Baud Rate: 9600, Data Bits: 8, Parity: None, Stop Bits: 1
5. Slave Node No: 1

### 6.3 Pemetaan Memori Modbus CP2E

| Area Omron | Modbus Address | Keterangan |
|-----------|---------------|-----------|
| DM0000–DM9999 | Holding Register 0–9999 | Data Memory words |
| CIO 000.00–099.15 | Coil 0–1599 | Output/Input bits |
| W000.00–W511.15 | Coil 4096–12287 | Work bits |
| TIM/CNT | Holding Register 10000+ | Timer/Counter |

### 6.4 Program Ladder CP2E – Contoh Baca Analog

```
Rung 1: Baca AI0 → DM100
  LD   P_On
  MOVD AIW000, DM100     ; Salin AI0 ke DM100

Rung 2: Konversi skala 0-4095 → 0-100%
  LD   P_On
  DIVL DM100, #4095, DM102   ; DM102 = DM100/4095
  MULR DM102, #100, DM104    ; DM104 = persentase

Rung 3: Output berdasarkan threshold
  LD   DM104
  GT   #80              ; Jika > 80%
  OUT  100.00            ; Aktifkan output Q100.00
```

---

## 7. EDGE DEVICE: MINIPC DENGAN PYTHON (pymodbus)

### 7.1 Library pymodbus

**pymodbus** adalah library Python yang mengimplementasikan protokol Modbus lengkap.

**Instalasi:**
```bash
pip install pymodbus pyserial paho-mqtt requests
```

### 7.2 Membaca Data via Modbus RTU (Python)

```python
from pymodbus.client import ModbusSerialClient
import time

client = ModbusSerialClient(
    port='/dev/ttyUSB0',   # Linux; Windows: 'COM3'
    baudrate=9600,
    bytesize=8,
    parity='N',
    stopbits=1,
    timeout=1
)

def baca_plc():
    if client.connect():
        # Baca 10 Holding Register mulai dari alamat 0
        result = client.read_holding_registers(address=0, count=10, slave=1)
        if not result.isError():
            print(f"Registers: {result.registers}")

        # Baca Coil output digital
        coils = client.read_coils(address=2048, count=10, slave=1)
        if not coils.isError():
            print(f"Outputs: {coils.bits[:10]}")

        client.close()

while True:
    baca_plc()
    time.sleep(1)
```

### 7.3 Menulis Data ke PLC via Modbus RTU (Python)

```python
from pymodbus.client import ModbusSerialClient

client = ModbusSerialClient(port='/dev/ttyUSB0', baudrate=9600,
                             bytesize=8, parity='N', stopbits=1, timeout=1)

if client.connect():
    # Tulis nilai ke Holding Register 0 (MW0 = 1500)
    client.write_register(address=0, value=1500, slave=1)

    # Aktifkan output Q0.0 (Coil 2048)
    client.write_coil(address=2048, value=True, slave=1)

    client.close()
```

### 7.4 Membaca Data via Modbus TCP (Python)

```python
from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient(host='192.168.1.10', port=502, timeout=3)

while True:
    if client.connect():
        result = client.read_holding_registers(address=0, count=5, slave=1)
        if not result.isError():
            regs = result.registers
            print(f"MW0={regs[0]}, MW1={regs[1]}, MW2={regs[2]}")
    time.sleep(2)
```

### 7.5 Gateway Lengkap: PLC → MQTT (Python)

```python
#!/usr/bin/env python3
"""
Edge Device Gateway: Modbus PLC → MQTT Broker
"""
import time
import json
import logging
from pymodbus.client import ModbusSerialClient
import paho.mqtt.client as mqtt

PLC_PORT = "/dev/ttyUSB0"
PLC_SLAVE = 1
MQTT_BROKER = "192.168.1.100"
MQTT_TOPIC = "plc/data"
POLL_INTERVAL = 1.0

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

modbus = ModbusSerialClient(port=PLC_PORT, baudrate=9600,
                             bytesize=8, parity='N', stopbits=1, timeout=1)

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, 1883, 60)
mqtt_client.loop_start()
modbus.connect()

while True:
    rr = modbus.read_holding_registers(address=0, count=10, slave=PLC_SLAVE)
    rc = modbus.read_coils(address=2048, count=10, slave=PLC_SLAVE)

    if not rr.isError():
        payload = {
            "timestamp": time.time(),
            "plc_id": PLC_SLAVE,
            "registers": rr.registers,
            "outputs": list(rc.bits[:10]) if not rc.isError() else []
        }
        mqtt_client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
        logger.info(f"Published: {payload}")

    time.sleep(POLL_INTERVAL)
```

---

## 8. EDGE DEVICE: ESP32 DENGAN PLATFORMIO

### 8.1 Pengenalan PlatformIO

**PlatformIO** adalah ekosistem pengembangan embedded berbasis VS Code.

**Instalasi:**
1. Install VS Code
2. Install ekstensi **PlatformIO IDE**
3. Buat project baru: PlatformIO Home → New Project → Board: ESP32 Dev Module

**`platformio.ini`:**
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
```

### 8.2 ESP32 – Modbus RTU Master (PlatformIO)

```cpp
#include <Arduino.h>
#include <ModbusRTU.h>

#define RXD2    16
#define TXD2    17
#define DE_RE    4

ModbusRTU mb;
uint16_t regData[10];

bool cbRead(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        Serial.print("Registers: ");
        for (int i = 0; i < 10; i++) Serial.printf("MW%d=%d ", i, regData[i]);
        Serial.println();
    } else {
        Serial.printf("Error: 0x%02X\n", event);
    }
    return true;
}

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
    mb.begin(&Serial2, DE_RE);
    mb.master();
    Serial.println("ESP32 Modbus RTU Master ready");
}

void loop() {
    if (!mb.slave()) {
        mb.readHreg(1, 0, regData, 10, cbRead);
    }
    mb.task();
    delay(1000);
}
```

### 8.3 ESP32 – Modbus TCP Client (PlatformIO)

```cpp
#include <Arduino.h>
#include <WiFi.h>
#include <ModbusTCP.h>

const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASS";
IPAddress plcIP(192, 168, 1, 10);

ModbusTCP mb;
uint16_t regData[10];

bool cbRead(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        for (int i = 0; i < 10; i++) Serial.printf("MW%d=%d ", i, regData[i]);
        Serial.println();
    }
    return true;
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    Serial.println("\nWiFi OK: " + WiFi.localIP().toString());
    mb.client();
}

void loop() {
    if (!mb.isConnected(plcIP)) mb.connect(plcIP);
    mb.readHreg(plcIP, 0, regData, 10, cbRead, 1);
    mb.task();
    delay(1000);
}
```

### 8.4 ESP32 – Modbus RTU + MQTT Publisher

```cpp
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <ModbusRTU.h>

const char* WIFI_SSID     = "WIFI_SSID";
const char* WIFI_PASS     = "WIFI_PASS";
const char* MQTT_SERVER   = "192.168.1.100";
const int   MQTT_PORT     = 1883;
const char* MQTT_TOPIC    = "plc/data";

#define RXD2 16
#define TXD2 17
#define DE_RE 4

ModbusRTU mb;
WiFiClient espClient;
PubSubClient mqttClient(espClient);
uint16_t regData[10];
bool dataReady = false;

bool cbRead(Modbus::ResultCode event, uint16_t t, void* d) {
    if (event == Modbus::EX_SUCCESS) dataReady = true;
    return true;
}

void reconnectMQTT() {
    while (!mqttClient.connected()) {
        if (mqttClient.connect("ESP32_Gateway")) Serial.println("MQTT OK");
        else delay(2000);
    }
}

void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
    mb.begin(&Serial2, DE_RE);
    mb.master();
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
    if (!mqttClient.connected()) reconnectMQTT();
    mqttClient.loop();

    if (!mb.slave()) mb.readHreg(1, 0, regData, 10, cbRead);
    mb.task();

    if (dataReady) {
        StaticJsonDocument<256> doc;
        doc["device"] = "ESP32";
        JsonArray regs = doc.createNestedArray("registers");
        for (int i = 0; i < 10; i++) regs.add(regData[i]);
        char payload[256];
        serializeJson(doc, payload);
        mqttClient.publish(MQTT_TOPIC, payload);
        Serial.println("Published: " + String(payload));
        dataReady = false;
    }
    delay(1000);
}
```

---

## 9. ARSITEKTUR PENGIRIMAN DATA KE SERVER

### 9.1 Opsi Arsitektur

| Opsi | Alur | Cocok Untuk |
|------|------|------------|
| **MQTT** | Edge → Broker → Subscriber | Real-time, bandwidth kecil |
| **REST API** | Edge → HTTP POST → Server | Data historis, integrasi web |
| **Hybrid** | Edge → MQTT + REST | Produksi industri |

### 9.2 Stack Teknologi Rekomendasi

| Komponen | Open Source | Cloud |
|---------|------------|-------|
| MQTT Broker | Mosquitto, EMQX | HiveMQ Cloud |
| REST API | FastAPI, Flask | AWS Lambda |
| Database TS | InfluxDB | InfluxDB Cloud |
| Dashboard | Grafana, Node-RED | Grafana Cloud |

---

## 10. MQTT BROKER

### 10.1 Konsep MQTT

**MQTT** adalah protokol messaging pub/sub ringan untuk IoT:
- **Broker:** server pusat (Mosquitto)
- **Publisher:** edge device (kirim data)
- **Subscriber:** aplikasi (terima data)

**Quality of Service:**
| QoS | Keterangan |
|-----|-----------|
| 0 | At most once (tidak ada jaminan) |
| 1 | At least once (bisa duplikat) |
| 2 | Exactly once (paling aman) |

### 10.2 Instalasi Mosquitto

```bash
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto && sudo systemctl start mosquitto
# Test:
mosquitto_sub -t "plc/#" -v &
mosquitto_pub -t "plc/data" -m '{"test":123}'
```

### 10.3 Subscriber MQTT → Simpan Database (Python)

```python
import json, sqlite3, time
import paho.mqtt.client as mqtt

def init_db():
    conn = sqlite3.connect("plc_data.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL, plc_id INTEGER,
        register_index INTEGER, value INTEGER)''')
    conn.commit(); conn.close()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    conn = sqlite3.connect("plc_data.db")
    for i, v in enumerate(data.get('registers', [])):
        conn.execute("INSERT INTO readings VALUES (NULL,?,?,?,?)",
                     (data.get('timestamp', time.time()), data.get('plc_id',0), i, v))
    conn.commit(); conn.close()

init_db()
c = mqtt.Client()
c.on_message = on_message
c.connect("localhost", 1883, 60)
c.subscribe("plc/data", qos=1)
c.loop_forever()
```

---

## 11. REST API – HTTP UNTUK IoT

### 11.1 FastAPI Server

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3, time

app = FastAPI(title="PLC IoT Gateway API")

class PLCData(BaseModel):
    plc_id: int
    registers: List[int]
    outputs: List[bool] = []

@app.post("/api/v1/plc/data")
async def receive_data(data: PLCData):
    conn = sqlite3.connect("plc_data.db")
    conn.execute("INSERT INTO readings VALUES (NULL,?,?,?,?)",
                 (time.time(), data.plc_id, 0, data.registers[0]))
    conn.commit(); conn.close()
    return {"status": "ok", "count": len(data.registers)}

@app.get("/api/v1/plc/{plc_id}/latest")
async def get_latest(plc_id: int):
    conn = sqlite3.connect("plc_data.db")
    row = conn.execute("SELECT * FROM readings WHERE plc_id=? ORDER BY timestamp DESC LIMIT 1",
                       (plc_id,)).fetchone()
    conn.close()
    return {"data": row} if row else {"error": "not found"}
```

```bash
pip install fastapi uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 12. DASHBOARD DAN VISUALISASI DATA

### 12.1 Node-RED

```bash
npm install -g node-red
node-red
# Buka: http://localhost:1880
```

Flow dasar: `[MQTT in] → [JSON] → [Gauge/Chart]`

### 12.2 Grafana + InfluxDB

```bash
# InfluxDB
sudo apt install influxdb && sudo systemctl start influxdb

# Grafana
sudo apt install grafana && sudo systemctl start grafana-server
# Buka: http://localhost:3000 (admin/admin)
```

---

## 13. KEAMANAN SISTEM IoT INDUSTRI

| Ancaman | Mitigasi |
|---------|---------|
| Unauthorized Modbus access | Firewall, VLAN, VPN |
| MQTT tanpa auth | Username/password + TLS |
| REST tanpa auth | API Key / JWT Token |
| Firmware lama | OTA update rutin |

**Best Practices:**
1. Segmentasi jaringan: jaringan PLC terpisah dari IT umum
2. Gunakan HTTPS, WSS, MQTTS (TLS)
3. Blokir port 502 dari internet publik
4. Catat log akses secara berkala

---

## 14. INTEGRASI AI PADA SISTEM IoT PLC

### 14.1 Use Cases

| Use Case | Teknologi |
|----------|-----------|
| Predictive Maintenance | LSTM, Random Forest |
| Anomaly Detection | Isolation Forest, OCSVM |
| Process Optimization | Reinforcement Learning |
| Quality Control | CNN, Decision Tree |

### 14.2 Deteksi Anomali Sederhana (Python)

```python
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

def train_model(data):
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(data)
    joblib.dump(model, 'anomaly.pkl')

def detect(point):
    model = joblib.load('anomaly.pkl')
    return model.predict([point])[0] == -1  # True = anomali

# Dalam loop edge device:
# registers = [val0, val1, ..., val4]
# if detect(registers[:5]):
#     send_alert("ANOMALI TERDETEKSI")
```

---

## 15. REFERENSI

1. Modbus Organization. *Modbus Application Protocol Specification V1.1b3*. https://modbus.org
2. Schneider Electric. *EcoStruxure Machine Expert – Basic Programming Guide*. https://www.se.com
3. Omron. *CP2E Series CPU Unit Software User's Manual*. https://www.ia.omron.com
4. emelianov. *modbus-esp8266 Arduino Library*. https://github.com/emelianov/modbus-esp8266
5. pymodbus. *A full Modbus protocol written in Python*. https://pymodbus.readthedocs.io
6. Eclipse Mosquitto. *An open source MQTT broker*. https://mosquitto.org
7. FastAPI. *Modern web framework for building APIs with Python*. https://fastapi.tiangolo.com
8. Node-RED. *Low-code programming for event-driven applications*. https://nodered.org
9. Grafana Labs. *Open source analytics & monitoring solution*. https://grafana.com
10. InfluxDB. *Time series database*. https://www.influxdata.com
11. EMQX. *Open Source MQTT Broker for IoT*. https://www.emqx.io
12. PlatformIO. *Professional collaborative platform for embedded development*. https://platformio.org
13. Texas Instruments. *RS-485/RS-422 Circuits Application Report SLLA272C*
14. IEC 61158. *Industrial communication networks fieldbus specifications*

---

*Dokumen ini adalah materi resmi Modul 05 Praktikum Mekatronika dan Robotika.*
