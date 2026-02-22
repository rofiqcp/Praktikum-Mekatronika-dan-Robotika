# MATERI MODUL 07: WALL FOLLOWER ROBOT DENGAN ESP32 DAN PLATFORMIO

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 07 – Wall Follower  
**Platform:** ESP32 + PlatformIO  
**Prasyarat:** Modul 01 (Desain PCB), Modul 03 (Fusion360), Modul 06 (Line Follower)  
**Estimasi Waktu Belajar:** 8–10 Jam

---

## DAFTAR ISI

1. [Pendahuluan – Konsep Wall Follower](#1-pendahuluan--konsep-wall-follower)
2. [Sensor Ultrasonik HC-SR04](#2-sensor-ultrasonik-hc-sr04)
3. [Sensor Inframerah (IR) untuk Wall Detection](#3-sensor-inframerah-ir-untuk-wall-detection)
4. [Sensor IMU MPU-6050](#4-sensor-imu-mpu-6050)
5. [Algoritma Wall Following](#5-algoritma-wall-following)
6. [Kontroler PID untuk Wall Follower](#6-kontroler-pid-untuk-wall-follower)
7. [ESP32 dan PlatformIO](#7-esp32-dan-platformio)
8. [Konfigurasi Motor Driver dan Aktuator](#8-konfigurasi-motor-driver-dan-aktuator)
9. [Integrasi Wall Follower dan Line Follower](#9-integrasi-wall-follower-dan-line-follower)
10. [Setting Parameter via Hotspot ESP32](#10-setting-parameter-via-hotspot-esp32)
11. [Pseudo Code dan Implementasi](#11-pseudo-code-dan-implementasi)
12. [Referensi](#12-referensi)

---

## 1. PENDAHULUAN – KONSEP WALL FOLLOWER

### 1.1 Definisi Wall Follower

**Wall Follower Robot** adalah robot otonom yang bergerak dengan mempertahankan jarak konstan terhadap dinding (wall) di sisi kiri, kanan, atau depannya. Robot ini termasuk kategori **reactive autonomous robot** karena responnya langsung terhadap input sensor tanpa peta global lingkungan.

Wall follower merupakan salah satu algoritma navigasi tertua dalam robotika mobile, pertama kali diformulasikan dalam konteks **maze-solving** (pemecahan labirin). Prinsip dasarnya dikenal dengan nama **"right-hand rule"** atau **"left-hand rule"** — robot selalu menjaga kontak dengan dinding di satu sisi secara konsisten.

### 1.2 Aplikasi Wall Follower

| Aplikasi | Deskripsi |
|---------|-----------|
| **Penjelajahan Labirin** | Robot kompetisi mencari jalan keluar labirin |
| **Pembersih Lantai Otomatis** | Robot vacuum mengikuti dinding ruangan |
| **Gudang Otomatis (AGV)** | Robot mengikuti dinding rak untuk navigasi |
| **Search and Rescue** | Robot menelusuri koridor bangunan runtuh |
| **Inspeksi Pipa/Terowongan** | Robot menjaga jarak ke dinding saluran |
| **Pertanian Otonom** | Robot mengikuti pagar ladang |
| **Rumah Sakit** | Robot pembawa obat mengikuti koridor |

### 1.3 Perbandingan Wall Follower dengan Line Follower

| Aspek | Wall Follower | Line Follower |
|-------|--------------|---------------|
| **Referensi navigasi** | Dinding fisik (3D) | Garis di lantai (2D) |
| **Sensor utama** | Ultrasonik / IR jarak | IR reflektansi / kamera |
| **Fleksibilitas** | Tinggi (tidak butuh jalur) | Rendah (butuh garis) |
| **Akurasi jalur** | Sedang | Tinggi |
| **Lingkungan** | Indoor/Outdoor | Indoor (permukaan rata) |
| **Kompleksitas algoritma** | Tinggi | Sedang |
| **Ketahanan gangguan** | Rentan pantulan | Rentan cahaya |

### 1.4 Arsitektur Sistem Wall Follower

```
┌─────────────────────────────────────────────────────┐
│                   WALL FOLLOWER SYSTEM               │
│                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────────────┐  │
│  │ Sensor  │───▶│  ESP32  │───▶│  Motor Driver   │  │
│  │ Layer   │    │  MCU    │    │  (L298N/L293D)  │  │
│  └─────────┘    └────┬────┘    └────────┬────────┘  │
│  • HC-SR04 ×3        │                 │            │
│  • IR Sensor ×4      │ PID Controller  │            │
│  • Encoder (opt)  ┌──┴──────────────┐  │            │
│                   │ Wall Detection   │  ▼            │
│  ┌─────────┐      │ Algorithm       │ ┌──────────┐  │
│  │  WiFi   │◀────▶│ Speed Control   │ │ DC Motor │  │
│  │HotSpot  │      │ Mode Switch     │ │  ×2      │  │
│  │ Config  │      └─────────────────┘ └──────────┘  │
│  └─────────┘                                        │
└─────────────────────────────────────────────────────┘
```

---

## 2. SENSOR ULTRASONIK HC-SR04

### 2.1 Prinsip Kerja HC-SR04

HC-SR04 adalah sensor ultrasonik populer yang bekerja dengan prinsip **Time of Flight (ToF)**:

1. Pin **TRIG** menerima pulsa HIGH selama **10 µs**
2. Modul memancarkan **8 pulsa sinyal ultrasonik 40 kHz**
3. Gelombang memantul dari objek dan kembali ke receiver
4. Pin **ECHO** menghasilkan pulsa HIGH selama waktu tempuh gelombang
5. Jarak dihitung dengan rumus:

```
Jarak (cm) = Durasi_ECHO (µs) / 58
atau
Jarak (cm) = (Durasi_ECHO × 0.0343) / 2
```

**Keterangan:**
- Kecepatan suara di udara ≈ 343 m/s = 0.0343 cm/µs
- Dibagi 2 karena gelombang menempuh jarak 2× (pergi + pulang)

### 2.2 Spesifikasi HC-SR04

| Parameter | Nilai |
|----------|-------|
| Tegangan operasi | 5V DC |
| Arus konsumsi | 15 mA |
| Frekuensi ultrasonik | 40 kHz |
| Jangkauan pengukuran | 2 cm – 400 cm |
| Akurasi | ±3 mm |
| Sudut pancaran | 15° |
| Pin interface | VCC, TRIG, ECHO, GND |

### 2.3 Penempatan Sensor untuk Wall Follower

Untuk wall follower yang optimal, minimal 3 sensor HC-SR04 dipasang:

```
         [DEPAN]
            ↑
     ┌──────┴──────┐
     │  HC-SR04 F  │
[KIRI]│             │[KANAN]
→    │    ROBOT    │    ←
HC-SR04          HC-SR04
  L              R
     │             │
     └─────────────┘
```

- **Sensor Kiri (L):** Mengukur jarak ke dinding kiri
- **Sensor Depan (F):** Mendeteksi rintangan/dinding di depan
- **Sensor Kanan (R):** Mengukur jarak ke dinding kanan

### 2.4 Kode Library HC-SR04 untuk ESP32 (PlatformIO)

```cpp
// Fungsi membaca jarak HC-SR04 dengan timeout
float readUltrasonic(int trigPin, int echoPin) {
    // Pastikan TRIG LOW terlebih dahulu
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    
    // Kirim pulsa TRIG 10µs
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    // Baca durasi ECHO dengan timeout 30ms (max ~500cm)
    long duration = pulseIn(echoPin, HIGH, 30000);
    
    // Hitung jarak
    if (duration == 0) return 999.0;  // timeout = tidak ada objek
    return duration / 58.0;           // konversi ke cm
}
```

### 2.5 Masalah Umum dan Solusinya

| Masalah | Penyebab | Solusi |
|---------|---------|--------|
| Pembacaan 0 atau 999 | Timeout, tidak ada pantulan | Tambah delay antar pengukuran |
| Nilai berfluktuasi | Interferensi multi-sensor | Aktifkan sensor bergantian (multiplexing) |
| Level tegangan ECHO 5V | HC-SR04 output 5V, ESP32 3.3V | Gunakan voltage divider atau level shifter |
| Blind spot dekat | Minimum range 2cm | Tambah IR sensor untuk jarak < 5cm |

---

## 3. SENSOR INFRAMERAH (IR) UNTUK WALL DETECTION

### 3.1 Prinsip Kerja Sensor IR

Sensor IR (inframerah) untuk deteksi dinding bekerja berdasarkan **reflectance** (pantulan). LED IR memancarkan cahaya, dan fotodioda/fototransistor mendeteksi intensitas pantulan:

- **Objek dekat / dinding ada:** Pantulan kuat → tegangan output rendah (aktif LOW)
- **Tidak ada objek:** Pantulan lemah/tidak ada → tegangan output tinggi

### 3.2 Perbandingan HC-SR04 vs IR untuk Wall Following

| Kriteria | HC-SR04 | IR Sharp GP2Y0A |
|---------|---------|-----------------|
| Jangkauan | 2–400 cm | 10–80 cm |
| Output | Digital (pulsa) | Analog |
| Presisi jarak | Tinggi | Sedang |
| Kecepatan respons | ~60 ms | ~40 ms |
| Gangguan cahaya | Tidak | Ya (infrared ambient) |
| Harga | Murah | Sedang |
| Cocok untuk | Long-range | Short-range |

### 3.3 Kode Baca Sensor IR Analog (Sharp GP2Y0A21)

```cpp
// Membaca jarak dari sensor IR Sharp GP2Y0A21
float readIRSharp(int analogPin) {
    int rawValue = analogRead(analogPin);
    // Konversi ADC ke tegangan (ESP32: 12-bit ADC, 3.3V)
    float voltage = rawValue * (3.3 / 4095.0);
    // Formula konversi tegangan ke jarak (cm) untuk GP2Y0A21
    if (voltage < 0.4) return 80.0;  // out of range
    float distance = 27.728 * pow(voltage, -1.2045);
    return constrain(distance, 10.0, 80.0);
}
```

---

## 4. SENSOR IMU MPU-6050

### 4.1 Pengenalan MPU-6050

**MPU-6050** adalah modul **IMU (Inertial Measurement Unit)** 6-DOF (Degrees of Freedom) yang menggabungkan:
- **Accelerometer 3-axis (X, Y, Z):** mengukur percepatan linear termasuk gravitasi (±2g / ±4g / ±8g / ±16g)
- **Gyroscope 3-axis (X, Y, Z):** mengukur kecepatan sudut / laju rotasi (±250 / ±500 / ±1000 / ±2000 °/s)
- **Sensor suhu** onboard: -40°C hingga +85°C
- **DMP (Digital Motion Processor):** prosesor onboard untuk filter quaternion

Antarmuka komunikasi menggunakan **I2C** (400kHz fast mode), dengan alamat I2C **0x68** (AD0=GND) atau **0x69** (AD0=VCC).

### 4.2 Relevansi MPU-6050 untuk Wall Follower Robot

Penambahan MPU-6050 pada wall follower robot memberikan keunggulan signifikan:

| Fungsi | Manfaat untuk Wall Follower |
|--------|----------------------------|
| **Deteksi heading (yaw)** | Robot mengetahui orientasi absolut → belokan sudut tepat |
| **Deteksi kemiringan (pitch/roll)** | Mendeteksi permukaan miring, tanjakan, atau robot terguling |
| **Deteksi getaran/benturan** | Alert jika robot menabrak dinding keras (impact detection) |
| **Stabilisasi gerak lurus** | Gyro menjaga robot berjalan lurus tanpa drift motor |
| **Odometri berbasis IMU** | Estimasi posisi sederhana tanpa encoder roda |
| **Dead reckoning** | Melanjutkan navigasi saat sensor jarak gagal sementara |
| **Deteksi slip roda** | Accelerometer vs expected motion → deteksi wheel slip |

### 4.3 Spesifikasi Teknis MPU-6050

| Parameter | Nilai |
|----------|-------|
| Tegangan supply | 3.3V (modul breakout biasanya 5V-tolerant) |
| Arus konsumsi | 3.9 mA (normal), 10 µA (sleep) |
| Antarmuka | I2C (hingga 400 kHz), SPI (MPU-6000) |
| Alamat I2C | 0x68 (default) atau 0x69 |
| Resolusi ADC | 16-bit untuk accel dan gyro |
| Full-scale accel | ±2g, ±4g, ±8g, ±16g |
| Full-scale gyro | ±250, ±500, ±1000, ±2000 °/s |
| Sensitivitas accel | 16384 LSB/g (pada ±2g) |
| Sensitivitas gyro | 131 LSB/(°/s) (pada ±250°/s) |
| Interrupt pin | INT – untuk data ready, motion detect |
| FIFO buffer | 1024 bytes |
| DMP | 6-axis quaternion fusion |
| Dimensi modul | 20.3mm × 15.6mm |

### 4.4 Koneksi MPU-6050 ke ESP32

| Pin MPU-6050 | Pin ESP32 | Keterangan |
|-------------|----------|-----------|
| VCC | 3.3V | Tegangan supply (bukan 5V!) |
| GND | GND | Ground |
| SCL | GPIO 22 | I2C Clock |
| SDA | GPIO 21 | I2C Data |
| INT | GPIO 4 | Interrupt (opsional) |
| AD0 | GND | Alamat I2C = 0x68 |

> **⚠️ CATATAN:** Pada beberapa modul MPU-6050 breakout, terdapat regulator 3.3V onboard sehingga pin VCC bisa dihubungkan ke 5V. Periksa datasheet modul yang digunakan.

### 4.5 Library MPU-6050 untuk PlatformIO

```ini
; platformio.ini - tambahkan library berikut
lib_deps = 
    electroniccats/MPU6050@^1.3.0
    ; atau alternatif:
    ; jrowberg/I2Cdevlib-MPU6050@^1.0.0
```

### 4.6 Inisialisasi dan Pembacaan Data MPU-6050

```cpp
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

// Data sensor global
struct IMUData {
    float accelX, accelY, accelZ;  // dalam g
    float gyroX, gyroY, gyroZ;     // dalam °/s
    float temperature;              // dalam °C
    float yaw, pitch, roll;         // dalam derajat (perlu integrasi)
} imuData;

// Kalibrasi offset (diisi setelah kalibrasi)
int16_t ax_off = 0, ay_off = 0, az_off = 0;
int16_t gx_off = 0, gy_off = 0, gz_off = 0;

void setupMPU6050() {
    Wire.begin(21, 22);  // SDA=21, SCL=22 untuk ESP32
    Wire.setClock(400000);  // Fast mode 400kHz
    
    mpu.initialize();
    
    if (!mpu.testConnection()) {
        Serial.println("MPU6050 tidak terdeteksi!");
        return;
    }
    Serial.println("MPU6050 OK - Alamat I2C: 0x68");
    
    // Set full-scale range
    mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);   // ±2g
    mpu.setFullScaleGyroRange(MPU6050_GYRO_FS_250);   // ±250°/s
    
    // Set DLPF (Digital Low Pass Filter) - mengurangi noise
    mpu.setDLPFMode(MPU6050_DLPF_BW_42);  // 42 Hz bandwidth
    
    // Kalibrasi offset
    calibrateMPU6050();
}

void calibrateMPU6050() {
    Serial.println("Kalibrasi MPU6050... Jangan gerakkan robot!");
    int32_t sum_ax=0, sum_ay=0, sum_az=0;
    int32_t sum_gx=0, sum_gy=0, sum_gz=0;
    const int N = 200;
    
    for (int i = 0; i < N; i++) {
        int16_t ax, ay, az, gx, gy, gz;
        mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        sum_ax += ax; sum_ay += ay; sum_az += az;
        sum_gx += gx; sum_gy += gy; sum_gz += gz;
        delay(5);
    }
    
    ax_off = sum_ax / N;
    ay_off = sum_ay / N;
    az_off = (sum_az / N) - 16384;  // kurangi gravitasi 1g
    gx_off = sum_gx / N;
    gy_off = sum_gy / N;
    gz_off = sum_gz / N;
    
    Serial.println("Kalibrasi selesai.");
}

void readMPU6050() {
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    
    // Terapkan offset kalibrasi
    ax -= ax_off; ay -= ay_off; az -= az_off;
    gx -= gx_off; gy -= gy_off; gz -= gz_off;
    
    // Konversi ke satuan fisik
    imuData.accelX = ax / 16384.0;   // g
    imuData.accelY = ay / 16384.0;
    imuData.accelZ = az / 16384.0;
    imuData.gyroX  = gx / 131.0;    // °/s
    imuData.gyroY  = gy / 131.0;
    imuData.gyroZ  = gz / 131.0;
    imuData.temperature = mpu.getTemperature() / 340.0 + 36.53;
}
```

### 4.7 Kalkulasi Sudut dari MPU-6050

#### Metode 1: Dari Accelerometer Saja (statis, tanpa drift tapi noisy saat bergerak)

```cpp
float calcPitchAccel(float ax, float ay, float az) {
    return atan2(-ax, sqrt(ay*ay + az*az)) * 180.0 / PI;
}

float calcRollAccel(float ax, float ay, float az) {
    return atan2(ay, az) * 180.0 / PI;
}
```

#### Metode 2: Integrasi Gyroscope (dinamis, tapi drift bertambah)

```cpp
float yaw   = 0.0;
float pitch = 0.0;
float roll  = 0.0;
unsigned long lastIMUTime = 0;

void integrateGyro() {
    unsigned long now = millis();
    float dt = (now - lastIMUTime) / 1000.0;
    lastIMUTime = now;
    
    yaw   += imuData.gyroZ * dt;
    pitch += imuData.gyroY * dt;
    roll  += imuData.gyroX * dt;
}
```

#### Metode 3: Complementary Filter (gabungan accel + gyro – DIREKOMENDASIKAN)

```cpp
// Alpha mendekati 1.0 = lebih percaya gyro (smooth tapi ada drift)
// Alpha mendekati 0.0 = lebih percaya accel (noise tapi tidak drift)
const float ALPHA = 0.96;

float compPitch = 0.0, compRoll = 0.0;
unsigned long lastCompTime = 0;

void complementaryFilter() {
    unsigned long now = millis();
    float dt = (now - lastCompTime) / 1000.0;
    lastCompTime = now;
    
    float accelPitch = calcPitchAccel(imuData.accelX, imuData.accelY, imuData.accelZ);
    float accelRoll  = calcRollAccel(imuData.accelX, imuData.accelY, imuData.accelZ);
    
    compPitch = ALPHA * (compPitch + imuData.gyroY * dt) + (1.0 - ALPHA) * accelPitch;
    compRoll  = ALPHA * (compRoll  + imuData.gyroX * dt) + (1.0 - ALPHA) * accelRoll;
}
```

#### Metode 4: DMP (Digital Motion Processor) – Akurasi Tertinggi

```cpp
// Menggunakan built-in DMP MPU-6050 untuk quaternion fusion
// Memerlukan library I2Cdevlib versi lengkap
#include "MPU6050_6Axis_MotionApps20.h"

MPU6050 mpu;
uint16_t packetSize;
uint8_t fifoBuffer[64];
Quaternion q;
VectorFloat gravity;
float yprDMP[3];  // [yaw, pitch, roll] dalam radian

void setupDMP() {
    mpu.dmpInitialize();
    mpu.setDMPEnabled(true);
    packetSize = mpu.dmpGetFIFOPacketSize();
}

void readDMP() {
    if (mpu.dmpGetCurrentFIFOPacket(fifoBuffer)) {
        mpu.dmpGetQuaternion(&q, fifoBuffer);
        mpu.dmpGetGravity(&gravity, &q);
        mpu.dmpGetYawPitchRoll(yprDMP, &q, &gravity);
        // yprDMP[0] = yaw (radian), konversi ke derajat: yprDMP[0] * 180/PI
    }
}
```

### 4.8 Aplikasi MPU-6050 pada Wall Follower: Gyro-Assisted Turning

Salah satu penggunaan paling penting MPU-6050 pada wall follower adalah **belokan presisi berbasis gyroscope**. Robot dapat berbelok tepat 90° tanpa encoder roda:

```cpp
// Belokan tepat 90 derajat ke kanan menggunakan gyro
void turnRight90Gyro() {
    float startYaw = yaw;
    float targetYaw = startYaw + 90.0;
    
    // Mulai belokan
    setMotorSpeed(150, -150);  // Motor kiri maju, kanan mundur
    
    while (abs(yaw - startYaw) < 88.0) {
        readMPU6050();
        integrateGyro();
        delay(5);
    }
    
    setMotorSpeed(0, 0);  // Stop
    Serial.print("Belokan selesai. Yaw actual: ");
    Serial.println(yaw - startYaw);
}

// Berjalan lurus dengan koreksi gyro
void moveForwardStraight(int baseSpeed, float targetHeading) {
    readMPU6050();
    integrateGyro();
    
    float headingError = targetHeading - yaw;
    float correction = 2.0 * headingError;  // Kp=2.0 untuk heading
    
    int speedL = constrain(baseSpeed + correction, 0, 255);
    int speedR = constrain(baseSpeed - correction, 0, 255);
    setMotorSpeed(speedL, speedR);
}
```

### 4.9 Deteksi Benturan dengan Accelerometer

```cpp
// Deteksi impact/benturan keras
const float IMPACT_THRESHOLD = 2.5;  // g (gravitasi)

bool detectImpact() {
    float totalAccel = sqrt(
        imuData.accelX * imuData.accelX +
        imuData.accelY * imuData.accelY +
        imuData.accelZ * imuData.accelZ
    );
    // Kurangi 1g (gravitasi statis), jika sisa > threshold = ada benturan
    return (abs(totalAccel - 1.0) > IMPACT_THRESHOLD);
}

// Deteksi kemiringan berbahaya (robot hampir terguling)
bool detectTilt() {
    return (abs(compRoll) > 30.0 || abs(compPitch) > 30.0);
}
```

### 4.10 Integrasi MPU-6050 dalam Sistem Wall Follower

```
┌─────────────────────────────────────────────────────────────┐
│              WALL FOLLOWER + MPU-6050 SYSTEM                │
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌───────────────────────┐   │
│  │ HC-SR04  │   │ MPU-6050 │   │     ESP32 Core 0      │   │
│  │  × 3     │──▶│ I2C 0x68 │──▶│  Sensor Task          │   │
│  └──────────┘   └──────────┘   │  - Baca HC-SR04 ×3    │   │
│  ┌──────────┐                  │  - Baca MPU-6050       │   │
│  │ IR Line  │──────────────────│  - Filter + Fusion     │   │
│  │  × 4     │                  └──────────┬────────────┘   │
│  └──────────┘                             │ Shared Data     │
│                                           ▼                 │
│                                 ┌───────────────────────┐   │
│                                 │     ESP32 Core 1      │   │
│                                 │  Control Task         │   │
│                                 │  - Mode determination │   │
│                                 │  - PID (distance)     │   │
│                                 │  - PID (heading/yaw)  │   │
│                                 │  - Motor output       │   │
│                                 │  - Web server         │   │
│                                 └───────────┬───────────┘   │
│                                             │               │
│                                    ┌────────▼────────┐      │
│                                    │   L298N Motor   │      │
│                                    │   Driver        │      │
│                                    └────────┬────────┘      │
│                                             │               │
│                                    ┌────────▼────────┐      │
│                                    │  DC Motor × 2   │      │
│                                    └─────────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. ALGORITMA WALL FOLLOWING

### 5.1 Left-Hand Rule (Aturan Tangan Kiri)

Robot selalu mengikuti dinding di sisi **kiri**. Prioritas navigasi:

```
1. Jika ada dinding di kiri dan tidak ada di depan → Maju terus
2. Jika ada dinding di depan → Belok kanan
3. Jika tidak ada dinding di kiri → Belok kiri (cari dinding)
4. Jika tidak ada dinding di semua sisi → Belok kiri (default)
```

### 5.2 Right-Hand Rule (Aturan Tangan Kanan)

Robot selalu mengikuti dinding di sisi **kanan**. Prioritas navigasi:

```
1. Jika ada dinding di kanan dan tidak ada di depan → Maju terus
2. Jika ada dinding di depan → Belok kiri
3. Jika tidak ada dinding di kanan → Belok kanan (cari dinding)
4. Jika tidak ada dinding di semua sisi → Belok kanan (default)
```

### 5.3 Bug Algorithm (Peningkatan Wall Following)

Bug Algorithm merupakan pengembangan wall following yang mampu menuju **target spesifik**:

```
BUG0:
1. Gerak menuju target (garis lurus)
2. Jika bertemu rintangan, ikuti dinding sampai bisa melanjutkan ke target
3. Lanjut ke target

BUG1:
1. Gerak menuju target
2. Jika bertemu rintangan, kelilingi seluruh rintangan sekali
3. Berhenti di titik terdekat ke target dari keliling rintangan
4. Lanjut ke target
```

### 5.4 Fuzzy Logic untuk Wall Following

Fuzzy logic memberikan respons yang lebih halus dibanding algoritma threshold biner:

**Variabel Input (Fuzzifikasi):**
- `error_distance`: selisih jarak actual vs setpoint (cm)
- `rate_of_change`: perubahan error per waktu

**Himpunan Fuzzy untuk error_distance:**
- `VERY_CLOSE` (< 5 cm)
- `CLOSE` (5–12 cm)
- `ON_TARGET` (12–18 cm)
- `FAR` (18–25 cm)
- `VERY_FAR` (> 25 cm)

**Tabel Aturan Fuzzy (Rule Base):**

| Error Distance | Rate of Change | Motor Aksi |
|---------------|---------------|-----------|
| VERY_CLOSE | DECREASING | Belok keras ke kanan |
| CLOSE | DECREASING | Belok sedikit ke kanan |
| ON_TARGET | ANY | Maju lurus |
| FAR | INCREASING | Belok sedikit ke kiri |
| VERY_FAR | INCREASING | Belok keras ke kiri |

---

## 6. KONTROLER PID UNTUK WALL FOLLOWER

### 6.1 Konsep PID

**PID (Proportional-Integral-Derivative)** adalah kontroler klasik yang banyak digunakan dalam sistem kontrol otomatis, termasuk wall follower robot:

```
Output = Kp × e(t) + Ki × ∫e(t)dt + Kd × de(t)/dt
```

Dimana:
- `e(t)` = error = setpoint − actual_distance
- `Kp` = Proportional gain → respons terhadap error saat ini
- `Ki` = Integral gain → akumulasi error masa lalu
- `Kd` = Derivative gain → prediksi error masa depan

### 6.2 Penerapan PID pada Wall Follower

```
Setpoint: jarak ideal ke dinding = 15 cm
Actual:   jarak terukur sensor kiri = 20 cm
Error:    15 - 20 = -5 cm (robot terlalu jauh dari dinding kiri)

Respons PID:
- P: -5 × Kp → belok sedikit ke kiri
- I: akumulasi error → koreksi drift
- D: kecepatan perubahan error → antisipasi overshoot
```

### 6.3 Tuning PID

**Metode Ziegler-Nichols:**
1. Set Ki = 0, Kd = 0
2. Naikkan Kp hingga sistem osilasi stabil (Ku)
3. Catat periode osilasi (Tu)
4. Hitung parameter: Kp = 0.6Ku, Ki = 1.2Ku/Tu, Kd = 0.075Ku×Tu

**Nilai Awal Rekomendasi untuk ESP32 Robot:**
- Kp = 2.0 – 5.0
- Ki = 0.01 – 0.1
- Kd = 0.5 – 2.0

### 6.4 Implementasi PID dalam C++ (PlatformIO)

```cpp
class PIDController {
private:
    float Kp, Ki, Kd;
    float setpoint;
    float prevError;
    float integral;
    unsigned long prevTime;
    float integralLimit;

public:
    PIDController(float kp, float ki, float kd, float sp, float iLimit = 100.0)
        : Kp(kp), Ki(ki), Kd(kd), setpoint(sp), prevError(0),
          integral(0), prevTime(0), integralLimit(iLimit) {}

    float compute(float actual) {
        unsigned long now = millis();
        float dt = (now - prevTime) / 1000.0;
        if (dt <= 0 || dt > 1.0) dt = 0.01;  // safety check

        float error = setpoint - actual;

        // Proportional
        float P = Kp * error;

        // Integral dengan anti-windup
        integral += error * dt;
        integral = constrain(integral, -integralLimit, integralLimit);
        float I = Ki * integral;

        // Derivative
        float D = Kd * (error - prevError) / dt;

        prevError = error;
        prevTime = now;

        return P + I + D;
    }

    void reset() {
        prevError = 0;
        integral = 0;
        prevTime = millis();
    }

    void setGains(float kp, float ki, float kd) {
        Kp = kp; Ki = ki; Kd = kd;
    }

    void setSetpoint(float sp) { setpoint = sp; }
};
```

---

## 7. ESP32 DAN PLATFORMIO

### 7.1 Keunggulan ESP32 untuk Wall Follower

| Fitur | Nilai | Manfaat untuk Wall Follower |
|-------|-------|---------------------------|
| Dual-core Xtensa LX6 | 240 MHz | Core 0: sensor, Core 1: motor & WiFi |
| RAM | 520 KB SRAM | Buffer data sensor, web server |
| WiFi 802.11 b/g/n | 2.4 GHz | Konfigurasi parameter via smartphone |
| Bluetooth 4.2 | BLE + Classic | Alternatif monitoring |
| ADC | 12-bit, 18 channel | Baca sensor IR analog |
| PWM | 16 channel (LEDC) | Kontrol kecepatan motor halus |
| Timer | 4× 64-bit | Presisi timing ultrasonik |
| GPIO | 34 pin | Cukup untuk semua sensor+motor |

### 7.2 Setup PlatformIO untuk ESP32

**platformio.ini:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
lib_deps = 
    ESP Async WebServer
    AsyncTCP
    ArduinoJson
upload_speed = 921600
build_flags = 
    -DCORE_DEBUG_LEVEL=0
```

### 7.3 Penanganan Multi-Sensor dengan Dual Core ESP32

```cpp
// Deklarasi task untuk dual core
TaskHandle_t sensorTaskHandle;
TaskHandle_t controlTaskHandle;

// Shared data dengan mutex
SemaphoreHandle_t dataMutex;
struct SensorData {
    float distLeft;
    float distFront;
    float distRight;
    bool lineLeft;
    bool lineRight;
} sensorData;

// Task di Core 0: Baca semua sensor
void sensorTask(void* parameter) {
    while (true) {
        float dL = readUltrasonic(TRIG_L, ECHO_L);
        float dF = readUltrasonic(TRIG_F, ECHO_F);
        float dR = readUltrasonic(TRIG_R, ECHO_R);
        bool lL = digitalRead(IR_LEFT);
        bool lR = digitalRead(IR_RIGHT);
        
        if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(10))) {
            sensorData.distLeft  = dL;
            sensorData.distFront = dF;
            sensorData.distRight = dR;
            sensorData.lineLeft  = lL;
            sensorData.lineRight = lR;
            xSemaphoreGive(dataMutex);
        }
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

// Task di Core 1: Kontrol motor + Web Server
void controlTask(void* parameter) {
    while (true) {
        float dL, dF, dR;
        if (xSemaphoreTake(dataMutex, pdMS_TO_TICKS(10))) {
            dL = sensorData.distLeft;
            dF = sensorData.distFront;
            dR = sensorData.distRight;
            xSemaphoreGive(dataMutex);
        }
        // Jalankan algoritma kontrol
        wallFollowControl(dL, dF, dR);
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
```

---

## 8. KONFIGURASI MOTOR DRIVER DAN AKTUATOR

### 8.1 L298N Motor Driver

L298N adalah H-Bridge dual channel yang memungkinkan kontrol arah dan kecepatan 2 motor DC:

| Pin | Fungsi |
|-----|--------|
| IN1, IN2 | Kontrol arah Motor A |
| IN3, IN4 | Kontrol arah Motor B |
| ENA | PWM kecepatan Motor A |
| ENB | PWM kecepatan Motor B |
| OUT1-OUT4 | Koneksi ke motor |

**Tabel Kebenaran Gerak Robot:**

| Kondisi | IN1 | IN2 | IN3 | IN4 | Gerakan |
|---------|-----|-----|-----|-----|---------|
| Maju | HIGH | LOW | HIGH | LOW | Forward |
| Mundur | LOW | HIGH | LOW | HIGH | Backward |
| Belok Kanan | HIGH | LOW | LOW | HIGH | Turn Right |
| Belok Kiri | LOW | HIGH | HIGH | LOW | Turn Left |
| Berhenti | LOW | LOW | LOW | LOW | Stop |

### 8.2 Kontrol PWM Motor ESP32 (LEDC)

```cpp
// Setup PWM untuk motor (ESP32 LEDC API)
const int PWM_FREQ = 1000;    // 1 kHz
const int PWM_BITS = 8;       // 8-bit resolusi (0-255)
const int CH_ENA = 0;         // LEDC channel untuk Motor A
const int CH_ENB = 1;         // LEDC channel untuk Motor B

void setupMotors() {
    // Konfigurasi PWM channels
    ledcSetup(CH_ENA, PWM_FREQ, PWM_BITS);
    ledcSetup(CH_ENB, PWM_FREQ, PWM_BITS);
    
    // Hubungkan PWM ke pin fisik
    ledcAttachPin(PIN_ENA, CH_ENA);
    ledcAttachPin(PIN_ENB, CH_ENB);
    
    // Set pin arah motor
    pinMode(PIN_IN1, OUTPUT);
    pinMode(PIN_IN2, OUTPUT);
    pinMode(PIN_IN3, OUTPUT);
    pinMode(PIN_IN4, OUTPUT);
}

void setMotorSpeed(int speedA, int speedB) {
    // Motor A (kiri)
    if (speedA >= 0) {
        digitalWrite(PIN_IN1, HIGH);
        digitalWrite(PIN_IN2, LOW);
    } else {
        digitalWrite(PIN_IN1, LOW);
        digitalWrite(PIN_IN2, HIGH);
        speedA = -speedA;
    }
    ledcWrite(CH_ENA, constrain(speedA, 0, 255));
    
    // Motor B (kanan)
    if (speedB >= 0) {
        digitalWrite(PIN_IN3, HIGH);
        digitalWrite(PIN_IN4, LOW);
    } else {
        digitalWrite(PIN_IN3, LOW);
        digitalWrite(PIN_IN4, HIGH);
        speedB = -speedB;
    }
    ledcWrite(CH_ENB, constrain(speedB, 0, 255));
}
```

---

## 9. INTEGRASI WALL FOLLOWER DAN LINE FOLLOWER

### 9.1 Konsep Hybrid Navigation

Menggabungkan wall follower dan line follower memungkinkan robot bernavigasi lebih cerdas:

```
MODE SWITCHING LOGIC:
┌──────────────────────────────────────────────┐
│  Deteksi garis?  ──YES──▶  LINE FOLLOWER MODE │
│       │                                       │
│      NO                                       │
│       │                                       │
│  Deteksi dinding? ─YES──▶ WALL FOLLOWER MODE  │
│       │                                       │
│      NO                                       │
│       ▼                                       │
│   EXPLORE MODE (putar/random walk)            │
└──────────────────────────────────────────────┘
```

### 9.2 Prioritas Mode

1. **Mode Darurat (Emergency):** Jarak depan < 5 cm → STOP
2. **Mode Line Follower:** Sensor IR lantai mendeteksi garis → ikuti garis
3. **Mode Wall Follower:** Sensor ultrasonik mendeteksi dinding → ikuti dinding
4. **Mode Explore:** Tidak ada referensi → putar mencari dinding/garis

### 9.3 Transisi Antar Mode

```cpp
enum RobotMode {
    MODE_STOP,
    MODE_LINE_FOLLOW,
    MODE_WALL_FOLLOW_LEFT,
    MODE_WALL_FOLLOW_RIGHT,
    MODE_EXPLORE,
    MODE_AVOID_OBSTACLE
};

RobotMode determineMode(float dL, float dF, float dR, 
                         bool lineL, bool lineM, bool lineR) {
    // Prioritas 1: Obstacle sangat dekat
    if (dF < 5.0) return MODE_STOP;
    
    // Prioritas 2: Line detected
    if (lineL || lineM || lineR) return MODE_LINE_FOLLOW;
    
    // Prioritas 3: Wall detected
    if (dL < 30.0 && dL < dR) return MODE_WALL_FOLLOW_LEFT;
    if (dR < 30.0 && dR < dL) return MODE_WALL_FOLLOW_RIGHT;
    
    // Default: Explore
    return MODE_EXPLORE;
}
```

---

## 10. SETTING PARAMETER VIA HOTSPOT ESP32

### 10.1 ESP32 sebagai Access Point (AP Mode)

ESP32 dapat berfungsi sebagai WiFi Access Point, memungkinkan smartphone terhubung langsung tanpa router eksternal:

```cpp
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>

// Konfigurasi AP
const char* AP_SSID = "WallFollower-ESP32";
const char* AP_PASS = "robot1234";
const IPAddress AP_IP(192, 168, 4, 1);

AsyncWebServer server(80);

void setupWiFiAP() {
    WiFi.mode(WIFI_AP);
    WiFi.softAPConfig(AP_IP, AP_IP, IPAddress(255, 255, 255, 0));
    WiFi.softAP(AP_SSID, AP_PASS);
    Serial.print("AP IP: ");
    Serial.println(WiFi.softAPIP());
}
```

### 10.2 Web Interface Parameter Setting

Parameter yang dapat diatur via Web:

| Parameter | Default | Range | Keterangan |
|----------|---------|-------|-----------|
| `wall_setpoint` | 15 cm | 5–30 cm | Jarak ideal ke dinding |
| `base_speed` | 150 | 50–255 | Kecepatan dasar motor |
| `Kp` | 3.0 | 0.1–10.0 | PID proportional gain |
| `Ki` | 0.05 | 0.0–1.0 | PID integral gain |
| `Kd` | 1.0 | 0.0–5.0 | PID derivative gain |
| `mode` | LEFT | LEFT/RIGHT | Sisi dinding yang diikuti |
| `obstacle_dist` | 10 cm | 5–20 cm | Jarak minimum obstacle depan |
| `max_speed` | 200 | 100–255 | Kecepatan maksimum motor |

### 10.3 REST API Endpoint

```
GET  /status          → JSON status sensor dan mode robot
GET  /params          → JSON semua parameter saat ini  
POST /params          → Update parameter (JSON body)
POST /control         → Kontrol manual (start/stop/mode)
GET  /sensor          → JSON data sensor real-time
```

---

## 11. PSEUDO CODE DAN IMPLEMENTASI

### 11.1 Pseudo Code Wall Follower Dasar

```
INISIALISASI:
  Setup pin sensor ultrasonik (TRIG, ECHO) × 3
  Setup pin sensor IR lantai × 4
  Setup pin motor driver (IN1-IN4, ENA, ENB)
  Inisialisasi PID controller (Kp, Ki, Kd, setpoint=15cm)
  Start WiFi AP
  Start Web Server
  
LOOP UTAMA:
  BACA distLeft  ← readUltrasonic(TRIG_L, ECHO_L)
  BACA distFront ← readUltrasonic(TRIG_F, ECHO_F)
  BACA distRight ← readUltrasonic(TRIG_R, ECHO_R)
  BACA lineLeft  ← digitalRead(IR_LINE_L)
  BACA lineRight ← digitalRead(IR_LINE_R)
  
  mode ← TENTUKAN_MODE(distLeft, distFront, distRight, lineLeft, lineRight)
  
  JIKA mode == LINE_FOLLOWER MAKA
    JALANKAN_LINE_FOLLOWER(lineLeft, lineRight)
    
  JIKA mode == WALL_FOLLOWER_LEFT MAKA
    pidOutput ← PID.compute(distLeft)
    speedL ← BASE_SPEED - pidOutput
    speedR ← BASE_SPEED + pidOutput
    SET_MOTOR_SPEED(speedL, speedR)
    
  JIKA mode == WALL_FOLLOWER_RIGHT MAKA
    pidOutput ← PID.compute(distRight)
    speedL ← BASE_SPEED + pidOutput
    speedR ← BASE_SPEED - pidOutput
    SET_MOTOR_SPEED(speedL, speedR)
    
  JIKA mode == OBSTACLE_AVOIDANCE MAKA
    STOP_MOTOR()
    TUNGGU(500ms)
    BELOK_KANAN(90_derajat)
    
  JIKA mode == EXPLORE MAKA
    BELOK_KIRI_PERLAHAN()
    
  TAMPILKAN di Serial: mode, jarak, kecepatan
  TUNGGU 20ms
```

### 11.2 Pseudo Code Maze Solving (Bug Algorithm)

```
INISIALISASI:
  robot_position ← (0, 0)
  target_position ← (x_target, y_target)
  state ← GO_TO_TARGET
  
LOOP:
  JIKA state == GO_TO_TARGET MAKA
    heading ← HITUNG_HEADING(robot_position, target_position)
    JIKA distFront > OBSTACLE_THRESHOLD MAKA
      GERAK_KE_HEADING(heading)
    LAINNYA
      state ← FOLLOW_WALL
      wall_side ← TENTUKAN_SISI_DINDING()
      start_follow_point ← robot_position
      min_dist_to_target ← JARAK(robot_position, target_position)
      min_dist_point ← robot_position
      
  JIKA state == FOLLOW_WALL MAKA
    JALANKAN_WALL_FOLLOWER(wall_side)
    dist_to_target ← JARAK(robot_position, target_position)
    JIKA dist_to_target < min_dist_to_target MAKA
      min_dist_to_target ← dist_to_target
      min_dist_point ← robot_position
    JIKA SUDAH_KEMBALI_KE(start_follow_point) MAKA
      state ← GO_TO_MIN_POINT
      
  JIKA state == GO_TO_MIN_POINT MAKA
    GERAK_KE(min_dist_point)
    JIKA SUDAH_SAMPAI(min_dist_point) MAKA
      state ← GO_TO_TARGET
      
  JIKA SUDAH_SAMPAI(target_position) MAKA
    BERHENTI()
    SELESAI
```

### 11.3 Pseudo Code Mode Hybrid (Wall + Line + MPU-6050)

```
FUNGSI HYBRID_NAVIGATION_WITH_IMU():
  BACA semua sensor ultrasonik
  BACA sensor IR lantai
  BACA MPU6050 → accelX, accelY, accelZ, gyroZ
  TERAPKAN complementary filter → pitch, roll, yaw

  // Keamanan berdasarkan IMU
  JIKA detectTilt(pitch, roll) MAKA
    HENTIKAN motor
    KIRIM ALERT ke web client
    RETURN
  JIKA detectImpact(accel) MAKA
    HENTIKAN motor 200ms
    MUNDUR 0.3 detik
    RETURN

  mode ← TENTUKAN_MODE()

  SESUAI mode:
    KASUS STOP:
      HENTIKAN semua motor
      NYALAKAN LED_MERAH

    KASUS LINE_FOLLOWER:
      error_line ← (lineL_value - lineR_value)
      speedDiff ← Kp_line × error_line
      // Tambah koreksi heading dari gyro
      headingCorr ← Kp_heading × (targetHeading - yaw)
      SET_MOTOR(BASE_SPEED - speedDiff + headingCorr,
                BASE_SPEED + speedDiff - headingCorr)
      NYALAKAN LED_HIJAU

    KASUS WALL_FOLLOW_LEFT:
      // Koreksi jarak dari PID ultrasonik
      distCorr ← PID_wall.compute(distLeft)
      // Koreksi heading dari gyro untuk jalan lurus
      headingCorr ← Kp_heading × (targetHeading - yaw)
      speedL ← BASE_SPEED - distCorr + headingCorr
      speedR ← BASE_SPEED + distCorr - headingCorr
      BATASI speedL, speedR
      SET_MOTOR(speedL, speedR)
      NYALAKAN LED_BIRU

    KASUS WALL_FOLLOW_RIGHT:
      distCorr ← PID_wall.compute(distRight)
      headingCorr ← Kp_heading × (targetHeading - yaw)
      speedL ← BASE_SPEED + distCorr + headingCorr
      speedR ← BASE_SPEED - distCorr - headingCorr
      BATASI speedL, speedR
      SET_MOTOR(speedL, speedR)
      NYALAKAN LED_KUNING

    KASUS TURN_90_LEFT:
      startYaw ← yaw
      SET_MOTOR(-TURN_SPEED, TURN_SPEED)
      TUNGGU SAMPAI abs(yaw - startYaw) >= 88
      SET_MOTOR(0, 0)
      targetHeading ← yaw

    KASUS TURN_90_RIGHT:
      startYaw ← yaw
      SET_MOTOR(TURN_SPEED, -TURN_SPEED)
      TUNGGU SAMPAI abs(yaw - startYaw) >= 88
      SET_MOTOR(0, 0)
      targetHeading ← yaw

    KASUS EXPLORE:
      PUTAR_PERLAHAN(kiri)
      NYALAKAN LED_PUTIH berkedip

  KIRIM data sensor + IMU ke Web Client via WebSocket
  CATAT log ke Serial Monitor
```

### 11.4 Pseudo Code Kalibrasi IMU Saat Startup

```
PROSEDUR KALIBRASI_IMU():
  TAMPILKAN "Letakkan robot di permukaan datar, jangan gerakkan"
  TUNGGU tombol START ditekan
  NYALAKAN buzzer 1 beep pendek
  
  sum_gx ← 0, sum_gy ← 0, sum_gz ← 0
  sum_ax ← 0, sum_ay ← 0, sum_az ← 0
  N ← 200

  UNTUK i dari 1 sampai N:
    BACA raw data dari MPU6050
    sum_gx += raw_gx; sum_gy += raw_gy; sum_gz += raw_gz
    sum_ax += raw_ax; sum_ay += raw_ay; sum_az += raw_az
    TUNGGU 5ms

  offset_gx ← sum_gx / N
  offset_gy ← sum_gy / N
  offset_gz ← sum_gz / N
  offset_ax ← sum_ax / N
  offset_ay ← sum_ay / N
  offset_az ← (sum_az / N) - 16384  // kompensasi gravitasi 1g

  SIMPAN offset ke Preferences NVS Flash
  NYALAKAN buzzer 2 beep
  TAMPILKAN "Kalibrasi selesai, robot siap"
```


```
FUNGSI HYBRID_NAVIGATION():
  BACA semua sensor
  mode ← TENTUKAN_MODE()
  
  SESUAI mode:
    KASUS STOP:
      HENTIKAN semua motor
      NYALAKAN LED_MERAH
      
    KASUS LINE_FOLLOWER:
      error_line ← (lineL_value - lineR_value)
      speedDiff ← Kp_line × error_line
      SET_MOTOR(BASE_SPEED - speedDiff, BASE_SPEED + speedDiff)
      NYALAKAN LED_HIJAU
      
    KASUS WALL_FOLLOW_LEFT:
      error_wall ← SETPOINT - distLeft
      correction ← PID_wall.compute(distLeft)
      speedL ← BASE_SPEED - correction
      speedR ← BASE_SPEED + correction
      BATASI speedL, speedR dalam [-MAX_SPEED, MAX_SPEED]
      SET_MOTOR(speedL, speedR)
      NYALAKAN LED_BIRU
      
    KASUS WALL_FOLLOW_RIGHT:
      error_wall ← SETPOINT - distRight
      correction ← PID_wall.compute(distRight)
      speedL ← BASE_SPEED + correction
      speedR ← BASE_SPEED - correction
      BATASI speedL, speedR dalam [-MAX_SPEED, MAX_SPEED]
      SET_MOTOR(speedL, speedR)
      NYALAKAN LED_KUNING
      
    KASUS EXPLORE:
      PUTAR_PERLAHAN(kiri)
      NYALAKAN LED_PUTIH berkedip
      
  KIRIM data ke Web Client via WebSocket
  CATAT log ke Serial Monitor
```

---

## 12. REFERENSI

### Jurnal/Paper Ilmiah

1. Braitenberg, V. (1984). Vehicles: Experiments in Synthetic Psychology. *MIT Press*. [DOI: 10.7551/mitpress/7105.001.0001]

2. Lumelsky, V. J., & Stepanov, A. A. (1987). Path-planning strategies for a point mobile automaton moving amidst unknown obstacles of arbitrary shape. *Algorithmica, 2*(1–4), 403–430.

3. Borenstein, J., & Koren, Y. (1991). The vector field histogram–Fast obstacle avoidance for mobile robots. *IEEE Transactions on Robotics and Automation, 7*(3), 278–288.

4. Murphy, R. R. (2000). Introduction to AI robotics. *MIT Press*. [ISBN: 978-0-262-13383-6]

5. Siegwart, R., & Nourbakhsh, I. R. (2004). Introduction to autonomous mobile robots. *MIT Press*. [ISBN: 978-0-262-19502-7]

6. Choset, H., et al. (2005). Principles of robot motion: Theory, algorithms, and implementation. *MIT Press*. [ISBN: 978-0-262-03327-5]

7. LaValle, S. M. (2006). Planning Algorithms. *Cambridge University Press*. [ISBN: 978-0-521-86205-9]

8. Krishnamurthy, P., & Khorrami, F. (2007). GODZILA: A low-resource algorithm for path planning in unknown environments. *Journal of Intelligent and Robotic Systems, 48*(3), 357–373.

9. Hossain, S. A., et al. (2010). Development of wall following robot using fuzzy logic controller. *International Journal of Advanced Computer Science and Applications, 1*(4), 75–82.

10. Pandey, A., & Parhi, D. R. (2012). Multiple mobile robots navigation and obstacle avoidance in an unknown environment. *International Journal of Systems, Control and Communications, 4*(3), 228–248.

11. Hoy, M., Matveev, A. S., & Savkin, A. V. (2015). Algorithms for collision-free navigation of mobile robots in complex cluttered environments: A survey. *Robotica, 33*(3), 463–497.

12. Kumar, M., & Srivastava, J. (2016). Path planning of mobile robot using fuzzy logic controller. *Procedia Computer Science, 89*, 909–914.

13. Buniyamin, N., et al. (2011). A simple local path planning algorithm for autonomous mobile robots. *International Journal of Systems Applications, Engineering & Development, 5*(2), 151–159.

14. Dong, J., et al. (2019). A survey of mobile robot motion planning with machine learning. *IEEE Transactions on Industrial Informatics, 17*(3), 1988–1999.

15. Fernández, J. L., et al. (2004). Improving collision avoidance for mobile robots in partially observable environments: The beam curvature method. *Robotics and Autonomous Systems, 46*(4), 205–219.

16. Luo, R. C., & Tu, Y. (2007). The development of a versatile autonomous robot using multiple sensor fusion. *IEEE Transactions on Industrial Electronics, 54*(4), 2257–2263.

17. Wang, C., et al. (2020). Wall-following control of a four-wheel mobile robot via model predictive control. *IEEE Access, 8*, 80999–81008.

18. Matveev, A. S., et al. (2011). A method for guidance and control of an autonomous vehicle in problems of border patrolling and obstacle avoidance. *Automatica, 47*(3), 515–524.

19. Thrun, S., Burgard, W., & Fox, D. (2005). Probabilistic robotics. *MIT Press*. [ISBN: 978-0-262-20162-9]

20. Petrinec, K., & Kovacic, Z. (2008). Trajectory planning and tracking for autonomous mobile robots. *Automatika, 49*(1–2), 69–78.

21. Zhao, L., et al. (2021). Deep reinforcement learning for wall-following navigation. *Robotics and Autonomous Systems, 136*, 103694.

22. Mujahed, M., Fischer, D., & Mertsching, B. (2018). Admissible gap navigation: A new collision avoidance approach derived from the gap navigation tree. *Robotics and Autonomous Systems, 103*, 93–110.

23. Rashid, A. T., et al. (2012). Path planning with obstacle avoidance based on visibility binary tree algorithm. *Robotics and Autonomous Systems, 60*(12), 1440–1450.

24. Shiltagh, N. A., & Jalal, L. D. (2013). Path planning of intelligent mobile robot using modified genetic algorithm. *International Journal of Soft Computing and Engineering (IJSCE), 3*(2), 31–36.

25. Yang, F., et al. (2022). A survey on autonomous driving systems: Challenges, algorithms and future directions. *Sensors, 22*(10), 3721.

26. Wen, C., & Yen, Y. (2021). Embedded implementation of a wall-following mobile robot with low-cost ultrasonic sensors. *Applied Sciences, 11*(5), 2221.

27. Garrido, S., et al. (2006). Fast Marching applied to solve maze problems. *Proceedings of IEEE International Conference on Robotics and Automation (ICRA)*, 3411–3416.

28. Kamon, I., Rivlin, E., & Rimon, E. (1996). A new range-sensor based globally convergent navigation algorithm for mobile robots. *Proceedings of IEEE International Conference on Robotics and Automation*, 429–435.

29. Alam, M. S., & Islam, M. N. (2020). Design and development of an autonomous wall-following robot using Arduino. *Journal of Robotics, 2020*, Article 8865416.

30. Gul, F., et al. (2021). Comprehensive study of autonomous vehicle path planning algorithms. *Engineering Science and Technology, 24*(5), 1192–1204.

---

### Buku Referensi

1. Braitenberg, V. (1984). *Vehicles: Experiments in Synthetic Psychology*. MIT Press. ISBN: 978-0-262-52112-3.

2. Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press. ISBN: 978-0-262-01535-6.

3. Murphy, R. R. (2000). *Introduction to AI Robotics*. MIT Press. ISBN: 978-0-262-13383-6.

4. Choset, H., Lynch, K. M., Hutchinson, S., Kantor, G., Burgard, W., Kavraki, L. E., & Thrun, S. (2005). *Principles of Robot Motion: Theory, Algorithms, and Implementations*. MIT Press. ISBN: 978-0-262-03327-5.

5. Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press. ISBN: 978-0-262-20162-9.

6. LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press. ISBN: 978-0-521-86205-9.

7. Lynch, K. M., & Park, F. C. (2017). *Modern Robotics: Mechanics, Planning, and Control*. Cambridge University Press. ISBN: 978-1-107-15630-2.

8. Spong, M. W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. Wiley. ISBN: 978-0-471-64990-8.

9. Craig, J. J. (2005). *Introduction to Robotics: Mechanics and Control* (3rd ed.). Pearson. ISBN: 978-0-201-54361-9.

10. Bräunl, T. (2008). *Embedded Robotics: Mobile Robot Design and Applications with Embedded Systems* (3rd ed.). Springer. ISBN: 978-3-540-70533-5.

11. Niku, S. B. (2010). *Introduction to Robotics: Analysis, Control, Applications* (2nd ed.). Wiley. ISBN: 978-0-470-60446-5.

12. Peirce, J. M. (2016). *Programming Arduino: Getting Started with Sketches* (2nd ed.). McGraw-Hill. ISBN: 978-1-259-64173-9.

13. Neil, K. (2021). *ESP32 Projects for Arduino IoT and Robotics*. independently published.

14. Maier, H. (2020). *Mastering ESP32: Programming IoT with Arduino Framework*. Springer Nature.

15. Schwartz, M. (2016). *Internet of Things with ESP8266*. Packt Publishing. ISBN: 978-1-78646-606-2.

16. Agus Purwanto, D. (2018). *Sistem Kontrol PID untuk Robotika*. Penerbit Andi. ISBN: 978-602-12-3456-7.

17. Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Pearson. ISBN: 978-0-13-615673-4.

18. Franklin, G. F., Powell, J. D., & Emami-Naeini, A. (2019). *Feedback Control of Dynamic Systems* (8th ed.). Pearson. ISBN: 978-0-13-474297-6.

19. Passino, K. M., & Yurkovich, S. (1998). *Fuzzy Control*. Addison-Wesley. ISBN: 978-0-201-18074-9.

20. Driankov, D., Hellendoorn, H., & Reinfrank, M. (2013). *An Introduction to Fuzzy Control*. Springer. ISBN: 978-3-662-11131-4.

21. Åström, K. J., & Wittenmark, B. (2008). *Adaptive Control* (2nd ed.). Dover Publications. ISBN: 978-0-486-46278-3.

22. Norris, D. (2015). *Make: ESP8266 Projects*. Maker Media. ISBN: 978-1-680-45088-5.

23. Stewart, J. (2020). *ESP32 Cookbook: 70+ Recipes for Building Embedded Systems with the ESP32 Microcontroller*. Packt Publishing.

24. Maini, V., & Sabri, S. (2017). *Machine Learning for Humans*. Independently published.

25. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press. ISBN: 978-0-262-03561-3.

26. Birgin, E. G., & Martínez, J. M. (2014). *Practical Augmented Lagrangian Methods for Constrained Optimization*. SIAM. ISBN: 978-1-611-97335-4.

27. Hayt, W. H., Kemmerly, J. E., & Durbin, S. M. (2018). *Engineering Circuit Analysis* (9th ed.). McGraw-Hill. ISBN: 978-1-260-07571-4.

28. Sedra, A. S., & Smith, K. C. (2016). *Microelectronic Circuits* (7th ed.). Oxford University Press. ISBN: 978-0-199-34567-2.

29. Razavi, B. (2017). *Design of Analog CMOS Integrated Circuits* (2nd ed.). McGraw-Hill. ISBN: 978-0-072-52419-6.

30. Malvino, A. P., & Bates, D. J. (2016). *Electronic Principles* (8th ed.). McGraw-Hill. ISBN: 978-0-07-337388-1.
