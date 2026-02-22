# PROJECT MODUL 07: WALL FOLLOWER ROBOT DENGAN ESP32

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 07 – Wall Follower  
**Platform:** ESP32 + PlatformIO  
**Pengerjaan:** Per Kelompok (Maks. 4 Orang)  
**Deadline:** ___________________

---

> ⚠️ **KETENTUAN UMUM PROJECT**
> - Setiap kelompok memilih **1 opsi project** dari 10 opsi yang tersedia
> - Project merupakan pengembangan dari percobaan dasar (bukan copy-paste kode percobaan)
> - Wajib melakukan **improvisasi dan inovasi** sesuai konteks nyata yang dipilih
> - Presentasi dan demonstrasi live di hadapan dosen
> - Laporan project dalam format PDF (maks. 20 halaman)

---

## OPSI PROJECT 1: ROBOT INSPEKSI SALURAN KORIDOR GEDUNG

### Latar Belakang

Inspeksi rutin koridor gedung, terowongan utilitas, atau saluran HVAC memerlukan tenaga manusia yang berisiko dan mahal. Robot otonom wall follower dapat menjelajahi area sempit ini secara mandiri, mencatat kondisi dinding, dan melaporkan anomali.

### Deskripsi Project

Kembangkan robot wall follower ESP32 yang dapat:
1. Menjelajahi koridor sempit (lebar 25–40 cm) secara otonom menggunakan sensor HC-SR04 kiri, depan, dan kanan
2. Mendeteksi retakan atau perubahan tekstur dinding (simulasi dengan perubahan reflektansi sensor IR)
3. Menggunakan MPU-6050 untuk mendeteksi getaran abnormal pada dinding (threshold akselerasi) dan mencatat event tersebut
4. Merekam "peta" jalur yang telah dilalui berdasarkan integrasi gyroscope (dead reckoning sederhana)
5. Mengirimkan laporan inspeksi (jarak tempuh, anomali terdeteksi, temperatur MPU) via web interface ESP32 AP

### Spesifikasi Teknis Minimum

| Komponen | Spesifikasi |
|---------|------------|
| HC-SR04 × 3 | Kiri, Depan, Kanan |
| MPU-6050 | Deteksi vibrasi + dead reckoning |
| Sensor IR × 2 | Deteksi anomali permukaan |
| Web Interface | Log inspeksi real-time, download CSV |
| LED Indikator | Status: Normal / Anomali Terdeteksi |
| Buzzer | Alert saat anomali |

### Improvisasi dari Percobaan Dasar

| Percobaan Dasar | Pengembangan di Project |
|----------------|------------------------|
| Percobaan 3-4 (wall following sederhana) | Tambah logging event ke array dinamis |
| Percobaan 9 (WiFi config) | Tambah endpoint `/log` untuk download laporan |
| Percobaan 11-13 (MPU-6050) | Threshold vibrasi adaptif sesuai permukaan |

### Kriteria Penilaian

- **Fungsionalitas (40%):** Robot berhasil navigasi koridor + deteksi anomali
- **Inovasi (20%):** Improvisasi di luar spesifikasi minimum
- **Laporan (20%):** Analisis data log inspeksi
- **Presentasi (20%):** Demonstrasi live + penjelasan teknis

---

## OPSI PROJECT 2: AGV (AUTOMATED GUIDED VEHICLE) MINI GUDANG

### Latar Belakang

Gudang modern menggunakan AGV untuk mengangkut barang secara otonom di antara rak penyimpanan. Robot wall follower yang mengikuti dinding rak gudang dapat menggantikan operator manusia untuk tugas pengiriman barang internal.

### Deskripsi Project

Kembangkan AGV mini ESP32 yang mensimulasikan operasi gudang:
1. Robot mengikuti dinding rak kiri menggunakan PID wall following
2. Berhenti di **titik-titik pickup/drop** yang ditandai dengan marker garis hitam (mode hybrid wall + line)
3. Menggunakan MPU-6050 untuk memastikan robot berhenti dengan orientasi tepat lurus (heading correction) di setiap titik
4. Navigasi antar titik: A → B → C → kembali ke A secara loop
5. Web interface menampilkan: posisi saat ini (A/B/C), jumlah trip selesai, status baterai estimasi

### Skenario Arena

```
Rak Kiri (Dinding)
│
│  [TITIK A]──────[TITIK B]──────[TITIK C]
│  (START)        (PICKUP)       (DROP)
│
└─────────────────── Koridor Gudang ─────────────────────
```

### Spesifikasi Teknis Minimum

| Komponen | Spesifikasi |
|---------|------------|
| HC-SR04 | Wall following sepanjang rak |
| Sensor IR × 4 | Deteksi marker garis di titik A, B, C |
| MPU-6050 | Orientasi lurus saat berhenti + heading correction |
| LED/OLED | Display titik tujuan saat ini |
| Web Interface | Dashboard posisi + trip counter |

### Improvisasi dari Percobaan Dasar

- Percobaan 7 (hybrid navigation) → tambah logic state: MOVING / STOPPED_AT_POINT / LOADING
- Percobaan 12 (gyro turn) → gunakan untuk belokan U-turn di ujung koridor
- Percobaan 9 (WiFi) → tambah fitur "assign destination" dari smartphone

---

## OPSI PROJECT 3: ROBOT PEMADAM KEBAKARAN MAZE

### Latar Belakang

Dalam skenario kebakaran gedung, robot otonom dapat dikirim ke area berbahaya untuk mencari titik api atau korban. Robot wall follower yang mampu menjelajahi labirin bangunan sangat relevan untuk aplikasi search and rescue.

### Deskripsi Project

Kembangkan robot ESP32 yang dapat:
1. Menjelajahi maze (denah bangunan disederhanakan) menggunakan Left-Hand Rule
2. Mendeteksi "titik panas" yang disimulasikan dengan sensor suhu (sensor suhu dari MPU-6050 atau DHT11 tambahan)
3. Ketika menemukan "titik panas", robot berhenti dan mengirim notifikasi via WiFi (web push notification sederhana)
4. MPU-6050 digunakan untuk: belokan presisi 90°, deteksi jika robot terbalik/terguling
5. Setelah eksplorasi selesai, robot kembali ke titik start menggunakan riwayat belokan yang tercatat (reversed path)

### Skenario Arena

Maze berbentuk denah bangunan sederhana (3 ruangan, 2 koridor) dengan:
- 1 titik "api" (sensor suhu menunjukkan T > threshold) yang disimulasikan dengan lampu atau sumber panas kecil
- Beberapa "dead end" (jalan buntu)

### Spesifikasi Teknis Minimum

| Komponen | Spesifikasi |
|---------|------------|
| HC-SR04 × 3 | Navigasi maze |
| MPU-6050 | Gyro turn + tilt safety |
| DHT11/sensor suhu | Deteksi "titik panas" |
| LED Merah | Menyala saat titik api terdeteksi |
| Buzzer | Alert sirene saat kebakaran |
| Web Interface | Peta eksplorasi + status titik api |

---

## OPSI PROJECT 4: ROBOT PEMANDU MUSEUM / GALERI

### Latar Belakang

Robot pemandu otonom yang bergerak di sepanjang dinding galeri/museum dapat menunjukkan koleksi kepada pengunjung tanpa panduan manusia. Robot mengikuti dinding, berhenti di setiap "karya", dan memutar penjelasan audio.

### Deskripsi Project

Kembangkan robot ESP32 wall follower sebagai pemandu mini:
1. Bergerak mengikuti dinding galeri (ruangan persegi panjang simulasi)
2. Berhenti di setiap "karya" yang ditandai oleh marker garis
3. Saat berhenti, memainkan "deskripsi audio" – dalam implementasi ini: menampilkan teks deskripsi di web client yang terhubung
4. MPU-6050 memastikan robot selalu menghadap lurus ke "karya" saat berhenti (orientasi 0°)
5. Pengunjung dapat meminta penjelasan ulang atau skip ke exhibit berikutnya melalui web interface

### Fitur Inovatif

- **Voice trigger simulation:** tombol di web interface sebagai pengganti voice command
- **Bahasa ganda:** deskripsi bisa dalam Bahasa Indonesia atau English (pilihan via web)
- **Tour statistics:** berapa pengunjung (koneksi WiFi) yang mengikuti tur, waktu rata-rata per exhibit

---

## OPSI PROJECT 5: ROBOT PERTANIAN – PATROLI GREENHOUSE

### Latar Belakang

Greenhouse modern memiliki koridor sempit di antara tanaman. Robot otonom yang berpatroli mengikuti dinding greenhouse dapat memonitor kondisi tanaman (suhu, kelembaban) tanpa mengganggu aktivitas petani.

### Deskripsi Project

Kembangkan robot ESP32 wall follower untuk patroli greenhouse:
1. Robot mengikuti dinding samping greenhouse menggunakan PID wall follower
2. Di setiap titik monitoring (marker garis), robot berhenti dan membaca:
   - Suhu dan kelembaban (DHT22)
   - Data IMU: temperatur MPU-6050 sebagai sensor suhu udara tambahan
3. Data dikumpulkan dan ditampilkan di web dashboard (grafik suhu sepanjang greenhouse)
4. MPU-6050 mendeteksi angin kencang (getaran akselerasi tiba-tiba) dan mencatat event cuaca ekstrem
5. Alert otomatis via web jika suhu > 35°C atau kelembaban < 40%

### Spesifikasi Teknis Minimum

| Komponen | Spesifikasi |
|---------|------------|
| HC-SR04 × 2 | Wall following (kiri + depan) |
| DHT22 | Suhu + kelembaban |
| MPU-6050 | Deteksi angin + dead reckoning posisi |
| Web Dashboard | Grafik Chart.js real-time |
| Data Logging | Buffer 100 titik data di ESP32 SPIFFS |

---

## OPSI PROJECT 6: ROBOT KEAMANAN PERIMETER

### Latar Belakang

Robot security patroli yang mengikuti dinding perimeter area (pabrik, kantor, sekolah) dapat mendeteksi intrusi atau anomali tanpa penjaga keamanan manusia yang kelelahan.

### Deskripsi Project

Kembangkan robot ESP32 sebagai robot security patroli:
1. Robot mengikuti dinding perimeter area tertutup (arena persegi) secara loop terus-menerus
2. Mendeteksi intrusi: jika ada objek yang tiba-tiba muncul di area sensor (perubahan jarak tiba-tiba > 20 cm), kirim alert
3. MPU-6050 digunakan untuk: deteksi jika robot dipindah secara paksa (akselerasi mendadak tanpa motor aktif = gangguan), dan sebagai timestamp orientasi
4. Setiap putaran patrol dicatat (waktu, anomali, status sensor)
5. Web dashboard: live feed sensor, log patrol, tombol "pause patrol"

### Fitur Keamanan

- **Anti-tampering:** jika MPU-6050 mendeteksi robot digeser paksa saat mode patroli → buzzer alarm + web alert
- **Patrol report:** setiap 5 putaran, kirim ringkasan status ke web client terhubung
- **Night mode simulation:** base speed lebih lambat, LED indikator berkedip (simulasi lampu patroli malam)

---

## OPSI PROJECT 7: ROBOT REHABILITASI LABIRIN (MAZE SOLVER)

### Latar Belakang

Maze solving adalah tantangan klasik robotika yang digunakan dalam kompetisi robotik tingkat nasional dan internasional (seperti Kontes Robot Indonesia). Robot ESP32 wall follower yang diperkaya dengan IMU dapat memberikan solusi maze yang lebih andal.

### Deskripsi Project

Kembangkan robot maze solver ESP32 kompetisi-grade:
1. Implementasi **Bug1 Algorithm** untuk navigasi maze dengan target spesifik
2. Belokan presisi berbasis gyroscope (kesalahan < 3°)
3. MPU-6050 digunakan untuk: belokan tepat, deteksi jika robot stuck di sudut, estimasi jarak tempuh via dead reckoning
4. Fase **learning run:** robot pertama kali menjelajahi maze dan mencatat semua persimpangan
5. Fase **speed run:** berdasarkan peta yang dipelajari, robot mengambil rute terpendek ke target
6. Web interface: visualisasi peta maze yang dipelajari (grid ASCII), waktu terbaik, komparasi rute

### Kompetisi Simulasi

Buat maze dengan ukuran **5×5 sel** (setiap sel 15×15 cm). Ukur:
- Waktu learning run
- Waktu speed run terbaik
- Akurasi peta yang dipelajari (bandingkan dengan peta sesungguhnya)

---

## OPSI PROJECT 8: ROBOT PENGIRIMAN DALAM RUANGAN (INDOOR DELIVERY)

### Latar Belakang

Restoran, rumah sakit, dan hotel mulai mengadopsi robot pengiriman otonom di koridor. Robot wall follower yang mampu navigasi hybrid (mengikuti dinding + mengikuti garis) sangat cocok untuk skenario ini.

### Deskripsi Project

Kembangkan robot pengiriman ESP32:
1. Sistem navigasi hybrid: line follower di area terbuka (garis di lantai), wall follower di koridor sempit
2. **3 titik tujuan** yang dapat dipilih via web interface: Meja A, Meja B, Dapur
3. Robot menentukan rute terbaik berdasarkan peta sederhana yang di-hardcode
4. MPU-6050 digunakan untuk: memastikan robot berhenti dengan orientasi lurus di setiap tujuan, deteksi jika "paket" (objek di atas robot) jatuh (perubahan tiba-tiba pada berat/akselerasi)
5. Status pengiriman ditampilkan di web: "En route to Meja A", "Delivered!", "Returning to base"

### Fitur Inovatif

- **Collision avoidance enhancement:** kombinasi HC-SR04 + MPU-6050 impact detection
- **ETA estimation:** perkiraan waktu tiba berdasarkan jarak dan kecepatan rata-rata
- **Order queue:** tambah beberapa pesanan dalam antrian, robot mengeksekusi satu per satu

---

## OPSI PROJECT 9: ROBOT EDUKASI INTERAKTIF STEM

### Latar Belakang

Robot edukasi yang dapat dikendalikan dan dimodifikasi oleh siswa SMA/SMK dapat menjadi alat pembelajaran STEM yang efektif. Robot wall follower ESP32 yang dilengkapi web interface interaktif memungkinkan siswa memahami prinsip robotika secara visual dan hands-on.

### Deskripsi Project

Kembangkan robot edukasi ESP32 dengan mode ganda:
1. **Mode Demo:** robot berjalan otonom sebagai wall follower (untuk demonstrasi ke siswa)
2. **Mode Learning:** web interface menampilkan data sensor real-time dengan penjelasan:
   - Grafik jarak sensor vs waktu
   - Grafik output PID vs waktu
   - Grafik akselerasi MPU-6050
3. **Mode Tuning:** siswa dapat mengubah Kp/Ki/Kd via slider dan langsung melihat hasilnya
4. **Kuis Interaktif:** web interface menampilkan pertanyaan tentang apa yang sedang terjadi (misalnya "Kenapa robot berbelok kanan saat ini?")
5. MPU-6050 digunakan untuk: visualisasi orientasi robot di web (compass digital), deteksi jika siswa mengangkat/membalik robot

### Target Pengguna

Siswa SMA/SMK kelas 10-12, atau mahasiswa semester awal yang baru belajar robotika.

### Metrik Keberhasilan

- Siswa dapat memahami dampak perubahan Kp dalam 10 menit percobaan mandiri
- Dashboard yang informatif dan mudah dipahami siswa non-teknik

---

## OPSI PROJECT 10: ROBOT PEMETAAN RUANGAN SEDERHANA (ROOM MAPPER)

### Latar Belakang

Pemetaan ruangan adalah fitur dasar dari robot otonom modern seperti robot vacuum. Meskipun tanpa LIDAR atau kamera, robot wall follower ESP32 dengan sensor ultrasonik dan IMU dapat menghasilkan peta kasar sebuah ruangan.

### Deskripsi Project

Kembangkan robot ESP32 sebagai room mapper sederhana:
1. Robot mengikuti dinding perimeter ruangan (left-hand rule) untuk satu putaran penuh
2. Setiap 100ms, robot mencatat: (x, y) estimasi posisi dari dead reckoning gyro + odometri waktu, jarak kiri/depan/kanan
3. Setelah satu putaran, data dikirim ke web interface untuk divisualisasikan sebagai **peta 2D ASCII/grid**
4. MPU-6050 digunakan untuk: orientasi robot (heading), deteksi robot kembali ke posisi awal (perbandingan sudut total ≈ 360°)
5. Peta ditampilkan di web: grid 20×20, titik dinding ditandai '#', path robot ditandai '.'

### Contoh Output Peta

```
####################
#..................#
#..####............#
#..#  #............#
#..#  ########.....#
#..................#
#..................#
####################
```

### Spesifikasi Teknis Minimum

| Komponen | Spesifikasi |
|---------|------------|
| HC-SR04 × 3 | Data jarak untuk pemetaan |
| MPU-6050 | Heading + dead reckoning |
| SPIFFS / RAM buffer | Simpan data path (maks. 500 titik) |
| Web Interface | Render peta ASCII dinamis + download |

### Evaluasi Akurasi Peta

Bandingkan peta yang dihasilkan robot dengan sketsa ruangan sesungguhnya:
- Hitung persentase dinding yang terdeteksi dengan benar
- Ukur error posisi di titik-titik kunci

---

## PANDUAN PENGERJAAN PROJECT

### Timeline

| Minggu | Kegiatan |
|--------|---------|
| 1 | Pemilihan opsi, studi literatur, desain arsitektur sistem |
| 2 | Implementasi hardware + program dasar |
| 3 | Integrasi semua fitur + pengujian awal |
| 4 | Refinement, dokumentasi, persiapan presentasi |

### Format Laporan Project

1. **Cover:** Judul, Nama Kelompok, NIM, Tanggal
2. **Abstrak** (maks. 200 kata)
3. **Pendahuluan:** Latar belakang, tujuan, ruang lingkup
4. **Tinjauan Pustaka:** 5 referensi minimum
5. **Metodologi:** Desain sistem, wiring diagram, flowchart
6. **Implementasi:** Deskripsi kode utama (tidak perlu semua kode)
7. **Hasil dan Pembahasan:** Data pengujian + analisis
8. **Kesimpulan dan Saran**
9. **Referensi**
10. **Lampiran:** Kode program lengkap

### Kriteria Penilaian Umum

| Aspek | Bobot | Indikator |
|-------|-------|-----------|
| Fungsionalitas Dasar | 30% | Semua fitur wajib berjalan |
| Inovasi & Improvisasi | 20% | Fitur tambahan di luar minimum |
| Kualitas Laporan | 20% | Analisis mendalam, data valid |
| Presentasi & Demo | 20% | Demonstrasi live berhasil |
| Pemahaman Konsep | 10% | Mampu menjawab pertanyaan |
