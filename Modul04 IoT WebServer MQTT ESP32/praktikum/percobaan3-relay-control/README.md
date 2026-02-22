# Percobaan 3: Remote Relay/LED Control via MQTT

## Deskripsi
Percobaan ini mengimplementasikan sistem kontrol relay dan LED jarak jauh menggunakan protokol MQTT.
ESP32 bertindak sebagai aktuator yang menerima perintah dan mempublikasikan status. Python CLI
di edge layer memungkinkan kontrol via terminal sekaligus meneruskan data ke backend Node.js.
Frontend Vue 3 menyajikan dashboard real-time via Socket.IO.

## Hardware yang Dibutuhkan
- 1x ESP32 DevKit
- 2x Relay Module (5V, aktif HIGH)
- 2x LED + resistor 220Ω
- Kabel jumper
- Breadboard

## Wiring Diagram (ASCII)

```
ESP32 DevKit
  ┌─────────────────┐
  │                 │
  │  GPIO26 ────────┼──► Relay 1 (IN)   ──► [Beban Listrik 1]
  │  GPIO27 ────────┼──► Relay 2 (IN)   ──► [Beban Listrik 2]
  │  GPIO2  ────────┼──► 220Ω ──► LED1 ──► GND
  │  GPIO4  ────────┼──► 220Ω ──► LED2 ──► GND
  │                 │
  │  3.3V   ────────┼──► Relay VCC (gunakan 5V jika relay butuh 5V)
  │  GND    ────────┼──► Relay GND, LED GND
  └─────────────────┘

Catatan: Untuk relay 5V, gunakan pin VIN (5V dari USB) bukan 3.3V
```

## Arsitektur Sistem

```
┌─────────────┐    MQTT      ┌──────────────┐    HTTP POST    ┌─────────────────┐
│   ESP32     │◄────────────►│  Python Edge │────────────────►│  Node.js Backend│
│  GPIO26,27  │              │  commander.py│                 │  Express + MQTT  │
│  GPIO2,4    │              │  (CLI + MQTT)│                 │  port 3001       │
└─────────────┘              └──────────────┘                 └────────┬────────┘
                                                                        │ Socket.IO
                                                               ┌────────▼────────┐
                                                               │  Vue 3 Frontend │
                                                               │  port 5173      │
                                                               └─────────────────┘
                                                                        │
                                                               ┌────────▼────────┐
                                                               │    MongoDB      │
                                                               │  port 27017     │
                                                               └─────────────────┘
```

## MQTT Topics

| Topic                  | Publisher | Subscriber    | Payload Contoh |
|------------------------|-----------|---------------|----------------|
| `control/relay/set`    | Edge/Web  | ESP32         | `{"relay":1,"state":"ON"}` |
| `control/relay/status` | ESP32     | Edge/Backend  | `{"relay1":"ON","relay2":"OFF","led1":"ON","led2":"OFF","uptime":123}` |
| `control/all/off`      | Edge/Web  | ESP32         | `{"command":"all_off"}` |

### Nomor Device pada `control/relay/set`:
| Nilai `relay` | Device  |
|---------------|---------|
| 1             | Relay 1 |
| 2             | Relay 2 |
| 3             | LED 1   |
| 4             | LED 2   |

## Setup & Cara Menjalankan

### 1. MQTT Broker (Mosquitto)
```bash
# Install
sudo apt install mosquitto mosquitto-clients

# Jalankan
sudo systemctl start mosquitto

# Test
mosquitto_sub -t "control/#" -v &
mosquitto_pub -t "control/relay/set" -m '{"relay":1,"state":"ON"}'
```

### 2. ESP32 Firmware
```bash
cd percobaan3-relay-control/esp32

# Edit kredensial WiFi dan IP broker di src/main.cpp:
# #define WIFI_SSID     "YOUR_WIFI_SSID"
# #define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
# #define MQTT_BROKER   "192.168.1.100"   ← IP komputer Anda

# Upload firmware
pio run --target upload

# Monitor serial
pio device monitor
```

### 3. MongoDB
```bash
# Install & jalankan
sudo systemctl start mongod

# Inisialisasi database
cd percobaan3-relay-control/server
node database/init.js
```

### 4. Backend Node.js
```bash
cd percobaan3-relay-control/server/backend
npm install
npm start
# Server berjalan di http://localhost:3001
```

### 5. Python Edge Commander
```bash
cd percobaan3-relay-control/edge
pip install -r requirements.txt
python commander.py
```

### 6. Frontend Vue 3
```bash
cd percobaan3-relay-control/server/frontend
npm install
npm run dev
# Buka http://localhost:5173
```

## Cara Menggunakan CLI Commander

Setelah menjalankan `python commander.py`, gunakan perintah berikut:

```
cmd> relay1 on        # Nyalakan Relay 1
cmd> relay1 off       # Matikan Relay 1
cmd> relay2 on        # Nyalakan Relay 2
cmd> led1 on          # Nyalakan LED 1
cmd> led2 off         # Matikan LED 2
cmd> all off          # Matikan semua (darurat)
cmd> status           # Tampilkan status terkini
cmd> help             # Tampilkan bantuan
cmd> quit             # Keluar program
```

## API Endpoints Backend

| Method | Endpoint                     | Deskripsi |
|--------|------------------------------|-----------|
| POST   | `/api/status`                | Terima status dari edge (Python) |
| GET    | `/api/status/latest`         | Status terbaru |
| GET    | `/api/status/history?limit=50` | Riwayat status |
| POST   | `/api/command`               | Kirim perintah ke MQTT |

## Troubleshooting

- **ESP32 tidak terhubung WiFi**: Periksa SSID dan password di `main.cpp`
- **MQTT connection refused**: Pastikan Mosquitto berjalan (`sudo systemctl status mosquitto`)
- **MongoDB error**: Pastikan MongoDB berjalan (`sudo systemctl status mongod`)
- **Frontend tidak menerima update**: Periksa koneksi Socket.IO di browser console (F12)
