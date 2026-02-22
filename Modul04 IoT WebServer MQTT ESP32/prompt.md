# Prompt NotebookLLM – Modul 04: IoT WebServer MQTT ESP32
**Praktikum Mekatronika dan Robotika**
Universitas | Semester Genap

> Gunakan setiap prompt di bawah ini secara berurutan di NotebookLLM untuk menghasilkan 45 slide presentasi profesional Modul 04.

---

## BAGIAN 1 – PEMBUKA & TUJUAN (Slide 1–3)

---

### Slide 1: Cover / Halaman Judul

**Prompt NotebookLLM:**
Buatkan slide cover presentasi mata kuliah "Praktikum Mekatronika dan Robotika" untuk Modul 04 dengan judul utama "IoT WebServer MQTT ESP32". Tampilkan sub-judul "Membangun Sistem IoT End-to-End: Sensor, Broker, Backend, dan Frontend". Sertakan elemen visual berupa ilustrasi alur data dari perangkat ESP32 melewati broker MQTT menuju cloud server dan dashboard web. Gunakan palet warna biru-gelap dan oranye yang terkesan modern dan teknologi. Tambahkan nama mata kuliah, nomor modul (Modul 04), dan kolom untuk nama dosen serta tahun ajaran. Desain harus bersih, profesional, dan cocok untuk presentasi universitas teknik.

**Kata Kunci:** IoT, MQTT, ESP32, WebServer, Mekatronika, Robotika, Modul 04
**Visualisasi:** Ilustrasi arsitektur IoT sederhana (ESP32 → Broker → Server → Dashboard), logo universitas (placeholder), ikon WiFi dan cloud

---

### Slide 2: Capaian Pembelajaran dan Tujuan Modul

**Prompt NotebookLLM:**
Buatkan slide "Capaian Pembelajaran" yang menampilkan daftar tujuan pembelajaran Modul 04 secara terstruktur. Mahasiswa diharapkan mampu: (1) menjelaskan konsep dasar IoT dan arsitekturnya; (2) mengkonfigurasi broker MQTT Mosquitto di server lokal maupun cloud; (3) memprogram ESP32 sebagai edge device yang mengirim dan menerima data via MQTT menggunakan PlatformIO; (4) membangun laptop/PC sebagai Python edge device dengan library paho-mqtt; (5) merancang backend REST API dengan minimal salah satu dari Spring Boot, FastAPI, Node.js, atau C#; (6) membuat frontend dashboard IoT interaktif dengan Vue, React, atau Angular; (7) melakukan deployment menggunakan PM2, Nginx, certbot, dan ngrok. Gunakan ikon centang hijau di setiap poin. Tambahkan keterangan level taksonomi Bloom (C2–C6) di sisi kanan setiap poin.

**Kata Kunci:** Capaian pembelajaran, tujuan modul, kompetensi, Bloom's Taxonomy, IoT, MQTT, ESP32
**Visualisasi:** Daftar bullet terstruktur dengan ikon, piramida Bloom di sudut slide

---

### Slide 3: Gambaran Umum Modul dan Peta Materi

**Prompt NotebookLLM:**
Buatkan slide "Gambaran Umum Modul" yang menampilkan peta materi (roadmap) Modul 04 secara visual. Modul ini terdiri dari 8 topik utama yang disusun secara berurutan: (1) Dasar IoT, (2) Protokol MQTT, (3) Mosquitto Broker, (4) Database IoT, (5) ESP32 Edge Device, (6) Python Edge Device, (7) Backend & Frontend, (8) Deployment & Arsitektur Lengkap. Tampilkan peta materi sebagai diagram alur horizontal (flowchart) dengan panah yang menghubungkan setiap topik. Di bawah setiap kotak topik, tuliskan nomor slide yang membahas topik tersebut. Tambahkan estimasi durasi praktikum (total 4×100 menit = 400 menit). Gunakan warna berbeda untuk setiap blok topik.

**Kata Kunci:** Peta materi, roadmap, struktur modul, alur pembelajaran, IoT pipeline
**Visualisasi:** Flowchart horizontal 8 kotak berwarna dengan panah, timeline durasi di bawah

---

## BAGIAN 2 – DASAR-DASAR IoT (Slide 4–8)

---

### Slide 4: Apa Itu IoT? Definisi dan Konsep Dasar

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan definisi Internet of Things (IoT) secara komprehensif untuk mahasiswa teknik. Definisi inti: "IoT adalah jaringan objek fisik yang dilengkapi sensor, aktuator, dan konektivitas internet untuk mengumpulkan dan bertukar data tanpa interaksi manusia-ke-manusia atau manusia-ke-komputer." Sertakan statistik: proyeksi perangkat IoT global mencapai 29,4 miliar unit pada 2030 (Statista). Tampilkan 4 pilar utama IoT: Things (perangkat fisik), Connectivity (konektivitas jaringan), Data Processing (pemrosesan data), dan Action (tindakan/output). Berikan 3 contoh nyata di industri: smart factory, smart home, dan precision agriculture. Gunakan infografis lingkaran atau 4-kuadran. Tambahkan kutipan Kevin Ashton sebagai penemu istilah IoT.

**Kata Kunci:** IoT definition, Internet of Things, smart device, connectivity, data processing, edge computing
**Visualisasi:** Infografis 4 pilar IoT dengan ikon; ilustrasi ekosistem IoT (rumah pintar, pabrik, pertanian)

---

### Slide 5: Arsitektur IoT – 4 Layer Model

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan arsitektur IoT menggunakan model 4 lapisan (layer). Layer 1 – Perception Layer (lapisan persepsi): sensor suhu, kelembaban, akselerometer, kamera, aktuator motor. Layer 2 – Network Layer (lapisan jaringan): WiFi, Bluetooth, Zigbee, LoRa, NB-IoT, 4G/5G, MQTT, CoAP, HTTP. Layer 3 – Processing/Middleware Layer (lapisan pemrosesan): edge computing, fog computing, cloud server, database, message broker. Layer 4 – Application Layer (lapisan aplikasi): dashboard web, mobile app, sistem kontrol, ERP, AI/ML analytics. Tampilkan diagram piramida atau diagram vertikal bertumpuk dengan anak panah dua arah di antara layer. Setiap layer diberi warna berbeda dan diberi contoh teknologi konkret. Tambahkan keterangan posisi ESP32 dan laptop Python berada di Layer 1 dan Layer 2.

**Kata Kunci:** Arsitektur IoT, 4 layer, perception layer, network layer, middleware, application layer, edge computing
**Visualisasi:** Diagram piramida 4 layer berwarna dengan label teknologi dan ikon perangkat

---

### Slide 6: Protokol Komunikasi IoT – Perbandingan Lengkap

**Prompt NotebookLLM:**
Buatkan slide yang membandingkan protokol komunikasi IoT secara tabel dan visual. Protokol yang dibandingkan: MQTT, HTTP/REST, CoAP, WebSocket, AMQP, dan LoRaWAN. Kolom perbandingan: Transport Protocol (TCP/UDP), Model (pub/sub vs request/response), Overhead (rendah/tinggi), QoS Support, Security, dan Use Case terbaik. Highlight MQTT sebagai pilihan terbaik untuk IoT low-bandwidth karena overhead minimal, model pub/sub, dan dukungan QoS 0/1/2. Tambahkan diagram bandwidth comparison (bar chart) yang menunjukkan ukuran header MQTT (2 bytes minimum) vs HTTP (>100 bytes). Gunakan tabel warna dengan baris MQTT di-highlight oranye/kuning.

**Kata Kunci:** MQTT, HTTP, CoAP, WebSocket, AMQP, LoRaWAN, protokol IoT, pub/sub, overhead
**Visualisasi:** Tabel perbandingan 6 protokol, bar chart ukuran header, ikon masing-masing protokol

---

### Slide 7: Use Case IoT di Industri dan Kehidupan Nyata

**Prompt NotebookLLM:**
Buatkan slide "Aplikasi IoT di Dunia Nyata" dengan 6 kategori use case industri disertai contoh konkret. Kategori: (1) Smart Home – kendali lampu, AC, kunci pintu via smartphone; (2) Smart Factory / Industry 4.0 – monitoring mesin CNC, predictive maintenance, OEE tracking; (3) Smart Agriculture – soil moisture monitoring, irigasi otomatis, drone surveillance; (4) Smart City – manajemen traffic, smart parking, pengelolaan sampah; (5) Healthcare IoT – wearable monitor detak jantung, remote patient monitoring, smart hospital; (6) Smart Energy – smart meter PLN, solar panel monitoring, EV charging management. Untuk setiap kategori, sebutkan sensor/aktuator yang digunakan, protokol yang lazim, dan nama produk/perusahaan nyata (contoh: Philips Hue, Siemens MindSphere, John Deere Operations Center). Gunakan layout grid 2×3 dengan ikon besar.

**Kata Kunci:** Smart home, smart factory, Industry 4.0, smart agriculture, smart city, healthcare IoT, smart energy
**Visualisasi:** Grid 6 kartu use case dengan ikon besar, foto produk nyata di tiap kartu

---

### Slide 8: Tantangan dan Keamanan IoT

**Prompt NotebookLLM:**
Buatkan slide "Tantangan Utama IoT" yang membahas 5 tantangan besar dalam implementasi IoT. Tantangan 1 – Keamanan (Security): perangkat IoT sering tidak di-update firmware, rentan terhadap brute force dan MITM attack; solusi: TLS/SSL, certificate pinning, firmware OTA. Tantangan 2 – Skalabilitas: jutaan perangkat terhubung serentak; solusi: load balancer, horizontal scaling, message queue. Tantangan 3 – Interoperabilitas: beragam protokol dan vendor; solusi: standar MQTT, REST API, dan platform IoT terpadu. Tantangan 4 – Konsumsi Daya: perangkat edge harus hemat energi; solusi: deep sleep mode, LoRa, NB-IoT. Tantangan 5 – Latensi & Bandwidth: data real-time membutuhkan latensi rendah; solusi: edge computing, CDN, MQTT QoS. Gunakan layout kartu 5 kolom dengan ikon bahaya merah dan solusi hijau.

**Kata Kunci:** IoT security, skalabilitas, interoperabilitas, konsumsi daya, latensi, TLS, OTA, edge computing
**Visualisasi:** 5 kartu tantangan dengan ikon bahaya dan solusi, diagram threat model IoT sederhana

---

## BAGIAN 3 – PROTOKOL MQTT (Slide 9–14)

---

### Slide 9: Pengenalan MQTT – Sejarah dan Filosofi

**Prompt NotebookLLM:**
Buatkan slide pengenalan MQTT (Message Queuing Telemetry Transport). Jelaskan: MQTT diciptakan oleh Andy Stanford-Clark (IBM) dan Arlen Nipper (Cirrus Link) pada 1999 untuk memantau pipa minyak jarak jauh via satelit dengan bandwidth sangat terbatas. Dirilis sebagai standar terbuka OASIS pada 2013. Versi terkini: MQTT 5.0 (2019). Filosofi utama: "Publish-Subscribe" – pengirim (publisher) tidak langsung mengirim ke penerima (subscriber), melainkan melalui perantara (broker). Keunggulan: header minimal (2 byte), berjalan di atas TCP/IP, mendukung QoS 0/1/2, sangat cocok untuk perangkat dengan sumber daya terbatas (microcontroller, embedded system). Tampilkan timeline sejarah MQTT dan diagram sederhana publisher-broker-subscriber.

**Kata Kunci:** MQTT, sejarah, Andy Stanford-Clark, OASIS, publish-subscribe, broker, TCP/IP, embedded system
**Visualisasi:** Timeline sejarah MQTT (1999→2013→2019), diagram P-B-S sederhana dengan panah

---

### Slide 10: Model Publish-Subscribe MQTT Secara Detail

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan model Publish-Subscribe MQTT secara mendalam dengan diagram animatif. Komponen utama: (1) Publisher – perangkat yang mengirim data (ESP32 dengan sensor suhu); (2) Broker – server perantara yang menerima, menyimpan sementara, dan mendistribusikan pesan (Mosquitto/HiveMQ); (3) Subscriber – klien yang berlangganan topik tertentu (laptop Python, dashboard web, database service). Jelaskan alur: Publisher mempublikasikan pesan ke topik "sensor/ruang01/suhu" → Broker menerima → Semua subscriber yang subscribe topik tersebut menerima pesan secara bersamaan (decoupling). Keunggulan decoupling: publisher tidak perlu tahu alamat subscriber dan sebaliknya. Bandingkan dengan model client-server HTTP (request-response) untuk memperjelas perbedaan. Gunakan diagram alur berwarna dengan multiple publisher dan subscriber.

**Kata Kunci:** Publish, subscribe, broker, decoupling, topik, pesan, ESP32, Mosquitto, HiveMQ, client-server
**Visualisasi:** Diagram pub/sub dengan 2 publisher, 1 broker, 3 subscriber; perbandingan dengan HTTP request-response

---

### Slide 11: Topik MQTT – Struktur, Hierarki, dan Wildcard

**Prompt NotebookLLM:**
Buatkan slide yang membahas struktur topik MQTT secara lengkap. Jelaskan: topik MQTT adalah string UTF-8 case-sensitive yang dipisahkan oleh karakter "/" membentuk hierarki. Contoh hierarki: "gedung/lantai1/ruang01/sensor/suhu". Wildcard: (1) Single-level wildcard "+" menggantikan satu level, contoh: "gedung/+/ruang01/sensor/suhu" akan menangkap semua lantai; (2) Multi-level wildcard "#" menggantikan semua level di bawahnya, contoh: "gedung/lantai1/#" akan menangkap semua topik di lantai 1. Aturan penting: topik tidak boleh diawali "/" kecuali ada alasan khusus; topik yang diawali "$" adalah topik sistem internal broker (contoh: "$SYS/broker/clients/connected"). Tampilkan pohon hierarki topik untuk gedung kampus dengan 3 lantai, masing-masing 2 ruangan, dengan sensor suhu dan kelembaban. Sertakan contoh kode subscribe Python sederhana.

**Kata Kunci:** MQTT topic, hierarki, wildcard, single-level, multi-level, UTF-8, sistem topik, $SYS
**Visualisasi:** Pohon hierarki topik gedung kampus, tabel wildcard dengan contoh, snippet kode Python

---

### Slide 12: Quality of Service (QoS) MQTT – Level 0, 1, dan 2

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan tiga level Quality of Service (QoS) MQTT secara detail dengan diagram alur pengiriman pesan. QoS 0 – "At most once" (fire and forget): pesan dikirim sekali tanpa konfirmasi, kemungkinan pesan hilang, overhead paling rendah, cocok untuk data sensor yang sering dikirim (kehilangan 1 data tidak kritis). QoS 1 – "At least once": pesan dijamin terkirim minimal 1 kali, penerima mengirim PUBACK, kemungkinan pesan duplikat, cocok untuk perintah penting. QoS 2 – "Exactly once": pesan dijamin terkirim tepat 1 kali menggunakan handshake 4 langkah (PUBLISH → PUBREC → PUBREL → PUBCOMP), overhead tertinggi, cocok untuk transaksi kritis (data finansial, perintah aktuator berbahaya). Tampilkan diagram sequence/ladder untuk masing-masing QoS. Buat tabel perbandingan Use Case, Overhead, Jaminan Pengiriman untuk ketiga level.

**Kata Kunci:** QoS 0, QoS 1, QoS 2, at most once, at least once, exactly once, PUBACK, handshake, overhead
**Visualisasi:** 3 diagram sequence diagram (ladder diagram) untuk QoS 0/1/2, tabel perbandingan, ikon traffic light

---

### Slide 13: Last Will and Testament (LWT) dan Retained Message

**Prompt NotebookLLM:**
Buatkan slide yang membahas dua fitur penting MQTT: Last Will and Testament (LWT) dan Retained Message. LWT (Pesan Wasiat Terakhir): pesan yang disiapkan oleh klien saat melakukan CONNECT, dan akan dikirim otomatis oleh broker ke topik tertentu jika klien terputus secara tidak terduga (tanpa mengirim DISCONNECT). Contoh use case: ESP32 tiba-tiba kehilangan daya, broker otomatis mempublikasikan "status/esp32_01" = "OFFLINE" sehingga dashboard segera menampilkan alert. Retained Message: broker menyimpan pesan terakhir pada suatu topik; subscriber yang baru terhubung langsung mendapat pesan tersebut tanpa harus menunggu update berikutnya. Contoh: sensor suhu mengirim data setiap 30 detik dengan retain=true; ketika dashboard baru dibuka, langsung tampil nilai suhu terakhir. Tampilkan diagram sequence untuk kedua fitur. Sertakan potongan kode Python/Arduino untuk mengaktifkan LWT dan retain.

**Kata Kunci:** LWT, Last Will Testament, retained message, disconnect, CONNECT, broker, status monitoring, offline detection
**Visualisasi:** Diagram sequence LWT (ESP32 putus → broker kirim will), diagram retained message, code snippet

---

### Slide 14: Keamanan MQTT – TLS, Autentikasi, dan ACL

**Prompt NotebookLLM:**
Buatkan slide "Keamanan MQTT" yang membahas 3 lapisan keamanan. Lapisan 1 – Transport Security: enkripsi menggunakan TLS 1.2/1.3 di atas port 8883 (MQTTS) vs port 1883 yang tidak terenkripsi; proses handshake TLS; penggunaan sertifikat self-signed vs CA-signed. Lapisan 2 – Authentication (Autentikasi): username/password dalam CONNECT packet; client certificate (mutual TLS / mTLS); token-based auth (JWT via MQTT 5.0 enhanced auth). Lapisan 3 – Authorization / ACL (Access Control List): pembatasan topik per klien; contoh konfigurasi file ACL Mosquitto: "user esp32_sensor01 – topic write sensor/ruang01/#" dan "user dashboard_user – topic read sensor/#". Tampilkan perbandingan port 1883 vs 8883, diagram TLS handshake, dan contoh file konfigurasi ACL Mosquitto. Tambahkan rekomendasi keamanan untuk produksi.

**Kata Kunci:** MQTT security, TLS, MQTTS, port 8883, autentikasi, ACL, username, password, mTLS, JWT, Mosquitto
**Visualisasi:** Diagram TLS handshake, tabel port 1883 vs 8883, contoh konfigurasi ACL Mosquitto, ikon gembok

---

## BAGIAN 4 – MOSQUITTO BROKER (Slide 15–18)

---

### Slide 15: Mosquitto Broker – Pengenalan dan Instalasi

**Prompt NotebookLLM:**
Buatkan slide yang memperkenalkan Eclipse Mosquitto sebagai implementasi broker MQTT open-source paling populer. Tampilkan informasi: dikembangkan oleh Eclipse Foundation, ditulis dalam bahasa C (sangat ringan), mendukung MQTT 3.1, 3.1.1, dan 5.0, tersedia untuk Linux, Windows, macOS, dan Docker. Bandingkan Mosquitto dengan broker MQTT lain: HiveMQ (enterprise, GUI web), EMQ X / EMQX (skala besar, dashboard built-in), VerneMQ (Erlang, highly available), AWS IoT Core (cloud managed), dan CloudMQTT (SaaS). Tampilkan langkah instalasi Mosquitto di Ubuntu/Debian: (1) `sudo apt update && sudo apt install -y mosquitto mosquitto-clients`; (2) `sudo systemctl enable mosquitto && sudo systemctl start mosquitto`; (3) verifikasi: `mosquitto -v`. Sertakan output terminal yang menunjukkan Mosquitto berjalan. Tambahkan diagram posisi Mosquitto dalam arsitektur sistem.

**Kata Kunci:** Mosquitto, Eclipse Foundation, broker MQTT, HiveMQ, EMQX, VerneMQ, AWS IoT Core, instalasi, Ubuntu
**Visualisasi:** Tabel perbandingan broker, screenshot terminal instalasi, diagram posisi broker dalam arsitektur

---

### Slide 16: Konfigurasi Mosquitto – File mosquitto.conf

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan konfigurasi Mosquitto melalui file `mosquitto.conf` secara lengkap. Tampilkan contoh file konfigurasi lengkap yang mencakup: (1) Port listener: `listener 1883` untuk koneksi biasa dan `listener 8883` untuk TLS; (2) Allow anonymous: `allow_anonymous false` untuk menonaktifkan koneksi tanpa autentikasi; (3) Password file: `password_file /etc/mosquitto/passwd` – cara membuat file password dengan perintah `mosquitto_passwd -c /etc/mosquitto/passwd username`; (4) ACL file: `acl_file /etc/mosquitto/acl`; (5) Konfigurasi TLS: `cafile`, `certfile`, `keyfile`, `tls_version tlsv1.2`; (6) Logging: `log_dest file /var/log/mosquitto/mosquitto.log` dan `log_type all`; (7) Persistence: `persistence true` dan `persistence_location /var/lib/mosquitto/`. Jelaskan cara restart service: `sudo systemctl restart mosquitto`. Gunakan syntax highlighting untuk kode konfigurasi.

**Kata Kunci:** mosquitto.conf, konfigurasi, listener, allow_anonymous, password_file, ACL, TLS, persistence, logging
**Visualisasi:** Code block konfigurasi mosquitto.conf dengan syntax highlighting, diagram file structure Mosquitto

---

### Slide 17: Pengujian Mosquitto dengan mosquitto_pub dan mosquitto_sub

**Prompt NotebookLLM:**
Buatkan slide panduan pengujian Mosquitto menggunakan command-line tools bawaan: `mosquitto_pub` dan `mosquitto_sub`. Tampilkan skenario pengujian langkah demi langkah: (1) Buka Terminal 1 – Subscribe: `mosquitto_sub -h localhost -p 1883 -u "testuser" -P "password" -t "sensor/test/#" -v` (flag -v menampilkan nama topik bersama pesan); (2) Buka Terminal 2 – Publish: `mosquitto_pub -h localhost -p 1883 -u "testuser" -P "password" -t "sensor/test/suhu" -m '{"nilai": 28.5, "satuan": "Celsius", "timestamp": "2024-01-15T10:30:00Z"}'`; (3) Verifikasi pesan muncul di Terminal 1. Tampilkan juga contoh pengujian dengan QoS: `mosquitto_pub ... -q 1` dan pengujian retain: `mosquitto_pub ... -r`. Tambahkan skenario pengujian LWT dengan flag `--will-topic` dan `--will-message`. Sertakan screenshot terminal dua jendela berdampingan. Tambahkan tips troubleshooting umum.

**Kata Kunci:** mosquitto_pub, mosquitto_sub, pengujian, CLI, QoS, retain, LWT, subscribe, publish, troubleshooting
**Visualisasi:** Screenshot dua terminal berdampingan (pub dan sub), flowchart alur pengujian, tabel flag penting

---

### Slide 18: Monitoring Mosquitto – Dashboard dan Topik $SYS

**Prompt NotebookLLM:**
Buatkan slide tentang cara memonitor performa dan status Mosquitto. Topik $SYS: Mosquitto secara otomatis mempublikasikan statistik ke topik yang diawali "$SYS/". Tampilkan topik-topik penting: `$SYS/broker/clients/connected` (jumlah klien aktif), `$SYS/broker/clients/total` (total klien pernah terhubung), `$SYS/broker/messages/received` (total pesan diterima), `$SYS/broker/messages/sent` (total pesan terkirim), `$SYS/broker/load/messages/received/1min` (pesan per menit), `$SYS/broker/heap/current` (penggunaan memori), `$SYS/broker/uptime` (uptime broker). Cara subscribe semua topik $SYS: `mosquitto_sub -t '$SYS/#' -v`. Perkenalkan tool MQTT Explorer (GUI desktop cross-platform) sebagai alternatif monitoring visual: fitur utama, screenshot antarmuka. Juga perkenalkan MQTTX (GUI modern dari EMQ). Tambahkan cara membaca file log Mosquitto: `tail -f /var/log/mosquitto/mosquitto.log`.

**Kata Kunci:** $SYS, monitoring Mosquitto, MQTT Explorer, MQTTX, statistik broker, log, uptime, klien terhubung
**Visualisasi:** Screenshot MQTT Explorer, daftar topik $SYS penting, screenshot log Mosquitto, diagram monitoring stack

---

## BAGIAN 5 – DATABASE IoT (Slide 19–22)

---

### Slide 19: Kategori Database untuk IoT – Pilihan dan Pertimbangan

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan 4 kategori database yang umum digunakan dalam sistem IoT beserta pertimbangan pemilihan. Kategori 1 – Relational (SQL): PostgreSQL dan MySQL; cocok untuk data terstruktur, relasi antar entitas, laporan kompleks; ACID compliant. Kategori 2 – Document (NoSQL): MongoDB; cocok untuk data semi-terstruktur, skema fleksibel (JSON), scaling horizontal; kurang cocok untuk query relasional. Kategori 3 – Time-Series Database: InfluxDB dan TimescaleDB; dioptimalkan untuk data time-stamped, query agregasi temporal (rata-rata per jam, min/max per hari); sangat cepat untuk data sensor IoT bervolume tinggi. Kategori 4 – In-Memory / Cache: Redis; latensi ultra-rendah (sub-millisecond), cocok untuk data real-time, pub/sub built-in, session storage, rate limiting. Tampilkan decision tree pemilihan database berdasarkan kebutuhan: volume data, pola query, kebutuhan transaksi, dan latensi.

**Kata Kunci:** PostgreSQL, MongoDB, InfluxDB, Redis, TimescaleDB, database IoT, SQL, NoSQL, time-series, cache
**Visualisasi:** Decision tree pemilihan database, tabel 4 kategori, diagram CAP theorem, ikon masing-masing database

---

### Slide 20: PostgreSQL untuk IoT – Schema, Indeks, dan Partisi

**Prompt NotebookLLM:**
Buatkan slide yang membahas penggunaan PostgreSQL sebagai database utama sistem IoT. Tampilkan contoh schema database untuk sistem monitoring gedung: tabel `devices` (device_id, name, location, type, created_at), tabel `sensors` (sensor_id, device_id FK, sensor_type, unit, calibration_factor), tabel `sensor_readings` (reading_id, sensor_id FK, value, quality, recorded_at TIMESTAMPTZ) dengan indeks pada kolom (sensor_id, recorded_at). Jelaskan pentingnya: (1) TIMESTAMPTZ vs TIMESTAMP untuk zona waktu; (2) Indeks komposit (sensor_id, recorded_at DESC) untuk query time-range yang cepat; (3) Table Partitioning by range (PARTITION BY RANGE (recorded_at)) untuk mengelola tabel besar – partisi per bulan; (4) Penggunaan TimescaleDB extension untuk hypertable jika data sangat besar. Sertakan contoh query PostgreSQL: ambil rata-rata suhu per jam dalam 24 jam terakhir menggunakan `date_trunc` dan `GROUP BY`. Tambahkan perintah instalasi PostgreSQL di Ubuntu.

**Kata Kunci:** PostgreSQL, schema, TIMESTAMPTZ, indeks, partisi, TimescaleDB, hypertable, query, sensor_readings
**Visualisasi:** ERD (Entity Relationship Diagram) tiga tabel, code block SQL schema dan query, diagram partisi tabel

---

### Slide 21: MongoDB dan InfluxDB untuk IoT – Kapan Menggunakannya

**Prompt NotebookLLM:**
Buatkan slide yang membandingkan MongoDB dan InfluxDB dalam konteks IoT. MongoDB – Use Case IoT: menyimpan konfigurasi perangkat (dokumen JSON fleksibel), event logs, alert history, dan metadata sensor yang sering berubah skemanya. Tampilkan contoh dokumen MongoDB untuk sensor reading: `{ "_id": ObjectId, "device_id": "esp32_01", "location": {"building": "A", "floor": 2, "room": "Lab01"}, "readings": [{"type": "temperature", "value": 28.5, "unit": "C"}, {"type": "humidity", "value": 65.2, "unit": "%"}], "timestamp": ISODate, "firmware": "v2.1.0" }`. InfluxDB – Use Case IoT: penyimpanan data time-series bervolume sangat tinggi (jutaan titik data per hari), query agregasi temporal, retention policy otomatis (hapus data lama), downsampling. Tampilkan contoh InfluxDB Line Protocol: `sensor_data,device=esp32_01,room=Lab01 temperature=28.5,humidity=65.2 1705310000000000000`. Bandingkan query rate (write throughput): InfluxDB vs PostgreSQL vs MongoDB.

**Kata Kunci:** MongoDB, InfluxDB, dokumen JSON, Line Protocol, retention policy, downsampling, time-series, write throughput
**Visualisasi:** Contoh dokumen MongoDB, contoh Line Protocol InfluxDB, bar chart write throughput perbandingan, diagram kapan pakai masing-masing

---

### Slide 22: Redis sebagai Cache dan Message Broker IoT

**Prompt NotebookLLM:**
Buatkan slide yang membahas Redis dalam konteks sistem IoT. Redis berperan sebagai: (1) Cache Layer: menyimpan nilai sensor terakhir (latest value cache) dengan TTL, sehingga dashboard tidak perlu query database utama setiap request – perintah: `SET sensor:esp32_01:temperature 28.5 EX 60`; (2) Pub/Sub Internal: Redis Pub/Sub untuk komunikasi antar service backend – `PUBLISH channel:alerts "Suhu Lab01 > 30°C"`; (3) Rate Limiting: mencegah ESP32 mengirim data terlalu sering – `INCR ratelimit:esp32_01:minute`; (4) Session Store: menyimpan session pengguna dashboard dengan JWT; (5) Job Queue: menggunakan Redis Streams atau Bull (Node.js) untuk antrian proses data berat. Tampilkan arsitektur cache-aside pattern: request dashboard → Redis (cache hit) atau Redis (cache miss) → query PostgreSQL → update Redis → return data. Sertakan contoh perintah Redis CLI dan snippet Python dengan library `redis-py`. Tambahkan perbandingan latensi Redis (< 1ms) vs PostgreSQL (1-10ms) vs MongoDB (1-5ms).

**Kata Kunci:** Redis, cache, pub/sub, rate limiting, session store, Redis Streams, cache-aside, latensi, TTL, redis-py
**Visualisasi:** Diagram cache-aside pattern, tabel latensi perbandingan, contoh perintah Redis CLI, diagram Redis Streams

---

## BAGIAN 6 – ESP32 EDGE DEVICE (Slide 23–26)

---

### Slide 23: Pengenalan ESP32 – Spesifikasi dan Ekosistem

**Prompt NotebookLLM:**
Buatkan slide pengenalan ESP32 sebagai microcontroller untuk IoT. Tampilkan spesifikasi teknis lengkap ESP32 (model ESP32-WROOM-32D): CPU Xtensa LX6 dual-core 240 MHz, RAM 520 KB SRAM + 4 MB Flash, konektivitas WiFi 802.11 b/g/n (2.4 GHz) + Bluetooth Classic 4.2 + BLE 4.2, tegangan operasi 3.3V (input 5V via USB), 34 GPIO pins, 18 ADC channels 12-bit, 2 DAC 8-bit, 3 UART, 2 SPI, 2 I2C, 16 PWM channels, harga terjangkau (~$3-5 USD). Bandingkan dengan Arduino Uno (tidak ada WiFi/BT built-in), ESP8266 (single-core, lebih terbatas), Raspberry Pi (Linux SBC, konsumsi daya lebih tinggi). Tampilkan pinout diagram ESP32-WROOM-32. Jelaskan ekosistem development: Arduino IDE, PlatformIO, ESP-IDF, MicroPython. Tambahkan foto/gambar modul ESP32 DEVKIT.

**Kata Kunci:** ESP32, ESP32-WROOM-32D, Xtensa LX6, WiFi, Bluetooth, GPIO, ADC, DAC, Arduino, PlatformIO, MicroPython
**Visualisasi:** Pinout diagram ESP32, tabel spesifikasi, perbandingan dengan Arduino/ESP8266/RPi, foto modul

---

### Slide 24: PlatformIO – Setup dan Struktur Proyek

**Prompt NotebookLLM:**
Buatkan slide panduan setup PlatformIO untuk pengembangan ESP32. Jelaskan PlatformIO: IDE extension untuk VS Code (dan IDE lain) yang menyediakan manajemen library, multi-platform support, build system otomatis, serial monitor, dan debugger. Langkah instalasi: (1) Install VS Code; (2) Install extension PlatformIO IDE dari VS Code Marketplace; (3) Tunggu proses instalasi (10-15 menit pertama kali); (4) Klik ikon PlatformIO di sidebar. Membuat proyek baru: New Project → Name: "esp32_mqtt_sensor" → Board: "Espressif ESP32 Dev Module" → Framework: "Arduino". Tampilkan struktur folder proyek PlatformIO yang dihasilkan: `.pio/`, `include/`, `lib/`, `src/main.cpp`, `platformio.ini`. Tampilkan contoh `platformio.ini` untuk ESP32 dengan library MQTT: `[env:esp32dev]`, `platform = espressif32`, `board = esp32dev`, `framework = arduino`, `lib_deps = knolleary/PubSubClient@^2.8.0, bblanchon/ArduinoJson@^6.21.0`. Jelaskan cara upload code: Ctrl+Alt+U atau tombol Upload.

**Kata Kunci:** PlatformIO, VS Code, ESP32, platformio.ini, struktur proyek, PubSubClient, ArduinoJson, upload, build
**Visualisasi:** Screenshot VS Code dengan PlatformIO extension, struktur folder proyek, contoh platformio.ini, tombol build/upload

---

### Slide 25: Koneksi WiFi dan MQTT pada ESP32 – Inisialisasi

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan proses inisialisasi koneksi WiFi dan MQTT pada ESP32 menggunakan library PubSubClient. Tampilkan kode C++ lengkap untuk fungsi `setup_wifi()`: include library WiFi.h, deklarasi SSID dan password, pemanggilan `WiFi.begin()`, loop menunggu status `WL_CONNECTED` dengan delay 500ms, print IP address setelah terhubung. Tampilkan fungsi `reconnect()`: mengecek `client.connected()`, jika false lakukan loop percobaan `client.connect("ESP32Client", mqtt_user, mqtt_pass)` dengan LWT: `client.connect("ESP32Client", mqtt_user, mqtt_pass, "status/esp32_01", 1, true, "OFFLINE")`, jika berhasil publish status "ONLINE" dan subscribe topik perintah `"cmd/esp32_01/#"`, jika gagal tunggu 5 detik. Sertakan penjelasan parameter `client.connect()` satu per satu. Tampilkan diagram state machine koneksi: DISCONNECTED → CONNECTING_WIFI → WIFI_CONNECTED → CONNECTING_MQTT → MQTT_CONNECTED → OPERATING. Gunakan syntax highlighting C++.

**Kata Kunci:** WiFi.h, PubSubClient, setup_wifi, reconnect, LWT, MQTT connect, state machine, ESP32, C++
**Visualisasi:** Code block C++ dengan highlighting, diagram state machine koneksi, flowchart fungsi reconnect

---

### Slide 26: Membaca Sensor dan Manajemen Waktu pada ESP32

**Prompt NotebookLLM:**
Buatkan slide tentang pembacaan sensor pada ESP32 untuk sistem IoT, dengan fokus pada sensor DHT22 (suhu dan kelembaban) dan sensor analog (potensiometer sebagai simulasi sensor). Tampilkan: (1) Kode pembacaan DHT22 menggunakan library `DHT.h`: inisialisasi objek `DHT dht(DHT_PIN, DHT22)`, fungsi baca `float suhu = dht.readTemperature()`, validasi nilai dengan `isnan()`, error handling jika pembacaan gagal; (2) Manajemen waktu non-blocking menggunakan `millis()` (bukan `delay()`) untuk mengirim data setiap 5 detik: deklarasi `unsigned long lastSendTime = 0` dan `const long sendInterval = 5000`, pengecekan `if (millis() - lastSendTime >= sendInterval)`; (3) Pembentukan payload JSON menggunakan ArduinoJson: buat `StaticJsonDocument<200> doc`, isi field `doc["device_id"]`, `doc["suhu"]`, `doc["kelembaban"]`, `doc["timestamp"]` (dari millis), serialize ke string, publish via `client.publish()`; (4) Penambahan NTP time sync untuk timestamp akurat: `configTime(7*3600, 0, "pool.ntp.org")`. Gunakan syntax highlighting.

**Kata Kunci:** DHT22, sensor, millis, non-blocking, ArduinoJson, JSON payload, NTP, timestamp, PubSubClient publish
**Visualisasi:** Code block C++ lengkap, diagram timing millis() vs delay(), skema wiring DHT22 ke ESP32

---

## BAGIAN 7 – KODE MQTT ESP32 (Slide 27–29)

---

### Slide 27: Kode Lengkap ESP32 – Publish Data Sensor

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan kode program C++ lengkap dan siap-pakai untuk ESP32 yang membaca sensor DHT22 dan mempublikasikan data ke broker MQTT setiap 5 detik dalam format JSON. Struktur kode: (1) Include: `<WiFi.h>`, `<PubSubClient.h>`, `<DHT.h>`, `<ArduinoJson.h>`; (2) Definisi konstanta: SSID, password, MQTT_SERVER, MQTT_PORT 1883, MQTT_USER, MQTT_PASS, MQTT_TOPIC "sensor/esp32_01/dht22", DHT_PIN 4, DHT_TYPE DHT22; (3) Inisialisasi objek: `WiFiClient espClient`, `PubSubClient client(espClient)`, `DHT dht(DHT_PIN, DHT_TYPE)`; (4) Fungsi `setup_wifi()`, `reconnect()`, `publishSensorData()`; (5) Fungsi `setup()`: inisialisasi Serial 115200, DHT, WiFi, set server `client.setServer()`, set callback; (6) Fungsi `loop()`: reconnect jika perlu, `client.loop()`, cek interval millis, panggil `publishSensorData()`. Payload JSON contoh: `{"device":"esp32_01","suhu":28.5,"kelembaban":65.2,"rssi":-67,"uptime":12345}`. Tambahkan komentar penjelasan di baris-baris penting.

**Kata Kunci:** ESP32, C++, DHT22, MQTT publish, JSON, PubSubClient, WiFiClient, ArduinoJson, loop, setup
**Visualisasi:** Full code block dengan syntax highlighting dan komentar, output Serial Monitor, diagram data flow

---

### Slide 28: Kode ESP32 – Subscribe dan Eksekusi Perintah (Aktuator)

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan kode ESP32 untuk menerima perintah dari broker MQTT dan mengeksekusi aksi pada aktuator (LED, relay). Tampilkan: (1) Fungsi callback MQTT `void callback(char* topic, byte* payload, unsigned int length)`: konversi payload byte ke String, parse JSON menggunakan ArduinoJson, switch/case berdasarkan field "command": "LED_ON" → `digitalWrite(LED_PIN, HIGH)`, "LED_OFF" → `digitalWrite(LED_PIN, LOW)`, "BLINK" → efek blink sebanyak `doc["times"].as<int>()` kali; (2) Subscribe topik perintah: `client.subscribe("cmd/esp32_01/aktuator")` dan `client.subscribe("cmd/broadcast/#")` (menerima broadcast ke semua perangkat); (3) Format JSON pesan perintah dari backend: `{"command": "LED_ON", "duration": 5000, "source": "dashboard_user1"}`; (4) Publish acknowledgment setelah eksekusi: `client.publish("ack/esp32_01/aktuator", "{\"status\":\"OK\",\"executed\":\"LED_ON\"}")`; (5) Penanganan error: command tidak dikenal, JSON malformed. Sertakan diagram alur callback MQTT.

**Kata Kunci:** MQTT subscribe, callback, aktuator, LED, relay, command, ArduinoJson parse, acknowledgment, broadcast
**Visualisasi:** Code block callback dengan syntax highlighting, diagram alur callback, tabel format pesan perintah

---

### Slide 29: Best Practices Pemrograman ESP32 untuk IoT

**Prompt NotebookLLM:**
Buatkan slide "Best Practices ESP32 IoT" yang merangkum praktik terbaik pemrograman ESP32 untuk sistem IoT produksi. Topik 1 – Manajemen Koneksi: selalu implementasikan auto-reconnect dengan exponential backoff (mulai 1s, maksimum 64s) untuk mencegah flooding broker; gunakan `client.setKeepAlive(60)`. Topik 2 – Keamanan: simpan credentials (SSID, password, MQTT user/pass) di file `credentials.h` yang masuk `.gitignore`; pertimbangkan penggunaan SPIFFS/LittleFS untuk menyimpan konfigurasi dinamis. Topik 3 – Watchdog Timer: aktifkan hardware watchdog `esp_task_wdt_init(30, true)` untuk auto-reset jika firmware hang. Topik 4 – Penghematan Daya: gunakan `esp_deep_sleep_start()` untuk baterai; wake-up periodik setiap 5 menit, kirim data, kembali sleep. Topik 5 – OTA (Over-the-Air Update): implementasikan `ArduinoOTA` untuk update firmware tanpa kabel. Topik 6 – Logging: gunakan macro `DEBUG_PRINT` yang bisa dinonaktifkan saat produksi. Tampilkan diagram siklus hidup firmware ESP32.

**Kata Kunci:** Best practices, ESP32, reconnect, exponential backoff, watchdog, deep sleep, OTA, SPIFFS, credentials, keamanan
**Visualisasi:** Diagram exponential backoff, diagram siklus deep sleep, flowchart OTA update, tabel checklist best practices

---

## BAGIAN 8 – PYTHON LAPTOP EDGE DEVICE (Slide 30–32)

---

### Slide 30: Python sebagai Edge Device – paho-mqtt Library

**Prompt NotebookLLM:**
Buatkan slide pengenalan penggunaan laptop/PC dengan Python sebagai edge device IoT menggunakan library `paho-mqtt`. Jelaskan skenario: laptop berfungsi sebagai data aggregator yang menerima data dari multiple ESP32, melakukan preprocessing (filtering, validasi, agregasi), kemudian meneruskan ke database atau backend server. Instalasi: `pip install paho-mqtt python-dotenv requests`. Contoh kode Python subscriber lengkap: import `paho.mqtt.client as mqtt`, definisi callback `on_connect(client, userdata, flags, rc)` yang subscribe topik saat terhubung, callback `on_message(client, userdata, msg)` yang parse JSON payload dan print data terstruktur, inisialisasi `client = mqtt.Client(client_id="python_edge_01")`, set credentials `client.username_pw_set(user, pass)`, set LWT, `client.connect(broker, port, keepalive=60)`, `client.loop_forever()`. Jelaskan perbedaan `loop_forever()` vs `loop_start()` (blocking vs non-blocking). Tambahkan contoh penggunaan `python-dotenv` untuk konfigurasi dari file `.env`.

**Kata Kunci:** paho-mqtt, Python, subscriber, on_connect, on_message, loop_forever, loop_start, dotenv, edge device, preprocessing
**Visualisasi:** Code block Python dengan highlighting, diagram posisi Python edge dalam arsitektur, screenshot terminal output

---

### Slide 31: Python MQTT Publisher dan Data Processing

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan kode Python untuk mempublikasikan data dan melakukan data processing. Tampilkan: (1) Fungsi publisher dengan QoS: `client.publish(topic, payload, qos=1, retain=False)` dan penanganan return code `MQTTMessageInfo`; (2) Data processing pipeline dalam `on_message`: parsing JSON → validasi range nilai (suhu harus antara -40°C hingga 85°C untuk DHT22) → kalkulasi rata-rata bergerak (moving average) menggunakan `collections.deque(maxlen=10)` → deteksi anomali dengan z-score sederhana → kirim ke database via REST API jika data valid, atau publish ke topik "alert/anomaly" jika anomali terdeteksi; (3) Penggunaan threading untuk multiple subscriber: `loop_start()` + `threading.Thread` untuk proses database insert paralel; (4) Contoh integrasi dengan `requests` library untuk POST data ke backend REST API: `requests.post(API_URL, json=payload, headers={"Authorization": "Bearer "+token})`; (5) Logging ke file menggunakan Python `logging` module. Sertakan contoh output log.

**Kata Kunci:** paho-mqtt publish, data processing, validasi, moving average, anomaly detection, threading, requests, REST API, logging
**Visualisasi:** Code block Python, diagram data processing pipeline, flowchart anomaly detection, diagram threading model

---

### Slide 32: Python MQTT – Skenario Lengkap: Simulasi Sensor Virtual

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan skenario praktis: menggunakan Python untuk mensimulasikan sensor virtual (virtual sensor) yang mengirim data ke broker MQTT – berguna untuk testing backend tanpa hardware fisik. Tampilkan kode Python `virtual_sensor.py`: (1) Import: `paho.mqtt.client`, `json`, `time`, `random`, `math`, `datetime`; (2) Fungsi `generate_sensor_data(device_id, sensor_count)`: menghasilkan data suhu realistis menggunakan gelombang sinus + noise random (simulasi fluktuasi siang-malam: `28 + 5 * math.sin(2 * math.pi * hour / 24) + random.gauss(0, 0.5)`), kelembaban berkorelasi terbalik dengan suhu; (3) Loop utama: kirim data setiap 2 detik untuk 5 device virtual (`esp32_sim_01` s/d `esp32_sim_05`) secara paralel menggunakan `asyncio` atau `threading`; (4) Simulasi event abnormal: secara acak (probabilitas 5%) kirim nilai di luar range normal untuk testing alert system. Tambahkan penjelasan penggunaan virtual sensor dalam tahap development dan testing sebelum deploy hardware. Sertakan contoh output JSON.

**Kata Kunci:** virtual sensor, simulasi, Python, MQTT, gelombang sinus, random noise, asyncio, testing, development, payload JSON
**Visualisasi:** Code block Python, grafik simulasi data suhu sinus+noise, diagram 5 virtual sensor, contoh output JSON

---

## BAGIAN 9 – BACKEND (Slide 33–35)

---

### Slide 33: Arsitektur Backend IoT – REST API dan WebSocket

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan peran dan arsitektur backend dalam sistem IoT. Backend berfungsi sebagai: (1) MQTT Subscriber Internal: menerima data dari broker, menyimpan ke database; (2) REST API Server: menyediakan endpoint untuk frontend dan mobile app (GET data historis, POST konfigurasi perangkat, PUT threshold alert, DELETE device); (3) WebSocket Server: push notifikasi real-time ke frontend tanpa polling (efisiensi tinggi); (4) Authentication Server: mengelola JWT token, user management, API key; (5) Alert Engine: evaluasi rule-based alert (suhu > threshold → kirim email/SMS/WhatsApp). Tampilkan tabel perbandingan 4 pilihan backend: Spring Boot (Java, enterprise, annotation-driven, Maven/Gradle), FastAPI (Python, async, auto-docs Swagger, pydantic validation), Node.js/Express (JavaScript, event-driven, npm ecosystem, Socket.IO untuk WebSocket), ASP.NET Core C# (Microsoft, performance tinggi, Entity Framework). Bandingkan: Language, Performance, Learning Curve, Ecosystem, Docker image size. Rekomendasikan FastAPI untuk pembelajaran cepat dan Node.js untuk WebSocket real-time.

**Kata Kunci:** Backend IoT, REST API, WebSocket, MQTT subscriber, JWT, Spring Boot, FastAPI, Node.js, C#, alert engine
**Visualisasi:** Diagram arsitektur backend lengkap, tabel perbandingan 4 backend framework, diagram alur data MQTT→Backend→Database

---

### Slide 34: FastAPI Backend – Implementasi Endpoint IoT

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan implementasi backend IoT menggunakan FastAPI (Python). Tampilkan struktur proyek FastAPI: `main.py`, `routers/`, `models/`, `schemas/`, `database.py`, `mqtt_handler.py`, `requirements.txt`. Tampilkan kode contoh endpoint penting: (1) `GET /api/v1/devices` – daftar semua perangkat terdaftar; (2) `GET /api/v1/sensors/{device_id}/readings?from=&to=&limit=100` – ambil data sensor dengan filter waktu dan pagination; (3) `POST /api/v1/devices/{device_id}/command` – kirim perintah ke ESP32 via `client.publish()` paho-mqtt; (4) `GET /api/v1/sensors/{device_id}/latest` – ambil data terbaru dari Redis cache. Tampilkan integrasi MQTT dalam FastAPI menggunakan `asyncio` dan `aiomqtt` atau `paho-mqtt` dengan `BackgroundTask`. Tampilkan contoh model Pydantic untuk validasi request body dan response. Sertakan contoh `requirements.txt`: `fastapi`, `uvicorn`, `paho-mqtt`, `asyncpg`, `redis`, `pydantic`. Tambahkan screenshot Swagger UI auto-generated.

**Kata Kunci:** FastAPI, Pydantic, endpoint, MQTT, asyncio, aiomqtt, Redis, PostgreSQL, Swagger UI, REST API, Python
**Visualisasi:** Struktur proyek FastAPI, code block endpoint, screenshot Swagger UI, diagram request-response flow

---

### Slide 35: Node.js Backend dengan Socket.IO untuk Real-Time Dashboard

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan implementasi backend Node.js/Express dengan Socket.IO untuk sistem IoT real-time. Tampilkan paket yang dibutuhkan: `npm install express socket.io mqtt pg redis dotenv cors jsonwebtoken`. Tampilkan alur kerja: MQTT message diterima oleh `mqtt.connect()` callback → data disimpan ke PostgreSQL via `pg` pool → data di-cache di Redis → data di-emit ke semua client WebSocket via `io.emit('sensor_update', data)`. Tampilkan kode contoh: (1) Setup Express server dan Socket.IO: `const io = require('socket.io')(httpServer, {cors: {origin: "*"}})`; (2) MQTT subscriber yang forward ke WebSocket: dalam `client.on('message', ...)` emit ke `io.to(room).emit('data', parsedPayload)`; (3) REST endpoint untuk data historis dengan query PostgreSQL menggunakan parameterized query untuk mencegah SQL injection; (4) JWT middleware untuk proteksi endpoint; (5) Event Socket.IO dari client: `socket.on('subscribe_device', deviceId)` → join room `deviceId`. Tambahkan diagram arsitektur lengkap Node.js + Socket.IO + MQTT.

**Kata Kunci:** Node.js, Express, Socket.IO, WebSocket, MQTT, real-time, PostgreSQL, Redis, JWT, room, emit, SQL injection
**Visualisasi:** Diagram arsitektur Node.js+Socket.IO+MQTT, code block JavaScript, diagram alur event WebSocket

---

## BAGIAN 10 – FRONTEND (Slide 36–38)

---

### Slide 36: Arsitektur Frontend IoT Dashboard – Pilihan Framework

**Prompt NotebookLLM:**
Buatkan slide yang membahas pilihan framework frontend untuk membangun dashboard IoT. Tampilkan perbandingan 3 framework: Vue.js 3 (Composition API, Pinia state management, Vite build tool, learning curve rendah-menengah, cocok untuk tim kecil dan rapid development), React 18 (JSX, hooks, Redux/Zustand state management, Create React App/Vite, learning curve menengah, ekosistem terbesar, backing Meta), Angular 17 (TypeScript-first, built-in DI, RxJS observable, learning curve tinggi, cocok untuk tim enterprise besar, backing Google). Komponen UI yang dibutuhkan dashboard IoT: (1) Real-time chart (line chart, gauge chart) – library: Chart.js, ECharts, atau ApexCharts; (2) Data table dengan sorting/filtering – library: AG Grid, TanStack Table; (3) Map view untuk lokasi sensor – library: Leaflet.js, Mapbox; (4) Alert notification – library: Toastify, Vue-Toastification. Rekomendasikan Vue.js + ECharts + Tailwind CSS untuk pemula. Tampilkan screenshot contoh dashboard IoT modern.

**Kata Kunci:** Vue.js, React, Angular, dashboard IoT, Chart.js, ECharts, ApexCharts, Tailwind CSS, real-time chart, Pinia, Redux
**Visualisasi:** Tabel perbandingan 3 framework, screenshot dashboard IoT, daftar library chart, diagram komponen dashboard

---

### Slide 37: Vue.js 3 – Implementasi Dashboard Real-Time dengan Socket.IO

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan implementasi komponen Vue.js 3 untuk dashboard IoT real-time menggunakan Socket.IO dan ECharts. Tampilkan: (1) Setup proyek: `npm create vite@latest iot-dashboard -- --template vue`, `npm install socket.io-client echarts vue-echarts pinia axios`; (2) Store Pinia untuk state management sensor: `useSensorStore()` dengan state `devices[]`, `latestReadings{}`, `alerts[]`, action `connectSocket()` yang buat koneksi Socket.IO, action `fetchHistoricalData(deviceId, hours)` yang call REST API; (3) Komponen `SensorCard.vue`: tampilkan nilai suhu/kelembaban terbaru, indikator online/offline, animasi pulse jika data baru diterima; (4) Komponen `RealtimeChart.vue` menggunakan vue-echarts: line chart dengan sliding window 60 titik data terakhir, update saat Socket.IO event `sensor_update` diterima, format timestamp di X-axis; (5) Event handling Socket.IO dalam `onMounted()` lifecycle hook. Sertakan screenshot tampilan dashboard. Gunakan Composition API `<script setup>`.

**Kata Kunci:** Vue.js 3, Composition API, Pinia, Socket.IO client, ECharts, vue-echarts, real-time chart, SensorCard, Vite
**Visualisasi:** Code block Vue.js dengan highlighting, screenshot komponen dashboard, diagram alur Socket.IO event ke chart

---

### Slide 38: React – Implementasi Dashboard dengan Hooks dan Context

**Prompt NotebookLLM:**
Buatkan slide yang menampilkan implementasi dashboard IoT menggunakan React 18 dengan hooks modern. Tampilkan: (1) Setup proyek: `npx create-react-app iot-dashboard` atau `npm create vite@latest iot-dashboard -- --template react`, `npm install socket.io-client recharts axios react-query zustand`; (2) Custom hook `useMQTTSocket(brokerUrl, deviceIds)`: menggunakan `useEffect` untuk setup/teardown Socket.IO connection, return `{ latestData, isConnected, error }`; (3) Custom hook `useSensorHistory(deviceId, timeRange)` menggunakan React Query: fetch data historis dari REST API dengan caching otomatis, staleTime, dan refetchInterval; (4) Komponen `<LiveChart />` menggunakan Recharts: `<LineChart>` dengan `<Line>` untuk suhu dan kelembaban, `<Tooltip>` custom, `<Legend>`, `<ReferenceLine>` untuk threshold; (5) Context API untuk tema dan autentikasi. Sertakan screenshot dashboard React. Tampilkan juga contoh penggunaan Tailwind CSS utility classes dalam JSX.

**Kata Kunci:** React 18, hooks, useEffect, custom hook, React Query, Zustand, Socket.IO, Recharts, Tailwind CSS, JSX, context
**Visualisasi:** Code block React/JSX dengan highlighting, screenshot dashboard React, diagram hooks lifecycle, struktur komponen

---

## BAGIAN 11 – DEPLOYMENT (Slide 39–41)

---

### Slide 39: PM2 – Process Manager untuk Node.js dan Python Backend

**Prompt NotebookLLM:**
Buatkan slide yang menjelaskan penggunaan PM2 (Process Manager 2) untuk mengelola proses backend di server produksi. Instalasi: `npm install -g pm2`. Perintah dasar: `pm2 start app.js --name "iot-backend"` (Node.js) atau `pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name "iot-fastapi"` (FastAPI Python). Fitur-fitur utama PM2: (1) Auto-restart jika crash; (2) Load balancing dengan cluster mode: `pm2 start app.js -i max` (spawn sesuai jumlah CPU core); (3) Auto-start saat server reboot: `pm2 startup` + `pm2 save`; (4) Log management: `pm2 logs iot-backend --lines 100`; (5) Monitoring real-time: `pm2 monit` (CPU, memory, restart count); (6) Zero-downtime reload: `pm2 reload iot-backend`. Tampilkan contoh file ekosistem PM2 `ecosystem.config.js` dengan konfigurasi multiple apps (backend + MQTT bridge + worker). Sertakan screenshot `pm2 list` dan `pm2 monit`. Tambahkan perbandingan PM2 vs systemd.

**Kata Kunci:** PM2, process manager, Node.js, Python, cluster mode, auto-restart, startup, ecosystem.config.js, monit, zero-downtime
**Visualisasi:** Screenshot `pm2 list`, screenshot `pm2 monit`, contoh ecosystem.config.js, diagram cluster mode

---

### Slide 40: Nginx – Reverse Proxy, Static File Serving, dan SSL Termination

**Prompt NotebookLLM:**
Buatkan slide yang membahas konfigurasi Nginx sebagai reverse proxy untuk sistem IoT. Instalasi: `sudo apt install nginx`. Peran Nginx dalam arsitektur: (1) Reverse Proxy: meneruskan request HTTP ke backend (Node.js port 3000, FastAPI port 8000); (2) Static File Serving: menyajikan file build frontend (Vue/React dist folder); (3) SSL Termination: menangani HTTPS di port 443, meneruskan HTTP ke backend; (4) WebSocket Proxy: konfigurasi khusus untuk Socket.IO dengan header `Upgrade` dan `Connection`; (5) Rate Limiting: `limit_req_zone` untuk mencegah abuse API. Tampilkan contoh konfigurasi Nginx lengkap `/etc/nginx/sites-available/iot-app`: `server { listen 443 ssl; server_name iot.contoh.com; ssl_certificate /etc/letsencrypt/live/...; location /api { proxy_pass http://localhost:8000; } location /socket.io { proxy_pass http://localhost:3000; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; } location / { root /var/www/iot-frontend/dist; try_files $uri /index.html; } }`. Sertakan diagram arsitektur dengan Nginx sebagai gateway.

**Kata Kunci:** Nginx, reverse proxy, SSL termination, WebSocket, rate limiting, static files, proxy_pass, Upgrade header, HTTPS
**Visualisasi:** Diagram arsitektur Nginx sebagai gateway, code block konfigurasi Nginx, tabel peran Nginx

---

### Slide 41: Certbot (Let's Encrypt) dan ngrok untuk HTTPS dan Tunneling

**Prompt NotebookLLM:**
Buatkan slide yang membahas dua solusi HTTPS: Certbot untuk domain publik dan ngrok untuk development/demo. Certbot + Let's Encrypt: (1) Instalasi: `sudo apt install certbot python3-certbot-nginx`; (2) Generate sertifikat: `sudo certbot --nginx -d iot.contoh.com -d www.iot.contoh.com`; (3) Proses verifikasi domain (HTTP-01 challenge) dan cara kerjanya; (4) Auto-renewal: `sudo certbot renew --dry-run`, cron job otomatis di `/etc/cron.d/certbot`; (5) Pengecekan: `sudo certbot certificates`. Konfigurasi MQTTS dengan sertifikat Let's Encrypt di Mosquitto: tambahkan path `cafile`, `certfile`, `keyfile` di `mosquitto.conf`. ngrok untuk Development/Demo: (1) Instalasi dan setup: `snap install ngrok`, daftar akun gratis di ngrok.com, `ngrok authtoken`; (2) Expose backend: `ngrok http 8000` → dapatkan URL publik `https://xxxx.ngrok.io`; (3) Expose MQTT: `ngrok tcp 1883`; (4) Konfigurasi ngrok.yml untuk multiple tunnels. Jelaskan kapan pakai certbot vs ngrok. Tambahkan peringatan: ngrok gratis = URL berubah setiap restart.

**Kata Kunci:** Certbot, Let's Encrypt, HTTPS, SSL certificate, auto-renewal, ngrok, tunneling, HTTP-01 challenge, MQTTS, domain
**Visualisasi:** Diagram proses certbot challenge, screenshot ngrok dashboard, diagram perbandingan certbot vs ngrok, flowchart auto-renewal

---

## BAGIAN 12 – ARSITEKTUR LENGKAP (Slide 42–43)

---

### Slide 42: Arsitektur End-to-End Sistem IoT Lengkap – Diagram Master

**Prompt NotebookLLM:**
Buatkan slide "Arsitektur Sistem IoT End-to-End" yang menampilkan diagram arsitektur lengkap seluruh komponen yang telah dipelajari dalam Modul 04 dalam satu diagram master yang komprehensif. Diagram harus menunjukkan alur data dari sumber hingga tampilan: Layer 1 (Physical/Edge): ESP32 #1 dengan DHT22 dan ESP32 #2 dengan sensor analog → terhubung via WiFi ke router; Python Laptop Edge Device → terhubung ke jaringan lokal. Layer 2 (Connectivity/Broker): Mosquitto Broker (server lokal/VPS) pada port 1883 (internal) dan 8883 (TLS eksternal); MQTT Explorer sebagai monitoring. Layer 3 (Processing/Backend): FastAPI/Node.js backend (PM2) yang subscribe MQTT → PostgreSQL database untuk data historis → Redis cache untuk data terkini → InfluxDB opsional untuk time-series. Layer 4 (Presentation/Frontend): Nginx reverse proxy + SSL (certbot/ngrok) → Vue.js/React dashboard → Socket.IO WebSocket untuk real-time → REST API untuk data historis. Layer 5 (External): Alert via email/Telegram bot → Mobile app. Tandai alur data dengan panah berwarna berbeda (publish=biru, subscribe=hijau, REST=oranye, WebSocket=merah, database=ungu).

**Kata Kunci:** Arsitektur end-to-end, diagram master, IoT stack, ESP32, Mosquitto, FastAPI, PostgreSQL, Redis, Vue.js, Nginx
**Visualisasi:** Diagram arsitektur master full-page, legenda warna alur data, tabel teknologi per layer

---

### Slide 43: Skenario Demo Langkah demi Langkah

**Prompt NotebookLLM:**
Buatkan slide "Panduan Demo Praktikum" yang memberikan panduan langkah-demi-langkah untuk menjalankan demo sistem IoT lengkap selama sesi praktikum. Urutan langkah: (1) Mulai Mosquitto broker: `sudo systemctl start mosquitto`, verifikasi dengan `mosquitto_sub -t '$SYS/#' -v`; (2) Jalankan database: `sudo systemctl start postgresql redis-server`; (3) Jalankan backend: `cd backend && pm2 start ecosystem.config.js`; (4) Build dan serve frontend: `cd frontend && npm run build && pm2 start "npx serve -s dist -l 3001" --name "frontend"`; (5) Upload firmware ke ESP32 via PlatformIO: verifikasi Serial Monitor menampilkan "MQTT Connected"; (6) Jalankan virtual sensor Python (jika tidak ada hardware): `python virtual_sensor.py`; (7) Buka browser ke `http://localhost:3001` atau URL ngrok, verifikasi data real-time muncul; (8) Test publish perintah ke ESP32: `mosquitto_pub -t "cmd/esp32_01/aktuator" -m '{"command":"LED_ON"}'`, verifikasi LED menyala. Tampilkan dalam format numbered checklist dengan ikon terminal/browser/hardware.

**Kata Kunci:** Demo, panduan, langkah demi langkah, checklist, praktikum, troubleshooting, verifikasi, startup order
**Visualisasi:** Checklist 8 langkah bergambar, diagram startup order dependencies, tabel troubleshooting umum

---

## BAGIAN 13 – PENUTUP (Slide 44–45)

---

### Slide 44: Ringkasan Modul dan Kompetensi yang Dicapai

**Prompt NotebookLLM:**
Buatkan slide ringkasan Modul 04 yang merangkum seluruh materi dan kompetensi yang telah dipelajari. Buat dalam format visual mind map atau diagram radial dengan "Sistem IoT End-to-End" di tengah, dan 8 cabang utama: (1) Dasar IoT: arsitektur 4 layer, protokol, use case; (2) MQTT: pub/sub, QoS, LWT, retain, keamanan; (3) Mosquitto: instalasi, konfigurasi, monitoring; (4) Database IoT: PostgreSQL, MongoDB, InfluxDB, Redis; (5) ESP32: PlatformIO, sensor, publish/subscribe, best practices; (6) Python Edge: paho-mqtt, data processing, virtual sensor; (7) Backend: FastAPI/Node.js, REST API, WebSocket, JWT; (8) Deployment: PM2, Nginx, certbot, ngrok. Di bawah diagram, tampilkan tabel "Apa yang Bisa Anda Bangun Setelah Modul Ini": sistem monitoring suhu gedung, sistem kendali lampu jarak jauh, dashboard energi solar panel, sistem peringatan dini banjir. Tambahkan pesan motivasi untuk mahasiswa.

**Kata Kunci:** Ringkasan, mind map, kompetensi, IoT end-to-end, MQTT, ESP32, backend, deployment, penutup modul
**Visualisasi:** Mind map radial 8 cabang berwarna, tabel proyek yang bisa dibangun, ilustrasi mahasiswa berhasil

---

### Slide 45: Referensi, Sumber Belajar, dan Tugas Praktikum

**Prompt NotebookLLM:**
Buatkan slide "Referensi dan Tugas Praktikum" yang menampilkan daftar sumber belajar terpercaya dan deskripsi tugas akhir modul. Referensi utama (format APA 7): (1) MQTT.org – Spesifikasi resmi MQTT 3.1.1 dan 5.0; (2) Eclipse Mosquitto Documentation – mosquitto.org; (3) PlatformIO Documentation – docs.platformio.org; (4) paho-mqtt Python Library – eclipse.dev/paho; (5) FastAPI Documentation – fastapi.tiangolo.com; (6) Vue.js 3 Documentation – vuejs.org; (7) PostgreSQL Documentation – postgresql.org/docs; (8) Redis Documentation – redis.io/docs; (9) Buku: "Designing Connected Products" oleh Claire Rowland et al. (O'Reilly, 2015); (10) Paper: "MQTT Protocol Overview" – IBM DeveloperWorks. Sumber belajar online: HiveMQ MQTT Essentials (blog series), Random Nerd Tutorials (ESP32), Fireship.io (Node.js/React). Tugas Praktikum: "Bangun sistem monitoring IoT minimal dengan 1 ESP32, broker Mosquitto, backend Python/Node.js, dan dashboard web sederhana. Data harus tersimpan di database dan dapat diakses melalui REST API." Sertakan kriteria penilaian (rubrik). Tampilkan QR code menuju repository GitHub modul.

**Kata Kunci:** Referensi, APA 7, tugas praktikum, sumber belajar, MQTT.org, PlatformIO, FastAPI, Vue.js, PostgreSQL, rubrik penilaian
**Visualisasi:** Daftar referensi terformat, QR code repository GitHub, tabel rubrik penilaian tugas, ikon buku dan laptop

---

## Catatan Penggunaan Prompt

> **Cara menggunakan file ini di NotebookLLM:**
> 1. Buka [NotebookLLM](https://notebooklm.google.com/) dan buat notebook baru.
> 2. Upload dokumen referensi relevan (dokumentasi MQTT, ESP32, dll.) sebagai sumber.
> 3. Salin setiap blok **Prompt NotebookLLM** satu per satu ke kolom chat.
> 4. Tambahkan instruksi format slide sesuai template presentasi yang digunakan (Google Slides, PowerPoint, Canva).
> 5. Iterasi dan perbaiki output sesuai kebutuhan.

> **Tips:** Untuk hasil terbaik, tambahkan instruksi tambahan seperti *"Gunakan bahasa Indonesia formal akademis"*, *"Buat dalam format poin-poin singkat, maksimal 5 baris per poin"*, atau *"Sertakan diagram ASCII sederhana jika diperlukan"*.

---

*Dibuat untuk: Praktikum Mekatronika dan Robotika – Modul 04*
*Jumlah Slide: 45 slide*
*Bahasa: Bahasa Indonesia*
