# PROMPT NOTEBOOKLLM – MODUL 06: BUILD LINE FOLLOWER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 06 – Build Line Follower  
**Jumlah Slide:** 45 Slide  

> Gunakan prompt berikut di NotebookLLM untuk menghasilkan narasi, penjelasan, atau isi slide presentasi. Setiap prompt dirancang agar menghasilkan konten yang kaya, akurat secara teknis, dan cocok untuk presentasi mahasiswa Teknologi Rekayasa Otomasi.

---

## BAGIAN 1: PENGANTAR LINE FOLLOWER (Slide 1–5)

### Slide 1 – Judul dan Gambaran Umum

**Prompt:**
```
Buatkan narasi pembuka yang menarik untuk slide presentasi berjudul "Build Line Follower: Dari PCB ke Robot Otonom" untuk mahasiswa Teknologi Rekayasa Otomasi semester 4. Narasi harus:
- Menjelaskan mengapa robot line follower adalah fondasi penting dalam robotika modern
- Menyebutkan contoh penerapan nyata di industri (AGV, manufaktur, logistik gudang)
- Menggambarkan apa yang akan dicapai mahasiswa di modul ini (menyolder PCB, assembly mekanik, program ESP32 dengan PlatformIO, 10 variasi percobaan)
- Gunakan bahasa yang antusias dan memotivasi, cocok untuk audiens mahasiswa teknik
- Panjang narasi: 120–150 kata
```

---

### Slide 2 – Sejarah dan Evolusi Line Follower

**Prompt:**
```
Jelaskan sejarah singkat dan evolusi robot line follower dari generasi pertama hingga modern untuk slide presentasi akademik. Sertakan:
- Tahun 1960-an: robot line follower pertama (Stanford Research Institute)
- Era mikrokontroler 8-bit (Arduino awal)
- Era sensor digital dan kontroler PID
- Era modern: ESP32, machine learning, computer vision
- Tren terkini: AGV warehouse (Amazon Robotics), medical delivery robots
- Format: timeline atau poin-poin singkat
- Panjang: 100–120 kata, cocok untuk slide dengan visual timeline
```

---

### Slide 3 – Prinsip Kerja Dasar

**Prompt:**
```
Jelaskan prinsip kerja robot line follower secara bertahap dan mudah dipahami untuk mahasiswa teknik. Gunakan analogi yang tepat:
- Analogi: seperti mata yang melihat garis dan otak yang memerintah kaki
- Jelaskan 4 tahap: Persepsi (sensor IR) → Kognisi (mikrokontroler) → Keputusan (algoritma kontrol) → Aksi (motor)
- Sertakan diagram blok sederhana dalam bentuk teks (ASCII art atau deskripsi)
- Jelaskan perbedaan deteksi garis hitam vs putih
- Mengapa frekuensi loop tinggi penting (>100Hz)
- Panjang: 130–150 kata
```

---

### Slide 4 – Aplikasi Line Follower di Industri

**Prompt:**
```
Buatkan konten slide tentang aplikasi nyata line follower di industri untuk mahasiswa Teknologi Rekayasa Otomasi. Bahas:
1. AGV (Automated Guided Vehicle) di pabrik otomotif Toyota dan BMW
2. Robot gudang Amazon Robotics (Kiva system)
3. Robot pengiriman obat di rumah sakit (Moxi robot)
4. Conveyor follower di lini produksi
5. Robot kompetisi (kontes robot Indonesia, ABU Robocon)
6. Untuk setiap aplikasi: sebutkan spesifikasi umum, tipe sensor, dan kontroller yang digunakan
7. Panjang: 150–180 kata
```

---

### Slide 5 – Overview Modul 06 dan Kompetensi

**Prompt:**
```
Buatkan slide overview Modul 06 "Build Line Follower" yang menunjukkan peta kompetensi dan alur pembelajaran. Sertakan:
- 3 fase utama: (1) Soldering & Assembly, (2) Pemrograman PlatformIO, (3) Eksperimen & Optimasi
- Daftar 10 percobaan yang akan dilakukan (P1: Binary ON/OFF → P10: Maze solver)
- Kompetensi akhir: mahasiswa mampu membangun dan memprogram robot line follower berbasis ESP32 yang mampu menyelesaikan lintasan kompleks
- Hubungan dengan Modul 01 (PCB yang sudah dibuat) dan Modul berikutnya (Wall Follower)
- Format: bullet points terstruktur
- Panjang: 130–150 kata
```

---

## BAGIAN 2: SENSOR INFRARED DAN ELEKTRONIKA (Slide 6–10)

### Slide 6 – Sensor Infrared: Prinsip Fisika

**Prompt:**
```
Jelaskan prinsip fisika deteksi infrared pada sensor garis untuk presentasi mahasiswa teknik otomasi. Sertakan:
- Spektrum elektromagnetik: posisi infrared 700nm–1mm, sensor robot menggunakan 940nm
- Hukum Lambert-Beer: bagaimana permukaan gelap menyerap vs permukaan terang memantulkan
- Diagram sederhana pasangan LED IR emitter dan photodiode receiver
- Pengaruh sudut pantulan dan jarak sensor ke permukaan (grafik ideal: 8-10mm optimal)
- Mengapa 940nm dipilih: minimasi gangguan cahaya ambient (lampu fluorescent di 400-700nm)
- Panjang: 140–160 kata, sertakan 2-3 poin kunci untuk highlight di slide
```

---

### Slide 7 – Rangkaian Sensor Garis dan Komparator

**Prompt:**
```
Jelaskan rangkaian elektronika sensor garis pada PCB Line Follower dari Modul 1. Sertakan penjelasan detail:
- Skema rangkaian: LED IR (dengan resistor seri 68Ω) + Photodioda (dengan resistor pull-down 10kΩ)
- Rumus perhitungan: tegangan pada node photodioda = VCC × R_pull / (R_photo + R_pull)
- Contoh kalkulasi: jika R_photo = 1kΩ saat terang → V = 5V × 10kΩ/(1kΩ+10kΩ) = 4.5V
- Fungsi trimpot (potensiometer adjustable) untuk kalibrasi threshold
- Perbedaan komparator LM393 vs pembacaan langsung ADC ESP32
- Kapan menggunakan output digital (komparator) vs analog (ADC)
- Panjang: 150–170 kata
```

---

### Slide 8 – Shift Register 74HC165 dan Multiplexing

**Prompt:**
```
Jelaskan cara kerja IC 74HC165 sebagai shift register untuk multiplexing 12 sensor ke 3 pin SPI ESP32. Sertakan:
- Fungsi: mengkonversi 8 input paralel → output serial, menghemat pin GPIO
- Timing diagram: CS (LOAD/PL) LOW → data latch → CS HIGH → shift out via CLK
- Konfigurasi daisy-chain: 2× 74HC165 untuk 16 input (digunakan 12)
- Rumus waktu baca: t = 16 × T_clk = 16 / f_SPI (pada 1MHz = 16μs)
- Perbandingan dengan MCP3208 (ADC 8-channel) dan CD4051 (multiplexer analog)
- Contoh kode Arduino (SPI.transfer) dalam pseudo-code
- Panjang: 160–180 kata
```

---

### Slide 9 – Kalibrasi Sensor

**Prompt:**
```
Jelaskan prosedur kalibrasi sensor garis untuk robot line follower, penting untuk akurasi deteksi. Sertakan:
- Mengapa kalibrasi diperlukan: variasi manufaktur LED/photodiode, perbedaan pencahayaan ambient
- Prosedur kalibrasi otomatis: robot berputar 360° di atas track → catat min/max setiap sensor
- Rumus normalisasi: nilai_ternormalisasi = (nilai - nilai_min) / (nilai_max - nilai_min)
- Threshold adaptif: threshold = (nilai_min + nilai_max) / 2
- Penyimpanan kalibrasi di EEPROM ESP32 (non-volatile)
- Tips praktis: kalibrasi dilakukan di kondisi pencahayaan yang sama dengan kondisi racing
- Panjang: 150–170 kata
```

---

### Slide 10 – Karakteristik Motor DC dan L293D

**Prompt:**
```
Jelaskan karakteristik motor DC yang digunakan pada robot line follower dan cara mengontrolnya dengan L293D. Sertakan:
- Kurva torsi-kecepatan motor DC: torsi maksimum saat stall, kecepatan idle maksimum tanpa beban
- Mengapa H-Bridge diperlukan: kontrol arah dan speed dari logika 3.3V ke motor 6V
- Internal diagram L293D: 4 transistor darlington per channel, dioda flyback
- Voltage drop L293D: ~2V per channel (penting untuk kalkulasi kecepatan aktual)
- Rumus kecepatan efektif: V_motor = V_supply - 2V_drop = 7.4V - 2×2V = 3.4V max
- Cara mengontrol kecepatan dengan PWM: duty cycle 0-100% → kecepatan 0-100%
- Panjang: 160–180 kata
```

---

## BAGIAN 3: TEKNIK SOLDERING (Slide 11–14)

### Slide 11 – Peralatan Solder dan Fungsinya

**Prompt:**
```
Buatkan deskripsi lengkap dan praktis tentang peralatan solder untuk PCB robot line follower, cocok untuk mahasiswa yang baru pertama kali menyolder. Sertakan:
- Solder iron 60W temperature-controlled: mengapa temperature control penting vs solder biasa
- Jenis solder wire: Sn63/Pb37 (leaded) vs SAC305 (lead-free) - kelebihan dan kekurangan
- Flux pasta dan flux liquid: fungsi kimia flux dalam membersihkan oksidasi
- Solder wick dan solder sucker: kapan masing-masing digunakan
- Alat bantu: helping hands, PCB vise, kaca pembesar
- Alat keselamatan: ventilasi, kacamata, sarung tangan
- Budget estimasi peralatan untuk mahasiswa Indonesia
- Panjang: 160–180 kata
```

---

### Slide 12 – Teknik Dasar Menyolder

**Prompt:**
```
Jelaskan teknik menyolder yang benar secara step-by-step untuk komponen through-hole pada PCB line follower. Fokus pada:
- Persiapan: bersihkan tip iron, tin the tip (lapisi timah tipis)
- Langkah 5-detik: (1) panaskan pad+kaki 2-3 detik, (2) sentuh solder wire ke joint (bukan ke iron tip), (3) tarik solder, (4) tarik iron, (5) jangan sentuh 3-5 detik
- Mengapa solder disentuhkan ke joint bukan ke iron tip: mencegah burn-off flux terlalu cepat
- Ciri hasil solder BAIK: mengkilap, bentuk kerucut konkav, kaki komponen terlihat
- Ciri hasil solder BURUK: cold joint (keruh), solder bridge, insufficient solder
- Foto/deskripsi visual yang jelas untuk slide
- Panjang: 150–170 kata
```

---

### Slide 13 – Urutan Solder PCB Sensor Line

**Prompt:**
```
Buatkan panduan urutan menyolder PCB Sensor Line (130×30mm) robot line follower secara detail dan sistematis. Sertakan:
- Prinsip dasar urutan: komponen terendah dahulu → tertinggi terakhir
- Langkah 1: Resistor SMD 0805 (jika ada) - teknik tack soldering
- Langkah 2: Resistor through-hole 68Ω (current limiter LED IR) dan 10kΩ (pull-down)
- Langkah 3: LED Infrared 940nm dan Photodiode - PERHATIAN polaritas dan orientasi menghadap bawah
- Langkah 4: IC 74HC165 (2 buah) - teknik solder IC multi-pin dengan solder wick
- Langkah 5: Konektor IDC 10-pin
- Troubleshooting umum: solder bridge pada IC, LED terbalik, photodiode tidak responsif
- Panjang: 160–180 kata
```

---

### Slide 14 – Quality Control dan Testing Setelah Solder

**Prompt:**
```
Jelaskan prosedur quality control dan testing setelah menyolder PCB line follower, cocok untuk mahasiswa teknik otomasi. Sertakan:
- Visual inspection: menggunakan kaca pembesar, cek setiap joint (15 ciri yang dicek)
- Electrical test dengan multimeter: continuity test, resistance measurement, short circuit check
- Cara cek tidak ada solder bridge IC 74HC165: diode mode multimeter antar pin
- Functional test awal: beri tegangan → cek arus tidak berlebihan → cek LED IR menyala (tampak dengan kamera HP)
- Test dengan ESP32: baca nilai SPI, verifikasi semua 12 sensor merespons perubahan (tangan menutup sensor)
- Panjang: 150–170 kata
```

---

## BAGIAN 4: ASSEMBLY MEKANIK (Slide 15–17)

### Slide 15 – Desain Chassis dan Layout Komponen

**Prompt:**
```
Jelaskan desain chassis robot line follower yang optimal untuk performa tinggi, untuk mahasiswa Teknologi Rekayasa Otomasi. Sertakan:
- Bahan chassis: akrilik 3mm, PCB, aluminium, atau 3D print - perbandingan kelebihan/kekurangan
- Dimensi optimal: 150×120mm chassis, wheelbase 90mm, track width 100mm
- Layout komponen: sensor di depan bawah, baterai di tengah-belakang (optimasi center of gravity)
- Jarak sensor ke permukaan: mengapa 8-10mm optimal (coverage width vs resolution tradeoff)
- Konfigurasi 2-wheel drive + ball caster vs 4-wheel drive: keunggulan masing-masing
- Tips: gunakan model 3D di Fusion360 (dari Modul 3) untuk simulasi sebelum fabrikasi
- Panjang: 160–180 kata
```

---

### Slide 16 – Langkah Assembly Mekanik

**Prompt:**
```
Buatkan panduan assembly mekanik robot line follower secara sistematis dan detail, dengan tips praktis dari pengalaman kompetisi. Sertakan:
- Step 1: Install motor ke bracket - torsi baut yang tepat, alignment roda
- Step 2: Pasang bracket ke chassis - cek kesejajaran kedua roda dengan penggaris
- Step 3: Install ball caster - kalkulasi tinggi agar roda utama menapak dengan benar
- Step 4: Mount PCB MAIN dengan standoff M3 nylon (isolasi listrik)
- Step 5: Bracket PCB Sensor Line di depan chassis - sudut dan jarak ke permukaan
- Step 6: Routing kabel yang rapih - gunakan cable tie, hindari kabel menyentuh roda
- Step 7: Pasang baterai - velcro strap untuk mudah dilepas
- Tips balance: geser baterai ke depan/belakang untuk optimasi traksi
- Panjang: 160–180 kata
```

---

### Slide 17 – Testing Mekanik dan Kalibrasi Fisik

**Prompt:**
```
Jelaskan prosedur testing mekanik robot line follower sebelum diprogram, untuk memastikan hardware berfungsi dengan baik. Sertakan:
- Test motor: beri tegangan langsung ke motor kiri dan kanan, cek putaran dan torsi
- Test roda: cek bebas berputar, tidak ada hambatan dari kabel atau baut
- Test sensor board: cek jarak ke lantai dengan penggaris (target 8-10mm), cek kemiringan
- Test center of gravity: letakkan robot di ujung meja - apakah jatuh ke depan atau belakang?
- Test running tanpa program: dorong robot, apakah lurus atau belok? (indikasi motor tidak balance)
- Pengukuran konsumsi arus: motor tanpa beban, motor stall - penting untuk cek baterai cukup
- Adjustment: cara fine-tune posisi sensor board
- Panjang: 150–170 kata
```

---

---

## BAGIAN 5b: SENSOR IMU MPU-6050 (Slide 18b–18e)

### Slide 18b – Pengenalan MPU-6050 dan Prinsip Kerja

**Prompt:**
```
Jelaskan sensor IMU MPU-6050 yang terpasang pada robot line follower ESP32, untuk mahasiswa Teknologi Rekayasa Otomasi yang baru mengenal sensor inersial. Sertakan:
- Definisi IMU: apa itu, mengapa disebut 6-DoF (3 accelerometer + 3 gyroscope)
- Prinsip MEMS: mengapa chip sekecil 4×4mm bisa mengukur percepatan dan rotasi
- Tabel spesifikasi: range gyro (±250 s.d. ±2000 °/s), range accel (±2 s.d. ±16g), ADC 16-bit, I2C 400kHz
- Register penting: WHO_AM_I (0x75), GYRO_CONFIG, ACCEL_CONFIG, register data 0x3B-0x48
- Koneksi ke ESP32: I2C bus bersama dengan OLED (GPIO21 SDA, GPIO22 SCL), AD0=GND → alamat 0x68
- Mengapa MPU-6050 ditambahkan ke line follower: koreksi yaw, deteksi ramp, stabilitas gerak
- Panjang: 160–180 kata
```

---

### Slide 18c – Accelerometer: Kalkulasi Sudut Pitch dan Roll

**Prompt:**
```
Jelaskan cara menghitung sudut pitch dan roll dari data raw accelerometer MPU-6050, dengan derivasi matematis yang jelas untuk mahasiswa teknik. Sertakan:
- Konsep: gravitasi bumi (1g = 9.81 m/s²) terproyeksi ke 3 sumbu saat sensor miring
- Rumus pitch: pitch = atan2(ay, sqrt(ax² + az²)) × (180/π)
- Rumus roll: roll = atan2(-ax, az) × (180/π)
- Contoh kalkulasi: robot miring 30° ke depan → ax=0.5g, ay=0, az=0.866g → pitch = 30°
- Keterbatasan: noisy saat robot bergerak (acceleration motion distorts gravity vector)
- Skala konversi raw ke g: ±2g range → 1g = 16384 LSB
- Aplikasi pada line follower: deteksi ramp (pitch > 10°), anti-terbalik (roll > 45° → stop)
- Panjang: 150–170 kata
```

---

### Slide 18d – Gyroscope dan Complementary Filter

**Prompt:**
```
Jelaskan cara kerja gyroscope MPU-6050 dan implementasi Complementary Filter untuk estimasi sudut yang akurat pada robot line follower. Sertakan:
- Gyroscope output: angular rate (°/s), bukan sudut absolut → perlu integrasi
- Masalah drift: integrasi error kecil terakumulasi seiring waktu (contoh: 0.1°/s drift = 6°/menit)
- Accelerometer: akurat jangka panjang tapi noisy saat gerak
- Complementary Filter: solusi gabungan high-pass gyro + low-pass accelerometer
- Rumus: angle = α × (angle + gyro_rate × dt) + (1-α) × accel_angle, dengan α = 0.98
- Time constant filter: τ = α×dt/(1-α) = 0.98×0.01/(0.02) = 0.49 detik
- Perbandingan dengan Kalman Filter: keunggulan complementary (lebih cepat, lebih sederhana) untuk aplikasi real-time
- Implementasi pada ESP32: dt menggunakan micros() untuk presisi
- Panjang: 160–180 kata
```

---

### Slide 18e – Integrasi MPU-6050 ke Kontrol Line Follower

**Prompt:**
```
Jelaskan cara mengintegrasikan data MPU-6050 ke dalam algoritma kontrol PID line follower untuk meningkatkan performa, dengan contoh konkret. Sertakan:
- Aplikasi 1 – Yaw correction: saat garis lurus (error kecil), gunakan gyro Z untuk mengoreksi rotasi tak terduga (slip ban, motor tidak balance) → tambahkan Kyaw × yaw_rate ke output motor
- Aplikasi 2 – Ramp compensation: pitch angle dari accelerometer → kalikan kecepatan base dengan cos(pitch) untuk mempertahankan kecepatan ground yang konstan
- Aplikasi 3 – Anti-overturn: jika roll > 45° atau pitch > 60° → stop motor (keselamatan)
- Aplikasi 4 – Smart speed reduction: deteksi getaran tinggi (standar deviasi akselerasi) → permukaan kasar → turunkan kecepatan
- Urutan pemrosesan dalam main loop: baca sensor garis → baca IMU → hitung PID garis → tambahkan koreksi IMU → aktuasi motor
- Panjang: 160–180 kata
```

---

## BAGIAN 5: PLATFORMIO DAN SETUP PROGRAM (Slide 19–22)

### Slide 18 – Pengenalan PlatformIO

**Prompt:**
```
Jelaskan PlatformIO IDE sebagai platform pengembangan embedded system untuk ESP32, dibandingkan dengan Arduino IDE untuk mahasiswa yang sudah mengenal Arduino. Sertakan:
- Apa itu PlatformIO: ekosistem pengembangan profesional (bukan hanya IDE)
- Keunggulan dibanding Arduino IDE: manajemen library otomatis, multi-platform, Git integration, unit testing, serial monitor canggih
- Integrasi dengan VS Code: mengapa VS Code + PlatformIO adalah standar industri
- platformio.ini: penjelasan setiap parameter (platform, board, framework, lib_deps, monitor_speed)
- IntelliSense dan autocomplete untuk ESP32/Arduino API
- Board manager: cara PlatformIO otomatis download toolchain yang benar
- Panjang: 160–180 kata
```

---

### Slide 19 – Struktur Project dan Konfigurasi ESP32

**Prompt:**
```
Jelaskan struktur project PlatformIO untuk robot line follower ESP32 dan konfigurasi pin ESP32 yang digunakan. Sertakan:
- Struktur folder: src/, include/, lib/, test/, platformio.ini
- Peran setiap folder dan file
- File config.h: praktik baik define semua pin dan konstanta di satu tempat (single source of truth)
- Pin mapping ESP32 untuk line follower: SPI (CLK18, MISO19, CS5), motor L (25,26,27), motor R (32,33,14), OLED I2C (21,22)
- Mengapa beberapa pin ESP32 tidak bisa digunakan sebagai output: GPIO6-11 (Flash), GPIO34-39 (input only)
- ESP32 LEDC hardware PWM: keunggulan dibanding analogWrite Arduino (resolusi, frekuensi, jumlah channel)
- Panjang: 160–180 kata
```

---

### Slide 21 – Library ESP32 untuk Line Follower

**Prompt:**
```
Jelaskan library-library yang digunakan dalam project line follower ESP32 dengan PlatformIO. Sertakan:
- SPI.h: komunikasi dengan 74HC165 - SPISettings, beginTransaction, endTransaction, transfer
- Wire.h / I2C: komunikasi dengan OLED SSD1306 dan MPU-6050 di bus yang sama
- Adafruit SSD1306 dan GFX: cara install via platformio.ini lib_deps, fungsi utama (begin, clearDisplay, print, display)
- ElectronicCats/MPU6050: cara install, MPU6050.initialize(), getMotion6() untuk baca 6-axis sekaligus
- Perbedaan ElectronicCats/MPU6050 vs Wire manual: library mengabstraksi register-level I2C
- ESP32 built-in: ledcSetup, ledcAttachPin, ledcWrite untuk hardware PWM motor
- Perbedaan delay() vs millis() untuk multitasking: mengapa millis() lebih baik untuk real-time control
- FreeRTOS ESP32: xTaskCreatePinnedToCore untuk pin IMU task ke Core 0 dan control task ke Core 1
- Panjang: 160–180 kata
```

---

### Slide 21 – Debugging dan Serial Monitor

**Prompt:**
```
Jelaskan teknik debugging robot line follower ESP32 menggunakan Serial Monitor PlatformIO dan tools lainnya. Sertakan:
- Serial.printf() vs Serial.println(): efisiensi dan format output
- Format debug yang baik: timestamp, nilai sensor, error, output PID, kecepatan motor dalam satu baris
- Parsing data serial dengan Python/Excel untuk analisis grafik PID tuning
- PlatformIO Serial Plotter: cara mem-visualisasikan nilai PID secara real-time
- Teknik LED indicator untuk debugging saat kabel serial tidak terhubung
- Penggunaan OLED sebagai mini dashboard: nilai kritis tanpa Serial
- Over-the-Air (OTA) update ESP32: mengapa berguna saat robot sedang berlari di track
- Panjang: 150–170 kata
```

---

## BAGIAN 6: ALGORITMA KONTROL (Slide 22–28)

### Slide 22 – Algoritma Binary (On-Off)

**Prompt:**
```
Jelaskan algoritma kontrol binary (on-off) untuk line follower sebagai fondasi sebelum PID, untuk mahasiswa teknik otomasi. Sertakan:
- Konsep: setiap sensor hanya 0 atau 1 (di atas garis atau tidak)
- Tabel keputusan untuk 2 sensor, 5 sensor, dan 8 sensor
- Implementasi dengan if-else bertingkat vs switch-case
- Kelemahan: gerakan tersentak (oscillation), kecepatan terbatas
- Mengapa binary masih berguna: implementasi sederhana, latency rendah, cocok untuk track lurus
- Contoh kode pseudo-code untuk 5 sensor: if (sensor_kiri && !sensor_kanan) → belok kiri
- Simulasi perilaku: diagram gerakan robot pada belokan
- Panjang: 150–170 kata
```

---

### Slide 23 – Weighted Position Calculation

**Prompt:**
```
Jelaskan metode weighted position calculation untuk menentukan posisi garis secara kontinu dari array 12 sensor, konsep kunci sebelum belajar PID. Sertakan:
- Konsep: transformasi dari 12 data biner menjadi 1 nilai posisi kontinu
- Pemberian bobot: sensor paling kiri = -55, paling kanan = +55, spacing 10
- Rumus weighted average: posisi = Σ(sensor_i × bobot_i) / Σ(sensor_i)
- Contoh kalkulasi manual: sensor 5, 6, 7 aktif → posisi = (−5+5+15)/3 = 5
- Penanganan kasus khusus: semua sensor OFF (garis hilang) → last-known position
- Penanganan garis putus-putus: hysteresis dalam pemilihan posisi
- Normalisasi ke skala -1 hingga +1 untuk portabilitas
- Panjang: 160–180 kata
```

---

### Slide 24 – Kontrol Proportional (P)

**Prompt:**
```
Jelaskan kontrol proportional (P controller) untuk line follower secara intuitif dan matematis, dengan analogi yang mudah dipahami. Sertakan:
- Analogi: seperti mengemudi mobil - semakin jauh posisi salah, semakin keras belok
- Rumus: output = Kp × error, di mana error = setpoint - posisi
- Pengaruh nilai Kp: terlalu kecil (robot lambat merespons), terlalu besar (osilasi berlebihan)
- Steady-state error: mengapa P controller saja tidak bisa mencapai setpoint sempurna
- Grafik respons sistem: underdamped, critically damped, overdamped
- Cara tuning Kp secara manual: mulai dari 0.05, naikkan bertahap hingga robot mengikuti garis
- Demo visual: grafik error vs output untuk Kp berbeda
- Panjang: 160–180 kata
```

---

### Slide 25 – Kontrol PD dan Pengenalan Derivative

**Prompt:**
```
Jelaskan komponen derivative (D) dalam kontrol PD untuk meredam osilasi robot line follower. Sertakan:
- Analogi: seperti shock absorber - memprediksi dan meredam gerakan berlebihan
- Rumus: D = Kd × (error_sekarang - error_sebelumnya) / dt
- Mengapa D mengurangi osilasi: bereaksi terhadap laju perubahan error, bukan besar error
- Efek noise pada derivatif: mengapa sensor harus stabil, atau butuh low-pass filter
- Nilai Kd yang tepat: dimulai dari Kd = 3×Kp, disesuaikan secara eksperimental
- Implementasi dengan millis() untuk dt yang akurat: dt = (millis() - last_time) / 1000.0
- Perbandingan respons P vs PD pada track belokan tajam
- Panjang: 150–170 kata
```

---

### Slide 26 – Kontrol PID Lengkap

**Prompt:**
```
Jelaskan kontrol PID penuh untuk robot line follower secara komprehensif, termasuk tuning dan anti-windup. Sertakan:
- Rumus lengkap: output = Kp×e + Ki×∫e dt + Kd×de/dt
- Komponen integral (I): mengatasi steady-state error, seperti "akumulasi pengalaman"
- Masalah integrator windup: ketika robot keluar jalur, integral menumpuk besar → solusi: anti-windup dengan clamp
- Metode tuning Ziegler-Nichols: Ku (ultimate gain), Tu (ultimate period) → formula Kp, Ki, Kd
- Nilai PID awal yang disarankan untuk line follower 12 sensor: Kp=0.15, Ki=0.0, Kd=0.8
- PID sampling rate: pentingnya loop time yang konsisten (10ms = 100Hz) untuk I dan D akurat
- Tabel hasil tuning untuk berbagai kondisi track
- Panjang: 170–200 kata
```

---

### Slide 27 – Fuzzy Logic untuk Line Follower

**Prompt:**
```
Jelaskan implementasi Fuzzy Logic Controller sebagai alternatif PID untuk robot line follower, dengan penekanan pada keunggulan dan cara implementasi. Sertakan:
- Konsep fuzzy: bekerja dengan derajat keanggotaan (0 hingga 1), bukan biner
- 7 himpunan fuzzy untuk error: NL, NM, NS, ZE, PS, PM, PL
- Rule base 49 aturan (7×7) untuk error dan delta-error
- Proses: Fuzzifikasi → Inferensi Mamdani → Defuzzifikasi Centroid
- Keunggulan dibanding PID: lebih robust terhadap variasi track, tidak perlu tuning matematis
- Implementasi pada ESP32: lookup table untuk efisiensi komputasi
- Perbandingan waktu eksekusi: Fuzzy ~200μs vs PID ~20μs pada ESP32
- Panjang: 170–200 kata
```

---

### Slide 28 – State Machine untuk Kondisi Khusus

**Prompt:**
```
Jelaskan State Machine (mesin keadaan) untuk menangani kondisi khusus pada robot line follower seperti persimpangan dan garis hilang. Sertakan:
- Mengapa state machine diperlukan: PID tidak cukup untuk situasi seperti garis hilang, persimpangan, atau marker
- State-state utama: IDLE → CALIBRATE → LINE_FOLLOW → LOST_LINE → INTERSECTION → STOP
- Diagram transisi state (dalam bentuk teks)
- Implementasi enum di C++: enum class RobotState { IDLE, CALIBRATE, FOLLOW, LOST, INTERSECT, STOP };
- Pendeteksian persimpangan: semua sensor aktif = persimpangan T atau +
- Recovery saat garis hilang: spin kiri/kanan berdasarkan arah terakhir (last direction)
- Penandaan finish line dengan reflective marker
- Panjang: 160–180 kata
```

---

## BAGIAN 7: 10 PERCOBAAN PRAKTIKUM (Slide 29–38)

### Slide 29 – Percobaan 1: Binary Line Follower (2 Sensor)

**Prompt:**
```
Buatkan deskripsi percobaan 1 robot line follower binary menggunakan hanya 2 sensor (sensor tengah-kiri dan tengah-kanan) untuk pengenalan dasar. Sertakan:
- Tujuan: memahami prinsip dasar on-off control, menyiapkan hardware dasar
- Hardware setup: pin sensor yang digunakan, kecepatan motor tetap
- Kode utama (pseudo-code + C++ snippet): if-else berdasarkan 2 sensor
- Lintasan yang direkomendasikan: oval sederhana, lebar garis 20mm
- Pengamatan: catat osilasi yang terjadi, kecepatan maksimum sebelum keluar jalur
- Pertanyaan analisis: mengapa robot berosilasi di garis lurus? Bagaimana mengatasinya?
- Parameter untuk dicatat: kecepatan motor, frekuensi osilasi, waktu selesai lintasan
- Panjang: 150–170 kata
```

---

### Slide 30 – Percobaan 2: Binary Line Follower (5 Sensor)

**Prompt:**
```
Buatkan deskripsi percobaan 2 menggunakan 5 sensor tengah dari array 12 sensor dengan algoritma binary bertingkat. Sertakan:
- Tujuan: mengurangi osilasi dibanding 2 sensor, memahami pengaruh jumlah sensor
- Perbedaan dengan percobaan 1: sensor aktif lebih banyak → respons lebih halus
- Tabel keputusan 5 sensor: 32 kemungkinan kondisi, sederhanakan ke 5 kondisi utama
- Implementasi kecepatan diferensial: sensor lebih luar terdeteksi → koreksi lebih besar
- Perbandingan kuantitatif dengan Percobaan 1: osilasi, kecepatan, akurasi
- Lintasan: tambahkan belokan 90° ke oval dari Percobaan 1
- Panjang: 150–170 kata
```

---

### Slide 31 – Percobaan 3: Weighted Position + P Controller

**Prompt:**
```
Buatkan deskripsi percobaan 3 menggunakan semua 12 sensor dengan weighted position dan kontrol Proportional (P). Sertakan:
- Tujuan: memahami weighted position, implementasi P controller pertama kali
- Langkah kalibrasi: scan permukaan putih dan hitam untuk normalisasi
- Tuning Kp: prosedur step-by-step, mulai dari 0.05 naikkan 0.02 tiap iterasi
- Grafik yang harus diplot: Kp vs. osilasi vs. kecepatan (tabel data eksperimen)
- Bagaimana menentukan Kp optimal dari grafik
- Lintasan: tambahkan S-curve ke lintasan Percobaan 2
- Pertanyaan: pada nilai Kp berapa robot mulai osilasi? Berapa Kp terbaik?
- Panjang: 150–170 kata
```

---

### Slide 32 – Percobaan 4: PD Controller

**Prompt:**
```
Buatkan deskripsi percobaan 4 implementasi PD Controller untuk meredam osilasi dari P Controller. Sertakan:
- Tujuan: memahami peran komponen derivative, membandingkan P vs PD
- Cara menambahkan Kd ke kode dari Percobaan 3
- Pengaruh Kd terlalu kecil vs terlalu besar pada perilaku robot
- Teknik tuning PD: fixed Kp, naikkan Kd bertahap hingga osilasi hilang
- Perbandingan video rekaman P vs PD pada belokan tajam (deskripsi visual)
- Lintasan: tambahkan hairpin curve (belokan 180°)
- Data yang dicatat: Kp, Kd, waktu lintasan, jumlah keluar garis
- Panjang: 150–170 kata
```

---

### Slide 33 – Percobaan 5: PID Controller Penuh

**Prompt:**
```
Buatkan deskripsi percobaan 5 implementasi PID Controller penuh dengan tuning sistematis. Sertakan:
- Tujuan: memahami peran integral (I), menerapkan PID penuh, menggunakan metode Ziegler-Nichols
- Kondisi yang memerlukan integral: robot tidak tepat di tengah saat lurus (steady-state error) → naikkan Ki kecil
- Anti-windup: implementasi dan pengaruh terhadap perilaku saat garis hilang
- Tabel tuning: eksperimen dengan 9 kombinasi Kp, Ki, Kd (3 level masing-masing)
- Grafik respons PID: plot error vs waktu dari data serial
- Lintasan: lintasan lengkap (oval + S-curve + hairpin + straight)
- Panjang: 150–170 kata
```

---

### Slide 35 – Percobaan 6: Integrasi MPU-6050 – Baca Data IMU

**Prompt:**
```
Buatkan deskripsi percobaan 6 membaca dan memvisualisasikan data raw MPU-6050 (accelerometer + gyroscope) pada robot line follower ESP32. Sertakan:
- Tujuan: memahami cara kerja IMU, membaca data 6-axis via I2C, kalibrasi offset gyroscope
- Setup kode: Wire.begin(21, 22), inisialisasi MPU6050 library, cek komunikasi (WHO_AM_I register)
- Prosedur kalibrasi offset: robot diam di permukaan rata, rata-rata 1000 sampel → simpan offset gyro
- Format Serial output yang disarankan: "ax,ay,az,gx,gy,gz,pitch,roll,yaw_rate"
- Visualisasi dengan Serial Plotter PlatformIO: plot pitch dan roll real-time saat robot dimiringkan
- Percobaan: miringkan robot ke depan, belakang, kiri, kanan → verifikasi nilai pitch/roll
- OLED display: baris 1=pitch, baris 2=roll, baris 3=yaw_rate
- Pertanyaan: mengapa nilai pitch tidak nol saat robot di bidang datar? Bagaimana mengatasinya?
- Panjang: 150–170 kata
```

---

### Slide 36 – Percobaan 7: Complementary Filter – Estimasi Sudut

**Prompt:**
```
Buatkan deskripsi percobaan 7 implementasi Complementary Filter untuk estimasi sudut yang stabil dari MPU-6050. Sertakan:
- Tujuan: memahami keterbatasan accelerometer dan gyroscope secara individual, mengimplementasikan fusion
- Eksperimen 1: hanya accelerometer → amati noise saat robot bergerak (getarkan robot)
- Eksperimen 2: hanya integrasikan gyro → amati drift dalam 60 detik (berapa derajat error?)
- Eksperimen 3: complementary filter α=0.98 → bandingkan dengan kedua di atas
- Tuning alpha: eksperimen α = 0.90, 0.95, 0.98, 0.99 → trade-off responsiveness vs stability
- Plot ketiga metode secara bersamaan via Serial Plotter (3 baris)
- Tabel hasil: drift setelah 60 detik untuk setiap metode
- Referensi: Mahony et al. (2008), Madgwick (2010) sebagai alternatif filter
- Panjang: 150–170 kata
```

---

### Slide 37 – Percobaan 8: Ramp Detection dan Speed Compensation

**Prompt:**
```
Buatkan deskripsi percobaan 8 menggunakan data pitch MPU-6050 untuk deteksi ramp dan kompensasi kecepatan otomatis. Sertakan:
- Tujuan: memprogram robot untuk mempertahankan kecepatan efektif di tanjakan dan turunan
- Setup lintasan: buat ramp dengan sudut 10° dan 20° dari akrilik atau buku
- Rumus kompensasi: base_speed_effective = base_speed × cos(pitch_rad) untuk tanjakan
  - Untuk turunan: tambahkan pengereman (brake) jika pitch < -5°
- Ambang deteksi: |pitch| > 5° = on ramp, |pitch| > 15° = steep ramp → peringatan buzzer
- Percobaan tanpa kompensasi vs dengan kompensasi: catat kecepatan aktual dan keluar garis
- Tantangan: sensor garis bisa terangkat dari permukaan di ramp tajam → perlu mount adjustable
- Panjang: 150–170 kata
```

---

### Slide 38 – Percobaan 9: Yaw Rate Correction (Gyro Feedback)

**Prompt:**
```
Buatkan deskripsi percobaan 9 menggunakan gyroscope Z-axis (yaw rate) sebagai feedback tambahan untuk mempertahankan robot tetap lurus pada bagian track lurus. Sertakan:
- Tujuan: mendemonstrasikan multi-sensor fusion, mengatasi motor drift dan slip ban
- Konsep: saat robot di garis lurus dan error sensor kecil → aktifkan koreksi yaw
  - koreksi = Kyaw × gz_filtered
  - motor_kiri  += koreksi; motor_kanan -= koreksi
- Tuning Kyaw: mulai 0.1, naikkan bertahap → hati-hati: terlalu besar akan mengganggu kontrol garis
- Aktivasi kondisional: hanya aktif jika |error_sensor| < threshold (misal 10)
- Low-pass filter pada gz: untuk mengurangi noise → alpha_filter = 0.8
- Perbandingan: track lurus panjang 2 meter, PD biasa vs PD + yaw correction → ukur deviasi dari garis
- Panjang: 150–170 kata
```

---

### Slide 39 – Percobaan 10: Speed Profiling Adaptif (dengan IMU)

**Prompt:**
```
Buatkan deskripsi percobaan 10 implementasi speed profiling adaptif - robot mempercepat di lurus dan melambat di tikungan secara otomatis. Sertakan:
- Konsep: kecepatan base tidak tetap, tapi bergantung pada absolut nilai error
- Rumus: base_speed = MAX_SPEED - (|error| × speed_reduction_factor)
- Implementasi: map(abs(error), 0, MAX_ERROR, MAX_SPEED, MIN_SPEED)
- Tuning speed_reduction_factor: terlalu besar → terlalu lambat di tikungan
- Manfaat: waktu lintasan total berkurang signifikan dibanding kecepatan konstan
- Pengukuran: catat waktu lintasan Percobaan 9 (yaw correction) vs Percobaan 10 (speed profiling adaptif + IMU)
- Lintasan: track dengan variasi panjang straight dan radius curve yang berbeda
- Panjang: 150–170 kata
```

---

### Slide 35 – Percobaan 7: Deteksi dan Penanganan Persimpangan

**Prompt:**
```
Buatkan deskripsi percobaan 7 implementasi deteksi dan penanganan persimpangan (intersection) menggunakan state machine. Sertakan:
- Tujuan: memprogram robot untuk mengambil keputusan di persimpangan T dan +
- Cara mendeteksi persimpangan: jika >8 dari 12 sensor aktif secara bersamaan
- Implementasi navigasi: baca marker warna (jika ada) atau jadwal keputusan pre-programmed (kiri/lurus/kanan)
- State machine: FOLLOWING → DETECT_INTERSECT → DECIDE → EXECUTE_TURN → RETURN_FOLLOWING
- Lintasan: buat track dengan 2 persimpangan T dan 1 persimpangan +
- Pengujian: program robot untuk mengambil rute tertentu dan verifikasi
- Panjang: 150–170 kata
```

---

### Slide 36 – Percobaan 8: OLED Dashboard dan Logging

**Prompt:**
```
Buatkan deskripsi percobaan 8 mengintegrasikan OLED SSD1306 sebagai dashboard real-time dan logging data via Serial. Sertakan:
- Tujuan: memahami pentingnya monitoring data real-time untuk tuning dan diagnostik
- OLED display layout: baris 1=status/mode, baris 2=posisi sensor, baris 3=error+PID output, baris 4=kecepatan L/R
- Teknik non-blocking display update: update setiap 200ms menggunakan millis(), tidak menghambat loop 100Hz
- Serial logging format untuk parsing: "timestamp,pos,error,L_speed,R_speed,kp,kd"
- Cara plot data dari Serial dengan Python matplotlib atau PlatformIO Serial Plotter
- Analisis data: bagaimana menggunakan grafik untuk tuning PID lebih efisien
- Panjang: 150–170 kata
```

---

### Slide 37 – Percobaan 9: Wireless Tuning via Wi-Fi (ESP32)

**Prompt:**
```
Buatkan deskripsi percobaan 9 implementasi wireless PID tuning menggunakan ESP32 Wi-Fi dan web server sederhana. Sertakan:
- Tujuan: memanfaatkan fitur unik ESP32 (Wi-Fi built-in) untuk real-time parameter tuning tanpa koneksi kabel
- Implementasi: ESP32 sebagai Access Point → smartphone connect → buka browser → input nilai Kp, Ki, Kd
- HTML form sederhana untuk input parameter (kode snippet HTML/ESP32 WebServer)
- Keamanan: hanya input angka dalam range tertentu yang diterima (validasi server-side)
- Cara menggunakan: robot berlari di track, engineer sambil melihat performa langsung mengubah parameter dari HP
- Manfaat industri: analog dengan SCADA parameter tuning di factory
- Catatan: mode AP tidak mengganggu performa robot karena dual-core ESP32
- Panjang: 150–170 kata
```

---

### Slide 38 – Percobaan 10: Kompetisi Lintasan Waktu (Time Trial)

**Prompt:**
```
Buatkan deskripsi percobaan 10 sebagai percobaan final: kompetisi time trial di lintasan lengkap untuk mengintegrasikan semua pembelajaran sebelumnya. Sertakan:
- Tujuan: mengintegrasikan semua percobaan sebelumnya, optimasi untuk kecepatan maksimum
- Spesifikasi lintasan kompetisi: panjang minimal 5 meter, lebar garis 20mm, minimal 4 tikungan
- Sistem penilaian: waktu lintasan + penalti per keluar garis + penalti per garis terlewat di persimpangan
- Strategi optimasi: urutan prioritas tuning (sensor kalibrasi → PD → speed profile → wireless tuning)
- Check list sebelum race: kalibrasi sensor, cek baterai, verifikasi semua sambungan
- Rekam video untuk tugas video: setup, kalibrasi, run pertama, tuning, run final
- Award: kelompok tercepat dan kelompok dengan peningkatan terbaik
- Panjang: 150–170 kata
```

---

## BAGIAN 8: TROUBLESHOOTING DAN OPTIMASI (Slide 39–42)

### Slide 39 – Troubleshooting Hardware

**Prompt:**
```
Buatkan panduan troubleshooting hardware robot line follower yang komprehensif, berdasarkan masalah umum yang sering dihadapi mahasiswa. Sertakan minimal 10 masalah umum dengan penyebab dan solusi:
1. Robot tidak bergerak sama sekali
2. Hanya satu motor yang bergerak
3. Sensor membaca nilai 0 semua
4. Sensor tidak merespons (selalu 1 atau selalu 0)
5. Robot berputar terus tidak mengikuti garis
6. OLED tidak menampilkan apa-apa
7. ESP32 tidak terdeteksi di USB
8. Baterai cepat habis
9. Robot berjalan miring meski garis lurus
10. SPI tidak berfungsi (data sensor acak)
Format: tabel 3 kolom (Masalah | Kemungkinan Penyebab | Solusi)
Panjang: 200–220 kata
```

---

### Slide 40 – Troubleshooting Software dan PID

**Prompt:**
```
Buatkan panduan troubleshooting software dan PID robot line follower, fokus pada masalah yang sering terjadi saat pemrograman ESP32. Sertakan:
- Robot berjalan maju kemudian tiba-tiba berhenti: kemungkinan penyebab (watchdog, stack overflow, infinite loop)
- Nilai sensor tidak berubah meski garis berubah: debug SPI, cek wiring 74HC165
- Robot berosilasi terus meski PID sudah di-set: analisis Kp terlalu besar, Kd kurang
- Robot lurus tapi tidak tepat di tengah (offset): cek kalibrasi sensor, cek alignment sensor board
- Integral windup menyebabkan robot berputar setelah kembali ke track: implementasi anti-windup
- Performa turun setelah ganti baterai: tegangan baterai mempengaruhi kecepatan motor, normalisasi
- Program compile tapi tidak upload ke ESP32: solusi driver CH340/CP2102, baud rate
- Panjang: 170–190 kata
```

---

### Slide 41 – Optimasi Performa Robot

**Prompt:**
```
Jelaskan teknik-teknik optimasi performa robot line follower untuk mencapai kecepatan dan akurasi maksimum dalam konteks kompetisi robot. Sertakan:
- Optimasi mekanik: balancing massa, alignment roda, material roda (rubber vs plastik)
- Optimasi sensor: jarak optimal, kemiringan sensor board, shielding dari cahaya ambient
- Optimasi kontrol: feed-forward kompensasi, look-ahead control (gunakan sensor ujung untuk prediksi belokan)
- Optimasi kode: interrupt-driven sensor reading, FreeRTOS task prioritization, avoid delay() dalam loop
- Optimasi daya: PWM frekuensi motor, baterai LiPo full charge, kabel pendek untuk drop tegangan rendah
- Benchmark: target waktu lintasan 5m dengan 4 tikungan untuk berbagai algoritma
- Panjang: 160–180 kata
```

---

### Slide 42 – Perbandingan Algoritma Kontrol

**Prompt:**
```
Buatkan tabel perbandingan komprehensif semua algoritma kontrol yang dipelajari di Modul 06 untuk line follower. Sertakan perbandingan untuk:
- Binary 2-sensor, Binary 5-sensor, P controller, PD controller, PID controller, Speed Adaptive PID, Fuzzy Logic
- Dimensi perbandingan: kemudahan implementasi, performa pada straight, performa pada tikungan, robustness terhadap noise, waktu tuning, kompleksitas kode (LoC), cocok untuk track mana
- Berikan rekomendasi: untuk pemula gunakan PD, untuk kompetisi gunakan Speed Adaptive PID atau Fuzzy
- Panjang: 180–200 kata, format tabel
```

---

## BAGIAN 9: KONEKSI KE INDUSTRI (Slide 43–45)

### Slide 43 – Line Follower sebagai Fondasi AGV

**Prompt:**
```
Jelaskan bagaimana robot line follower di modul ini merupakan fondasi dari Automated Guided Vehicle (AGV) yang digunakan di industri manufaktur modern, untuk memotivasi mahasiswa Teknologi Rekayasa Otomasi. Sertakan:
- Definisi AGV dan perbedaan dengan line follower sederhana (payload, safety, navigation complexity)
- Contoh AGV industrial: Toyota Material Handling, Jungheinrich, KUKA Mobile Robotics
- Upgrade dari line follower ke AGV: QR code navigation, SLAM, Lidar, safety scanners
- Standar industri AGV: ISO 3691-4 (keselamatan), VDA 5050 (komunikasi)
- Gaji insinyur AGV/robotika di Indonesia (2024): range Rp 10-25 juta/bulan
- Perusahaan di Indonesia yang butuh insinyur ini: PT Astra, PT Unilever, PT Indofood, SILO group
- Panjang: 170–190 kata
```

---

### Slide 44 – Hubungan dengan Modul Lain dan Kurikulum

**Prompt:**
```
Jelaskan hubungan Modul 06 "Build Line Follower" dengan modul-modul lain dalam kurikulum Praktikum Mekatronika dan Robotika, membentuk narasi pembelajaran yang utuh. Sertakan:
- Modul 01 (Desain PCB) → Modul 06: PCB yang didesain kini disolder dan difungsikan
- Modul 03 (Fusion360) → Modul 06: chassis yang mungkin di-3D print dari Modul 3
- Modul 04 (IoT ESP32) → Modul 06: wireless tuning menggunakan Wi-Fi yang dipelajari di Modul 4
- Modul 07 (Wall Follower) → Modul 06+sensor ultrasonik: natural extension dari line follower
- Modul 08-11 (ROS) → Modul 06: persiapan memahami mobile robot, odometry, dan SLAM
- Keterampilan transferable: PID, state machine, sensor fusion, debugging embedded
- Panjang: 160–180 kata
```

---

### Slide 45 – Kesimpulan dan Langkah Selanjutnya

**Prompt:**
```
Buatkan narasi penutup yang kuat untuk presentasi Modul 06 "Build Line Follower" yang merangkum pembelajaran dan memotivasi mahasiswa untuk terus berkembang. Sertakan:
- 5 kompetensi utama yang telah dicapai: soldering, assembly mekanik, PlatformIO, PID tuning, sistem kontrol
- Refleksi: dari PCB mentah (Modul 01) hingga robot yang berlari mandiri
- Challenge selanjutnya: ikut kontes robot lokal/nasional (KRI, KRCI, INABOT)
- Quote inspiratif dari tokoh robotika dunia (Rodney Brooks atau Marvin Minsky)
- Call to action: post video robot kalian di media sosial dengan hashtag prodi
- Preview Modul 07 (Wall Follower): dari mengikuti garis ke menghindari dinding
- Panjang: 140–160 kata, penuh semangat dan motivasi
```

---

*Dokumen prompt ini dibuat untuk mendukung pembelajaran berbasis AI di Prodi Teknologi Rekayasa Otomasi.*  
*Gunakan NotebookLLM atau AI assistant lainnya untuk menghasilkan konten berdasarkan prompt di atas.*  
*Sesuaikan narasi yang dihasilkan dengan kondisi laboratorium dan kemampuan mahasiswa.*
