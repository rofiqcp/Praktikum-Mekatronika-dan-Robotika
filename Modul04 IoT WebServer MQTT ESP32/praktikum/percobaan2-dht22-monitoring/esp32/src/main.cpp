#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ─── Configuration ────────────────────────────────────────────────────────────
#define WIFI_SSID        "YOUR_WIFI_SSID"
#define WIFI_PASSWORD    "YOUR_WIFI_PASSWORD"
#define MQTT_BROKER_IP   "192.168.1.100"
#define MQTT_BROKER_PORT 1883
#define MQTT_CLIENT_ID   "ESP32-DHT22"

// ─── Hardware pins ────────────────────────────────────────────────────────────
#define DHT_PIN          4      // GPIO4 – DATA pin of DHT22
#define DHT_TYPE         DHT22
#define LED_PIN          2      // Built-in LED (active HIGH on most ESP32 boards)

// ─── MQTT Topics ──────────────────────────────────────────────────────────────
#define TOPIC_SENSOR     "sensor/dht22/data"
#define TOPIC_LED        "sensor/dht22/led"

// ─── Timing ───────────────────────────────────────────────────────────────────
#define PUBLISH_INTERVAL_MS 10000UL

DHT          dht(DHT_PIN, DHT_TYPE);
WiFiClient   espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublishMs = 0;
bool          ledState      = false;

// ─── WiFi ─────────────────────────────────────────────────────────────────────
void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  Serial.printf("\n[WiFi] Connecting to %s", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  unsigned long startMs = millis();
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startMs > 20000UL) {
      Serial.println("\n[WiFi] Timeout – will retry.");
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
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];

  Serial.printf("[MQTT] Received on '%s': %s\n", topic, msg.c_str());

  // Toggle LED on "sensor/dht22/led"
  if (String(topic) == TOPIC_LED) {
    if (msg == "ON" || msg == "on" || msg == "1") {
      ledState = true;
    } else if (msg == "OFF" || msg == "off" || msg == "0") {
      ledState = false;
    } else {
      ledState = !ledState;   // any other message toggles
    }
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
    Serial.printf("[LED] State → %s\n", ledState ? "ON" : "OFF");
  }
}

// ─── MQTT connect / reconnect ─────────────────────────────────────────────────
void connectMQTT() {
  if (mqttClient.connected()) return;
  if (WiFi.status() != WL_CONNECTED) return;

  Serial.printf("[MQTT] Connecting to %s:%d … ", MQTT_BROKER_IP, MQTT_BROKER_PORT);

  if (mqttClient.connect(MQTT_CLIENT_ID)) {
    Serial.println("connected.");
    mqttClient.subscribe(TOPIC_LED);
    Serial.printf("[MQTT] Subscribed to '%s'\n", TOPIC_LED);
  } else {
    Serial.printf("failed (rc=%d). Will retry.\n", mqttClient.state());
  }
}

// ─── Read DHT22 and publish ───────────────────────────────────────────────────
void readAndPublish() {
  float temperature = dht.readTemperature();
  float humidity    = dht.readHumidity();

  // Check for NaN (sensor read failure)
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("[DHT22] Read failed – skipping publish.");
    return;
  }

  float heatIndex = dht.computeHeatIndex(temperature, humidity, false);

  StaticJsonDocument<256> doc;
  doc["device"]      = MQTT_CLIENT_ID;
  doc["temperature"] = serialized(String(temperature, 1));
  doc["humidity"]    = serialized(String(humidity,    1));
  doc["heat_index"]  = serialized(String(heatIndex,   1));
  doc["ts"]          = millis() / 1000;

  char buffer[256];
  size_t len = serializeJson(doc, buffer);

  bool ok = mqttClient.publish(TOPIC_SENSOR, buffer, len);
  Serial.printf("[MQTT] Published → T=%.1f°C  H=%.1f%%  HI=%.1f°C  [%s]\n",
                temperature, humidity, heatIndex, ok ? "OK" : "FAIL");
}

// ─── Arduino entry points ─────────────────────────────────────────────────────
void setup() {
  Serial.begin(115200);
  Serial.println("\n=== Percobaan 2: DHT22 Sensor Monitoring ===");

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  dht.begin();
  delay(2000);   // DHT22 needs 2 s after power-on

  mqttClient.setServer(MQTT_BROKER_IP, MQTT_BROKER_PORT);
  mqttClient.setCallback(mqttCallback);
  mqttClient.setKeepAlive(60);

  connectWiFi();
  connectMQTT();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqttClient.connected())        connectMQTT();

  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublishMs >= PUBLISH_INTERVAL_MS) {
    lastPublishMs = now;
    readAndPublish();
  }
}
