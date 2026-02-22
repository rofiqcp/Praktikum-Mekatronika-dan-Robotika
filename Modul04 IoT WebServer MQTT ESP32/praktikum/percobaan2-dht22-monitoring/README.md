# Percobaan 2: DHT22 Temperature & Humidity Monitoring

## Tujuan Percobaan

1. Membaca data suhu, kelembaban, dan heat index dari sensor DHT22 menggunakan ESP32.
2. Mengirim data sensor secara periodik ke MQTT broker dalam format JSON.
3. Memproses data di edge (Python) dan menyimpannya ke file CSV dan database PostgreSQL.
4. Menampilkan data secara real-time pada dashboard React + Vite.
5. Memahami integrasi penuh ESP32 → MQTT → Edge → REST API → Frontend.

---

## Kebutuhan Hardware

| Komponen | Jumlah | Keterangan |
|----------|--------|------------|
| ESP32 DevKit | 1 | Board utama |
| DHT22 (AM2302) | 1 | Sensor suhu & kelembaban |
| Resistor 10kΩ | 1 | Pull-up pada pin DATA |
| Kabel jumper | 3 | Koneksi sensor ke ESP32 |

### Wiring DHT22 → ESP32

```
DHT22          ESP32
─────          ─────
VCC   ────────► 3.3V
DATA  ────┬───► GPIO4
          │
        [10kΩ]
          │
GND   ────┴───► GND
```

> **Catatan:** Pin DATA membutuhkan resistor pull-up 10kΩ ke VCC untuk operasi yang stabil.

---

## Arsitektur Sistem

```
┌──────────────────────┐      MQTT       ┌──────────────────┐      HTTP POST     ┌─────────────────────┐
│  ESP32 + DHT22       │ ──────────────► │  Mosquitto MQTT  │ ──────────────────► │  Edge (Python)      │
│  Baca sensor 10 dtk  │  sensor/dht22/  │     Broker       │                    │  subscriber.py      │
│  Publish JSON        │  data           │  192.168.1.100   │                    │  - CSV logger       │
│                      │                 │  port: 1883      │                    │  - Stats rolling    │
│                      │ ◄────────────── │                  │                    └─────────┬───────────┘
│  LED toggle via MQTT │  sensor/dht22/  └──────────────────┘                              │
└──────────────────────┘  led                                                    HTTP POST │ /api/sensor
                                                                                           ▼
                                                                                ┌─────────────────────┐
                                                                                │  Flask Backend      │
                                                                                │  app.py             │
                                                                                │  PostgreSQL         │
                                                                                │  port: 5000         │
                                                                                └─────────┬───────────┘
                                                                                          │ HTTP GET /api
                                                                                          ▼
                                                                                ┌─────────────────────┐
                                                                                │  React Frontend     │
                                                                                │  Vite dev server    │
                                                                                │  port: 5173         │
                                                                                │  (auto-refresh 5s)  │
                                                                                └─────────────────────┘
```

---

## Topologi Jaringan

```
LAN / WiFi (192.168.1.0/24)
├── ESP32 + DHT22   : 192.168.1.xxx  (DHCP)
├── MQTT Broker     : 192.168.1.100  (Mosquitto)
├── Edge Computer   : 192.168.1.xxx  (Python subscriber + CSV)
└── Server/Laptop   : 192.168.1.xxx  (Flask + PostgreSQL + React)
```

---

## MQTT Topics

| Topic                  | Arah           | Payload (JSON)                                                                               |
|------------------------|----------------|----------------------------------------------------------------------------------------------|
| `sensor/dht22/data`    | ESP32 → Broker | `{"device":"ESP32-DHT22","temperature":26.5,"humidity":65.2,"heat_index":27.1,"ts":12345}`   |
| `sensor/dht22/led`     | Broker → ESP32 | `"ON"` / `"OFF"` / `"1"` / `"0"` – toggle LED GPIO2                                         |

---

## Cara Menjalankan

### 1. PostgreSQL – Buat Database dan Tabel

```bash
# Pastikan PostgreSQL sudah terinstall dan berjalan
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql

# Buat database
sudo -u postgres psql -c "CREATE DATABASE iot_db;"

# Buat user jika perlu (opsional)
sudo -u postgres psql -c "CREATE USER iot_user WITH PASSWORD 'iot_pass';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE iot_db TO iot_user;"

# Jalankan init.sql
sudo -u postgres psql -d iot_db -f server/database/init.sql
```

---

### 2. Flash ESP32

1. Buka folder `esp32/` dengan PlatformIO.
2. Edit `src/main.cpp` – ubah konstanta berikut:
   ```cpp
   #define WIFI_SSID       "NAMA_WIFI_ANDA"
   #define WIFI_PASSWORD   "PASSWORD_WIFI_ANDA"
   #define MQTT_BROKER_IP  "192.168.1.100"
   ```
3. Flash dan buka serial monitor:
   ```bash
   cd esp32/
   pio run --target upload
   pio device monitor
   ```

Output serial yang diharapkan:
```
=== Percobaan 2: DHT22 Sensor Monitoring ===
[WiFi] Connecting to MY_WIFI ............
[WiFi] Connected. IP: 192.168.1.105
[MQTT] Connecting to 192.168.1.100:1883 … connected.
[MQTT] Subscribed to 'sensor/dht22/led'
[MQTT] Published → T=26.5°C  H=65.2%  HI=27.1°C  [OK]
```

---

### 3. Jalankan Edge Python Subscriber

```bash
cd edge/
pip install -r requirements.txt
python subscriber.py
```

Output yang diharapkan:
```
=== Percobaan 2 – DHT22 Edge Subscriber ===
Broker : 192.168.1.100:1883
...
[2024-01-15 10:30:05] ESP32-DHT22       T= 26.5°C  H= 65.2%  HI= 27.1°C
  ┌─ Stats (last 1 readings) ─────────────────────────
  │ Temp min=26.5°C  max=26.5°C  avg=26.50°C
  └─────────────────────────────────────────────────────
  → Backend OK (HTTP 200)
```

Data CSV tersimpan di `edge/data/sensor_log.csv`.

---

### 4. Jalankan Flask Backend

```bash
cd server/backend/

# Opsional: buat file .env untuk DATABASE_URL kustom
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/iot_db" > .env

pip install -r requirements.txt
python app.py
```

Output:
```
[DB] Table sensor_readings ready.
 * Running on http://0.0.0.0:5000
```

Test API:
```bash
curl http://localhost:5000/api/sensor?limit=5
curl http://localhost:5000/api/sensor/stats
```

---

### 5. Jalankan React Frontend (Vite)

```bash
cd server/frontend/
npm install
npm run dev
```

Buka browser: **http://localhost:5173**

Dashboard menampilkan:
- **Suhu, Kelembaban, Heat Index** terbaru dalam kartu besar berwarna
- **Stats** (min/max/avg, 1 jam terakhir)
- **Tabel** 20 pembacaan terbaru, auto-refresh setiap 5 detik

---

## Struktur File

```
percobaan2-dht22-monitoring/
├── esp32/
│   ├── platformio.ini             # PlatformIO + library DHT22
│   └── src/
│       └── main.cpp               # ESP32: baca DHT22 + MQTT pub/sub + LED control
├── edge/
│   ├── subscriber.py              # MQTT → CSV + Flask + rolling stats
│   └── requirements.txt
├── server/
│   ├── backend/
│   │   ├── app.py                 # Flask REST API (POST/GET/stats)
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── index.html             # Entry HTML untuk Vite
│   │   ├── package.json
│   │   ├── vite.config.js         # Proxy /api → Flask :5000
│   │   └── src/
│   │       ├── main.jsx           # React root render
│   │       └── App.jsx            # Dashboard component
│   └── database/
│       └── init.sql               # PostgreSQL DDL
└── README.md
```

---

## Output yang Diharapkan

### Serial Monitor ESP32
```
[MQTT] Published → T=26.5°C  H=65.2%  HI=27.1°C  [OK]
[MQTT] Received on 'sensor/dht22/led': ON
[LED] State → ON
```

### Edge Subscriber
```
[2024-01-15 10:30:15] ESP32-DHT22       T= 26.5°C  H= 65.2%  HI= 27.1°C
  ┌─ Stats (last 5 readings) ─────────────────────────
  │ Temp min=25.8°C  max=27.1°C  avg=26.44°C
  └─────────────────────────────────────────────────────
  → Backend OK (HTTP 200)
```

### API Response `GET /api/sensor/stats`
```json
{
  "period": "last_1_hour",
  "count": 36,
  "temperature": { "min": 25.8, "max": 27.5, "avg": 26.44 },
  "humidity":    { "min": 62.1, "max": 68.3, "avg": 65.12 }
}
```

---

## Catatan Troubleshooting

| Masalah | Solusi |
|---------|--------|
| DHT22 membaca NaN | Periksa koneksi kabel, pastikan pull-up 10kΩ terpasang |
| ESP32 tidak konek WiFi | Periksa SSID/password, jarak ke router |
| Flask error koneksi DB | Periksa `DATABASE_URL`, pastikan PostgreSQL berjalan |
| Vite tidak bisa reach `/api` | Pastikan Flask berjalan di port 5000 sebelum `npm run dev` |
| Data tidak masuk ke tabel | Periksa log edge subscriber dan Flask untuk error HTTP |
