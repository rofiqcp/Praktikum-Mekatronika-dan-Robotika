# Percobaan 4: Multi-Sensor Dashboard dengan Spring Boot + Angular

## Deskripsi
Percobaan ini mengimplementasikan sistem monitoring multi-sensor menggunakan ESP32 sebagai node
sensor, Python edge processor untuk pemrosesan data, Spring Boot sebagai backend REST API dengan
PostgreSQL, dan Angular sebagai frontend dashboard yang melakukan polling otomatis setiap 5 detik.

## Hardware yang Dibutuhkan
- 1x ESP32 DevKit
- 1x Sensor DHT22 (suhu + kelembaban)
- 1x Sensor LDR (Light Dependent Resistor) + resistor 10kΩ
- 1x Sensor Kelembaban Tanah (Soil Moisture)
- Kabel jumper + breadboard

## Wiring Diagram (ASCII)

```
ESP32 DevKit
  ┌──────────────────────────────┐
  │                              │
  │  GPIO4  ───────────────────┤ DHT22 (DATA)
  │                            │   ├── VCC → 3.3V
  │                            │   └── GND → GND
  │                            │   (Pull-up 4.7kΩ ke 3.3V)
  │                              │
  │  GPIO34 ──────────┬────────┤ LDR
  │                   │        │   ├── LDR ───── 3.3V
  │                   └─ 10kΩ ─┤   └── 10kΩ ─── GND
  │                   │        │   (Voltage divider: LDR + 10kΩ)
  │                              │
  │  GPIO35 ───────────────────┤ Soil Moisture (AOUT)
  │                            │   ├── VCC → 3.3V
  │                            │   └── GND → GND
  │                              │
  │  GPIO2  ─── LED (built-in) │
  │  3.3V   ─── DHT22 VCC      │
  │  GND    ─── Semua GND      │
  └──────────────────────────────┘

Catatan:
- GPIO34 dan GPIO35 adalah input-only (tidak ada pull-up internal)
- Untuk LDR: ADC rendah = terang, ADC tinggi = gelap
- Untuk Soil: ADC rendah = basah, ADC tinggi = kering
```

## Arsitektur Sistem

```
┌─────────────┐   MQTT (15s)   ┌──────────────┐   HTTP POST   ┌──────────────────┐
│   ESP32     │───────────────►│ Python Edge  │──────────────►│  Spring Boot     │
│  DHT22      │                │ processor.py │               │  Port 8080       │
│  LDR        │                │ • Outlier     │               │  REST API + JPA  │
│  Soil Moist │                │ • Moving Avg  │               └────────┬─────────┘
└─────────────┘                │ • Enrichment  │                        │ JPA
                               └──────────────┘               ┌────────▼─────────┐
                                                               │   PostgreSQL     │
                                                               │   Port 5432      │
                                                               └────────┬─────────┘
                                                                        │ HTTP Poll
                                                               ┌────────▼─────────┐
                                                               │  Angular 17      │
                                                               │  Port 4200       │
                                                               │  Polling 5s      │
                                                               └──────────────────┘
```

## MQTT Topics

| Topic                  | Publisher | Subscriber    | Payload Contoh |
|------------------------|-----------|---------------|----------------|
| `sensors/multi/data`   | ESP32     | Python Edge   | `{"device":"ESP32-MULTI","temperature":25.4,"humidity":62.1,"light":78,"soil_moisture":45,"battery":3.7,"ts":12345}` |
| `sensors/multi/config` | Operator  | ESP32         | `{"interval":30}` (interval dalam detik) |

## API Endpoints Spring Boot

| Method | Endpoint                        | Deskripsi |
|--------|---------------------------------|-----------|
| POST   | `/api/sensors`                  | Simpan pembacaan sensor baru |
| GET    | `/api/sensors?limit=100`        | Ambil pembacaan terbaru |
| GET    | `/api/sensors/stats`            | Statistik min/max/avg |
| GET    | `/api/sensors/device/{device}`  | Pembacaan per device |
| GET    | `/api/sensors/range?start=&end=`| Pembacaan berdasarkan rentang waktu |

## Setup & Cara Menjalankan

### 1. MQTT Broker (Mosquitto)
```bash
sudo apt install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
```

### 2. PostgreSQL
```bash
# Install
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Inisialisasi database
sudo -u postgres psql -f percobaan4-multisensor-springboot/server/database/init.sql

# Verifikasi
sudo -u postgres psql -d iot_praktikum -c "SELECT COUNT(*) FROM sensor_readings;"
```

### 3. ESP32 Firmware
```bash
cd percobaan4-multisensor-springboot/esp32

# Edit WiFi credentials dan MQTT broker IP di src/main.cpp:
# #define WIFI_SSID     "YOUR_WIFI_SSID"
# #define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
# #define MQTT_BROKER   "192.168.1.100"

# Upload firmware
pio run --target upload

# Monitor serial output
pio device monitor
```

### 4. Spring Boot Backend
```bash
cd percobaan4-multisensor-springboot/server/backend

# Sesuaikan database credentials di src/main/resources/application.properties:
# spring.datasource.password=YOUR_POSTGRES_PASSWORD

# Build
mvn clean package -DskipTests

# Jalankan
java -jar target/praktikum-1.0.0.jar

# Atau gunakan Maven langsung:
mvn spring-boot:run
```

### 5. Python Edge Processor
```bash
cd percobaan4-multisensor-springboot/edge
pip install -r requirements.txt
python processor.py
```

### 6. Angular Frontend
```bash
cd percobaan4-multisensor-springboot/server/frontend
npm install
npm start
# Buka http://localhost:4200
```

## Pemrosesan Data di Edge

Python processor melakukan tahapan berikut pada setiap pembacaan:

1. **Outlier Detection**: Membuang data di luar batas normal:
   - Suhu: -10°C hingga 80°C
   - Kelembaban: 0% hingga 100%
   - Cahaya & Kelembaban Tanah: 0% hingga 100%
   - Baterai: 2.5V hingga 4.3V

2. **Moving Average**: Merata-ratakan 5 pembacaan terakhir untuk mengurangi noise

3. **Unit Conversion**: Menambahkan suhu dalam Fahrenheit

4. **Enrichment**: Menambahkan metadata lokasi dan device

5. **Rotating Log**: Semua data tersimpan di `edge_processor.log` (max 10MB, 5 backup)

6. **Dashboard Summary**: Menampilkan statistik setiap 60 detik di terminal

## Mengubah Interval Publish ESP32

Kirim pesan MQTT ke `sensors/multi/config` untuk mengubah interval (dalam detik, 5-300):
```bash
mosquitto_pub -t "sensors/multi/config" -m '{"interval":30}'
```

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Spring Boot gagal start | Pastikan PostgreSQL berjalan dan credentials benar |
| Edge tidak bisa forward | Pastikan Spring Boot sudah berjalan di port 8080 |
| Angular tidak menerima data | Periksa browser console (F12), pastikan Spring Boot berjalan |
| DHT22 baca NaN | Periksa koneksi DATA pin dan pull-up resistor 4.7kΩ |
| LDR nilai selalu 0 atau 4095 | Periksa voltage divider (10kΩ ke GND) |
| MQTT tidak connect | Jalankan: `sudo systemctl status mosquitto` |
