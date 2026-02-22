/*
 * Percobaan 6: Real-Time Dashboard
 * ESP32 membaca DHT22, MQ-2 gas sensor, dan PIR motion sensor.
 * Mengirim data secara periodik dan alert motion secara langsung.
 *
 * Hardware:
 *  - DHT22   : GPIO4
 *  - MQ-2    : GPIO36 (ADC1_CH0) – analog output
 *  - PIR     : GPIO14 – digital output
 *  - LED     : GPIO2  – indikator bahaya/gerak
 *
 * MQTT Topics:
 *  - Publish data  : realtime/sensors/data
 *  - Publish alert : realtime/alerts/motion
 *  - Publish LED   : (internal logic only)
 */

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ─── Konfigurasi WiFi ─────────────────────────────────────────────────────────
const char* WIFI_SSID     = "NamaWiFi";
const char* WIFI_PASSWORD = "PasswordWiFi";

// ─── Konfigurasi MQTT ─────────────────────────────────────────────────────────
const char* MQTT_BROKER      = "192.168.1.100";
const int   MQTT_PORT        = 1883;
const char* MQTT_CLIENT      = "ESP32-RT-001";
const char* TOPIC_SENSOR     = "realtime/sensors/data";
const char* TOPIC_MOTION     = "realtime/alerts/motion";

// ─── Pin Definitions ──────────────────────────────────────────────────────────
const int PIN_DHT  = 4;
const int PIN_MQ2  = 36;
const int PIN_PIR  = 14;
const int PIN_LED  = 2;

// ─── DHT22 ───────────────────────────────────────────────────────────────────
#define DHT_TYPE DHT22
DHT dht(PIN_DHT, DHT_TYPE);

// ─── MQ-2 Kalibrasi sederhana (PPM estimasi linier) ───────────────────────────
// ADC 12-bit (0-4095) → 0-1000 ppm (kalibrasi kasar untuk praktikum)
float adcToPpm(int raw) {
    return raw * (1000.0f / 4095.0f);
}

// ─── PWM LED ──────────────────────────────────────────────────────────────────
const int PWM_CHANNEL    = 0;
const int PWM_FREQ       = 1000;
const int PWM_RESOLUTION = 8;

// ─── State ───────────────────────────────────────────────────────────────────
const unsigned long PUBLISH_INTERVAL_MS = 5000;
unsigned long lastPublishMs = 0;

bool lastPirState  = false;
bool dangerMode    = false;    // gas > 400 ppm
bool motionMode    = false;    // gerak terdeteksi

unsigned long lastLedToggleMs = 0;
bool          ledState        = false;

WiFiClient   wifiClient;
PubSubClient mqttClient(wifiClient);

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
        } else {
            Serial.printf("[MQTT] Gagal (state=%d). Retry 3s...\n", mqttClient.state());
            delay(3000);
        }
    }
}

// ─── Publish data sensor periodik ────────────────────────────────────────────
void publishSensorData() {
    float temp = dht.readTemperature();
    float hum  = dht.readHumidity();

    if (isnan(temp) || isnan(hum)) {
        Serial.println("[DHT22] Gagal membaca sensor!");
        temp = 0.0f;
        hum  = 0.0f;
    }

    int   gasRaw  = analogRead(PIN_MQ2);
    float gasPpm  = adcToPpm(gasRaw);
    bool  pirVal  = digitalRead(PIN_PIR);

    dangerMode = (gasPpm > 400.0f);
    motionMode = pirVal;

    unsigned long uptimeSec = millis() / 1000;

    StaticJsonDocument<256> doc;
    doc["device"]      = "ESP32-RT";
    doc["temperature"] = serialized(String(temp, 1));
    doc["humidity"]    = serialized(String(hum, 1));
    doc["gas_level"]   = gasRaw;
    doc["gas_ppm"]     = serialized(String(gasPpm, 1));
    doc["motion"]      = pirVal;
    doc["uptime"]      = uptimeSec;

    char buf[256];
    size_t len = serializeJson(doc, buf);

    if (mqttClient.publish(TOPIC_SENSOR, buf, len)) {
        Serial.printf("[MQTT] Publish data: %s\n", buf);
    } else {
        Serial.println("[MQTT] Publish data gagal!");
    }
}

// ─── Publish alert gerakan ────────────────────────────────────────────────────
void publishMotionAlert() {
    unsigned long ts = millis() / 1000;

    StaticJsonDocument<128> doc;
    doc["device"] = "ESP32-RT";
    doc["alert"]  = "motion_detected";
    doc["ts"]     = ts;

    char buf[128];
    size_t len = serializeJson(doc, buf);

    if (mqttClient.publish(TOPIC_MOTION, buf, len)) {
        Serial.printf("[MQTT] Alert motion: %s\n", buf);
    }
}

// ─── Update LED indikator ─────────────────────────────────────────────────────
void updateLed() {
    unsigned long now = millis();
    unsigned long interval = dangerMode ? 200 : (motionMode ? 800 : 0);

    if (interval == 0) {
        ledcWrite(PWM_CHANNEL, 0);
        ledState = false;
        return;
    }

    if (now - lastLedToggleMs >= interval) {
        lastLedToggleMs = now;
        ledState = !ledState;
        ledcWrite(PWM_CHANNEL, ledState ? 255 : 0);
    }
}

// ─── Setup ────────────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    delay(500);
    Serial.println("\n=== Percobaan 6: Real-Time Dashboard ===");

    dht.begin();

    pinMode(PIN_PIR, INPUT);
    analogSetAttenuation(ADC_11db);

    ledcSetup(PWM_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
    ledcAttachPin(PIN_LED, PWM_CHANNEL);
    ledcWrite(PWM_CHANNEL, 0);

    connectWiFi();

    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
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

    // Publish periodik
    unsigned long now = millis();
    if (now - lastPublishMs >= PUBLISH_INTERVAL_MS) {
        lastPublishMs = now;
        publishSensorData();
    }

    // Deteksi rising edge PIR → alert langsung
    bool pirNow = digitalRead(PIN_PIR);
    if (pirNow && !lastPirState) {
        publishMotionAlert();
    }
    lastPirState = pirNow;

    updateLed();
    delay(10);
}
