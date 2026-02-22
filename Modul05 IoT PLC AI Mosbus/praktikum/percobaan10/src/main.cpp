/**
 * Percobaan 10: ESP32 – Sensor Node + MQTT Publisher
 * Mengirim data dari sensor lokal ESP32 ke MQTT Broker
 * sebagai pelengkap data dari PLC Gateway
 *
 * Libraries: PubSubClient, ArduinoJson
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ============================================================
const char* WIFI_SSID   = "NAMA_WIFI";
const char* WIFI_PASS   = "PASSWORD_WIFI";
const char* MQTT_SERVER = "192.168.1.100";
const int   MQTT_PORT   = 1883;
const char* MQTT_TOPIC  = "esp32/sensor_node";
const char* CLIENT_ID   = "ESP32_SensorNode";

// Simulasi sensor dengan ADC (potensiometer)
#define ANALOG_PIN_1 34   // ADC1_CH6 – sensor 1
#define ANALOG_PIN_2 35   // ADC1_CH7 – sensor 2
#define LED_STATUS   2    // LED bawaan ESP32
// ============================================================

WiFiClient espClient;
PubSubClient mqttClient(espClient);
uint32_t lastPub  = 0;
uint32_t pubCount = 0;

void setupWiFi() {
    Serial.printf("WiFi '%s'...", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    uint8_t tries = 0;
    while (WiFi.status() != WL_CONNECTED && tries < 20) {
        delay(500);
        Serial.print(".");
        tries++;
    }
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n[WiFi OK] " + WiFi.localIP().toString());
    }
}

void reconnectMQTT() {
    uint8_t att = 0;
    while (!mqttClient.connected() && att < 3) {
        if (mqttClient.connect(CLIENT_ID)) {
            Serial.println("[MQTT OK]");
            mqttClient.subscribe("esp32/cmd");  // Subscribe perintah
        } else {
            delay(2000);
            att++;
        }
    }
}

void mqttCallback(char* topic, byte* payload, unsigned int len) {
    Serial.printf("[CMD] topic=%s len=%u\n", topic, len);
    // Proses perintah dari server (opsional)
}

float bacaSensor1() {
    // Baca ADC → konversi ke nilai persentase 0–100%
    int raw = analogRead(ANALOG_PIN_1);
    return (raw / 4095.0f) * 100.0f;
}

float bacaSensor2() {
    int raw = analogRead(ANALOG_PIN_2);
    return (raw / 4095.0f) * 100.0f;
}

void publishData() {
    StaticJsonDocument<256> doc;
    doc["device"]  = CLIENT_ID;
    doc["ts"]      = millis();
    doc["pub"]     = pubCount;
    doc["sensor1"] = round(bacaSensor1() * 10) / 10.0;  // 1 desimal
    doc["sensor2"] = round(bacaSensor2() * 10) / 10.0;
    doc["wifi_rssi"] = WiFi.RSSI();
    doc["uptime_s"]  = millis() / 1000;

    char buf[256];
    serializeJson(doc, buf);

    if (mqttClient.publish(MQTT_TOPIC, buf)) {
        pubCount++;
        digitalWrite(LED_STATUS, HIGH);
        delay(50);
        digitalWrite(LED_STATUS, LOW);
        Serial.printf("[PUB #%lu] %s\n", pubCount, buf);
    } else {
        Serial.println("[PUB FAIL]");
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(LED_STATUS, OUTPUT);
    setupWiFi();
    mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
    mqttClient.setCallback(mqttCallback);
    Serial.println("=== ESP32 Sensor Node ===");
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) setupWiFi();
    if (!mqttClient.connected()) reconnectMQTT();
    mqttClient.loop();

    uint32_t now = millis();
    if (now - lastPub >= 2000) {   // Publish setiap 2 detik
        lastPub = now;
        publishData();
    }
}
