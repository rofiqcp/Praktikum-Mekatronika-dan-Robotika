# MATERI MODUL 04: IoT WebServer MQTT ESP32

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 04 – IoT WebServer MQTT ESP32  
**Platform:** ESP32, PlatformIO, Python, Node.js, Java Spring Boot  
**Protokol:** MQTT, HTTP, WebSocket  
**Estimasi Waktu Belajar:** 8–12 Jam

---

## DAFTAR ISI

1. [IoT (Internet of Things)](#1-iot-internet-of-things)
2. [Protokol MQTT](#2-protokol-mqtt)
3. [Database untuk IoT](#3-database-untuk-iot)
4. [ESP32 sebagai Edge Device dengan PlatformIO](#4-esp32-sebagai-edge-device-dengan-platformio)
5. [Python sebagai Laptop Edge Device](#5-python-sebagai-laptop-edge-device)
6. [Server Backend](#6-server-backend)
7. [Server Frontend](#7-server-frontend)
8. [Deployment](#8-deployment)
9. [Arsitektur Sistem IoT Lengkap](#9-arsitektur-sistem-iot-lengkap)
10. [Referensi](#10-referensi)

---

## 1. IoT (INTERNET OF THINGS)

### 1.1 Definisi dan Konsep IoT

**Internet of Things (IoT)** adalah konsep di mana perangkat fisik (things) — seperti sensor, aktuator, mesin industri, peralatan rumah tangga — dihubungkan ke internet sehingga dapat mengumpulkan data, berkomunikasi satu sama lain, dan dikendalikan dari jarak jauh tanpa intervensi manusia secara langsung.

Istilah IoT pertama kali dipopulerkan oleh **Kevin Ashton** pada tahun 1999 dalam konteks supply chain management menggunakan RFID. Saat ini, IoT telah berkembang menjadi ekosistem raksasa yang mencakup miliaran perangkat di seluruh dunia.

**Karakteristik utama IoT:**
- **Connectivity** – perangkat selalu terhubung ke jaringan
- **Things** – objek fisik dengan sensor/aktuator
- **Data** – pengumpulan dan pengiriman data secara kontinu
- **Intelligence** – analisis data untuk pengambilan keputusan otomatis
- **Action** – tindakan nyata berdasarkan analisis (otomatisasi)

### 1.2 Arsitektur IoT

Arsitektur IoT modern terdiri dari tiga lapisan utama:

```
┌─────────────────────────────────────────────────────────────┐
│                        CLOUD LAYER                          │
│   Big Data Analytics │ Machine Learning │ Long-term Storage │
│   AWS IoT │ Google Cloud IoT │ Azure IoT Hub │ ThingsBoard   │
├─────────────────────────────────────────────────────────────┤
│                         FOG LAYER                           │
│   Local Server │ Gateway │ Edge Computing Node              │
│   Raspberry Pi │ Industrial PC │ Smart Gateway               │
├─────────────────────────────────────────────────────────────┤
│                        EDGE LAYER                           │
│   Sensor │ Aktuator │ Mikrokontroler │ Embedded Device       │
│   ESP32 │ Arduino │ STM32 │ Raspberry Pi Pico               │
└─────────────────────────────────────────────────────────────┘
```

#### Edge Layer
Lapisan paling bawah, tempat data dihasilkan secara langsung dari dunia fisik.
- **Sensor**: temperatur (DS18B20, DHT22), kelembaban, tekanan, cahaya, akselerometer
- **Aktuator**: relay, motor, solenoid, buzzer, LED
- **Mikrokontroler**: ESP32, ESP8266, STM32, Arduino
- Komputasi terbatas, konsumsi daya rendah, real-time response

#### Fog Layer (Edge Computing)
Lapisan tengah, bertugas memproses data lokal sebelum dikirim ke cloud.
- Mengurangi latensi (tidak harus ke cloud untuk keputusan cepat)
- Filtering dan agregasi data (hanya data penting yang dikirim ke cloud)
- Contoh: Raspberry Pi sebagai gateway MQTT → Database lokal
- **Laptop/PC dengan Python** juga bisa berperan sebagai fog node

#### Cloud Layer
Lapisan tertinggi, tempat penyimpanan jangka panjang dan analisis data skala besar.
- **Storage**: database skala besar (terabyte hingga petabyte)
- **Analytics**: visualisasi dashboard, trend analysis, anomaly detection
- **ML/AI**: prediksi perawatan (predictive maintenance), klasifikasi data
- Platform: AWS IoT Core, Google Cloud IoT, Azure IoT Hub, ThingsBoard

### 1.3 Protokol Komunikasi IoT

| Protokol | Transport | Port | Model | Overhead | Penggunaan |
|----------|-----------|------|-------|----------|------------|
| **MQTT** | TCP | 1883/8883 | Pub/Sub | Sangat rendah | Sensor ke broker, M2M |
| **HTTP/HTTPS** | TCP | 80/443 | Request/Response | Tinggi | REST API, web service |
| **WebSocket** | TCP | 80/443 | Bidirectional | Rendah | Real-time dashboard |
| **CoAP** | UDP | 5683 | Request/Response | Sangat rendah | Constrained devices |
| **AMQP** | TCP | 5672 | Pub/Sub + Queue | Sedang | Enterprise messaging |
| **Zigbee** | RF 2.4GHz | — | Mesh | — | Smart home, low power |
| **LoRaWAN** | RF sub-GHz | — | LPWAN | — | Jarak jauh, low power |

### 1.4 Use Cases IoT Industri

| Industri | Aplikasi | Sensor/Aktuator |
|----------|----------|-----------------|
| **Manufaktur** | Predictive maintenance mesin | Vibration, temperatur, arus listrik |
| **Pertanian** | Smart irrigation, greenhouse | Kelembaban tanah, pH, cahaya |
| **Kesehatan** | Patient monitoring, wearables | Detak jantung, SpO2, suhu tubuh |
| **Smart City** | Lampu jalan otomatis, parkir | LDR, ultrasonic, RFID |
| **Logistik** | Tracking aset, cold chain | GPS, RFID, temperatur |
| **Energi** | Smart grid, pemantauan panel surya | Arus, tegangan, daya |
| **Rumah** | Smart home, keamanan | PIR, kamera, kontrol daya |

> **💡 Catatan:** Dalam praktikum ini, kita akan membangun sistem IoT skala kecil dengan ESP32 sebagai edge device, MQTT sebagai protokol, dan web server sebagai fog/cloud layer.

---

## 2. PROTOKOL MQTT

### 2.1 Konsep Publish/Subscribe

MQTT (Message Queuing Telemetry Transport) menggunakan model **Publish/Subscribe (Pub/Sub)** yang berbeda dengan HTTP (request/response).

```
      PUBLISHER                 BROKER                SUBSCRIBER
   ┌───────────┐    publish    ┌─────────┐  deliver   ┌───────────┐
   │  ESP32    │──────────────►│ Mosquitto│───────────►│  Python   │
   │ (sensor)  │  topic: /suhu │         │ topic: /suhu│  (server) │
   └───────────┘               │         │             └───────────┘
                                │         │             ┌───────────┐
   ┌───────────┐    publish    │         │  deliver   │ Dashboard │
   │  ESP32 #2 │──────────────►│         │───────────►│  (React)  │
   │ (sensor)  │  topic: /suhu │         │ topic: /suhu└───────────┘
   └───────────┘               └─────────┘
```

**Keunggulan Pub/Sub dibanding Request/Response:**
- Publisher tidak perlu tahu siapa subscriber-nya
- Subscriber bisa berlangganan kapan saja tanpa mengganggu publisher
- Satu pesan bisa diterima banyak subscriber sekaligus (fan-out)
- Decoupling antara producer dan consumer data

### 2.2 Komponen MQTT

#### Broker
Server pusat yang menerima semua pesan dari publisher dan mendistribusikannya ke subscriber yang relevan.
- **Mosquitto**: open-source, ringan, paling populer untuk embedded/IoT
- **EMQ X (EMQX)**: high-performance, cocok untuk jutaan koneksi
- **HiveMQ**: enterprise, cloud-native
- **AWS IoT Core**: managed cloud broker dari Amazon
- **Adafruit IO**: cloud broker dengan dashboard gratis

#### Publisher
Perangkat atau aplikasi yang mengirim (mempublikasikan) pesan ke broker melalui sebuah **topic**.
- Contoh: ESP32 mengirim data suhu setiap 5 detik ke topic `sensor/ruang1/suhu`

#### Subscriber
Perangkat atau aplikasi yang berlangganan (subscribe) ke topic tertentu dan akan menerima pesan setiap kali ada publisher yang mengirim ke topic tersebut.
- Contoh: Python server berlangganan `sensor/#` untuk menerima semua data sensor

### 2.3 Topics

Topic adalah string hierarkis yang digunakan sebagai alamat pesan, mirip dengan path URL.

```
sensor/ruang1/suhu
sensor/ruang1/kelembaban
sensor/ruang2/suhu
aktuator/ruang1/kipas
aktuator/ruang1/ac
```

**Wildcard dalam subscription:**
- `+` : menggantikan satu level. Contoh: `sensor/+/suhu` → cocok dengan `sensor/ruang1/suhu`, `sensor/ruang2/suhu`
- `#` : menggantikan satu atau lebih level (harus di akhir). Contoh: `sensor/#` → cocok dengan semua topic yang dimulai `sensor/`

> **⚠️ Perhatian:** Topic bersifat case-sensitive. `Sensor/Suhu` ≠ `sensor/suhu`

### 2.4 QoS (Quality of Service)

MQTT mendefinisikan tiga level QoS untuk menjamin pengiriman pesan:

| QoS | Nama | Jaminan | Cara Kerja |
|-----|------|---------|------------|
| **0** | At most once | Pesan mungkin hilang | Fire and forget, tidak ada acknowledgment |
| **1** | At least once | Pesan pasti sampai, mungkin duplikat | Publisher simpan pesan sampai dapat PUBACK dari broker |
| **2** | Exactly once | Pesan sampai tepat satu kali | Handshake 4 tahap (PUBLISH → PUBREC → PUBREL → PUBCOMP) |

**Kapan menggunakan masing-masing:**
- **QoS 0**: Data sensor periodik yang tidak kritis (suhu ruangan, update posisi)
- **QoS 1**: Perintah kontrol (nyalakan kipas) — lebih aman jika ada duplikat
- **QoS 2**: Transaksi kritis (pembayaran, perintah keselamatan industri)

### 2.5 Retain Messages

Ketika pesan dikirim dengan flag `retain = true`, broker akan menyimpan pesan terakhir untuk topic tersebut. Subscriber baru yang berlangganan topic itu akan langsung menerima pesan tersimpan tanpa harus menunggu publisher mengirim ulang.

```python
# Publisher mengirim dengan retain
client.publish("sensor/suhu", "28.5", retain=True)

# Subscriber baru langsung dapat nilai terakhir saat connect
```

**Penggunaan umum:** Status ON/OFF perangkat, konfigurasi terakhir, nilai sensor yang jarang berubah.

### 2.6 Last Will and Testament (LWT)

LWT adalah pesan yang sudah disiapkan sebelumnya, yang akan dikirim broker secara otomatis jika klien tiba-tiba terputus (disconnect tidak normal / koneksi putus).

```python
# Disiapkan saat connect
client.will_set("perangkat/esp32-1/status", "offline", qos=1, retain=True)
client.connect(broker_address)

# Jika ESP32 putus mendadak, broker otomatis publish:
# topic: perangkat/esp32-1/status
# payload: "offline"
```

**Penggunaan:** Monitoring status perangkat IoT, deteksi perangkat offline.

### 2.7 Setup Mosquitto Broker

#### Instalasi di Linux/Ubuntu:
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients -y

# Aktifkan dan jalankan service
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Cek status
sudo systemctl status mosquitto
```

#### Konfigurasi Mosquitto (`/etc/mosquitto/mosquitto.conf`):
```conf
# Listener default
listener 1883
allow_anonymous true

# Untuk keamanan (produksi), gunakan autentikasi:
# listener 1883
# allow_anonymous false
# password_file /etc/mosquitto/passwd
```

#### Membuat user dan password:
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd username
sudo systemctl restart mosquitto
```

#### Uji dengan mosquitto_clients:
```bash
# Terminal 1 - Subscribe
mosquitto_sub -h localhost -t "sensor/#" -v

# Terminal 2 - Publish
mosquitto_pub -h localhost -t "sensor/suhu" -m "28.5"
```

### 2.8 MQTT vs HTTP

| Aspek | MQTT | HTTP |
|-------|------|------|
| **Model** | Pub/Sub | Request/Response |
| **Overhead header** | 2 byte minimum | Ratusan byte |
| **Koneksi** | Persistent (TCP keep-alive) | Baru setiap request |
| **Real-time** | Ya (push dari broker) | Butuh polling |
| **Cocok untuk** | IoT sensor, M2M, low bandwidth | REST API, web browser |
| **Keamanan** | TLS (port 8883) | TLS (HTTPS, port 443) |
| **Bandwidth** | Sangat efisien | Kurang efisien |

---

## 3. DATABASE UNTUK IoT

### 3.1 Perbandingan Database IoT

| Database | Tipe | Kekuatan | Kelemahan | Cocok untuk |
|----------|------|----------|-----------|-------------|
| **PostgreSQL** | Relasional | ACID, query kompleks, ekstensi kuat | Setup lebih kompleks | Backend enterprise, data terstruktur |
| **MySQL/MariaDB** | Relasional | Populer, banyak dokumentasi | Fitur lebih terbatas dari Postgres | Web app umum, CMS |
| **MongoDB** | NoSQL Document | Skema fleksibel, scale horizontal | Konsistensi lebih lemah | Data tidak terstruktur, JSON |
| **Redis** | In-Memory K/V | Ultra cepat, pub/sub built-in | Data hilang jika restart (tanpa persistence) | Cache, session, real-time counter |
| **InfluxDB** | Time-Series | Optimal untuk data berkala, retention policy | Kurang cocok untuk relational query | Data sensor IoT, monitoring |
| **SQLite** | Relasional Embedded | Zero setup, single file, portabel | Tidak untuk concurrent write | Edge device, prototype, mobile |
| **TimescaleDB** | Time-Series (PostgreSQL) | Gabungan kekuatan Postgres + time-series | Butuh PostgreSQL | IoT skala besar dengan query kompleks |

### 3.2 PostgreSQL

PostgreSQL adalah sistem database relasional paling canggih yang bersifat open-source. Sangat cocok untuk data IoT yang terstruktur dan membutuhkan query analitik kompleks.

```sql
-- Buat database dan tabel untuk data sensor
CREATE DATABASE iot_db;

CREATE TABLE sensor_data (
    id          BIGSERIAL PRIMARY KEY,
    device_id   VARCHAR(50) NOT NULL,
    topic       VARCHAR(100),
    suhu        DECIMAL(5,2),
    kelembaban  DECIMAL(5,2),
    timestamp   TIMESTAMPTZ DEFAULT NOW()
);

-- Index untuk query berdasarkan waktu dan device
CREATE INDEX idx_sensor_timestamp ON sensor_data(timestamp DESC);
CREATE INDEX idx_sensor_device ON sensor_data(device_id);

-- Query data 1 jam terakhir per device
SELECT device_id, AVG(suhu), AVG(kelembaban)
FROM sensor_data
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY device_id;
```

**Instalasi di Ubuntu:**
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo -u postgres psql -c "CREATE USER iotuser WITH PASSWORD 'iotpass';"
sudo -u postgres psql -c "CREATE DATABASE iot_db OWNER iotuser;"
```

### 3.3 InfluxDB (Rekomendasi untuk Time-Series IoT)

InfluxDB adalah database yang didesain khusus untuk data time-series — data yang memiliki timestamp dan terus bertambah secara berkala, seperti data sensor IoT.

```bash
# Instalasi InfluxDB v2
curl -s https://repos.influxdata.com/influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdb.gpg
echo "deb [signed-by=/etc/apt/trusted.gpg.d/influxdb.gpg] https://repos.influxdata.com/debian stable main" | sudo tee /etc/apt/sources.list.d/influxdb.list
sudo apt update && sudo apt install influxdb2 -y
sudo systemctl start influxdb
```

```python
# Python client untuk InfluxDB
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

client = InfluxDBClient(url="http://localhost:8086", token="my-token", org="my-org")
write_api = client.write_api(write_options=SYNCHRONOUS)

# Menulis data sensor
point = Point("sensor_data") \
    .tag("device_id", "esp32-1") \
    .tag("lokasi", "ruang-server") \
    .field("suhu", 28.5) \
    .field("kelembaban", 65.0) \
    .time(datetime.utcnow())

write_api.write(bucket="iot-bucket", record=point)
```

### 3.4 Redis untuk Caching dan Pub/Sub

Redis sangat berguna dalam sistem IoT untuk:
1. **Cache** nilai sensor terbaru (tanpa query database)
2. **Pub/Sub** internal antar microservice
3. **Rate limiting** dan session management

```python
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Simpan data sensor terbaru (TTL 60 detik)
data = {"suhu": 28.5, "kelembaban": 65, "timestamp": "2024-01-01T10:00:00"}
r.setex("sensor:esp32-1:latest", 60, json.dumps(data))

# Baca data terbaru (sangat cepat, dari memory)
latest = json.loads(r.get("sensor:esp32-1:latest"))
print(latest["suhu"])

# Pub/Sub internal
pubsub = r.pubsub()
pubsub.subscribe("sensor_updates")
```

### 3.5 SQLite untuk Edge Device

SQLite cocok digunakan di edge device (Raspberry Pi, laptop lokal) karena tidak memerlukan server terpisah.

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect("sensor_data.db")
cursor = conn.cursor()

# Buat tabel
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT NOT NULL,
        suhu      REAL,
        kelembaban REAL,
        timestamp TEXT DEFAULT (datetime('now'))
    )
""")

# Simpan data
cursor.execute(
    "INSERT INTO sensor_data (device_id, suhu, kelembaban) VALUES (?, ?, ?)",
    ("esp32-1", 28.5, 65.0)
)
conn.commit()

# Query data
rows = cursor.execute(
    "SELECT * FROM sensor_data WHERE device_id=? ORDER BY timestamp DESC LIMIT 10",
    ("esp32-1",)
).fetchall()
conn.close()
```

---

## 4. ESP32 SEBAGAI EDGE DEVICE DENGAN PLATFORMIO

### 4.1 Spesifikasi ESP32

| Komponen | Spesifikasi |
|----------|-------------|
| **CPU** | Xtensa LX6 dual-core 32-bit, 240 MHz |
| **RAM** | 520 KB SRAM |
| **Flash** | 4 MB (default) hingga 16 MB |
| **WiFi** | 802.11 b/g/n 2.4 GHz |
| **Bluetooth** | BT Classic + BLE 4.2 |
| **GPIO** | 34 pin (beberapa hanya input) |
| **ADC** | 12-bit, 18 channel |
| **DAC** | 8-bit, 2 channel |
| **PWM** | 16 channel independent |
| **I2C/SPI/UART** | Multiple interface |
| **Konsumsi daya** | 240 mA (aktif WiFi) / ~10 µA (deep sleep) |
| **Tegangan** | 3.3V logic, 5V power via USB |

### 4.2 PlatformIO

PlatformIO adalah IDE dan build system modern untuk pengembangan embedded/IoT yang mendukung 1000+ board dan 40+ platform.

**Keunggulan PlatformIO dibanding Arduino IDE:**
- Manajemen library otomatis (seperti npm/pip)
- Mendukung VS Code sebagai editor
- Build system lebih cepat
- Mendukung multiple framework (Arduino, ESP-IDF, Zephyr, dll.)
- Unit testing dan static analysis

#### Instalasi PlatformIO:
```bash
# 1. Install VS Code terlebih dahulu dari https://code.visualstudio.com

# 2. Install ekstensi PlatformIO di VS Code:
#    Extensions → cari "PlatformIO IDE" → Install

# 3. Atau install PlatformIO CLI:
pip install platformio
```

#### Struktur Project PlatformIO:
```
my_iot_project/
├── platformio.ini          ← Konfigurasi project
├── src/
│   └── main.cpp            ← Kode utama
├── include/
│   └── config.h            ← Header / konstanta
├── lib/
│   └── (library lokal)
└── test/
    └── (unit tests)
```

#### File `platformio.ini`:
```ini
[env:esp32dev]
platform  = espressif32
board     = esp32dev
framework = arduino

; Library yang dibutuhkan
lib_deps =
    knolleary/PubSubClient @ ^2.8
    bblanchon/ArduinoJson @ ^6.21.0
    adafruit/DHT sensor library @ ^1.4.4

; Kecepatan serial monitor
monitor_speed = 115200

; Upload speed
upload_speed = 921600

; Konfigurasi partisi untuk OTA
board_build.partitions = min_spiffs.csv
```

### 4.3 Library ESP32 Penting

| Library | Fungsi | Sumber |
|---------|--------|--------|
| `WiFi.h` | Koneksi WiFi (built-in Arduino framework) | Built-in |
| `PubSubClient` | MQTT client | knolleary/PubSubClient |
| `ArduinoJson` | Parse dan buat JSON | bblanchon/ArduinoJson |
| `DHT` | Sensor DHT11/DHT22 | adafruit/DHT sensor library |
| `OneWire` + `DallasTemperature` | Sensor DS18B20 | milesburton/DallasTemperature |
| `HTTPClient` | HTTP request ke REST API | Built-in |
| `WebServer` | HTTP server di ESP32 | Built-in |
| `ArduinoOTA` | Over-The-Air update | Built-in |
| `ESP32Servo` | Kontrol servo | madhephaestus/ESP32Servo |

### 4.4 Contoh Kode: ESP32 Publisher MQTT

```cpp
// src/main.cpp - ESP32 MQTT Publisher dengan DHT22
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ─── Konfigurasi WiFi & MQTT ───────────────────────────────
const char* WIFI_SSID     = "NamaWiFi";
const char* WIFI_PASSWORD = "PasswordWiFi";
const char* MQTT_BROKER   = "192.168.1.100";   // IP server/laptop
const int   MQTT_PORT     = 1883;
const char* MQTT_CLIENT_ID = "esp32-sensor-01";

// ─── Konfigurasi Sensor ────────────────────────────────────
#define DHT_PIN  4
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

// ─── Topics MQTT ──────────────────────────────────────────
const char* TOPIC_SENSOR  = "sensor/ruang1/data";
const char* TOPIC_STATUS  = "perangkat/esp32-1/status";

// ─── Interval pengiriman (ms) ─────────────────────────────
const unsigned long PUBLISH_INTERVAL = 5000;
unsigned long lastPublish = 0;

WiFiClient   espClient;
PubSubClient mqttClient(espClient);

// ─── Callback: pesan masuk dari broker ────────────────────
void onMessageReceived(char* topic, byte* payload, unsigned int length) {
    String msg = "";
    for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
    Serial.printf("[MQTT] Topic: %s  |  Pesan: %s\n", topic, msg.c_str());
}

// ─── Fungsi koneksi WiFi ──────────────────────────────────
void connectWiFi() {
    Serial.print("Menghubungkan ke WiFi");
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.printf("\nWiFi terhubung! IP: %s\n", WiFi.localIP().toString().c_str());
}

// ─── Fungsi koneksi MQTT ──────────────────────────────────
void connectMQTT() {
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    mqttClient.setCallback(onMessageReceived);

    while (!mqttClient.connected()) {
        Serial.print("Menghubungkan ke MQTT broker...");
        // LWT: jika putus mendadak, broker publish "offline"
        if (mqttClient.connect(MQTT_CLIENT_ID, nullptr, nullptr,
                               TOPIC_STATUS, 1, true, "offline")) {
            Serial.println(" terhubung!");
            // Publish status online dengan retain
            mqttClient.publish(TOPIC_STATUS, "online", true);
            // Subscribe ke topic perintah
            mqttClient.subscribe("perintah/ruang1/#");
        } else {
            Serial.printf(" gagal (rc=%d), coba lagi 5s\n", mqttClient.state());
            delay(5000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    dht.begin();
    connectWiFi();
    connectMQTT();
}

void loop() {
    // Pastikan MQTT tetap terhubung
    if (!mqttClient.connected()) connectMQTT();
    mqttClient.loop();

    // Kirim data setiap PUBLISH_INTERVAL ms
    if (millis() - lastPublish >= PUBLISH_INTERVAL) {
        lastPublish = millis();

        float suhu = dht.readTemperature();
        float hum  = dht.readHumidity();

        if (isnan(suhu) || isnan(hum)) {
            Serial.println("Gagal baca DHT22!");
            return;
        }

        // Buat JSON payload
        StaticJsonDocument<128> doc;
        doc["device_id"]  = MQTT_CLIENT_ID;
        doc["suhu"]       = round(suhu * 10) / 10.0;
        doc["kelembaban"] = round(hum  * 10) / 10.0;
        doc["uptime_ms"]  = millis();

        char payload[128];
        serializeJson(doc, payload);

        mqttClient.publish(TOPIC_SENSOR, payload, false); // QoS 0
        Serial.printf("[Publish] %s → %s\n", TOPIC_SENSOR, payload);
    }
}
```

### 4.5 Contoh Kode: ESP32 Subscriber MQTT (Kontrol Relay)

```cpp
// src/main.cpp - ESP32 MQTT Subscriber untuk kontrol relay
#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID      = "NamaWiFi";
const char* WIFI_PASSWORD  = "PasswordWiFi";
const char* MQTT_BROKER    = "192.168.1.100";
const char* MQTT_CLIENT_ID = "esp32-relay-01";

#define RELAY_PIN  26

WiFiClient   espClient;
PubSubClient mqttClient(espClient);

void onMessageReceived(char* topic, byte* payload, unsigned int length) {
    String msg = "";
    for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];

    Serial.printf("[MQTT RX] %s : %s\n", topic, msg.c_str());

    // Parse JSON perintah
    StaticJsonDocument<64> doc;
    if (deserializeJson(doc, msg) == DeserializationError::Ok) {
        bool state = doc["relay"];
        digitalWrite(RELAY_PIN, state ? HIGH : LOW);
        Serial.printf("Relay → %s\n", state ? "ON" : "OFF");
    }
}

void connectWiFi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) delay(500);
    Serial.printf("WiFi OK: %s\n", WiFi.localIP().toString().c_str());
}

void connectMQTT() {
    mqttClient.setServer(MQTT_BROKER, 1883);
    mqttClient.setCallback(onMessageReceived);
    while (!mqttClient.connected()) {
        if (mqttClient.connect(MQTT_CLIENT_ID)) {
            mqttClient.subscribe("perintah/relay/#", 1); // QoS 1
            Serial.println("MQTT terhubung & subscribe berhasil");
        } else {
            delay(3000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);
    connectWiFi();
    connectMQTT();
}

void loop() {
    if (!mqttClient.connected()) connectMQTT();
    mqttClient.loop();
}
```

### 4.6 OTA (Over-The-Air) Update

OTA memungkinkan upload firmware baru ke ESP32 melalui WiFi tanpa kabel USB.

```cpp
#include <ArduinoOTA.h>

void setupOTA() {
    ArduinoOTA.setHostname("esp32-sensor-01");
    ArduinoOTA.setPassword("ota_password_rahasia");

    ArduinoOTA.onStart([]() { Serial.println("OTA: Mulai update..."); });
    ArduinoOTA.onEnd([]()   { Serial.println("\nOTA: Selesai!"); });
    ArduinoOTA.onError([](ota_error_t error) {
        Serial.printf("OTA Error[%u]\n", error);
    });

    ArduinoOTA.begin();
    Serial.println("OTA siap");
}

void loop() {
    ArduinoOTA.handle(); // Harus dipanggil di setiap loop
    // ... kode lainnya
}
```

### 4.7 Deep Sleep untuk Hemat Daya

```cpp
#define SLEEP_DURATION_US (60 * 1000000ULL) // 60 detik

void setup() {
    Serial.begin(115200);
    // Baca sensor, kirim data MQTT
    // ...

    // Tidur selama 60 detik
    Serial.println("Masuk deep sleep...");
    esp_sleep_enable_timer_wakeup(SLEEP_DURATION_US);
    esp_deep_sleep_start();
}

void loop() {
    // Tidak pernah dieksekusi saat deep sleep aktif
}
```

---

## 5. PYTHON SEBAGAI LAPTOP EDGE DEVICE

### 5.1 Paho MQTT Library

```bash
pip install paho-mqtt
```

### 5.2 Python MQTT Subscriber Lengkap

```python
# mqtt_subscriber.py - Python menerima data dari ESP32
import paho.mqtt.client as mqtt
import json
import sqlite3
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC_SUBSCRIBE = "sensor/#"

# ─── Inisialisasi database SQLite ────────────────────────────
def init_db():
    conn = sqlite3.connect("iot_data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id  TEXT,
            topic      TEXT,
            suhu       REAL,
            kelembaban REAL,
            timestamp  TEXT
        )
    """)
    conn.commit()
    return conn

db_conn = init_db()

# ─── Callback saat terhubung ke broker ───────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Terhubung ke broker {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC_SUBSCRIBE, qos=1)
        print(f"[MQTT] Subscribe ke: {TOPIC_SUBSCRIBE}")
    else:
        print(f"[MQTT] Gagal terhubung, kode: {rc}")

# ─── Callback saat pesan diterima ────────────────────────────
def on_message(client, userdata, msg):
    topic   = msg.topic
    payload = msg.payload.decode("utf-8")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {topic}: {payload}")

    try:
        data = json.loads(payload)
        # Proses dan simpan ke database
        db_conn.execute(
            "INSERT INTO sensor_data (device_id, topic, suhu, kelembaban, timestamp) VALUES (?,?,?,?,?)",
            (
                data.get("device_id", "unknown"),
                topic,
                data.get("suhu"),
                data.get("kelembaban"),
                datetime.now().isoformat()
            )
        )
        db_conn.commit()

        # Trigger alert jika suhu terlalu tinggi
        if data.get("suhu", 0) > 35:
            print(f"⚠️  PERINGATAN: Suhu tinggi {data['suhu']}°C dari {data.get('device_id')}")
            client.publish(f"alert/{data.get('device_id')}", 
                           json.dumps({"level": "warning", "message": "Suhu tinggi!"}))

    except json.JSONDecodeError:
        print(f"[ERROR] Payload bukan JSON valid: {payload}")

# ─── Setup MQTT client ────────────────────────────────────────
client = mqtt.Client(client_id="python-edge-processor")
client.on_connect = on_connect
client.on_message = on_message

# LWT untuk Python client
client.will_set("perangkat/python-edge/status", "offline", qos=1, retain=True)
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

client.publish("perangkat/python-edge/status", "online", qos=1, retain=True)

print("Python MQTT Edge Processor berjalan... (Ctrl+C untuk berhenti)")
client.loop_forever()
```

### 5.3 Python MQTT Publisher

```python
# mqtt_publisher.py - Python mengirim perintah ke ESP32
import paho.mqtt.client as mqtt
import json
import time

client = mqtt.Client(client_id="python-commander")
client.connect("localhost", 1883)
client.loop_start()

# Kirim perintah nyalakan relay
perintah = {"relay": True, "timestamp": time.time()}
client.publish("perintah/relay/ruang1", json.dumps(perintah), qos=1)
print("Perintah relay ON dikirim")

time.sleep(5)

# Matikan relay
perintah["relay"] = False
client.publish("perintah/relay/ruang1", json.dumps(perintah), qos=1)
print("Perintah relay OFF dikirim")

client.loop_stop()
client.disconnect()
```

### 5.4 Data Processing dan Filtering di Python

```python
# data_processor.py - Agregasi dan filtering data sensor
import json
import statistics
from collections import deque

class SensorDataProcessor:
    def __init__(self, window_size=10):
        self.buffers = {}  # device_id -> deque
        self.window  = window_size

    def add_data(self, device_id: str, suhu: float, kelembaban: float):
        if device_id not in self.buffers:
            self.buffers[device_id] = {"suhu": deque(maxlen=self.window),
                                        "kelembaban": deque(maxlen=self.window)}
        self.buffers[device_id]["suhu"].append(suhu)
        self.buffers[device_id]["kelembaban"].append(kelembaban)

    def get_stats(self, device_id: str) -> dict:
        if device_id not in self.buffers:
            return {}
        s = list(self.buffers[device_id]["suhu"])
        h = list(self.buffers[device_id]["kelembaban"])
        return {
            "suhu_avg":    round(statistics.mean(s), 2),
            "suhu_min":    min(s),
            "suhu_max":    max(s),
            "suhu_stdev":  round(statistics.stdev(s), 2) if len(s) > 1 else 0,
            "hum_avg":     round(statistics.mean(h), 2),
            "sample_count": len(s)
        }

    def is_anomaly(self, device_id: str, suhu: float) -> bool:
        """Deteksi anomali sederhana menggunakan z-score"""
        if device_id not in self.buffers:
            return False
        s = list(self.buffers[device_id]["suhu"])
        if len(s) < 3:
            return False
        mean   = statistics.mean(s)
        stdev  = statistics.stdev(s)
        z_score = abs((suhu - mean) / stdev) if stdev > 0 else 0
        return z_score > 2.5  # anomali jika > 2.5 standar deviasi

processor = SensorDataProcessor(window_size=20)
```

### 5.5 Python Serial Communication

```python
# serial_reader.py - Baca data dari ESP32 via USB Serial
import serial
import json
import paho.mqtt.client as mqtt

SERIAL_PORT  = "/dev/ttyUSB0"   # Linux; Windows: "COM3"
BAUD_RATE    = 115200

mqtt_client = mqtt.Client("serial-bridge")
mqtt_client.connect("localhost", 1883)
mqtt_client.loop_start()

with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    print(f"Membaca serial dari {SERIAL_PORT}...")
    while True:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line:
            try:
                data = json.loads(line)
                # Forward ke MQTT
                mqtt_client.publish("sensor/serial/data", json.dumps(data))
                print(f"Serial → MQTT: {data}")
            except json.JSONDecodeError:
                print(f"Serial (raw): {line}")
```

---

## 6. SERVER BACKEND

### 6.1 Java Spring Boot

Spring Boot adalah framework Java paling populer untuk membangun REST API dan backend enterprise.

**Buat project baru:**
```bash
# Dengan Spring Initializr CLI atau kunjungi https://start.spring.io
curl https://start.spring.io/starter.zip \
  -d dependencies=web,data-jpa,postgresql \
  -d name=iot-server \
  -d artifactId=iot-server \
  -o iot-server.zip
unzip iot-server.zip
```

**`src/main/java/com/iot/server/SensorData.java`:**
```java
@Entity
@Table(name = "sensor_data")
public class SensorData {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "device_id")
    private String deviceId;

    private Double suhu;
    private Double kelembaban;

    @Column(name = "timestamp")
    private LocalDateTime timestamp = LocalDateTime.now();

    // Getters & Setters
}
```

**`SensorRepository.java`:**
```java
@Repository
public interface SensorRepository extends JpaRepository<SensorData, Long> {
    Optional<SensorData> findFirstByDeviceIdOrderByTimestampDesc(String deviceId);

    @Query("SELECT AVG(s.suhu) FROM SensorData s WHERE s.deviceId = :deviceId")
    Double findAvgSuhuByDeviceId(@Param("deviceId") String deviceId);
}
```

**`SensorController.java`:**
```java
@RestController
@RequestMapping("/api/sensor")
@CrossOrigin(origins = "*")
public class SensorController {

    @Autowired
    private SensorRepository sensorRepository;

    @GetMapping
    public List<SensorData> getAllData() {
        return sensorRepository.findAll(Sort.by("timestamp").descending());
    }

    @GetMapping("/latest/{deviceId}")
    public ResponseEntity<SensorData> getLatest(@PathVariable String deviceId) {
        return sensorRepository.findFirstByDeviceIdOrderByTimestampDesc(deviceId)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public SensorData saveData(@RequestBody SensorData data) {
        return sensorRepository.save(data);
    }

    @GetMapping("/stats/{deviceId}")
    public Map<String, Object> getStats(@PathVariable String deviceId) {
        // Implementasi statistik
        return Map.of(
            "device_id", deviceId,
            "avg_suhu",  sensorRepository.findAvgSuhuByDeviceId(deviceId)
        );
    }
}
```

**`application.properties`:**
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/iot_db
spring.datasource.username=iotuser
spring.datasource.password=iotpass
spring.jpa.hibernate.ddl-auto=update
server.port=8080
```

### 6.2 Python FastAPI

FastAPI adalah framework Python modern yang cepat, async-native, dan menghasilkan dokumentasi API otomatis (Swagger UI).

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary paho-mqtt
```

```python
# main.py - FastAPI IoT Server
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3

app = FastAPI(title="IoT API Server", version="1.0.0")

# CORS untuk akses dari frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Model data ───────────────────────────────────────────
class SensorData(BaseModel):
    device_id: str
    suhu: Optional[float] = None
    kelembaban: Optional[float] = None
    timestamp: Optional[datetime] = None

class SensorDataResponse(SensorData):
    id: int

# ─── Database helper ──────────────────────────────────────
def get_db():
    conn = sqlite3.connect("iot_data.db")
    conn.row_factory = sqlite3.Row
    return conn

# ─── Endpoints ────────────────────────────────────────────
@app.get("/api/sensor", response_model=List[SensorDataResponse])
def get_all_sensor_data(limit: int = 100):
    """Ambil semua data sensor, terbaru di atas"""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(row) for row in rows]

@app.get("/api/sensor/{device_id}/latest")
def get_latest(device_id: str):
    """Ambil data terbaru dari device tertentu"""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM sensor_data WHERE device_id=? ORDER BY timestamp DESC LIMIT 1",
        (device_id,)
    ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Device tidak ditemukan")
    return dict(row)

@app.post("/api/sensor", status_code=201)
def create_sensor_data(data: SensorData):
    """Simpan data sensor baru"""
    conn = get_db()
    conn.execute(
        "INSERT INTO sensor_data (device_id, suhu, kelembaban, timestamp) VALUES (?,?,?,?)",
        (data.device_id, data.suhu, data.kelembaban, datetime.now().isoformat())
    )
    conn.commit()
    return {"message": "Data tersimpan", "device_id": data.device_id}

@app.get("/api/sensor/{device_id}/stats")
def get_stats(device_id: str):
    """Statistik data sensor"""
    conn = get_db()
    row = conn.execute("""
        SELECT COUNT(*) as total,
               AVG(suhu) as avg_suhu, MIN(suhu) as min_suhu, MAX(suhu) as max_suhu,
               AVG(kelembaban) as avg_kelembaban
        FROM sensor_data WHERE device_id=?
    """, (device_id,)).fetchone()
    return dict(row)
```

```bash
# Jalankan server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# Dokumentasi otomatis: http://localhost:8000/docs
```

### 6.3 Node.js / Express

```bash
npm init -y
npm install express cors mqtt sqlite3 body-parser
```

```javascript
// server.js - Node.js Express IoT Server
const express = require('express');
const cors    = require('cors');
const mqtt    = require('mqtt');
const sqlite3 = require('sqlite3').verbose();

const app  = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// ─── Database ─────────────────────────────────────────────
const db = new sqlite3.Database('./iot_data.db');
db.run(`CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT, suhu REAL, kelembaban REAL,
    timestamp TEXT DEFAULT (datetime('now'))
)`);

// ─── MQTT Client ──────────────────────────────────────────
const mqttClient = mqtt.connect('mqtt://localhost:1883');
mqttClient.on('connect', () => {
    console.log('MQTT terhubung');
    mqttClient.subscribe('sensor/#');
});
mqttClient.on('message', (topic, payload) => {
    try {
        const data = JSON.parse(payload.toString());
        db.run(
            'INSERT INTO sensor_data (device_id, suhu, kelembaban) VALUES (?,?,?)',
            [data.device_id, data.suhu, data.kelembaban]
        );
        console.log(`[MQTT] ${topic}: ${payload.toString()}`);
    } catch (e) { /* abaikan pesan non-JSON */ }
});

// ─── REST API ─────────────────────────────────────────────
app.get('/api/sensor', (req, res) => {
    const limit = parseInt(req.query.limit) || 100;
    db.all('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT ?',
           [limit], (err, rows) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json(rows);
    });
});

app.post('/api/perintah/relay', (req, res) => {
    const { device_id, relay } = req.body;
    const perintah = JSON.stringify({ relay, timestamp: Date.now() });
    mqttClient.publish(`perintah/relay/${device_id}`, perintah, { qos: 1 });
    res.json({ message: 'Perintah dikirim', relay });
});

app.listen(PORT, () => console.log(`Server berjalan di http://localhost:${PORT}`));
```

### 6.4 Perbandingan Backend

| Aspek | Java Spring Boot | Python FastAPI | Node.js/Express |
|-------|-----------------|----------------|-----------------|
| **Performa** | Tinggi | Tinggi (async) | Tinggi (async) |
| **Kemudahan** | Sedang (verbose) | Mudah | Mudah |
| **Ekosistem** | Enterprise, kuat | Ilmiah, ML | Web, real-time |
| **Startup time** | Lambat (JVM) | Cepat | Cepat |
| **Tipe data** | Statis (Java) | Dinamis + Pydantic | Dinamis |
| **Dokumentasi API** | Springdoc | Otomatis (Swagger) | Manual / Swagger |
| **Cocok untuk** | Enterprise, skala besar | Prototype, ML pipeline | Real-time, WebSocket |

### 6.5 WebSocket untuk Real-Time

```python
# websocket_server.py - FastAPI WebSocket
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        for conn in self.active:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/sensor")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

---

## 7. SERVER FRONTEND

### 7.1 Vue.js + Vite

Vue.js adalah framework JavaScript progresif yang ringan dengan Composition API (Vue 3).

```bash
# Buat project Vue 3 + Vite
npm create vite@latest iot-dashboard -- --template vue
cd iot-dashboard
npm install
npm install axios pinia chart.js vue-chartjs mqtt
npm run dev
```

**Struktur project Vue:**
```
iot-dashboard/
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── components/
│   │   ├── SensorCard.vue
│   │   ├── TemperatureChart.vue
│   │   └── DeviceStatus.vue
│   ├── stores/
│   │   └── sensorStore.js     ← Pinia store
│   └── views/
│       └── Dashboard.vue
├── package.json
└── vite.config.js
```

**`src/stores/sensorStore.js`:**
```javascript
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSensorStore = defineStore('sensor', {
  state: () => ({
    sensorData: [],
    latestValues: {},
    isLoading: false
  }),

  getters: {
    getLatestByDevice: (state) => (deviceId) =>
      state.latestValues[deviceId] || null
  },

  actions: {
    async fetchData(limit = 50) {
      this.isLoading = true
      try {
        const res = await axios.get(`http://localhost:8000/api/sensor?limit=${limit}`)
        this.sensorData = res.data
      } finally {
        this.isLoading = false
      }
    },

    updateFromMQTT(deviceId, data) {
      this.latestValues[deviceId] = data
      this.sensorData.unshift({ ...data, device_id: deviceId })
      if (this.sensorData.length > 200) this.sensorData.pop()
    }
  }
})
```

**`src/components/TemperatureChart.vue`:**
```vue
<template>
  <div class="chart-container">
    <h3>📈 Grafik Suhu Real-Time</h3>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, LineElement, PointElement, LinearScale,
  CategoryScale, Title, Tooltip, Legend
} from 'chart.js'
import { useSensorStore } from '../stores/sensorStore'

ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend)

const store = useSensorStore()

const chartData = computed(() => ({
  labels: store.sensorData.slice(0, 20).map(d => d.timestamp?.slice(11, 19)).reverse(),
  datasets: [{
    label: 'Suhu (°C)',
    data: store.sensorData.slice(0, 20).map(d => d.suhu).reverse(),
    borderColor: '#ef4444',
    backgroundColor: 'rgba(239,68,68,0.1)',
    fill: true,
    tension: 0.4
  }]
}))

const chartOptions = {
  responsive: true,
  plugins: { legend: { position: 'top' } },
  scales: { y: { min: 20, max: 50 } }
}
</script>
```

### 7.2 React

```bash
npm create vite@latest iot-react -- --template react
cd iot-react
npm install axios mqtt recharts
```

```jsx
// src/components/SensorDashboard.jsx
import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import mqtt from 'mqtt'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

export default function SensorDashboard() {
  const [data, setData]    = useState([])
  const [latest, setLatest] = useState({})
  const mqttRef = useRef(null)

  useEffect(() => {
    // Fetch data awal
    axios.get('http://localhost:8000/api/sensor?limit=20')
      .then(res => setData(res.data.reverse()))

    // Koneksi MQTT via WebSocket (broker harus enable websocket port 9001)
    mqttRef.current = mqtt.connect('ws://localhost:9001')
    mqttRef.current.on('connect', () => {
      mqttRef.current.subscribe('sensor/#')
    })
    mqttRef.current.on('message', (topic, payload) => {
      try {
        const msg = JSON.parse(payload.toString())
        setLatest(msg)
        setData(prev => [...prev.slice(-49), msg])
      } catch (e) {}
    })

    return () => mqttRef.current?.end()
  }, [])

  return (
    <div style={{ padding: '20px' }}>
      <h1>🌡️ IoT Dashboard</h1>
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div style={{ background: '#fee2e2', padding: '16px', borderRadius: '8px' }}>
          <h3>Suhu Terkini</h3>
          <p style={{ fontSize: '2rem', margin: 0 }}>{latest.suhu ?? '--'}°C</p>
        </div>
        <div style={{ background: '#dbeafe', padding: '16px', borderRadius: '8px' }}>
          <h3>Kelembaban</h3>
          <p style={{ fontSize: '2rem', margin: 0 }}>{latest.kelembaban ?? '--'}%</p>
        </div>
      </div>
      <LineChart width={700} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="timestamp" hide />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="suhu" stroke="#ef4444" dot={false} />
        <Line type="monotone" dataKey="kelembaban" stroke="#3b82f6" dot={false} />
      </LineChart>
    </div>
  )
}
```

### 7.3 Angular

Angular adalah framework TypeScript lengkap dari Google, cocok untuk aplikasi enterprise besar.

```bash
npm install -g @angular/cli
ng new iot-angular --routing --style scss
cd iot-angular
ng generate component dashboard
ng generate service sensor
npm install mqtt chart.js
```

### 7.4 Perbandingan Frontend Framework

| Aspek | Vue.js 3 | React | Angular |
|-------|----------|-------|---------|
| **Kurva belajar** | Mudah | Sedang | Sulit |
| **Boilerplate** | Sedikit | Sedikit | Banyak |
| **State management** | Pinia (built-in feel) | Redux/Zustand | NgRx/Services |
| **TypeScript** | Opsional | Opsional | Wajib |
| **Cocok untuk** | Prototype, SPA | Besar, fleksibel | Enterprise |
| **Bundle size** | Kecil | Sedang | Besar |
| **Ekosistem** | Besar | Sangat besar | Besar (Google) |

### 7.5 Dashboard IoT dengan Chart.js / ECharts

```html
<!-- dashboard.html - Dashboard sederhana tanpa framework -->
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>IoT Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
    <style>
        body { font-family: sans-serif; background: #0f172a; color: #e2e8f0; margin: 20px; }
        .card { background: #1e293b; border-radius: 12px; padding: 20px; margin: 10px; display: inline-block; }
        .value { font-size: 3rem; font-weight: bold; color: #38bdf8; }
    </style>
</head>
<body>
    <h1>🌐 IoT Real-Time Dashboard</h1>
    <div class="card">
        <p>Suhu (°C)</p>
        <div class="value" id="suhu">--</div>
    </div>
    <div class="card">
        <p>Kelembaban (%)</p>
        <div class="value" id="hum">--</div>
    </div>
    <canvas id="chart" width="800" height="300"></canvas>

    <script>
        const ctx = document.getElementById('chart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    { label: 'Suhu (°C)',  data: [], borderColor: '#ef4444', fill: false },
                    { label: 'Hum (%)',    data: [], borderColor: '#3b82f6', fill: false }
                ]
            },
            options: { animation: false, scales: { y: { min: 0, max: 100 } } }
        });

        const client = mqtt.connect('ws://localhost:9001');
        client.on('connect', () => client.subscribe('sensor/#'));
        client.on('message', (topic, payload) => {
            const d = JSON.parse(payload.toString());
            document.getElementById('suhu').textContent = d.suhu + '°C';
            document.getElementById('hum').textContent  = d.kelembaban + '%';

            const time = new Date().toLocaleTimeString();
            if (chart.data.labels.length > 30) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
                chart.data.datasets[1].data.shift();
            }
            chart.data.labels.push(time);
            chart.data.datasets[0].data.push(d.suhu);
            chart.data.datasets[1].data.push(d.kelembaban);
            chart.update();
        });
    </script>
</body>
</html>
```

---

## 8. DEPLOYMENT

### 8.1 Localhost (Development)

Untuk pengembangan lokal, jalankan semua service secara bersamaan:

```bash
# Terminal 1: MQTT Broker
mosquitto -v

# Terminal 2: Python FastAPI Backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Node.js server (opsional)
node server.js

# Terminal 4: Frontend development server
cd iot-dashboard && npm run dev
# → http://localhost:5173

# Terminal 5: Python MQTT processor
python mqtt_subscriber.py
```

### 8.2 PM2 – Node.js Process Manager

PM2 mengelola proses Node.js agar berjalan terus-menerus, auto-restart jika crash, dan startup otomatis saat boot.

```bash
# Instalasi
npm install -g pm2

# Jalankan aplikasi
pm2 start server.js --name "iot-backend"
pm2 start mqtt_subscriber.py --interpreter python3 --name "mqtt-processor"

# Manajemen
pm2 list          # daftar semua proses
pm2 logs          # lihat semua log
pm2 logs iot-backend  # log spesifik
pm2 restart all   # restart semua
pm2 stop all      # stop semua
pm2 delete all    # hapus semua dari list

# Auto-start saat boot
pm2 startup       # ikuti instruksi yang muncul
pm2 save          # simpan konfigurasi
```

**Ecosystem file (`ecosystem.config.js`):**
```javascript
module.exports = {
  apps: [
    {
      name: "iot-backend",
      script: "server.js",
      env: { NODE_ENV: "production", PORT: 3000 },
      watch: false,
      autorestart: true,
      max_restarts: 10
    },
    {
      name: "mqtt-processor",
      script: "mqtt_subscriber.py",
      interpreter: "python3",
      autorestart: true
    }
  ]
}
```

```bash
pm2 start ecosystem.config.js
```

### 8.3 Nginx – Reverse Proxy dan Static File Server

Nginx digunakan sebagai:
1. **Reverse proxy**: meneruskan request HTTP ke backend (Node.js/Python)
2. **Static file server**: menyajikan file frontend (HTML/JS/CSS)
3. **Load balancer**: mendistribusikan traffic ke beberapa backend
4. **SSL termination**: menangani HTTPS

```bash
sudo apt install nginx -y
sudo systemctl enable nginx
```

**Konfigurasi Nginx (`/etc/nginx/sites-available/iot`):**
```nginx
# Redirect HTTP ke HTTPS
server {
    listen 80;
    server_name iot.domainanda.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name iot.domainanda.com;

    # SSL (diisi oleh Certbot)
    ssl_certificate     /etc/letsencrypt/live/iot.domainanda.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/iot.domainanda.com/privkey.pem;

    # Frontend - sajikan file build Vue/React
    root /var/www/iot-dashboard/dist;
    index index.html;
    location / {
        try_files $uri $uri/ /index.html;  # SPA routing
    }

    # Backend API - reverse proxy ke FastAPI/Node.js
    location /api/ {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
    }

    # WebSocket proxy
    location /ws/ {
        proxy_pass          http://127.0.0.1:8000;
        proxy_http_version  1.1;
        proxy_set_header    Upgrade $http_upgrade;
        proxy_set_header    Connection "upgrade";
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/iot /etc/nginx/sites-enabled/
sudo nginx -t          # test konfigurasi
sudo systemctl reload nginx
```

### 8.4 Certbot / Let's Encrypt – SSL Certificate

```bash
sudo apt install certbot python3-certbot-nginx -y

# Dapatkan sertifikat SSL gratis
sudo certbot --nginx -d iot.domainanda.com

# Renewal otomatis (sudah dikonfigurasi di cron)
sudo certbot renew --dry-run
```

### 8.5 ngrok – Tunnel Localhost ke Internet

ngrok sangat berguna untuk testing atau demo tanpa perlu domain dan server publik.

```bash
# Instalasi
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Daftar akun di https://ngrok.com dan dapatkan auth token
ngrok config add-authtoken TOKEN_DARI_NGROK

# Expose port 8000 ke internet
ngrok http 8000
# → https://abc123.ngrok.io (URL publik sementara)

# Expose MQTT (TCP)
ngrok tcp 1883
# → tcp://0.tcp.ngrok.io:PORT (untuk koneksi ESP32 dari mana saja)
```

### 8.6 Arsitektur Deployment Lengkap

```
INTERNET
    │
    │  HTTPS/443
    ▼
┌─────────────────────────────────────┐
│          NGINX (Reverse Proxy)      │
│  - SSL Termination (Certbot)        │
│  - Static file serving (Frontend)   │
│  - Proxy /api/ → Backend port 8000  │
│  - Proxy /ws/  → WebSocket server   │
└──────────────┬──────────────────────┘
               │ localhost
    ┌──────────┴──────────────────────┐
    │                                 │
    ▼                                 ▼
┌─────────┐                    ┌────────────┐
│ FastAPI │                    │  Node.js   │
│ :8000   │                    │  :3000     │
│ (PM2)   │                    │  (PM2)     │
└────┬────┘                    └─────┬──────┘
     │                               │
     └───────────┬───────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │        MQTT Broker            │
    │      Mosquitto :1883          │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │      Python Processor         │
    │   (MQTT → DB, Alerting)       │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │        Database               │
    │   PostgreSQL / InfluxDB       │
    └───────────────────────────────┘
         ↕
    ┌────────────────────────────────┐
    │     ESP32 Edge Devices         │
    │  (WiFi → MQTT → Broker)        │
    └────────────────────────────────┘
```

---

## 9. ARSITEKTUR SISTEM IoT LENGKAP

### 9.1 Alur Data End-to-End

```
1. ESP32 membaca sensor DHT22 setiap 5 detik
2. ESP32 publish JSON ke MQTT broker (topic: sensor/ruang1/data)
3. Python processor subscribe → terima data → simpan ke database
4. FastAPI expose REST API endpoint /api/sensor
5. Vue.js frontend fetch data via API + subscribe MQTT (WebSocket)
6. Dashboard tampilkan grafik real-time
7. Jika suhu > threshold → Python publish alert → ESP32 subscribe alert → nyalakan kipas
```

### 9.2 Format Pesan JSON Standar

```json
{
  "device_id":    "esp32-ruang-server-01",
  "lokasi":       "ruang-server",
  "suhu":         28.5,
  "kelembaban":   65.2,
  "tekanan_hpa":  1013.25,
  "uptime_ms":    3600000,
  "firmware_ver": "1.2.0",
  "timestamp":    "2024-01-15T10:30:00Z"
}
```

### 9.3 Checklist Implementasi

- [ ] Mosquitto broker terinstal dan berjalan
- [ ] ESP32 bisa connect WiFi dan terhubung ke MQTT broker
- [ ] ESP32 publish data sensor setiap interval tertentu
- [ ] Python subscriber menerima dan menyimpan data ke database
- [ ] FastAPI / Node.js menyediakan REST API
- [ ] Frontend menampilkan data real-time
- [ ] Alert berfungsi jika nilai sensor melewati threshold
- [ ] OTA update ESP32 berfungsi
- [ ] Nginx reverse proxy terkonfigurasi (untuk deployment)
- [ ] PM2 mengelola proses backend

---

## 10. REFERENSI

| Topik | Sumber | URL |
|-------|--------|-----|
| MQTT Specification | OASIS | mqtt.org |
| Mosquitto Broker | Eclipse Foundation | mosquitto.org |
| ESP32 Dokumentasi | Espressif | docs.espressif.com |
| PlatformIO | PlatformIO | docs.platformio.org |
| PubSubClient | Nick O'Leary | github.com/knolleary/pubsubclient |
| ArduinoJson | Benoit Blanchon | arduinojson.org |
| Paho MQTT Python | Eclipse | pypi.org/project/paho-mqtt |
| FastAPI | Sebastián Ramírez | fastapi.tiangolo.com |
| Vue.js 3 | Evan You | vuejs.org |
| React | Meta | react.dev |
| Chart.js | Community | chartjs.org |
| InfluxDB | InfluxData | docs.influxdata.com |
| PM2 | Unitech | pm2.keymetrics.io |
| Nginx | NGINX Inc | nginx.org/en/docs |
| ngrok | ngrok Inc | ngrok.com/docs |
| Let's Encrypt | ISRG | letsencrypt.org |

---

> **📝 Catatan Praktikum:**  
> Pada sesi lab, minimal implementasikan: ESP32 + Mosquitto + Python subscriber + FastAPI + Vue.js dashboard dalam jaringan lokal (localhost). Pastikan seluruh komponen dapat berkomunikasi sebelum mencoba deployment ke internet menggunakan ngrok atau server publik.

---

*Modul 04 – Praktikum Mekatronika dan Robotika | Teknik Mekatronika dan Robotika*
