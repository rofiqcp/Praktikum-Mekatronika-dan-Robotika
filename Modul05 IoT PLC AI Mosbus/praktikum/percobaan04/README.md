# PERCOBAAN 04: KOMUNIKASI MODBUS RTU – ESP32 PLATFORMIO (MASTER)

**Modul:** 05 – IoT PLC AI Modbus  
**Topik:** ESP32 sebagai Modbus RTU Master membaca PLC  
**Platform:** ESP32 + PlatformIO + PLC TM221/CP2E via RS-485 (MAX485)  
**Estimasi Waktu:** 90 menit

---

## A. TUJUAN

1. Mengkonfigurasi ESP32 sebagai Modbus RTU Master menggunakan PlatformIO
2. Memahami wiring ESP32 ke modul MAX485 untuk RS-485 half-duplex
3. Membaca Holding Register dan Coil dari PLC menggunakan library modbus-esp8266
4. Menampilkan data PLC di Serial Monitor PlatformIO

---

## B. WIRING HARDWARE

```
ESP32           MAX485 Module      RS-485 Bus
GPIO17 (TX2) ──► DI                A(+) ──── PLC SL1 A(+)
GPIO16 (RX2) ◄── RO                B(-) ──── PLC SL1 B(-)
GPIO4        ──► DE
GPIO4        ──► RE (DE dan RE dihubungkan)
3.3V         ──► VCC (modul 3.3V) atau 5V (modul 5V, perlu level shifter)
GND          ──► GND
```

> **Catatan:** Pin DE dan RE pada MAX485 harus dihubungkan ke GPIO yang sama.
> HIGH = Transmit mode, LOW = Receive mode.

**Resistor terminasi:** Pasang resistor 120Ω antara A(+) dan B(-) di setiap ujung bus RS-485.

---

## C. KONFIGURASI PLATFORMIO

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
    emelianov/modbus-esp8266@^4.1.0
monitor_speed = 115200
upload_speed = 921600
```

---

## D. PROGRAM ESP32 (PlatformIO)

**File: `src/main.cpp`**

```cpp
/**
 * Percobaan 04: ESP32 Modbus RTU Master
 * Membaca Holding Register dan Coil dari PLC TM221/CP2E
 *
 * Library: emelianov/modbus-esp8266
 * Hardware: ESP32 + MAX485 + PLC via RS-485
 */

#include <Arduino.h>
#include <ModbusRTU.h>

// ============================================================
// KONFIGURASI
// ============================================================
#define RXD2        16      // GPIO RX untuk RS-485
#define TXD2        17      // GPIO TX untuk RS-485
#define RS485_DE_RE  4      // GPIO direction control MAX485

#define PLC_SLAVE_ID  1
#define REG_START     0
#define REG_COUNT    10
#define COIL_START 2048
#define COIL_COUNT    4

#define POLL_INTERVAL_MS 1000
// ============================================================

ModbusRTU mb;

uint16_t regData[REG_COUNT];
bool     coilData[COIL_COUNT];
bool     regReady  = false;
bool     coilReady = false;
uint32_t lastPoll  = 0;
uint32_t errorCount = 0;

// Callback: dipanggil setelah read_holding_registers selesai
bool cbReadRegs(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        regReady = true;
    } else {
        Serial.printf("[ERROR] ReadHreg: 0x%02X\n", event);
        errorCount++;
    }
    return true;
}

// Callback: dipanggil setelah read_coils selesai
bool cbReadCoils(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        coilReady = true;
    } else {
        Serial.printf("[ERROR] ReadCoil: 0x%02X\n", event);
        errorCount++;
    }
    return true;
}

void tampilkanData() {
    Serial.println("──────────────────────────────────");
    Serial.print("Holding Registers (MW0-MW9): ");
    for (int i = 0; i < REG_COUNT; i++) {
        Serial.printf("MW%d=%d ", i, regData[i]);
    }
    Serial.println();

    Serial.print("Coils (Q0.0-Q0.3): ");
    for (int i = 0; i < COIL_COUNT; i++) {
        Serial.printf("Q0.%d=%s ", i, coilData[i] ? "ON" : "OFF");
    }
    Serial.println();
    Serial.printf("Error count: %lu\n", errorCount);
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    // Inisialisasi UART2 untuk RS-485
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);

    // Inisialisasi Modbus RTU Master dengan DE/RE control
    mb.begin(&Serial2, RS485_DE_RE);
    mb.master();

    Serial.println("=== ESP32 Modbus RTU Master ===");
    Serial.printf("RX=%d TX=%d DE/RE=%d\n", RXD2, TXD2, RS485_DE_RE);
    Serial.printf("PLC Slave ID=%d, Baud=9600\n", PLC_SLAVE_ID);
    Serial.println("Polling PLC setiap 1 detik...");
}

void loop() {
    // Proses antrian Modbus (wajib dipanggil di setiap loop)
    mb.task();

    uint32_t now = millis();
    if (now - lastPoll >= POLL_INTERVAL_MS) {
        lastPoll = now;

        // Jika tidak ada transaksi aktif, mulai pembacaan baru
        if (!mb.slave()) {
            // Baca Holding Register
            mb.readHreg(
                PLC_SLAVE_ID,
                REG_START,
                regData,
                REG_COUNT,
                cbReadRegs
            );
        }
    }

    // Tampilkan data setelah berhasil dibaca
    if (regReady) {
        regReady = false;
        tampilkanData();

        // Baca Coil setelah register berhasil (opsional, bisa juga serial)
        mb.readCoil(
            PLC_SLAVE_ID,
            COIL_START,
            coilData,
            COIL_COUNT,
            cbReadCoils
        );
    }
}
```

---

## E. LANGKAH PERCOBAAN

1. Buat project PlatformIO baru (ESP32 Dev Module, Arduino framework)
2. Edit `platformio.ini` seperti di atas
3. Salin kode ke `src/main.cpp`
4. **Build** (PlatformIO: Build): pastikan 0 error
5. Rangkai ESP32-MAX485 sesuai wiring diagram
6. Sambungkan bus RS-485 ESP32 ke port SL1 PLC
7. **Upload** ke ESP32
8. Buka **Serial Monitor** (115200 baud)
9. Amati output: nilai register PLC harus tampil setiap 1 detik

---

## F. TABEL PENGAMATAN

| Iterasi | MW0 | MW1 | MW2 | MW3 | MW4 | Q0.0 | Q0.1 | Error |
|---------|-----|-----|-----|-----|-----|------|------|-------|
| 1 | | | | | | | | |
| 2 | | | | | | | | |
| 3 | | | | | | | | |
| 4 | | | | | | | | |
| 5 | | | | | | | | |

**Total Error Count setelah 60 detik:** ________

---

## G. PERTANYAAN ANALISIS

1. Mengapa `mb.task()` harus dipanggil setiap iterasi `loop()`? Apa yang terjadi jika tidak dipanggil?

2. Apa fungsi pin DE/RE pada MAX485? Jelaskan perbedaan mode transmit dan receive pada RS-485 half-duplex.

3. Bandingkan pendekatan callback pada library Arduino ini dengan pendekatan synchronous pada pymodbus Python. Apa kelebihan dan kekurangan masing-masing?

---

## H. REFERENSI

- Library modbus-esp8266: https://github.com/emelianov/modbus-esp8266
- PlatformIO ESP32: https://docs.platformio.org/en/latest/boards/espressif32/
- MAX485 Datasheet: https://www.maximintegrated.com/en/products/interface/transceivers/MAX485.html
