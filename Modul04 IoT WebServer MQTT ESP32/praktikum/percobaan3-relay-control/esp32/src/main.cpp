#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ─── WiFi Credentials ────────────────────────────────────────────────────────
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// ─── MQTT Broker ─────────────────────────────────────────────────────────────
#define MQTT_BROKER   "192.168.1.100"
#define MQTT_PORT     1883
#define MQTT_CLIENT   "ESP32-RelayControl"

// ─── MQTT Topics ─────────────────────────────────────────────────────────────
#define TOPIC_RELAY_SET    "control/relay/set"
#define TOPIC_RELAY_STATUS "control/relay/status"
#define TOPIC_ALL_OFF      "control/all/off"

// ─── GPIO Pin Definitions ────────────────────────────────────────────────────
#define PIN_RELAY1  26
#define PIN_RELAY2  27
#define PIN_LED1     2
#define PIN_LED2     4

// ─── Timing ──────────────────────────────────────────────────────────────────
#define STATUS_INTERVAL_MS  2000UL

// ─── State ───────────────────────────────────────────────────────────────────
bool relay1State = false;
bool relay2State = false;
bool led1State   = false;
bool led2State   = false;

unsigned long lastStatusMs = 0;

WiFiClient   wifiClient;
PubSubClient mqttClient(wifiClient);

// ─── Forward Declarations ────────────────────────────────────────────────────
void connectWiFi();
void connectMQTT();
void publishStatus();
void turnAllOff();
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
        Serial.printf("[MQTT] Connecting to broker %s:%d ...\n", MQTT_BROKER, MQTT_PORT);
        if (mqttClient.connect(MQTT_CLIENT)) {
            Serial.println("[MQTT] Connected!");
            mqttClient.subscribe(TOPIC_RELAY_SET);
            mqttClient.subscribe(TOPIC_ALL_OFF);
            Serial.printf("[MQTT] Subscribed to: %s, %s\n", TOPIC_RELAY_SET, TOPIC_ALL_OFF);
        } else {
            Serial.printf("[MQTT] Failed (state=%d). Retry in 3s...\n", mqttClient.state());
            delay(3000);
        }
    }
}

// ─── MQTT Callback ───────────────────────────────────────────────────────────
void mqttCallback(char* topic, byte* payload, unsigned int length) {
    String topicStr(topic);
    String message;
    message.reserve(length);
    for (unsigned int i = 0; i < length; i++) {
        message += (char)payload[i];
    }

    Serial.printf("[MQTT] Message on [%s]: %s\n", topic, message.c_str());

    // ── Handle "all off" command ──────────────────────────────────────────────
    if (topicStr == TOPIC_ALL_OFF) {
        turnAllOff();
        return;
    }

    // ── Handle relay/led set command ─────────────────────────────────────────
    if (topicStr == TOPIC_RELAY_SET) {
        StaticJsonDocument<128> doc;
        DeserializationError err = deserializeJson(doc, message);
        if (err) {
            Serial.printf("[JSON] Parse error: %s\n", err.c_str());
            return;
        }

        if (!doc.containsKey("relay") || !doc.containsKey("state")) {
            Serial.println("[JSON] Missing 'relay' or 'state' key");
            return;
        }

        int  relayNum = doc["relay"].as<int>();
        bool newState = (strcmp(doc["state"].as<const char*>(), "ON") == 0);

        switch (relayNum) {
            case 1:
                relay1State = newState;
                digitalWrite(PIN_RELAY1, relay1State ? HIGH : LOW);
                Serial.printf("[CTRL] Relay1 -> %s\n", relay1State ? "ON" : "OFF");
                break;
            case 2:
                relay2State = newState;
                digitalWrite(PIN_RELAY2, relay2State ? HIGH : LOW);
                Serial.printf("[CTRL] Relay2 -> %s\n", relay2State ? "ON" : "OFF");
                break;
            case 3:
                led1State = newState;
                digitalWrite(PIN_LED1, led1State ? HIGH : LOW);
                Serial.printf("[CTRL] LED1   -> %s\n", led1State ? "ON" : "OFF");
                break;
            case 4:
                led2State = newState;
                digitalWrite(PIN_LED2, led2State ? HIGH : LOW);
                Serial.printf("[CTRL] LED2   -> %s\n", led2State ? "ON" : "OFF");
                break;
            default:
                Serial.printf("[CTRL] Unknown device number: %d\n", relayNum);
                break;
        }

        publishStatus();
    }
}

// ─── Turn Everything Off ─────────────────────────────────────────────────────
void turnAllOff() {
    relay1State = false;
    relay2State = false;
    led1State   = false;
    led2State   = false;

    digitalWrite(PIN_RELAY1, LOW);
    digitalWrite(PIN_RELAY2, LOW);
    digitalWrite(PIN_LED1,   LOW);
    digitalWrite(PIN_LED2,   LOW);

    Serial.println("[CTRL] All outputs turned OFF");
    publishStatus();
}

// ─── Publish Status ───────────────────────────────────────────────────────────
void publishStatus() {
    StaticJsonDocument<192> doc;
    doc["relay1"]  = relay1State ? "ON" : "OFF";
    doc["relay2"]  = relay2State ? "ON" : "OFF";
    doc["led1"]    = led1State   ? "ON" : "OFF";
    doc["led2"]    = led2State   ? "ON" : "OFF";
    doc["uptime"]  = millis() / 1000UL;

    char buffer[192];
    serializeJson(doc, buffer);
    mqttClient.publish(TOPIC_RELAY_STATUS, buffer, true);
    Serial.printf("[MQTT] Published status: %s\n", buffer);
}

// ─── Setup ───────────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Percobaan 3: Remote Relay/LED Control via MQTT ===");

    pinMode(PIN_RELAY1, OUTPUT);
    pinMode(PIN_RELAY2, OUTPUT);
    pinMode(PIN_LED1,   OUTPUT);
    pinMode(PIN_LED2,   OUTPUT);

    digitalWrite(PIN_RELAY1, LOW);
    digitalWrite(PIN_RELAY2, LOW);
    digitalWrite(PIN_LED1,   LOW);
    digitalWrite(PIN_LED2,   LOW);

    connectWiFi();
    connectMQTT();
    publishStatus();
}

// ─── Loop ─────────────────────────────────────────────────────────────────────
void loop() {
    if (!mqttClient.connected()) {
        Serial.println("[MQTT] Disconnected. Reconnecting...");
        connectMQTT();
    }
    mqttClient.loop();

    unsigned long now = millis();
    if (now - lastStatusMs >= STATUS_INTERVAL_MS) {
        lastStatusMs = now;
        publishStatus();
    }
}
