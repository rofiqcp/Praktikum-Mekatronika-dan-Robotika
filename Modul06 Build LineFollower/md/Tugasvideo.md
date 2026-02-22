# TUGAS VIDEO MODUL 06: BUILD LINE FOLLOWER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 06 – Build Line Follower  
**Platform:** ESP32 + PlatformIO + MPU-6050  
**Batas Upload:** Sesuai jadwal dosen  
**Durasi Video:** 15–25 menit  
**Format:** MP4, resolusi minimal HD 720p  
**Platform Upload:** Google Drive / YouTube (unlisted) / LMS  

---

## A. KETENTUAN UMUM

> ⚠️ **TUGAS VIDEO DIKERJAKAN SECARA INDIVIDUAL (PER ORANG)**

1. Setiap mahasiswa wajib membuat **video sendiri-sendiri** (bukan per kelompok)
2. Video berisi **screen recording** proses pemrograman PlatformIO DAN **rekaman kamera** proses soldering, assembly, dan robot berlari
3. Tampilkan **nama lengkap dan NIM** di awal video (on-screen text atau ditulis di kertas yang terlihat jelas)
4. Gunakan **Bahasa Indonesia** yang baik dan benar
5. Setiap poin harus didukung dengan **demonstrasi nyata** (bukan slideshow)
6. Penjelasan harus **orisinal** — jangan hanya membaca teks dari layar
7. Rekaman robot yang berlari di lintasan harus menggunakan robot **kelompok Anda sendiri**

---

## B. POIN-POIN YANG HARUS DIJELASKAN DAN DIDEMONSTRASIKAN

---

### BAGIAN 1: PENJELASAN MATERI TEORI (Maks. 4 menit)

**Yang harus dijelaskan tanpa perlu menunjukkan robot (boleh dengan papan tulis, kertas, atau layar):**

- [ ] **1.1** Prinsip kerja sensor infrared pada robot line follower: mengapa permukaan hitam menyerap IR dan putih memantulkan — berikan penjelasan fisika singkat
- [ ] **1.2** Weighted position calculation: jelaskan dengan contoh kalkulasi manual (ambil 3 sensor aktif, hitung posisi)
- [ ] **1.3** Perbedaan algoritma P, PD, dan PID: kapan masing-masing digunakan, apa kelemahan tiap algoritma — gunakan analogi yang mudah dipahami
- [ ] **1.4** Prinsip kerja MPU-6050: apa itu IMU 6-DoF, bagaimana accelerometer mengukur sudut, bagaimana gyroscope mengukur laju rotasi
- [ ] **1.5** Complementary Filter: mengapa dibutuhkan, rumus, makna nilai alpha — jelaskan dengan kata-kata sendiri
- [ ] **1.6** Bagaimana MPU-6050 membantu line follower: sebutkan minimal 3 aplikasi (yaw correction, ramp detection, anti-terbalik) dan jelaskan cara kerjanya secara konseptual

*Panduan: Durasi ideal per poin ~30–40 detik. Total Bagian 1 tidak boleh lebih dari 4 menit.*

---

### BAGIAN 2: PROSES SOLDERING PCB (Maks. 3 menit)

**Yang harus direkam dengan kamera (bukan screen recording):**

- [ ] **2.1** Tampilkan kondisi PCB sebelum disolder (PCB kosong + komponen belum terpasang)
- [ ] **2.2** Demonstrasikan teknik menyolder yang benar: panaskan pad+kaki → sentuh solder ke joint → hasil mengkilap
- [ ] **2.3** Tunjukkan proses menyolder komponen yang paling menantang (IC 74HC165 atau LED IR + photodiode)
- [ ] **2.4** Demonstrasikan cara mengecek solder bridge pada IC menggunakan multimeter (mode continuity/diode)
- [ ] **2.5** Tampilkan hasil PCB Sensor Line yang sudah selesai disolder dari berbagai sudut
- [ ] **2.6** Tampilkan hasil PCB MAIN yang sudah selesai disolder dari berbagai sudut
- [ ] **2.7** Berikan **1 tips soldering** dari pengalaman Anda sendiri selama praktikum ini

*Catatan: Rekam proses nyata, bukan hanya hasil akhir. Kesalahan yang diakui dan diperbaiki justru menunjukkan pemahaman.*

---

### BAGIAN 3: PROSES ASSEMBLY MEKANIK (Maks. 2 menit)

**Yang harus direkam dengan kamera:**

- [ ] **3.1** Tampilkan semua komponen mekanik sebelum dirakit (motor, roda, chassis, standoff)
- [ ] **3.2** Demonstrasikan pemasangan motor ke bracket dan roda ke shaft
- [ ] **3.3** Tunjukkan cara mengukur dan mengatur jarak sensor board ke permukaan (target 8–10mm) — gunakan penggaris yang terlihat kamera
- [ ] **3.4** Tunjukkan posisi pemasangan MPU-6050 di chassis (dan bagaimana orientasinya berpengaruh pada pembacaan pitch/roll)
- [ ] **3.5** Tampilkan robot yang sudah selesai dirakit dan jelaskan tata letak komponen: PCB MAIN, Sensor Line, MPU-6050, baterai, posisi center of gravity

---

### BAGIAN 4: SETUP PLATFORMIO DAN KONFIGURASI (Maks. 2 menit)

**Yang harus ditunjukkan (screen recording):**

- [ ] **4.1** Tampilkan struktur project PlatformIO: folder `src/`, `include/`, `platformio.ini`
- [ ] **4.2** Tampilkan isi `platformio.ini` — jelaskan setiap baris: platform, board, framework, lib_deps (SSD1306, MPU6050)
- [ ] **4.3** Tampilkan isi `config.h` — jelaskan semua define: pin SPI sensor, pin motor, pin I2C OLED + MPU-6050 (shared bus), MPU address 0x68
- [ ] **4.4** Demonstrasikan cara upload program ke ESP32 (klik upload, tampilkan progress bar)
- [ ] **4.5** Tampilkan Serial Monitor yang menunjukkan inisialisasi berhasil: "MPU6050 OK", "12 sensors ready"

---

### BAGIAN 5: PERCOBAAN 1 – TEST SENSOR DAN BINARY LINE FOLLOWER (Maks. 2 menit)

**Yang harus ditunjukkan:**

- [ ] **5.1** Screen recording Serial Monitor saat program test sensor berjalan — tunjukkan bit pattern berubah saat tangan menutup sensor
- [ ] **5.2** Tunjukkan **semua 12 sensor merespons** (tutup satu per satu dengan jari, amati perubahan di Serial Monitor)
- [ ] **5.3** Rekam robot berlari dengan algoritma binary di lintasan oval — tampak osilasi jelas
- [ ] **5.4** Jelaskan secara lisan: mengapa robot berosilasi pada algoritma binary? Apa hubungannya dengan sifat on-off dari algoritma?

---

### BAGIAN 6: PERCOBAAN 2 – P CONTROLLER DAN TUNING Kp (Maks. 2 menit)

**Yang harus ditunjukkan:**

- [ ] **6.1** Screen recording kode P controller (tunjukkan bagian weighted position dan rumus P)
- [ ] **6.2** Rekam robot berlari dengan **setidaknya 3 nilai Kp berbeda** (Kp kecil → lambat berkoreks, Kp besar → osilasi, Kp optimal → mulus) — beri label di video atau narasi
- [ ] **6.3** Tampilkan tabel hasil tuning Kp (foto atau screenshot) — nilai Kp, waktu lintasan, evaluasi
- [ ] **6.4** Jelaskan: bagaimana Anda menentukan Kp optimal? Apa parameter yang Anda perhatikan?

---

### BAGIAN 7: PERCOBAAN 3 – PD CONTROLLER (Maks. 2 menit)

**Yang harus ditunjukkan:**

- [ ] **7.1** Screen recording kode — tunjukkan tambahan komponen Kd dibanding P
- [ ] **7.2** Rekam perbandingan **P vs PD** pada belokan yang sama — tunjukkan perbedaan osilasi
- [ ] **7.3** Rekam robot dengan PD controller terbaik menyelesaikan lintasan dengan lancar
- [ ] **7.4** Dari Serial Monitor saat robot berlari, tunjukkan nilai error dan PID output — jelaskan bagaimana data tersebut dapat diinterpretasikan

---

### BAGIAN 8: PERCOBAAN MPU-6050 (Maks. 4 menit)

**Bagian terpenting — demonstrasikan semua yang berikut:**

- [ ] **8.1** Screen recording: inisialisasi MPU-6050, tampilkan "MPU6050 connection OK" di Serial Monitor
- [ ] **8.2** Demonstrasikan **pembacaan data real-time** di Serial Monitor: ax, ay, az, gx, gy, gz
- [ ] **8.3** Tunjukkan **pitch dan roll berubah** saat robot dimiringkan ke berbagai arah (rekam kamera + Serial Monitor secara bersamaan atau bergantian)
- [ ] **8.4** Screen recording: tampilkan **Serial Plotter** dengan 3 baris (accel angle, complementary filter, gyro only) — jelaskan perbedaan ketiga kurva
- [ ] **8.5** Demonstrasikan **gyro drift**: biarkan robot diam 60 detik dengan hanya integrasi gyro → tampilkan berapa derajat error yang terakumulasi
- [ ] **8.6** Demonstrasikan **Complementary Filter bekerja**: plot menunjukkan kurva stabil meski robot digetarkan
- [ ] **8.7** Demonstrasikan **yaw correction aktif**: jalankan robot di garis lurus panjang, tunjukkan robot lebih tepat di tengah garis dibanding tanpa koreksi (rekam dari atas atau dari depan)
- [ ] **8.8** Jika percobaan ramp dilakukan: rekam robot naik/turun ramp, tunjukkan `pitchDeg` berubah di Serial Monitor dan robot menyesuaikan kecepatan
- [ ] **8.9** Jelaskan secara lisan: apa perbedaan nyata yang Anda rasakan (atau ukur) ketika MPU-6050 aktif vs tidak aktif dalam kontrol robot?

---

### BAGIAN 9: HASIL AKHIR DAN PROJECT (Maks. 2 menit)

**Yang harus ditunjukkan:**

- [ ] **9.1** Rekam robot menyelesaikan **lintasan lengkap** (minimal 2 putaran) dengan PD + MPU optimal — ini adalah penampilan terbaik robot Anda
- [ ] **9.2** Tampilkan OLED dashboard saat robot berlari (posisi, error, kecepatan, dan setidaknya satu data IMU)
- [ ] **9.3** Jelaskan singkat **project kelompok** yang dikerjakan: opsi project mana yang dipilih, apa inovasinya, hasil awal yang sudah dicapai
- [ ] **9.4** Demonstrasikan minimal satu fitur dari project kelompok yang melibatkan MPU-6050

---

### BAGIAN 10: ANALISIS DAN KESIMPULAN (Maks. 1 menit)

**Yang harus disampaikan (narasi + tampilkan data jika ada):**

- [ ] **10.1** Sebutkan **3 hal yang paling Anda pelajari** dari Modul 06 ini
- [ ] **10.2** Sebutkan **1 kesulitan terbesar** yang Anda hadapi dan bagaimana mengatasinya
- [ ] **10.3** Berikan pendapat Anda: apakah MPU-6050 memberikan peningkatan nyata pada performa robot? Jelaskan dengan data atau observasi konkret
- [ ] **10.4** Sebutkan **1 pengembangan** yang ingin Anda lakukan jika ada waktu lebih

---

## C. RUBRIK PENILAIAN VIDEO

**Total Nilai: 100 poin**

---

### C.1 Kelengkapan Konten (40 poin)

| No | Bagian | Bobot | Skor (0–10) | Nilai |
|----|--------|-------|------------|-------|
| 1 | Bag. 1 – Teori (sensor IR, weighted pos., PID, MPU-6050, complementary filter) | 6 | | |
| 2 | Bag. 2 – Proses soldering (teknik, tips, hasil) | 4 | | |
| 3 | Bag. 3 – Assembly mekanik (ukur jarak sensor, orientasi MPU, CG) | 3 | | |
| 4 | Bag. 4 – Setup PlatformIO (platformio.ini, config.h, upload) | 3 | | |
| 5 | Bag. 5 – Test sensor + binary (12 sensor responsif, osilasi terlihat) | 3 | | |
| 6 | Bag. 6 – P controller tuning (3 nilai Kp, tabel, analisis) | 4 | | |
| 7 | Bag. 7 – PD controller (perbandingan P vs PD, run terbaik) | 3 | | |
| 8 | Bag. 8 – MPU-6050 (inisialisasi, data raw, complementary filter, yaw correction) | 8 | | |
| 9 | Bag. 9 – Hasil akhir + preview project | 3 | | |
| 10 | Bag. 10 – Analisis + kesimpulan | 3 | | |
| **TOTAL** | | **40** | | |

*Skor per bagian: 10=sempurna; 7–9=baik; 4–6=cukup; 1–3=kurang; 0=tidak ada*

---

### C.2 Akurasi Teknis (30 poin)

| No | Kriteria | Bobot | Skor (0–10) | Nilai |
|----|---------|-------|------------|-------|
| 1 | Penjelasan teori (IR, weighted, PID, IMU, CF) **benar secara teknis** | 8 | | |
| 2 | Robot berlari **stabil di lintasan** (tidak keluar garis >3× dalam 2 putaran) | 8 | | |
| 3 | MPU-6050 **diintegrasikan bermakna** ke dalam kontrol (bukan hanya dibaca, tapi mempengaruhi motor) | 8 | | |
| 4 | Data yang ditampilkan **konsisten dan masuk akal** (nilai sensor, PID, IMU wajar) | 6 | | |
| **TOTAL** | | **30** | | |

---

### C.3 Kualitas Presentasi (20 poin)

| No | Kriteria | Bobot | Skor (0–5) | Nilai |
|----|---------|-------|-----------|-------|
| 1 | Narasi jelas, tidak terlalu cepat/lambat, mudah dipahami | 5 | | |
| 2 | Kualitas rekaman layar: resolusi HD, teks terbaca, tidak buram | 5 | | |
| 3 | Kualitas rekaman kamera: stabil, cukup terang, robot/PCB terlihat jelas | 5 | | |
| 4 | Struktur video: pembukaan → materi → demo → kesimpulan, alur logis | 5 | | |
| **TOTAL** | | **20** | | |

---

### C.4 Demonstrasi Fitur Wajib (10 poin)

| No | Fitur yang Wajib Didemonstrasikan | Skor (0 atau 1) |
|----|----------------------------------|----------------|
| 1 | 12 sensor merespons (tutup satu per satu terlihat di Serial) | |
| 2 | Binary → terlihat osilasi di rekaman | |
| 3 | P vs PD perbandingan terlihat jelas di rekaman | |
| 4 | MPU-6050 init OK di Serial Monitor | |
| 5 | Serial Plotter complementary filter (3 kurva) | |
| 6 | Pitch/roll berubah saat robot dimiringkan (direkam) | |
| 7 | Gyro drift terbukti (nilai drift dicatat atau diplot) | |
| 8 | Yaw correction mempengaruhi motor (didemonstrasikan) | |
| 9 | OLED menampilkan data IMU saat robot berlari | |
| 10 | Robot menyelesaikan 2 putaran penuh dengan PD+IMU | |
| **TOTAL** | | **/10** |

---

### C.5 Rangkuman Nilai

| Komponen | Bobot | Nilai Didapat |
|---------|-------|--------------|
| Kelengkapan Konten | 40 | |
| Akurasi Teknis | 30 | |
| Kualitas Presentasi | 20 | |
| Demonstrasi Fitur Wajib | 10 | |
| **TOTAL** | **100** | |

**Penilai:** ___________________  
**Tanggal:** ___________________  
**Catatan:**
```
_______________________________________________
```

---

## D. PANDUAN TEKNIS PEMBUATAN VIDEO

### D.1 Tools Screen Recording

| Tool | Platform | Link | Keterangan |
|------|---------|------|-----------|
| **OBS Studio** | Win/Mac/Linux | obsproject.com | Gratis, paling lengkap, bisa scene switching |
| Windows Game Bar | Windows | `Win+G` | Built-in, mudah |
| Loom | Browser/App | loom.com | Gratis (terbatas), langsung share |
| ShareX | Windows | getsharex.com | Gratis, banyak fitur |

### D.2 Cara Rekam Kamera + Screen Sekaligus (OBS Studio)

1. **Scene 1:** Full screen recording (untuk bagian PlatformIO / Serial Monitor)
2. **Scene 2:** Picture-in-picture → screen recording + kamera pojok kanan bawah (untuk bagian robot berlari)
3. **Scene 3:** Full kamera (untuk soldering dan assembly)
4. Gunakan **hotkey** untuk ganti scene tanpa memotong rekaman

### D.3 Tips Merekam Robot Berlari

- Pasang kamera di **tripod** atau stabilizer, jangan pegang tangan
- Rekam dari **atas (bird's eye view)** untuk melihat pergerakan robot di garis
- Tambahkan **kamera kedua** jika ada: satu dari atas, satu untuk OLED
- Gunakan **pencahayaan yang sama** dengan saat robot dikalibrasi
- Tandai lintasan dengan penggaris di pinggir video agar performa terlihat jelas

### D.4 Tips Merekam MPU-6050

- Split screen: Serial Monitor di satu sisi, kamera robot di sisi lain (OBS Scene switching)
- Saat demonstrasi pitch/roll: pegang robot perlahan, jangan gerakan mendadak
- Serial Plotter: atur batas Y-axis yang masuk akal (misal -90 s.d. +90 untuk sudut)
- Beri narasi verbal: "sekarang saya miringkan robot ke depan... terlihat nilai pitch naik ke sekitar 20 derajat"

### D.5 Pengaturan Rekaman

| Aspek | Rekomendasi |
|-------|------------|
| Resolusi | 1920×1080 atau minimal 1280×720 |
| Frame rate | 30 fps |
| Audio | Headset microphone (lebih bersih dari mic internal) |
| Format | MP4 (H.264) |
| Ukuran file max | 3 GB |
| Nama file | `Video_LF_[NIM]_[NamaLengkap].mp4` |

### D.6 Struktur Video yang Disarankan

```
[0:00–0:20]  Opening: Nama, NIM, "Tugas Video Modul 06 Build Line Follower"
[0:20–4:20]  Bagian 1: Penjelasan teori (IR sensor, PID, MPU-6050, CF)
[4:20–7:20]  Bagian 2–3: Soldering + assembly mekanik
[7:20–9:20]  Bagian 4–5: Setup PlatformIO + test sensor + binary run
[9:20–12:20] Bagian 6–7: P controller tuning + PD controller
[12:20–16:20] Bagian 8: MPU-6050 (semua 9 poin demonstrasi)
[16:20–18:20] Bagian 9: Hasil akhir robot + preview project kelompok
[18:20–19:20] Bagian 10: Analisis + kesimpulan
[19:20–20:00] Penutup singkat
```

---

## E. CHECKLIST SEBELUM SUBMIT

**Konten:**
- [ ] Semua 10 bagian ada dalam video
- [ ] Nama dan NIM tampil di awal video
- [ ] Semua 12 sensor terbukti merespons di video
- [ ] Tiga nilai Kp berbeda dan perbandingan P vs PD didemonstrasikan
- [ ] MPU-6050: init OK, raw data, pitch/roll, complementary filter, yaw correction — semuanya ada
- [ ] Robot menyelesaikan minimal 2 putaran penuh dengan PD+IMU
- [ ] Data di OLED menampilkan informasi IMU
- [ ] Project kelompok dijelaskan dan didemonstrasikan minimal 1 fitur

**Kualitas:**
- [ ] Resolusi minimal HD 720p
- [ ] Audio jelas tanpa noise berlebihan
- [ ] Durasi 15–25 menit
- [ ] Teks di Serial Monitor/OLED terbaca di video
- [ ] Robot terlihat jelas saat berlari (tidak goyang atau kabur)

**File:**
- [ ] Format MP4
- [ ] Nama file: `Video_LF_[NIM]_[NamaLengkap].mp4`
- [ ] Diupload ke platform yang ditentukan dosen sebelum batas waktu

---

> ⚠️ *Video yang tidak memenuhi minimal 70% kelengkapan konten tidak akan dinilai.*  
> ⚠️ *Bagian MPU-6050 (Bagian 8) yang tidak didemonstrasikan sama sekali akan kehilangan 8 poin dari Kelengkapan Konten dan 8 poin dari Akurasi Teknis.*  
> ⚠️ *Tugas video dikerjakan secara INDIVIDUAL — tidak boleh bergabung dengan anggota kelompok lain dalam satu video.*
