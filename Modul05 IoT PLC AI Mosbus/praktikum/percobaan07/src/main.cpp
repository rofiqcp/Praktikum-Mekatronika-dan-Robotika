/**
 * Percobaan 07: ESP32 Modbus RTU Master + MQTT Publisher
 * Baca register PLC via RS-485 → publish JSON ke MQTT Broker via WiFi
 *
 * Libraries: modbus-esp8266, PubSubClient, ArduinoJson
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <ModbusRTU.h>

// ============================================================
// KONFIGURASI — Ganti sesuai lab
// ============================================================
const char* WIFI_SSID   = "NAMA_WIFI";
const char* WIFI_PASS   = "PASSWORD_WIFI";
const char* MQTT_SERVER = "192.168.1.100";  // IP MiniPC/server MQTT
const int   MQTT_PORT   = 1883;
const char* MQTT_TOPIC  = "plc/data";
const char* CLIENT_ID   = "ESP32_ModbusGW";

// RS-485
#define RXD2   16
#define TXD2   17
#define DE_RE   4

// Modbus
#define SLAVE_ID 1
// ============================================================

ModbusRTU mb;
WiFiClient espClient;
PubSubClient mqttClient(espClient);

uint16_t regData[10];
bool     dataReady  = false;
uint32_t lastPoll   = 0;
uint32_t pubCount   = 0;
uint32_t errCount   = 0;

// ──────────────────────────────────────────────────────────────
// Modbus callback
// ──────────────────────────────────────────────────────────────
bool cbReadRegs(Modbus::ResultCode event, uint16_t transId, void* data) {
    if (event == Modbus::EX_SUCCESS) {
        dataReady = true;
    } else {
        Serial.printf("[MODBUS ERROR] 0x%02X\n", event);
        errCount++;
    }
    return true;
}

// ──────────────────────────────────────────────────────────────
// WiFi
// ──────────────────────────────────────────────────────────────
void setupWiFi() {
    Serial.printf("Menghubungkan ke WiFi '%s'", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    uint8_t tries = 0;
    while (WiFi.status() != WL_CONNECTED && tries < 20) {
        delay(500);
        Serial.print(".");
        tries++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[WiFi OK] IP: " + WiFi.localIP().toString());
    } else {
        Serial.println("\n[WiFi GAGAL]");
    }
}

// ──────────────────────────────────────────────────────────────
// MQTT
// ──────────────────────────────────────────────────────────────
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    // Terima perintah dari broker (opsional)
    Serial.printf("[MQTT IN] topic=%s len=%d\n", topic, length);
}

void reconnectMQTT() {
    uint8_t attempts = 0;
    while (!mqttClient.connected() && attempts < 3) {
        Serial.printf("Connecting MQTT %s:%d...", MQTT_SERVER, MQTT_PORT);
        if (mqttClient.connect(CLIENT_ID)) {
            Serial.println(" OK");
            mqttClient.subscribe("plc/cmd/#");  // Subscribe topic perintah
        } else {
            Serial.printf(" gagal (rc=%d), coba lagi 2 detik\n", mqttClient.state());
            delay(2000);
            attempts++;
        }
    }
}

// ──────────────────────────────────────────────────────────────
// Publish data ke MQTT
// ──────────────────────────────────────────────────────────────
void publishData() {
    StaticJsonDocument<320> doc;
    doc["device"]  = CLIENT_ID;
    doc["plc_id"]  = SLAVE_ID;
    doc["ts"]      = millis();          // Gunakan timestamp relatif (ms sejak boot)
    doc["pub"]     = pubCount;
    doc["errors"]  = errCount;

    JsonArray regs = doc.createNestedArray("registers");
    for (int i = 0; i < 10; i++) regs.add(regData[i]);

    char buf[320];
    size_t len = serializeJson(doc, buf);

    if (mqttClient.publish(MQTT_TOPIC, buf, len)) {
        pubCount++;
        Serial.printf("[PUB #%lu] %s\n", pubCount, buf);
    } else {
        Serial.println("[PUB GAGAL]");
    }
}

// ──────────────────────────────────────────────────────────────
// Setup & Loop
// ──────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    delay(500);

    // RS-485 / Modbus
    Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2);
    mb.begin(&Serial2, DE_RE);
    mb.master();

    // WiFi
    setupWiFi();

    // MQTT
    mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
    mqttClient.setCallback(mqttCallback);
    mqttClient.setKeepAlive(60);

    Serial.println("=== ESP32 Modbus RTU + MQTT Gateway ===");
}

void loop() {
    // Pastikan koneksi WiFi
    if (WiFi.status() != WL_CONNECTED) setupWiFi();

    // Pastikan koneksi MQTT
    if (!mqttClient.connected()) reconnectMQTT();
    mqttClient.loop();

    // Poll Modbus setiap 1 detik
    uint32_t now = millis();
    if (now - lastPoll >= 1000) {
        lastPoll = now;
        if (!mb.slave()) {
            mb.readHreg(SLAVE_ID, 0, regData, 10, cbReadRegs);
        }
    }

    mb.task();

    // Publish jika data baru tersedia
    if (dataReady) {
        dataReady = false;
        publishData();
    }
}
