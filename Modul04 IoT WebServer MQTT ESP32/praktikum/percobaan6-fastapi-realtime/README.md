# Percobaan 6: Real-Time Dashboard FastAPI + WebSocket + Vue.js 3 + MongoDB + PM2

Dashboard IoT real-time penuh menggunakan arsitektur **event-driven**: ESP32 mengirim data melalui MQTT → edge layer mendeteksi anomali → FastAPI menyiarkan ke browser melalui WebSocket tanpa polling.

---

## 🔧 Hardware yang Dibutuhkan

| Komponen              | Jumlah |
|-----------------------|--------|
| ESP32 DevKit V1        | 1      |
| DHT22 (sensor suhu & kelembaban) | 1 |
| MQ-2 (sensor gas/asap) | 1     |
| PIR HC-SR501 (sensor gerak) | 1  |
| LED + R 220Ω           | 1 set  |
| Breadboard + kabel     | secukupnya |

---

## 📐 Diagram Wiring

```
DHT22:
  VCC → 3.3V
  GND → GND
  DATA → GPIO4 (+ pull-up 10kΩ ke 3.3V)

MQ-2:
  VCC → 5V (gunakan pin VIN atau sumber 5V)
  GND → GND
  AOUT → GPIO36 (ADC1_CH0, input-only)

PIR HC-SR501:
  VCC → 5V
  GND → GND
  OUT → GPIO14

LED Indikator:
  GPIO2 → [220Ω] → Anoda → Katoda → GND
```

---

## 🏗️ Arsitektur Sistem

```
┌──────────────┐  MQTT publish  ┌────────────────┐
│   ESP32      │ ─────────────► │  MQTT Broker   │
│ DHT22/MQ2/PIR│ ◄──────────── │  (Mosquitto)   │
└──────────────┘  (alert sub)   └───────┬────────┘
                                        │ subscribe
                            ┌───────────┴───────────┐
                            │                       │
                    ┌───────▼───────┐   ┌───────────▼────────┐
                    │  Anomaly      │   │  FastAPI Backend   │
                    │  Detector     │   │  (MQTT subscriber) │
                    │  (Z-score)    │   │  mqtt_client.py    │
                    └───────┬───────┘   └───────────┬────────┘
                            │ HTTP POST              │
                            └──────────►────────────┘
                                        │ save
                                        ▼
                                ┌───────────────┐
                                │   MongoDB     │
                                │  iot_realtime │
                                └───────┬───────┘
                                        │ WebSocket broadcast
                                        ▼
                                ┌───────────────┐
                                │  Vue.js 3     │
                                │  Dashboard    │
                                │  (Real-Time)  │
                                └───────────────┘
```

---

## 📡 MQTT Topics

| Topik                     | Arah                | Deskripsi                      |
|---------------------------|---------------------|--------------------------------|
| `realtime/sensors/data`   | ESP32 → Broker      | Data DHT22 + MQ-2 + PIR setiap 5 detik |
| `realtime/alerts/motion`  | ESP32 → Broker      | Alert langsung saat PIR aktif  |
| `realtime/alerts/anomaly` | Edge → Broker       | Alert anomali dari Z-score     |

### Contoh Payload Sensor
```json
{
  "device":      "ESP32-RT",
  "temperature": 26.5,
  "humidity":    58.0,
  "gas_level":   312,
  "gas_ppm":     45.2,
  "motion":      false,
  "uptime":      12345
}
```

### Contoh Payload Motion Alert
```json
{ "device": "ESP32-RT", "alert": "motion_detected", "ts": 123456789 }
```

---

## 🧠 Cara Kerja Deteksi Anomali (Z-score)

Z-score mengukur seberapa jauh sebuah nilai dari rata-rata distribusi:

```
z = (x - μ) / σ
```

- `x` = nilai baru yang masuk
- `μ` = rata-rata dari N data sebelumnya (window = 20)
- `σ` = standar deviasi window

**Jika `|z| > 2.5`**, nilai tersebut dianggap anomali dan alert dipublikasikan ke `realtime/alerts/anomaly`.

Artinya: nilai yang melebihi 2.5× standar deviasi dari rata-rata historis akan memicu peringatan.

---

## 🛠️ Prerequisites

- Python 3.11+
- Node.js ≥ 18
- MongoDB Community Edition (lokal)
- MQTT Broker: `sudo apt install mosquitto mosquitto-clients`
- PM2: `npm install -g pm2`
- PlatformIO (untuk upload firmware ESP32)

---

## 🚀 Langkah Setup

### 1. MQTT Broker
```bash
sudo systemctl start mosquitto
```

### 2. MongoDB
```bash
sudo systemctl start mongod
```

### 3. Upload Firmware ESP32
```bash
cd esp32
# Edit WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER di src/main.cpp
pio run --target upload
pio device monitor
```

### 4. Inisialisasi Database
```bash
cd server/database
pip install pymongo
python init_mongo.py
```

### 5. Setup Backend
```bash
cd server/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Setup Edge (Anomaly Detector)
```bash
cd edge
pip install -r requirements.txt
python anomaly_detector.py
```

### 7. Setup Frontend
```bash
cd server/frontend
npm install
npm run dev
# Buka http://localhost:5174
```

### 8. Deploy dengan PM2 (Produksi)
```bash
cd server
mkdir -p logs
pm2 start ecosystem.config.js
pm2 status
pm2 logs
```

---

## 🔌 Endpoint API

| Method    | Endpoint              | Deskripsi                         |
|-----------|-----------------------|-----------------------------------|
| GET       | `/`                   | Health check                      |
| POST      | `/api/sensor`         | Kirim data sensor dari edge       |
| GET       | `/api/sensors?limit=50` | Ambil pembacaan terbaru         |
| GET       | `/api/alerts?limit=20` | Ambil alert terbaru              |
| GET       | `/api/stats`          | Statistik agregat                 |
| WebSocket | `/ws`                 | Stream real-time ke browser       |

---

## 📂 Struktur Direktori

```
percobaan6-fastapi-realtime/
├── esp32/                      # Firmware PlatformIO
│   ├── platformio.ini
│   └── src/main.cpp
├── edge/                       # Edge processing
│   ├── anomaly_detector.py
│   └── requirements.txt
└── server/
    ├── backend/                # FastAPI + MongoDB
    │   ├── main.py
    │   ├── models.py
    │   ├── database.py
    │   ├── mqtt_client.py
    │   └── requirements.txt
    ├── frontend/               # Vue 3 + Pinia + Vite
    │   ├── src/
    │   │   ├── App.vue
    │   │   ├── main.js
    │   │   ├── components/
    │   │   │   ├── MetricGauge.vue
    │   │   │   ├── AlertList.vue
    │   │   │   └── RealtimeChart.vue
    │   │   └── stores/sensor.js
    │   ├── index.html
    │   ├── package.json
    │   └── vite.config.js
    ├── database/
    │   └── init_mongo.py
    └── ecosystem.config.js     # PM2 deployment
```

---

## ❓ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| DHT22 membaca NaN | Periksa kabel data + pull-up 10kΩ |
| MQ-2 nilai tidak stabil | Beri waktu pemanasan ±2 menit sebelum baca |
| WebSocket putus terus | Periksa firewall/proxy; store akan auto-reconnect |
| MongoDB tidak tersambung | `sudo systemctl start mongod` |
| PM2 proses error | `pm2 logs iot-backend --lines 50` |
