/*
 * ============================================================
 * config.h – Konfigurasi Pin dan Parameter Default
 * Modul 07: Wall Follower ESP32 + MPU-6050
 * Program Studi: Teknologi Rekayasa Otomasi
 * ============================================================
 */
#pragma once

// ---- Pin HC-SR04 Ultrasonik --------------------------------
#define TRIG_L   5   // HC-SR04 Kiri  – TRIG
#define ECHO_L  18   // HC-SR04 Kiri  – ECHO (via voltage divider)
#define TRIG_F  19   // HC-SR04 Depan – TRIG
#define ECHO_F  39   // HC-SR04 Depan – ECHO (input-only GPIO, via voltage divider)
#define TRIG_R  17   // HC-SR04 Kanan – TRIG (moved from GPIO22 to free MPU_SCL)
#define ECHO_R  23   // HC-SR04 Kanan – ECHO (via voltage divider)

// ---- Pin Sensor IR Line ------------------------------------
#define IR_LL   34   // IR Line Kiri-Luar  (ADC1, input only)
#define IR_LR   35   // IR Line Kiri-Dalam (ADC1, input only)
#define IR_RL   32   // IR Line Kanan-Dalam
#define IR_RR   33   // IR Line Kanan-Luar

// ---- Pin Motor Driver L298N --------------------------------
#define PIN_IN1 25   // Motor A (kiri) – Arah
#define PIN_IN2 26
#define PIN_IN3 27   // Motor B (kanan) – Arah
#define PIN_IN4 14
#define PIN_ENA 12   // Motor A – PWM Enable
#define PIN_ENB 13   // Motor B – PWM Enable

// ---- Pin MPU-6050 (I2C) ------------------------------------
#define MPU_SDA 21   // I2C SDA (no conflict: ECHO_F moved to GPIO39)
#define MPU_SCL 22   // I2C SCL (no conflict: TRIG_R moved to GPIO17)
// AD0 = GND  →  alamat I2C = 0x68

// ---- Pin LED Indikator Mode --------------------------------
#define LED_R    2   // Merah  – STOP / Error
#define LED_G    4   // Hijau  – Line Follower
#define LED_B   16   // Biru   – Wall Follow Kiri
// LED_Y removed – GPIO17 reassigned to TRIG_R. Right-wall mode indicated by buzzer.

// ---- Pin Buzzer & Tombol -----------------------------------
#define BUZZER  15   // Buzzer aktif
#define BTN_START 0  // Tombol START (BOOT button bawaan ESP32)
#define BTN_STOP 36  // Tombol STOP  (input-only GPIO, no internal pull-up)
                     // → Pasang resistor 10kΩ pull-down ke GND; tekan HIGH

// ---- PWM Motor Config --------------------------------------
#define PWM_FREQ   1000   // Hz
#define PWM_BITS      8   // Resolusi 8-bit (0–255)
#define CH_ENA        0   // LEDC channel Motor A
#define CH_ENB        1   // LEDC channel Motor B

// ---- Parameter Default (bisa diubah via WiFi) --------------
#define DEFAULT_SETPOINT      15.0f  // cm – jarak ideal ke dinding
#define DEFAULT_BASE_SPEED   150     // 0–255
#define DEFAULT_MAX_SPEED    200     // 0–255
#define DEFAULT_KP             3.0f
#define DEFAULT_KI             0.05f
#define DEFAULT_KD             1.0f
#define DEFAULT_KP_LINE        2.0f  // Kp untuk line follower
#define DEFAULT_KP_HEADING     2.0f  // Kp koreksi heading dari gyro
#define OBSTACLE_DIST_FRONT   10.0f  // cm – jarak emergency stop
#define WALL_DETECT_DIST      30.0f  // cm – threshold ada dinding
#define LINE_DETECT_THRESH   500     // ADC threshold garis hitam
#define IMPACT_THRESHOLD       2.5f  // g – threshold deteksi benturan
#define TILT_THRESHOLD        30.0f  // derajat – threshold kemiringan
#define COMPLEMENTARY_ALPHA    0.96f // Complementary filter koef.

// ---- WiFi AP Config ----------------------------------------
#define WIFI_AP_SSID  "WallFollower-ESP32"
#define WIFI_AP_PASS  "robot1234"

// ---- NVS Preferences Keys ----------------------------------
#define NVS_NAMESPACE "wallbot"
#define KEY_SETPOINT  "setpoint"
#define KEY_BASE_SPD  "base_spd"
#define KEY_MAX_SPD   "max_spd"
#define KEY_KP        "kp"
#define KEY_KI        "ki"
#define KEY_KD        "kd"
#define KEY_KP_LINE   "kp_line"
#define KEY_KP_HEAD   "kp_head"
#define KEY_WALL_SIDE "wall_side"  // 0 = kiri, 1 = kanan

// ---- Mode Robot --------------------------------------------
enum RobotMode : uint8_t {
    MODE_STOP            = 0,
    MODE_LINE_FOLLOW     = 1,
    MODE_WALL_FOLLOW_L   = 2,
    MODE_WALL_FOLLOW_R   = 3,
    MODE_EXPLORE         = 4,
    MODE_AVOID_OBSTACLE  = 5,
    MODE_TURN_90_LEFT    = 6,
    MODE_TURN_90_RIGHT   = 7,
    MODE_CALIBRATE_IMU   = 8
};
