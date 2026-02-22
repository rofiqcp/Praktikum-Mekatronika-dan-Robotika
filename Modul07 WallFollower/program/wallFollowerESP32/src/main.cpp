/*
 * ============================================================
 * main.cpp – Wall Follower ESP32 + MPU-6050 + WiFi Config
 * Modul 07: Praktikum Mekatronika dan Robotika
 * Program Studi: Teknologi Rekayasa Otomasi
 *
 * Fitur:
 *  - 13 Percobaan: kalibrasi sensor, wall following (PID),
 *    left/right hand rule, line follower hybrid,
 *    adaptive setpoint, WiFi parameter config,
 *    MPU-6050 kalibrasi, gyro-assisted turn & straight,
 *    impact detection, tilt safety
 *  - ESP32 Access Point: setting parameter via browser
 *  - Dual-Core: Core 0 = sensor + IMU, Core 1 = kontrol + web
 *  - Parameter tersimpan di NVS (Preferences)
 *
 * Pin Assignment: lihat include/config.h
 * Library: electroniccats/MPU6050, ESPAsyncWebServer, ArduinoJson
 * ============================================================
 */

#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include <MPU6050.h>
#include "config.h"

// ============================================================
// STRUKTUR DATA
// ============================================================

struct SensorData {
    float distLeft;
    float distFront;
    float distRight;
    int   irLL, irLR, irRL, irRR;  // ADC values
    bool  lineLeft;
    bool  lineRight;
    // MPU-6050 data
    float accelX, accelY, accelZ;   // g
    float gyroX,  gyroY,  gyroZ;    // °/s
    float pitch, roll, yaw;          // complementary filter output (°)
    float temperature;               // °C (MPU onboard)
    bool  impactDetected;
    bool  tiltDetected;
};

struct RobotParams {
    float setpoint;
    int   baseSpeed;
    int   maxSpeed;
    float Kp, Ki, Kd;
    float KpLine;
    float KpHeading;
    uint8_t wallSide;  // 0 = kiri, 1 = kanan
};

// ============================================================
// OBJEK GLOBAL
// ============================================================

MPU6050          mpu;
AsyncWebServer   server(80);
Preferences      prefs;
SemaphoreHandle_t dataMutex;

SensorData   sensorData;
RobotParams  params;
RobotMode    currentMode = MODE_STOP;

// IMU kalibrasi offset
int16_t ax_off = 0, ay_off = 0, az_off = 0;
int16_t gx_off = 0, gy_off = 0, gz_off = 0;

// Complementary filter state
float compPitch = 0.0f, compRoll = 0.0f;
float integratedYaw = 0.0f;
unsigned long lastIMUTime = 0;

// PID state (wall distance)
float pidPrevError  = 0.0f;
float pidIntegral   = 0.0f;
unsigned long pidLastTime = 0;

// Task handles
TaskHandle_t sensorTaskHandle  = nullptr;
TaskHandle_t controlTaskHandle = nullptr;

// ============================================================
// DEKLARASI FUNGSI
// ============================================================

// Sensor
float  readUltrasonic(int trigPin, int echoPin);
void   readAllSensors();
void   setupMPU6050();
void   calibrateMPU6050();
void   readMPU6050();
void   updateComplementaryFilter();

// Motor
void   setupMotors();
void   setMotorSpeed(int speedA, int speedB);
void   motorStop();
void   motorForward(int speed);
void   motorBackward(int speed);
void   motorTurnLeft(int speed);
void   motorTurnRight(int speed);

// Kontrol
float  computePID(float actual);
RobotMode determineMode();
void   executeMode(RobotMode mode);
void   turnGyro(float targetDeg, bool clockwise);
void   moveForwardStraight(int baseSpeed, float targetHeading);

// WiFi & Web
void   setupWiFiAP();
void   setupWebServer();
void   loadParams();
void   saveParams();
String buildStatusJson();
String buildParamsJson();

// Utilitas
void   beep(int count, int durationMs = 80);
void   setLED(uint8_t mode);

// FreeRTOS Tasks
void   sensorTask(void* param);
void   controlTask(void* param);

// ============================================================
// SETUP
// ============================================================

void setup() {
    Serial.begin(115200);
    Serial.println("\n=== Wall Follower ESP32 + MPU-6050 ===");
    Serial.println("Modul 07 – Teknologi Rekayasa Otomasi");

    // LED & Buzzer
    pinMode(LED_R, OUTPUT);
    pinMode(LED_G, OUTPUT);
    pinMode(LED_B, OUTPUT);
    // LED_Y (GPIO17) removed – reassigned to TRIG_R
    pinMode(BUZZER, OUTPUT);
    pinMode(BTN_START, INPUT_PULLUP);
    pinMode(BTN_STOP,  INPUT);

    // Motor setup
    setupMotors();

    // Muat parameter dari NVS
    loadParams();

    // Inisialisasi MPU-6050
    setupMPU6050();

    // Mutex untuk shared data
    dataMutex = xSemaphoreCreateMutex();

    // WiFi AP + Web Server
    setupWiFiAP();
    setupWebServer();

    // Buat FreeRTOS tasks
    xTaskCreatePinnedToCore(sensorTask,  "SensorTask",  4096, nullptr, 2, &sensorTaskHandle,  0);
    xTaskCreatePinnedToCore(controlTask, "ControlTask", 8192, nullptr, 1, &controlTaskHandle, 1);

    beep(2);
    setLED(MODE_STOP);
    Serial.println("Setup selesai. Tekan BTN_START untuk mulai.");
}

void loop() {
    // Loop utama kosong – semua logika di FreeRTOS tasks
    vTaskDelay(pdMS_TO_TICKS(1000));
}

// ============================================================
// SENSOR TASK – Core 0
// ============================================================

void sensorTask(void* param) {
    while (true) {
        SensorData local;

        // Baca ultrasonik (aktifkan bergantian untuk hindari interferensi)
        local.distLeft  = readUltrasonic(TRIG_L, ECHO_L);
        vTaskDelay(pdMS_TO_TICKS(5));
        local.distFront = readUltrasonic(TRIG_F, ECHO_F);
        vTaskDelay(pdMS_TO_TICKS(5));
        local.distRight = readUltrasonic(TRIG_R, ECHO_R);

        // Baca IR line sensors
        local.irLL = analogRead(IR_LL);
        local.irLR = analogRead(IR_LR);
        local.irRL = analogRead(IR_RL);
        local.irRR = analogRead(IR_RR);
        local.lineLeft  = (local.irLL < LINE_DETECT_THRESH) ||
                          (local.irLR < LINE_DETECT_THRESH);
        local.lineRight = (local.irRL < LINE_DETECT_THRESH) ||
                          (local.irRR < LINE_DETECT_THRESH);

        // Baca MPU-6050
        if (mpu.testConnection()) {
            int16_t ax, ay, az, gx, gy, gz;
            mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

            // Terapkan offset kalibrasi
            ax -= ax_off; ay -= ay_off; az -= az_off;
            gx -= gx_off; gy -= gy_off; gz -= gz_off;

            local.accelX = ax / 16384.0f;
            local.accelY = ay / 16384.0f;
            local.accelZ = az / 16384.0f;
            local.gyroX  = gx / 131.0f;
            local.gyroY  = gy / 131.0f;
            local.gyroZ  = gz / 131.0f;
            local.temperature = mpu.getTemperature() / 340.0f + 36.53f;

            // Complementary filter
            unsigned long now = millis();
            float dt = (now - lastIMUTime) / 1000.0f;
            if (dt <= 0.0f || dt > 1.0f) dt = 0.02f;
            lastIMUTime = now;

            float accelPitch = atan2f(-local.accelX,
                sqrtf(local.accelY * local.accelY +
                      local.accelZ * local.accelZ)) * (180.0f / PI);
            float accelRoll = atan2f(local.accelY, local.accelZ) *
                              (180.0f / PI);

            compPitch = COMPLEMENTARY_ALPHA * (compPitch + local.gyroY * dt)
                        + (1.0f - COMPLEMENTARY_ALPHA) * accelPitch;
            compRoll  = COMPLEMENTARY_ALPHA * (compRoll  + local.gyroX * dt)
                        + (1.0f - COMPLEMENTARY_ALPHA) * accelRoll;
            integratedYaw += local.gyroZ * dt;

            local.pitch = compPitch;
            local.roll  = compRoll;
            local.yaw   = integratedYaw;

            // Deteksi benturan
            float totalAccel = sqrtf(local.accelX * local.accelX +
                                     local.accelY * local.accelY +
                                     local.accelZ * local.accelZ);
            local.impactDetected = (fabsf(totalAccel - 1.0f) > IMPACT_THRESHOLD);

            // Deteksi kemiringan berbahaya
            local.tiltDetected = (fabsf(compPitch) > TILT_THRESHOLD ||
                                  fabsf(compRoll)  > TILT_THRESHOLD);
        } else {
            local.accelX = local.accelY = local.accelZ = 0.0f;
            local.gyroX  = local.gyroY  = local.gyroZ  = 0.0f;
            local.pitch  = local.roll   = local.yaw     = 0.0f;
            local.temperature    = 0.0f;
            local.impactDetected = false;
            local.tiltDetected   = false;
        }

        // Salin ke shared data dengan mutex
        if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            sensorData = local;
            xSemaphoreGive(dataMutex);
        }

        vTaskDelay(pdMS_TO_TICKS(20));  // 50 Hz sampling
    }
}

// ============================================================
// CONTROL TASK – Core 1
// ============================================================

void controlTask(void* param) {
    static float targetHeading = 0.0f;
    static bool  running       = false;
    static unsigned long avoidTimer = 0;

    while (true) {
        // Cek tombol START/STOP
        if (digitalRead(BTN_START) == LOW) {
            vTaskDelay(pdMS_TO_TICKS(50));
            if (digitalRead(BTN_START) == LOW) {
                running = !running;
                if (running) {
                    targetHeading = sensorData.yaw;  // lock current heading
                    pidPrevError = 0.0f;
                    pidIntegral  = 0.0f;
                    pidLastTime  = millis();
                    beep(1);
                } else {
                    motorStop();
                    beep(2);
                }
                while (digitalRead(BTN_START) == LOW) vTaskDelay(pdMS_TO_TICKS(10));
            }
        }
        // BTN_STOP (GPIO36): external 10kΩ pull-down to GND; HIGH = pressed
        if (digitalRead(BTN_STOP) == HIGH) {
            running = false;
            motorStop();
        }

        if (!running) {
            motorStop();
            setLED(MODE_STOP);
            vTaskDelay(pdMS_TO_TICKS(50));
            continue;
        }

        // Salin sensor data
        SensorData sd;
        if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(10)) == pdTRUE) {
            sd = sensorData;
            xSemaphoreGive(dataMutex);
        }

        // --- Keamanan berbasis IMU ---
        if (sd.tiltDetected) {
            motorStop();
            setLED(MODE_STOP);
            beep(3, 200);
            Serial.println("[SAFETY] Tilt terdeteksi! Motor dihentikan.");
            vTaskDelay(pdMS_TO_TICKS(500));
            continue;
        }
        if (sd.impactDetected && currentMode != MODE_STOP) {
            motorStop();
            setLED(MODE_AVOID_OBSTACLE);
            Serial.println("[IMPACT] Benturan terdeteksi!");
            motorBackward(params.baseSpeed);
            vTaskDelay(pdMS_TO_TICKS(300));
            motorStop();
            vTaskDelay(pdMS_TO_TICKS(100));
            continue;
        }

        // --- Tentukan mode ---
        currentMode = determineMode();

        // --- Eksekusi mode ---
        switch (currentMode) {
        case MODE_STOP:
            motorStop();
            setLED(MODE_STOP);
            break;

        case MODE_LINE_FOLLOW: {
            // Line following sederhana dengan 4 sensor
            int leftVal  = (sd.irLL + sd.irLR) / 2;
            int rightVal = (sd.irRL + sd.irRR) / 2;
            int error    = leftVal - rightVal;
            int corr     = (int)(params.KpLine * error / 100);

            // Tambah koreksi heading dari gyro
            float headCorr = (int)(params.KpHeading *
                                   (targetHeading - sd.yaw));
            int sL = constrain(params.baseSpeed - corr + (int)headCorr,
                               -params.maxSpeed, params.maxSpeed);
            int sR = constrain(params.baseSpeed + corr - (int)headCorr,
                               -params.maxSpeed, params.maxSpeed);
            setMotorSpeed(sL, sR);
            setLED(MODE_LINE_FOLLOW);
            break;
        }

        case MODE_WALL_FOLLOW_L: {
            float corr = computePID(sd.distLeft);
            // Koreksi heading untuk jalan lurus
            float headCorr = params.KpHeading * (targetHeading - sd.yaw);
            int sL = constrain(params.baseSpeed - (int)corr + (int)headCorr,
                               -params.maxSpeed, params.maxSpeed);
            int sR = constrain(params.baseSpeed + (int)corr - (int)headCorr,
                               -params.maxSpeed, params.maxSpeed);
            setMotorSpeed(sL, sR);
            setLED(MODE_WALL_FOLLOW_L);
            break;
        }

        case MODE_WALL_FOLLOW_R: {
            float corr = computePID(sd.distRight);
            float headCorr = params.KpHeading * (targetHeading - sd.yaw);
            int sL = constrain(params.baseSpeed + (int)corr + (int)headCorr,
                               -params.maxSpeed, params.maxSpeed);
            int sR = constrain(params.baseSpeed - (int)corr - (int)headCorr,
                               -params.maxSpeed, params.maxSpeed);
            setMotorSpeed(sL, sR);
            setLED(MODE_WALL_FOLLOW_R);
            break;
        }

        case MODE_AVOID_OBSTACLE:
            // Obstacle depan: berhenti, mundur, belok
            motorStop();
            vTaskDelay(pdMS_TO_TICKS(200));
            motorBackward(params.baseSpeed);
            vTaskDelay(pdMS_TO_TICKS(400));
            // Belok berdasarkan sisi mana yang lebih lapang
            if (sd.distLeft >= sd.distRight) {
                turnGyro(85.0f, false);  // belok kiri
                targetHeading = sd.yaw;
            } else {
                turnGyro(85.0f, true);   // belok kanan
                targetHeading = sd.yaw;
            }
            break;

        case MODE_EXPLORE:
            // Putar perlahan mencari dinding
            motorTurnLeft(params.baseSpeed / 2);
            setLED(MODE_EXPLORE);
            break;

        default:
            motorStop();
            break;
        }

        // Serial output untuk plotter (CSV)
        Serial.print(sd.distLeft,  1); Serial.print(",");
        Serial.print(sd.distFront, 1); Serial.print(",");
        Serial.print(sd.distRight, 1); Serial.print(",");
        Serial.print(sd.yaw,       1); Serial.print(",");
        Serial.print(sd.pitch,     1); Serial.print(",");
        Serial.print(sd.roll,      1); Serial.print(",");
        Serial.println((int)currentMode);

        vTaskDelay(pdMS_TO_TICKS(20));  // 50 Hz control loop
    }
}

// ============================================================
// SENSOR FUNCTIONS
// ============================================================

float readUltrasonic(int trigPin, int echoPin) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    long dur = pulseIn(echoPin, HIGH, 30000UL);
    if (dur == 0) return 999.0f;
    return dur / 58.0f;
}

void setupMPU6050() {
    Wire.begin(MPU_SDA, MPU_SCL);
    Wire.setClock(400000);
    mpu.initialize();
    if (!mpu.testConnection()) {
        Serial.println("[MPU6050] Tidak terdeteksi! Cek wiring.");
        return;
    }
    mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);
    mpu.setFullScaleGyroRange(MPU6050_GYRO_FS_250);
    mpu.setDLPFMode(MPU6050_DLPF_BW_42);
    Serial.println("[MPU6050] OK – Alamat: 0x68");
    calibrateMPU6050();
}

void calibrateMPU6050() {
    Serial.println("[MPU6050] Kalibrasi – jangan gerakkan robot...");
    const int N = 200;
    int32_t sax=0, say=0, saz=0, sgx=0, sgy=0, sgz=0;
    for (int i = 0; i < N; i++) {
        int16_t ax, ay, az, gx, gy, gz;
        mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        sax+=ax; say+=ay; saz+=az;
        sgx+=gx; sgy+=gy; sgz+=gz;
        delay(5);
    }
    ax_off = sax/N; ay_off = say/N;
    az_off = saz/N - 16384;   // kompensasi 1g
    gx_off = sgx/N; gy_off = sgy/N; gz_off = sgz/N;
    Serial.printf("[MPU6050] Offset – ax:%d ay:%d az:%d gx:%d gy:%d gz:%d\n",
                  ax_off, ay_off, az_off, gx_off, gy_off, gz_off);
    lastIMUTime = millis();
}

// ============================================================
// MOTOR FUNCTIONS
// ============================================================

void setupMotors() {
    ledcSetup(CH_ENA, PWM_FREQ, PWM_BITS);
    ledcSetup(CH_ENB, PWM_FREQ, PWM_BITS);
    ledcAttachPin(PIN_ENA, CH_ENA);
    ledcAttachPin(PIN_ENB, CH_ENB);
    pinMode(PIN_IN1, OUTPUT); pinMode(PIN_IN2, OUTPUT);
    pinMode(PIN_IN3, OUTPUT); pinMode(PIN_IN4, OUTPUT);
    motorStop();
}

void setMotorSpeed(int speedA, int speedB) {
    // Motor A (kiri)
    if (speedA >= 0) {
        digitalWrite(PIN_IN1, HIGH); digitalWrite(PIN_IN2, LOW);
    } else {
        digitalWrite(PIN_IN1, LOW);  digitalWrite(PIN_IN2, HIGH);
        speedA = -speedA;
    }
    ledcWrite(CH_ENA, constrain(speedA, 0, 255));

    // Motor B (kanan)
    if (speedB >= 0) {
        digitalWrite(PIN_IN3, HIGH); digitalWrite(PIN_IN4, LOW);
    } else {
        digitalWrite(PIN_IN3, LOW);  digitalWrite(PIN_IN4, HIGH);
        speedB = -speedB;
    }
    ledcWrite(CH_ENB, constrain(speedB, 0, 255));
}

void motorStop()              { setMotorSpeed(0, 0); }
void motorForward(int s)      { setMotorSpeed(s, s); }
void motorBackward(int s)     { setMotorSpeed(-s, -s); }
void motorTurnLeft(int s)     { setMotorSpeed(-s, s); }
void motorTurnRight(int s)    { setMotorSpeed(s, -s); }

// ============================================================
// GYRO-ASSISTED TURN
// ============================================================

void turnGyro(float targetDeg, bool clockwise) {
    float startYaw = integratedYaw;
    float elapsed  = 0.0f;
    int   turnSpd  = params.baseSpeed;

    if (clockwise) motorTurnRight(turnSpd);
    else           motorTurnLeft(turnSpd);

    unsigned long t0 = millis();
    while (fabsf(elapsed) < (targetDeg - 3.0f)) {
        elapsed = fabsf(integratedYaw - startYaw);
        if (millis() - t0 > 5000) break;  // timeout 5 detik
        vTaskDelay(pdMS_TO_TICKS(5));
    }
    motorStop();
    Serial.printf("[TURN] target=%.1f° actual=%.1f°\n",
                  targetDeg, fabsf(integratedYaw - startYaw));
}

// ============================================================
// PID CONTROLLER
// ============================================================

float computePID(float actual) {
    unsigned long now = millis();
    float dt = (now - pidLastTime) / 1000.0f;
    if (dt <= 0.0f || dt > 1.0f) dt = 0.02f;
    pidLastTime = now;

    float error = params.setpoint - actual;

    float P = params.Kp * error;

    pidIntegral += error * dt;
    pidIntegral  = constrain(pidIntegral, -100.0f, 100.0f);
    float I = params.Ki * pidIntegral;

    float D = params.Kd * (error - pidPrevError) / dt;
    pidPrevError = error;

    return constrain(P + I + D, -(float)params.maxSpeed,
                                 (float)params.maxSpeed);
}

// ============================================================
// MODE DETERMINATION
// ============================================================

RobotMode determineMode() {
    SensorData sd;
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(5)) == pdTRUE) {
        sd = sensorData;
        xSemaphoreGive(dataMutex);
    }

    // Prioritas 1: Emergency stop
    if (sd.distFront < OBSTACLE_DIST_FRONT) return MODE_AVOID_OBSTACLE;

    // Prioritas 2: Line detected
    if (sd.lineLeft || sd.lineRight) return MODE_LINE_FOLLOW;

    // Prioritas 3: Wall detected sesuai sisi pilihan
    if (params.wallSide == 0 && sd.distLeft < WALL_DETECT_DIST)
        return MODE_WALL_FOLLOW_L;
    if (params.wallSide == 1 && sd.distRight < WALL_DETECT_DIST)
        return MODE_WALL_FOLLOW_R;

    // Fallback: coba temukan dinding di sisi manapun
    if (sd.distLeft < sd.distRight && sd.distLeft < WALL_DETECT_DIST)
        return MODE_WALL_FOLLOW_L;
    if (sd.distRight < WALL_DETECT_DIST)
        return MODE_WALL_FOLLOW_R;

    return MODE_EXPLORE;
}

// ============================================================
// WIFI ACCESS POINT
// ============================================================

void setupWiFiAP() {
    WiFi.mode(WIFI_AP);
    IPAddress apIP(192, 168, 4, 1);
    WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
    WiFi.softAP(WIFI_AP_SSID, WIFI_AP_PASS);
    Serial.printf("[WiFi] AP SSID: %s | IP: %s\n",
                  WIFI_AP_SSID, WiFi.softAPIP().toString().c_str());
}

// ============================================================
// WEB SERVER
// ============================================================

String buildStatusJson() {
    SensorData sd;
    if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(10)) == pdTRUE) {
        sd = sensorData;
        xSemaphoreGive(dataMutex);
    }
    JsonDocument doc;
    doc["dL"]     = sd.distLeft;
    doc["dF"]     = sd.distFront;
    doc["dR"]     = sd.distRight;
    doc["lineL"]  = sd.lineLeft;
    doc["lineR"]  = sd.lineRight;
    doc["yaw"]    = sd.yaw;
    doc["pitch"]  = sd.pitch;
    doc["roll"]   = sd.roll;
    doc["accelX"] = sd.accelX;
    doc["accelY"] = sd.accelY;
    doc["accelZ"] = sd.accelZ;
    doc["gyroZ"]  = sd.gyroZ;
    doc["temp"]   = sd.temperature;
    doc["impact"] = sd.impactDetected;
    doc["tilt"]   = sd.tiltDetected;
    doc["mode"]   = (int)currentMode;
    String out;
    serializeJson(doc, out);
    return out;
}

String buildParamsJson() {
    JsonDocument doc;
    doc["setpoint"]  = params.setpoint;
    doc["baseSpeed"] = params.baseSpeed;
    doc["maxSpeed"]  = params.maxSpeed;
    doc["Kp"]        = params.Kp;
    doc["Ki"]        = params.Ki;
    doc["Kd"]        = params.Kd;
    doc["KpLine"]    = params.KpLine;
    doc["KpHeading"] = params.KpHeading;
    doc["wallSide"]  = params.wallSide;
    String out;
    serializeJson(doc, out);
    return out;
}

// HTML halaman utama (inline)
static const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wall Follower ESP32</title>
<style>
  body{font-family:Arial,sans-serif;max-width:480px;margin:0 auto;padding:10px;background:#1a1a2e;color:#eee}
  h2{color:#e94560;text-align:center}
  .card{background:#16213e;border-radius:8px;padding:12px;margin:8px 0}
  .sensor-row{display:flex;justify-content:space-between;padding:4px 0}
  label{display:block;margin:6px 0 2px;font-size:13px;color:#aaa}
  input[type=range]{width:100%}
  input[type=number]{width:70px;background:#0f3460;color:#eee;border:1px solid #e94560;border-radius:4px;padding:2px 5px}
  .btn{background:#e94560;color:white;border:none;padding:10px 20px;border-radius:6px;cursor:pointer;margin:4px;font-size:15px}
  .btn-green{background:#27ae60}
  .btn-blue{background:#2980b9}
  select{background:#0f3460;color:#eee;padding:5px;border:1px solid #e94560;border-radius:4px}
  #modeLabel{font-size:20px;font-weight:bold;text-align:center;padding:8px}
  .imu-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;text-align:center;font-size:13px}
  .imu-val{background:#0f3460;border-radius:4px;padding:4px}
</style>
</head>
<body>
<h2>🤖 Wall Follower ESP32</h2>

<div class="card">
  <div id="modeLabel">Mode: --</div>
  <div class="sensor-row"><span>Kiri:</span><span id="dL">-</span> cm</div>
  <div class="sensor-row"><span>Depan:</span><span id="dF">-</span> cm</div>
  <div class="sensor-row"><span>Kanan:</span><span id="dR">-</span> cm</div>
</div>

<div class="card">
  <b>IMU MPU-6050</b>
  <div class="imu-grid">
    <div class="imu-val">Yaw<br><span id="iYaw">-</span>°</div>
    <div class="imu-val">Pitch<br><span id="iPitch">-</span>°</div>
    <div class="imu-val">Roll<br><span id="iRoll">-</span>°</div>
    <div class="imu-val">aX<br><span id="iAX">-</span>g</div>
    <div class="imu-val">aY<br><span id="iAY">-</span>g</div>
    <div class="imu-val">Temp<br><span id="iTemp">-</span>°C</div>
  </div>
  <div class="sensor-row" style="margin-top:6px">
    <span>Impact:</span><span id="impact" style="color:#e94560">-</span>
    <span style="margin-left:16px">Tilt:</span><span id="tilt" style="color:#e94560">-</span>
  </div>
</div>

<div class="card">
  <b>Parameter PID & Kontrol</b>
  <label>Setpoint (cm): <input type="number" id="pSetpoint" min="5" max="40" step="0.5"></label>
  <label>Base Speed: <input type="range" id="pBase" min="50" max="255" oninput="document.getElementById('vBase').textContent=this.value"> <span id="vBase">-</span></label>
  <label>Kp: <input type="number" id="pKp" min="0" max="20" step="0.1"></label>
  <label>Ki: <input type="number" id="pKi" min="0" max="2"  step="0.01"></label>
  <label>Kd: <input type="number" id="pKd" min="0" max="10" step="0.1"></label>
  <label>Kp Heading (Gyro): <input type="number" id="pKpH" min="0" max="10" step="0.1"></label>
  <label>Sisi Dinding:
    <select id="pSide">
      <option value="0">Kiri</option>
      <option value="1">Kanan</option>
    </select>
  </label>
  <button class="btn" onclick="saveParams()">💾 Simpan Parameter</button>
</div>

<div class="card" style="text-align:center">
  <button class="btn btn-green" onclick="sendControl('start')">▶ START</button>
  <button class="btn" onclick="sendControl('stop')">⏹ STOP</button>
  <button class="btn btn-blue" onclick="sendControl('calibrate_imu')">🔧 Kalibrasi IMU</button>
</div>

<script>
const modeNames = ["STOP","LINE","WALL-L","WALL-R","EXPLORE","AVOID","TURN-L","TURN-R","CALIB"];

function fetchStatus(){
  fetch('/status').then(r=>r.json()).then(d=>{
    document.getElementById('dL').textContent = d.dL.toFixed(1);
    document.getElementById('dF').textContent = d.dF.toFixed(1);
    document.getElementById('dR').textContent = d.dR.toFixed(1);
    document.getElementById('modeLabel').textContent = 'Mode: ' + (modeNames[d.mode]||d.mode);
    document.getElementById('iYaw').textContent   = d.yaw.toFixed(1);
    document.getElementById('iPitch').textContent = d.pitch.toFixed(1);
    document.getElementById('iRoll').textContent  = d.roll.toFixed(1);
    document.getElementById('iAX').textContent    = d.accelX.toFixed(2);
    document.getElementById('iAY').textContent    = d.accelY.toFixed(2);
    document.getElementById('iTemp').textContent  = d.temp.toFixed(1);
    document.getElementById('impact').textContent = d.impact ? '⚠ YA' : 'Tidak';
    document.getElementById('tilt').textContent   = d.tilt   ? '⚠ YA' : 'Tidak';
  }).catch(()=>{});
}

function fetchParams(){
  fetch('/params').then(r=>r.json()).then(d=>{
    document.getElementById('pSetpoint').value = d.setpoint;
    document.getElementById('pBase').value     = d.baseSpeed;
    document.getElementById('vBase').textContent = d.baseSpeed;
    document.getElementById('pKp').value       = d.Kp;
    document.getElementById('pKi').value       = d.Ki;
    document.getElementById('pKd').value       = d.Kd;
    document.getElementById('pKpH').value      = d.KpHeading;
    document.getElementById('pSide').value     = d.wallSide;
  }).catch(()=>{});
}

function saveParams(){
  const body = JSON.stringify({
    setpoint:   parseFloat(document.getElementById('pSetpoint').value),
    baseSpeed:  parseInt(document.getElementById('pBase').value),
    Kp:         parseFloat(document.getElementById('pKp').value),
    Ki:         parseFloat(document.getElementById('pKi').value),
    Kd:         parseFloat(document.getElementById('pKd').value),
    KpHeading:  parseFloat(document.getElementById('pKpH').value),
    wallSide:   parseInt(document.getElementById('pSide').value)
  });
  fetch('/params',{method:'POST',headers:{'Content-Type':'application/json'},body})
    .then(r=>r.json()).then(d=>alert(d.status==='ok'?'✅ Parameter tersimpan!':'❌ Gagal'));
}

function sendControl(action){
  fetch('/control',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({action})}).catch(()=>{});
}

fetchParams();
setInterval(fetchStatus, 300);
</script>
</body>
</html>
)rawliteral";

void setupWebServer() {
    // Halaman utama
    server.on("/", HTTP_GET, [](AsyncWebServerRequest* req) {
        req->send_P(200, "text/html", INDEX_HTML);
    });

    // Status sensor (JSON)
    server.on("/status", HTTP_GET, [](AsyncWebServerRequest* req) {
        req->send(200, "application/json", buildStatusJson());
    });

    // GET parameter
    server.on("/params", HTTP_GET, [](AsyncWebServerRequest* req) {
        req->send(200, "application/json", buildParamsJson());
    });

    // POST parameter
    server.on("/params", HTTP_POST, [](AsyncWebServerRequest* req) {},
              nullptr,
              [](AsyncWebServerRequest* req, uint8_t* data, size_t len,
                 size_t, size_t) {
        JsonDocument doc;
        if (deserializeJson(doc, data, len) != DeserializationError::Ok) {
            req->send(400, "application/json", "{\"status\":\"bad json\"}");
            return;
        }
        if (doc["setpoint"].is<float>())
            params.setpoint  = doc["setpoint"].as<float>();
        if (doc["baseSpeed"].is<int>())
            params.baseSpeed = doc["baseSpeed"].as<int>();
        if (doc["Kp"].is<float>())       params.Kp       = doc["Kp"].as<float>();
        if (doc["Ki"].is<float>())       params.Ki       = doc["Ki"].as<float>();
        if (doc["Kd"].is<float>())       params.Kd       = doc["Kd"].as<float>();
        if (doc["KpHeading"].is<float>())params.KpHeading= doc["KpHeading"].as<float>();
        if (doc["wallSide"].is<int>())   params.wallSide = doc["wallSide"].as<int>();
        saveParams();
        // Reset PID integral setelah parameter diubah
        pidIntegral  = 0.0f;
        pidPrevError = 0.0f;
        req->send(200, "application/json", "{\"status\":\"ok\"}");
    });

    // POST kontrol robot
    server.on("/control", HTTP_POST, [](AsyncWebServerRequest* req) {},
              nullptr,
              [](AsyncWebServerRequest* req, uint8_t* data, size_t len,
                 size_t, size_t) {
        JsonDocument doc;
        if (deserializeJson(doc, data, len) != DeserializationError::Ok) {
            req->send(400, "application/json", "{\"status\":\"bad json\"}");
            return;
        }
        String action = doc["action"].as<String>();
        if (action == "stop")  {
            currentMode = MODE_STOP; motorStop();
        } else if (action == "calibrate_imu") {
            currentMode = MODE_CALIBRATE_IMU;
            calibrateMPU6050();
            currentMode = MODE_STOP;
        }
        req->send(200, "application/json", "{\"status\":\"ok\"}");
    });

    // 404 handler
    server.onNotFound([](AsyncWebServerRequest* req) {
        req->send(404, "text/plain", "Not found");
    });

    server.begin();
    Serial.println("[WebServer] Berjalan di http://192.168.4.1");
}

// ============================================================
// PREFERENCES (NVS)
// ============================================================

void loadParams() {
    prefs.begin(NVS_NAMESPACE, true);
    params.setpoint   = prefs.getFloat(KEY_SETPOINT, DEFAULT_SETPOINT);
    params.baseSpeed  = prefs.getInt  (KEY_BASE_SPD, DEFAULT_BASE_SPEED);
    params.maxSpeed   = prefs.getInt  (KEY_MAX_SPD,  DEFAULT_MAX_SPEED);
    params.Kp         = prefs.getFloat(KEY_KP,       DEFAULT_KP);
    params.Ki         = prefs.getFloat(KEY_KI,       DEFAULT_KI);
    params.Kd         = prefs.getFloat(KEY_KD,       DEFAULT_KD);
    params.KpLine     = prefs.getFloat(KEY_KP_LINE,  DEFAULT_KP_LINE);
    params.KpHeading  = prefs.getFloat(KEY_KP_HEAD,  DEFAULT_KP_HEADING);
    params.wallSide   = prefs.getUChar(KEY_WALL_SIDE, 0);
    prefs.end();
    Serial.printf("[Params] Setpoint=%.1f Kp=%.2f Ki=%.3f Kd=%.2f Side=%s\n",
                  params.setpoint, params.Kp, params.Ki, params.Kd,
                  params.wallSide == 0 ? "KIRI" : "KANAN");
}

void saveParams() {
    prefs.begin(NVS_NAMESPACE, false);
    prefs.putFloat(KEY_SETPOINT, params.setpoint);
    prefs.putInt  (KEY_BASE_SPD, params.baseSpeed);
    prefs.putInt  (KEY_MAX_SPD,  params.maxSpeed);
    prefs.putFloat(KEY_KP,       params.Kp);
    prefs.putFloat(KEY_KI,       params.Ki);
    prefs.putFloat(KEY_KD,       params.Kd);
    prefs.putFloat(KEY_KP_LINE,  params.KpLine);
    prefs.putFloat(KEY_KP_HEAD,  params.KpHeading);
    prefs.putUChar(KEY_WALL_SIDE,params.wallSide);
    prefs.end();
    Serial.println("[Params] Tersimpan ke NVS.");
}

// ============================================================
// UTILITAS
// ============================================================

void beep(int count, int durationMs) {
    for (int i = 0; i < count; i++) {
        digitalWrite(BUZZER, HIGH);
        delay(durationMs);
        digitalWrite(BUZZER, LOW);
        if (i < count - 1) delay(100);
    }
}

void setLED(uint8_t mode) {
    digitalWrite(LED_R, mode == MODE_STOP          ? HIGH : LOW);
    digitalWrite(LED_G, mode == MODE_LINE_FOLLOW   ? HIGH : LOW);
    digitalWrite(LED_B, (mode == MODE_WALL_FOLLOW_L ||
                         mode == MODE_WALL_FOLLOW_R) ? HIGH : LOW);
    // LED_Y removed (GPIO17 = TRIG_R). Right-wall mode: LED_B + buzzer short beep.
}
