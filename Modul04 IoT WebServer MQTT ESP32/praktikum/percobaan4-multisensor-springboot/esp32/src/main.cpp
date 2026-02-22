#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ─── WiFi Credentials ────────────────────────────────────────────────────────
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ─── MQTT Broker ─────────────────────────────────────────────────────────────
#define MQTT_BROKER  "192.168.1.100"
#define MQTT_PORT    1883
#define MQTT_CLIENT  "ESP32-MultiSensor"

// ─── MQTT Topics ─────────────────────────────────────────────────────────────
#define TOPIC_DATA   "sensors/multi/data"
#define TOPIC_CONFIG "sensors/multi/config"

// ─── GPIO Pin Definitions ────────────────────────────────────────────────────
#define PIN_DHT          4      // DHT22 data pin
#define PIN_LDR         34      // LDR analog input
#define PIN_SOIL        35      // Soil moisture analog input
#define PIN_LED_BUILTIN  2      // Built-in LED

// ─── DHT22 ───────────────────────────────────────────────────────────────────
#define DHT_TYPE DHT22
DHT dht(PIN_DHT, DHT_TYPE);

// ─── ADC Reference Values (12-bit: 0-4095) ───────────────────────────────────
#define ADC_MAX        4095
// LDR: low ADC = bright (low resistance), high ADC = dark (high resistance)
// Soil: low ADC = wet, high ADC = dry

// ─── Publish Interval (ms) ────────────────────────────────────────────────────
unsigned long publishIntervalMs = 15000UL;
unsigned long lastPublishMs     = 0;

WiFiClient   wifiClient;
PubSubClient mqttClient(wifiClient);

// ─── Forward Declarations ────────────────────────────────────────────────────
void connectWiFi();
void connectMQTT();
void publishSensorData();
void blinkLED(int times, int delayMs);
void mqttCallback(char* topic, byte* payload, unsigned int length);

// ─── WiFi Connection ─────────────────────────────────────────────────────────
void connectWiFi() {
    Serial.printf("\n[WiFi] Connecting to %s", WIFI_SSID);
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.printf("\n[WiFi] Connected! IP: %s\n", WiFi.localIP().toString().c_str());
}

// ─── MQTT Connection ─────────────────────────────────────────────────────────
void connectMQTT() {
    mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
    mqttClient.setCallback(mqttCallback);

    while (!mqttClient.connected()) {
        Serial.printf("[MQTT] Connecting to %s:%d ...\n", MQTT_BROKER, MQTT_PORT);
        if (mqttClient.connect(MQTT_CLIENT)) {
            Serial.println("[MQTT] Connected!");
            mqttClient.subscribe(TOPIC_CONFIG);
            Serial.printf("[MQTT] Subscribed to: %s\n", TOPIC_CONFIG);
        } else {
            Serial.printf("[MQTT] Failed (state=%d). Retry in 3s...\n", mqttClient.state());
            delay(3000);
        }
    }
}

// ─── MQTT Callback: Handle Config Updates ────────────────────────────────────
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    String message;
    message.reserve(length);
    for (unsigned int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    Serial.printf("[MQTT] Config message: %s\n", message.c_str());

    StaticJsonDocument<128> doc;
    DeserializationError err = deserializeJson(doc, message);
    if (err) {
        Serial.printf("[JSON] Parse error: %s\n", err.c_str());
        return;
    }

    if (doc.containsKey("interval")) {
        unsigned long newInterval = doc["interval"].as<unsigned long>() * 1000UL;
        if (newInterval >= 5000UL && newInterval <= 300000UL) {
            publishIntervalMs = newInterval;
            Serial.printf("[CONFIG] Publish interval updated to %lu ms\n", publishIntervalMs);
        } else {
            Serial.println("[CONFIG] Interval out of range (5-300 seconds)");
        }
    }
}

// ─── Blink Built-in LED ──────────────────────────────────────────────────────
void blinkLED(int times, int delayMs) {
    for (int i = 0; i < times; i++) {
        digitalWrite(PIN_LED_BUILTIN, HIGH);
        delay(delayMs);
        digitalWrite(PIN_LED_BUILTIN, LOW);
        delay(delayMs);
    }
}

// ─── Read Sensors and Publish ────────────────────────────────────────────────
void publishSensorData() {
    // Read DHT22
    float temperature = dht.readTemperature();
    float humidity    = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("[DHT] Failed to read sensor! Using last values.");
        temperature = 25.0f;
        humidity    = 60.0f;
    }

    // Read LDR (GPIO34 - analog)
    int ldrRaw  = analogRead(PIN_LDR);
    // Invert: higher ADC = darker, map to 0-100% light level
    int light   = map(ADC_MAX - ldrRaw, 0, ADC_MAX, 0, 100);
    light = constrain(light, 0, 100);

    // Read Soil Moisture (GPIO35 - analog)
    int soilRaw      = analogRead(PIN_SOIL);
    // Higher ADC = dryer soil, invert for moisture percentage
    int soilMoisture = map(ADC_MAX - soilRaw, 0, ADC_MAX, 0, 100);
    soilMoisture = constrain(soilMoisture, 0, 100);

    // Estimate battery voltage from ADC pin (or use fixed value for demonstration)
    // In real deployment: use a voltage divider on an analog pin
    float battery = 3.7f;

    // Unix timestamp approximation (seconds since boot, not real epoch)
    unsigned long ts = millis() / 1000UL;

    // Build JSON
    StaticJsonDocument<256> doc;
    doc["device"]        = MQTT_CLIENT;
    doc["temperature"]   = serialized(String(temperature, 1));
    doc["humidity"]      = serialized(String(humidity,    1));
    doc["light"]         = light;
    doc["soil_moisture"] = soilMoisture;
    doc["battery"]       = serialized(String(battery,    1));
    doc["ts"]            = ts;

    char buffer[256];
    serializeJson(doc, buffer);

    if (mqttClient.publish(TOPIC_DATA, buffer, false)) {
        Serial.printf("[MQTT] Published: %s\n", buffer);
        blinkLED(1, 100);
    } else {
        Serial.println("[MQTT] Publish failed!");
    }
}

// ─── Setup ───────────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Percobaan 4: Multi-Sensor Dashboard ===");

    pinMode(PIN_LED_BUILTIN, OUTPUT);
    digitalWrite(PIN_LED_BUILTIN, LOW);

    // Configure ADC for 12-bit resolution
    analogReadResolution(12);
    analogSetAttenuation(ADC_11db);  // Full range 0-3.3V

    dht.begin();
    Serial.println("[DHT22] Sensor initialized on GPIO4");

    connectWiFi();
    connectMQTT();

    Serial.printf("[CONFIG] Publish interval: %lu ms\n", publishIntervalMs);

    // Initial blink to confirm ready
    blinkLED(3, 200);
}

// ─── Loop ─────────────────────────────────────────────────────────────────────
void loop() {
    if (!mqttClient.connected()) {
        Serial.println("[MQTT] Disconnected. Reconnecting...");
        connectMQTT();
    }
    mqttClient.loop();

    unsigned long now = millis();
    if (now - lastPublishMs >= publishIntervalMs) {
        lastPublishMs = now;
        publishSensorData();
    }
}
