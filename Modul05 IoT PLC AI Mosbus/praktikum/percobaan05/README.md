# PERCOBAAN 05: ESP32 MODBUS TCP CLIENT – BACA PLC VIA WIFI

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** ESP32 sebagai Modbus TCP Client terhubung ke PLC via WiFi  
**Platform:** ESP32 + PlatformIO + PLC TM221/CP2E via Ethernet/WiFi  
**Estimasi Waktu:** 90 menit

---

## A. TUJUAN

1. Mengkonfigurasi ESP32 sebagai Modbus TCP Client via WiFi
2. Membaca dan menulis register PLC tanpa kabel RS-485 (hanya WiFi)
3. Memahami perbedaan implementasi Modbus RTU vs TCP pada ESP32
4. Menangani reconnect otomatis pada koneksi WiFi dan Modbus TCP

---

## B. KONFIGURASI

ESP32 terhubung ke AP/Router yang sama dengan PLC melalui WiFi.
PLC TM221 dikonfigurasi dengan IP statis 192.168.1.10 (lihat Percobaan 03).

---

## C. PROGRAM ESP32

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
    emelianov/modbus-esp8266@^4.1.0
monitor_speed = 115200
```

**`src/main.cpp`:**
```cpp
/**
 * Percobaan 05: ESP32 Modbus TCP Client
 * Terhubung ke PLC TM221 via WiFi
 */
#include <Arduino.h>
#include <WiFi.h>
#include <ModbusTCP.h>

const char* WIFI_SSID = "NAMA_WIFI";    // Ganti dengan SSID lab
const char* WIFI_PASS = "PASSWORD_WIFI"; // Ganti dengan password WiFi

IPAddress PLC_IP(192, 168, 1, 10);
const int PLC_PORT = 502;

ModbusTCP mb;
uint16_t regData[10];
bool dataReady = false;
uint32_t lastPoll = 0;
uint32_t errorCount = 0;

bool cbRead(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        dataReady = true;
    } else {
        Serial.printf("[ERROR] Modbus TCP: 0x%02X\n", event);
        errorCount++;
    }
    return true;
}

void connectWiFi() {
    if (WiFi.status() == WL_CONNECTED) return;
    Serial.printf("Menghubungkan ke WiFi '%s'...\n", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    uint8_t attempt = 0;
    while (WiFi.status() != WL_CONNECTED && attempt < 20) {
        delay(500);
        Serial.print(".");
        attempt++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[OK] WiFi terhubung: " + WiFi.localIP().toString());
    } else {
        Serial.println("\n[ERROR] WiFi gagal terhubung");
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    connectWiFi();
    mb.client();
    Serial.println("=== ESP32 Modbus TCP Client ===");
    Serial.println("PLC IP: " + PLC_IP.toString());
}

void loop() {
    // Reconnect WiFi jika terputus
    if (WiFi.status() != WL_CONNECTED) {
        connectWiFi();
    }

    uint32_t now = millis();
    if (now - lastPoll >= 1000) {
        lastPoll = now;

        if (!mb.isConnected(PLC_IP)) {
            Serial.println("Menghubungkan ke PLC Modbus TCP...");
            mb.connect(PLC_IP, PLC_PORT);
        }

        mb.readHreg(PLC_IP, 0, regData, 10, cbRead, 1);
    }

    mb.task();

    if (dataReady) {
        dataReady = false;
        Serial.print("Registers: ");
        for (int i = 0; i < 10; i++) {
            Serial.printf("MW%d=%d ", i, regData[i]);
        }
        Serial.printf(" | Errors: %lu\n", errorCount);
    }
}
```

---

## D. LANGKAH PERCOBAAN

1. Ganti `WIFI_SSID` dan `WIFI_PASS` sesuai jaringan lab
2. Build dan upload ke ESP32
3. Buka Serial Monitor
4. Amati: ESP32 connect ke WiFi → connect ke PLC → baca register
5. Cabut kabel Ethernet PLC sejenak — amati bagaimana sistem recover

---

## E. TABEL PENGAMATAN

| Iterasi | MW0-4 | WiFi RSSI (dBm) | TCP Connect Time (ms) | Error? |
|---------|-------|---------------|----------------------|--------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

**Waktu reconnect setelah disconnect:** ________ detik

---

## F. PERTANYAAN ANALISIS

1. Bagaimana `mb.task()` bekerja secara internal di library modbus-esp8266? Mengapa harus dipanggil di setiap iterasi loop?

2. Jelaskan dampak WiFi signal lemah (RSSI < -80 dBm) terhadap keandalan komunikasi Modbus TCP. Bagaimana mengatasinya?

3. Dalam konteks industri, apakah WiFi atau Ethernet lebih direkomendasikan untuk komunikasi Modbus TCP? Jelaskan alasannya.
