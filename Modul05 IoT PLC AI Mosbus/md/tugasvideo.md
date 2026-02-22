# TUGAS VIDEO MODUL 05: KOMUNIKASI MODBUS PLC DENGAN EDGE DEVICE DAN SERVER IoT

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 05 – IoT PLC AI Modbus  
**Batas Upload:** Sesuai jadwal dosen  
**Durasi Video:** 15–25 menit  
**Format:** MP4, resolusi minimal HD 720p  
**Platform Upload:** Google Drive / YouTube (unlisted) / LMS  

---

## A. KETENTUAN UMUM

> ⚠️ **TUGAS VIDEO DIKERJAKAN SECARA INDIVIDUAL (PER ORANG)**

1. Setiap mahasiswa wajib membuat **video sendiri-sendiri** (bukan per kelompok)
2. Video menampilkan **proses dan hasil praktikum yang Anda kerjakan sendiri** dari Modul 05
3. Tampilkan **nama lengkap dan NIM** di awal video (tampil di layar atau tulisan overlay)
4. Gunakan **screen recording** yang jelas untuk bagian pemrograman dan konfigurasi
5. Gunakan **video kamera/smartphone** untuk merekam hardware (PLC, ESP32, dashboard)
6. Penjelasan dalam **Bahasa Indonesia** yang baik dan benar
7. Video harus mencakup **semua percobaan** yang dilakukan dan **project kelompok**

---

## B. POIN-POIN YANG HARUS DIJELASKAN DAN DIDEMONSTRASIKAN

---

### BAGIAN 1: KONSEP DASAR MODBUS DAN IIoT (Maks. 4 menit)

**Jelaskan tanpa harus menunjukkan hardware (boleh pakai slide/whiteboard):**

- [ ] **1.1** Definisi Industri 4.0 dan Industrial IoT (IIoT) — mengapa PLC perlu terhubung ke cloud
- [ ] **1.2** Protokol Modbus: sejarah singkat, standar (modbus.org), alasan masih digunakan di industri
- [ ] **1.3** Perbedaan **Modbus RTU** vs **Modbus TCP**: physical layer, jarak, kecepatan, jumlah perangkat
- [ ] **1.4** Model data Modbus: 4 jenis tabel (Coil, Discrete Input, Input Register, Holding Register) — jelaskan perbedaan dan Function Code yang digunakan
- [ ] **1.5** Arsitektur Master-Slave Modbus: siapa master, siapa slave dalam sistem yang Anda bangun
- [ ] **1.6** Peran edge device: mengapa MiniPC dan ESP32 diperlukan sebagai jembatan antara PLC dan server

*Panduan: Gambarkan diagram arsitektur sistem di whiteboard atau jelaskan menggunakan slide yang Anda buat sendiri*

---

### BAGIAN 2: KONFIGURASI PLC SEBAGAI MODBUS SLAVE (Maks. 3 menit)

**Tunjukkan layar software PLC (EMEB atau CX-Programmer):**

- [ ] **2.1** Software PLC yang digunakan: EMEB (untuk TM221) atau CX-Programmer (untuk CP2E)
- [ ] **2.2** Demonstrasikan konfigurasi **Modbus RTU Slave** pada PLC (serial line settings, slave ID, baud rate)
- [ ] **2.3** Demonstrasikan konfigurasi **Modbus TCP** pada PLC (IP address, port 502)
- [ ] **2.4** Tampilkan **register map** yang digunakan — jelaskan pemetaan %MW, %Q, %I, %IW ke alamat Modbus
- [ ] **2.5** Tunjukkan program **Ladder Diagram** yang dibuat: minimal rung kontrol I/O, rung salin AI ke MW, rung counter

---

### BAGIAN 3: PERCOBAAN KOMUNIKASI MODBUS RTU – MINIPC PYTHON (Maks. 3 menit)

**Tunjukkan screen recording terminal + video hardware:**

- [ ] **3.1** Tampilkan koneksi fisik: kabel RS-485 dari port serial PLC ke konverter USB-RS485 di MiniPC
- [ ] **3.2** Tunjukkan perintah identifikasi port USB: `ls /dev/ttyUSB*` (Linux) atau Device Manager (Windows)
- [ ] **3.3** Jalankan dan **rekam output** script `test_modbus_rtu.py` yang membaca holding register dari PLC
- [ ] **3.4** Jelaskan parameter konfigurasi: port, baudrate, parity, stopbits, slave ID
- [ ] **3.5** Demonstrasikan **menulis data ke PLC** (write_register dan write_coil) — tunjukkan perubahan di PLC (LED output menyala/mati)
- [ ] **3.6** Demonstrasikan respons PLC saat **koneksi terputus** (cabut kabel) — bagaimana program menangani error

---

### BAGIAN 4: PERCOBAAN KOMUNIKASI MODBUS TCP – MINIPC PYTHON (Maks. 2 menit)

- [ ] **4.1** Tampilkan koneksi fisik: kabel Ethernet dari PLC ke switch, dan MiniPC ke switch yang sama
- [ ] **4.2** Demonstrasikan `ping 192.168.1.10` untuk verifikasi konektivitas jaringan
- [ ] **4.3** Jalankan dan rekam output script `test_modbus_tcp.py` — tunjukkan data yang terbaca
- [ ] **4.4** Bandingkan secara kualitatif: apakah ada perbedaan respons antara RTU dan TCP?

---

### BAGIAN 5: PERCOBAAN KOMUNIKASI MODBUS – ESP32 PLATFORMIO (Maks. 3 menit)

**Screen recording VS Code + video hardware ESP32:**

- [ ] **5.1** Tampilkan project PlatformIO di VS Code: struktur folder, `platformio.ini`, `src/main.cpp`
- [ ] **5.2** Jelaskan konfigurasi `platformio.ini`: platform, board, lib_deps yang digunakan
- [ ] **5.3** Tunjukkan wiring ESP32 ke modul MAX485: GPIO17(TX), GPIO16(RX), GPIO4(DE/RE), A(+), B(-)
- [ ] **5.4** Demonstrasikan proses **build** (0 errors) → **upload** ke ESP32
- [ ] **5.5** Buka **Serial Monitor** di PlatformIO — rekam output: nilai register PLC yang terbaca oleh ESP32
- [ ] **5.6** Demonstrasikan **Modbus TCP** pada ESP32: ESP32 terhubung ke PLC via WiFi, tampilkan hasil pembacaan

---

### BAGIAN 6: PERCOBAAN GATEWAY MODBUS → MQTT (Maks. 3 menit)

- [ ] **6.1** Tampilkan Mosquitto MQTT Broker berjalan: `sudo systemctl status mosquitto`
- [ ] **6.2** Buka terminal subscriber: `mosquitto_sub -t "plc/data" -v`
- [ ] **6.3** Jalankan `gateway_mqtt.py` di terminal lain — rekam output log gateway
- [ ] **6.4** Tunjukkan data JSON diterima oleh subscriber di terminal subscriber
- [ ] **6.5** Buka **MQTT Explorer** — tampilkan tree topic dan payload secara visual
- [ ] **6.6** Jelaskan struktur JSON yang dikirim: timestamp, plc_id, registers[], outputs[], analog[]
- [ ] **6.7** Demonstrasikan dengan mengubah nilai register PLC (via EMEB/CX-Programmer) — tunjukkan perubahan langsung terlihat di subscriber MQTT

---

### BAGIAN 7: PERCOBAAN REST API DAN INTEGRASI SERVER (Maks. 2 menit)

- [ ] **7.1** Jalankan `uvicorn api_server:app ...` dan buka **Swagger UI** di `http://localhost:8000/docs`
- [ ] **7.2** Demonstrasikan endpoint **POST /api/v1/plc/data** di Swagger UI: isi body JSON, klik Execute, tampilkan response
- [ ] **7.3** Demonstrasikan endpoint **GET /api/v1/plc/{plc_id}/latest** dan GET history
- [ ] **7.4** Jalankan `gateway_rest.py` — tunjukkan data dari PLC dikirim ke API setiap 2 detik
- [ ] **7.5** Verifikasi: GET latest menampilkan data terbaru setelah gateway mengirim

---

### BAGIAN 8: DASHBOARD IoT REAL-TIME (Maks. 3 menit)

- [ ] **8.1** Buka **Node-RED** di browser (`http://localhost:1880`)
- [ ] **8.2** Tunjukkan flow yang sudah dibuat: MQTT in → JSON → Function → Gauge/Chart
- [ ] **8.3** Jelaskan setiap node dalam flow dan fungsinya
- [ ] **8.4** Buka **Node-RED Dashboard** (`http://localhost:1880/ui`) — rekam tampilan gauge dan chart real-time
- [ ] **8.5** Demonstrasikan: ubah nilai di PLC → lihat perubahan di dashboard secara real-time
- [ ] **8.6** Tunjukkan **alert/notifikasi** yang terpicu saat nilai melebihi batas yang dikonfigurasi

---

### BAGIAN 9: PROJECT KELOMPOK (Maks. 4 menit)

**Setiap mahasiswa wajib menjelaskan project kelompoknya secara individual:**

- [ ] **9.1** Sebutkan nomor dan nama project yang dipilih kelompok
- [ ] **9.2** Jelaskan latar belakang masalah (skenario cerita dari jobsheet project)
- [ ] **9.3** Tampilkan **arsitektur sistem** yang dirancang kelompok (diagram blok atau slide)
- [ ] **9.4** Demonstrasikan **program PLC** yang dibuat untuk project — jelaskan logika kontrolnya
- [ ] **9.5** Demonstrasikan **program Python/ESP32** yang dibuat — jelaskan peran masing-masing
- [ ] **9.6** Tampilkan **dashboard project** yang dibangun — tunjukkan fitur-fiturnya
- [ ] **9.7** Rekam **demo live** sistem project berjalan minimal 2 menit tanpa error
- [ ] **9.8** Jelaskan **hasil fisik** yang terlihat: lampu yang menyala, nilai yang berubah, alert yang muncul
- [ ] **9.9** Ceritakan **tantangan teknis** terbesar yang dihadapi dan bagaimana mengatasinya
- [ ] **9.10** Apa **pengembangan lebih lanjut** yang bisa dilakukan untuk project ini?

---

## C. RUBRIK PENILAIAN VIDEO

**Total Nilai: 100 poin**

---

### C.1 Kelengkapan Konten (40 poin)

| No | Bagian | Bobot | Skor (0–10) | Nilai |
|----|--------|-------|------------|-------|
| 1 | Bag. 1 – Konsep Modbus dan IIoT | 5 | | |
| 2 | Bag. 2 – Konfigurasi PLC | 5 | | |
| 3 | Bag. 3 – Modbus RTU Python | 6 | | |
| 4 | Bag. 4 – Modbus TCP Python | 3 | | |
| 5 | Bag. 5 – ESP32 PlatformIO | 6 | | |
| 6 | Bag. 6 – Gateway MQTT | 5 | | |
| 7 | Bag. 7 – REST API | 4 | | |
| 8 | Bag. 8 – Dashboard | 4 | | |
| 9 | Bag. 9 – Project | 2 | | |
| **TOTAL** | | **40** | | |

*Skor per bagian: 10 = sempurna; 7–9 = baik; 4–6 = cukup; 1–3 = kurang; 0 = tidak ada*

---

### C.2 Akurasi Teknis (30 poin)

| No | Kriteria | Bobot | Skor (0–10) | Nilai |
|----|---------|-------|------------|-------|
| 1 | Penjelasan Modbus teknis benar (format frame, FC, register map) | 8 | | |
| 2 | Konfigurasi PLC benar (slave ID, baud, IP, register mapping) | 7 | | |
| 3 | Program Python/ESP32 berjalan tanpa error, pembacaan data akurat | 8 | | |
| 4 | Integrasi MQTT/REST benar, data JSON terkirim sesuai format | 7 | | |
| **TOTAL** | | **30** | | |

---

### C.3 Kualitas Presentasi (20 poin)

| No | Kriteria | Bobot | Skor (0–5) | Nilai |
|----|---------|-------|-----------|-------|
| 1 | Narasi jelas, terstruktur, tempo sesuai | 5 | | |
| 2 | Kualitas video: resolusi HD, tidak blur, teks terbaca | 5 | | |
| 3 | Kualitas audio: jelas, tidak berisik | 5 | | |
| 4 | Durasi sesuai (15–25 menit), ada opening dan penutup | 5 | | |
| **TOTAL** | | **20** | | |

---

### C.4 Demonstrasi Hardware (10 poin)

| No | Item yang Wajib Direkam | Ada? |
|----|------------------------|------|
| 1 | Koneksi fisik PLC – RS-485 – MiniPC/ESP32 | ☐ Ya ☐ Tidak |
| 2 | PLC berjalan (LED RUN menyala) | ☐ Ya ☐ Tidak |
| 3 | Input PLC aktif saat tombol ditekan | ☐ Ya ☐ Tidak |
| 4 | Output PLC berubah saat dicontrol dari Python/ESP32 | ☐ Ya ☐ Tidak |
| 5 | ESP32 terhubung ke MAX485 | ☐ Ya ☐ Tidak |
| 6 | Serial monitor ESP32 menampilkan data PLC | ☐ Ya ☐ Tidak |
| 7 | MQTT subscriber menerima data | ☐ Ya ☐ Tidak |
| 8 | Dashboard menampilkan data real-time | ☐ Ya ☐ Tidak |
| 9 | Demo project kelompok berjalan | ☐ Ya ☐ Tidak |
| 10 | Reaksi sistem saat nilai PLC berubah terlihat di dashboard | ☐ Ya ☐ Tidak |

*Skor: 1 poin per item yang ada dengan kualitas memadai*

---

### C.5 Rangkuman Nilai

| Komponen | Bobot | Nilai Didapat |
|---------|-------|--------------|
| Kelengkapan Konten | 40 | |
| Akurasi Teknis | 30 | |
| Kualitas Presentasi | 20 | |
| Demonstrasi Hardware | 10 | |
| **TOTAL** | **100** | |

**Penilai:** ___________________  
**Tanggal:** ___________________

---

## D. PANDUAN TEKNIS PEMBUATAN VIDEO

### D.1 Tools Screen Recording

| Tool | Platform | Link | Keterangan |
|------|---------|------|-----------|
| **OBS Studio** | Win/Mac/Linux | obsproject.com | Gratis, paling lengkap |
| Windows Game Bar | Windows | `Win+G` | Built-in, mudah |
| Loom | Browser/App | loom.com | Gratis (terbatas) |
| SimpleScreenRecorder | Linux | via apt | Ringan untuk Linux |

### D.2 Pengaturan Recording yang Direkomendasikan

| Aspek | Rekomendasi |
|-------|------------|
| Resolusi | 1920×1080 (Full HD) minimal 1280×720 |
| Frame rate | 30 fps |
| Audio | Headset microphone (bukan mic internal) |
| Format output | MP4 (H.264) |
| Ukuran file maks | 2 GB |
| Bitrate video | 4000–8000 kbps |

### D.3 Tips Merekam Video Teknis yang Baik

1. **Zoom in** ke terminal/code yang sedang dijalankan agar teks terbaca jelas
2. **Slow down** saat menunjukkan konfigurasi — beri waktu penonton membaca
3. **Zoom ke hardware** saat menunjukkan LED menyala atau koneksi kabel
4. **Aktifkan highlight kursor** di OBS agar penonton tahu di mana pointer berada
5. **Tutup notifikasi sistem** sebelum merekam (Do Not Disturb)
6. **Jika ada error**, jangan dipotong — rekam proses troubleshooting dan jelaskan solusinya (ini nilai tambah!)
7. Gunakan **font terminal yang besar** (increase font size terminal sebelum recording)
8. Beri **pause sejenak** antar bagian agar penonton bisa ikuti alur

### D.4 Struktur Video yang Disarankan

```
[0:00–0:30]   Opening: Nama, NIM, perkenalan singkat modul
[0:30–4:30]   Bagian 1: Teori Modbus dan IIoT
[4:30–7:30]   Bagian 2: Konfigurasi PLC
[7:30–10:30]  Bagian 3+4: Demo Modbus RTU dan TCP Python
[10:30–13:30] Bagian 5: Demo ESP32 PlatformIO
[13:30–16:30] Bagian 6+7: Demo MQTT dan REST API
[16:30–18:30] Bagian 8: Demo Dashboard
[18:30–22:30] Bagian 9: Demo Project Kelompok
[22:30–23:00] Penutup: ringkasan dan refleksi belajar
```

### D.5 Cara Menggabungkan Video Hardware + Screen Recording

Gunakan OBS Studio dengan **Scene Collection**:
1. Scene 1 "Screen": hanya screen recording
2. Scene 2 "Camera + Screen": Picture-in-Picture (webcam kecil di pojok + screen)
3. Scene 3 "Camera Only": kamera penuh untuk show hardware

**Atau** gunakan DaVinci Resolve / OpenShot (free) untuk editing pasca recording.

---

## E. CHECKLIST SEBELUM SUBMIT

### Konten Video:
- [ ] Nama dan NIM tampil jelas di awal video
- [ ] Semua 9 bagian ada dalam video
- [ ] Demo Modbus RTU Python berhasil (data register terbaca)
- [ ] Demo Modbus TCP Python berhasil
- [ ] Demo ESP32 Serial Monitor menampilkan data PLC
- [ ] Demo MQTT subscriber menerima data JSON dari PLC
- [ ] Demo REST API Swagger UI — POST dan GET berhasil
- [ ] Demo dashboard real-time menampilkan data PLC
- [ ] Demo project kelompok berjalan minimal 2 menit

### Kualitas:
- [ ] Resolusi minimal HD 720p
- [ ] Audio jelas tanpa noise berlebihan
- [ ] Durasi 15–25 menit
- [ ] Teks di terminal/code terbaca
- [ ] LED/hardware terlihat jelas saat demo

### File:
- [ ] Format MP4
- [ ] Nama file: `Video_Modul05_[NIM]_[NamaLengkap].mp4`
- [ ] Diupload ke platform yang ditentukan dosen sebelum batas waktu
- [ ] Jika menggunakan Google Drive: pastikan link sudah di-share (Anyone with link can view)

---

## F. PERTANYAAN YANG SERING DIAJUKAN (FAQ)

**Q: Apakah boleh menggunakan simulator PLC jika hardware tidak tersedia?**  
A: Ya, boleh menggunakan simulator seperti ModRSsim2 (Modbus RTU simulator) atau Modbus TCP simulator. Namun tetap harus ada demo hardware PLC jika tersedia di laboratorium.

**Q: Bagaimana jika koneksi Modbus selalu error saat direkam?**  
A: Rekam saja error-nya dan jelaskan proses troubleshootingnya. Ini menunjukkan kemampuan problem-solving dan diberi nilai positif.

**Q: Apakah perlu merekam semua 10 percobaan?**  
A: Ya, seluruh percobaan harus tercakup dalam video, minimal ditunjukkan hasilnya. Fokuskan penjelasan mendalam pada percobaan yang paling relevan dengan project kelompok Anda.

**Q: Bolehkah video lebih dari 25 menit?**  
A: Video di atas 25 menit tidak akan mendapat poin kualitas presentasi penuh. Latih editing untuk memangkas bagian yang tidak relevan.

---

*Video yang tidak memenuhi minimal 70% kelengkapan konten tidak akan dinilai.*  
*Tugas video dikerjakan secara INDIVIDUAL — tidak boleh bergabung dengan anggota kelompok.*  
*Mahasiswa yang tidak mengumpulkan video tidak dapat lulus mata kuliah Praktikum.*
