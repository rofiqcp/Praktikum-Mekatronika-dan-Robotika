# TUGAS VIDEO MODUL 04: IoT WEBSERVER MQTT ESP32

**Program Studi:** Teknologi Rekayasa Otomasi
**Mata Kuliah:** Praktikum Mekatronika dan Robotika
**Modul:** 04 – IoT WebServer MQTT ESP32
**Hardware:** ESP32, Sensor DHT22/DS18B20/MQ-135, Relay/LED Aktuator
**Software:** PlatformIO (VS Code), Mosquitto MQTT Broker, Node.js/Python FastAPI, Vue.js/HTML5, PostgreSQL/SQLite
**Batas Upload:** Sesuai jadwal dosen
**Durasi Video:** 20–45 menit
**Format:** MP4, resolusi minimal HD 720p
**Platform Upload:** Google Drive / YouTube (unlisted) / LMS

---

## A. KETENTUAN UMUM

> ⚠️ **TUGAS VIDEO DIKERJAKAN SECARA INDIVIDUAL (PER ORANG)**

1. Setiap mahasiswa wajib membuat **video sendiri-sendiri** (bukan per kelompok)
2. Video menampilkan **screen recording seluruh 10 percobaan** (Langkah 1–10) milik Anda sendiri
3. Video **juga harus menyertakan rekaman fisik (hardware)** — tampilkan ESP32, sensor, aktuator, dan hasilnya secara nyata di kamera
4. Tampilkan **nama lengkap dan NIM** di awal video
5. Gunakan **screen recording** yang jelas — proses nyata, bukan slideshow
6. Penjelasan dalam **Bahasa Indonesia** yang baik dan benar
7. Setiap percobaan harus ditunjukkan **dua sisi**: (a) kode dan terminal di layar, dan (b) hasil fisik pada hardware
8. Demo project yang dipilih harus berjalan **end-to-end** dari ESP32 hingga dashboard web

---

## B. POIN-POIN YANG HARUS DIJELASKAN DALAM VIDEO

---

### BAGIAN 1: PENDAHULUAN – KONSEP DASAR IoT DAN MQTT (Maks. 3 menit)

**Yang harus dijelaskan (boleh tanpa menunjukkan layar kode):**

- [ ] **1.1** Definisi IoT (Internet of Things) dan peranannya dalam otomasi industri dan robotika
- [ ] **1.2** Arsitektur sistem IoT tiga lapisan: Perception Layer (sensor/ESP32), Network Layer (MQTT Broker), Application Layer (server/dashboard)
- [ ] **1.3** Protokol MQTT: apa itu, mengapa efisien untuk IoT, perbedaannya dengan HTTP
- [ ] **1.4** Model Publish/Subscribe MQTT: peran Publisher, Subscriber, dan Broker — jelaskan dengan contoh topik sensor
- [ ] **1.5** QoS MQTT (Level 0, 1, 2): perbedaan dan kapan masing-masing digunakan
- [ ] **1.6** Kemampuan ESP32 sebagai IoT node: WiFi dual-band, Bluetooth, ADC, GPIO, clock 240 MHz
- [ ] **1.7** Alur data sistem yang dibangun: ESP32 → MQTT Broker → Python/Node.js Backend → Database → Dashboard Web

*Panduan: Jelaskan seolah mengajar teman yang baru pertama kali belajar IoT. Gunakan diagram atau sketsa jika membantu.*

---

### BAGIAN 2: DEMO PERCOBAAN 1–5 (Maks. 15 menit)

> Setiap percobaan: tampilkan **screen recording kode + terminal**, lalu tunjukkan **hasil fisik di kamera**.

---

#### Percobaan 1 – Instalasi dan Konfigurasi Mosquitto MQTT Broker (Maks. 3 menit)

- [ ] **2.1.1** Tampilkan proses instalasi Mosquitto di sistem Anda (Windows/Linux/macOS)
- [ ] **2.1.2** Tampilkan file konfigurasi `mosquitto.conf` yang digunakan — jelaskan setiap baris penting (`listener`, `allow_anonymous`, `password_file`)
- [ ] **2.1.3** Demonstrasikan menjalankan Mosquitto Broker dari terminal dan verifikasi port 1883 aktif
- [ ] **2.1.4** Demonstrasikan uji koneksi menggunakan `mosquitto_pub` dan `mosquitto_sub` di dua terminal berbeda
- [ ] **2.1.5** Tampilkan pesan berhasil terkirim dan diterima di terminal subscriber sebagai bukti broker berjalan

---

#### Percobaan 2 – Setup Project ESP32 dengan PlatformIO (Maks. 3 menit)

- [ ] **2.2.1** Tampilkan VS Code dengan ekstensi PlatformIO terinstal
- [ ] **2.2.2** Demonstrasikan membuat project PlatformIO baru: pilih board `esp32dev`, framework Arduino
- [ ] **2.2.3** Tampilkan `platformio.ini` yang dikonfigurasi — jelaskan `lib_deps` (PubSubClient, DHT, ArduinoJson)
- [ ] **2.2.4** Tampilkan file `config.h` yang berisi SSID WiFi, password, dan IP broker MQTT
- [ ] **2.2.5** Demonstrasikan proses build (compile) pertama — tampilkan output "SUCCESS" di terminal
- [ ] **2.2.6** Tampilkan fisik: papan ESP32 yang terhubung ke komputer via USB

---

#### Percobaan 3 – Setup Python Environment (Maks. 3 menit)

- [ ] **2.3.1** Tampilkan pembuatan virtual environment Python (`python -m venv venv`) dan proses aktivasinya
- [ ] **2.3.2** Demonstrasikan instalasi library yang diperlukan: `paho-mqtt`, `psycopg2`, `fastapi`, `uvicorn`, `requests`
- [ ] **2.3.3** Tampilkan file `requirements.txt` yang dihasilkan dan jelaskan fungsi masing-masing library
- [ ] **2.3.4** Demonstrasikan test koneksi Python ke Mosquitto Broker menggunakan script sederhana
- [ ] **2.3.5** Tampilkan output sukses koneksi di terminal Python sebagai bukti environment siap

---

#### Percobaan 4 – Program ESP32: Baca Sensor dan Publish ke MQTT (Maks. 3 menit)

- [ ] **2.4.1** Jelaskan dan tampilkan kode fungsi `setup()`: inisialisasi WiFi, koneksi ke MQTT Broker, pin sensor
- [ ] **2.4.2** Jelaskan kode fungsi `loop()`: baca sensor, format JSON payload, publish ke topik MQTT
- [ ] **2.4.3** Tampilkan struktur topik MQTT yang digunakan (contoh: `lab/sensor/suhu`, `lab/sensor/kelembaban`)
- [ ] **2.4.4** Demonstrasikan upload kode ke ESP32 (proses flash) — tampilkan output "Uploading... Done"
- [ ] **2.4.5** Tampilkan **Serial Monitor** VS Code: data sensor tercetak dan konfirmasi pesan MQTT terkirim
- [ ] **2.4.6** Tampilkan **fisik hardware**: ESP32 menyala, sensor DHT22/DS18B20 terhubung, LED indikator aktif

---

#### Percobaan 5 – Python Subscriber: Menerima Data dari Broker (Maks. 3 menit)

- [ ] **2.5.1** Tampilkan dan jelaskan kode Python subscriber: fungsi `on_connect`, `on_message`, dan loop utama
- [ ] **2.5.2** Demonstrasikan subscribe ke topik sensor ESP32 secara real-time
- [ ] **2.5.3** Tampilkan data JSON yang diterima Python dari ESP32 di terminal — verifikasi nilai suhu/kelembaban sesuai fisik
- [ ] **2.5.4** Tunjukkan proses parsing JSON (`json.loads`) dan tampilkan nilai individual di terminal
- [ ] **2.5.5** Tampilkan **fisik**: sensor didekatkan sumber panas/dingin → nilai berubah di terminal Python secara real-time

---

### BAGIAN 3: DEMO PERCOBAAN 6–10 (Maks. 15 menit)

> Setiap percobaan: tampilkan **screen recording kode + terminal/browser**, lalu tunjukkan **hasil fisik di kamera**.

---

#### Percobaan 6 – Python Publisher: Kirim Perintah ke ESP32 (Maks. 3 menit)

- [ ] **3.6.1** Tampilkan dan jelaskan kode Python publisher: publish perintah JSON ke topik kontrol aktuator
- [ ] **3.6.2** Tunjukkan kode ESP32 yang subscribe ke topik perintah dan mengeksekusi aksi (nyalakan relay/LED)
- [ ] **3.6.3** Demonstrasikan live: jalankan script Python publisher di terminal, kirim perintah `{"relay": "ON"}`
- [ ] **3.6.4** Tampilkan **Serial Monitor** ESP32 menerima perintah dan mengonfirmasi eksekusi
- [ ] **3.6.5** Tampilkan **fisik hardware**: relay/LED menyala dan mati sesuai perintah dari Python secara real-time

---

#### Percobaan 7 – Setup Backend REST API (Maks. 3 menit)

- [ ] **3.7.1** Jelaskan pilihan stack yang digunakan: Node.js/Express (Track A) atau Python FastAPI (Track B)
- [ ] **3.7.2** Tampilkan struktur folder backend dan file konfigurasi utama (`app.js` / `main.py`)
- [ ] **3.7.3** Tunjukkan definisi endpoint REST API: `GET /api/sensor`, `POST /api/control`, `GET /api/history`
- [ ] **3.7.4** Demonstrasikan menjalankan server backend di terminal — tampilkan pesan "Server running on port 3000/8000"
- [ ] **3.7.5** Uji endpoint menggunakan **Postman** atau `curl` — tampilkan response JSON sukses di layar

---

#### Percobaan 8 – Integrasi Database PostgreSQL/SQLite (Maks. 3 menit)

- [ ] **3.8.1** Tampilkan konfigurasi koneksi database di backend (host, port, nama DB, user, password)
- [ ] **3.8.2** Tampilkan skema tabel database: kolom `id`, `timestamp`, `suhu`, `kelembaban`, `device_id`, dsb.
- [ ] **3.8.3** Demonstrasikan proses migrasi/pembuatan tabel (`CREATE TABLE` atau ORM migration)
- [ ] **3.8.4** Tunjukkan kode backend yang menyimpan data sensor masuk ke database secara otomatis via MQTT
- [ ] **3.8.5** Buka **pgAdmin / DBeaver / CLI psql** — tampilkan record data sensor tersimpan dalam tabel

---

#### Percobaan 9 – Frontend Dashboard Web (Maks. 3 menit)

- [ ] **3.9.1** Tampilkan struktur folder frontend dan file utama (`App.vue` / `index.html`)
- [ ] **3.9.2** Tunjukkan komponen grafik real-time (Chart.js / ApexCharts) yang menampilkan data sensor
- [ ] **3.9.3** Demonstrasikan dashboard di browser: grafik bergerak saat ESP32 mengirim data baru
- [ ] **3.9.4** Tunjukkan komponen kontrol aktuator di dashboard (toggle switch/tombol relay) dan demonstrasikan fungsinya
- [ ] **3.9.5** Tampilkan **fisik**: klik tombol di dashboard web → relay/LED fisik merespons secara real-time

---

#### Percobaan 10 – Deployment dengan PM2/Nginx dan ngrok (Maks. 3 menit)

- [ ] **3.10.1** Demonstrasikan konfigurasi **PM2** (`ecosystem.config.js`) untuk menjalankan backend sebagai service
- [ ] **3.10.2** Tampilkan PM2 process list (`pm2 list`) — backend berstatus `online`
- [ ] **3.10.3** Tampilkan konfigurasi Nginx sebagai reverse proxy ke backend (file `/etc/nginx/sites-available/iot-app`)
- [ ] **3.10.4** Demonstrasikan **ngrok** — jalankan tunnel, tampilkan URL publik yang dihasilkan
- [ ] **3.10.5** Akses dashboard web melalui URL ngrok dari **browser di HP/perangkat lain** — tampilkan berhasil terbuka dan data real-time berjalan

---

### BAGIAN 4: DEMO PROJECT (Maks. 10 menit)

**Tunjukkan project pilihan Anda berjalan secara end-to-end:**

- [ ] **4.1** Sebutkan nama project yang dipilih (Proyek 1–10) dan jelaskan tujuannya secara singkat
- [ ] **4.2** Tampilkan **arsitektur sistem project** Anda: diagram komponen hardware dan software yang digunakan
- [ ] **4.3** Demo **ESP32 + sensor/aktuator project** berjalan — tampilkan fisik hardware secara jelas di kamera
- [ ] **4.4** Tampilkan data mengalir dari ESP32 → MQTT Broker → Backend → Database secara live (tampilkan log terminal)
- [ ] **4.5** Demo **dashboard web project** di browser: grafik real-time, panel kontrol, dan histori data
- [ ] **4.6** Demonstrasikan skenario **kontrol aktuator** dari dashboard → tampilkan respons fisik hardware
- [ ] **4.7** Tunjukkan akses dashboard melalui **URL ngrok** dari HP/perangkat lain sebagai bukti akses remote berhasil
- [ ] **4.8** Jelaskan tantangan teknis yang dihadapi saat pengerjaan project dan bagaimana solusinya

---

### BAGIAN 5: PENJELASAN TEKNIS MENDALAM (Maks. 5 menit)

**Yang harus dijelaskan:**

- [ ] **5.1** Jelaskan arsitektur keseluruhan sistem yang telah dibangun — gambarkan aliran data dari sensor hingga browser
- [ ] **5.2** Bandingkan MQTT vs HTTP/REST: kapan MQTT lebih unggul, kapan REST lebih tepat digunakan
- [ ] **5.3** Jelaskan kenapa ESP32 lebih cocok dibanding Arduino Uno untuk proyek IoT berbasis WiFi ini
- [ ] **5.4** Jelaskan konsep **retained message** dan **last will** di MQTT — bagaimana keduanya meningkatkan reliabilitas sistem
- [ ] **5.5** Jelaskan pelajaran teknis terpenting yang Anda peroleh dari modul ini dan apa yang ingin Anda kembangkan selanjutnya

---

## C. RUBRIK PENILAIAN VIDEO

**Total Nilai: 100 poin**

---

### C.1 Kelengkapan Konten (40 poin)

| No | Bagian | Bobot | Skor (0–10) | Nilai |
| --- | --- | --- | --- | --- |
| 1 | Bag. 1 – Konsep dasar IoT dan MQTT (arsitektur, pub/sub, QoS, alur data) | 4 | | |
| 2 | Bag. 2 – Percobaan 1: Instalasi dan konfigurasi Mosquitto Broker | 3 | | |
| 3 | Bag. 2 – Percobaan 2: Setup project PlatformIO + ESP32 | 3 | | |
| 4 | Bag. 2 – Percobaan 3: Setup Python environment + library | 2 | | |
| 5 | Bag. 2 – Percobaan 4: Program ESP32 publish sensor ke MQTT | 4 | | |
| 6 | Bag. 2 – Percobaan 5: Python subscriber terima data real-time | 3 | | |
| 7 | Bag. 3 – Percobaan 6: Python publisher kirim perintah ke ESP32 | 3 | | |
| 8 | Bag. 3 – Percobaan 7: Setup backend REST API | 4 | | |
| 9 | Bag. 3 – Percobaan 8: Integrasi database | 4 | | |
| 10 | Bag. 3 – Percobaan 9: Frontend dashboard web real-time | 4 | | |
| 11 | Bag. 3 – Percobaan 10: Deployment PM2/Nginx + ngrok | 3 | | |
| 12 | Bag. 4 – Demo project end-to-end | 3 | | |
| **TOTAL** | | **40** | | |

*Skor per bagian: 10 = sempurna; 7–9 = baik; 4–6 = cukup; 1–3 = kurang; 0 = tidak ada*

---

### C.2 Akurasi Teknis (30 poin)

| No | Kriteria | Bobot | Skor (0–10) | Nilai |
| --- | --- | --- | --- | --- |
| 1 | Konsep IoT dan MQTT dijelaskan **secara benar** (arsitektur, QoS, topik, pub/sub) | 6 | | |
| 2 | Kode ESP32 **berfungsi benar** — sensor terbaca, data terpublish ke broker dengan format JSON yang tepat | 8 | | |
| 3 | Sistem backend dan database **terintegrasi dengan benar** — data tersimpan dan dapat diambil melalui REST API | 8 | | |
| 4 | Dashboard web dan kontrol aktuator **bekerja secara real-time** — respons fisik hardware sesuai perintah dari browser | 8 | | |
| **TOTAL** | | **30** | | |

---

### C.3 Kualitas Presentasi (20 poin)

| No | Kriteria | Bobot | Skor (0–5) | Nilai |
| --- | --- | --- | --- | --- |
| 1 | Narasi jelas, tidak terlalu cepat/lambat, mudah dipahami | 5 | | |
| 2 | Kualitas rekaman layar — resolusi HD, terminal/kode terbaca, browser terlihat jelas | 5 | | |
| 3 | Kualitas rekaman fisik (kamera) — hardware terlihat jelas, pencahayaan cukup, LED/relay terlihat merespons | 5 | | |
| 4 | Durasi sesuai (20–45 menit) — tidak terlalu singkat maupun terlalu panjang | 5 | | |
| **TOTAL** | | **20** | | |

---

### C.4 Demo Hardware dan Software (10 poin)

| No | Item yang Wajib Didemonstrasikan | Skor (0 atau 1) |
| --- | --- | --- |
| 1 | ESP32 menyala dan terhubung WiFi (tampak di Serial Monitor) | |
| 2 | Sensor fisik terbaca — nilai berubah saat kondisi fisik berubah (suhu/kelembaban/dsb.) | |
| 3 | Pesan MQTT publish dari ESP32 terlihat di terminal subscriber | |
| 4 | Perintah dari Python publisher menggerakkan aktuator (relay/LED) secara fisik | |
| 5 | Server backend berjalan dan merespons request REST API (Postman / curl) | |
| 6 | Data sensor tersimpan di database (tampilkan di pgAdmin/DBeaver/CLI) | |
| 7 | Dashboard web menampilkan grafik real-time yang bergerak saat ESP32 aktif | |
| 8 | Kontrol aktuator dari dashboard web berhasil menggerakkan hardware fisik | |
| 9 | Sistem diakses dari perangkat lain melalui URL ngrok (tampilkan di HP/tablet) | |
| 10 | Demo project pilihan berjalan end-to-end tanpa error kritis | |
| **TOTAL** | | **/10** |

---

### C.5 Rangkuman Nilai

| Komponen | Bobot | Nilai Didapat |
| --- | --- | --- |
| Kelengkapan Konten | 40 | |
| Akurasi Teknis | 30 | |
| Kualitas Presentasi | 20 | |
| Demo Hardware dan Software | 10 | |
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
| --- | --- | --- | --- |
| **OBS Studio** | Win/Mac/Linux | obsproject.com | Gratis, paling lengkap, bisa rekam + kamera sekaligus |
| Windows Game Bar | Windows | `Win+G` | Built-in, mudah, cukup untuk satu layar |
| Loom | Browser/App | loom.com | Gratis (terbatas), langsung share via link |
| ShareX | Windows | getsharex.com | Gratis, banyak fitur, bisa anotasi |
| QuickTime | macOS | Built-in | Bawaan macOS, mudah digunakan |

### D.2 Tools Rekaman Kamera (Hardware Demo)

| Metode | Keterangan |
| --- | --- |
| **OBS Studio (scene berganti)** | Rekam layar dan webcam bergantian dalam satu sesi, direkomendasikan |
| HP sebagai webcam (DroidCam/EpocCam) | Gunakan HP sebagai kamera eksternal yang terhubung ke laptop |
| HP rekam terpisah | Rekam hardware dengan HP, edit gabungkan dengan rekaman layar di post-production |
| Webcam eksternal | Kualitas lebih baik dari webcam laptop bawaan |

### D.3 Pengaturan Recording

| Aspek | Rekomendasi |
| --- | --- |
| Resolusi layar | 1920×1080 (Full HD) atau minimal 1280×720 |
| Resolusi kamera hardware | Minimal 720p, lebih baik 1080p |
| Frame rate | 30 fps (cukup untuk screen recording dan demo hardware) |
| Audio | Headset microphone — lebih bersih dari mic internal laptop |
| Format output | MP4 (H.264) |
| Ukuran file maksimal | 4 GB (video lebih panjang dari Modul 01) |
| Bitrate | 3000–6000 kbps untuk layar; 1500–3000 kbps untuk kamera |

### D.4 Tips Rekaman yang Baik

1. **Zoom in terminal** saat menampilkan output MQTT atau log server — gunakan `Ctrl++` atau perbesar font terminal
2. **Perbesar font VS Code** sebelum merekam: `File > Preferences > Settings > Font Size` → atur ke 16–18px
3. Aktifkan **Show Mouse Clicks** di OBS agar penonton tahu di mana Anda mengklik
4. **Tutup notifikasi sistem** sebelum merekam (Do Not Disturb mode) — notifikasi HP di layar bisa mengekspos data pribadi
5. **Siapkan semua terminal** sebelum merekam — buka terminal Mosquitto, terminal Python, Serial Monitor, dan browser secara bersamaan
6. Saat demo hardware, **pegang kamera stabil** atau gunakan tripod improvisasi — ESP32 dan LED harus terlihat jelas
7. **Jelaskan sebelum melakukan** — beritahu apa yang akan ditunjukkan sebelum mengklik atau mengetik
8. Jika terjadi error saat merekam, **jangan dipotong** — jelaskan error, baca pesan error, dan perbaiki secara live (ini justru nilai tambah teknis)
9. Gunakan **multi-scene OBS**: Scene 1 = layar penuh, Scene 2 = layar + kamera (picture-in-picture), Scene 3 = kamera penuh untuk demo hardware
10. Pastikan **Mosquitto Broker sudah berjalan** dan **ESP32 sudah terflash** sebelum memulai rekaman demo

### D.5 Struktur Video yang Disarankan

```
[0:00–0:30]   Opening: Nama, NIM, nama project yang dipilih, overview singkat sistem
[0:30–3:30]   Bagian 1: Konsep IoT, MQTT, arsitektur sistem, ESP32
[3:30–6:30]   Percobaan 1–2: Instalasi Mosquitto + Setup PlatformIO ESP32
[6:30–9:30]   Percobaan 3–4: Python environment + Program ESP32 publish sensor
[9:30–12:30]  Percobaan 5–6: Python subscriber + Python publisher kontrol aktuator
[12:30–15:30] Percobaan 7–8: Backend REST API + Integrasi database
[15:30–18:30] Percobaan 9–10: Dashboard web + Deployment PM2/Nginx/ngrok
[18:30–28:30] Bagian 4: Demo project end-to-end (pilih satu dari 10 proyek)
[28:30–33:30] Bagian 5: Penjelasan teknis mendalam, perbandingan, lessons learned
[33:30–35:00] Penutup: ringkasan singkat, kesimpulan
```

---

## E. CHECKLIST SEBELUM SUBMIT

**Konten Percobaan:**

- [ ] Percobaan 1 — Instalasi Mosquitto Broker ditampilkan (config + uji pub/sub terminal)
- [ ] Percobaan 2 — Setup PlatformIO ESP32 ditampilkan (project baru + platformio.ini + build sukses)
- [ ] Percobaan 3 — Setup Python environment ditampilkan (venv + install library + requirements.txt)
- [ ] Percobaan 4 — Program ESP32 publish sensor ditampilkan (kode + flash + Serial Monitor + fisik)
- [ ] Percobaan 5 — Python subscriber real-time ditampilkan (kode + terminal menerima data + demo perubahan fisik)
- [ ] Percobaan 6 — Python publisher kirim perintah ditampilkan (kode + terminal + aktuator fisik merespons)
- [ ] Percobaan 7 — Backend REST API ditampilkan (kode + server berjalan + uji Postman/curl)
- [ ] Percobaan 8 — Integrasi database ditampilkan (skema tabel + data tersimpan di pgAdmin/DBeaver)
- [ ] Percobaan 9 — Dashboard web ditampilkan (grafik real-time + kontrol aktuator dari browser)
- [ ] Percobaan 10 — Deployment ditampilkan (PM2 list + Nginx config + URL ngrok aktif + akses dari HP)

**Konten Project:**

- [ ] Nama project disebutkan dan dijelaskan di awal demo
- [ ] Arsitektur sistem project ditampilkan
- [ ] Demo hardware project berjalan (ESP32 + sensor/aktuator khusus project)
- [ ] Dashboard web project ditampilkan dengan data real-time
- [ ] Akses remote via ngrok dari perangkat lain berhasil ditampilkan

**Hardware Demo (Kamera):**

- [ ] ESP32 fisik terlihat jelas di kamera saat beroperasi
- [ ] Sensor fisik terlihat — nilai di Serial Monitor/dashboard berubah saat kondisi fisik berubah
- [ ] Aktuator fisik (relay/LED/buzzer) terlihat merespons perintah dari software
- [ ] Pencahayaan cukup — komponen dan teks pada hardware bisa diidentifikasi

**Kualitas Video:**

- [ ] Nama lengkap dan NIM tampil di awal video
- [ ] Resolusi minimal HD 720p
- [ ] Audio jelas tanpa noise berlebihan
- [ ] Durasi 20–45 menit
- [ ] Font terminal/kode cukup besar untuk terbaca di video

**File:**

- [ ] Format MP4
- [ ] Nama file: `Video_IoT_[NIM]_[NamaLengkap].mp4`
- [ ] Diupload ke platform yang ditentukan dosen sebelum batas waktu

---

*Video yang tidak memenuhi minimal 70% kelengkapan konten tidak akan dinilai.*
*Tugas video dikerjakan secara INDIVIDUAL — tidak boleh menggabungkan rekaman dengan anggota kelompok lain.*
*Wajib menampilkan DUA jenis rekaman: screen recording layar komputer DAN rekaman kamera fisik hardware.*
