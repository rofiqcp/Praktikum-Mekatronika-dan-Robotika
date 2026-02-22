# PERCOBAAN 07: ESP32 MODBUS RTU + MQTT PUBLISHER

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** ESP32 membaca PLC via RS-485 lalu publish data ke MQTT Broker  
**Platform:** ESP32 PlatformIO + PLC TM221/CP2E + Mosquitto MQTT  
**Estimasi Waktu:** 90 menit

---

## A. TUJUAN

1. Mengintegrasikan Modbus RTU dan MQTT dalam satu program ESP32
2. Memformat data PLC sebagai JSON menggunakan ArduinoJson
3. Mempublish data PLC ke MQTT broker via WiFi dari ESP32
4. Menangani reconnect WiFi dan MQTT secara otomatis

---

## B. KONFIGURASI

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
upload_speed = 921600
```

---

## C. PROGRAM ESP32

Lihat file `src/main.cpp` pada direktori ini.

---

## D. LANGKAH PERCOBAAN

1. Ganti konfigurasi WiFi dan MQTT server sesuai lab
2. Build dan upload ke ESP32
3. Buka Serial Monitor (115200 baud)
4. Buka `mosquitto_sub -t "plc/data" -v` di terminal lain
5. Amati data PLC mengalir dari ESP32 ke MQTT broker
6. Simulasikan disconnect WiFi: matikan AP → tunggu → nyalakan lagi
7. Catat waktu reconnect otomatis

---

## E. TABEL PENGAMATAN

| Iterasi | Registers [0-4] | WiFi? | MQTT? | JSON OK? | Waktu (ms) |
|---------|----------------|-------|-------|---------|-----------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Waktu reconnect WiFi setelah disconnect:** ________ detik

---

## F. PERTANYAAN ANALISIS

1. Mengapa ArduinoJson lebih baik dibanding membuat string JSON manual di ESP32?

2. Jelaskan fungsi `keepAlive` pada `mqttClient.setKeepAlive()`. Apa dampaknya terhadap konsumsi daya ESP32?

3. Dalam sistem industri, mana yang lebih handal: ESP32 sebagai gateway Modbus+MQTT vs Raspberry Pi Python? Jelaskan trade-off-nya.
