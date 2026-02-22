# Percobaan 1: Basic MQTT Publisher/Subscriber

## Tujuan Percobaan

1. Memahami protokol MQTT dan cara kerja model publish/subscribe.
2. Mengonfigurasi ESP32 sebagai MQTT Publisher yang mengirim data JSON secara periodik.
3. Mengonfigurasi Python edge subscriber untuk menerima dan meneruskan data ke backend.
4. Membangun backend Node.js/SQLite dan dashboard web untuk visualisasi data real-time.

---

## Arsitektur Sistem

```
┌─────────────┐        MQTT        ┌──────────────────┐       HTTP POST      ┌──────────────────────┐
│   ESP32     │ ─────────────────► │  Mosquitto MQTT  │ ◄──────────────────► │   Edge (Python)      │
│  Publisher  │  topic: praktikum/ │     Broker       │                      │   subscriber.py      │
│             │  esp32/hello       │  192.168.1.100   │                      │                      │
└─────────────┘                    │  port: 1883      │                      └──────────┬───────────┘
      ▲                            └──────────────────┘                                 │
      │ MQTT subscribe                                                         HTTP POST │ /api/data
      │ topic: praktikum/                                                               ▼
      │ esp32/command                                                       ┌──────────────────────┐
      │                                                                     │  Node.js Backend     │
      └ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤  Express + SQLite    │
                                                                            │  port: 3000          │
                                                                            └──────────┬───────────┘
                                                                                       │ HTTP GET /
                                                                                       ▼
                                                                            ┌──────────────────────┐
                                                                            │   Web Dashboard      │
                                                                            │   index.html         │
                                                                            │   (auto-refresh 3s)  │
                                                                            └──────────────────────┘
```

---

## Topologi Jaringan

```
LAN / WiFi (192.168.1.0/24)
├── ESP32          : 192.168.1.xxx  (DHCP)
├── MQTT Broker    : 192.168.1.100  (Mosquitto)
├── Edge Computer  : 192.168.1.xxx  (Python subscriber)
└── Server/Laptop  : 192.168.1.xxx  (Node.js backend + browser)
```

---

## MQTT Topics

| Topic                      | Arah          | Payload (JSON)                                                         |
|----------------------------|---------------|------------------------------------------------------------------------|
| `praktikum/esp32/hello`    | ESP32 → Broker | `{"device":"ESP32-01","uptime":123,"counter":1,"message":"Hello…"}`   |
| `praktikum/esp32/command`  | Broker → ESP32 | Pesan teks/JSON bebas untuk memerintah ESP32                           |

---

## Cara Menjalankan

### 1. Install & Jalankan Mosquitto MQTT Broker

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y mosquitto mosquitto-clients

# Aktifkan dan jalankan
sudo systemctl enable mosquitto
sudo systemctl start mosquitto

# Verifikasi broker berjalan
mosquitto_sub -h localhost -t "#" -v   # dengarkan semua topic
```

Edit `/etc/mosquitto/mosquitto.conf` jika perlu mengizinkan koneksi tanpa autentikasi:
```
listener 1883
allow_anonymous true
```

---

### 2. Flash ESP32

1. Buka folder `esp32/` dengan PlatformIO (VS Code Extension atau CLI).
2. Edit `src/main.cpp` – ubah konstanta berikut:
   ```cpp
   #define WIFI_SSID       "NAMA_WIFI_ANDA"
   #define WIFI_PASSWORD   "PASSWORD_WIFI_ANDA"
   #define MQTT_BROKER_IP  "192.168.1.100"   // IP komputer yang menjalankan Mosquitto
   ```
3. Flash ke board:
   ```bash
   cd esp32/
   pio run --target upload
   pio device monitor   # Serial Monitor 115200 baud
   ```

---

### 3. Jalankan Edge Python Subscriber

```bash
cd edge/
pip install -r requirements.txt

# Edit subscriber.py jika IP broker berbeda:
# MQTT_BROKER = "192.168.1.100"

python subscriber.py
```

Output yang diharapkan:
```
=== Percobaan 1 – Edge Subscriber ===
Broker : 192.168.1.100:1883
Topic  : praktikum/esp32/hello
Backend: http://localhost:3000/api/data
────────────────────────────────────────────────────────────
[MQTT] Connected to broker 192.168.1.100:1883
[MQTT] Subscribed to 'praktikum/esp32/hello'
[2024-01-15 10:30:05] device='ESP32-01'       uptime=    10s  counter=    1  msg='Hello from ESP32'
  → Backend OK (HTTP 200)
```

---

### 4. Jalankan Backend Node.js

```bash
cd server/backend/
npm install
npm start
```

Output yang diharapkan:
```
[Server] Percobaan 1 backend running on http://localhost:3000
[DB]     SQLite database at .../server/database/praktikum1.db
```

---

### 5. Buka Dashboard di Browser

```
http://localhost:3000
```

Dashboard menampilkan:
- **Total Pesan** yang tersimpan di database
- **Device / Counter / Uptime** terbaru
- **Tabel** 50 pesan terakhir yang di-refresh otomatis setiap 3 detik

---

## Struktur File

```
percobaan1-basic-mqtt/
├── esp32/
│   ├── platformio.ini        # Konfigurasi PlatformIO
│   └── src/
│       └── main.cpp          # Kode ESP32 (WiFi + MQTT Pub/Sub)
├── edge/
│   ├── subscriber.py         # Python MQTT subscriber + HTTP forwarder
│   └── requirements.txt
├── server/
│   ├── backend/
│   │   ├── index.js          # Express API (POST + GET /api/data)
│   │   └── package.json
│   ├── frontend/
│   │   └── index.html        # Dashboard (auto-refresh, dark theme)
│   └── database/
│       └── schema.sql        # Skema SQLite (referensi)
└── README.md
```

---

## Catatan Troubleshooting

| Masalah | Solusi |
|---------|--------|
| ESP32 tidak konek ke WiFi | Periksa SSID/password, pastikan ESP32 dalam jangkauan AP |
| ESP32 tidak konek ke MQTT broker | Periksa IP broker, pastikan Mosquitto berjalan dan `allow_anonymous true` |
| Python subscriber tidak bisa konek | Periksa IP broker di `subscriber.py` |
| Backend tidak menerima data | Pastikan backend sudah `npm start` sebelum menjalankan subscriber |
| Dashboard tidak update | Buka DevTools browser, cek Console/Network untuk error |
