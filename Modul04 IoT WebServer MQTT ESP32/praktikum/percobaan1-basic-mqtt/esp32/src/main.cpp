#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ─── WiFi & MQTT configuration ────────────────────────────────────────────────
#define WIFI_SSID       "YOUR_WIFI_SSID"
#define WIFI_PASSWORD   "YOUR_WIFI_PASSWORD"
#define MQTT_BROKER_IP  "192.168.1.100"
#define MQTT_BROKER_PORT 1883
#define MQTT_CLIENT_ID  "ESP32-01"

// ─── MQTT Topics ──────────────────────────────────────────────────────────────
#define TOPIC_PUBLISH   "praktikum/esp32/hello"
#define TOPIC_SUBSCRIBE "praktikum/esp32/command"

// ─── Timing ───────────────────────────────────────────────────────────────────
#define PUBLISH_INTERVAL_MS 5000

WiFiClient   espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublishMs = 0;
int           msgCounter    = 0;

// ─── WiFi ─────────────────────────────────────────────────────────────────────
void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.printf("\n[WiFi] Connecting to %s", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startMs = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startMs > 15000) {
      Serial.println("\n[WiFi] Timeout – retrying later");
      return;
    }
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\n[WiFi] Connected. IP: %s\n", WiFi.localIP().toString().c_str());
}

// ─── MQTT callback ────────────────────────────────────────────────────────────
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
  Serial.printf("[MQTT] Received on '%s': %s\n", topic, msg.c_str());
}

// ─── MQTT connect / reconnect ─────────────────────────────────────────────────
void connectMQTT() {
  if (mqttClient.connected()) return;
  if (WiFi.status() != WL_CONNECTED) return;

  Serial.printf("[MQTT] Connecting to %s:%d … ", MQTT_BROKER_IP, MQTT_BROKER_PORT);

  if (mqttClient.connect(MQTT_CLIENT_ID)) {
    Serial.println("connected.");
    mqttClient.subscribe(TOPIC_SUBSCRIBE);
    Serial.printf("[MQTT] Subscribed to '%s'\n", TOPIC_SUBSCRIBE);
  } else {
    Serial.printf("failed (rc=%d). Will retry.\n", mqttClient.state());
  }
}

// ─── Publish sensor payload ───────────────────────────────────────────────────
void publishHello() {
  if (!mqttClient.connected()) return;

  msgCounter++;

  StaticJsonDocument<200> doc;
  doc["device"]  = MQTT_CLIENT_ID;
  doc["uptime"]  = millis() / 1000;
  doc["counter"] = msgCounter;
  doc["message"] = "Hello from ESP32";

  char buffer[200];
  size_t len = serializeJson(doc, buffer);

  bool ok = mqttClient.publish(TOPIC_PUBLISH, buffer, len);
  Serial.printf("[MQTT] Published to '%s': %s [%s]\n",
                TOPIC_PUBLISH, buffer, ok ? "OK" : "FAIL");
}

// ─── Arduino entry points ─────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial.println("\n=== Percobaan 1: Basic MQTT Publisher/Subscriber ===");

  mqttClient.setServer(MQTT_BROKER_IP, MQTT_BROKER_PORT);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setKeepAlive(60);

  connectWiFi();
  connectMQTT();
}

void loop() {
  // Maintain connections
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }
  if (!mqttClient.connected()) {
    connectMQTT();
  }

  mqttClient.loop();

  // Publish every PUBLISH_INTERVAL_MS
  unsigned long now = millis();
  if (now - lastPublishMs >= PUBLISH_INTERVAL_MS) {
    lastPublishMs = now;
    publishHello();
  }
}
