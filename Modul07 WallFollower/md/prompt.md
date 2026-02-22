# PROMPT NOTEBOOKLM – MODUL 07: WALL FOLLOWER ROBOT ESP32

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 07 – Wall Follower  
**Jumlah Prompt:** 45 Prompt untuk 45 Slide Presentasi  
**Platform AI:** NotebookLLM / Google NotebookLM  

---

> **PETUNJUK PENGGUNAAN:**
> Upload file `materi.md`, `jobsheet.md`, dan `project.md` ke NotebookLM terlebih dahulu.
> Kemudian gunakan prompt di bawah ini satu per satu untuk menghasilkan konten setiap slide.

---

## BAGIAN A: SLIDE PEMBUKA & OVERVIEW (Slide 1–5)

---

### PROMPT 01 – SLIDE PEMBUKA / JUDUL

```
Buatkan konten slide pembuka (title slide) untuk presentasi akademik berjudul 
"Wall Follower Robot dengan ESP32 dan PlatformIO". 
Slide harus mencakup:
- Judul utama yang menarik dan profesional
- Subjudul: Modul 07 Praktikum Mekatronika dan Robotika
- Nama Program Studi: Teknologi Rekayasa Otomasi
- Tagline singkat (1 kalimat) yang mendeskripsikan esensi wall follower
- Daftar topik yang akan dibahas (6-8 poin dalam format bullet)
Gunakan bahasa Indonesia yang formal dan akademis.
Format output: teks siap pakai untuk slide presentasi.
```

---

### PROMPT 02 – SLIDE OVERVIEW MODUL

```
Berdasarkan materi wall follower yang tersedia, buatkan konten slide overview modul yang mencakup:
1. Tujuan pembelajaran modul (5-6 poin SMART)
2. Kompetensi yang akan dicapai mahasiswa (dalam format tabel: Kode | Kompetensi | Indikator)
3. Hubungan modul 07 dengan modul sebelumnya (01, 03, 06)
4. Timeline praktikum (gambaran singkat setiap pertemuan)
5. Alat dan bahan utama yang dibutuhkan
Sertakan juga pertanyaan pemantik untuk mahasiswa: "Apa bedanya robot yang mengikuti garis dengan robot yang mengikuti dinding?"
Bahasa Indonesia, format slide presentasi.
```

---

### PROMPT 03 – SLIDE MOTIVASI & APLIKASI NYATA

```
Buatkan slide motivasi yang menjelaskan mengapa wall follower robot penting dipelajari.
Slide harus mencakup:
- 5 aplikasi nyata wall follower di industri (dengan gambar deskripsi/ikon)
- Perbandingan robot dengan dan tanpa kemampuan wall following
- Contoh produk komersial yang menggunakan prinsip wall follower (robot vacuum, AGV, dsb.)
- Statistik atau data pasar robot otonom (jika tersedia dalam materi)
- Quote inspiratif dari tokoh robotika
Gunakan pendekatan storytelling: mulai dari masalah → solusi → aplikasi.
Format: slide presentasi dengan narasi singkat per poin.
```

---

### PROMPT 04 – SLIDE PETA KONSEP WALL FOLLOWER

```
Buatkan slide berisi peta konsep (concept map) wall follower robot yang menghubungkan:
- Komponen hardware: ESP32, HC-SR04, IR sensor, motor driver, motor DC
- Algoritma: right-hand rule, left-hand rule, PID, fuzzy logic
- Mode operasi: wall follow, line follow, explore, obstacle avoidance
- Interface: WiFi AP, web server, parameter setting
Visualisasikan dalam format diagram hierarki atau mind map yang dapat dijelaskan secara verbal.
Sertakan penjelasan singkat 2-3 kalimat untuk setiap cabang utama.
Bahasa Indonesia, format slide presentasi.
```

---

### PROMPT 05 – SLIDE PERBANDINGAN WALL FOLLOWER vs LINE FOLLOWER

```
Buatkan slide perbandingan mendalam antara Wall Follower dan Line Follower robot.
Tampilkan dalam format tabel lengkap dengan aspek berikut:
- Referensi navigasi (apa yang dijadikan acuan)
- Sensor yang digunakan
- Algoritma kontrol
- Keterbatasan lingkungan
- Kelebihan dan kekurangan masing-masing
- Contoh aplikasi spesifik
- Kompleksitas implementasi
- Kemampuan adaptasi lingkungan baru
Akhiri dengan slide insight: kapan menggunakan wall follower dan kapan line follower lebih tepat.
Bahasa Indonesia, format tabel dan bullet points.
```

---

## BAGIAN B: SENSOR DAN HARDWARE (Slide 6–12)

---

### PROMPT 06 – SLIDE SENSOR ULTRASONIK HC-SR04

```
Buatkan slide lengkap tentang sensor ultrasonik HC-SR04 untuk wall follower robot.
Cakupan materi:
1. Prinsip kerja Time of Flight (ToF) - dengan diagram timing signal
2. Spesifikasi teknis lengkap dalam tabel
3. Rumus perhitungan jarak (derivasi lengkap + contoh numerik)
4. Penempatan sensor optimal (kiri, depan, kanan) beserta alasannya
5. Masalah umum dan troubleshooting (tabel: masalah | penyebab | solusi)
6. Level shifting: kenapa HC-SR04 membutuhkan 5V dan ESP32 3.3V logic
7. Kode Arduino/PlatformIO untuk membaca sensor (tampilkan kode lengkap)
Sertakan diagram timing sinyal TRIG dan ECHO.
Bahasa Indonesia dengan istilah teknis.
```

---

### PROMPT 07 – SLIDE SENSOR IR UNTUK WALL & LINE DETECTION

```
Buatkan slide yang menjelaskan dua fungsi sensor IR pada robot wall follower:
BAGIAN 1 - IR untuk deteksi dinding jarak dekat:
- Prinsip reflektansi IR
- Sharp GP2Y0A series (analog distance sensor)
- Karakteristik kurva tegangan vs jarak
- Kode konversi ADC ke jarak

BAGIAN 2 - IR untuk deteksi garis (line follower mode):
- Sensor IR reflektansi digital (TCRT5000/QRE1113)
- Kalibrasi threshold hitam/putih
- Array sensor untuk deteksi posisi garis

BAGIAN 3 - Perbandingan HC-SR04 vs IR:
- Tabel perbandingan spesifikasi
- Kapan memilih ultrasonik vs IR

Sertakan diagram skematik koneksi ke ESP32 dan kode baca sensor.
Bahasa Indonesia.
```

---

### PROMPT 08 – SLIDE ESP32 ARSITEKTUR DAN FITUR

```
Buatkan slide penjelasan arsitektur ESP32 yang relevan untuk wall follower robot.
Fokus pada:
1. Dual-core Xtensa LX6: bagaimana memanfaatkan 2 core untuk robot
   - Core 0: sensor reading dan WiFi
   - Core 1: motor control dan algoritma
2. LEDC (LED Control): cara menghasilkan PWM untuk motor driver
3. Timer hardware: penggunaan untuk ultrasonik timing yang presisi
4. ADC 12-bit: membaca sensor analog dengan resolusi tinggi
5. WiFi AP mode: ESP32 sebagai access point tanpa router eksternal
6. Pinout ESP32 DevKit V1: identifikasi pin yang digunakan (tabel)
7. Perbandingan ESP32 vs Arduino Uno untuk robot otonom

Sertakan diagram alokasi pin (pin assignment table).
Bahasa Indonesia, format teknis presentasi.
```

---

### PROMPT 09 – SLIDE MOTOR DRIVER L298N / L293D

```
Buatkan slide penjelasan motor driver untuk wall follower robot.
Cakupan:
1. Konsep H-Bridge: mengapa diperlukan untuk kontrol motor DC
2. Spesifikasi L298N: tegangan, arus, jumlah channel
3. Tabel kebenaran (truth table) kontrol arah motor
4. Perhitungan PWM: hubungan duty cycle dengan kecepatan
5. Wiring diagram: ESP32 → L298N → Motor DC (kiri dan kanan)
6. Kode PlatformIO untuk kontrol motor dengan LEDC API
7. Masalah panas berlebih pada L298N dan solusinya (heatsink)
8. Alternatif: TB6612FNG, DRV8833 untuk efisiensi lebih baik

Sertakan tabel pin mapping ESP32 ↔ L298N.
Bahasa Indonesia.
```

---

### PROMPT 10 – SLIDE DESAIN MEKANIK ROBOT

```
Buatkan slide tentang desain mekanik robot wall follower yang terhubung dengan materi Modul 03 (Fusion360).
Cakupan:
1. Tipe chassis robot: differential drive vs holonomic
2. Dimensi ideal chassis untuk wall follower (panjang, lebar, tinggi)
3. Penempatan sensor yang optimal:
   - HC-SR04 kiri: sudut 90° ke sisi kiri
   - HC-SR04 depan: tegak lurus depan
   - HC-SR04 kanan: sudut 90° ke sisi kanan
   - IR sensor lantai: di bawah depan robot
4. Center of mass dan stabilitas gerakan
5. Mounting motor dan roda: turning radius calculation
6. Material chassis: akrilik vs PCB custom vs 3D print
7. Bill of Materials (BOM) mekanik

Kaitkan dengan desain PCB dari Modul 01 (PCB sebagai base board).
Bahasa Indonesia.
```

---

### PROMPT 11 – SLIDE WIRING DIAGRAM LENGKAP

```
Buatkan slide wiring diagram komprehensif untuk wall follower robot ESP32.
Tampilkan koneksi lengkap untuk:
1. Sensor HC-SR04 × 3 (kiri, depan, kanan) → ESP32
   - Tabel pin: TRIG_L=5, ECHO_L=18, TRIG_F=19, ECHO_F=21, TRIG_R=22, ECHO_R=23
   - Catatan level shifting ECHO 5V → 3.3V (voltage divider)
2. Sensor IR line × 4 → ESP32
   - Pin: IR_LL=34, IR_LR=35, IR_RL=32, IR_RR=33
3. Motor driver L298N → ESP32
   - IN1=25, IN2=26, IN3=27, IN4=14, ENA=12, ENB=13
4. Power supply: baterai 7.4V → L298N → 5V via LM7805 → ESP32
5. LED indikator × 4 untuk status mode
6. Buzzer untuk feedback audio

Format: deskripsi tabel koneksi + diagram ASCII sederhana.
Sertakan catatan keselamatan listrik.
Bahasa Indonesia.
```

---

### PROMPT 12 – SLIDE SETUP PLATFORMIO

```
Buatkan slide panduan setup PlatformIO untuk proyek wall follower ESP32.
Langkah-langkah yang harus dijelaskan:
1. Instalasi VS Code + PlatformIO extension
2. Membuat project baru: Board = "Espressif ESP32 Dev Module"
3. Konfigurasi platformio.ini (tampilkan kode lengkap):
   - Platform, board, framework
   - Monitor speed
   - Library dependencies (ESPAsyncWebServer, ArduinoJson, electroniccats/MPU6050)
   - Upload speed
4. Struktur folder proyek PlatformIO yang benar:
   src/main.cpp, include/config.h, lib/, test/
5. Upload program pertama: "Hello World" + blink LED
6. Menggunakan Serial Monitor di PlatformIO
7. Tips debugging: Serial.print vs breakpoint

Sertakan screenshot placeholder dan kode konfigurasi.
Bahasa Indonesia, step-by-step guide.
```

---

### PROMPT 12B – SLIDE SENSOR IMU MPU-6050 (BAGIAN 1: DASAR)

```
Buatkan slide penjelasan lengkap sensor IMU MPU-6050 untuk wall follower robot.
Cakupan:
1. Apa itu IMU? Perbedaan accelerometer vs gyroscope vs magnetometer
2. MPU-6050: sensor 6-DOF (3-axis accel + 3-axis gyro)
3. Cara kerja MEMS accelerometer: massa pegas mikro, perubahan kapasitansi
4. Cara kerja MEMS gyroscope: efek Coriolis pada massa getar
5. Spesifikasi MPU-6050 (tabel lengkap): resolusi, range, noise, supply
6. Koneksi ke ESP32 via I2C (SDA=GPIO21, SCL=GPIO22, alamat 0x68/0x69)
7. Kode inisialisasi dengan library electroniccats/MPU6050
8. Mengapa perlu kalibrasi offset? Demonstrasi numerik (robot diam tapi GyroZ ≠ 0)

Sertakan diagram koneksi I2C dan timing diagram I2C.
Bahasa Indonesia.
```

---

### PROMPT 12C – SLIDE SENSOR IMU MPU-6050 (BAGIAN 2: KALKULASI SUDUT)

```
Buatkan slide penjelasan cara menghitung sudut (pitch, roll, yaw) dari MPU-6050.
Cakupan:
1. Metode 1 – Accelerometer only:
   - Rumus pitch = atan2(-ax, sqrt(ay²+az²))
   - Rumus roll  = atan2(ay, az)
   - Kelebihan: tidak drift | Kekurangan: noise saat bergerak
2. Metode 2 – Gyroscope integration:
   - angle += gyro_rate × dt
   - Kelebihan: smooth | Kekurangan: drift bertambah seiring waktu
3. Metode 3 – Complementary Filter (DIREKOMENDASIKAN):
   - angle = α × (angle + gyro×dt) + (1-α) × accel_angle
   - Visualisasi: accel = slow truth, gyro = fast smooth → gabungan terbaik
   - Pilih α = 0.96 (96% gyro, 4% accel)
4. Metode 4 – DMP onboard MPU-6050:
   - Quaternion fusion dalam chip, output langsung yaw/pitch/roll
   - Library: MPU6050_6Axis_MotionApps20.h
5. Perbandingan keempat metode (tabel: akurasi, latency, CPU load)
6. Kode implementasi complementary filter

Bahasa Indonesia, dengan grafik perbandingan sinyal (konseptual).
```

---

### PROMPT 12D – SLIDE MPU-6050: APLIKASI DI WALL FOLLOWER

```
Buatkan slide tentang aplikasi konkret MPU-6050 pada sistem wall follower robot.
Cakupan dengan kode contoh masing-masing:

1. GYRO-ASSISTED STRAIGHT MOVEMENT:
   - Masalah: motor kiri/kanan sedikit berbeda kecepatan → robot miring
   - Solusi: PID heading dengan gyro Z sebagai feedback
   - Kode: moveForwardStraight(baseSpeed, targetHeading)

2. GYRO-ASSISTED 90° TURN:
   - Masalah: belokan berbasis timer tidak akurat (bergantung baterai, permukaan)
   - Solusi: berhenti tepat saat gyro menunjukkan 90° terputar
   - Kode: turnRight90Gyro() dengan while loop + yaw comparison

3. TILT/ROLL SAFETY DETECTION:
   - Masalah: robot terjatuh dari meja atau terguling di permukaan miring
   - Solusi: deteksi roll > 30° atau pitch > 30° → motor stop otomatis
   - Kode: detectTilt(compPitch, compRoll)

4. IMPACT/COLLISION DETECTION:
   - Masalah: robot bertabrakan sebelum sensor ultrasonik mendeteksi
   - Solusi: spike pada total acceleration > 2.5g → emergency stop
   - Kode: detectImpact()

5. DEAD RECKONING SEDERHANA:
   - Integrasi gyro Z untuk estimasi posisi sudut saat bernavigasi
   - Akurasi terbatas, cocok untuk jangka pendek

Bahasa Indonesia, sertakan diagram alir untuk setiap aplikasi.
```

---

## BAGIAN C: ALGORITMA & KONTROL (Slide 13–22)

---

### PROMPT 13 – SLIDE RIGHT-HAND RULE & LEFT-HAND RULE

```
Buatkan slide penjelasan mendalam tentang Right-Hand Rule dan Left-Hand Rule dalam wall following.
Cakupan:
1. Definisi formal kedua aturan
2. Flowchart pengambilan keputusan (Right-Hand Rule):
   - Cek dinding depan → belok kiri atau kanan?
   - Cek dinding kanan → maju atau belok kanan?
3. Flowchart pengambilan keputusan (Left-Hand Rule)
4. Contoh maze: robot menggunakan Right-Hand Rule berhasil keluar labirin
5. Keterbatasan: maze dengan rintangan tidak terhubung ke dinding luar
6. Kapan Right lebih baik dari Left (dan sebaliknya)
7. Implementasi dalam C++ (tampilkan fungsi determineAction)

Sertakan diagram maze ASCII dengan path robot yang ditandai.
Bahasa Indonesia.
```

---

### PROMPT 14 – SLIDE KONTROLER PID

```
Buatkan slide penjelasan komprehensif PID controller untuk wall follower robot.
Harus mencakup:
1. Analogi intuitif PID: Pengemudi mobil yang menjaga jarak ke bahu jalan
2. Persamaan matematis PID (lengkap dengan notasi)
3. Peran masing-masing komponen:
   - P: respons proporsional (contoh numerik)
   - I: eliminasi steady-state error (contoh kasus)
   - D: prediksi dan reduksi overshoot (contoh kasus)
4. Grafik respons: underdamped, overdamped, critically damped
5. Metode tuning: Ziegler-Nichols (tabel rumus)
6. Implementasi PID dalam C++ (kelas PIDController lengkap)
7. Anti-windup: mengapa penting dan cara implementasinya
8. Nilai Kp, Ki, Kd awal yang direkomendasikan untuk robot ESP32

Gunakan contoh spesifik: setpoint 15 cm, actual 20 cm.
Bahasa Indonesia, dengan persamaan LaTeX jika memungkinkan.
```

---

### PROMPT 15 – SLIDE FUZZY LOGIC CONTROLLER

```
Buatkan slide penjelasan Fuzzy Logic Controller untuk wall follower.
Struktur slide:
1. Mengapa fuzzy logic? Masalah dengan threshold biner
2. Tahapan fuzzy control:
   a. Fuzzifikasi: membership function untuk error jarak
   b. Rule evaluation: tabel aturan (rule base)
   c. Defuzzifikasi: konversi ke output crisp
3. Definisi 5 himpunan fuzzy: VERY_CLOSE, CLOSE, ON_TARGET, FAR, VERY_FAR
4. Membership function: segitiga dan trapesoid (dengan grafik ASCII)
5. Tabel aturan lengkap (Error × Rate_of_Change → Output)
6. Perbandingan respons PID vs Fuzzy Logic (grafik konseptual)
7. Implementasi sederhana fuzzy dalam C++ untuk ESP32
8. Kapan fuzzy lebih unggul dari PID?

Bahasa Indonesia dengan penjelasan step-by-step.
```

---

### PROMPT 16 – SLIDE BUG ALGORITHM (MAZE SOLVING)

```
Buatkan slide penjelasan Bug Algorithm untuk navigasi robot dalam maze.
Cakupan:
1. Klasifikasi Bug Algorithm: Bug0, Bug1, Bug2, Tangent Bug
2. Bug0 Algorithm: 
   - Deskripsi dan pseudocode
   - Diagram path dalam maze sederhana
3. Bug1 Algorithm:
   - Deskripsi dan pseudocode  
   - Jaminan konvergensi ke target
4. Perbandingan efisiensi path: Bug0 vs Bug1 vs Bug2
5. Implementasi Bug1 dalam C++ (pseudocode → kode)
6. Integrasi dengan ESP32: penggunaan encoder atau odometri sederhana
7. Limitasi: asumsi yang diperlukan (obstacle convex, dsb.)

Sertakan diagram ASCII yang menunjukkan path robot di maze.
Bahasa Indonesia.
```

---

### PROMPT 17 – SLIDE NAVIGASI HYBRID (WALL + LINE)

```
Buatkan slide tentang sistem navigasi hybrid yang menggabungkan Wall Follower dan Line Follower.
Cakupan:
1. Motivasi: mengapa hybrid navigation lebih powerful
2. State machine diagram (diagram mesin keadaan):
   - State: STOP, LINE_FOLLOW, WALL_FOLLOW_L, WALL_FOLLOW_R, EXPLORE
   - Transisi antar state beserta kondisi trigger
3. Prioritas mode (priority hierarchy):
   - Emergency stop → Line follow → Wall follow → Explore
4. Implementasi state machine dalam C++:
   - Enum RobotMode
   - Fungsi determineMode()
   - Switch case eksekusi mode
5. Contoh skenario: robot mengikuti garis → garis berakhir → otomatis wall follow
6. Parameter yang dapat dikonfigurasi via WiFi untuk tiap mode

Sertakan diagram state machine (format ASCII).
Bahasa Indonesia.
```

---

### PROMPT 18 – SLIDE PENGOLAHAN DATA SENSOR

```
Buatkan slide tentang teknik pengolahan data sensor untuk wall follower yang lebih andal.
Cakupan:
1. Moving Average Filter:
   - Mengapa diperlukan (noise ultrasonik)
   - Implementasi ring buffer dalam C++
   - Perbandingan sinyal raw vs filtered
2. Median Filter:
   - Lebih baik untuk spike/outlier
   - Implementasi insertion sort untuk 5 sampel
3. Kalman Filter (konseptual):
   - Dasar teori tanpa derivasi penuh
   - Kapan diperlukan untuk sensor fusion
4. Sensor Fusion: kombinasi ultrasonik + IR untuk estimasi jarak
5. Dead zone handling: apa yang dilakukan jika sensor timeout
6. Kode contoh: fungsi readFilteredDistance()

Bahasa Indonesia, sertakan perbandingan grafik signal.
```

---

### PROMPT 19 – SLIDE KONTROL KECEPATAN MOTOR

```
Buatkan slide tentang kontrol kecepatan motor DC untuk wall follower yang smooth.
Cakupan:
1. PWM dan hubungannya dengan kecepatan motor
2. Speed ramping: why abrupt speed change is bad (inertia)
   - Fungsi ramp up dan ramp down
   - Implementasi dalam C++
3. Motor deadband: threshold minimum duty cycle agar motor berputar
4. Differential drive kinematics:
   - Hubungan kecepatan kiri/kanan dengan radius belokan
   - Rumus: v_left dan v_right untuk radius R
5. Saturasi output PID: constrain() dan clamping
6. Feed-forward term: base speed sebagai offset PID
7. Backlash compensation (jika menggunakan gear motor)

Contoh numerik: kecepatan 150 PWM, PID output +30 → kiri=120, kanan=180.
Bahasa Indonesia.
```

---

### PROMPT 20 – SLIDE PENANGANAN SUDUT DAN BELOKAN

```
Buatkan slide tentang bagaimana wall follower robot menangani sudut dan belokan tajam.
Cakupan:
1. Jenis belokan: sudut tumpul (>90°), tegak (90°), lancip (<90°)
2. Deteksi sudut dengan sensor:
   - Sensor depan: mendeteksi jarak tiba-tiba berkurang
   - Sensor samping: mendeteksi dinding yang menghilang
3. Algoritma belokan pada labirin:
   - Inner corner (sudut dalam): robot cenderung terlalu dekat
   - Outer corner (sudut luar): robot cenderung terlalu jauh
4. Strategi belokan:
   - Pirouette turn: berhenti, putar di tempat
   - Sweeping turn: belokan sambil maju
5. Timing dan kecepatan saat belokan
6. Implementasi dalam C++: fungsi handleCorner()
7. Pengujian: labirin kotak 3×3 dengan semua tipe sudut

Sertakan diagram labirin dengan sudut-sudut yang ditandai.
Bahasa Indonesia.
```

---

### PROMPT 21 – SLIDE WALL FOLLOWING DENGAN PID: STUDI KASUS

```
Buatkan slide studi kasus implementasi PID wall follower secara lengkap.
Skenario: Robot mengikuti dinding kiri di koridor selebar 50 cm.
Setpoint: 15 cm dari dinding kiri.

Tampilkan:
1. Grafik respons sistem untuk 3 set Kp/Ki/Kd berbeda:
   - Too aggressive (Kp=10, Ki=0, Kd=0): osilasi
   - Too sluggish (Kp=0.5, Ki=0, Kd=0): lambat koreksi
   - Optimal (Kp=3, Ki=0.05, Kd=1): smooth
2. Tabel data pengujian (jarak, error, PID output, kecepatan motor)
3. Analisis transient response: rise time, overshoot, settling time
4. Efek disturbance: lantai tidak rata, pantulan palsu
5. Rekomendasi nilai awal PID untuk berbagai ukuran robot

Format: slide analisis dengan tabel + grafik (deskriptif).
Bahasa Indonesia.
```

---

### PROMPT 22 – SLIDE OBSTACLE AVOIDANCE INTEGRATION

```
Buatkan slide tentang integrasi obstacle avoidance ke dalam sistem wall follower.
Cakupan:
1. Perbedaan dinding (wall) vs rintangan (obstacle):
   - Dinding: permanen, robot mengikutinya
   - Rintangan: sementara, robot menghindarinya
2. Algoritma deteksi dan penghindaran rintangan:
   - Simple threshold: jika depan < 10 cm, berhenti dan belok
   - VFH (Vector Field Histogram) konseptual
3. Integrasi dengan wall following:
   - Priority: obstacle avoidance > wall following
   - Resume wall following setelah menghindari obstacle
4. Skenario: wall follower bertemu kursi di tengah koridor
5. Implementasi: fungsi avoidObstacle() dalam C++
6. Testing: obstacle bergerak (orang berjalan) vs statis (kotak)

Bahasa Indonesia.
```

---

## BAGIAN D: WIFI & KONFIGURASI (Slide 23–28)

---

### PROMPT 23 – SLIDE ESP32 WIFI ACCESS POINT

```
Buatkan slide penjelasan fitur ESP32 WiFi Access Point untuk konfigurasi robot.
Cakupan:
1. Perbedaan mode WiFi: Station (STA) vs Access Point (AP) vs AP+STA
2. Mengapa AP mode dipilih untuk konfigurasi robot:
   - Tidak memerlukan router
   - Koneksi langsung smartphone ke robot
   - Lebih portable di lapangan
3. Konfigurasi AP di ESP32:
   - SSID dan password
   - IP address statis: 192.168.4.1
   - Kode: WiFi.softAP() + WiFi.softAPConfig()
4. Jumlah client yang dapat terhubung (maksimal 4)
5. Bandwidth dan latency AP mode untuk real-time monitoring
6. Keamanan: password protection, MAC filtering (opsional)
7. Cara koneksi dari smartphone: WiFi settings → pilih SSID robot

Bahasa Indonesia, sertakan screenshot placeholder.
```

---

### PROMPT 24 – SLIDE WEB SERVER DENGAN ESPASYNCWEBSERVER

```
Buatkan slide penjelasan implementasi web server di ESP32 menggunakan ESPAsyncWebServer.
Cakupan:
1. Mengapa AsyncWebServer lebih baik dari WebServer standar:
   - Non-blocking operation
   - Mendukung WebSocket
   - Lebih efisien untuk ESP32
2. Instalasi library: platformio.ini lib_deps
3. REST API endpoints untuk robot wall follower:
   - GET /status → JSON status lengkap
   - GET /params → JSON parameter PID
   - POST /params → Update parameter
   - POST /control → Kontrol robot
4. Kode: setup server dengan handler untuk tiap endpoint
5. JSON response format (tampilkan contoh JSON)
6. CORS headers untuk akses dari browser
7. Error handling: 404, 400 response

Tampilkan kode C++ untuk setup web server.
Bahasa Indonesia.
```

---

### PROMPT 25 – SLIDE WEB INTERFACE PARAMETER SETTING

```
Buatkan slide yang menjelaskan web interface untuk setting parameter robot wall follower via smartphone.
Cakupan:
1. Desain UI mobile-friendly (deskripsi layout):
   - Header: status robot (mode, jarak sensor)
   - Parameter section: slider untuk Kp, Ki, Kd, setpoint
   - Control buttons: Start, Stop, Mode (Left/Right wall)
   - Real-time graph: jarak sensor kiri vs waktu
2. HTML/CSS/JavaScript (tampilkan kode ringkas)
3. Cara update parameter:
   - Geser slider → JavaScript fetch POST /params
   - Server update config → langsung efektif tanpa restart
4. Parameter yang dapat diubah real-time (tabel lengkap)
5. Penyimpanan parameter ke EEPROM/Preferences:
   - Agar tidak hilang saat restart
   - Kode: Preferences library ESP32
6. Tampilan Serial Monitor saat parameter berubah

Sertakan wireframe ASCII dari tampilan web.
Bahasa Indonesia.
```

---

### PROMPT 26 – SLIDE WEBSOCKET UNTUK MONITORING REAL-TIME

```
Buatkan slide tentang penggunaan WebSocket untuk monitoring sensor real-time pada wall follower robot.
Cakupan:
1. Perbedaan HTTP polling vs WebSocket:
   - HTTP: setiap 500ms client tanya server (tidak efisien)
   - WebSocket: server push data ke client (lebih efisien, lebih cepat)
2. Implementasi WebSocket di ESP32 (ESPAsyncWebServer):
   - onEvent handler untuk WebSocket
   - Broadcast data setiap 100ms
3. Format data JSON yang dikirim:
   ```json
   {"dL":15.2,"dF":45.8,"dR":16.1,"mode":"WALL_LEFT","speedL":145,"speedR":165}
   ```
4. JavaScript client untuk menerima dan menampilkan data real-time
5. Chart.js untuk visualisasi grafik sensor real-time (konsep)
6. Disconnect handling: reconnect otomatis
7. Bandwidth estimation: data setiap 100ms × 200 bytes = 2KB/s

Bahasa Indonesia.
```

---

### PROMPT 27 – SLIDE PENYIMPANAN PARAMETER (PREFERENCES/EEPROM)

```
Buatkan slide tentang cara menyimpan dan memuat parameter robot secara persisten di ESP32.
Cakupan:
1. Mengapa perlu persistent storage:
   - Parameter PID tidak hilang saat baterai habis
   - Kalibrasi sensor tersimpan
2. Dua opsi storage di ESP32:
   a. EEPROM emulation: byte-level access, ukuran terbatas
   b. Preferences library: key-value store, lebih mudah, NVS flash
3. Implementasi dengan Preferences:
   ```cpp
   Preferences prefs;
   prefs.begin("wallbot", false);
   prefs.putFloat("kp", Kp);
   float kp = prefs.getFloat("kp", 3.0); // dengan default value
   prefs.end();
   ```
4. Kapan harus save: setelah menerima POST /params dari web
5. Factory reset: endpoint /reset yang menghapus semua preferences
6. Tabel: semua key yang disimpan beserta default value

Bahasa Indonesia.
```

---

### PROMPT 28 – SLIDE OTA UPDATE (OVER THE AIR)

```
Buatkan slide tentang update firmware robot wall follower secara nirkabel menggunakan OTA.
Cakupan:
1. Apa itu OTA update dan manfaatnya untuk robot
2. ESP32 OTA menggunakan ArduinoOTA library
3. Setup OTA dalam proyek PlatformIO:
   - Tambahan kode inisialisasi ArduinoOTA
   - platformio.ini: upload_protocol = espota, upload_port = IP address
4. Alur OTA update:
   - Kompilasi firmware baru → PlatformIO → Upload via WiFi
   - Robot tetap bergerak, lalu reboot setelah upload selesai
5. Keamanan OTA: password protection
6. Partisi flash ESP32: OTA membutuhkan 2 slot firmware
7. Best practice: cek versi firmware via /status endpoint

Tampilkan kode setup OTA yang minimal.
Bahasa Indonesia.
```

---

## BAGIAN E: PERCOBAAN PRAKTIKUM (Slide 29–38)

---

### PROMPT 29 – SLIDE PERCOBAAN 1-2 (SENSOR DASAR)

```
Buatkan slide deskripsi percobaan 1 dan 2 dari praktikum wall follower.

PERCOBAAN 1 – Kalibrasi Sensor HC-SR04:
- Tujuan: memahami karakteristik dan akurasi sensor
- Langkah: baca jarak pada 5cm, 10cm, 15cm, 20cm, 30cm, 50cm
- Data yang dicatat: nilai raw, nilai rata-rata 10 sampel, error vs penggaris
- Kesimpulan yang diharapkan

PERCOBAAN 2 – Wall Detection Threshold:
- Tujuan: menentukan threshold jarak "ada dinding" vs "tidak ada dinding"
- Langkah: gerakkan objek mendekat dari 50cm → 5cm, catat perubahan output
- Tuning: tentukan nilai threshold optimal untuk tiap sensor
- Implementasi dalam kode: fungsi isWallDetected()

Format: slide dengan tabel data, prosedur step-by-step, diagram setup.
Bahasa Indonesia.
```

---

### PROMPT 30 – SLIDE PERCOBAAN 3-4 (WALL FOLLOWING DASAR)

```
Buatkan slide deskripsi percobaan 3 dan 4.

PERCOBAAN 3 – Wall Following Sederhana (Tanpa PID):
- Tujuan: implementasi Right-Hand Rule dengan threshold biner
- Algoritma: if-else sederhana berdasarkan 3 sensor
- Setup: labirin kotak sederhana (4 dinding)
- Observasi: robot berhasil navigasi? berapa lama?
- Kelemahan yang diamati: gerakan kasar, osilasi

PERCOBAAN 4 – Wall Following dengan PID:
- Tujuan: membuktikan PID lebih baik dari threshold biner
- Kp=3, Ki=0, Kd=0 → amati respons
- Kp=3, Ki=0.05, Kd=0 → amati perbaikan
- Kp=3, Ki=0.05, Kd=1 → amati smoothness
- Data yang dicatat: grafik jarak vs waktu, kecepatan motor
- Perbandingan kuantitatif: standar deviasi error

Format: slide dengan prosedur, tabel data, dan instruksi analisa.
Bahasa Indonesia.
```

---

### PROMPT 31 – SLIDE PERCOBAAN 5-6 (VARIASI ALGORITMA)

```
Buatkan slide deskripsi percobaan 5 dan 6.

PERCOBAAN 5 – Left Wall Following:
- Ubah dari right-hand rule ke left-hand rule
- Observasi perbedaan path di maze yang sama
- Kasus maze solvable dari satu sisi tapi tidak dari sisi lain
- Diskusi: mengapa solusi maze bergantung pada topologi maze

PERCOBAAN 6 – Adaptive Wall Following (Dynamic Setpoint):
- Setpoint berubah sesuai lebar koridor
- Jika koridor sempit (<20cm): setpoint = corridor_width/2
- Jika koridor normal: setpoint = 15cm
- Implementasi: deteksi lebar koridor dari (distLeft + distRight)
- Keuntungan: robot selalu berada di tengah koridor
- Pengujian di koridor berbeda lebar

Format: slide prosedur, kode, dan pertanyaan analisa.
Bahasa Indonesia.
```

---

### PROMPT 32 – SLIDE PERCOBAAN 7-8 (INTEGRASI LINE FOLLOWER)

```
Buatkan slide deskripsi percobaan 7 dan 8.

PERCOBAAN 7 – Mode Switching Wall+Line Follower:
- Setup: lantai dengan garis hitam DAN dinding di sisi kiri
- Robot dimulai mengikuti garis
- Garis berakhir → robot beralih ke wall follower otomatis
- Implementasi state machine
- Observasi: seamless transition atau ada hesitation?
- Tuning waktu debounce untuk mode switching

PERCOBAAN 8 – Hybrid Navigation Lengkap:
- Arena: labirin dengan kombinasi garis (koridor) dan dinding
- Robot harus bisa memanfaatkan keduanya
- Skenario: mulai dari garis → masuk area tanpa garis → wall follow → 
  keluar ke area bergarsis lagi → kembali line follow
- Diskusi: kapan tiap mode aktif (log mode switching)

Format: slide dengan diagram arena, kode state machine, tabel log.
Bahasa Indonesia.
```

---

### PROMPT 33 – SLIDE PERCOBAAN 9-10 (WIFI & ADVANCED)

```
Buatkan slide deskripsi percobaan 9 dan 10.

PERCOBAAN 9 – Konfigurasi Parameter via Smartphone:
- Setup: ESP32 AP mode "WallFollower-ESP32"
- Hubungkan smartphone → buka browser → 192.168.4.1
- Ubah Kp dari 3.0 → 6.0 sambil robot berjalan
- Amati: perubahan perilaku robot secara real-time
- Ubah setpoint dari 15cm → 8cm
- Simpan parameter dan restart: apakah parameter tersimpan?
- Data yang dicatat: tabel perbandingan perilaku sebelum/sesudah

PERCOBAAN 10 – Wall Follower di Lingkungan Dinamis:
- Rintangan bergerak dimasukkan saat robot berjalan
- Orang berjalan di depan robot (obstacle avoidance aktif)
- Dinding bergeser sedikit (±2cm): respons robot
- Multiple robots: 2 robot wall follower di maze yang sama (jika tersedia)
- Tugas: modifikasi kode untuk menangani rintangan lebih robust

Bahasa Indonesia.
```

---

### PROMPT 33B – SLIDE PERCOBAAN 11-13 (MPU-6050)

```
Buatkan slide deskripsi tiga percobaan yang menggunakan sensor IMU MPU-6050.

PERCOBAAN 11 – Kalibrasi dan Pembacaan MPU-6050:
- Tujuan: memahami output raw accelerometer dan gyroscope
- Prosedur: robot diam → amati baseline; robot dimiringkan → amati perubahan
- Data: tabel AccelX/Y/Z dan GyroX/Y/Z pada berbagai posisi
- Pertanyaan: mengapa AccelZ ≈ +1g saat robot datar?
- Visualisasi: Serial Plotter real-time

PERCOBAAN 12 – Gyro-Assisted Straight Movement & 90° Turn:
- Bagian A: Gerak lurus 1 meter tanpa vs dengan koreksi gyro
  → ukur penyimpangan lateral (cm) dan penyimpangan arah (°)
- Bagian B: Belokan 90° dengan timer vs dengan gyro
  → ukur error sudut dengan busur derajat (3× ulangan)
- Tabel perbandingan akurasi: timer-based vs gyro-based

PERCOBAAN 13 – Impact Detection & Tilt Safety:
- Bagian A: Robot menabrak dinding → deteksi spike akselerasi
  → tuning threshold: 1.5g, 2.0g, 2.5g, 3.0g
- Bagian B: Robot diangkat/dimiringkan → motor stop otomatis
  → uji pada kemiringan 15°, 30°, 45°
- Evaluasi: false positive rate dan detection time

Format: slide prosedur, tabel data, kode utama yang relevan.
Bahasa Indonesia.
```

---

### PROMPT 34 – SLIDE ANALISIS DAN DISKUSI PERCOBAAN

```
Buatkan slide panduan analisis dan diskusi untuk setiap percobaan wall follower.
Pertanyaan analisis yang harus dijawab mahasiswa:
1. Bagaimana pengaruh nilai Kp terhadap osilasi dan kecepatan respons?
2. Mengapa sensor ultrasonik menghasilkan nilai anomali di sudut-sudut?
3. Apa hubungan antara frekuensi sampling sensor dan kualitas kontrol?
4. Bandingkan efisiensi energi (waktu baterai) wall following vs line following
5. Mengapa fuzzy logic menghasilkan gerakan lebih halus dibanding PID biner?
6. Bagaimana cara meningkatkan akurasi navigasi tanpa menambah sensor?
7. Apa trade-off antara kecepatan navigasi dan akurasi wall following?

Panduan penulisan laporan:
- Format tabel data yang benar
- Cara menghitung RMSE (Root Mean Square Error) jarak
- Cara membuat grafik dengan Excel atau Python matplotlib

Bahasa Indonesia.
```

---

### PROMPT 35 – SLIDE TABEL VARIASI PARAMETER

```
Buatkan slide berisi tabel variasi parameter yang bisa dicoba mahasiswa.
Tabel variasi:
1. Variasi Kp: [0.5, 1, 2, 3, 5, 8] → efek pada osilasi
2. Variasi setpoint: [8, 10, 12, 15, 20] cm → efek pada clearance
3. Variasi base_speed: [80, 100, 130, 150, 180, 200] → efek pada stabilitas
4. Variasi sensor placement: sudut 0°, 15°, 30° pada sensor samping
5. Variasi sensor filter: no filter, MA-3, MA-5, MA-10
6. Kombinasi wall + line: threshold mode switching 20cm, 25cm, 30cm

Untuk setiap variasi:
- Buat hipotesis sebelum pengujian
- Ukur: RMSE error jarak, max overshoot, settling time
- Buat grafik respons

Bahasa Indonesia, format panduan eksperimen.
```

---

## BAGIAN F: PROJECT & EVALUASI (Slide 39–45)

---

### PROMPT 36 – SLIDE PROJECT DUNIA NYATA (5 OPSI PERTAMA)

```
Buatkan slide yang mempresentasikan 5 opsi project wall follower untuk dunia nyata.
Untuk setiap opsi sertakan:
- Judul dan deskripsi singkat skenario
- Komponen tambahan yang mungkin dibutuhkan
- Tingkat kesulitan (Mudah/Sedang/Sulit)
- Potensi aplikasi industri/sosial

Opsi 1-5 meliputi:
1. Robot inspeksi saluran air (pipa/selokan)
2. Robot penjelajah gedung untuk pemetaan darurat
3. AGV (Automated Guided Vehicle) mini untuk gudang kecil
4. Robot pembersih lantai otomatis di koridor sekolah
5. Robot monitoring kualitas udara di sepanjang dinding pabrik

Format: slide satu opsi per kolom atau carousel format.
Bahasa Indonesia.
```

---

### PROMPT 37 – SLIDE PROJECT DUNIA NYATA (5 OPSI TERAKHIR)

```
Buatkan slide yang mempresentasikan 5 opsi project wall follower berikutnya.
Untuk setiap opsi sertakan:
- Judul dan deskripsi singkat
- Hardware tambahan yang dibutuhkan
- Estimasi biaya tambahan
- Tingkat kesulitan

Opsi 6-10 meliputi:
6. Robot pemandu tuna netra di koridor gedung (dengan speaker TTS)
7. Robot security patrol mengikuti dinding perimeter pabrik
8. Robot edukasi interaktif yang berjalan mengikuti dinding labirin anak
9. Robot pengiriman makanan di restoran mengikuti dinding antara meja
10. Robot pertanian: wall follower mengikuti pagar greenhouse otomatis

Untuk setiap opsi: berikan pseudocode utama dan modifikasi kode yang diperlukan.
Bahasa Indonesia.
```

---

### PROMPT 38 – SLIDE RUBRIK PENILAIAN PRAKTIKUM

```
Buatkan slide rubrik penilaian yang detail untuk praktikum wall follower.
Komponen penilaian:
1. PRETEST (10%): soal pilihan ganda 10 pertanyaan tentang sensor dan algoritma
2. PERCOBAAN (40%):
   - Percobaan 1-4 (dasar): 20%
   - Percobaan 5-8 (lanjutan): 20%
3. LAPORAN (30%):
   - Completeness (data lengkap): 10%
   - Analysis quality (analisa mendalam): 10%
   - Presentation (format, bahasa): 10%
4. PROJECT (20%): perancangan dan demonstrasi

Rubrik detail tiap komponen (tabel: Nilai | Kriteria | Indikator):
- A (90-100): ...kriteria detail...
- B (80-89): ...kriteria detail...
- C (70-79): ...kriteria detail...
- D (<70): ...kriteria detail...

Bahasa Indonesia, format tabel.
```

---

### PROMPT 39 – SLIDE TROUBLESHOOTING GUIDE

```
Buatkan slide panduan troubleshooting komprehensif untuk wall follower robot.
Format tabel: Gejala | Kemungkinan Penyebab | Langkah Diagnosa | Solusi

Masalah yang harus dicakup:
1. Robot tidak bergerak sama sekali
2. Robot bergerak maju terus tidak ada respons sensor
3. Sensor membaca nilai 0 terus menerus
4. Robot osilasi kiri-kanan berlebihan
5. Robot terlalu dekat ke dinding (menabrak)
6. Robot terlalu jauh dari dinding
7. Web interface tidak bisa diakses
8. Parameter tidak tersimpan setelah restart
9. Robot berjalan normal tapi satu motor lebih lambat
10. Sensor ultrasonik saling interfere
11. ESP32 hang/restart secara random (watchdog)
12. Upload firmware gagal

Bahasa Indonesia, format referensi cepat.
```

---

### PROMPT 40 – SLIDE TIPS DAN BEST PRACTICES

```
Buatkan slide berisi tips dan best practices untuk wall follower robot ESP32.

TIPS HARDWARE:
- Cara mengurangi noise sensor dengan kapasitor bypass
- Penempatan sensor yang mengurangi blind spot
- Pemilihan baterai yang tepat (Li-Po vs Li-Ion vs NiMH)
- Grounding yang benar untuk mengurangi interferensi EMI

TIPS SOFTWARE:
- Gunakan FreeRTOS task untuk multi-sensor tanpa blocking
- Implementasi watchdog timer untuk robustness
- Logging data ke SD card untuk analisis offline
- Unit testing komponen: sensor, PID, motor secara terpisah

TIPS TUNING PID:
- Mulai dengan Ki=0, Kd=0, tuning Kp dulu
- Gunakan Serial Plotter Arduino IDE untuk visualisasi
- Uji di lingkungan yang konsisten sebelum uji dinamis

TIPS KEAMANAN:
- Selalu ada tombol stop fisik (kill switch)
- Batas kecepatan saat testing pertama kali
- Hindari testing di dekat tangga atau ujung meja

Bahasa Indonesia, format bullet points.
```

---

### PROMPT 41 – SLIDE PENGEMBANGAN LANJUTAN

```
Buatkan slide tentang arah pengembangan lanjutan dari proyek wall follower ini.
Cakupan:
1. Integrasi dengan Modul 08 (ROS): wall follower sebagai node ROS
2. SLAM (Simultaneous Localization and Mapping):
   - Wall follower + encoders → peta lingkungan sederhana
3. Deep Reinforcement Learning:
   - Robot belajar sendiri strategi wall following
4. Multi-robot coordination:
   - 3 robot wall follower di maze yang sama
5. Computer Vision addition:
   - Kamera untuk deteksi jenis dinding (material, warna)
6. Energy harvesting:
   - Solar panel kecil untuk robot outdoor wall follower
7. Integrasi dengan sistem smart building:
   - Robot laporan status dinding ke cloud IoT

Kaitkan dengan modul-modul berikutnya (08, 09, 10, 11, 12).
Bahasa Indonesia.
```

---

### PROMPT 42 – SLIDE PERBANDINGAN FRAMEWORK ROBOTIKA

```
Buatkan slide perbandingan framework dan platform yang bisa digunakan untuk wall follower robot.
Bandingkan:
1. Bare Metal (PlatformIO/Arduino) → digunakan di modul ini
2. FreeRTOS + ESP-IDF → lebih control, lebih kompleks
3. ROS (Robot Operating System) → digunakan di modul 08-12
4. MicroPython → prototyping cepat, performa lebih lambat
5. Simulasi: Webots/Gazebo → testing tanpa hardware fisik

Tabel perbandingan: Kemudahan | Performa | Komunitas | Cocok untuk | Belajar

Insight: mengapa kita mulai dari PlatformIO/Arduino sebelum ROS?
Analogi: seperti belajar mengendarai sepeda sebelum mobil.

Bahasa Indonesia.
```

---

### PROMPT 43 – SLIDE KUIS DAN PERTANYAAN REFLEKSI

```
Buatkan slide berisi kuis dan pertanyaan refleksi untuk mengukur pemahaman mahasiswa.

KUIS PILIHAN GANDA (5 soal):
1. Apa yang dimaksud dengan Left-Hand Rule? [4 pilihan]
2. Rumus jarak HC-SR04? [4 pilihan dengan nilai numerik]
3. Komponen PID mana yang eliminasi steady-state error? [4 pilihan]
4. Dalam ESP32 AP mode, IP default adalah? [4 pilihan]
5. Apa fungsi anti-windup dalam PID? [4 pilihan]

PERTANYAAN ESAI SINGKAT (3 soal):
1. Jelaskan perbedaan wall follower dan line follower dari segi sensor dan algoritma.
2. Mengapa PID lebih baik dari threshold biner untuk wall following?
3. Bagaimana cara setting parameter PID tanpa harus upload ulang firmware?

PERTANYAAN REFLEKSI:
- Apa yang paling menantang dari percobaan ini?
- Modifikasi apa yang ingin Anda lakukan pada robot ini?

Bahasa Indonesia, format slide interaktif.
```

---

### PROMPT 44 – SLIDE RINGKASAN DAN KESIMPULAN

```
Buatkan slide ringkasan komprehensif Modul 07 Wall Follower.
Konten:
1. Recap konsep kunci yang telah dipelajari (poin-poin utama):
   - Sensor HC-SR04 dan cara kerjanya
   - Algoritma wall following (right/left hand rule)
   - PID controller untuk smooth navigation
   - Navigasi hybrid wall + line follower
   - Setting parameter via WiFi hotspot
2. Hubungan antar konsep (mini concept map)
3. Kompetensi yang telah dicapai (vs CPMK di awal)
4. Lesson learned dari 10 percobaan
5. Koneksi ke modul berikutnya (Modul 08: ROS)
6. Quote motivasi tentang robotika

Bahasa Indonesia, format slide penutup yang berkesan.
```

---

### PROMPT 45 – SLIDE PENUTUP DAN REFERENSI

```
Buatkan slide penutup dan daftar referensi untuk presentasi Modul 07.
Konten slide penutup:
1. Ucapan terima kasih
2. QR Code placeholder untuk repository GitHub proyek
3. Link ke materi online tambahan (PlatformIO docs, ESP32 docs)
4. Kontak/email dosen untuk pertanyaan

Daftar referensi terpilih (10 terpenting dari 60 total referensi di materi):
Format: Author (Tahun). Judul. Publikasi.
Pilih yang paling relevan untuk mahasiswa pemula yang ingin mendalami.

Informasi praktis untuk mahasiswa:
- Deadline laporan
- Format pengumpulan (PDF + video)
- Platform pengumpulan (LMS/Google Drive)

Bahasa Indonesia, format slide formal akademis.
```
