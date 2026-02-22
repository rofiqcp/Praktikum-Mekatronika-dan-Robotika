# JOBSHEET MODUL 07: WALL FOLLOWER ROBOT DENGAN ESP32 DAN PLATFORMIO

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 07 – Wall Follower  
**Platform:** ESP32 + PlatformIO  
**Prasyarat:** Modul 01 (Desain PCB), Modul 03 (Fusion360), Modul 06 (Line Follower)  
**Pertemuan:** 7–8 (2 × 2 SKS)  
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

1. Menjelaskan prinsip kerja sensor ultrasonik HC-SR04 dan cara pengukuran jarak berbasis Time of Flight
2. Mengimplementasikan algoritma Right-Hand Rule dan Left-Hand Rule untuk navigasi wall follower
3. Merancang dan mengimplementasikan kontroler PID untuk wall following yang smooth dan stabil
4. Memprogram robot hybrid yang dapat beralih antara mode wall follower dan line follower secara otomatis
5. Mengkonfigurasi ESP32 sebagai WiFi Access Point untuk setting parameter robot via smartphone
6. Menggunakan PlatformIO untuk mengembangkan, men-debug, dan mengupload firmware ESP32
7. Menganalisis dan membandingkan berbagai algoritma wall following berdasarkan data pengujian kuantitatif
8. Menerapkan konsep dual-core ESP32 untuk pemrosesan sensor dan kontrol motor secara paralel
9. Mengintegrasikan web server dan REST API ke dalam sistem robot embedded
10. Merancang sistem robot otonom yang robust terhadap gangguan lingkungan

---

## B. CAPAIAN PEMBELAJARAN MATA KULIAH (CPMK)

| Kode | Kompetensi | Indikator Penilaian |
|------|-----------|---------------------|
| CPMK-1 | Mampu membaca dan menganalisis output sensor HC-SR04 serta melakukan kalibrasi | Error pengukuran < 5% dibanding penggaris, data terdokumentasi |
| CPMK-2 | Mampu mengimplementasikan algoritma wall following (right/left hand rule) | Robot berhasil menavigasi maze kotak minimal 2 putaran |
| CPMK-3 | Mampu merancang PID controller dengan tuning parameter yang tepat | RMSE error jarak ≤ 3 cm pada kecepatan normal |
| CPMK-4 | Mampu mengintegrasikan wall follower dan line follower dalam satu sistem | Transisi mode berjalan otomatis dan mulus |
| CPMK-5 | Mampu mengkonfigurasi parameter robot via web interface ESP32 hotspot | Parameter tersimpan dan efektif tanpa restart |
| CPMK-6 | Mampu menganalisis data percobaan dan menyimpulkan secara ilmiah | Laporan dengan grafik, tabel, dan analisis yang koheren |

---

## C. ALAT DAN BAHAN

### C.1 Hardware

| No | Komponen | Spesifikasi | Jumlah | Keterangan |
|----|---------|------------|--------|-----------|
| 1 | **ESP32 DevKit V1** | 38-pin, dual core 240MHz | 1 | MCU utama |
| 2 | **Sensor HC-SR04** | 2-400cm, 5V, ±3mm | 3 | Kiri, depan, kanan |
| 3 | **Motor Driver L298N** | 2A per channel, 5-35V | 1 | Atau L293D |
| 4 | **Motor DC + Gearbox** | 3-6V, 1:48 gearbox | 2 | Roda kiri & kanan |
| 5 | **Sensor IR TCRT5000** | Reflective, digital out | 4 | Line detection |
| 6 | **Baterai Li-Po** | 7.4V 1000mAh (2S) | 1 | Power utama |
| 7 | **Modul Step-Down LM2596** | 7.4V → 5V, 3A | 1 | Supply L298N+Sensor |
| 8 | **Resistor 1kΩ + 2kΩ** | 1/4 Watt | 6 set | Voltage divider ECHO |
| 9 | **LED 5mm** | Merah, Hijau, Biru, Kuning | 4 | Indikator mode |
| 10 | **Resistor 220Ω** | 1/4 Watt | 4 | Seri LED |
| 11 | **Buzzer aktif** | 5V | 1 | Feedback audio |
| 12 | **Push button** | 6×6mm | 2 | Start / Stop |
| 13 | **Breadboard 830 pin** | Full size | 1 | Prototyping |
| 14 | **Kabel jumper** | Male-to-male, M-to-F | 1 set | Wiring |
| 15 | **PCB Chassis Robot** | Dari Modul 01 (jika ada) | 1 | Body robot |
| 16 | **Roda + Caster Ball** | Ø65mm | 2+1 | Roda + penyeimbang |

### C.2 Perangkat Lunak

| No | Software | Sumber | Fungsi |
|----|---------|--------|--------|
| 1 | **VS Code** | https://code.visualstudio.com | Code editor |
| 2 | **PlatformIO Extension** | VS Code Marketplace | Framework ESP32 |
| 3 | **Driver CP2102/CH340** | Sesuai USB chip ESP32 | Driver USB-Serial |
| 4 | **Browser** | Chrome/Firefox (mobile) | Akses web interface |
| 5 | **Serial Plotter** | Terintegrasi di PlatformIO | Visualisasi data real-time |

### C.3 Pin Assignment ESP32

| Nama Pin | GPIO ESP32 | Komponen | Keterangan |
|---------|-----------|---------|-----------|
| TRIG_L | GPIO 5 | HC-SR04 Kiri - TRIG | Output |
| ECHO_L | GPIO 18 | HC-SR04 Kiri - ECHO | Input (via voltage divider) |
| TRIG_F | GPIO 19 | HC-SR04 Depan - TRIG | Output |
| ECHO_F | GPIO 21 | HC-SR04 Depan - ECHO | Input (via voltage divider) |
| TRIG_R | GPIO 22 | HC-SR04 Kanan - TRIG | Output |
| ECHO_R | GPIO 23 | HC-SR04 Kanan - ECHO | Input (via voltage divider) |
| IR_LL | GPIO 34 | Sensor IR Line Kiri-Luar | Input (ADC1) |
| IR_LR | GPIO 35 | Sensor IR Line Kiri-Dalam | Input (ADC1) |
| IR_RL | GPIO 32 | Sensor IR Line Kanan-Dalam | Input (ADC1) |
| IR_RR | GPIO 33 | Sensor IR Line Kanan-Luar | Input (ADC1) |
| IN1 | GPIO 25 | L298N Motor A IN1 | Output |
| IN2 | GPIO 26 | L298N Motor A IN2 | Output |
| IN3 | GPIO 27 | L298N Motor B IN3 | Output |
| IN4 | GPIO 14 | L298N Motor B IN4 | Output |
| ENA | GPIO 12 | L298N Enable A (PWM) | Output PWM |
| ENB | GPIO 13 | L298N Enable B (PWM) | Output PWM |
| LED_R | GPIO 2 | LED Merah (mode stop) | Output |
| LED_G | GPIO 4 | LED Hijau (line mode) | Output |
| LED_B | GPIO 16 | LED Biru (wall kiri) | Output |
| LED_Y | GPIO 17 | LED Kuning (wall kanan) | Output |
| BUZZER | GPIO 15 | Buzzer aktif | Output |
| BTN_START | GPIO 0 | Tombol Start | Input Pull-up |
| BTN_STOP | GPIO 36 | Tombol Stop | Input |

> **⚠️ PERHATIAN:** Pin ECHO HC-SR04 mengeluarkan tegangan 5V. ESP32 maksimal 3.3V. WAJIB menggunakan voltage divider (1kΩ + 2kΩ) atau level shifter.

---

## D. LANGKAH KERJA

### D.1 PERCOBAAN 1: Kalibrasi Sensor HC-SR04

**Tujuan:** Memahami karakteristik sensor dan menentukan akurasi pengukuran jarak.

**Durasi:** 20 menit

**Prosedur:**

1. Pasang satu sensor HC-SR04 pada breadboard
2. Hubungkan ke ESP32 sesuai pin assignment (TRIG_F = GPIO 19, ECHO_F = GPIO 21)
3. Pasang voltage divider pada pin ECHO (1kΩ ke ECHO, sambungkan titik tengah ke GPIO 21, 2kΩ ke GND)
4. Upload program berikut menggunakan PlatformIO:

```cpp
// Percobaan 1: Kalibrasi HC-SR04
#include <Arduino.h>

#define TRIG_PIN 19
#define ECHO_PIN 21

float readDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    long dur = pulseIn(ECHO_PIN, HIGH, 30000);
    if (dur == 0) return -1.0;
    return dur / 58.0;
}

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    Serial.println("Percobaan 1: Kalibrasi HC-SR04");
    Serial.println("Jarak_Referensi(cm), Rata_Rata_10_Sampel(cm), Error(cm)");
}

void loop() {
    float sum = 0;
    int valid = 0;
    for (int i = 0; i < 10; i++) {
        float d = readDistance();
        if (d > 0) { sum += d; valid++; }
        delay(60);
    }
    float avg = (valid > 0) ? sum / valid : -1;
    Serial.print("Rata-rata 10 sampel: ");
    Serial.print(avg);
    Serial.println(" cm");
    delay(2000);
}
```

5. Posisikan objek datar (buku/kardus) pada jarak terukur dengan penggaris: **5, 10, 15, 20, 30, 50 cm**
6. Catat data pada tabel berikut:

**Tabel Data Percobaan 1:**

| No | Jarak Referensi (cm) | Rata-rata Sensor (cm) | Error Absolut (cm) | Error Relatif (%) |
|----|---------------------|----------------------|-------------------|------------------|
| 1 | 5 | | | |
| 2 | 10 | | | |
| 3 | 15 | | | |
| 4 | 20 | | | |
| 5 | 30 | | | |
| 6 | 50 | | | |

**Pertanyaan Analisis P1:**
- a. Pada jarak berapa sensor paling akurat?
- b. Apakah ada korelasi antara jarak dan error? Jelaskan!
- c. Mengapa perlu mengambil rata-rata 10 sampel?

---

### D.2 PERCOBAAN 2: Wall Detection Threshold

**Tujuan:** Menentukan threshold jarak yang tepat untuk deteksi dinding.

**Durasi:** 20 menit

**Prosedur:**

1. Gunakan setup sensor dari Percobaan 1
2. Upload program threshold detection:

```cpp
// Percobaan 2: Wall Detection Threshold
#include <Arduino.h>

#define TRIG_PIN 19
#define ECHO_PIN 21
#define THRESHOLD_CM 20.0   // ← ubah-ubah nilai ini

float readDistance() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    long dur = pulseIn(ECHO_PIN, HIGH, 30000);
    return (dur == 0) ? 999.0 : dur / 58.0;
}

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    Serial.println("Percobaan 2: Wall Detection");
}

void loop() {
    float dist = readDistance();
    bool wallDetected = (dist < THRESHOLD_CM);
    Serial.print("Jarak: ");
    Serial.print(dist);
    Serial.print(" cm | Dinding: ");
    Serial.println(wallDetected ? "ADA" : "TIDAK ADA");
    delay(200);
}
```

3. Gerakkan objek dari 50 cm mendekati sensor secara perlahan
4. Catat pada jarak berapa status berubah dari "TIDAK ADA" → "ADA"
5. Ulangi dengan threshold: 10, 15, 20, 25, 30 cm

**Tabel Data Percobaan 2:**

| Threshold (cm) | Jarak Deteksi Aktual (cm) | Kesesuaian? |
|---------------|--------------------------|-------------|
| 10 | | |
| 15 | | |
| 20 | | |
| 25 | | |
| 30 | | |

---

### D.3 PERCOBAAN 3: Wall Following Sederhana (Tanpa PID)

**Tujuan:** Implementasi Right-Hand Rule dengan logika if-else sederhana.

**Durasi:** 30 menit

**Prosedur:**

1. Rakit robot lengkap (3 sensor HC-SR04 + motor driver + ESP32)
2. Upload program wall following sederhana dari repositori: `program/percobaan3_simple_wall_follow/`
3. Siapkan arena maze kotak (4 dinding, minimal 50cm × 50cm)
4. Jalankan robot dan observasi:
   - Apakah robot berhasil menavigasi maze?
   - Bagaimana kualitas gerakan? (mulus/kasar)
   - Berapa kali robot menyentuh dinding?

**Tabel Observasi Percobaan 3:**

| Pengujian | Berhasil Selesai? | Waktu (detik) | Sentuh Dinding? | Catatan |
|-----------|-----------------|--------------|----------------|---------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

### D.4 PERCOBAAN 4: Wall Following dengan PID

**Tujuan:** Membandingkan PID dengan threshold biner dan menemukan parameter PID optimal.

**Durasi:** 40 menit

**Prosedur:**

1. Upload program PID wall follower dari: `program/percobaan4_pid_wall_follow/`
2. Jalankan dengan 3 set parameter berbeda:

**Set A (Kp tinggi, Ki=0, Kd=0):** Kp=8.0, Ki=0.0, Kd=0.0

| Waktu (ms) | Jarak Kiri (cm) | Error (cm) | Kec. Motor Kiri | Kec. Motor Kanan |
|-----------|----------------|-----------|----------------|-----------------|
| 0 | | | | |
| 500 | | | | |
| 1000 | | | | |
| 1500 | | | | |
| 2000 | | | | |

**Set B (Kp sedang, Ki+Kd):** Kp=3.0, Ki=0.05, Kd=1.0

| Waktu (ms) | Jarak Kiri (cm) | Error (cm) | Kec. Motor Kiri | Kec. Motor Kanan |
|-----------|----------------|-----------|----------------|-----------------|
| 0 | | | | |
| 500 | | | | |
| 1000 | | | | |
| 1500 | | | | |
| 2000 | | | | |

**Set C (Parameter terbaik mahasiswa):** Kp=___, Ki=___, Kd=___

(Mahasiswa menentukan sendiri)

**Pertanyaan Analisis P4:**
- a. Set parameter mana yang menghasilkan RMSE error terkecil?
- b. Jelaskan efek Kd dalam mengurangi overshoot!
- c. Apa yang terjadi jika Ki terlalu besar?

---

### D.5 PERCOBAAN 5: Left Wall Following vs Right Wall Following

**Tujuan:** Membandingkan perilaku robot pada maze yang sama dengan dua strategi berbeda.

**Durasi:** 30 menit

**Prosedur:**

1. Upload program yang mendukung kedua mode dari: `program/percobaan5_left_right_wall/`
2. Siapkan maze huruf "F" atau "T" (maze yang tidak simetris)
3. Jalankan robot dengan Right-Hand Rule → catat path dan waktu
4. Jalankan robot dengan Left-Hand Rule di maze yang sama → catat path dan waktu

**Sketsa Path Robot:**

```
MAZE:
┌────────────────────────┐
│                        │
│  ┌──────┐              │
│  │      │              │
│  │      └──────────┐   │
│  │                 │   │
│  └─────────────────┘   │
│                        │
└────────────────────────┘

Path Right-Hand Rule: (gambar dengan tangan)


Path Left-Hand Rule: (gambar dengan tangan)
```

---

### D.6 PERCOBAAN 6: Adaptive Setpoint (Tengah Koridor)

**Tujuan:** Robot secara otomatis memposisikan diri di tengah koridor.

**Prosedur:**

1. Upload program dari: `program/percobaan6_adaptive_setpoint/`
2. Uji di koridor dengan lebar: 20 cm, 30 cm, 40 cm, 50 cm
3. Ukur apakah robot berhasil berada di tengah (±2 cm dari titik tengah)

**Tabel Data Percobaan 6:**

| Lebar Koridor | Setpoint Dihitung | Posisi Aktual Robot | Error Posisi |
|--------------|-------------------|--------------------|-----------  |
| 20 cm | | | |
| 30 cm | | | |
| 40 cm | | | |
| 50 cm | | | |

---

### D.7 PERCOBAAN 7: Mode Switching Wall + Line Follower

**Tujuan:** Implementasi hybrid navigation dengan transisi mode otomatis.

**Prosedur:**

1. Siapkan arena: lantai dengan garis hitam yang berakhir di dekat dinding
2. Upload program hybrid dari: `program/percobaan7_hybrid_navigation/`
3. Tes skenario berikut:
   - Robot mulai di garis → ikuti garis → garis berakhir → beralih wall follow
   - Robot mulai di area tanpa garis → wall follow → temukan garis → beralih line follow

**Log Mode Switching:**

| Waktu (ms) | Mode Aktif | Sensor Trigger | Keterangan |
|-----------|-----------|---------------|-----------|
| | | | |
| | | | |
| | | | |

---

### D.8 PERCOBAAN 8: Hybrid Navigation Arena Lengkap

**Tujuan:** Uji sistem hybrid di arena yang mensimulasikan lingkungan nyata.

**Prosedur:**

1. Desain arena kombinasi: garis + dinding (area terbuka + koridor)
2. Jalankan robot selama 3 menit
3. Hitung: berapa kali mode switching terjadi? Apakah semua transisi berhasil?

---

### D.9 PERCOBAAN 9: Setting Parameter via WiFi

**Tujuan:** Mengkonfigurasi parameter PID secara real-time via web interface.

**Prosedur:**

1. Upload program dengan web server dari: `program/percobaan9_wifi_config/`
2. Nyalakan robot → ESP32 akan broadcast SSID "WallFollower-ESP32"
3. Hubungkan smartphone ke WiFi tersebut (password: robot1234)
4. Buka browser smartphone → ketik 192.168.4.1
5. Lakukan perubahan parameter berikut sambil robot berjalan:

**Tabel Eksperimen Perubahan Parameter:**

| Parameter | Nilai Awal | Nilai Baru | Perubahan Perilaku yang Diamati |
|----------|-----------|----------|-------------------------------|
| Kp | 3.0 | 6.0 | |
| Kp | 6.0 | 1.5 | |
| Setpoint | 15 cm | 8 cm | |
| Base Speed | 150 | 200 | |
| Mode | LEFT | RIGHT | |

6. Restart ESP32 → periksa apakah parameter tetap tersimpan

**Pertanyaan Analisis P9:**
- a. Apakah perubahan parameter efektif real-time atau butuh restart?
- b. Apa yang terjadi jika Kp diubah drastis saat robot sedang bergerak?

---

### D.10 PERCOBAAN 10: Uji Robustness di Lingkungan Dinamis

**Tujuan:** Menguji ketahanan sistem wall follower terhadap gangguan.

**Prosedur:**

1. Jalankan robot di koridor sederhana
2. Tambahkan gangguan satu per satu:
   - **Gangguan 1:** Letakkan kotak di tengah koridor (obstacle statis)
   - **Gangguan 2:** Gerakkan tangan di depan robot saat berjalan
   - **Gangguan 3:** Miringkan/geser sedikit dinding (5-10 cm)
   - **Gangguan 4:** Matikan salah satu sensor (cabut kabel)
3. Catat respons robot terhadap setiap gangguan

**Tabel Observasi Robustness:**

| Gangguan | Respons Robot | Berhasil Mengatasi? | Waktu Recovery (ms) |
|---------|--------------|--------------------|--------------------|
| Obstacle statis | | | |
| Tangan bergerak | | | |
| Dinding bergeser | | | |
| Sensor mati | | | |

---

## E. ANALISIS DAN DISKUSI

### E.1 Analisis Kualitas Sensor (Percobaan 1-2)

Hitung **Mean Absolute Error (MAE)** dan **RMSE** pengukuran sensor:

```
MAE  = (1/n) × Σ |x_measured - x_actual|
RMSE = √((1/n) × Σ (x_measured - x_actual)²)
```

| Metrik | Nilai |
|--------|-------|
| MAE (cm) | |
| RMSE (cm) | |
| Max Error (cm) | |
| Min Error (cm) | |

### E.2 Analisis Performa PID (Percobaan 4)

Untuk parameter PID terbaik yang ditemukan, hitung:

| Metrik | Nilai |
|--------|-------|
| Rise Time (ms) | |
| Overshoot (%) | |
| Settling Time (ms) | |
| Steady-State Error (cm) | |
| RMSE Error Jarak (cm) | |

**Parameter PID terbaik yang ditemukan:** Kp=___, Ki=___, Kd=___

### E.3 Perbandingan Algoritma

| Aspek | Simple Threshold | PID Controller | Fuzzy Logic (opsional) |
|-------|-----------------|---------------|----------------------|
| Kualitas gerakan | | | |
| RMSE error | | | |
| Kecepatan adaptasi | | | |
| Kompleksitas kode | | | |
| Konsumsi memori | | | |

### E.4 Analisis Mode Switching

Gambarkan diagram transisi mode yang terekam pada Percobaan 7-8:

```
Timeline mode:
0ms ──[LINE]── 2340ms ──[WALL_L]── 5100ms ──[LINE]── ...
```

(Isi dengan data aktual dari log percobaan)

---

## F. KESIMPULAN

Isi tabel kesimpulan berdasarkan hasil percobaan:

| No | Pernyataan | Terbukti / Tidak Terbukti | Bukti Data |
|----|-----------|--------------------------|-----------|
| 1 | PID menghasilkan gerakan lebih smooth dibanding threshold biner | | |
| 2 | Parameter Kd mengurangi overshoot secara signifikan | | |
| 3 | Mode switching otomatis berhasil dalam semua skenario uji | | |
| 4 | Parameter dapat diubah real-time via WiFi tanpa restart | | |
| 5 | Robot berhasil mengatasi semua gangguan pada Percobaan 10 | | |

**Kesimpulan Narasi:**

(Tulis minimal 3 paragraf yang menjelaskan: apa yang dipelajari, apa yang berhasil dan tidak berhasil, dan rekomendasi perbaikan)

---

## G. REFERENSI WAJIB

1. Siegwart, R., Nourbakhsh, I. R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.
2. Borenstein, J., & Koren, Y. (1991). The vector field histogram: Fast obstacle avoidance for mobile robots. *IEEE Transactions on Robotics and Automation, 7*(3), 278–288.
3. Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Pearson Education.
4. Espressif Systems. (2024). *ESP32 Technical Reference Manual*. https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf
5. PlatformIO. (2024). *PlatformIO Documentation*. https://docs.platformio.org/en/latest/
6. ESPAsyncWebServer. (2024). *ESPAsyncWebServer Library Documentation*. https://github.com/me-no-dev/ESPAsyncWebServer

---

## H. LAMPIRAN

### H.1 Checklist Komponen (diisi sebelum praktikum dimulai)

- [ ] ESP32 DevKit V1 terpasang dengan baik di breadboard
- [ ] 3× HC-SR04 terhubung dengan voltage divider yang benar
- [ ] L298N terhubung ke motor dan ESP32
- [ ] 2× Motor DC terhubung ke L298N output
- [ ] Power supply 7.4V baterai terpasang
- [ ] 4× Sensor IR terpasang di bawah chassis
- [ ] PlatformIO terinstall dan proyek berhasil di-build
- [ ] Driver USB-Serial terinstall (CP2102/CH340)
- [ ] Arena maze/koridor sudah disiapkan
- [ ] Penggaris tersedia untuk kalibrasi

### H.2 Kode Error PlatformIO Umum

| Error | Kemungkinan Penyebab | Solusi |
|-------|---------------------|--------|
| `Fatal error: Arduino.h not found` | Platform belum terinstall | `pio pkg install` |
| `Error: Could not open port` | Driver USB tidak terinstall | Install driver CP2102/CH340 |
| `Error: Timed out waiting for packet` | Baud rate tidak cocok | Periksa monitor_speed di platformio.ini |
| `Sketch too large` | Program terlalu besar | Gunakan partition scheme yang lebih besar |

### H.3 Format Laporan Praktikum

Format file: **PDF**  
Nama file: `Laporan_M07_Kelompok[X]_[NamaKetua].pdf`  
Isi laporan:
1. Cover (nama, NIM, kelompok, tanggal)
2. Tujuan Praktikum
3. Dasar Teori (singkat, 1-2 halaman)
4. Data Percobaan (semua tabel terisi)
5. Analisis dan Pembahasan
6. Kesimpulan
7. Referensi
8. Lampiran: kode program yang dimodifikasi

**Deadline:** _________________ (1 minggu setelah praktikum)
