/**
 * Percobaan 05: ESP32 Modbus TCP Client
 * Terhubung ke PLC TM221/CP2E via WiFi
 */

#include <Arduino.h>
#include <WiFi.h>
#include <ModbusTCP.h>

const char* WIFI_SSID = "NAMA_WIFI";
const char* WIFI_PASS = "PASSWORD_WIFI";

IPAddress PLC_IP(192, 168, 1, 10);
const int PLC_PORT = 502;

ModbusTCP mb;
uint16_t  regData[10];
bool      dataReady  = false;
uint32_t  lastPoll   = 0;
uint32_t  errorCount = 0;

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
        Serial.println("\n[OK] WiFi: " + WiFi.localIP().toString());
    } else {
        Serial.println("\n[WARN] WiFi gagal terhubung");
    }
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    connectWiFi();
    mb.client();
    Serial.println("=== ESP32 Modbus TCP Client ===");
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) connectWiFi();

    uint32_t now = millis();
    if (now - lastPoll >= 1000) {
        lastPoll = now;
        if (!mb.isConnected(PLC_IP)) {
            Serial.println("Connecting to PLC...");
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
        Serial.printf("| Errors: %lu\n", errorCount);
    }
}
