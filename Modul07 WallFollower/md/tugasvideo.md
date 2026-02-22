# TUGAS VIDEO MODUL 07: WALL FOLLOWER ROBOT DENGAN ESP32 DAN MPU-6050

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 07 – Wall Follower  
**Batas Upload:** Sesuai jadwal dosen  
**Durasi Video:** 15–25 menit  
**Format:** MP4, resolusi minimal HD 720p (1080p disarankan)  
**Platform Upload:** Google Drive / YouTube (unlisted) / LMS  

---

## A. KETENTUAN UMUM

> ⚠️ **TUGAS VIDEO DIKERJAKAN SECARA INDIVIDUAL (PER ORANG)**

1. Setiap mahasiswa wajib membuat **video sendiri-sendiri** (bukan per kelompok)
2. Video menampilkan **screen recording** layar komputer (saat menjelaskan kode/teori) DAN **rekaman langsung robot** saat percobaan berlangsung
3. Tampilkan **nama lengkap dan NIM** di awal video (bisa lewat teks overlay atau ucapkan langsung)
4. Penjelasan dalam **Bahasa Indonesia** yang baik dan benar
5. Kualitas audio harus jelas, hindari noise/suara berisik di latar belakang
6. **Wajib rekam kamera fisik robot** saat percobaan dan project, bukan hanya screen recording Serial Monitor
7. Setiap percobaan yang didemonstrasikan harus menampilkan **sensor aktif dan gerakan robot secara jelas**
8. **Tidak diperbolehkan** mengedit video untuk menyembunyikan kegagalan – tampilkan proses nyata termasuk debugging

---

## B. STRUKTUR VIDEO

Video dibagi menjadi **4 bagian utama** sesuai urutan di bawah.

---

## BAGIAN 1: PENJELASAN MATERI (Maks. 7 menit)

> Lakukan screen recording layar, tampilkan slide/materi atau kode sambil menjelaskan

---

### CHECKLIST 1.1 – Konsep Wall Follower dan Perbandingan Sensor

- [ ] **1.1.1** Jelaskan definisi wall follower robot dan bedanya dengan line follower robot (contoh nyata)
- [ ] **1.1.2** Sebutkan minimal 3 aplikasi nyata wall follower di industri yang relevan dengan Teknologi Rekayasa Otomasi
- [ ] **1.1.3** Jelaskan prinsip kerja sensor ultrasonik HC-SR04 (Time of Flight, rumus jarak, timing TRIG-ECHO)
- [ ] **1.1.4** Demonstrasikan pembacaan HC-SR04 di Serial Monitor/Plotter – tampilkan nilai saat objek didekatkan dan dijauhkan
- [ ] **1.1.5** Jelaskan mengapa pin ECHO HC-SR04 membutuhkan voltage divider untuk ESP32 (5V vs 3.3V)
- [ ] **1.1.6** Jelaskan perbedaan sensor ultrasonik vs sensor IR untuk deteksi dinding (kapan masing-masing lebih baik)

---

### CHECKLIST 1.2 – Sensor IMU MPU-6050

- [ ] **1.2.1** Jelaskan apa itu IMU dan perbedaan accelerometer vs gyroscope dengan analogi yang mudah dipahami
- [ ] **1.2.2** Tunjukkan koneksi MPU-6050 ke ESP32 via I2C (SDA=21, SCL=22) dan konfirmasi alamat 0x68 terdeteksi
- [ ] **1.2.3** Demonstrasikan pembacaan raw data MPU-6050 (AccelX/Y/Z, GyroX/Y/Z) di Serial Plotter saat robot dimiringkan
- [ ] **1.2.4** Jelaskan mengapa gyroscope mengalami **drift** dan bagaimana complementary filter mengatasinya
- [ ] **1.2.5** Jelaskan minimal **2 manfaat konkret** MPU-6050 pada robot wall follower yang Anda implementasikan
- [ ] **1.2.6** Tunjukkan proses **kalibrasi offset** MPU-6050 – jelaskan mengapa offset diperlukan

---

### CHECKLIST 1.3 – Algoritma Wall Following dan PID

- [ ] **1.3.1** Jelaskan Right-Hand Rule dan Left-Hand Rule dengan menggambar diagram di kertas atau whiteboard digital
- [ ] **1.3.2** Tunjukkan flowchart/pseudocode state machine (STOP / LINE_FOLLOW / WALL_FOLLOW_L / WALL_FOLLOW_R / EXPLORE)
- [ ] **1.3.3** Jelaskan konsep PID controller dengan analogi intuitif (misalnya: pengemudi menjaga jarak ke bahu jalan)
- [ ] **1.3.4** Tunjukkan kelas `PIDController` di kode Anda dan jelaskan fungsi setiap bagian (P, I, D, anti-windup)
- [ ] **1.3.5** Jelaskan mengapa Kd penting untuk mengurangi overshoot – tunjukkan contoh numerik
- [ ] **1.3.6** Tunjukkan kode `complementaryFilter()` atau penggunaan DMP MPU-6050 dalam kode Anda

---

### CHECKLIST 1.4 – ESP32, PlatformIO, dan Web Interface

- [ ] **1.4.1** Jelaskan keunggulan dual-core ESP32: core 0 untuk sensor, core 1 untuk motor + web server
- [ ] **1.4.2** Tampilkan file `platformio.ini` dan jelaskan konfigurasi (platform, library MPU6050, ESPAsyncWebServer)
- [ ] **1.4.3** Jelaskan cara kerja ESP32 sebagai WiFi Access Point dan demonstrasikan koneksi smartphone ke "WallFollower-ESP32"
- [ ] **1.4.4** Tunjukkan web interface di browser smartphone: slider parameter, grafik sensor, tombol kontrol
- [ ] **1.4.5** Demonstrasikan perubahan parameter Kp secara real-time via web sambil robot bergerak

---

## BAGIAN 2: PERCOBAAN SENSOR DAN DASAR (Maks. 6 menit)

> Wajib tampilkan rekaman robot fisik + Serial Monitor secara bersamaan (split screen dianjurkan)

---

### CHECKLIST 2.1 – Percobaan 1-2: Kalibrasi Sensor HC-SR04

- [ ] **2.1.1** Tampilkan setup fisik: sensor HC-SR04 + voltage divider terpasang di breadboard
- [ ] **2.1.2** Rekam proses pengukuran pada minimal 4 jarak referensi berbeda (penggaris sebagai referensi)
- [ ] **2.1.3** Bacakan dan jelaskan data tabel kalibrasi: error absolut dan error relatif
- [ ] **2.1.4** Jawab pertanyaan: pada jarak berapa sensor paling akurat? Mengapa?

---

### CHECKLIST 2.2 – Percobaan 11-13: MPU-6050

- [ ] **2.2.1** Rekam **kalibrasi MPU-6050**: robot diam, tampilkan Serial Monitor nilai offset sebelum dan sesudah kalibrasi
- [ ] **2.2.2** Rekam pembacaan sensor saat robot dimiringkan 4 arah: tampilkan nilai AccelX/Y/Z berubah di Serial Plotter
- [ ] **2.2.3** Demonstrasikan **gyro-assisted straight movement**: robot maju 1 meter tanpa gyro vs dengan gyro – ukur penyimpangan secara fisik (penggaris/meteran)
- [ ] **2.2.4** Demonstrasikan **gyro-assisted 90° turn**: tampilkan angka yaw di Serial Monitor saat robot berputar, bandingkan akurasi dengan busur derajat
- [ ] **2.2.5** Demonstrasikan **impact detection**: robot bergerak → sengaja tabrakkan ke dinding dengan kecepatan rendah → tampilkan alert di Serial Monitor dan LED/buzzer aktif
- [ ] **2.2.6** Demonstrasikan **tilt safety**: angkat salah satu sisi robot > 30° → motor berhenti otomatis

---

### CHECKLIST 2.3 – Percobaan 3-4: Wall Following Dasar vs PID

- [ ] **2.3.1** Rekam robot berjalan di maze/koridor dengan **threshold sederhana** (tanpa PID) – tampilkan gerakan kasar
- [ ] **2.3.2** Rekam robot berjalan dengan **PID aktif** di maze yang sama – tampilkan perbedaan kehalusan gerakan
- [ ] **2.3.3** Tunjukkan Serial Plotter grafik jarak sensor kiri vs waktu: bandingkan threshold vs PID
- [ ] **2.3.4** Jelaskan secara lisan: mengapa PID lebih smooth? Hubungkan dengan teori yang sudah dijelaskan di Bagian 1

---

## BAGIAN 3: PERCOBAAN LANJUTAN DAN INTEGRASI (Maks. 5 menit)

---

### CHECKLIST 3.1 – Percobaan 5-8: Variasi Algoritma dan Hybrid Navigation

- [ ] **3.1.1** Rekam robot menggunakan **Right-Hand Rule** di maze sederhana
- [ ] **3.1.2** Rekam robot menggunakan **Left-Hand Rule** di maze yang sama – tampilkan perbedaan jalur
- [ ] **3.1.3** Rekam **mode switching otomatis**: robot mengikuti garis → garis berakhir → beralih ke wall follower → tampilkan log mode di Serial Monitor
- [ ] **3.1.4** Jelaskan kondisi trigger yang menyebabkan mode switching terjadi di kode Anda

---

### CHECKLIST 3.2 – Percobaan 9-10: WiFi Config dan Lingkungan Dinamis

- [ ] **3.2.1** Rekam **layar smartphone** saat mengakses `192.168.4.1` – tampilkan web interface
- [ ] **3.2.2** Rekam perubahan parameter Kp secara langsung sambil robot bergerak – tampilkan perubahan perilaku robot
- [ ] **3.2.3** Rekam robot menghindari **rintangan dinamis** (tangan/kotak yang dimasukkan ke jalur robot)
- [ ] **3.2.4** Rekam restart ESP32 dan konfirmasi parameter tersimpan di Preferences (nilai sama dengan sebelum restart)

---

### CHECKLIST 3.3 – Pengujian Komprehensif MPU-6050 dalam Wall Follower

- [ ] **3.3.1** Rekam robot berjalan di koridor dan demonstrasikan **heading correction**: tampilkan nilai yaw di Serial Monitor saat robot bergerak lurus
- [ ] **3.3.2** Rekam robot melewati **belokan sudut 90°** menggunakan gyro-assisted turn – tampilkan akurasi belokan secara fisik
- [ ] **3.3.3** Rekam **combined scenario**: wall follower + gyro heading correction + impact detection semuanya aktif dalam satu run

---

## BAGIAN 4: PROJECT (Maks. 5 menit)

> Tampilkan implementasi project yang dipilih kelompok (presentasikan secara individual)

---

### CHECKLIST 4.1 – Penjelasan Project

- [ ] **4.1.1** Sebutkan opsi project yang dipilih dan jelaskan konteks masalah nyata yang diselesaikan
- [ ] **4.1.2** Jelaskan **arsitektur sistem** project: sensor yang digunakan, algoritma tambahan, fitur inovatif
- [ ] **4.1.3** Tunjukkan **flowchart atau pseudocode utama** yang membedakan project ini dari percobaan dasar
- [ ] **4.1.4** Jelaskan peran **MPU-6050** dalam project yang dipilih (contoh: dead reckoning, impact detection, orientasi)

---

### CHECKLIST 4.2 – Demonstrasi Project

- [ ] **4.2.1** Rekam **demonstrasi live project** secara fisik (robot bergerak sesuai skenario project)
- [ ] **4.2.2** Tampilkan **web interface project** yang sudah dikembangkan (dashboard, log, kontrol)
- [ ] **4.2.3** Tampilkan setidaknya **1 fitur inovatif** yang tidak ada di percobaan standar
- [ ] **4.2.4** Jika ada kegagalan, jelaskan: apa penyebabnya? bagaimana solusinya?

---

### CHECKLIST 4.3 – Analisis dan Refleksi Project

- [ ] **4.3.1** Sebutkan **3 tantangan teknis** terbesar yang dihadapi saat mengerjakan project dan bagaimana mengatasinya
- [ ] **4.3.2** Bandingkan performa project dengan percobaan dasar: apa yang lebih baik? apa trade-off-nya?
- [ ] **4.3.3** Usulkan **1 pengembangan lanjutan** yang realistis jika proyek ini dilanjutkan ke semester depan

---

## C. RUBRIK PENILAIAN VIDEO

### C.1 Penilaian Konten (70%)

| Bagian | Poin Maks | Kriteria |
|--------|----------|---------|
| **Bagian 1: Materi** | 25 | Penjelasan akurat, runtut, menggunakan bahasa teknis yang tepat, semua checklist 1.x terpenuhi |
| **Bagian 2: Percobaan Sensor** | 20 | Data percobaan nyata (bukan simulasi), semua checklist 2.x terpenuhi |
| **Bagian 3: Percobaan Lanjutan** | 15 | Demonstrasi berhasil, analisis bermakna, checklist 3.x terpenuhi |
| **Bagian 4: Project** | 20 | Inovasi terlihat, demonstrasi live, refleksi mendalam |

### C.2 Penilaian Presentasi (30%)

| Aspek | Poin Maks | Kriteria |
|-------|----------|---------|
| **Kualitas rekaman** | 10 | Gambar jelas (min. 720p), audio terdengar bersih, pencahayaan cukup |
| **Penguasaan materi** | 10 | Menjelaskan dengan yakin tanpa terlalu banyak membaca, mampu improvisasi |
| **Struktur dan alur** | 5 | Video mengalir logis, ada transisi antar bagian, tidak berulang |
| **Kelengkapan** | 5 | Durasi sesuai, semua bagian ada, nama/NIM tercantum |

### C.3 Skala Nilai

| Nilai | Range | Deskripsi |
|-------|-------|-----------|
| **A** | 90–100 | Semua checklist terpenuhi, penjelasan sangat jelas dan mendalam, inovasi project menonjol, kualitas rekaman sangat baik |
| **B** | 80–89 | Sebagian besar checklist terpenuhi (min. 80%), penjelasan jelas, project berjalan dengan baik |
| **C** | 70–79 | Minimal 60% checklist terpenuhi, penjelasan memadai, project berjalan meski ada kekurangan |
| **D** | 60–69 | Kurang dari 60% checklist, banyak bagian tidak didemonstrasikan, kualitas rekaman buruk |
| **E** | < 60 | Video tidak diunggah, atau konten tidak relevan, atau robot tidak berfungsi sama sekali |

---

## D. PANDUAN TEKNIS PEMBUATAN VIDEO

### D.1 Alat yang Direkomendasikan

| Alat | Rekomendasi | Alternatif |
|------|------------|-----------|
| Screen recording | OBS Studio (gratis) | Camtasia, Bandicam |
| Rekaman robot | Smartphone (kamera belakang) | Kamera webcam eksternal |
| Editing (opsional) | DaVinci Resolve (gratis) | CapCut, Filmora |
| Mikrofon | Earphone dengan mikrofon | Mikrofon laptop bawaan |

### D.2 Tips Setup Rekaman Robot

1. **Pencahayaan:** Pastikan robot terlihat jelas. Gunakan lampu meja atau rekam di dekat jendela.
2. **Sudut kamera:** Rekam dari atas (bird's eye view) untuk melihat jalur robot, atau dari samping untuk melihat sensor.
3. **Split screen:** Gunakan OBS atau edit video untuk menampilkan Serial Monitor dan robot secara bersamaan.
4. **Jarak kamera:** Cukup dekat agar sensor HC-SR04 dan LED indikator terlihat, tapi cukup jauh agar seluruh arena terlihat.

### D.3 Tips Setup Screen Recording

1. Buka **Serial Plotter** (bukan hanya Serial Monitor) untuk menampilkan grafik data sensor secara visual
2. Tampilkan **file `main.cpp`** saat menjelaskan kode – zoom in ke bagian yang relevan
3. Saat menjelaskan web interface, rekam layar **smartphone** (gunakan screen mirror seperti Vysor atau rekam langsung dari HP)

### D.4 Struktur Folder Pengumpulan

```
Kelompok[X]_[NamaKetua]/
├── Video_Individual_[NIM1]_[Nama1].mp4
├── Video_Individual_[NIM2]_[Nama2].mp4
├── Video_Individual_[NIM3]_[Nama3].mp4
├── Video_Individual_[NIM4]_[Nama4].mp4
└── Laporan_Project_Kelompok[X].pdf
```

---

## E. CHECKLIST MANDIRI SEBELUM UPLOAD

Isi checklist ini sebelum mengupload video. Jika ada item yang belum terpenuhi, perbaiki videonya terlebih dahulu.

### Konten

- [ ] Nama lengkap dan NIM tercantum jelas di awal video
- [ ] Semua sensor (HC-SR04, MPU-6050, IR) didemonstrasikan secara fisik
- [ ] Percobaan 11 (kalibrasi MPU), 12 (gyro turn), dan 13 (impact/tilt) direkam
- [ ] Mode switching wall follower ↔ line follower didemonstrasikan
- [ ] WiFi hotspot config didemonstrasikan dari smartphone
- [ ] Demonstrasi project dilakukan secara live (bukan rekaman yang diedit/dipercepat)
- [ ] Refleksi dan analisis disampaikan secara lisan

### Teknis

- [ ] Resolusi minimal 720p (cek di properties file video)
- [ ] Durasi 15–25 menit (tidak lebih pendek dari 15 menit)
- [ ] Suara jelas dan dapat didengar tanpa noise berlebihan
- [ ] Format file MP4 (bukan AVI/MOV)
- [ ] Ukuran file wajar (gunakan kompresi jika > 2 GB)

---

## F. PERTANYAAN TEKNIS YANG MUNGKIN DITANYAKAN DOSEN

Siapkan jawaban untuk pertanyaan-pertanyaan berikut saat presentasi/tanya jawab:

1. Mengapa complementary filter lebih baik dari integrasi gyro saja untuk mendapatkan sudut?
2. Apa yang terjadi pada robot jika MPU-6050 tidak dikalibrasi sebelum digunakan?
3. Bagaimana cara memilih nilai Kp yang optimal tanpa melakukan trial-error berulang kali?
4. Jelaskan perbedaan angular drift pada gyroscope dan bagaimana efeknya pada navigasi jangka panjang?
5. Mengapa right-hand rule tidak selalu dapat menyelesaikan semua jenis maze?
6. Bagaimana cara robot mengetahui apakah ia harus menggunakan mode wall follower atau line follower?
7. Apa kelemahan dead reckoning menggunakan gyro MPU-6050 untuk pemetaan ruangan?
8. Mengapa digunakan `Preferences` library untuk menyimpan parameter, bukan `EEPROM.write()`?
9. Apa trade-off antara kecepatan sampling sensor (50ms vs 100ms) dan kualitas kontrol PID?
10. Bagaimana cara menguji sistem wall follower secara unit testing sebelum integrasi penuh?
