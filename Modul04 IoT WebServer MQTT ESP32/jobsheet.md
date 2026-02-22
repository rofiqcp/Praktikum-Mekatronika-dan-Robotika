# JOBSHEET MODUL 04: IoT WebServer MQTT ESP32

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 04 – IoT WebServer MQTT ESP32  
**Platform:** ESP32 + PlatformIO + Python + Node.js / FastAPI / Spring Boot / ASP.NET  
**Broker:** Mosquitto MQTT  
**Pertemuan:** 7–8 (2 × 2 SKS)  
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

1. Menjelaskan arsitektur sistem IoT secara menyeluruh, meliputi lapisan *edge*, *gateway*, *backend*, dan *frontend* serta peran masing-masing komponen
2. Menginstal dan mengonfigurasi **Mosquitto MQTT Broker** pada komputer lokal serta melakukan pengujian koneksi *publish/subscribe* menggunakan MQTT Explorer
3. Memprogram **ESP32** dengan **PlatformIO** (VS Code) untuk membaca sensor DHT22 dan LDR, kemudian mempublikasikan data sensor secara periodik ke topik MQTT
4. Membuat **Python edge device** sebagai *subscriber* MQTT yang menerima data sensor dan meneruskannya ke backend melalui REST API atau menyimpannya ke database
5. Membangun **REST API backend** menggunakan salah satu opsi: **Node.js/Express**, **Python FastAPI**, **Java Spring Boot**, atau **C# ASP.NET Core**
6. Mengintegrasikan database (**PostgreSQL** atau **MongoDB**) ke backend untuk penyimpanan data sensor secara persisten
7. Membangun **frontend dashboard** berbasis web menggunakan **Vue.js** atau **React** yang menampilkan data sensor secara *real-time* melalui WebSocket atau polling
8. Mengimplementasikan **komunikasi dua arah**: ESP32 dapat menerima perintah dari backend melalui MQTT untuk mengontrol aktuator (LED, relay)
9. Melakukan **deployment lokal** menggunakan PM2 (Node.js) atau Gunicorn (Python) dengan Nginx sebagai *reverse proxy*, serta pengujian akses eksternal menggunakan ngrok
10. Mendokumentasikan seluruh alur data sistem IoT dari sensor fisik hingga dashboard browser menggunakan diagram arsitektur dan tabel pengamatan

---

## B. KOMPETENSI YANG DICAPAI (CPMK)

| Kode | Kompetensi |
|------|-----------|
| K1 | Mampu menjelaskan dan merancang arsitektur sistem IoT multi-layer (edge → broker → backend → frontend) |
| K2 | Mampu memprogram ESP32 dengan PlatformIO untuk akuisisi data sensor dan komunikasi MQTT |
| K3 | Mampu mengonfigurasi Mosquitto MQTT Broker dan memverifikasi komunikasi *publish/subscribe* |
| K4 | Mampu membangun REST API backend yang terhubung ke MQTT broker dan database |
| K5 | Mampu mengintegrasikan database relasional (PostgreSQL) atau non-relasional (MongoDB) ke sistem IoT |
| K6 | Mampu membuat frontend dashboard web yang menampilkan data sensor secara *real-time* |
| K7 | Mampu mengimplementasikan kontrol aktuator berbasis MQTT dari antarmuka web |
| K8 | Mampu melakukan deployment aplikasi backend dan frontend serta pengujian akses jaringan |

---

## C. ALAT DAN BAHAN

### Perangkat Keras (Hardware)

| No | Komponen | Jumlah | Keterangan |
|----|---------|--------|------------|
| 1 | ESP32 DevKit V1 / ESP32-WROOM-32 | 1 | Mikrokontroler utama dengan WiFi |
| 2 | Sensor DHT22 (AM2302) | 1 | Suhu dan kelembaban |
| 3 | Sensor LDR (Light Dependent Resistor) | 1 | Intensitas cahaya |
| 4 | LED (merah dan hijau) | 2 | Indikator status aktuator |
| 5 | Relay Module 5V 1-Channel | 1 | Aktuator on/off beban |
| 6 | Resistor 10 kΩ | 2 | Pull-up DHT22 dan voltage divider LDR |
| 7 | Resistor 220 Ω | 2 | Current limiter LED |
| 8 | Breadboard 400 titik | 1 | Prototyping |
| 9 | Kabel jumper male-male dan male-female | 20+ | Koneksi komponen |
| 10 | Kabel USB Type-A ke Micro-B / USB-C | 1 | Power + upload program ESP32 |
| 11 | Laptop / PC (minimum RAM 8 GB) | 1 | Development environment |

### Skema Wiring ESP32

```
ESP32 Pin   →  Komponen
─────────────────────────────────────────────────────
GPIO 4      →  DHT22 DATA pin (dengan pull-up 10kΩ ke 3V3)
GPIO 34     →  LDR (pembagi tegangan: LDR + 10kΩ ke GND)
GPIO 2      →  LED Hijau (+ resistor 220Ω ke GND)
GPIO 5      →  LED Merah (+ resistor 220Ω ke GND)
GPIO 26     →  Relay IN pin
3V3         →  DHT22 VCC, LDR salah satu ujung
GND         →  DHT22 GND, Relay GND, LED GND
```

> **Perhatian:** GPIO 34 adalah *input-only* pin, cocok untuk ADC pembaca LDR. Jangan gunakan untuk output.

### Perangkat Lunak (Software)

| No | Software | Versi | Fungsi | Unduhan |
|----|---------|-------|--------|---------|
| 1 | **Visual Studio Code** | ≥ 1.85 | Code editor utama | https://code.visualstudio.com |
| 2 | **PlatformIO IDE** (ekstensi VS Code) | ≥ 6.1 | Pemrograman ESP32 / embedded | https://platformio.org/install/ide?install=vscode |
| 3 | **Mosquitto MQTT Broker** | ≥ 2.0 | MQTT broker lokal | https://mosquitto.org/download |
| 4 | **MQTT Explorer** | ≥ 0.4 | GUI monitoring MQTT | https://mqtt-explorer.com |
| 5 | **Python** | ≥ 3.10 | Edge device & backend (FastAPI) | https://python.org/downloads |
| 6 | **Node.js + npm** | ≥ 20 LTS | Backend (Express) & frontend build tool | https://nodejs.org |
| 7 | **JDK 17 + Maven** | JDK 17 LTS | Backend Spring Boot (opsional) | https://adoptium.net |
| 8 | **.NET SDK** | ≥ 8.0 | Backend ASP.NET Core (opsional) | https://dotnet.microsoft.com/download |
| 9 | **PostgreSQL** | ≥ 16 | Database relasional | https://www.postgresql.org/download |
| 10 | **MongoDB Community** | ≥ 7.0 | Database non-relasional (alternatif) | https://www.mongodb.com/try/download/community |
| 11 | **DBeaver Community** | ≥ 23 | GUI database universal | https://dbeaver.io/download |
| 12 | **Postman** | ≥ 10 | Pengujian REST API | https://www.postman.com/downloads |
| 13 | **PM2** (`npm i -g pm2`) | ≥ 5 | Process manager Node.js | https://pm2.keymetrics.io |
| 14 | **ngrok** | ≥ 3 | Tunnel akses publik | https://ngrok.com/download |
| 15 | **Git** | ≥ 2.40 | Version control | https://git-scm.com |

> **Catatan:** Pilih satu opsi backend sesuai track studi:
> - **Track A (JavaScript):** Node.js/Express + Vue.js
> - **Track B (Python):** FastAPI + React
> - **Track C (Java):** Spring Boot + Vue.js
> - **Track D (C#):** ASP.NET Core + React

---

## D. DASAR TEORI SINGKAT

### D.1 Protokol MQTT

**MQTT** (*Message Queuing Telemetry Transport*) adalah protokol komunikasi ringan berbasis *publish/subscribe* yang dirancang untuk perangkat IoT dengan sumber daya terbatas dan koneksi bandwidth rendah. MQTT bekerja di atas TCP/IP dengan port default **1883** (tanpa TLS) atau **8883** (dengan TLS).

**Konsep utama MQTT:**

| Istilah | Penjelasan |
|---------|-----------|
| **Broker** | Server pusat yang menerima dan mendistribusikan pesan (contoh: Mosquitto, HiveMQ, EMQX) |
| **Publisher** | Klien yang mengirim (*publish*) pesan ke suatu topik |
| **Subscriber** | Klien yang berlangganan (*subscribe*) topik untuk menerima pesan |
| **Topic** | String hierarkis sebagai alamat pesan (contoh: `sensor/ruang_a/suhu`) |
| **QoS 0** | *At most once* – pesan dikirim sekali, tidak ada konfirmasi |
| **QoS 1** | *At least once* – pesan dijamin sampai, mungkin duplikat |
| **QoS 2** | *Exactly once* – paling andal, overhead paling besar |
| **Retain** | Broker menyimpan pesan terakhir; subscriber baru langsung dapat data terbaru |
| **LWT** | *Last Will and Testament* – pesan otomatis dikirim jika klien terputus mendadak |

### D.2 Arsitektur Sistem IoT yang Dibangun

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SISTEM IoT PRAKTIKUM                         │
├─────────────────┬──────────────────┬──────────────────┬────────────┤
│   LAYER EDGE    │  LAYER BROKER    │  LAYER BACKEND   │  LAYER UI  │
│                 │                  │                  │            │
│  ┌───────────┐  │  ┌────────────┐  │  ┌────────────┐  │  ┌──────┐  │
│  │  ESP32    │  │  │ Mosquitto  │  │  │ REST API   │  │  │ Web  │  │
│  │ + DHT22   │──┼─▶│   MQTT     │──┼─▶│ (Express / │  │  │ App  │  │
│  │ + LDR     │  │  │  Broker   │  │  │  FastAPI / │──┼─▶│(Vue/ │  │
│  │ + LED     │  │  │:1883       │  │  │  Spring /  │  │  │React)│  │
│  │ + Relay   │  │  └────────────┘  │  │  ASP.NET)  │  │  └──────┘  │
│  └───────────┘  │        ▲         │  └─────┬──────┘  │     ▲      │
│       ▲         │        │         │        │          │     │      │
│  ┌───────────┐  │  ┌─────┴──────┐  │  ┌─────▼──────┐  │  WebSocket │
│  │  Python   │──┼─▶│ paho-mqtt  │  │  │  Database  │  │  / HTTP    │
│  │  Edge Dev │  │  │ (Python)   │  │  │(PostgreSQL/│  │  Polling   │
│  │ (Laptop)  │  │  └────────────┘  │  │  MongoDB)  │  │            │
│  └───────────┘  │                  │  └────────────┘  │            │
└─────────────────┴──────────────────┴──────────────────┴────────────┘
       WiFi             TCP/IP             HTTP/WS           Browser
```

**Alur data:**
1. ESP32 membaca sensor DHT22 (suhu, kelembaban) dan LDR (cahaya) setiap 5 detik
2. ESP32 *publish* data JSON ke topik MQTT: `iot/sensor/data`
3. Python edge device / backend *subscribe* ke topik tersebut
4. Backend menyimpan data ke database dan menyediakan REST API
5. Frontend mengambil data melalui API atau WebSocket dan menampilkan grafik *real-time*
6. User dapat mengirim perintah dari dashboard → backend → MQTT publish ke `iot/aktuator/cmd` → ESP32 menerima dan menjalankan perintah

### D.3 ESP32 dan PlatformIO

**ESP32** adalah mikrokontroler dual-core Xtensa LX6 240 MHz dengan WiFi 802.11 b/g/n dan Bluetooth terintegrasi. Diprogram dengan **Arduino framework** melalui **PlatformIO** yang memberikan manajemen library dan build system lebih baik dari Arduino IDE.

**Library penting untuk modul ini:**
- `knolleary/PubSubClient` – klien MQTT untuk Arduino/ESP32
- `adafruit/DHT sensor library` – driver sensor DHT22
- `adafruit/Adafruit Unified Sensor` – dependensi DHT library
- `bblanchon/ArduinoJson` – serialisasi/deserialisasi JSON

### D.4 Struktur Topik MQTT yang Digunakan

```
iot/
├── sensor/
│   └── data          ← ESP32 publish data sensor (JSON)
├── aktuator/
│   ├── cmd           ← Backend publish perintah ke ESP32
│   └── status        ← ESP32 publish status aktuator
└── system/
    ├── heartbeat     ← ESP32 publish heartbeat setiap 30 detik
    └── log           ← Pesan log/error
```

**Contoh payload JSON sensor:**
```json
{
  "device_id": "esp32_lab01",
  "timestamp": 1710000000,
  "temperature": 27.5,
  "humidity": 65.2,
  "light_raw": 2048,
  "light_percent": 50.0
}
```

**Contoh payload JSON perintah aktuator:**
```json
{
  "command": "led_green",
  "state": true,
  "source": "dashboard_user"
}
```

---

## E. LANGKAH KERJA

---

### SESI 1: PERSIAPAN ENVIRONMENT

---

#### LANGKAH 1: Instalasi dan Konfigurasi Mosquitto MQTT Broker

**Estimasi waktu: 20 menit**

**A. Instalasi Mosquitto:**

**Windows:**
1. Download installer dari https://mosquitto.org/download → pilih Windows installer 64-bit
2. Jalankan installer → centang *Install as a service*
3. Buka **Services** (`services.msc`) → pastikan **Mosquitto Broker** sudah *Running*

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

**macOS (via Homebrew):**
```bash
brew install mosquitto
brew services start mosquitto
```

**B. Konfigurasi Mosquitto (izinkan koneksi lokal tanpa autentikasi):**

1. Cari file konfigurasi Mosquitto:
   - Windows: `C:\Program Files\mosquitto\mosquitto.conf`
   - Linux: `/etc/mosquitto/mosquitto.conf`
   - macOS: `/usr/local/etc/mosquitto/mosquitto.conf`

2. Tambahkan baris berikut di akhir file:
   ```
   listener 1883
   allow_anonymous true
   ```

3. Restart Mosquitto:
   - Windows: `net stop mosquitto && net start mosquitto`
   - Linux/macOS: `sudo systemctl restart mosquitto`

**C. Pengujian Mosquitto via command line:**

Buka **dua terminal** secara bersamaan:

*Terminal 1 (subscriber):*
```bash
mosquitto_sub -h localhost -t "iot/test" -v
```

*Terminal 2 (publisher):*
```bash
mosquitto_pub -h localhost -t "iot/test" -m "Hello MQTT dari Terminal"
```

→ Terminal 1 harus menampilkan: `iot/test Hello MQTT dari Terminal`

**D. Pengujian dengan MQTT Explorer:**

1. Buka MQTT Explorer → klik `+` untuk koneksi baru
2. Isi:
   - Host: `localhost`
   - Port: `1883`
   - Protocol: `mqtt://`
3. Klik **Connect**
4. Publish pesan ke topik `iot/test` melalui GUI
5. Amati topic tree yang terbentuk

**Checkpoint ✅:** Mosquitto berjalan, komunikasi publish/subscribe berhasil di dua terminal, MQTT Explorer terhubung.

---

#### LANGKAH 2: Setup Project ESP32 dengan PlatformIO

**Estimasi waktu: 25 menit**

1. Buka VS Code → pastikan ekstensi **PlatformIO IDE** sudah terinstal
2. Klik ikon PlatformIO (semut) → **New Project**
3. Isi:
   - Name: `IoT_ESP32_MQTT`
   - Board: `Espressif ESP32 Dev Module`
   - Framework: `Arduino`
   - Location: Pilih folder kerja kelompok
4. Klik **Finish** → tunggu proses indexing selesai

5. Edit file `platformio.ini`:
   ```ini
   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   monitor_speed = 115200
   lib_deps =
       knolleary/PubSubClient @ ^2.8
       adafruit/DHT sensor library @ ^1.4.6
       adafruit/Adafruit Unified Sensor @ ^1.1.14
       bblanchon/ArduinoJson @ ^7.0.4
   ```

6. Simpan dengan `Ctrl+S` → PlatformIO otomatis mengunduh library

7. Buat file konfigurasi `include/config.h`:
   ```cpp
   #ifndef CONFIG_H
   #define CONFIG_H

   // Konfigurasi WiFi
   #define WIFI_SSID     "SSID_WIFI_ANDA"
   #define WIFI_PASSWORD "PASSWORD_WIFI_ANDA"

   // Konfigurasi MQTT Broker
   // Ganti dengan IP komputer di jaringan yang sama
   #define MQTT_BROKER   "192.168.x.x"
   #define MQTT_PORT     1883
   #define DEVICE_ID     "esp32_lab01"

   // Pin sensor dan aktuator
   #define PIN_DHT       4
   #define PIN_LDR       34
   #define PIN_LED_GREEN 2
   #define PIN_LED_RED   5
   #define PIN_RELAY     26

   // Interval publish (ms)
   #define PUBLISH_INTERVAL 5000

   #endif
   ```

> **Cara cari IP komputer:** Windows: `ipconfig` | Linux/macOS: `ip addr` atau `ifconfig`

**Checkpoint ✅:** Project PlatformIO berhasil dibuat, library terunduh, file `config.h` sudah diisi IP broker.

---

#### LANGKAH 3: Setup Python Environment

**Estimasi waktu: 15 menit**

1. Verifikasi Python sudah terinstal:
   ```bash
   python --version    # atau python3 --version
   pip --version
   ```

2. Buat virtual environment untuk proyek ini:
   ```bash
   # Buat folder proyek Python
   mkdir iot_edge_python && cd iot_edge_python
   python -m venv venv

   # Aktifkan virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Install library Python yang diperlukan:
   ```bash
   pip install paho-mqtt requests python-dotenv fastapi uvicorn sqlalchemy psycopg2-binary pymongo
   ```

4. Simpan daftar dependensi:
   ```bash
   pip freeze > requirements.txt
   ```

5. Buat file `.env` untuk konfigurasi:
   ```
   MQTT_BROKER=localhost
   MQTT_PORT=1883
   DB_URL=postgresql://user:password@localhost:5432/iot_db
   API_PORT=8000
   ```

**Checkpoint ✅:** Virtual environment aktif, semua library Python terinstal, file `.env` tersedia.

---

### SESI 2: ESP32 DAN PYTHON EDGE DEVICE

---

#### LANGKAH 4: Program ESP32 – Baca Sensor dan Publish ke MQTT

**Estimasi waktu: 40 menit**

Buat program utama di `src/main.cpp`:

```cpp
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include "config.h"

// Objek global
WiFiClient   espClient;
PubSubClient mqtt(espClient);
DHT          dht(PIN_DHT, DHT22);

unsigned long lastPublish = 0;

// Fungsi koneksi WiFi
void connectWiFi() {
  Serial.print("Menghubungkan ke WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi terhubung. IP: " + WiFi.localIP().toString());
}

// Callback MQTT – menerima perintah dari broker
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg = "";
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.println("Pesan diterima [" + String(topic) + "]: " + msg);

  // Parse perintah JSON
  JsonDocument doc;
  if (deserializeJson(doc, msg) == DeserializationError::Ok) {
    const char* command = doc["command"];
    bool state = doc["state"];

    if (strcmp(command, "led_green") == 0) {
      digitalWrite(PIN_LED_GREEN, state ? HIGH : LOW);
    } else if (strcmp(command, "led_red") == 0) {
      digitalWrite(PIN_LED_RED, state ? HIGH : LOW);
    } else if (strcmp(command, "relay") == 0) {
      digitalWrite(PIN_RELAY, state ? HIGH : LOW);
    }

    // Publish status aktuator kembali
    mqtt.publish("iot/aktuator/status", msg.c_str());
  }
}

// Fungsi koneksi MQTT
void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Menghubungkan ke MQTT broker...");
    String clientId = "ESP32-" + String(DEVICE_ID);
    if (mqtt.connect(clientId.c_str())) {
      Serial.println("Terhubung!");
      mqtt.subscribe("iot/aktuator/cmd");
      mqtt.publish("iot/system/heartbeat", "online");
    } else {
      Serial.println("Gagal, rc=" + String(mqtt.state()) + " coba lagi dalam 3 detik");
      delay(3000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_RED,   OUTPUT);
  pinMode(PIN_RELAY,     OUTPUT);
  dht.begin();

  connectWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  connectMQTT();
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL) {
    lastPublish = now;

    // Baca sensor
    float temperature = dht.readTemperature();
    float humidity    = dht.readHumidity();
    int   lightRaw    = analogRead(PIN_LDR);
    float lightPct    = (lightRaw / 4095.0) * 100.0;

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Gagal membaca DHT22!");
      return;
    }

    // Buat payload JSON
    JsonDocument doc;
    doc["device_id"]      = DEVICE_ID;
    doc["timestamp"]      = millis() / 1000;
    doc["temperature"]    = round(temperature * 10) / 10.0;
    doc["humidity"]       = round(humidity * 10) / 10.0;
    doc["light_raw"]      = lightRaw;
    doc["light_percent"]  = round(lightPct * 10) / 10.0;

    String payload;
    serializeJson(doc, payload);

    // Publish ke broker
    bool success = mqtt.publish("iot/sensor/data", payload.c_str());
    Serial.println("Publish " + String(success ? "OK" : "GAGAL") + ": " + payload);
  }
}
```

**Upload dan uji:**
1. Sambungkan ESP32 via USB
2. Pilih port di PlatformIO (status bar bawah)
3. Klik **Upload** (→ ikon) atau `Ctrl+Alt+U`
4. Buka **Serial Monitor** (`Ctrl+Alt+M`) → amati output
5. Di MQTT Explorer, amati topik `iot/sensor/data` → data JSON harus muncul setiap 5 detik

**Checkpoint ✅:** ESP32 terhubung WiFi & MQTT, data sensor tampil di Serial Monitor dan MQTT Explorer setiap 5 detik.

---

#### LANGKAH 5: Python Subscriber – Menerima Data dari Broker

**Estimasi waktu: 25 menit**

Buat file `subscriber.py` di folder `iot_edge_python/`:

```python
import json
import signal
import sys
from datetime import datetime
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

BROKER   = os.getenv("MQTT_BROKER", "localhost")
PORT     = int(os.getenv("MQTT_PORT", 1883))
TOPIC_IN = "iot/sensor/data"

# Penyimpanan sementara data terakhir
latest_data: dict = {}

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"[{datetime.now()}] Terhubung ke broker MQTT: {reason_code}")
    client.subscribe(TOPIC_IN, qos=1)
    print(f"Berlangganan topik: {TOPIC_IN}")

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        latest_data = payload
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[{ts}] Data diterima dari {payload.get('device_id', '?')}:")
        print(f"  Suhu     : {payload.get('temperature')} °C")
        print(f"  Kelembaban: {payload.get('humidity')} %")
        print(f"  Cahaya   : {payload.get('light_percent')} %")
        print("-" * 40)
    except json.JSONDecodeError as e:
        print(f"Error parse JSON: {e}")

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"Terputus dari broker: {reason_code}")

def signal_handler(sig, frame):
    print("\nMenghentikan subscriber...")
    client.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect    = on_connect
client.on_message    = on_message
client.on_disconnect = on_disconnect

print(f"Menghubungkan ke MQTT broker {BROKER}:{PORT}...")
client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
```

Jalankan:
```bash
python subscriber.py
```

Amati output – data sensor dari ESP32 harus muncul setiap 5 detik.

**Checkpoint ✅:** Python subscriber berjalan dan mencetak data sensor dari ESP32 secara real-time.

---

#### LANGKAH 6: Python Publisher – Kirim Perintah ke ESP32

**Estimasi waktu: 20 menit**

Buat file `publisher_cmd.py` untuk mengirim perintah ke ESP32:

```python
import json
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

BROKER      = os.getenv("MQTT_BROKER", "localhost")
PORT        = int(os.getenv("MQTT_PORT", 1883))
TOPIC_CMD   = "iot/aktuator/cmd"
TOPIC_STATUS = "iot/aktuator/status"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Terhubung: {reason_code}")
    client.subscribe(TOPIC_STATUS)

def on_message(client, userdata, msg):
    print(f"Status aktuator: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT)
client.loop_start()

# Kirim sekuens perintah untuk pengujian
commands = [
    {"command": "led_green", "state": True,  "source": "python_test"},
    {"command": "led_red",   "state": True,  "source": "python_test"},
    {"command": "relay",     "state": True,  "source": "python_test"},
    {"command": "led_green", "state": False, "source": "python_test"},
    {"command": "led_red",   "state": False, "source": "python_test"},
    {"command": "relay",     "state": False, "source": "python_test"},
]

for cmd in commands:
    payload = json.dumps(cmd)
    result  = client.publish(TOPIC_CMD, payload, qos=1)
    print(f"Publish perintah: {payload} → {'OK' if result.rc == 0 else 'GAGAL'}")
    time.sleep(2)

client.loop_stop()
client.disconnect()
print("Selesai.")
```

Jalankan dan amati LED/relay di ESP32:
```bash
python publisher_cmd.py
```

**Checkpoint ✅:** Perintah berhasil dikirim, LED dan relay di ESP32 merespons sesuai perintah, status aktuator diterima kembali.

---

### SESI 3: BACKEND DAN FRONTEND SERVER

---

#### LANGKAH 7: Setup Backend REST API

**Estimasi waktu: 45 menit**

Pilih **salah satu** opsi backend sesuai track studi. Semua opsi mengekspos endpoint yang sama.

---

##### OPSI A: Node.js/Express (Track A)

```bash
mkdir iot_backend_node && cd iot_backend_node
npm init -y
npm install express mqtt pg sequelize dotenv cors ws
```

Buat `server.js`:

```javascript
const express   = require('express');
const mqtt      = require('mqtt');
const { Sequelize, DataTypes } = require('sequelize');
const cors      = require('cors');
const WebSocket = require('ws');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Database (PostgreSQL via Sequelize)
const sequelize = new Sequelize(process.env.DB_URL, { logging: false });
const SensorData = sequelize.define('SensorData', {
  device_id:     { type: DataTypes.STRING },
  temperature:   { type: DataTypes.FLOAT },
  humidity:      { type: DataTypes.FLOAT },
  light_raw:     { type: DataTypes.INTEGER },
  light_percent: { type: DataTypes.FLOAT },
  recorded_at:   { type: DataTypes.DATE, defaultValue: DataTypes.NOW },
}, { tableName: 'sensor_data', timestamps: false });

// MQTT Client
const mqttClient = mqtt.connect(`mqtt://${process.env.MQTT_BROKER}:${process.env.MQTT_PORT}`);
mqttClient.on('connect', () => {
  console.log('Backend terhubung ke MQTT broker');
  mqttClient.subscribe('iot/sensor/data', { qos: 1 });
});

// WebSocket untuk streaming ke frontend
const wss = new WebSocket.Server({ noServer: true });
const wsClients = new Set();
wss.on('connection', ws => { wsClients.add(ws); ws.on('close', () => wsClients.delete(ws)); });

mqttClient.on('message', async (topic, payload) => {
  if (topic === 'iot/sensor/data') {
    try {
      const data = JSON.parse(payload.toString());
      await SensorData.create(data);
      // Broadcast ke semua WebSocket client
      const msg = JSON.stringify({ type: 'sensor_update', data });
      wsClients.forEach(ws => ws.readyState === WebSocket.OPEN && ws.send(msg));
    } catch (e) { console.error('DB error:', e.message); }
  }
});

// REST Endpoints
app.get('/api/sensor/latest',      async (req, res) => {
  const row = await SensorData.findOne({ order: [['id', 'DESC']] });
  res.json(row);
});
app.get('/api/sensor/history',     async (req, res) => {
  const rows = await SensorData.findAll({ order: [['id', 'DESC']], limit: 100 });
  res.json(rows);
});
app.post('/api/aktuator/command',  (req, res) => {
  const cmd = JSON.stringify(req.body);
  mqttClient.publish('iot/aktuator/cmd', cmd, { qos: 1 });
  res.json({ status: 'ok', published: req.body });
});

const PORT = process.env.API_PORT || 3000;
const server = app.listen(PORT, async () => {
  await sequelize.sync();
  console.log(`Backend berjalan di http://localhost:${PORT}`);
});
server.on('upgrade', (req, socket, head) => wss.handleUpgrade(req, socket, head, ws => wss.emit('connection', ws)));
```

Jalankan: `node server.js`

---

##### OPSI B: Python FastAPI (Track B)

```bash
cd iot_edge_python
pip install fastapi uvicorn sqlalchemy psycopg2-binary paho-mqtt websockets python-dotenv
```

Buat `main_api.py`:

```python
import json, asyncio
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Session
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(title="IoT Dashboard API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Database
engine = create_engine(os.getenv("DB_URL"))
class Base(DeclarativeBase): pass
class SensorData(Base):
    __tablename__ = "sensor_data"
    id            = Column(Integer, primary_key=True)
    device_id     = Column(String)
    temperature   = Column(Float)
    humidity      = Column(Float)
    light_raw     = Column(Integer)
    light_percent = Column(Float)
    recorded_at   = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

ws_clients: list[WebSocket] = []
latest: dict = {}

# MQTT setup
def on_message(client, userdata, msg):
    global latest
    data = json.loads(msg.payload)
    latest = data
    with Session(engine) as s:
        s.add(SensorData(**{k: data[k] for k in ("device_id","temperature","humidity","light_raw","light_percent")}))
        s.commit()
    asyncio.run(broadcast(data))

async def broadcast(data):
    dead = []
    for ws in ws_clients:
        try: await ws.send_json({"type": "sensor_update", "data": data})
        except: dead.append(ws)
    for ws in dead: ws_clients.remove(ws)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_message = on_message
mqttc.connect(os.getenv("MQTT_BROKER","localhost"), int(os.getenv("MQTT_PORT",1883)))
mqttc.subscribe("iot/sensor/data", qos=1)
mqttc.loop_start()

# REST & WebSocket endpoints
@app.get("/api/sensor/latest")
def get_latest():
    with Session(engine) as s:
        row = s.query(SensorData).order_by(SensorData.id.desc()).first()
        return row.__dict__ if row else {}

@app.get("/api/sensor/history")
def get_history(limit: int = 100):
    with Session(engine) as s:
        rows = s.query(SensorData).order_by(SensorData.id.desc()).limit(limit).all()
        return [r.__dict__ for r in rows]

@app.post("/api/aktuator/command")
def send_command(body: dict):
    mqttc.publish("iot/aktuator/cmd", json.dumps(body), qos=1)
    return {"status": "ok", "published": body}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    ws_clients.append(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect:
        ws_clients.remove(ws)
```

Jalankan: `uvicorn main_api:app --reload --port 8000`

**Uji API dengan Postman:**
- `GET http://localhost:3000/api/sensor/latest` (Node) atau `GET http://localhost:8000/api/sensor/latest` (Python)
- `POST /api/aktuator/command` dengan body `{"command":"led_green","state":true}`

**Checkpoint ✅:** Backend berjalan, endpoint `/api/sensor/latest` mengembalikan data JSON, POST command berhasil mengontrol ESP32.

---

#### LANGKAH 8: Integrasi Database PostgreSQL

**Estimasi waktu: 25 menit**

**A. Instalasi dan konfigurasi PostgreSQL:**

1. Download dan install PostgreSQL dari https://www.postgresql.org/download
2. Buka pgAdmin atau psql dan buat database:
   ```sql
   CREATE DATABASE iot_db;
   CREATE USER iot_user WITH PASSWORD 'iot_password';
   GRANT ALL PRIVILEGES ON DATABASE iot_db TO iot_user;
   ```

3. Buat tabel `sensor_data`:
   ```sql
   \c iot_db;

   CREATE TABLE sensor_data (
       id            SERIAL PRIMARY KEY,
       device_id     VARCHAR(50)  NOT NULL,
       temperature   NUMERIC(5,2),
       humidity      NUMERIC(5,2),
       light_raw     INTEGER,
       light_percent NUMERIC(5,2),
       recorded_at   TIMESTAMPTZ  DEFAULT NOW()
   );

   CREATE INDEX idx_sensor_device   ON sensor_data(device_id);
   CREATE INDEX idx_sensor_recorded ON sensor_data(recorded_at DESC);
   ```

4. Update file `.env`:
   ```
   DB_URL=postgresql://iot_user:iot_password@localhost:5432/iot_db
   ```

**B. Verifikasi data masuk dengan DBeaver:**

1. Buka DBeaver → New Connection → PostgreSQL
2. Isi host `localhost`, port `5432`, database `iot_db`, user `iot_user`
3. Test Connection → OK
4. Browse tabel `sensor_data` → amati data yang masuk dari ESP32
5. Screenshot tabel berisi minimal 10 baris data

**Checkpoint ✅:** Database `iot_db` dapat diakses via DBeaver, data sensor tersimpan otomatis setiap backend menerima MQTT.

---

#### LANGKAH 9: Frontend Dashboard Web

**Estimasi waktu: 50 menit**

Pilih **salah satu** opsi frontend sesuai track studi.

---

##### OPSI A: Vue.js + Chart.js (Track A & C)

```bash
npm create vue@latest iot-dashboard -- --template default
cd iot-dashboard
npm install chart.js vue-chartjs axios
npm run dev
```

Edit `src/App.vue`:

```vue
<template>
  <div class="dashboard">
    <header>
      <h1>🌡️ IoT Dashboard – Modul 04</h1>
      <span :class="wsStatus === 'Terhubung' ? 'badge-ok' : 'badge-err'">
        WS: {{ wsStatus }}
      </span>
    </header>

    <section class="cards">
      <div class="card">
        <p class="label">Suhu</p>
        <p class="value">{{ sensor.temperature ?? '—' }} °C</p>
      </div>
      <div class="card">
        <p class="label">Kelembaban</p>
        <p class="value">{{ sensor.humidity ?? '—' }} %</p>
      </div>
      <div class="card">
        <p class="label">Cahaya</p>
        <p class="value">{{ sensor.light_percent ?? '—' }} %</p>
      </div>
    </section>

    <section class="chart-section">
      <Line :data="chartData" :options="chartOptions" />
    </section>

    <section class="controls">
      <h2>Kontrol Aktuator</h2>
      <button @click="sendCommand('led_green', true)"  class="btn-on">LED Hijau ON</button>
      <button @click="sendCommand('led_green', false)" class="btn-off">LED Hijau OFF</button>
      <button @click="sendCommand('led_red',   true)"  class="btn-on">LED Merah ON</button>
      <button @click="sendCommand('led_red',   false)" class="btn-off">LED Merah OFF</button>
      <button @click="sendCommand('relay',     true)"  class="btn-on">Relay ON</button>
      <button @click="sendCommand('relay',     false)" class="btn-off">Relay OFF</button>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend } from 'chart.js'
import axios from 'axios'

Chart.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend)

const API_BASE = 'http://localhost:3000/api'  // ganti ke port FastAPI jika Track B
const WS_URL   = 'ws://localhost:3000'         // ganti ke ws://localhost:8000/ws jika Track B

const sensor    = reactive({})
const wsStatus  = ref('Menghubungkan...')
const labels    = ref([])
const tempData  = ref([])
const humData   = ref([])
let   ws        = null

const chartData = reactive({
  labels,
  datasets: [
    { label: 'Suhu (°C)',     data: tempData, borderColor: '#e74c3c', tension: 0.4, fill: false },
    { label: 'Kelembaban (%)',data: humData,  borderColor: '#3498db', tension: 0.4, fill: false },
  ],
})
const chartOptions = { responsive: true, animation: false }

async function loadHistory() {
  const { data } = await axios.get(`${API_BASE}/sensor/history`)
  data.reverse().slice(-20).forEach(d => {
    labels.value.push(new Date(d.recorded_at).toLocaleTimeString())
    tempData.value.push(d.temperature)
    humData.value.push(d.humidity)
  })
}

function connectWS() {
  ws = new WebSocket(WS_URL)
  ws.onopen = () => { wsStatus.value = 'Terhubung' }
  ws.onmessage = ({ data }) => {
    const msg = JSON.parse(data)
    if (msg.type === 'sensor_update') {
      Object.assign(sensor, msg.data)
      labels.value.push(new Date().toLocaleTimeString())
      tempData.value.push(msg.data.temperature)
      humData.value.push(msg.data.humidity)
      if (labels.value.length > 20) { labels.value.shift(); tempData.value.shift(); humData.value.shift() }
    }
  }
  ws.onclose = () => { wsStatus.value = 'Terputus'; setTimeout(connectWS, 3000) }
}

async function sendCommand(command, state) {
  await axios.post(`${API_BASE}/aktuator/command`, { command, state, source: 'dashboard' })
}

onMounted(() => { loadHistory(); connectWS() })
onUnmounted(() => ws?.close())
</script>

<style scoped>
.dashboard  { font-family: sans-serif; padding: 1rem; max-width: 900px; margin: auto; }
.cards      { display: flex; gap: 1rem; margin: 1rem 0; }
.card       { flex: 1; background: #f4f6f8; border-radius: 8px; padding: 1rem; text-align: center; }
.label      { color: #7f8c8d; font-size: 0.85rem; }
.value      { font-size: 2rem; font-weight: bold; color: #2c3e50; }
.controls   { margin-top: 1rem; }
.btn-on     { background: #27ae60; color: white; margin: 4px; padding: 8px 14px; border: none; border-radius: 4px; cursor: pointer; }
.btn-off    { background: #e74c3c; color: white; margin: 4px; padding: 8px 14px; border: none; border-radius: 4px; cursor: pointer; }
.badge-ok   { background: #27ae60; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; }
.badge-err  { background: #e74c3c; color: white; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; }
</style>
```

Jalankan frontend:
```bash
npm run dev
# Akses di http://localhost:5173
```

**Checkpoint ✅:** Dashboard menampilkan data sensor secara real-time, grafik terbaru, tombol kontrol aktuator berfungsi.

---

#### LANGKAH 10: Deployment dengan PM2/Nginx dan ngrok

**Estimasi waktu: 30 menit**

**A. Deployment Backend dengan PM2 (Node.js) atau Gunicorn (Python):**

*Node.js (Track A/C):*
```bash
npm install -g pm2
pm2 start server.js --name iot-backend
pm2 save
pm2 startup     # ikuti instruksi yang muncul untuk autostart
pm2 status      # cek status
pm2 logs iot-backend  # lihat log
```

*Python FastAPI (Track B):*
```bash
pip install gunicorn
pm2 start "uvicorn main_api:app --port 8000" --name iot-api-python --interpreter python
# atau gunakan systemd service
```

**B. Build Frontend untuk Produksi:**
```bash
cd iot-dashboard
npm run build
# Output di folder dist/
```

**C. Nginx sebagai Reverse Proxy (opsional – jika Nginx terinstal):**

Konfigurasi `/etc/nginx/sites-available/iot`:
```nginx
server {
    listen 80;
    server_name localhost;

    # Frontend static
    location / {
        root /path/to/iot-dashboard/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade    $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/iot /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

**D. Akses Publik via ngrok:**

1. Daftar akun di https://ngrok.com → salin auth token
2. Autentikasi ngrok:
   ```bash
   ngrok config add-authtoken TOKEN_ANDA
   ```
3. Expose backend:
   ```bash
   ngrok http 3000     # Track A/C (Node.js)
   # atau
   ngrok http 8000     # Track B (Python)
   ```
4. Salin URL ngrok (contoh: `https://abcd1234.ngrok-free.app`)
5. Update `API_BASE` di konfigurasi frontend dengan URL ngrok
6. Rebuild frontend: `npm run build`
7. Akses dashboard dari HP atau laptop lain menggunakan URL ngrok

**Checkpoint ✅:** Backend berjalan via PM2 (persistent), frontend dapat diakses lewat browser, URL ngrok dapat dibuka dari perangkat lain.

---

## F. TABEL PENGAMATAN DAN DATA

### F.1 Data Lingkungan – Pengukuran Sensor

Catat 10 data berturut-turut dari ESP32 setiap 30 detik:

| No | Waktu | Suhu (°C) | Kelembaban (%) | Cahaya (ADC raw) | Cahaya (%) | Kondisi Ruangan |
|----|-------|-----------|----------------|-----------------|------------|----------------|
| 1  |       |           |                |                 |            |                |
| 2  |       |           |                |                 |            |                |
| 3  |       |           |                |                 |            |                |
| 4  |       |           |                |                 |            |                |
| 5  |       |           |                |                 |            |                |
| 6  |       |           |                |                 |            |                |
| 7  |       |           |                |                 |            |                |
| 8  |       |           |                |                 |            |                |
| 9  |       |           |                |                 |            |                |
| 10 |       |           |                |                 |            |                |
| **Rata-rata** | | | | | | |
| **Min** | | | | | | |
| **Max** | | | | | | |

### F.2 Pengujian Aktuator – Respons Waktu

Ukur waktu dari klik tombol di dashboard hingga LED/relay merespons:

| No | Perintah | Waktu Kirim | Waktu Respons ESP32 | Δt (ms) | Berhasil? |
|----|---------|-------------|---------------------|---------|-----------|
| 1  | LED Hijau ON  |  |  |  | ☐ Ya ☐ Tidak |
| 2  | LED Hijau OFF |  |  |  | ☐ Ya ☐ Tidak |
| 3  | LED Merah ON  |  |  |  | ☐ Ya ☐ Tidak |
| 4  | LED Merah OFF |  |  |  | ☐ Ya ☐ Tidak |
| 5  | Relay ON      |  |  |  | ☐ Ya ☐ Tidak |
| 6  | Relay OFF     |  |  |  | ☐ Ya ☐ Tidak |

**Rata-rata latency:** ________ ms

### F.3 Pengujian Koneksi MQTT

| Parameter | Nilai Pengamatan |
|-----------|-----------------|
| IP komputer (MQTT broker) | |
| IP ESP32 (dari Serial Monitor) | |
| QoS yang digunakan | |
| Port MQTT | |
| Jumlah topik yang digunakan | |
| Daftar topik | `iot/sensor/data`, `iot/aktuator/cmd`, `iot/aktuator/status`, ... |
| Frekuensi publish ESP32 | setiap ___ detik |
| Ukuran payload JSON (bytes) | |
| Koneksi terputus selama praktikum | ☐ Ya ☐ Tidak |

### F.4 Statistik Database

| Informasi | Nilai |
|-----------|-------|
| Nama database | iot_db |
| Nama tabel | sensor_data |
| Jumlah baris data setelah 30 menit | |
| Ukuran tabel (dari DBeaver) | |
| Query `SELECT AVG(temperature)` | °C |
| Query `SELECT MAX(humidity)` | % |
| Query `SELECT MIN(light_percent)` | % |
| Indeks yang dibuat | idx_sensor_device, idx_sensor_recorded |

### F.5 Pengujian REST API (Postman)

| No | Method | Endpoint | Status Code | Response Time | Hasil |
|----|--------|---------|-------------|---------------|-------|
| 1  | GET  | `/api/sensor/latest`   |  | ms | ☐ OK ☐ Error |
| 2  | GET  | `/api/sensor/history`  |  | ms | ☐ OK ☐ Error |
| 3  | POST | `/api/aktuator/command`|  | ms | ☐ OK ☐ Error |

### F.6 Konfigurasi Deployment

| Komponen | Status | URL / Port | Catatan |
|---------|--------|-----------|---------|
| Mosquitto Broker | ☐ Running ☐ Stopped | localhost:1883 | |
| Backend API | ☐ Running ☐ Stopped | localhost:____ | |
| Frontend Dev | ☐ Running ☐ Stopped | localhost:____ | |
| PM2 Process | ☐ Online ☐ Offline | — | |
| ngrok Tunnel | ☐ Aktif ☐ Tidak | https://______.ngrok-free.app | |
| Akses dari HP | ☐ Berhasil ☐ Gagal | — | |

---

## G. PERTANYAAN ANALISIS

1. **Jelaskan** perbedaan antara arsitektur **request/response** (HTTP REST) dan **publish/subscribe** (MQTT). Dalam konteks sistem IoT yang Anda bangun, kapan sebaiknya menggunakan masing-masing pola tersebut?

   **Jawaban:**
   _______________________________________________
   _______________________________________________
   _______________________________________________

2. **Hitunglah** estimasi ukuran data yang dihasilkan sistem IoT ini dalam sehari jika sensor membaca setiap 5 detik dan setiap record berukuran rata-rata 200 byte. Berapa GB data yang akan terakumulasi dalam setahun? Bagaimana strategi pengelolaan data tersebut?

   **Jawaban:**
   _______________________________________________
   _______________________________________________
   _______________________________________________

3. **Analisis** apa yang terjadi pada sistem jika:
   - (a) Mosquitto broker mati sementara ESP32 tetap berjalan
   - (b) Backend mati sementara ESP32 dan broker tetap berjalan
   - (c) ESP32 kehilangan koneksi WiFi

   Tuliskan observasi Anda berdasarkan percobaan atau analisis teoritis!

   **Jawaban:**
   _______________________________________________
   _______________________________________________
   _______________________________________________

4. **Bandingkan** latensi kontrol aktuator dari tabel F.2. Apakah nilai latensi yang Anda ukur sesuai ekspektasi untuk sistem IoT? Faktor apa saja yang mempengaruhi latensi tersebut (WiFi, MQTT QoS, processing backend)?

   **Jawaban:**
   _______________________________________________
   _______________________________________________
   _______________________________________________

5. **Evaluasi** keamanan sistem IoT yang Anda bangun. Identifikasi minimal **3 kerentanan keamanan** yang ada, kemudian jelaskan solusi teknis untuk masing-masing kerentanan tersebut (petunjuk: pertimbangkan autentikasi MQTT, enkripsi TLS, validasi input API, dan keamanan database)!

   **Jawaban:**
   _______________________________________________
   _______________________________________________
   _______________________________________________

---

## H. KESIMPULAN

Tuliskan kesimpulan praktikum dalam 5 poin berdasarkan hasil pengamatan dan analisis:

1. _______________________________________________
   _______________________________________________

2. _______________________________________________
   _______________________________________________

3. _______________________________________________
   _______________________________________________

4. _______________________________________________
   _______________________________________________

5. _______________________________________________
   _______________________________________________

---

## I. LAMPIRAN (Screenshot Wajib)

**SESI 1 – Persiapan Environment:**
- [ ] Screenshot Mosquitto berjalan sebagai service (Services / `systemctl status mosquitto`)
- [ ] Screenshot pengujian `mosquitto_pub` dan `mosquitto_sub` di dua terminal
- [ ] Screenshot MQTT Explorer terhubung ke broker
- [ ] Screenshot PlatformIO project berhasil dibuat (explorer VS Code)
- [ ] Screenshot output `pip list` menampilkan library Python yang terinstal

**SESI 2 – ESP32 dan Python Edge Device:**
- [ ] Screenshot Serial Monitor ESP32 menampilkan data sensor yang dipublish
- [ ] Screenshot MQTT Explorer menampilkan topik `iot/sensor/data` dengan payload JSON
- [ ] Screenshot Python subscriber menerima dan mencetak data sensor
- [ ] Screenshot Python publisher mengirim perintah + ESP32 LED/relay merespons (foto hardware)
- [ ] Screenshot MQTT Explorer menampilkan topik `iot/aktuator/status`

**SESI 3 – Backend dan Frontend:**
- [ ] Screenshot terminal backend berjalan tanpa error
- [ ] Screenshot Postman – `GET /api/sensor/latest` mengembalikan data JSON
- [ ] Screenshot Postman – `POST /api/aktuator/command` berhasil
- [ ] Screenshot DBeaver – tabel `sensor_data` berisi minimal 20 baris data
- [ ] Screenshot dashboard frontend menampilkan data real-time (grafik + nilai sensor)
- [ ] Screenshot tombol kontrol aktuator berhasil mengontrol LED/relay (foto hardware + browser)
- [ ] Screenshot PM2 `pm2 status` menampilkan proses online
- [ ] Screenshot ngrok tunnel aktif + akses dashboard dari perangkat lain (HP/laptop lain)

---

## J. REFERENSI

1. **MQTT Specification v5.0.** OASIS Standard, 2019. https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
2. **Eclipse Mosquitto Documentation.** https://mosquitto.org/documentation
3. **PubSubClient Arduino Library.** Nick O'Leary. https://pubsubclient.knolleary.net
4. **Espressif ESP32 Technical Reference Manual.** https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf
5. **ArduinoJson Documentation.** Benoît Blanchon. https://arduinojson.org/v7
6. **FastAPI Documentation.** Sebastián Ramírez. https://fastapi.tiangolo.com
7. **Express.js Guide.** https://expressjs.com/en/guide/routing.html
8. **Sequelize ORM Documentation.** https://sequelize.org/docs/v6
9. **SQLAlchemy 2.0 Documentation.** https://docs.sqlalchemy.org/en/20
10. **Vue.js 3 Documentation.** https://vuejs.org/guide/introduction.html
11. **Chart.js Documentation.** https://www.chartjs.org/docs/latest
12. **PostgreSQL 16 Documentation.** https://www.postgresql.org/docs/16
13. **PM2 Process Manager Documentation.** https://pm2.keymetrics.io/docs/usage/quick-start
14. **ngrok Documentation.** https://ngrok.com/docs
15. Al-Fuqaha, A., et al. (2015). *Internet of Things: A Survey on Enabling Technologies, Protocols, and Applications*. IEEE Communications Surveys & Tutorials, 17(4), 2347–2376. https://doi.org/10.1109/COMST.2015.2444095

---

*Jobsheet ini merupakan dokumen resmi praktikum. Isi dengan lengkap dan jujur.*  
*Nilai ditentukan berdasarkan kelengkapan jobsheet, kualitas implementasi, dan pemahaman analitis.*

**Tanda Tangan Dosen/Asisten:** ___________________  
**Tanggal:** ___________________
