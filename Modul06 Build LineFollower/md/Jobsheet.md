# JOBSHEET MODUL 06: BUILD LINE FOLLOWER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 06 – Build Line Follower  
**Platform:** ESP32 + PlatformIO  
**Pertemuan:** 11–12 (2 × 2 SKS)  
**Tanggal:** ___________________  
**Nama Kelompok:** ___________________  
**Anggota:**

| No | Nama | NIM |
|----|------|-----|
| 1  |      |     |
| 2  |      |     |
| 3  |      |     |
| 4  |      |     |

---

## A. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menyolder PCB Line Follower hasil desain Modul 01 sesuai dengan teknik soldering yang benar
2. Melakukan assembly mekanik robot line follower termasuk mounting motor, sensor board, dan baterai
3. Menyiapkan project ESP32 menggunakan PlatformIO IDE di Visual Studio Code
4. Membaca data sensor garis (12 sensor via 74HC165 SPI) pada ESP32
5. Mengimplementasikan algoritma kontrol binary (on-off) sebagai dasar line following
6. Mengimplementasikan algoritma kontrol Proportional (P) dengan weighted position
7. Mengimplementasikan algoritma kontrol PD dan PID untuk performa yang lebih baik
8. Melakukan tuning parameter kontrol (Kp, Ki, Kd) secara sistematis
9. Menampilkan data sensor dan status robot pada OLED SSD1306
10. Mendokumentasikan hasil percobaan dan menganalisis pengaruh parameter terhadap performa robot

---

## B. CAPAIAN PEMBELAJARAN MATA KULIAH (CPMK)

| Kode | Kompetensi |
|------|-----------|
| CPMK1 | Mampu menyolder PCB elektronika dan melakukan quality control hasil soldering |
| CPMK2 | Mampu melakukan assembly mekanik robot mobile secara sistematis |
| CPMK3 | Mampu memprogram mikrokontroler ESP32 menggunakan PlatformIO dengan framework Arduino |
| CPMK4 | Mampu mengimplementasikan dan men-tuning kontroler PID pada sistem robot mobile |
| CPMK5 | Mampu menganalisis performa sistem kontrol berdasarkan data eksperimen |

---

## C. ALAT DAN BAHAN

### C.1 Perangkat Keras

| No | Komponen | Spesifikasi | Qty | Keterangan |
|----|---------|-----------|-----|-----------|
| 1 | PCB MAIN | Dari Modul 01, ESP32-S2, L293D, LM2596 | 1 set | Sudah jadi dari JLCPCB |
| 2 | PCB Sensor Line | Dari Modul 01, 12 sensor IR, 74HC165×2 | 1 set | Sudah jadi dari JLCPCB |
| 3 | Komponen THT PCB MAIN | ESP32, L293D, resistor, kapasitor, dsb. | 1 set | BOM dari Modul 01 |
| 4 | Komponen THT Sensor | LED IR, photodioda, resistor | 1 set | BOM dari Modul 01 |
| 5 | Motor DC | 3-6V, 150 RPM dengan gearbox | 2 buah | Kiri dan kanan |
| 6 | Roda | Diameter 65mm | 2 buah | |
| 7 | Ball caster | 1 inch | 1 buah | |
| 8 | Chassis robot | Akrilik 3mm, 150×120mm | 1 buah | |
| 9 | Baterai LiPo 2S | 7.4V 2000mAh | 1 buah | |
| 10 | Kabel IDC 10-pin | Flat cable, 20cm | 1 buah | PCB MAIN ↔ Sensor |

### C.2 Peralatan Solder

| No | Alat | Spesifikasi | Qty |
|----|------|-----------|-----|
| 1 | Solder iron | 60W, adjustable temperature | 1 |
| 2 | Solder wire | Sn63/Pb37, 0.8mm, rosin core | 1 rol |
| 3 | Flux pasta | No-clean rosin flux | 1 pot |
| 4 | Solder wick | 2.5mm | 1 rol |
| 5 | Wire cutter | Flush cutter | 1 |
| 6 | Helping hands / PCB vise | — | 1 |
| 7 | Multimeter | Digital, auto-range | 1 |
| 8 | Isopropyl alcohol 99% | — | secukupnya |
| 9 | Kuas kecil/sikat gigi | — | 1 |
| 10 | Kaca pembesar | 5× minimal | 1 |

### C.3 Peralatan Assembly

| No | Alat | Qty |
|----|------|-----|
| 1 | Obeng set (Phillips dan Flathead) | 1 set |
| 2 | Tang lancip (needlenose plier) | 1 |
| 3 | Kunci hex set (M3) | 1 set |
| 4 | Baut dan standoff M3 (berbagai panjang) | 1 set |
| 5 | Cable tie (zip tie) kecil | 10 buah |
| 6 | Double-sided tape | 1 rol |
| 7 | Penggaris 30cm | 1 |

### C.4 Perangkat Lunak

| No | Software | Fungsi | Cara Install |
|----|---------|--------|-------------|
| 1 | Visual Studio Code | IDE utama | https://code.visualstudio.com |
| 2 | PlatformIO IDE | Extension VS Code untuk ESP32 | VS Code → Extensions → PlatformIO |
| 3 | Driver USB ESP32 | CH340 atau CP2102 | Sesuai chip USB-UART di board |
| 4 | Git (opsional) | Version control kode | https://git-scm.com |

---

## D. DASAR TEORI SINGKAT

### D.1 Sistem Robot Line Follower

Robot line follower terdiri dari 4 subsistem utama:
1. **Sensor:** 12× sensor IR (LED + photodioda) dibaca via SPI (74HC165)
2. **Kontroler:** ESP32 menjalankan algoritma kontrol
3. **Aktuator:** 2× motor DC dikontrol L293D H-Bridge dengan PWM
4. **Power:** Baterai LiPo 2S (7.4V) → LM2596 (5V) → supply semua komponen

### D.2 Weighted Position

Posisi garis dihitung dengan **weighted average** dari 12 sensor:
```
posisi = Σ(bobot[i] × sensor[i]) / Σ(sensor[i])
```
Bobot sensor dari kiri ke kanan: -55, -45, -35, -25, -15, -5, +5, +15, +25, +35, +45, +55

### D.3 Algoritma PID

```
error   = 0 - posisi_garis
output  = Kp×error + Ki×integral(error) + Kd×d(error)/dt
motor_L = base_speed + output
motor_R = base_speed - output
```

**Tuning awal yang disarankan:** Kp = 0.15, Ki = 0.0, Kd = 0.8

### D.4 Kontrol Motor dengan LEDC PWM

ESP32 menggunakan hardware LEDC (LED Control) untuk PWM motor:
```cpp
ledcSetup(channel, freq, resolution);  // Setup channel
ledcAttachPin(pin, channel);            // Attach ke pin
ledcWrite(channel, duty);               // Set duty cycle (0-255)
```

---

## E. LANGKAH KERJA

---

### SESI 1: SOLDERING PCB (Estimasi: 90 menit)

---

#### LANGKAH 1: Persiapan Soldering

**Estimasi waktu: 10 menit**

1. Siapkan PCB MAIN dan PCB Sensor Line (hasil order Modul 01)
2. Buka BOM Modul 01, siapkan semua komponen di tray terpisah per jenis
3. Panaskan solder iron ke **350°C**
4. Bersihkan tip dengan sponge basah atau brass wire cleaner
5. Tin the tip: sentuh solder ke tip → lapisi tipis → lap bersih
6. Siapkan helping hands/PCB vise, flux pasta, dan solder wick

> **✅ Checkpoint:** Solder iron panas, tip bersih dan berlapis timah tipis.

---

#### LANGKAH 2: Solder PCB Sensor Line

**Estimasi waktu: 40 menit**

**Urutan soldering (terendah dahulu):**

**2a. Resistor SMD 0805 (jika ada):**
- Oleskan flux ke pad SMD
- Taruh komponen dengan pinset
- Solder satu sisi (tack), cek posisi, solder sisi lain

**2b. Resistor Through-Hole:**
- R_IR: 68Ω (12 buah, seri dengan LED IR)
- R_photo: 10kΩ (12 buah, pull-down photodioda)
- Teknik: masukkan → tekuk kaki → panaskan pad+kaki → sentuh solder → dinginkan → potong

**2c. LED Infrared 940nm (12 buah):**
- ⚠️ **PERHATIAN POLARITAS:** Kaki panjang = Anode (+) → ke resistor
- ⚠️ **PERHATIAN ORIENTASI:** LED menghadap ke BAWAH (ke permukaan lahan)
- Cek: nyalakan sementara → LED IR tidak terlihat mata tapi terlihat di kamera HP

**2d. Photodioda (12 buah):**
- ⚠️ **PERHATIAN POLARITAS:** Kaki panjang = Katode (negatif)
- ⚠️ **ORIENTASI:** Menghadap ke BAWAH, sejajar dengan LED IR
- Jarak LED-Photodioda harus konsisten antar pasangan

**2e. IC 74HC165 (2 buah):**
- Luruskan kaki IC jika bengkok
- Masukkan ke PCB, solder pin 1 dan pin 9 dulu (diagonal fixation)
- Solder semua pin dengan cepat (<3 detik per pin)
- ⚠️ Cek solder bridge: gunakan kaca pembesar, cek antar pin IC

**2f. Konektor IDC 10-pin (2 buah):**
- Masukkan, pastikan tegak lurus PCB
- Solder satu pin fixation → cek lurus → solder semua pin

**Checklist soldering PCB Sensor:**
- [ ] Semua 12 resistor 68Ω tersolder
- [ ] Semua 12 resistor 10kΩ tersolder
- [ ] Semua 12 LED IR tersolder (polaritas dan orientasi benar)
- [ ] Semua 12 photodioda tersolder (polaritas dan orientasi benar)
- [ ] 2× IC 74HC165 tersolder tanpa solder bridge
- [ ] 2× konektor IDC tersolder lurus

> **✅ Checkpoint:** Visual inspection dengan kaca pembesar — tidak ada solder bridge, semua komponen terpasang dengan orientasi benar.

---

#### LANGKAH 3: Solder PCB MAIN

**Estimasi waktu: 40 menit**

**Urutan soldering:**

**3a. Komponen SMD (jika ada):**
- Kapasitor decoupling 100nF (0805) dekat setiap IC
- Resistor SMD

**3b. Komponen Through-Hole Kecil:**
- Resistor pull-up push button (10kΩ)
- Resistor LED indikator (100Ω)
- Kapasitor elektrolit filter (perhatikan polaritas! kaki panjang = +)

**3c. Transistor 2N2222 (driver buzzer):**
- Perhatikan orientasi flat-side transistor sesuai silkscreen PCB

**3d. Dioda 1N4007 (flyback L293D):**
- ⚠️ POLARITAS: garis pada dioda = Katode (-)

**3e. IC L293D:**
- Pin 1 biasanya ditandai titik atau notch pada IC
- Solder dengan metode diagonal fixation

**3f. Regulator LM2596:**
- Package TO-263 (SMD) atau TO-220 (THT) → sesuaikan dengan PCB
- Pastikan heatsink/thermal pad terpasang jika diperlukan

**3g. Push button, LED, buzzer:**
- Semua komponen ini relatif mudah, pastikan polaritas LED benar

**3h. Konektor (terminal block, pin header, JST):**
- Terminal block motor: pastikan terarah sesuai silk screen (L/R motor)
- Pin header untuk modul: OLED, HC-SR04, servo

**3i. Modul ESP32-S2:**
- Jika menggunakan pin header (modul bisa dilepas): solder header dulu, pasang modul
- Jika disolder langsung: hati-hati memanaskan pad modul terlalu lama

**3j. Modul LM2596 / AMS1117 (jika sebagai modul):**
- Solder ke pin header pada PCB

**Checklist soldering PCB MAIN:**
- [ ] Kapasitor decoupling tersolder dekat setiap IC
- [ ] L293D tersolder, tidak ada solder bridge
- [ ] LM2596/regulator tersolder dengan benar
- [ ] ESP32 tersolder atau di-seat pada header dengan benar
- [ ] Semua konektor tersolder lurus
- [ ] Semua LED dan dioda berorientasi benar

> **✅ Checkpoint:** PCB MAIN selesai disolder. Bersihkan flux residue dengan IPA + sikat.

---

#### LANGKAH 4: Testing PCB Sebelum Dinyalakan

**Estimasi waktu: 10 menit**

1. **Cek short circuit supply:** Gunakan multimeter mode resistansi, ukur antara pin VCC dan GND pada PCB. Nilai harus **> 100Ω** (bukan 0 atau sangat rendah)
2. **Cek kontinuitas jalur penting:** Trace dari pin ESP32 GPIO ke L293D, dari SPI CS ke 74HC165
3. **Visual check terakhir:** Kaca pembesar, pastikan tidak ada solder bridge
4. **Bersihkan PCB:** IPA + sikat → keringkan

| Pengukuran | Nilai Normal | Nilai Terukur | Status |
|-----------|-------------|--------------|--------|
| Resistansi VCC-GND PCB MAIN | >100Ω | | ☐ OK ☐ Short! |
| Resistansi VCC-GND Sensor | >100Ω | | ☐ OK ☐ Short! |
| Kontinuitas SPI CLK | Menyambung | | ☐ OK ☐ Putus |
| Kontinuitas SPI MISO | Menyambung | | ☐ OK ☐ Putus |

> **✅ Checkpoint:** Tidak ada short circuit, jalur kritis terhubung. Aman untuk dinyalakan.

---

### SESI 2: ASSEMBLY MEKANIK (Estimasi: 60 menit)

---

#### LANGKAH 5: Assembly Motor dan Roda

**Estimasi waktu: 15 menit**

1. Pasang motor DC ke bracket motor dengan baut M3×8
   - Jangan terlalu kencang (dapat menghancurkan body motor plastik)
   - Pastikan shaft motor benar-benar lurus
2. Pasang roda ke shaft motor
   - Press fit atau gunakan set screw (baut kecil pada hub roda)
   - Tes: putar roda dengan tangan → harus bebas berputar, tidak goyang
3. Pasang bracket motor + roda ke chassis
   - Posisi: kiri dan kanan, simetris
   - Gunakan baut M3×12 + washer

**Data pengamatan:**

| Motor | Putaran Bebas (RPM estimasi) | Kondisi |
|-------|---------------------------|---------|
| Motor Kiri | | ☐ Normal ☐ Berat ☐ Macet |
| Motor Kanan | | ☐ Normal ☐ Berat ☐ Macet |

---

#### LANGKAH 6: Assembly Ball Caster dan Chassis

**Estimasi waktu: 10 menit**

1. Tentukan posisi ball caster: **belakang chassis** (berlawanan dengan sensor)
2. Ukur tinggi roda utama dari permukaan (A mm)
3. Pilih standoff ball caster agar tinggi ball caster = A - 1mm (sedikit lebih rendah)
4. Pasang ball caster dengan baut M3

| Tinggi roda utama (A) | Tinggi ball caster dipilih | Selisih |
|----------------------|--------------------------|---------|
| mm | mm | mm |

---

#### LANGKAH 7: Mount PCB MAIN

**Estimasi waktu: 10 menit**

1. Tentukan posisi PCB MAIN di chassis (area tengah)
2. Tandai lubang baut dengan spidol
3. Bor atau gunakan lubang yang sudah ada di chassis akrilik
4. Pasang standoff nylon M3×10 di 4 titik
5. Pasang PCB MAIN di atas standoff, kencangkan dengan baut M3

> **Tips:** Gunakan standoff **nylon** (bukan metal) untuk menghindari short circuit antara PCB dan chassis konduktif.

---

#### LANGKAH 8: Mount PCB Sensor Line

**Estimasi waktu: 15 menit**

1. Tentukan posisi mounting di depan bawah chassis
2. Target jarak sensor ke permukaan lahan: **8–10 mm**
3. Buat bracket L dari aluminium atau 3D print (jika tersedia)
4. Pasang sensor board dengan baut M3, atur jarak dengan standoff
5. Ukur jarak aktual dengan penggaris

| Sensor | Jarak ke Permukaan (mm) | Target (8-10mm) |
|--------|------------------------|-----------------|
| Kiri (sensor 1) | | ☐ OK ☐ Perlu adjust |
| Tengah (sensor 6-7) | | ☐ OK ☐ Perlu adjust |
| Kanan (sensor 12) | | ☐ OK ☐ Perlu adjust |

---

#### LANGKAH 9: Routing Kabel dan Final Assembly

**Estimasi waktu: 10 menit**

1. Sambungkan kabel flat IDC 10-pin: PCB Sensor → PCB MAIN
   - ⚠️ Pastikan orientasi pin 1 ke pin 1 (biasanya ditandai segitiga/merah pada kabel)
2. Sambungkan kabel motor: terminal block PCB MAIN → motor
   - Kiri: ke Motor Kiri, kanan: ke Motor Kanan
3. Sambungkan kabel baterai ke konektor PCB MAIN
4. Ikat kabel dengan cable tie agar tidak mengenai roda
5. **Tes terakhir:** Putar semua roda dengan tangan → tidak ada kabel tersangkut

**Checklist assembly:**
- [ ] Kedua motor terpasang dan roda berputar bebas
- [ ] Ball caster terpasang, tinggi sesuai
- [ ] PCB MAIN terpasang dengan standoff nylon
- [ ] PCB Sensor terpasang, jarak 8-10mm dari permukaan
- [ ] Kabel IDC terhubung dengan orientasi benar
- [ ] Kabel motor terhubung
- [ ] Semua kabel rapih, tidak mengenai roda

> **✅ Checkpoint:** Robot secara mekanik sudah siap. Foto robot dari depan, atas, dan samping.

---

### SESI 3: SETUP PROGRAM DAN PERCOBAAN (Estimasi: 100 menit)

---

#### LANGKAH 10: Setup PlatformIO dan Project Baru

**Estimasi waktu: 15 menit**

1. Buka VS Code → klik ikon PlatformIO di sidebar kiri
2. Klik **New Project**:
   - Name: `LineFollower_Kelompok[X]`
   - Board: `Espressif ESP32 Dev Module`
   - Framework: Arduino
3. Edit `platformio.ini`:
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
```
4. PlatformIO akan otomatis download library → tunggu selesai
5. Buat file `include/config.h` dengan semua define pin (lihat Materi.md)

> **✅ Checkpoint:** Project terbuat, library terinstall, `config.h` sudah dibuat.

---

#### LANGKAH 11: Upload Program Test Sensor

**Estimasi waktu: 15 menit**

Buat program sederhana untuk memverifikasi pembacaan semua 12 sensor:

```cpp
#include <Arduino.h>
#include <SPI.h>
#include "config.h"

void setup() {
  Serial.begin(115200);
  SPI.begin(PIN_SPI_CLK, PIN_SPI_MISO, -1, PIN_SPI_CS);
  pinMode(PIN_SPI_CS, OUTPUT);
  digitalWrite(PIN_SPI_CS, HIGH);
  Serial.println("=== Sensor Test ===");
}

void loop() {
  // Latch data
  digitalWrite(PIN_SPI_CS, LOW);
  delayMicroseconds(1);
  digitalWrite(PIN_SPI_CS, HIGH);
  
  // Baca 2 byte
  SPI.beginTransaction(SPISettings(1000000, MSBFIRST, SPI_MODE0));
  uint8_t hi = SPI.transfer(0xFF);
  uint8_t lo = SPI.transfer(0xFF);
  SPI.endTransaction();
  
  uint16_t data = ((uint16_t)hi << 8 | lo) >> 4;
  
  // Tampilkan binary
  Serial.print("Sensors: ");
  for (int i = 11; i >= 0; i--) {
    Serial.print((data >> i) & 1);
  }
  Serial.println();
  delay(100);
}
```

**Catat hasil pengujian sensor:**

| Sensor # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---------|---|---|---|---|---|---|---|---|---|----|----|-----|
| Nilai saat di atas PUTIH | | | | | | | | | | | | |
| Nilai saat di atas HITAM | | | | | | | | | | | | |
| Status | | | | | | | | | | | | |

> **✅ Checkpoint:** Semua 12 sensor merespons (berbeda antara di atas hitam dan putih).

---

#### LANGKAH 12: PERCOBAAN 1 – Binary Line Follower

**Estimasi waktu: 20 menit**

Implementasikan algoritma binary menggunakan hanya **sensor 5, 6, 7, 8** (sensor tengah):

```cpp
// Baca sensor 5-8 (bit 4-7 dari kiri)
bool s5 = (data >> 7) & 1;
bool s6 = (data >> 6) & 1;
bool s7 = (data >> 5) & 1;
bool s8 = (data >> 4) & 1;

// Kontrol binary
if      ( s6 && !s7)         { motorLeft(100); motorRight(150); } // Belok kanan
else if (!s6 &&  s7)         { motorLeft(150); motorRight(100); } // Belok kiri
else if ( s6 &&  s7)         { motorLeft(140); motorRight(140); } // Lurus
else if (!s6 && !s7 &&  s5)  { motorLeft( 80); motorRight(150); } // Belok kanan jauh
else if (!s6 && !s7 && !s5 && s8) { motorLeft(150); motorRight(80); } // Belok kiri jauh
else                         { motorLeft(150); motorRight(-150); } // Putar cari garis
```

**Data Pengamatan P1:**

| Parameter | Nilai |
|-----------|-------|
| Kecepatan motor (PWM, 0-255) | |
| Kecepatan lintasan oval sederhana (waktu, detik) | |
| Jumlah keluar garis dalam 1 putaran | |
| Observasi perilaku (osilasi?) | |
| Catatan | |

---

#### LANGKAH 13: PERCOBAAN 2 – P Controller dengan Weighted Position

**Estimasi waktu: 20 menit**

Implementasikan P controller menggunakan semua 12 sensor:

1. Salin program dasar dari `Materi.md` bagian B.3.3
2. Set `Ki = 0`, `Kd = 0`
3. Eksperimen dengan berbagai nilai `Kp`:

**Tabel Tuning Kp:**

| Kp | Perilaku Robot | Waktu Lintasan (s) | Keluar Garis? | Evaluasi |
|----|---------------|-------------------|--------------|---------|
| 0.05 | | | | |
| 0.10 | | | | |
| 0.15 | | | | |
| 0.20 | | | | |
| 0.25 | | | | |
| 0.30 | | | | |
| Kp optimal: | | | | ✅ Terbaik |

---

#### LANGKAH 14: PERCOBAAN 3 – PD Controller

**Estimasi waktu: 20 menit**

Tambahkan komponen Kd ke program Percobaan 2:

1. Gunakan `Kp` optimal dari Percobaan 2
2. Tambahkan `Kd` bertahap:

**Tabel Tuning PD (Kp fixed dari P2):**

| Kd | Perilaku Robot | Waktu Lintasan (s) | Keluar Garis? | Evaluasi |
|----|---------------|-------------------|--------------|---------|
| 0.0 | (sama dengan P) | | | |
| 0.3 | | | | |
| 0.6 | | | | |
| 0.8 | | | | |
| 1.2 | | | | |
| 1.5 | | | | |
| Kd optimal: | | | | ✅ Terbaik |

---

#### LANGKAH 15: PERCOBAAN 4 – PID Controller Penuh (Opsional/Lanjutan)

**Estimasi waktu: 20 menit (jika waktu cukup)**

Tambahkan komponen Ki ke program Percobaan 3:

1. Gunakan Kp dan Kd optimal dari Percobaan 3
2. Mulai dengan Ki yang sangat kecil (0.001)
3. Tambahkan anti-windup: `integral = constrain(integral, -100, 100);`

**Tabel Tuning PID:**

| Ki | Steady-state error | Waktu Lintasan (s) | Windup? | Evaluasi |
|----|-------------------|--------------------|---------|---------|
| 0.000 | (baseline PD) | | | |
| 0.001 | | | | |
| 0.005 | | | | |
| 0.010 | | | | |
| Ki optimal: | | | | ✅ Terbaik |

---

## F. TABEL PENGAMATAN DAN DATA

### F.1 Spesifikasi Hardware Robot

| Parameter | Nilai Terukur |
|-----------|--------------|
| Dimensi chassis (P×L mm) | |
| Berat total robot (gram) | |
| Jarak sensor ke permukaan (mm) | |
| Wheelbase (jarak antara roda kiri-kanan, mm) | |
| Tegangan baterai saat penuh (V) | |
| Tegangan baterai saat dipakai (V) | |
| Arus total robot saat bergerak (mA) | |

### F.2 Kalibrasi Sensor

| Sensor # | Nilai Saat Putih | Nilai Saat Hitam | Threshold | Sensitivitas |
|---------|-----------------|-----------------|-----------|-------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | | | |
| 7 | | | | |
| 8 | | | | |
| 9 | | | | |
| 10 | | | | |
| 11 | | | | |
| 12 | | | | |

### F.3 Perbandingan Performa Algoritma

| Algoritma | Kp | Ki | Kd | Waktu Lintasan (s) | Keluar Garis | Evaluasi |
|----------|----|----|----|--------------------|-------------|---------|
| Binary | — | — | — | | | |
| P Controller | | 0 | 0 | | | |
| PD Controller | | 0 | | | | |
| PID Controller | | | | | | |

### F.4 Pengamatan Perilaku per Kondisi Track

| Kondisi Track | Algoritma Terbaik | Kecepatan Optimal | Catatan |
|--------------|------------------|------------------|---------|
| Garis lurus panjang | | | |
| Belokan 90° | | | |
| Belokan 45° | | | |
| S-curve | | | |
| Hairpin (180°) | | | |

---

## G. PERTANYAAN ANALISIS

1. **Bandingkan** perilaku robot pada algoritma binary vs P controller. Mengapa P controller menghasilkan gerakan yang lebih halus?

   **Jawaban:**
   _______________________________________________

2. **Jelaskan** peran komponen Kd dalam PD controller. Apa yang terjadi jika Kd terlalu besar?

   **Jawaban:**
   _______________________________________________

3. **Mengapa** pembacaan sensor melalui SPI (74HC165) dipilih daripada pembacaan langsung GPIO untuk 12 sensor? Berikan analisis dari sisi jumlah pin, kecepatan, dan konsumsi daya.

   **Jawaban:**
   _______________________________________________

4. **Hitung** frekuensi loop kontrol maksimum robot ini, jika waktu baca sensor = 16μs, waktu hitung PID = 5μs, waktu tulis motor = 2μs, dan waktu update OLED = 500μs (setiap 200ms). Apakah frekuensi ini cukup?

   **Jawaban:**
   _______________________________________________

5. **Analisis** pengaruh tegangan baterai terhadap kecepatan motor. Jika baterai 7.4V turun ke 6.5V, berapa persen kecepatan motor berkurang? Bagaimana solusinya?

   **Jawaban:**
   _______________________________________________

---

## H. KESIMPULAN

Tuliskan kesimpulan praktikum dalam 5–6 poin:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
4. _______________________________________________
5. _______________________________________________
6. _______________________________________________

---

## I. LAMPIRAN (Screenshot/Foto Wajib)

**Hardware:**
- [ ] Foto PCB Sensor Line setelah disolder (tampak atas)
- [ ] Foto PCB MAIN setelah disolder (tampak atas)
- [ ] Foto robot assembled (tampak depan, samping, atas)
- [ ] Foto robot di atas lintasan (sebelum menjalankan)

**Software:**
- [ ] Screenshot project PlatformIO (struktur folder + platformio.ini)
- [ ] Screenshot Serial Monitor saat test sensor (12 sensor terdeteksi)
- [ ] Screenshot atau rekaman Serial Monitor saat robot berlari dengan P controller
- [ ] Screenshot atau rekaman Serial Monitor saat robot berlari dengan PD controller

**Grafik:**
- [ ] Grafik Kp vs Waktu Lintasan (dari tabel tuning Percobaan 2)
- [ ] Grafik perbandingan error vs waktu untuk P vs PD (dari Serial data)
- [ ] Video robot berlari dengan PD controller (minimal 1 putaran oval)

---

## J. REFERENSI

1. Siegwart, R., Nourbakhsh, I.R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.
2. Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Prentice Hall.
3. PlatformIO Documentation. https://docs.platformio.org
4. Espressif ESP32 Technical Reference Manual. https://www.espressif.com/en/support/documents/technical-documents
5. Adafruit SSD1306 Library. https://github.com/adafruit/Adafruit_SSD1306
6. 74HC165 Datasheet. Texas Instruments. https://www.ti.com/product/SN74HC165
7. L293D Datasheet. STMicroelectronics. https://www.st.com/en/motor-drivers/l293d.html
8. LM2596 Datasheet. Texas Instruments. https://www.ti.com/product/LM2596
9. Dong, J., et al. (2023). "Line Following Robot Navigation Using Improved PID Control Algorithm." *IEEE Transactions on Industrial Electronics*, 70(4), 3821–3830.
10. Kurniawan, D., et al. (2022). "Performance Comparison of P, PD, PI, and PID Controllers for Mobile Robot Line Following." *TELKOMNIKA*, 20(1), 45–53.

---

*Jobsheet ini merupakan dokumen resmi praktikum. Isi dengan lengkap dan jujur.*  
*Nilai ditentukan berdasarkan kelengkapan jobsheet, kualitas hasil soldering, kualitas program, dan analisis.*

**Tanda Tangan Dosen/Asisten:** ___________________  
**Tanggal:** ___________________
