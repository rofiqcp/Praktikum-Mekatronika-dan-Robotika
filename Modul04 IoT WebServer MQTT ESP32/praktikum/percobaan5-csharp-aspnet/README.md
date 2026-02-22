# Percobaan 5: MQTT-HTTP Bridge dengan C# .NET 8 + React

Arsitektur penuh tiga lapis: **ESP32 → MQTT Broker → C# Bridge App → ASP.NET Core API → SQLite → React Frontend**

---

## 🔧 Hardware yang Dibutuhkan

| Komponen         | Jumlah |
|-----------------|--------|
| ESP32 DevKit V1  | 1      |
| LDR (fotoresistor) + R 10kΩ | 1 set |
| Potensiometer 10kΩ | 1   |
| LED + R 220Ω    | 1 set  |
| Breadboard + kabel | secukupnya |

---

## 📐 Diagram Wiring

```
                    3.3V
                     │
                    ┌┤ LDR ├┐
                    │       │
ESP32 GPIO34 ───────┤       │
                    │       │
                   [10kΩ]
                    │
                   GND

                    3.3V
                     │
              ┌──────┤ POT ├──────┐
              │      │            │
             GND   GPIO35        GND
                  (wiper)

LED: GPIO2 → [220Ω] → Anoda LED → Katoda → GND
```

---

## 🏗️ Arsitektur Sistem

```
┌─────────────┐     MQTT publish      ┌───────────────┐
│   ESP32     │ ──────────────────►  │  MQTT Broker  │
│  (sensor)   │ ◄──────────────────  │ (Mosquitto)   │
│             │     MQTT subscribe    │               │
└─────────────┘                       └───────┬───────┘
                                              │ subscribe
                                              ▼
                                    ┌─────────────────┐
                                    │  C# Bridge App  │
                                    │  (MqttBridge)   │
                                    │  edge/           │
                                    └────────┬────────┘
                                             │ HTTP POST
                                             ▼
                                    ┌─────────────────┐
                                    │ ASP.NET Core 8  │
                                    │  REST API       │
                                    │  server/backend │
                                    └────────┬────────┘
                                             │ EF Core
                                             ▼
                                    ┌─────────────────┐
                                    │    SQLite DB    │
                                    │  iot_sensor.db  │
                                    └────────┬────────┘
                                             │ GET /api/sensors
                                             ▼
                                    ┌─────────────────┐
                                    │  React Frontend │
                                    │  (Vite + React) │
                                    │  server/frontend│
                                    └─────────────────┘
```

---

## 📡 MQTT Topics

| Topik                  | Arah          | Deskripsi                       |
|------------------------|---------------|---------------------------------|
| `bridge/sensors/raw`   | ESP32 → Broker | Data sensor LDR & potensiometer |
| `bridge/led/control`   | Broker → ESP32 | Kontrol brightness LED PWM      |

### Contoh Payload Sensor
```json
{
  "device":    "ESP32-BRIDGE",
  "light_raw": 2048,
  "light_pct": 50,
  "pot_raw":   1024,
  "pot_pct":   25,
  "uptime":    12345
}
```

### Contoh Payload LED Control
```json
{ "brightness": 128 }
```

---

## 🛠️ Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- [Node.js ≥ 18](https://nodejs.org/)
- MQTT Broker: `sudo apt install mosquitto mosquitto-clients`
- PlatformIO (untuk upload firmware ESP32)

---

## 🚀 Langkah Setup

### 1. MQTT Broker
```bash
sudo systemctl start mosquitto
# Verifikasi
mosquitto_sub -t "bridge/#" -v
```

### 2. Upload Firmware ESP32
```bash
cd esp32
# Edit WIFI_SSID, WIFI_PASSWORD, MQTT_BROKER di src/main.cpp
pio run --target upload
pio device monitor
```

### 3. Jalankan C# Bridge (Edge)
```bash
cd edge/MqttBridge
dotnet restore
dotnet run
```

### 4. Jalankan ASP.NET Core API (Backend)
```bash
cd server/backend/IotApi
dotnet restore
# Buat migration (pertama kali)
dotnet ef migrations add InitialCreate
dotnet run --urls "http://localhost:5000"
```

### 5. Jalankan React Frontend
```bash
cd server/frontend
npm install
npm run dev
# Buka http://localhost:5173
```

---

## 🔌 Endpoint API

| Method | Endpoint                  | Deskripsi                        |
|--------|---------------------------|----------------------------------|
| POST   | `/api/sensors`            | Terima data dari MQTT Bridge     |
| GET    | `/api/sensors?limit=50`   | Ambil data terbaru               |
| GET    | `/api/sensors/latest`     | Ambil data paling baru           |
| POST   | `/api/led/brightness`     | Kirim brightness ke MQTT → ESP32 |

---

## 📂 Struktur Direktori

```
percobaan5-csharp-aspnet/
├── esp32/                    # Firmware PlatformIO
│   ├── platformio.ini
│   └── src/main.cpp
├── edge/                     # Aplikasi C# Bridge
│   └── MqttBridge/
│       ├── MqttBridge.csproj
│       ├── Program.cs
│       ├── MqttService.cs
│       └── HttpForwarder.cs
├── server/
│   ├── backend/              # ASP.NET Core 8 REST API
│   │   └── IotApi/
│   │       ├── IotApi.csproj
│   │       ├── Program.cs
│   │       ├── appsettings.json
│   │       ├── Controllers/SensorController.cs
│   │       ├── Models/SensorReading.cs
│   │       └── Data/AppDbContext.cs
│   ├── frontend/             # React 18 + Vite 5
│   │   ├── src/
│   │   │   ├── App.jsx
│   │   │   ├── SensorCard.jsx
│   │   │   ├── SensorTable.jsx
│   │   │   └── main.jsx
│   │   ├── index.html
│   │   ├── package.json
│   │   └── vite.config.js
│   └── database/
│       └── schema.sql        # Referensi skema (EF Core auto-migrate)
└── README.md
```

---

## ❓ Troubleshooting

| Masalah | Solusi |
|---------|--------|
| ESP32 tidak terhubung WiFi | Periksa SSID/password di `main.cpp` |
| Bridge tidak menerima pesan | Periksa `MQTT_BROKER` IP di `Program.cs` |
| API tidak menerima data | Pastikan port 5000 tidak diblokir firewall |
| CORS error di browser | Pastikan CORS `AllowAll` aktif di `Program.cs` |
