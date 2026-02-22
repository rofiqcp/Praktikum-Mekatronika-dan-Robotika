# PROJECT MODUL 06: BUILD LINE FOLLOWER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 06 – Build Line Follower  
**Platform:** ESP32 + PlatformIO  
**Pengerjaan:** Per Kelompok (Maks. 4 Orang)  

---

> ⚠️ **Proyek ini merupakan improvisasi dari percobaan praktikum yang telah dilakukan.**  
> Pilih **SATU** dari 10 opsi soal project berikut dan kembangkan secara mandiri oleh kelompok.  
> Setiap proyek harus memanfaatkan robot line follower (ESP32 + PCB Modul 01 + MPU-6050) sebagai basis.

---

## A. LATAR BELAKANG

Pada Modul 06, mahasiswa telah:
1. Menyolder PCB Main dan PCB Sensor Line hasil desain Modul 01
2. Melakukan assembly mekanik robot line follower
3. Memprogram ESP32 dengan PlatformIO untuk kontrol binary dan PID
4. Mengintegrasikan MPU-6050 untuk koreksi yaw dan deteksi kemiringan

Proyek ini mendorong mahasiswa untuk **menerapkan kompetensi tersebut pada masalah nyata** dengan memodifikasi, meningkatkan, atau mengintegrasikan robot line follower ke dalam konteks industri yang relevan dengan Prodi Teknologi Rekayasa Otomasi.

---

## B. ATURAN UMUM PROYEK

- Setiap kelompok memilih **1 opsi project**
- Hardware basis: robot line follower dari Modul 06 (boleh modifikasi)
- Wajib menggunakan: ESP32, PCB sensor line, MPU-6050
- Diperbolehkan menambahkan sensor/aktuator tambahan
- Program menggunakan PlatformIO
- Durasi pengerjaan: 2 minggu setelah praktikum Modul 06
- Deliverables: program (kode), laporan singkat, video demo

---

## C. 10 OPSI SOAL PROJECT

---

### PROJECT 1: Sistem AGV Mini untuk Sortir Barang di Gudang

**Deskripsi Dunia Nyata:**
PT Logistika Indonesia memiliki gudang seluas 200m² dengan 3 stasiun sortir (A, B, C). Mereka membutuhkan robot kecil yang dapat membawa barang dari titik pengambilan ke stasiun sortir yang tepat berdasarkan kode warna pada barcode (disimulasikan dengan marker warna di jalur).

**Spesifikasi Project:**
1. Robot mengikuti jalur utama (line following dengan PID tuning dari percobaan)
2. Pada setiap persimpangan, robot membaca **marker identifikasi** (perbedaan pola garis) untuk menentukan arah: kiri (stasiun A), lurus (stasiun B), kanan (stasiun C)
3. MPU-6050 digunakan untuk deteksi apabila robot melewati **permukaan miring** (ramp antar lantai) → adjust kecepatan otomatis
4. Di setiap stasiun: buzzer berbunyi 2× sebagai konfirmasi pengiriman, LED indikator sesuai stasiun
5. ESP32 Wi-Fi: kirim status pengiriman (stasiun mana, waktu, jumlah) ke Serial/MQTT setiap kali barang "dikirim"
6. Tambahkan **counter LCD/OLED** yang menampilkan: stasiun terakhir, jumlah delivery hari ini
7. MPU-6050 yaw correction aktif di jalur lurus panjang antara stasiun

**Improvisasi yang Diharapkan:**
- Tambahkan mekanik payload sederhana (box kecil di atas robot)
- Simulasikan 3 delivery berturut-turut tanpa intervensi manusia
- Catat waktu total per rute, optimasi lintasan

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Navigasi persimpangan berhasil (>90%) | 25% |
| Deteksi ramp + kompensasi kecepatan MPU | 20% |
| Integrasi OLED/Buzzer konfirmasi | 20% |
| Logging data via Serial/Wi-Fi | 15% |
| Laporan + analisis data | 20% |

---

### PROJECT 2: Robot Patroli Keamanan Pabrik dengan Deteksi Anomali IMU

**Deskripsi Dunia Nyata:**
Pabrik PT Manufaktur Maju membutuhkan robot patroli otomatis yang bergerak mengikuti jalur di koridor pabrik dan mendeteksi anomali getaran yang mengindikasikan mesin bermasalah. Robot juga harus bisa diawasi dari jarak jauh melalui Wi-Fi.

**Spesifikasi Project:**
1. Robot mengikuti jalur patroli oval (simulating koridor pabrik) dengan PID optimal
2. MPU-6050 membaca **akselerasi 3-axis setiap 100ms** selama patroli
3. Jika **standar deviasi akselerasi** dalam 1 detik terakhir melebihi threshold → robot berhenti dan memberi sinyal alarm (buzzer + LED merah berkedip) → "anomali terdeteksi di titik X"
4. Posisi robot pada saat alarm dikiri menggunakan **dead reckoning** (estimasi posisi dari jumlah putaran dan arah berdasarkan gyro Z integral)
5. ESP32 Wi-Fi mode AP: dashboard web sederhana menampilkan:
   - Status robot (patroli / alarm / stop)
   - Nilai akselerasi real-time
   - Log event alarm (waktu, estimasi posisi)
6. Tombol reset alarm di dashboard web

**Improvisasi yang Diharapkan:**
- Simulasikan anomali: taruh buku tipis di bawah salah satu roda → getaran meningkat → robot alarm
- Bandingkan data akselerasi di jalur normal vs saat anomali (grafik)

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Patroli line follower stabil | 20% |
| Deteksi anomali getaran MPU akurat | 30% |
| Dashboard Wi-Fi real-time | 25% |
| Dead reckoning estimasi posisi | 10% |
| Laporan + grafik data | 15% |

---

### PROJECT 3: Conveyor Robot dengan Speed Sinkronisasi dan Kontrol Posisi

**Deskripsi Dunia Nyata:**
Lini produksi PT Elektronika Prima membutuhkan robot conveyor yang bergerak mengikuti garis dengan kecepatan yang dapat dikontrol secara presisi dari panel operator, dan mampu mempertahankan kecepatan konstan meski melewati ramp loading dock.

**Spesifikasi Project:**
1. Line following PID dengan **kecepatan yang dapat diatur via potentiometer** (atau via web interface)
2. MPU-6050 **mengkompensasi kecepatan di ramp** (pitch compensation) sehingga kecepatan ground speed tetap konstan ±5% dari setpoint
3. **Encoder motor** (opsional: tambahkan encoder ke motor) atau estimasi kecepatan dari duty cycle → tampilkan kecepatan aktual di OLED
4. Kontrol kecepatan closed-loop: PID kecepatan (outer loop) + PID posisi garis (inner loop) → cascade control
5. ESP32 WebServer: slider HTML untuk mengatur kecepatan setpoint (0–100%)
6. Log kecepatan aktual setiap 500ms, tampilkan grafik di Serial Plotter
7. Alert MPU: jika roll > 30° → stop darurat (conveyor jatuh)

**Improvisasi yang Diharapkan:**
- Buat ramp 15° dari buku atau kardus
- Bandingkan kecepatan aktual dengan dan tanpa IMU compensation di ramp

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Cascade control (PID posisi + kecepatan) berjalan | 30% |
| Ramp compensation MPU akurat | 25% |
| Web interface kecepatan setpoint | 20% |
| OLED menampilkan kecepatan aktual | 10% |
| Laporan perbandingan data | 15% |

---

### PROJECT 4: Robot Inspeksi Jalur Produksi dengan Pemetaan Cacat

**Deskripsi Dunia Nyata:**
PT Karpet Nusantara membutuhkan robot kecil yang berjalan di atas jalur produksi karpet dan mendeteksi serta mencatat posisi cacat (garis putus, noda) pada jalur garis referensi, untuk quality control otomatis.

**Spesifikasi Project:**
1. Robot mengikuti garis sambil **menganalisis pola pembacaan sensor** setiap 5ms
2. Deteksi "cacat jalur":
   - **Garis putus** (gap): semua sensor OFF selama >50ms
   - **Garis melebar** (noda): >8 sensor aktif secara bersamaan
   - **Garis miring tiba-tiba** (kink): error sensor berubah >30 dalam satu cycle
3. Setiap cacat dicatat ke **buffer EEPROM/SPIFFS** ESP32: {type, timestamp, posisi_estimasi_gyro}
4. MPU-6050 gyro Z diintegrasi untuk estimasi **posisi angular** robot (berapa derajat dari start)
5. Setelah satu putaran selesai: tampilkan laporan cacat di OLED dan kirim via Serial
6. LED: hijau = normal, kuning = garis melebar, merah = garis putus
7. Tombol export: kirim seluruh log ke Serial Monitor dalam format CSV

**Improvisasi yang Diharapkan:**
- Buat track dengan sengaja ada gap dan melebar → verifikasi deteksi
- Bandingkan akurasi posisi estimasi gyro dengan pengukuran fisik

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Deteksi 3 jenis cacat akurat | 35% |
| Logging EEPROM/SPIFFS | 20% |
| Estimasi posisi dengan gyro | 20% |
| Laporan OLED + Serial export | 10% |
| Analisis akurasi deteksi | 15% |

---

### PROJECT 5: Robot Balap Line Follower dengan Adaptive Racing Strategy

**Deskripsi Dunia Nyata:**
Kompetisi Kontes Robot Indonesia (KRI) kategori Line Follower membutuhkan robot yang dapat menyelesaikan lintasan dengan waktu tercepat. Tim robot PT Robotika Unggul membutuhkan sistem yang secara otomatis menyesuaikan strategi balap berdasarkan kondisi trek.

**Spesifikasi Project:**
1. Implementasikan **semua optimasi** yang dipelajari di percobaan:
   - PD controller dengan speed profile adaptif (error besar → lambat, error kecil → kencang)
   - MPU-6050 yaw correction di straight
   - MPU-6050 ramp compensation
2. **Auto-tune mode**: sebelum balapan, robot berjalan satu putaran lambat sambil mencatat:
   - Panjang setiap segmen straight dan curved (dari waktu × kecepatan)
   - Sudut tikungan (dari integral gyro Z)
   - Kemiringan (pitch dari accelerometer)
3. Berdasarkan data auto-tune, robot menghitung **profil kecepatan optimal** per segmen
4. Balapan utama: gunakan profil kecepatan yang sudah dihitung
5. OLED: tampilkan waktu lintasan real-time, lap counter, kecepatan saat ini
6. Setelah finish: tampilkan best lap time, rata-rata kecepatan, jumlah keluar garis

**Improvisasi yang Diharapkan:**
- Bandingkan waktu lap sebelum dan sesudah auto-tune
- Uji di track dengan minimal 2 ramp dan 4 tikungan

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Auto-tune berjalan dan menghasilkan profil valid | 30% |
| Performa balapan (waktu dan stabilitas) | 25% |
| Integrasi IMU (yaw + ramp) | 20% |
| OLED dashboard balapan | 10% |
| Laporan perbandingan | 15% |

---

### PROJECT 6: Smart Line Follower dengan Machine Learning Gesture Recognition

**Deskripsi Dunia Nyata:**
PT Interaktif Solusi mengembangkan robot edukasi yang dapat dikontrol melalui gerakan tangan instruktur. Robot harus mengenali 5 jenis "gesture" dari getaran yang dipicu instruktur (tepuk meja, ketuk dinding, dll.) dan mengubah mode operasinya.

**Spesifikasi Project:**
1. **Rekam dataset gesture** menggunakan MPU-6050:
   - Gesture 1: tepuk meja 1× → robot mulai
   - Gesture 2: tepuk meja 2× → robot berhenti
   - Gesture 3: goyangkan robot kiri-kanan → robot belok kiri 90° (satu tikungan)
   - Gesture 4: goyangkan robot maju-mundur → robot belok kanan 90°
   - Gesture 5: angkat robot → robot masuk mode kalibrasi sensor
2. Implementasikan **simple threshold classifier** pada ESP32:
   - Baca 50 sampel akselerasi (500ms window)
   - Hitung fitur: mean, std_dev, max, min per axis
   - Klasifikasikan gesture berdasarkan aturan threshold
3. Integrasikan ke line follower: saat tidak ada gesture → line following normal
4. OLED: tampilkan gesture terdeteksi + mode aktif
5. Logging: catat semua gesture terdeteksi + timestamp ke SPIFFS

**Improvisasi yang Diharapkan:**
- Uji akurasi klasifikasi: 20 percobaan per gesture, hitung true positive rate
- Tambahkan buzzer feedback berbeda untuk setiap gesture

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Klasifikasi gesture akurat (>80%) | 35% |
| Integrasi gesture ke line follower | 25% |
| Logging SPIFFS | 15% |
| OLED + buzzer feedback | 10% |
| Laporan akurasi dan analisis | 15% |

---

### PROJECT 7: Robot Penghantar Obat Otomatis (Medical Delivery Robot)

**Deskripsi Dunia Nyata:**
RS Modern Indonesia membutuhkan robot kecil yang mengantarkan obat dari apotek ke 4 ruang pasien yang terhubung dengan koridor. Robot harus dapat beroperasi aman di lingkungan rumah sakit (tidak bertabrakan, mendeteksi rintangan manusia yang lewat).

**Spesifikasi Project:**
1. Robot mengikuti jalur garis di koridor (lintasan dengan 4 persimpangan ke ruang pasien)
2. **Sistem antrian pengiriman** via web interface:
   - Input: nomor ruang tujuan (1–4)
   - Robot mengeksekusi antrian secara urutan (FIFO)
3. MPU-6050 mendeteksi **getaran berat** (seseorang menabrak robot) → stop + buzzer alarm + kirim notifikasi via Serial
4. **Sensor ultrasonic** (HC-SR04 yang sudah ada di PCB) → obstacle avoidance: jika ada orang/benda dalam 30cm → berhenti menunggu → lanjut jika clear
5. Di setiap ruang tujuan: robot berhenti 5 detik (simulasi serah terima), OLED tampilkan "RUANG X – MENUNGGU", buzzer 3×
6. MPU-6050 roll: jika robot didorong keras ke samping → alarm + kirim event

**Improvisasi yang Diharapkan:**
- Simulasikan 3 pengiriman berturut-turut
- Uji obstacle avoidance dengan menghalangi jalan manual

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Antrian pengiriman multi-destination | 25% |
| Obstacle avoidance HC-SR04 | 25% |
| Deteksi tabrakan MPU-6050 | 20% |
| Web interface antrian | 15% |
| OLED + protokol pengiriman | 15% |

---

### PROJECT 8: Robot Pemantau Kondisi Lingkungan Jalur (Track Condition Monitor)

**Deskripsi Dunia Nyata:**
PT Konstruksi Jaya membutuhkan robot kecil yang berpatroli di atas rel/jalur dan memantau kondisi permukaan — mendeteksi getaran abnormal yang mengindikasikan keretakan rel atau permukaan yang tidak rata, lalu melaporkan posisinya.

**Spesifikasi Project:**
1. Robot mengikuti garis sebagai "jalur rel" dengan line following PID
2. MPU-6050 merekam **data akselerasi kontinu** selama patroli
3. Implementasikan **analisis frekuensi sederhana (FFT approx)** di ESP32:
   - Buffer 128 sampel akselerasi Z
   - Hitung rata-rata dan standar deviasi
   - Deteksi komponen frekuensi tinggi (>10Hz) yang mengindikasikan retakan
4. **Posisi estimasi** menggunakan dead reckoning: integrasi gyro Z untuk yaw, asumsi kecepatan konstan dari duty cycle PWM
5. Setiap anomali disimpan: {timestamp, posisi_x, posisi_y, level_getaran}
6. Setelah satu putaran penuh: kirim laporan JSON via Serial ke PC (atau simpan di SPIFFS)
7. PC-side: script Python sederhana untuk visualisasi peta retakan (plot posisi × level getaran)

**Improvisasi yang Diharapkan:**
- Buat 2 area "cacat" di jalur (taruh kertas berlapis untuk bergelombang)
- Verifikasi bahwa posisi terdeteksi mendekati posisi fisik cacat

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Deteksi anomali frekuensi akurat | 30% |
| Dead reckoning posisi | 20% |
| Logging JSON + SPIFFS | 20% |
| Visualisasi Python | 15% |
| Laporan dan analisis | 15% |

---

### PROJECT 9: Multi-Robot Coordination (Leader-Follower System)

**Deskripsi Dunia Nyata:**
PT Otomasi Canggih membutuhkan sistem 2 robot yang bergerak berkonvoi — robot Pemimpin (Leader) mengikuti garis, robot Pengikut (Follower) mengikuti robot Pemimpin menggunakan sinyal Wi-Fi/ESP-NOW tanpa melihat garis.

**Spesifikasi Project:**
1. **Robot Leader** (ESP32 #1):
   - Line following PID normal
   - MPU-6050: kirim data yaw_rate dan pitch via **ESP-NOW** setiap 50ms ke robot Follower
   - OLED: tampilkan "LEADER | Speed:X | Yaw:Y"
2. **Robot Follower** (ESP32 #2):
   - Tidak membaca sensor garis (atau hanya sebagai backup)
   - Menerima paket ESP-NOW dari Leader
   - Mengikuti Leader dengan kecepatan dan koreksi arah berbasis data IMU yang diterima
   - Implementasikan **virtual leader tracking**: jika sinyal terputus >500ms → berhenti
3. Jarak antar robot: 30–50cm (diukur dari waktu tempuh)
4. Sinkronisasi: Leader mengirim kecepatan + yaw → Follower menerapkan dengan delay 200ms
5. Uji: konvoi 2 robot menyelesaikan lintasan oval tanpa tabrakan

**Improvisasi yang Diharapkan:**
- Bandingkan: Follower mengikuti garis sendiri vs mengikuti Leader via ESP-NOW
- Uji ketangguhan: matikan Leader sebentar, apakah Follower berhenti dengan aman?

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| ESP-NOW komunikasi stabil | 25% |
| Leader line following + IMU broadcast | 20% |
| Follower tracking berhasil | 30% |
| Failsafe saat sinyal putus | 10% |
| Laporan sinkronisasi + analisis delay | 15% |

---

### PROJECT 10: Sistem Pembelajaran Reinforcement Learning (Q-Learning) untuk Line Follower

**Deskripsi Dunia Nyata:**
Lab AI Universitas Nusantara mengembangkan robot yang mampu **belajar sendiri** cara mengikuti garis tanpa perlu tuning manual. Robot menggunakan Q-Learning sederhana untuk menemukan strategi gerakan optimal dari pengalaman.

**Spesifikasi Project:**
1. **State space** (dari sensor garis): posisi garis dikuantisasi ke 7 state: {sangat kiri, kiri, sedikit kiri, tengah, sedikit kanan, kanan, sangat kanan}
2. **Action space**: 5 aksi: {belok kiri keras, belok kiri halus, lurus, belok kanan halus, belok kanan keras}
3. **Reward function**:
   - +10: sensor tengah aktif (di garis)
   - -5: sensor tepi aktif (mendekati keluar)
   - -20: semua sensor OFF (keluar garis)
   - Bonus: MPU-6050 akselerasi rendah (gerakan mulus) → +2
4. **Q-table**: 7 state × 5 action = 35 nilai, disimpan di SPIFFS
5. **Training mode**: jalankan 50 episode (tiap episode = 1 putaran oval)
   - Epsilon-greedy: mulai epsilon=1.0 (random) → turun bertahap ke 0.1 (exploit)
   - Learning rate α = 0.1, discount γ = 0.9
6. **Inference mode**: tombol MODE → robot menggunakan Q-table hasil belajar
7. OLED: tampilkan episode, cumulative reward, epsilon saat ini

**Improvisasi yang Diharapkan:**
- Plot learning curve (cumulative reward per episode) dari log Serial
- Bandingkan: Q-Learning setelah 50 episode vs PD manual dari Percobaan 3

**Rubrik:**
| Kriteria | Bobot |
|---------|-------|
| Implementasi Q-Learning benar | 35% |
| Integrasi reward MPU-6050 | 15% |
| Training + inference mode | 20% |
| SPIFFS Q-table storage | 10% |
| Learning curve + analisis | 20% |

---

## D. FORMAT DELIVERABLES

### D.1 Kode Program

```
LineFollower_Project_[Kelompok]/
├── src/
│   ├── main.cpp
│   ├── line_follower.cpp
│   ├── imu_handler.cpp    ← MPU-6050 specific
│   └── project_logic.cpp  ← Logika project spesifik
├── include/
│   ├── config.h
│   ├── line_follower.h
│   ├── imu_handler.h
│   └── project_logic.h
├── lib/
├── platformio.ini
└── README.md              ← Penjelasan project, cara run, parameter
```

### D.2 Laporan Singkat (Maks. 8 Halaman)

1. Cover: nama proyek, kelompok, anggota NIM
2. Deskripsi masalah nyata yang diselesaikan
3. Diagram blok sistem (termasuk MPU-6050 dalam alur kontrol)
4. Penjelasan teknis implementasi utama
5. Data hasil pengujian dan grafik
6. Analisis: apakah MPU-6050 memberikan peningkatan nyata? Bukti data?
7. Kendala dan solusi
8. Kesimpulan dan rekomendasi pengembangan

### D.3 Video Demo (3–5 Menit)

- [ ] Tampilkan robot running di lintasan (setidaknya 2 putaran)
- [ ] Demonstrasikan fitur utama project (bukan hanya line following biasa)
- [ ] Tunjukkan data real-time di Serial Monitor / OLED saat robot berlari
- [ ] Demonstrasikan peran MPU-6050 (misal: goyangkan robot → lihat respons, buat ramp → lihat kompensasi)
- [ ] Narasi menjelaskan cara kerja dan inovasi yang ditambahkan

---

## E. RUBRIK PENILAIAN UMUM

**Total: 100 poin**

| No | Kriteria | Bobot | Keterangan |
|----|---------|-------|-----------|
| 1 | Fungsi dasar line following berjalan (PID, >2 putaran stabil) | 20 | Baseline wajib |
| 2 | Integrasi MPU-6050 bermakna dan berfungsi | 20 | Bukan hanya read data, harus mempengaruhi kontrol |
| 3 | Fitur utama project terpilih berjalan | 25 | Sesuai spesifikasi project |
| 4 | Kualitas kode (modular, commented, config.h) | 10 | Code review |
| 5 | Laporan: analisis data + bukti peningkatan vs baseline | 15 | Data harus ada |
| 6 | Video demo: jelas, menunjukkan semua fitur | 10 | Minimal 3 menit |
| **TOTAL** | | **100** | |

---

## F. JADWAL DAN PENGUMPULAN

| Kegiatan | Batas Waktu |
|---------|------------|
| Konfirmasi pilihan project ke dosen | H+3 setelah Modul 06 |
| Progress check (kode + demo parsial) | H+10 |
| Pengumpulan kode + laporan + video | H+14 |
| Presentasi project (5 menit per kelompok) | Pertemuan Modul 07 |

**Platform pengumpulan:** LMS / Google Drive kelompok / GitHub repository  
**Nama file:** `Project_M06_[NamaKelompok]_[NomorProject]`

---

## G. REFERENSI

- Espressif ESP-NOW Documentation. https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/network/esp_now.html
- InvenSense MPU-6050 Product Specification Rev 3.4. https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/
- Mahony, R., et al. (2008). "Nonlinear Complementary Filters on the Special Orthogonal Group." *IEEE Transactions on Automatic Control*, 53(5), 1203–1218.
- Sutton, R.S., & Barto, A.G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- ElectronicCats MPU6050 Library. https://github.com/ElectronicCats/mpu6050
- Adafruit SSD1306 Library. https://github.com/adafruit/Adafruit_SSD1306

---

*Dokumen ini diperbarui untuk Prodi Teknologi Rekayasa Otomasi.*  
*Hubungi dosen jika ada pertanyaan mengenai spesifikasi project atau teknis implementasi.*
