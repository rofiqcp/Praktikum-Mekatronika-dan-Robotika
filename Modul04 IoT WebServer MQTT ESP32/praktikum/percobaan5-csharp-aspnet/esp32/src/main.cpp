/*
 * Percobaan 5: MQTT-HTTP Bridge
 * ESP32 membaca sensor LDR dan potensiometer, mempublikasikan data ke MQTT broker.
 * Menerima perintah brightness LED melalui topik MQTT.
 *
 * Hardware:
 *  - LDR     : GPIO34 (ADC1_CH6)
 *  - Pot     : GPIO35 (ADC1_CH7)
 *  - LED     : GPIO2  (PWM)
 *
 * MQTT Topics:
 *  - Publish : bridge/sensors/raw
 *  - Subscribe: bridge/led/control
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ─── Konfigurasi WiFi ─────────────────────────────────────────────────────────
const char* WIFI_SSID     = "NamaWiFi";
const char* WIFI_PASSWORD = "PasswordWiFi";

// ─── Konfigurasi MQTT ─────────────────────────────────────────────────────────
const char* MQTT_BROKER   = "192.168.1.100";
const int   MQTT_PORT     = 1883;
const char* MQTT_CLIENT   = "ESP32-BRIDGE-001";
const char* TOPIC_PUB     = "bridge/sensors/raw";
const char* TOPIC_SUB     = "bridge/led/control";

// ─── Pin Definitions ──────────────────────────────────────────────────────────
const int PIN_LDR   = 34;
const int PIN_POT   = 35;
const int PIN_LED   = 2;

// ─── PWM Konfigurasi ──────────────────────────────────────────────────────────
const int PWM_CHANNEL   = 0;
const int PWM_FREQ      = 5000;
const int PWM_RESOLUTION = 8;   // 8-bit → 0-255

// ─── Interval Publish ─────────────────────────────────────────────────────────
const unsigned long PUBLISH_INTERVAL_MS = 8000;
unsigned long lastPublishMs = 0;

WiFiClient   wifiClient;
PubSubClient mqttClient(wifiClient);

// ─── Callback pesan MQTT masuk ────────────────────────────────────────────────
void onMqttMessage(const char* topic, byte* payload, unsigned int length) {
    String topicStr(topic);
    String msg;
    msg.reserve(length);
    for (unsigned int i = 0; i < length; i++) {
        msg += (char)payload[i];
    }

    Serial.printf("[MQTT] Pesan diterima [%s]: %s\n", topic, msg.c_str());

    if (topicStr == TOPIC_SUB) {
        StaticJsonDocument<128> doc;
        DeserializationError err = deserializeJson(doc, msg);
        if (err) {
            Serial.printf("[MQTT] JSON parse error: %s\n", err.c_str());
            return;
        }
        int brightness = doc["brightness"] | 0;
        brightness = constrain(brightness, 0, 255);
        ledcWrite(PWM_CHANNEL, brightness);
        Serial.printf("[LED] Brightness diset ke %d\n", brightness);
    }
}

// ─── Koneksi WiFi ─────────────────────────────────────────────────────────────
void connectWiFi() {
    Serial.printf("\n[WiFi] Menghubungkan ke %s", WIFI_SSID);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.printf("\n[WiFi] Terhubung! IP: %s\n", WiFi.localIP().toString().c_str());
}

// ─── Koneksi MQTT ─────────────────────────────────────────────────────────────
void connectMqtt() {
    while (!mqttClient.connected()) {
        Serial.printf("[MQTT] Menghubungkan ke %s:%d ...\n", MQTT_BROKER, MQTT_PORT);
        if (mqttClient.connect(MQTT_CLIENT)) {
            Serial.println("[MQTT] Terhubung!");
            mqttClient.subscribe(TOPIC_SUB);
            Serial.printf("[MQTT] Subscribe ke topik: %s\n", TOPIC_SUB);
        } else {
            Serial.printf("[MQTT] Gagal (state=%d). Coba lagi 3s...\n", mqttClient.state());
            delay(3000);
        }
    }
}

// ─── Baca sensor dan publish ──────────────────────────────────────────────────
void publishSensorData() {
    int lightRaw = analogRead(PIN_LDR);
    int potRaw   = analogRead(PIN_POT);

    // Konversi ke persentase (ADC 12-bit → 0-4095)
    int lightPct = (int)((lightRaw / 4095.0f) * 100.0f);
    int potPct   = (int)((potRaw   / 4095.0f) * 100.0f);

    unsigned long uptimeSec = millis() / 1000;

    StaticJsonDocument<256> doc;
    doc["device"]    = "ESP32-BRIDGE";
    doc["light_raw"] = lightRaw;
    doc["light_pct"] = lightPct;
    doc["pot_raw"]   = potRaw;
    doc["pot_pct"]   = potPct;
    doc["uptime"]    = uptimeSec;

    char buf[256];
    size_t len = serializeJson(doc, buf);

    if (mqttClient.publish(TOPIC_PUB, buf, len)) {
        Serial.printf("[MQTT] Publish ke %s: %s\n", TOPIC_PUB, buf);
    } else {
        Serial.println("[MQTT] Publish gagal!");
    }
}

// ─── Setup ────────────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println("\n=== Percobaan 5: MQTT-HTTP Bridge ===");

    // Inisialisasi PWM LED
    ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
    ledcAttachPin(PIN_LED, PWM_CHANNEL);
    ledcWrite(PWM_CHANNEL, 0);

    // ADC pins (GPIO34, GPIO35 adalah input-only, tidak perlu pinMode)
    analogSetAttenuation(ADC_11db);   // rentang 0-3.3V

    connectWiFi();

    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    mqttClient.setCallback(onMqttMessage);
    mqttClient.setKeepAlive(60);
    mqttClient.setBufferSize(512);

    connectMqtt();
}

// ─── Loop ─────────────────────────────────────────────────────────────────────
void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        connectWiFi();
    }
    if (!mqttClient.connected()) {
        connectMqtt();
    }
    mqttClient.loop();

    unsigned long now = millis();
    if (now - lastPublishMs >= PUBLISH_INTERVAL_MS) {
        lastPublishMs = now;
        publishSensorData();
    }
}
