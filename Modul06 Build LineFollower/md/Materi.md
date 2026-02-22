# MATERI MODUL 06: BUILD LINE FOLLOWER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 06 – Build Line Follower  
**Platform:** ESP32 + PlatformIO  

---

## A. DASAR TEORI

### A.1 Pengantar Robot Line Follower

Robot line follower (pengikut garis) adalah jenis robot otonom yang mampu mendeteksi dan mengikuti jalur garis (biasanya garis hitam di atas permukaan putih atau sebaliknya) menggunakan sensor optik. Robot ini termasuk kategori mobile robot paling mendasar namun mengandung konsep fundamental robotika yang penting: persepsi sensor, pengolahan sinyal, algoritma kontrol, dan aktuasi.

**Prinsip kerja dasar:**
1. Sensor infrared (IR) mendeteksi perbedaan reflektansi antara garis hitam dan latar putih
2. Mikrokontroler membaca data sensor dan menentukan posisi relatif robot terhadap garis
3. Algoritma kontrol menghitung koreksi arah yang diperlukan
4. Motor DC dikendalikan untuk mengoreksi arah gerak robot

### A.2 Sensor Garis Infrared

#### A.2.1 Prinsip Deteksi Optik

Sensor garis bekerja berdasarkan prinsip refleksi cahaya infrared. Setiap pasangan sensor terdiri dari:
- **Emitter IR (LED Infrared 940nm):** Memancarkan cahaya infrared ke permukaan
- **Receiver IR (Photodiode/Phototransistor):** Mendeteksi intensitas cahaya IR yang dipantulkan

**Karakteristik refleksi:**
- Permukaan **putih** → memantulkan ~80-90% cahaya IR → tegangan output **rendah** (sensor aktif)
- Permukaan **hitam** → menyerap ~90-95% cahaya IR → tegangan output **tinggi** (sensor tidak aktif)

#### A.2.2 Rangkaian Sensor dengan Komparator

Pada PCB Line Follower yang dibuat di Modul 1, setiap sensor memiliki rangkaian:

```
LED IR (940nm) — R_seri (68Ω) — VCC (5V)
Photodioda — R_pulldown (10kΩ) — GND
Tegangan node → Komparator (opsional: LM393) atau langsung ke ADC ESP32
```

**Rumus tegangan photodioda:**
```
V_sensor = (R_pulldown / (R_photodioda + R_pulldown)) × VCC
```

Ketika permukaan gelap: R_photodioda naik → V_sensor turun
Ketika permukaan terang: R_photodioda turun → V_sensor naik

#### A.2.3 Konfigurasi 12 Sensor dengan 74HC165

PCB Sensor Line menggunakan 2× 74HC165 (shift register 8-bit parallel-in, serial-out) untuk multiplexing 12 sensor ke 3 pin SPI:

```
Sensor 1-8  → 74HC165 (U1) → SPI (CLK, MISO, CS)
Sensor 9-12 → 74HC165 (U2) → daisy-chain dari U1
```

**Pembacaan SPI 74HC165:**
```
1. CS (LOAD/PL) = LOW → latch data parallel ke register
2. CS = HIGH → enable shift
3. Clock 16 pulsa → baca 16 bit (byte atas = sensor 1-8, byte bawah = 9-16)
4. Ambil 12 bit pertama → status 12 sensor
```

### A.3 Mikrokontroler ESP32

#### A.3.1 Spesifikasi ESP32 untuk Line Follower

| Parameter | Nilai |
|-----------|-------|
| CPU | Xtensa dual-core 32-bit LX6, 240 MHz |
| Flash | 4 MB (modul WROOM) |
| SRAM | 520 KB |
| GPIO | 34 pin (input/output) |
| PWM channels | 16 channel LEDC hardware |
| ADC | 12-bit, 18 channel |
| SPI | 4 interface (HSPI, VSPI, dll.) |
| Operating voltage | 3.3V logic |
| Supply | 3.3–3.6V |

#### A.3.2 Pin Assignment untuk Line Follower

| Fungsi | ESP32 Pin | Keterangan |
|--------|-----------|-----------|
| SPI CLK (74HC165) | GPIO18 | VSPI CLK |
| SPI MISO (74HC165) | GPIO19 | VSPI MISO |
| SPI CS/LOAD | GPIO5 | Chip Select |
| Motor Kiri PWM | GPIO25 | LEDC PWM |
| Motor Kiri IN1 | GPIO26 | Arah motor |
| Motor Kiri IN2 | GPIO27 | Arah motor |
| Motor Kanan PWM | GPIO32 | LEDC PWM |
| Motor Kanan IN1 | GPIO33 | Arah motor |
| Motor Kanan IN2 | GPIO14 | Arah motor |
| OLED SDA | GPIO21 | I2C SDA (bus bersama MPU-6050) |
| OLED SCL | GPIO22 | I2C SCL (bus bersama MPU-6050) |
| MPU-6050 SDA | GPIO21 | I2C SDA (bus bersama OLED) |
| MPU-6050 SCL | GPIO22 | I2C SCL (bus bersama OLED) |
| MPU-6050 INT | GPIO34 | Interrupt (opsional) |
| Push Button START | GPIO4 | Input, pull-up |
| Push Button MODE | GPIO15 | Input, pull-up |
| LED Indikator | GPIO2 | Output |
| Buzzer | GPIO23 | PWM tone |

### A.4 Driver Motor L293D

#### A.4.1 Konfigurasi L293D

L293D adalah IC motor driver dual H-bridge yang dapat mengontrol 2 motor DC secara independen.

**Truth Table L293D untuk satu channel:**

| EN | IN1 | IN2 | Motor |
|----|-----|-----|-------|
| 1 | 0 | 0 | Brake (rem) |
| 1 | 0 | 1 | Mundur |
| 1 | 1 | 0 | Maju |
| 1 | 1 | 1 | Brake (rem) |
| 0 | X | X | Free-wheeling |

**Kontrol kecepatan dengan PWM:**
- Pin EN (Enable) dikendalikan dengan sinyal PWM
- Frekuensi PWM yang disarankan: 1 kHz – 20 kHz
- Duty cycle: 0–100% (0 = berhenti, 100% = kecepatan penuh)

#### A.4.2 Spesifikasi Kelistrikan

| Parameter | Nilai |
|-----------|-------|
| Tegangan supply motor (Vs) | 4.5V – 36V |
| Tegangan logik (Vss) | 5V |
| Arus output per channel | 600 mA (peak 1.2A) |
| Voltage drop tiap H-bridge | ~1.8V – 2V |
| Internal protection diodes | Tidak ada (perlu eksternal) |

### A.5 Sensor IMU MPU-6050

#### A.5.1 Pengantar MPU-6050

MPU-6050 adalah IC IMU (Inertial Measurement Unit) 6-DoF (Degree of Freedom) buatan InvenSense yang mengintegrasikan **3-axis gyroscope** dan **3-axis accelerometer** dalam satu chip berukuran 4×4×0.9 mm. Pada robot line follower, MPU-6050 memberikan informasi orientasi dan gerakan yang melengkapi data sensor garis.

| Parameter | Nilai |
|-----------|-------|
| Interface | I2C (400 kHz Fast Mode) |
| Alamat I2C | 0x68 (AD0=LOW) atau 0x69 (AD0=HIGH) |
| Supply voltage | 2.375V – 3.46V (gunakan 3.3V dari ESP32) |
| Gyroscope range | ±250 / ±500 / ±1000 / ±2000 °/s |
| Accelerometer range | ±2g / ±4g / ±8g / ±16g |
| ADC resolution | 16-bit per axis |
| Digital Motion Processor (DMP) | Built-in, mampu fusi sensor onboard |
| Konsumsi arus | 3.8 mA (normal), 5 µA (sleep) |
| Package | QFN-24 (chip), atau modul GY-521 |

#### A.5.2 Prinsip Kerja Sensor IMU

**Accelerometer:**
Mengukur akselerasi linear menggunakan prinsip massa-pegas pada skala MEMS. Ketika sensor mengalami akselerasi, massa proof defleksi relatif terhadap frame → perubahan kapasitansi → tegangan → nilai digital.

- Saat diam: membaca gravitasi bumi = ±1g pada sumbu vertikal
- Saat bergerak: membaca kombinasi akselerasi gerak + gravitasi
- Rumus sudut dari akselerasi (pitch/roll):
```
pitch = atan2(ay, sqrt(ax²+az²)) × (180/π)
roll  = atan2(-ax, az)           × (180/π)
```

**Gyroscope:**
Mengukur kecepatan sudut (angular velocity) dalam °/s menggunakan efek Coriolis pada massa getar MEMS.

- Output: laju perubahan sudut (bukan sudut absolut)
- Untuk mendapatkan sudut: integrasi terhadap waktu
```
angle_gyro += (gyro_rate / 131.0) × dt   // untuk ±250°/s range
```

- **Kelemahan:** drift (bias) — error terakumulasi seiring waktu

#### A.5.3 Complementary Filter

Untuk mendapatkan estimasi sudut yang akurat, digunakan **complementary filter** yang menggabungkan:
- Accelerometer: akurat jangka panjang tapi noisy saat bergerak
- Gyroscope: halus dan cepat tapi drift jangka panjang

```
alpha = 0.98  // trust factor untuk gyro (0 < alpha < 1)

angle = alpha * (angle + gyro_rate * dt) + (1 - alpha) * accel_angle
```

**Penjelasan:**
- `alpha × (angle + gyro_rate × dt)` = prediksi dari integras gyro (98%)
- `(1-alpha) × accel_angle` = koreksi dari accelerometer (2%)
- Nilai alpha = 0.98 setara dengan time constant filter 49 ms pada loop 10 ms

#### A.5.4 Aplikasi MPU-6050 pada Line Follower

| Aplikasi | Data Sensor | Manfaat |
|---------|------------|---------|
| Deteksi kemiringan (ramp) | Pitch angle dari accelerometer | Sesuaikan kecepatan di tanjakan/turunan |
| Koreksi yaw (straight correction) | Gyro Z-axis (yaw rate) | Robot tetap lurus tanpa drift |
| Deteksi getaran / permukaan | Akselerasi X/Y high-frequency | Monitor kualitas lintasan |
| Anti-terbalik | Roll/pitch >45° → stop | Keselamatan robot |
| Estimasi kecepatan sudut belok | Gyro Z pada tikungan | Kontrol kecepatan adaptif di belokan |
| Logging inertial data | Semua 6 axis | Analisis dan machine learning |

#### A.5.5 Koneksi MPU-6050 ke ESP32

MPU-6050 berbagi bus I2C dengan OLED SSD1306 (GPIO21=SDA, GPIO22=SCL):

```
MPU-6050     ESP32
VCC    →    3.3V
GND    →    GND
SDA    →    GPIO21 (bersama OLED)
SCL    →    GPIO22 (bersama OLED)
AD0    →    GND (I2C addr = 0x68)
INT    →    GPIO34 (interrupt, opsional)
```

> **Catatan:** OLED SSD1306 menggunakan alamat 0x3C, MPU-6050 menggunakan 0x68. Keduanya bisa aktif bersamaan di bus I2C yang sama karena alamat berbeda.

---

### A.6 Algoritma Kontrol Line Follower

#### A.5.1 Kontrol Binary (On-Off) Sederhana

Algoritma paling sederhana menggunakan logika biner: sensor di atas garis = 1, tidak di atas garis = 0.

**Kasus 2 sensor:**
```
IF kiri=1 AND kanan=0: belok kiri (motor kiri lambat/mundur)
IF kiri=0 AND kanan=1: belok kanan (motor kanan lambat/mundur)
IF kiri=1 AND kanan=1: lurus (garis di tengah)
IF kiri=0 AND kanan=0: cari garis (putar di tempat)
```

**Keterbatasan:** Gerakan tersentak-sentak (oscillasi), tidak halus.

#### A.5.2 Kontrol Proportional (P Controller)

Kontrol Proportional (P) menghitung **error posisi** berdasarkan pembacaan sensor dan menghasilkan output koreksi yang **proporsional** terhadap error tersebut.

**Konsep error:**
```
error = posisi_setpoint - posisi_robot_pada_garis
```

Untuk array sensor dengan posisi bobot:
```
sensor[0]=-5, sensor[1]=-3, sensor[2]=-1, sensor[3]=+1, sensor[4]=+3, sensor[5]=+5

posisi = Σ(nilai_sensor[i] × bobot[i]) / Σ(nilai_sensor[i])
error  = 0 - posisi  (setpoint = 0, di tengah)
```

**Output kontrol:**
```
koreksi = Kp × error
motor_kiri  = kecepatan_base + koreksi
motor_kanan = kecepatan_base - koreksi
```

#### A.5.3 Kontrol PID (Proportional-Integral-Derivative)

PID adalah algoritma kontrol umpan balik (feedback control) yang paling umum digunakan di industri. Mengkombinasikan tiga aksi:

**Proportional (P):** Bereaksi terhadap error saat ini
```
P = Kp × error
```

**Integral (I):** Memperbaiki error steady-state (akumulasi error masa lalu)
```
I = Ki × Σerror × dt
```

**Derivative (D):** Memprediksi dan meredam osilasi (laju perubahan error)
```
D = Kd × (error - error_sebelumnya) / dt
```

**Output PID:**
```
output = P + I + D
       = Kp×error + Ki×integral + Kd×(error-error_prev)/dt
```

**Tuning PID (Metode Ziegler-Nichols Manual):**
1. Set Ki=0, Kd=0
2. Naikkan Kp hingga robot berosilasi stabil (Ku = ultimate gain)
3. Catat periode osilasi (Tu)
4. Gunakan rumus: Kp=0.6Ku, Ki=2Kp/Tu, Kd=KpTu/8

#### A.5.4 Fuzzy Logic Controller

Fuzzy Logic menggunakan aturan linguistik ("JIKA error BESAR KIRI MAKA belok CEPAT KIRI") untuk menghasilkan kontrol yang lebih intuitif dan robust.

**Fungsi keanggotaan error:**
- NL (Negatif Besar): -1 sd -0.6
- NM (Negatif Sedang): -0.8 sd -0.2
- NS (Negatif Kecil): -0.4 sd 0
- ZE (Nol): -0.2 sd +0.2
- PS (Positif Kecil): 0 sd +0.4
- PM (Positif Sedang): +0.2 sd +0.8
- PL (Positif Besar): +0.6 sd +1

**Contoh Rule Base:**
```
IF error=NL THEN output=PL (belok kiri kencang)
IF error=NM THEN output=PM (belok kiri sedang)
IF error=NS THEN output=PS (belok kiri sedikit)
IF error=ZE THEN output=ZE (lurus)
IF error=PS THEN output=NS (belok kanan sedikit)
IF error=PM THEN output=NM (belok kanan sedang)
IF error=PL THEN output=NL (belok kanan kencang)
```

---

## B. MATERI LENGKAP

### B.1 Menyolder PCB Line Follower

#### B.1.1 Persiapan Alat Solder

**Alat yang dibutuhkan:**

| Alat | Spesifikasi | Fungsi |
|------|-----------|--------|
| Solder iron | 60W, temperature-controlled | Memanaskan solder |
| Solder wire | 63/37 timah-timbal, diameter 0.8mm | Material solder |
| Flux pasta | No-clean rosin flux | Membersihkan oksidasi, bantu alir solder |
| Solder wick | 2.5mm/3mm lebar | Menyedot solder berlebih |
| Solder sucker | Pompa vakum | Alternatif solder wick |
| Helping hands | Dengan kaca pembesar | Memegang PCB saat solder |
| PCB holder | Vise / papan kayu | Stabilisasi PCB |
| Multimeter | Digital | Cek koneksi setelah solder |
| Isopropyl alcohol | 99% IPA | Membersihkan flux residue |
| Sikat kecil/toothbrush | — | Membersihkan PCB |

#### B.1.2 Pengaturan Suhu Solder

| Jenis Solder | Suhu Kerja | Keterangan |
|-------------|-----------|------------|
| Sn63/Pb37 (leaded) | 320–370°C | Standard, mudah mengalir |
| SAC305 (lead-free) | 360–400°C | Ramah lingkungan, sedikit lebih sulit |
| Pasta solder SMD | Reflow 240°C puncak | Untuk komponen SMD reflow |

> **Tips:** Solder iron yang terlalu dingin menyebabkan cold joint (sambungan buruk). Terlalu panas merusak komponen dan PCB. Gunakan 350°C untuk komponen through-hole standar.

#### B.1.3 Urutan Solder Komponen PCB Line Follower

**Prinsip: Solder komponen terendah dahulu, tertinggi terakhir**

**Langkah 1: Komponen SMD (jika ada pada PCB)**
1. Oleskan flux pasta ke pad SMD
2. Taruh komponen dengan pinset (tangan jangan menyentuh pad)
3. Solder satu sisi dulu untuk fiksasi (tack)
4. Solder sisi lainnya
5. Cek dengan multimeter: tidak ada short antar pad

**Langkah 2: Resistor (Through-Hole)**
1. Tekuk kaki resistor dengan jarak = jarak lubang PCB
2. Masukkan kaki ke lubang PCB
3. Tekuk kaki di bawah PCB sedikit (~30°) agar tidak jatuh
4. Panaskan pad + kaki dengan solder iron (2-3 detik)
5. Sentuhkan solder wire ke persimpangan kaki+pad (BUKAN ke tip solder iron)
6. Solder mengalir → angkat solder wire → angkat iron
7. Biarkan mendingin 3-5 detik (jangan ditiup!)
8. Potong kaki dengan wire cutter, sisakan ~0.5-1mm

**Langkah 3: Kapasitor dan LED**
- Perhatikan **polaritas**:
  - Kapasitor elektrolit: kaki panjang = (+), kaki pendek = (-)
  - LED: kaki panjang = anode (+), kaki pendek = katode (-)
- LED IR dan photodiode harus menghadap ke BAWAH (ke lahan)

**Langkah 4: IC (Shift Register 74HC165)**
1. Luruskan kaki IC jika bengkok (taruh di permukaan datar, tekan perlahan)
2. Masukkan IC ke socket atau langsung ke PCB
3. Solder kaki diagonal dulu (pin 1 dan pin 9) untuk fiksasi
4. Solder semua pin dengan cepat (maks. 3 detik per pin)
5. Cek: tidak ada solder bridge (short) antar pin

**Langkah 5: Konektor dan Header**
1. Masukkan konektor, tahan dengan jari atau tape
2. Solder satu pin untuk fiksasi
3. Cek posisi sudah lurus dan tegak lurus PCB
4. Solder semua pin

#### B.1.4 Tips dan Trik Menyolder

**✅ DO (Lakukan):**
- Jaga ujung solder iron (tip) selalu bersih dan berlapis solder tipis (tin-on)
- Bersihkan tip dengan sponge basah atau brass wire cleaner setiap beberapa solder
- Panaskan pad PCB DAN kaki komponen sebelum menambahkan solder
- Gunakan flux tambahan untuk pad yang sulit (oksidasi)
- Periksa dengan kaca pembesar setelah selesai menyolder area
- Bersihkan flux residue dengan IPA dan sikat

**❌ DON'T (Jangan):**
- Jangan solder terlalu lama (>5 detik) di satu titik → merusak komponen
- Jangan menyentuh tip solder ke kaki IC yang sensitif panas
- Jangan meniup solder cair → cold joint + berbahaya
- Jangan menggerakkan komponen saat solder belum dingin
- Jangan memaksakan solder cair dengan mengoleskan ke tip lalu ke PCB (globbing)
- Jangan biarkan flux residue → korosif dalam jangka panjang

**Ciri Solder yang Baik (Good Solder Joint):**
- Permukaan mengkilap dan halus
- Bentuk seperti gunung kecil (concave cone)
- Kaki komponen terlihat jelas di dalam solder
- Tidak ada void (lubang udara)

**Ciri Solder yang Buruk (Bad Solder Joint):**
- **Cold joint:** Suram/keruh, mudah retak, kontak tidak sempurna
- **Solder bridge:** Solder menyambungkan 2 pad yang harusnya terpisah
- **Insufficient solder:** Terlalu sedikit solder, kontak lemah
- **Tombstoning:** Komponen SMD berdiri karena ketidakseimbangan panas

#### B.1.5 Troubleshooting Soldering

| Masalah | Penyebab | Solusi |
|---------|---------|--------|
| Cold joint | Suhu terlalu rendah / komponen bergerak | Tambah flux, panaskan lagi |
| Solder bridge | Terlalu banyak solder / pad terlalu dekat | Gunakan solder wick untuk menyedot kelebihan |
| Tidak bisa solder | Pad teroksidasi / flux habis | Bersihkan dengan flux + gosok halus |
| IC terlalu panas | Iron terlalu lama di pin | Tunggu dingin, cek IC masih berfungsi |
| PCB gosong | Suhu terlalu tinggi | Turunkan suhu, gunakan heat sink clip |

### B.2 Assembly Mekanik Robot Line Follower

#### B.2.1 Komponen Mekanik

| Komponen | Spesifikasi | Fungsi |
|---------|-----------|--------|
| Chassis robot | Akrilik/PCB/3D print, min 120×150mm | Rangka utama |
| Motor DC | 3-6V, 100-300 RPM (dengan gear) | Penggerak roda |
| Roda | Diameter 60-80mm, lebar 20mm | Pergerakan |
| Ball caster / roda depan | 1 inch | Penyeimbang depan |
| Standoff M3 | 10mm, 20mm, 30mm | Jarak antar layer |
| Baut M3×8 | — | Pengikat |
| Baut M3×12 | — | Pengikat panjang |
| Motor bracket | Aluminium/plastik | Dudukan motor |
| PCB spacer | Nylon M3 | Isolasi PCB |
| Baterai LiPo 2S | 7.4V 2000mAh | Sumber daya |
| Strap baterai | Velcro | Pengikat baterai |

#### B.2.2 Layout Fisik Robot

```
         [PCB Sensor Line 130mm]  ← Posisi paling bawah, ujung depan
                  |
    [Bracket Motor Kiri] [Bracket Motor Kanan]
         [Roda Kiri]       [Roda Kanan]
                  |
            [Chassis Akrilik]
                  |
         [PCB MAIN (ESP32)]      ← Layer tengah
                  |
          [Baterai LiPo 2S]      ← Layer bawah/belakang
                  |
          [Ball Caster]          ← Penyeimbang belakang
```

#### B.2.3 Langkah Assembly Mekanik

**Step 1: Pasang Motor ke Bracket**
1. Masukkan motor DC ke bracket motor
2. Kencangkan dengan baut M3 (jangan terlalu kencang → crush motor body)
3. Pasang roda ke shaft motor (press fit atau set screw)
4. Tes: putar roda dengan tangan, harus bebas berputar

**Step 2: Pasang Motor+Bracket ke Chassis**
1. Posisikan bracket motor di sisi kiri-kanan chassis
2. Motor menghadap ke dalam chassis
3. Kencangkan baut M3×12
4. Pastikan kedua roda sejajar (tidak miring/toe-in/toe-out)

**Step 3: Pasang Ball Caster**
1. Ball caster dipasang di belakang chassis (berlawanan arah PCB sensor)
2. Gunakan standoff untuk menyamakan tinggi dengan roda
3. Tinggi ball caster = tinggi roda – 2mm (sedikit lebih rendah agar roda menapak)

**Step 4: Pasang PCB MAIN**
1. Gunakan standoff nylon M3×10mm di 4 sudut PCB
2. Pasang PCB di layer tengah chassis
3. Orientasikan konektor ke arah yang mudah diakses

**Step 5: Pasang PCB Sensor Line**
1. PCB Sensor Line dipasang di bawah depan chassis
2. Jarak sensor ke permukaan lahan: **5–15mm** (optimal 8-10mm)
3. Gunakan bracket aluminium L atau 3D print untuk mount
4. Kabel flat IDC 10-pin menghubungkan ke PCB MAIN

**Step 6: Routing Kabel**
1. Kabel motor: from L293D connector → motor (cukup panjang untuk memutar)
2. Kabel sensor: flat cable IDC menempel rapi di chassis
3. Gunakan cable tie untuk mengatur kabel
4. Pastikan tidak ada kabel yang menyentuh roda

**Step 7: Pasang Baterai**
1. LiPo 2S di posisi tengah/belakang chassis (untuk balance CG)
2. Gunakan velcro strap
3. Konektor XT30 atau JST ke PCB MAIN

#### B.2.4 Tips Assembly Mekanik

- **Keseimbangan (balance):** Pusat massa robot harus sedekat mungkin ke sumbu roda. Baterai yang berat sebaiknya di belakang sumbu roda sedikit agar roda traksi baik.
- **Tinggi sensor:** Terlalu rendah → sensor tersangkut permukaan; terlalu tinggi → area deteksi membesar, akurasi turun. Optimal: 8-10mm.
- **Kesejajaran roda:** Roda harus sejajar (parallel) dan tegak lurus chassis. Cek dengan penggaris.
- **Kabel fleksibel:** Gunakan kabel yang cukup panjang dan fleksibel antara PCB MAIN dan sensor board agar tidak putus saat berbelok.
- **Anti-getaran:** Gunakan washer nylon di antara motor dan bracket untuk meredam getaran.

### B.3 Pemrograman ESP32 dengan PlatformIO

#### B.3.1 Setup PlatformIO

**Instalasi:**
1. Install Visual Studio Code dari https://code.visualstudio.com
2. Buka VS Code → Extensions → cari "PlatformIO IDE" → Install
3. Tunggu instalasi selesai → restart VS Code

**Buat Project Baru:**
1. Klik ikon PlatformIO di sidebar kiri
2. **PIO Home > New Project**
3. Isi:
   - Name: `LineFollower_ESP32`
   - Board: `Espressif ESP32 Dev Module`
   - Framework: `Arduino`
   - Location: pilih folder
4. Klik **Finish**

**Struktur Project:**
```
LineFollower_ESP32/
├── .pio/
├── include/
│   └── config.h          ← Konfigurasi pin dan parameter
├── lib/
├── src/
│   └── main.cpp          ← Program utama
├── test/
└── platformio.ini        ← Konfigurasi PlatformIO
```

**platformio.ini untuk ESP32:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
upload_speed = 921600
lib_deps =
    adafruit/Adafruit SSD1306@^2.5.7
    adafruit/Adafruit GFX Library@^1.11.9
    electroniccats/MPU6050@^1.3.0
```

#### B.3.2 Library yang Digunakan

| Library | Fungsi | Install via PlatformIO |
|---------|--------|----------------------|
| Arduino ESP32 | Core framework | Built-in |
| Adafruit SSD1306 | OLED display | `adafruit/Adafruit SSD1306` |
| Adafruit GFX | Grafik OLED | `adafruit/Adafruit GFX Library` |
| Wire | I2C komunikasi | Built-in |
| SPI | SPI komunikasi | Built-in |
| ESP32 LEDC | Hardware PWM | Built-in |

#### B.3.3 Program Dasar Line Follower

**File: include/config.h**
```cpp
#pragma once

// ===== PIN KONFIGURASI =====
// SPI untuk 74HC165 (Sensor Line)
#define PIN_SPI_CLK     18
#define PIN_SPI_MISO    19
#define PIN_SPI_CS      5

// Motor Kiri (L293D Channel 1)
#define PIN_MOTOR_L_EN  25   // PWM Enable
#define PIN_MOTOR_L_IN1 26   // Arah 1
#define PIN_MOTOR_L_IN2 27   // Arah 2

// Motor Kanan (L293D Channel 2)
#define PIN_MOTOR_R_EN  32   // PWM Enable
#define PIN_MOTOR_R_IN1 33   // Arah 1
#define PIN_MOTOR_R_IN2 14   // Arah 2

// OLED I2C (berbagi bus dengan MPU-6050)
#define PIN_OLED_SDA    21
#define PIN_OLED_SCL    22

// MPU-6050 IMU (I2C, berbagi bus dengan OLED)
#define MPU6050_ADDR    0x68   // AD0=GND
#define PIN_MPU_INT     34     // Interrupt (opsional)

// Tombol dan indikator
#define PIN_BTN_START   4
#define PIN_BTN_MODE    15
#define PIN_LED         2
#define PIN_BUZZER      23

// ===== PARAMETER MOTOR =====
#define PWM_FREQ        5000   // Frekuensi PWM (Hz)
#define PWM_RESOLUTION  8      // Resolusi bit (0-255)
#define PWM_CH_LEFT     0      // LEDC channel motor kiri
#define PWM_CH_RIGHT    1      // LEDC channel motor kanan

// ===== PARAMETER KONTROL =====
#define NUM_SENSORS     12     // Jumlah sensor
#define BASE_SPEED      150    // Kecepatan dasar (0-255)
#define MAX_SPEED       200    // Kecepatan maksimum
#define MIN_SPEED       0      // Kecepatan minimum

// Bobot posisi sensor (kiri negatif, kanan positif)
const int SENSOR_WEIGHT[12] = {-55, -45, -35, -25, -15, -5, 5, 15, 25, 35, 45, 55};
```

**File: src/main.cpp (Program Dasar)**
```cpp
#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "config.h"

// OLED
#define OLED_WIDTH 128
#define OLED_HEIGHT 64
Adafruit_SSD1306 oled(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

// Variabel sensor
uint16_t sensorRaw = 0;        // 12-bit raw sensor data
bool sensorState[NUM_SENSORS]; // Status tiap sensor (true=hitam)
int sensorPosition = 0;        // Posisi estimasi (-550 to +550)

// Variabel PID
float Kp = 0.15, Ki = 0.0, Kd = 0.8;
float error = 0, lastError = 0, integral = 0;
float pidOutput = 0;

// State robot
bool running = false;

// ===== FUNGSI MOTOR =====
void motorSetup() {
  ledcSetup(PWM_CH_LEFT, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CH_RIGHT, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(PIN_MOTOR_L_EN, PWM_CH_LEFT);
  ledcAttachPin(PIN_MOTOR_R_EN, PWM_CH_RIGHT);
  
  pinMode(PIN_MOTOR_L_IN1, OUTPUT);
  pinMode(PIN_MOTOR_L_IN2, OUTPUT);
  pinMode(PIN_MOTOR_R_IN1, OUTPUT);
  pinMode(PIN_MOTOR_R_IN2, OUTPUT);
}

void motorLeft(int speed) {
  speed = constrain(speed, -255, 255);
  if (speed >= 0) {
    digitalWrite(PIN_MOTOR_L_IN1, HIGH);
    digitalWrite(PIN_MOTOR_L_IN2, LOW);
    ledcWrite(PWM_CH_LEFT, speed);
  } else {
    digitalWrite(PIN_MOTOR_L_IN1, LOW);
    digitalWrite(PIN_MOTOR_L_IN2, HIGH);
    ledcWrite(PWM_CH_LEFT, -speed);
  }
}

void motorRight(int speed) {
  speed = constrain(speed, -255, 255);
  if (speed >= 0) {
    digitalWrite(PIN_MOTOR_R_IN1, HIGH);
    digitalWrite(PIN_MOTOR_R_IN2, LOW);
    ledcWrite(PWM_CH_RIGHT, speed);
  } else {
    digitalWrite(PIN_MOTOR_R_IN1, LOW);
    digitalWrite(PIN_MOTOR_R_IN2, HIGH);
    ledcWrite(PWM_CH_RIGHT, -speed);
  }
}

void motorStop() {
  motorLeft(0);
  motorRight(0);
}

// ===== FUNGSI SENSOR =====
uint16_t readSensors() {
  uint16_t data = 0;
  
  // Latch data parallel ke 74HC165
  digitalWrite(PIN_SPI_CS, LOW);
  delayMicroseconds(1);
  digitalWrite(PIN_SPI_CS, HIGH);
  
  // Baca 16 bit via SPI (2x 74HC165 = 16 bit, ambil 12 bit)
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  byte high = SPI.transfer(0xFF);
  byte low  = SPI.transfer(0xFF);
  SPI.endTransaction();
  
  data = ((uint16_t)high << 8) | low;
  data >>= 4; // Ambil 12 bit teratas
  return data & 0x0FFF;
}

int calculatePosition(uint16_t sensors) {
  long weightedSum = 0;
  int activeCount = 0;
  
  for (int i = 0; i < NUM_SENSORS; i++) {
    if (sensors & (1 << (NUM_SENSORS - 1 - i))) {
      weightedSum += SENSOR_WEIGHT[i];
      activeCount++;
      sensorState[i] = true;
    } else {
      sensorState[i] = false;
    }
  }
  
  if (activeCount == 0) return sensorPosition; // Pertahankan posisi terakhir
  return (int)(weightedSum / activeCount);
}

// ===== FUNGSI PID =====
float computePID(float currentError) {
  integral += currentError;
  integral = constrain(integral, -100, 100); // Anti-windup
  
  float derivative = currentError - lastError;
  float output = Kp * currentError + Ki * integral + Kd * derivative;
  
  lastError = currentError;
  return output;
}

// ===== SETUP =====
void setup() {
  Serial.begin(115200);
  
  // Pin setup
  pinMode(PIN_BTN_START, INPUT_PULLUP);
  pinMode(PIN_BTN_MODE, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  
  // SPI
  SPI.begin(PIN_SPI_CLK, PIN_SPI_MISO, -1, PIN_SPI_CS);
  pinMode(PIN_SPI_CS, OUTPUT);
  digitalWrite(PIN_SPI_CS, HIGH);
  
  // Motor
  motorSetup();
  
  // OLED
  Wire.begin(PIN_OLED_SDA, PIN_OLED_SCL);
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("SSD1306 allocation failed");
  }
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setTextColor(SSD1306_WHITE);
  oled.setCursor(0, 0);
  oled.println("Line Follower v1.0");
  oled.println("Press START...");
  oled.display();
  
  Serial.println("Line Follower Ready");
}

// ===== LOOP UTAMA =====
void loop() {
  // Tombol START
  if (digitalRead(PIN_BTN_START) == LOW) {
    delay(50); // Debounce
    running = !running;
    if (!running) motorStop();
    digitalWrite(PIN_LED, running);
    delay(300);
  }
  
  if (!running) {
    // Mode idle: tampilkan status sensor
    sensorRaw = readSensors();
    Serial.print("Sensors: ");
    Serial.println(sensorRaw, BIN);
    delay(100);
    return;
  }
  
  // Baca sensor
  sensorRaw = readSensors();
  sensorPosition = calculatePosition(sensorRaw);
  
  // Hitung PID
  error = 0 - sensorPosition; // Setpoint = 0 (tengah)
  pidOutput = computePID(error);
  
  // Hitung kecepatan motor
  int leftSpeed  = BASE_SPEED + (int)pidOutput;
  int rightSpeed = BASE_SPEED - (int)pidOutput;
  
  // Clamp kecepatan
  leftSpeed  = constrain(leftSpeed,  MIN_SPEED, MAX_SPEED);
  rightSpeed = constrain(rightSpeed, MIN_SPEED, MAX_SPEED);
  
  // Gerakkan motor
  motorLeft(leftSpeed);
  motorRight(rightSpeed);
  
  // Debug serial
  Serial.printf("Pos:%4d | Err:%6.1f | PID:%6.1f | L:%3d R:%3d\n",
                sensorPosition, error, pidOutput, leftSpeed, rightSpeed);
  
  // Update OLED (setiap 200ms agar tidak lambat)
  static unsigned long lastDisplay = 0;
  if (millis() - lastDisplay > 200) {
    oled.clearDisplay();
    oled.setCursor(0, 0);
    oled.printf("Pos: %d", sensorPosition);
    oled.setCursor(0, 10);
    oled.printf("Err: %.1f", error);
    oled.setCursor(0, 20);
    oled.printf("L:%d R:%d", leftSpeed, rightSpeed);
    oled.display();
    lastDisplay = millis();
  }
  
  delay(10); // Loop rate ~100Hz
}
```

---

## C. CONTOH PSEUDO CODE DAN PENJELASAN

### C.1 Pseudo Code Algoritma Umum Line Follower

```
MULAI

INISIALISASI:
  setup_pin_motor()
  setup_pin_sensor()
  setup_SPI()
  setup_OLED()
  tampilkan "Siap, tekan START"

LOOP UTAMA:
  JIKA tombol_START ditekan MAKA
    toggle(status_running)
  AKHIR JIKA

  JIKA status_running == FALSE MAKA
    hentikan_motor()
    tampilkan_status_sensor()
    LANJUTKAN ke LOOP UTAMA
  AKHIR JIKA

  // Fase deteksi
  data_sensor = baca_sensor_12bit_via_SPI()
  posisi_garis = hitung_posisi_weighted(data_sensor)

  // Fase kontrol
  error = setpoint - posisi_garis  // setpoint = 0 (tengah)
  output_PID = hitung_PID(error, Kp, Ki, Kd)

  // Fase aktuasi
  kecepatan_kiri  = kecepatan_base + output_PID
  kecepatan_kanan = kecepatan_base - output_PID
  clamp(kecepatan_kiri,  MIN, MAX)
  clamp(kecepatan_kanan, MIN, MAX)
  gerakkan_motor(kecepatan_kiri, kecepatan_kanan)

  // Fase monitoring
  kirim_data_serial()
  update_OLED()
  tunggu(10ms)

ULANGI LOOP UTAMA

SELESAI
```

**Penjelasan pseudo code:**
1. **Inisialisasi:** Dilakukan sekali di awal (fungsi `setup()` di Arduino). Menyiapkan semua peripheral.
2. **Toggle running:** Tombol START mengubah status ON/OFF robot tanpa perlu reset.
3. **Baca sensor:** Data 12-bit dibaca via SPI dari shift register 74HC165.
4. **Hitung posisi:** Weighted average memberikan nilai negatif = garis di kiri, positif = garis di kanan.
5. **Hitung PID:** Menghasilkan koreksi berdasarkan error, akumulasi, dan laju perubahan.
6. **Aktuasi motor:** Kecepatan dikurangi/ditambah berlawanan untuk berbelok.
7. **Monitoring:** Serial print dan OLED untuk debugging.

### C.2 Pseudo Code Pembacaan Sensor 74HC165

```
FUNGSI baca_sensor():
  // Latch data: ubah CS dari HIGH ke LOW ke HIGH
  SET CS = LOW
  TUNGGU 1 mikrodetik
  SET CS = HIGH

  // Baca 2 byte via SPI (16 bit, ambil 12 bit)
  byte_tinggi = SPI_transfer(0xFF)  // Sensor 1-8
  byte_rendah = SPI_transfer(0xFF)  // Sensor 9-16 (hanya pakai 4 bit)

  // Gabungkan menjadi 16-bit
  data_16bit = (byte_tinggi << 8) OR byte_rendah

  // Ambil 12 bit pertama (MSB)
  data_12bit = data_16bit >> 4

  // Kembalikan 12 bit masker
  KEMBALIKAN (data_12bit AND 0x0FFF)

AKHIR FUNGSI
```

**Penjelasan:**
- 74HC165 bekerja dengan **parallel load**: CS LOW mengambil semua data 8-pin sekaligus
- Kemudian **serial shift**: CLK pulsa memindahkan data satu bit per CLK
- ESP32 SPI otomatis menghasilkan 8 CLK per byte transfer
- Dua byte = 16 CLK = cukup untuk dua 74HC165 daisy-chain

### C.3 Pseudo Code Weighted Position

```
FUNGSI hitung_posisi(data_12bit):
  bobot = [-55, -45, -35, -25, -15, -5, +5, +15, +25, +35, +45, +55]
  jumlah_bobot = 0
  jumlah_aktif = 0

  UNTUK i dari 0 sampai 11:
    bit_sensor = (data_12bit >> (11 - i)) AND 1
    JIKA bit_sensor == 1:  // Sensor mendeteksi garis
      jumlah_bobot += bobot[i]
      jumlah_aktif += 1
    AKHIR JIKA
  AKHIR UNTUK

  JIKA jumlah_aktif == 0:
    KEMBALIKAN posisi_terakhir  // Garis hilang: pertahankan
  AKHIR JIKA

  KEMBALIKAN jumlah_bobot / jumlah_aktif

AKHIR FUNGSI
```

**Penjelasan:**
- Bobot negatif untuk sensor kiri, positif untuk kanan
- Weighted average menghasilkan posisi kontinu, bukan diskrit
- Jika tidak ada sensor aktif (garis hilang), pertahankan posisi terakhir (last known position)
- Nilai 0 = garis tepat di tengah, nilai ±55 = garis di ujung kiri/kanan

### C.4 Pseudo Code PID Controller

```
VARIABEL GLOBAL:
  error_sebelumnya = 0
  integral = 0
  Kp, Ki, Kd = nilai tuning

FUNGSI hitung_PID(error_sekarang):
  // Komponen Proportional
  P = Kp * error_sekarang

  // Komponen Integral (dengan anti-windup)
  integral = integral + error_sekarang
  integral = clamp(integral, -100, +100)  // Anti-windup
  I = Ki * integral

  // Komponen Derivative
  derivative = error_sekarang - error_sebelumnya
  D = Kd * derivative

  // Simpan error untuk iterasi berikutnya
  error_sebelumnya = error_sekarang

  // Output total
  KEMBALIKAN P + I + D

AKHIR FUNGSI
```

**Penjelasan:**
- **P:** Semakin besar error, semakin besar koreksi. Jika Kp terlalu besar → osilasi.
- **I:** Memperbaiki error sistematis yang tidak teratasi P saja. Anti-windup mencegah integral terlalu besar saat garis hilang lama.
- **D:** Meredam osilasi dengan memprediksi tren error. Jika Kd terlalu besar → noise-sensitive.

### C.5 Pseudo Code Kontrol Fuzzy Logic

```
FUNGSI fuzzy_control(error, delta_error):
  // Fuzzifikasi
  derajat_keanggotaan = fuzzifikasi(error, delta_error)

  // Inferensi (Rule Base)
  UNTUK setiap rule dalam rule_base:
    aktivasi = MIN(derajat[rule.input_error], derajat[rule.input_delta])
    output_rule[i] = (aktivasi, rule.output_label)
  AKHIR UNTUK

  // Defuzzifikasi (Centroid method)
  pembilang = 0
  penyebut  = 0
  UNTUK setiap output_label:
    nilai_tengah = centroid(output_label)
    aktivasi_total = MAX dari semua rule dengan label ini
    pembilang += aktivasi_total * nilai_tengah
    penyebut  += aktivasi_total
  AKHIR UNTUK

  JIKA penyebut == 0:
    KEMBALIKAN 0
  KEMBALIKAN pembilang / penyebut

AKHIR FUNGSI
```

### C.6 Pseudo Code MPU-6050 Complementary Filter

```
INISIALISASI:
  I2C_begin(SDA=21, SCL=22)
  MPU6050_init(addr=0x68)
  kalibrasi_gyro_offset()   // Rata-rata 1000 sample saat diam
  sudut_pitch = 0, sudut_roll = 0, sudut_yaw_rate = 0

FUNGSI baca_mpu():
  data_raw = I2C_read_14_bytes(0x68)  // Accel(6) + Temp(2) + Gyro(6)
  
  ax = data_raw[0..1] / 16384.0   // Skala ±2g
  ay = data_raw[2..3] / 16384.0
  az = data_raw[4..5] / 16384.0
  
  gx = (data_raw[8..9]  - offset_gx) / 131.0   // Skala ±250°/s
  gy = (data_raw[10..11] - offset_gy) / 131.0
  gz = (data_raw[12..13] - offset_gz) / 131.0
  
  // Sudut dari accelerometer
  pitch_accel = atan2(ay, sqrt(ax²+az²)) × (180/π)
  roll_accel  = atan2(-ax, az) × (180/π)
  
  // Complementary filter
  dt = waktu_sekarang - waktu_sebelumnya  // detik
  sudut_pitch = 0.98 × (sudut_pitch + gy × dt) + 0.02 × pitch_accel
  sudut_roll  = 0.98 × (sudut_roll  + gx × dt) + 0.02 × roll_accel
  sudut_yaw_rate = gz  // Hanya laju, tidak ada referensi absolut
  
  KEMBALIKAN (sudut_pitch, sudut_roll, sudut_yaw_rate)

AKHIR FUNGSI
```

**Penjelasan:**
- `baca_14_bytes` membaca akselerometer, temperatur, dan gyroscope sekaligus dari register 0x3B (burst read)
- Kalibrasi offset dilakukan satu kali di awal: rata-rata bacaan saat robot diam
- Complementary filter: 98% percaya gyro (cepat, halus), 2% percaya accelerometer (koreksi drift)

### C.7 Pseudo Code Yaw Rate Correction

```
FUNGSI kontrol_dengan_imu():
  // Baca sensor garis
  posisi_garis = hitung_posisi(baca_sensor())
  
  // Baca IMU
  (pitch, roll, yaw_rate) = baca_mpu()
  
  // Deteksi kemiringan (ramp)
  JIKA abs(pitch) > 15:
    // Robot di tanjakan/turunan
    faktor_kecepatan = cos(pitch × π/180)  // Kurangi kecepatan
  LAINNYA:
    faktor_kecepatan = 1.0
  AKHIR JIKA
  
  // PID garis
  error_garis = 0 - posisi_garis
  output_pid  = hitung_PID(error_garis)
  
  // Koreksi yaw: jika robot berputar sendiri tanpa belokan garis → koreksi
  // Hanya aktif ketika garis lurus (error kecil)
  JIKA abs(error_garis) < 10:
    Kyaw = 0.5
    koreksi_yaw = Kyaw × yaw_rate
  LAINNYA:
    koreksi_yaw = 0
  AKHIR JIKA
  
  // Gabungkan
  motor_kiri  = (kecepatan_base + output_pid + koreksi_yaw) × faktor_kecepatan
  motor_kanan = (kecepatan_base - output_pid - koreksi_yaw) × faktor_kecepatan
  
  clamp(motor_kiri,  MIN_SPEED, MAX_SPEED)
  clamp(motor_kanan, MIN_SPEED, MAX_SPEED)
  gerakkan_motor(motor_kiri, motor_kanan)

AKHIR FUNGSI
```

**Penjelasan:**
- Ketika robot di garis lurus (error kecil), gyroscope Z (yaw rate) mendeteksi rotasi tak terduga (slip, angin, permukaan tidak rata) → koreksi aktif.
- Di tikungan (error besar), koreksi yaw dinonaktifkan agar tidak mengganggu kontrol PID garis.
- `cos(pitch)` memberikan faktor kecepatan: pitch=0° → faktor=1.0; pitch=30° → faktor=0.866.

---



### D.1 Jurnal dan Paper (30 Referensi)

1. Dong, J., et al. (2023). "Line Following Robot Navigation Using Improved PID Control Algorithm." *IEEE Transactions on Industrial Electronics*, 70(4), 3821–3830.

2. Supriyono, H., & Riyadi, M.A. (2022). "Optimization of PID Parameters for Line Follower Robot Using Genetic Algorithm." *Journal of Physics: Conference Series*, 2193, 012042.

3. Rahman, M., et al. (2021). "Fuzzy Logic Based Line Following Robot with Obstacle Avoidance." *International Journal of Robotics and Automation*, 36(2), 114–123.

4. Yilmaz, A., & Ozturk, S. (2022). "Adaptive PID Control for High-Speed Line Following Robots." *Mechatronics*, 85, 102817.

5. Li, Z., et al. (2023). "Deep Reinforcement Learning for Autonomous Line Following in Unstructured Environments." *Robotics and Autonomous Systems*, 161, 104340.

6. Kurniawan, D., et al. (2022). "Performance Comparison of P, PD, PI, and PID Controllers for Mobile Robot Line Following." *TELKOMNIKA Telecommunication, Computing, Electronics and Control*, 20(1), 45–53.

7. Wang, H., & Zhang, Y. (2021). "Neural Network-Based Line Following Control for Mobile Robots." *Neural Computing and Applications*, 33(8), 3421–3433.

8. Patel, R., et al. (2023). "ESP32-Based Autonomous Line Following Robot with Real-Time Monitoring via Wi-Fi." *Microprocessors and Microsystems*, 96, 104728.

9. Santoso, B., et al. (2022). "Implementation of Cascade PID Controller for Line Follower Robot on Curved Track." *Indonesian Journal of Electrical Engineering and Computer Science*, 25(3), 1421–1430.

10. Kim, J., & Park, S. (2021). "Optimal Control of Line Following Robot Using Model Predictive Control." *Journal of Intelligent and Robotic Systems*, 103(4), 67.

11. Ahmad, N., et al. (2023). "Infrared Sensor Array Calibration for Robust Line Detection in Line Following Robots." *Sensors*, 23(5), 2641.

12. Zeng, Q., et al. (2022). "Fast Line-Following Robot Using Predictive Control and Sensor Fusion." *IEEE Robotics and Automation Letters*, 7(2), 3156–3163.

13. Mohan, R., et al. (2021). "Comparative Analysis of Digital Controller Designs for Line Follower Robots." *Control Engineering Practice*, 115, 104891.

14. Fikri, M.A., et al. (2023). "Design and Implementation of Line Following Robot Competition System Using PlatformIO Framework." *Jurnal Elektronika dan Telekomunikasi*, 23(1), 18–26.

15. Cheng, X., et al. (2022). "Sliding Mode Control for Line Following Mobile Robots." *Robotics and Autonomous Systems*, 148, 103937.

16. Oktariawan, I., et al. (2021). "Performance Analysis of Line Follower Robot with Proportional Controller on Various Track Curvatures." *Journal of Mechatronics, Electrical Power, and Vehicular Technology*, 12(2), 88–96.

17. Srivastava, A., et al. (2023). "Machine Learning Approach for Adaptive Speed Control in Line Follower Robots." *Expert Systems with Applications*, 218, 119617.

18. Chen, L., & Liu, W. (2022). "Multi-Sensor Fusion for Improved Line Detection in Mobile Robots." *IEEE Sensors Journal*, 22(8), 7842–7851.

19. Ibrahim, D., et al. (2021). "Microcontroller-Based PID Control of DC Motor for Line Following Application." *Advances in Engineering Software*, 160, 103050.

20. Nurhayati, S., et al. (2023). "IoT-Enabled Line Follower Robot with Remote Monitoring Using ESP32 and MQTT." *Indonesian Journal of Electrical Engineering and Informatics*, 11(2), 312–322.

21. Zhang, F., et al. (2022). "Optimization of Sensor Placement for Line Following Robot Using Genetic Algorithm." *Applied Soft Computing*, 118, 108453.

22. Saputra, E., et al. (2021). "Implementasi Kontroler PID Digital pada Robot Line Follower Berbasis Arduino." *Jurnal Nasional Teknik Elektro*, 10(2), 96–104.

23. Hussain, A., et al. (2023). "Robust Line Following Using Edge Detection and H-Bridge Motor Driver." *Robotica*, 41(3), 875–890.

24. Prawiroredjo, K., & Dodit, S. (2022). "Comparison of Heuristic and Analytical PID Tuning Methods for Line Follower Robot." *Jurnal Teknik Elektro*, 14(2), 55–63.

25. Yang, T., et al. (2021). "High-Speed Omnidirectional Line Following Robot with Visual Feedback." *Optics and Lasers in Engineering*, 147, 106720.

26. Ramirez, C., et al. (2023). "Energy-Efficient Path Planning for Line Following Robots in Warehouse Applications." *Journal of Manufacturing Systems*, 68, 123–135.

27. Mardiyah, N.A., et al. (2022). "Desain dan Implementasi Robot Line Follower dengan Kontrol Fuzzy-PID." *Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)*, 6(4), 661–669.

28. Liu, H., et al. (2021). "Adaptive Gain Scheduling PID for Line Following on Dynamic Environments." *Control Theory and Technology*, 19(3), 287–298.

29. Setiawan, J.D., et al. (2023). "Performance Evaluation of Line Follower Robot on Intersecting Track using State Machine Algorithm." *JITCE (Journal of Information Technology and Computer Engineering)*, 7(1), 22–30.

30. Ferreira, P., et al. (2022). "Low-Cost Educational Line Following Robot Platform for Teaching Control Systems." *International Journal of Engineering Education*, 38(4), 983–995.

### D.2 Buku Referensi (30 Referensi)

1. Siegwart, R., Nourbakhsh, I.R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.

2. Murphy, R.R. (2019). *Introduction to AI Robotics* (2nd ed.). MIT Press.

3. Craig, J.J. (2017). *Introduction to Robotics: Mechanics and Control* (4th ed.). Pearson.

4. Corke, P. (2017). *Robotics, Vision and Control: Fundamental Algorithms in MATLAB* (2nd ed.). Springer.

5. Braunl, T. (2008). *Embedded Robotics: Mobile Robot Design and Applications with Embedded Systems* (3rd ed.). Springer.

6. Nehmzow, U. (2003). *Mobile Robotics: A Practical Introduction* (2nd ed.). Springer.

7. Bräunl, T. (2021). *EyeBot: Mobile Robots for Research and Education*. Springer.

8. Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Prentice Hall.

9. Franklin, G.F., Powell, J.D., & Emami-Naeini, A. (2018). *Feedback Control of Dynamic Systems* (8th ed.). Pearson.

10. Astrom, K.J., & Wittenmark, B. (2013). *Computer-Controlled Systems: Theory and Design* (3rd ed.). Dover Publications.

11. Passino, K.M., & Yurkovich, S. (1998). *Fuzzy Control*. Addison-Wesley.

12. Mamdani, E.H., & Assilian, S. (1975). *An Experiment in Linguistic Synthesis with a Fuzzy Logic Controller*. Academic Press.

13. Sutton, R.S., & Barto, A.G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.

14. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.

15. Horowitz, P., & Hill, W. (2015). *The Art of Electronics* (3rd ed.). Cambridge University Press.

16. Sedra, A.S., & Smith, K.C. (2020). *Microelectronic Circuits* (8th ed.). Oxford University Press.

17. Boylestad, R.L. (2015). *Electronic Devices and Circuit Theory* (11th ed.). Pearson.

18. Axelson, J. (2011). *USB Complete: The Developer's Guide* (5th ed.). Lakeview Research.

19. Kaplan, R. (2014). *Embedded Systems: An Integrated Approach*. Pearson Education India.

20. Barr, M., & Massa, A. (2006). *Programming Embedded Systems: With C and GNU Development Tools* (2nd ed.). O'Reilly Media.

21. Monk, S. (2022). *Programming the ESP32: Learning MicroPython*. McGraw-Hill.

22. Schwartz, M. (2016). *Internet of Things with ESP8266*. Packt Publishing.

23. Kolban, N. (2018). *Kolban's Book on ESP32*. Leanpub.

24. Banzi, M., & Shiloh, M. (2022). *Getting Started with Arduino* (4th ed.). Maker Media.

25. Blum, J. (2019). *Exploring Arduino: Tools and Techniques for Engineering Wizardry* (2nd ed.). Wiley.

26. Margolis, M. (2020). *Arduino Cookbook* (3rd ed.). O'Reilly Media.

27. Buono, M. (2014). *Practical Electronics for Inventors* (4th ed.). McGraw-Hill.

28. Scherz, P., & Monk, S. (2016). *Practical Electronics for Inventors* (4th ed.). McGraw-Hill.

29. Petriu, E.M. (2005). *Instrumentation and Measurement in Electrical Engineering*. Boca Raton: CRC Press.

30. Ziegler, J.G., & Nichols, N.B. (1942/Reprinted 2003). *Optimum Settings for Automatic Controllers*. ASME Press.

---

*Materi ini merupakan dokumen resmi Praktikum Mekatronika dan Robotika. Diperbarui sesuai kurikulum Prodi Teknologi Rekayasa Otomasi.*
