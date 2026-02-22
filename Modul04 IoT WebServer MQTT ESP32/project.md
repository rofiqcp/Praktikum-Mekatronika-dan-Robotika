# PROJECT MODUL 04: IoT WEBSERVER MQTT ESP32 — IMPROVISASI & INOVASI

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 04 – IoT WebServer MQTT ESP32  
**Platform:** ESP32 (PlatformIO), Python Edge, Backend Server, Frontend Dashboard  
**Protokol:** MQTT, HTTP/REST, WebSocket  
**Pengerjaan:** Per Kelompok (Maks. 4 Orang)

---

> ⚠️ **CATATAN PENTING**  
> Proyek ini merupakan **improvisasi dan inovasi** dari percobaan praktikum dasar Modul 04.  
> Setiap kelompok **memilih SATU** dari 10 opsi proyek berikut.  
> Sistem harus berjalan end-to-end: ESP32 → MQTT Broker → Backend → Database → Frontend Dashboard.

---

## A. DESKRIPSI PROYEK

Pada praktikum dasar Modul 04, mahasiswa telah mempelajari:
- ESP32 sebagai edge device dengan sensor DHT22 / LDR / soil moisture
- Python sebagai laptop edge device (MQTT subscriber + data processing)
- Backend REST API (Node.js / FastAPI / Spring Boot)
- Frontend dashboard sederhana (Vue.js / React)
- Database penyimpanan time-series (InfluxDB / PostgreSQL / MongoDB)
- Deployment lokal dan publik (PM2 + Nginx / ngrok / certbot)

Proyek ini menantang setiap kelompok untuk **mengangkat masalah nyata** di dunia industri, pertanian, bangunan, atau kampus, lalu membangun sistem IoT yang **lebih lengkap, lebih kompleks, dan lebih bernilai** dari sekadar percobaan dasar. Cerita di setiap opsi proyek menggambarkan **skenario dunia nyata** yang menjadi motivasi teknis sistem yang dibangun.

**Teknologi yang boleh digunakan:**

| Lapisan | Pilihan Teknologi |
|---------|------------------|
| Edge Device | ESP32 (PlatformIO, C++) |
| Edge Processing | Python (paho-mqtt, pandas, numpy) |
| Backend | Java Spring Boot / Python FastAPI / Node.js Express / C# ASP.NET / C++ Crow |
| Frontend | Vue.js / React / Angular |
| Database | PostgreSQL / MySQL / MongoDB / Redis / InfluxDB |
| Deployment | localhost / PM2 + Nginx / ngrok / certbot (HTTPS) |

---

## B. OPSI PROYEK (PILIH SATU)

---

### Proyek 1 — Sistem Monitoring Kualitas Udara Pabrik

**Judul Proyek:** SmartAir Factory — Sistem Pemantauan Kualitas Udara Real-Time untuk Industri Manufaktur

---

**Cerita / Skenario:**

PT. Anugerah Logam Nusantara adalah perusahaan pengolahan logam di Kawasan Industri Cikarang yang mempekerjakan lebih dari 500 buruh di lantai produksi. Bapak Hendra, selaku manajer K3 (Keselamatan dan Kesehatan Kerja), sering menerima laporan bahwa para pekerja di area pengecoran mengalami pusing dan sesak napas. Setelah ditelusuri, ternyata konsentrasi gas CO, partikulat PM2.5, dan VOC (Volatile Organic Compound) di area tersebut sering melampaui ambang batas aman yang ditetapkan BPNK.

Selama ini, pengukuran kualitas udara dilakukan secara manual oleh petugas K3 menggunakan alat ukur portabel sekali sehari. Data tidak tersimpan secara terstruktur, dan ketika insiden terjadi, tidak ada catatan historis yang bisa dijadikan bukti. Bapak Hendra ingin sebuah sistem yang bisa memantau kualitas udara 24 jam non-stop di 4 zona produksi, mengirim peringatan otomatis ke ponsel supervisor ketika ada parameter yang melewati batas, dan menyimpan data historis untuk laporan kepatuhan regulasi setiap bulan.

Tim mahasiswa Teknik Mekatronika dari Universitas Bahari ditugaskan untuk membangun prototipe sistem tersebut menggunakan ESP32 yang dipasang di setiap zona, dengan dasbor web yang bisa diakses oleh manajemen dari ruang kantor maupun dari luar pabrik melalui jaringan internet.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 4 node sensor (MQ-7 CO, MQ-135 VOC, GP2Y1010AU0F PM2.5, DHT22 suhu/kelembaban) per zona, kirim data via MQTT setiap 10 detik |
| Python / Laptop Edge Role | Subscriber MQTT → agregasi data 5 menit → deteksi anomali → trigger alert jika melebihi threshold AQI |
| Backend Technology | **Python FastAPI** — REST API untuk CRUD data, endpoint WebSocket untuk live streaming ke dashboard |
| Frontend Technology | **React** + Recharts / Chart.js — dashboard peta zona pabrik, grafik real-time, panel alert |
| Database | **InfluxDB** (time-series sensor) + **Redis** (cache status zona terkini) |
| Deployment Method | **PM2 + Nginx** — FastAPI di-serve dengan uvicorn + PM2, Nginx sebagai reverse proxy port 80 |

**Fitur Wajib:**
1. Live dashboard menampilkan nilai CO, VOC, PM2.5, suhu, dan AQI per zona dalam kartu berwarna (hijau/kuning/merah)
2. Notifikasi alert muncul di dashboard (toast/banner) ketika AQI zona melebihi batas aman (AQI > 100)
3. Grafik historis interaktif per zona dengan filter rentang waktu (1 jam / 6 jam / 24 jam / 7 hari)
4. Endpoint REST `/api/report/monthly` menghasilkan ringkasan statistik (rata-rata, maks, menit) per zona
5. Sistem menyimpan riwayat alert lengkap dengan timestamp, zona, parameter, dan nilai terukur

**Kriteria Keberhasilan:**
- Semua 4 node ESP32 mengirim data valid ke broker MQTT tanpa putus selama 30 menit pengujian
- Dashboard React menampilkan data real-time dengan latensi < 5 detik dari pengukuran ESP32
- InfluxDB menyimpan minimal 1000 data point dan query historis berjalan < 2 detik
- Nginx berhasil serve frontend dan memproxy API, dapat diakses dari perangkat lain di jaringan yang sama

**Tingkat Kesulitan:** ⭐⭐⭐⭐

---

### Proyek 2 — Smart Greenhouse Otomatis

**Judul Proyek:** GreenSmart — Platform Manajemen Greenhouse Berbasis IoT untuk Pertanian Presisi

---

**Cerita / Skenario:**

Ibu Siti Rahayu adalah pemilik usaha greenhouse hidroponik selada di Kabupaten Magelang. Greenhouse-nya memiliki luas 500 m² dengan kapasitas 2.000 tanaman. Selama ini Ibu Siti dan satu orang pekerjanya harus datang dua kali sehari untuk mengecek kondisi tanaman: memeriksa kadar air media tanam, mengatur ventilasi jika suhu terlalu panas, dan menghidupkan/mematikan pompa irigasi secara manual. Ketika Ibu Siti bepergian ke luar kota, tanaman pernah stres akibat kekeringan karena pekerja lupa menyiram.

Ibu Siti membutuhkan sistem yang dapat membaca kondisi greenhouse secara otomatis: sensor kelembaban tanah (soil moisture), suhu dan kelembaban udara (DHT22), serta intensitas cahaya (BH1750). Jika kelembaban tanah turun di bawah 40%, pompa irigasi otomatis menyala selama 3 menit. Jika suhu melebihi 32°C, exhaust fan otomatis aktif. Semua kejadian ini harus tercatat dan bisa dilihat Ibu Siti dari ponselnya di mana saja.

Proyek ini dikerjakan oleh tim mahasiswa magang dari program studi Mekatronika yang bekerja sama dengan Dinas Pertanian Kabupaten Magelang sebagai bagian dari program digitalisasi pertanian rakyat.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 2 node sensor (DHT22, kapasitif soil moisture, BH1750 LUX, relay 2-channel untuk pompa + fan), kirim data via MQTT setiap 15 detik, terima command MQTT untuk kontrol relay manual |
| Python / Laptop Edge Role | Subscriber MQTT → rule engine otomasi (hysteresis control) → publish command MQTT ke ESP32 → logging ke database |
| Backend Technology | **Java Spring Boot** — REST API + WebSocket endpoint, schedule task untuk laporan harian via email |
| Frontend Technology | **Angular** + Angular Material — dashboard greenhouse, kontrol relay manual, grafik tren suhu & kelembaban |
| Database | **PostgreSQL** (data sensor + log aktuasi + user management) |
| Deployment Method | **PM2 + Nginx** — Spring Boot JAR dijalankan dengan PM2, Nginx reverse proxy dengan HTTPS self-signed |

**Fitur Wajib:**
1. Kontrol relay manual (pompa & fan) dari dashboard Angular dengan tombol ON/OFF yang hasilnya langsung terlihat di status indikator
2. Rule engine otomatis: pompa nyala jika soil moisture < 40%, fan nyala jika suhu > 32°C, dengan hysteresis ±5% untuk mencegah flapping
3. Grafik historis suhu, kelembaban, dan soil moisture per hari / minggu
4. Log aktuasi: setiap relay ON/OFF dicatat dengan timestamp, trigger (otomatis/manual), dan durasi
5. Halaman konfigurasi threshold yang bisa diubah dari UI tanpa perlu modifikasi kode

**Kriteria Keberhasilan:**
- Rule engine Python berhasil memicu command relay dalam < 3 detik setelah sensor membaca nilai di bawah/di atas threshold
- Dashboard Angular dapat diakses dan berfungsi penuh dari perangkat mobile (responsif)
- Data tersimpan di PostgreSQL dan dapat di-query dengan filter tanggal
- Nginx berhasil melayani frontend Angular (dist build) dan memproxy API Spring Boot

**Tingkat Kesulitan:** ⭐⭐⭐⭐

---

### Proyek 3 — Dashboard Energi Rumah Pintar

**Judul Proyek:** EnergiKu — Sistem Pemantauan Konsumsi Energi Real-Time untuk Rumah Tangga Cerdas

---

**Cerita / Skenario:**

Pak Budi Santoso tinggal di perumahan Griya Asri, Tangerang Selatan. Setiap bulan ia selalu kaget dengan tagihan listrik yang membengkak hingga Rp 800.000 padahal menurutnya penggunaan peralatan di rumah tidak berlebihan. Pak Budi curiga ada salah satu peralatan yang boros listrik, namun tidak tahu cara membuktikannya karena hanya memiliki meteran listrik analog di garasi yang harus dilihat secara fisik.

Pak Budi bergabung dengan komunitas rumah pintar di media sosial dan menemukan bahwa ia bisa memasang sensor arus (SCT-013) di jalur utama panel listrik untuk mengukur daya yang dikonsumsi setiap peralatan. Ia ingin sebuah dashboard yang menampilkan daya real-time per sirkuit (ruang tamu, dapur, kamar tidur), grafik konsumsi harian/bulanan, estimasi tagihan bulan ini, dan notifikasi jika ada peralatan yang terus menyala lebih dari 2 jam.

Pak Budi meminta bantuan putranya yang mahasiswa Teknik Mekatronika untuk membangun sistem ini sebagai proyek semester. Karena anggaran terbatas dan koneksi internet di rumah sudah ada, sistem cukup berjalan di laptop bekas yang dijadikan server lokal.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 1 node dengan 3 kanal SCT-013 (sensor arus non-invasif) + ZMPT101B (sensor tegangan) → hitung daya (P = V × I × cos φ), kirim via MQTT setiap 5 detik |
| Python / Laptop Edge Role | Subscriber MQTT → kalkulasi kWh kumulatif → estimasi tagihan berdasarkan tarif PLN → simpan ke MongoDB |
| Backend Technology | **Node.js Express** — REST API, Socket.io untuk real-time push ke frontend |
| Frontend Technology | **Vue.js** + Vuetify — kartu daya per sirkuit, grafik konsumsi, kalkulator estimasi tagihan |
| Database | **MongoDB** (time-series fleksibel) + **Redis** (buffer data real-time 5 menit terakhir) |
| Deployment Method | **ngrok** — expose server Node.js lokal ke internet publik agar bisa diakses dari ponsel Pak Budi di kantor |

**Fitur Wajib:**
1. Dashboard menampilkan daya aktif (Watt) real-time per sirkuit dengan animasi live update
2. Grafik konsumsi kWh per jam (hari ini) dan per hari (bulan ini) dalam bentuk bar chart
3. Estimasi tagihan bulan berjalan berdasarkan TDL PLN R-1 (900 VA / 1300 VA / 2200 VA, bisa dipilih di pengaturan)
4. Alert "Perangkat Aktif Terlalu Lama" jika daya sirkuit melebihi threshold selama > 120 menit berturut-turut
5. Ekspor data konsumsi bulanan ke CSV dari halaman dashboard

**Kriteria Keberhasilan:**
- Pembacaan daya ESP32 akurat ±10% dibandingkan clamp meter referensi
- Socket.io berhasil push update ke Vue.js frontend dengan interval ≤ 5 detik
- ngrok tunnel stabil dan dashboard dapat diakses dari jaringan berbeda
- MongoDB menyimpan data 7 hari dengan query agregasi per jam berjalan < 1 detik

**Tingkat Kesulitan:** ⭐⭐⭐

---

### Proyek 4 — Sistem Keamanan Gedung IoT

**Judul Proyek:** SecureNet — Platform Keamanan Gedung Berbasis Multi-Sensor IoT dengan Notifikasi Real-Time

---

**Cerita / Skenario:**

Gedung Perkantoran Graha Mandiri di Jalan Sudirman, Surabaya, memiliki 8 lantai dan 120 ruangan. Pak Agus, kepala sekuriti gedung, mengeluh bahwa sistem CCTV analog yang ada sangat mahal perawatannya dan tidak bisa memberikan notifikasi otomatis ketika ada kejadian di luar jam kantor. Beberapa bulan lalu, terjadi percobaan pencurian di lantai 3 pada pukul 02.00 dini hari yang baru diketahui keesokan paginya saat rekaman CCTV diperiksa.

Pak Agus ingin melengkapi sistem keamanan dengan sensor tambahan yang lebih cerdas: sensor PIR (Passive Infrared) untuk mendeteksi pergerakan, sensor magnetic door/window untuk mendeteksi pintu/jendela yang terbuka, dan buzzer alarm lokal. Ketika ada deteksi di luar jam operasional (18.00–07.00), sistem harus langsung mengirim notifikasi ke ponsel petugas sekuriti dan menyimpan log kejadian dengan foto timestamp digital.

Proyek ini menjadi bagian dari program peningkatan keamanan gedung yang diinisiasi oleh manajemen properti PT. Graha Mandiri Sejahtera, bekerja sama dengan tim riset mahasiswa yang berminat di bidang IoT security.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 2 node (lantai 1 & lantai 3) masing-masing dengan PIR HC-SR501, sensor pintu magnetic reed switch × 2, buzzer, LED alarm; publish event ke MQTT topic per sensor |
| Python / Laptop Edge Role | Subscriber MQTT → evaluasi jadwal (jam operasional) → trigger alarm logic → kirim notifikasi webhook Telegram Bot API |
| Backend Technology | **C# ASP.NET Core** — REST API dengan Entity Framework Core, SignalR untuk real-time push event ke dashboard |
| Frontend Technology | **React** + Tailwind CSS — live event feed, denah gedung interaktif (SVG), panel manajemen jadwal |
| Database | **SQLite** (via EF Core, cukup untuk skala prototipe) dengan migrasi ke PostgreSQL sebagai opsi produksi |
| Deployment Method | **ngrok** — expose ASP.NET Core server agar notifikasi Telegram callback bisa masuk dari internet |

**Fitur Wajib:**
1. Live event feed di React dashboard menampilkan setiap deteksi PIR atau door sensor dengan timestamp dan lokasi (lantai/zona)
2. Denah gedung SVG interaktif: zona yang terpicu menyala merah, zona aman hijau, update real-time via SignalR
3. Panel konfigurasi jadwal "Arm/Disarm" per zona (sistem alarm aktif di luar jam kerja)
4. Notifikasi Telegram: pesan teks dikirim ke grup sekuriti saat event terdeteksi dalam mode "Armed"
5. Laporan harian otomatis: ringkasan jumlah event per zona, dikirim ke Telegram setiap pukul 07.00

**Kriteria Keberhasilan:**
- Notifikasi Telegram terkirim dalam < 10 detik setelah sensor terpicu
- SignalR berhasil push event ke React dashboard tanpa reload halaman
- SQLite menyimpan log event minimal 500 entry dan query filter per tanggal berjalan benar
- Mode Arm/Disarm berfungsi: tidak ada alarm/notifikasi saat mode Disarm aktif

**Tingkat Kesulitan:** ⭐⭐⭐

---

### Proyek 5 — Monitoring Peralatan Lab Kampus

**Judul Proyek:** LabWatch — Sistem Pemantauan Kondisi dan Penggunaan Peralatan Laboratorium Kampus

---

**Cerita / Skenario:**

Laboratorium Mekatronika Universitas Teknologi Nusantara memiliki peralatan senilai lebih dari Rp 2 miliar, termasuk 3D printer, laser engraver, CNC mini, dan stasiun solder profesional. Kepala lab, Dr. Fajar Wicaksono, sering menemukan peralatan dalam keadaan menyala padahal tidak ada yang menggunakan, menyebabkan pemborosan energi dan memperpendek umur peralatan. Selain itu, beberapa peralatan sensitif memerlukan suhu ruangan di bawah 28°C untuk bekerja optimal, namun AC sering dimatikan setelah jam kuliah selesai.

Dr. Fajar ingin sebuah sistem yang dapat mencatat siapa yang menggunakan alat apa dan kapan (menggunakan RFID atau tombol check-in manual), memantau suhu dan kelembaban ruangan, mengukur konsumsi daya tiap peralatan, dan menghasilkan laporan utilisasi bulanan. Dengan sistem ini, pengelolaan lab menjadi lebih terukur dan pengajuan anggaran peralatan baru pun memiliki data pendukung yang kuat.

Sistem ini akan diimplementasikan oleh tim mahasiswa sebagai bagian dari tugas akhir sekaligus menjadi kontribusi nyata bagi infrastruktur kampus.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 1 node utama dengan DHT22 (suhu/kelembaban ruangan), 4 kanal sensor arus ACS712 (satu per peralatan), 1 modul RFID RC522 (check-in pengguna), OLED display status; publish data MQTT setiap 30 detik + event RFID instan |
| Python / Laptop Edge Role | Subscriber MQTT → identifikasi kartu RFID dari database pengguna → hitung jam pemakaian per alat → push ke API |
| Backend Technology | **Python FastAPI** — REST API async, background task untuk agregasi statistik, export laporan PDF (ReportLab) |
| Frontend Technology | **Vue.js** + PrimeVue — tabel sesi penggunaan real-time, grafik utilisasi per alat, halaman profil pengguna |
| Database | **InfluxDB** (time-series daya & lingkungan) + file JSON flat (mapping RFID UID → nama pengguna) |
| Deployment Method | **PM2** — FastAPI dijalankan dengan uvicorn, PM2 menjaga proses tetap hidup dan auto-restart |

**Fitur Wajib:**
1. Deteksi check-in/out pengguna via RFID: sesi aktif ditampilkan real-time di dashboard (nama, alat, waktu mulai)
2. Grafik konsumsi daya per alat dengan overlay sesi penggunaan (kapan alat digunakan vs menyala idle)
3. Alert "Alat Idle Terlalu Lama": notifikasi di dashboard jika alat menyala > 30 menit tanpa ada sesi aktif
4. Laporan utilisasi bulanan: jam pakai per alat, pengguna terbanyak, konsumsi energi total — dapat diunduh sebagai PDF
5. Halaman admin untuk tambah/hapus pengguna dan assignment RFID UID ke nama

**Kriteria Keberhasilan:**
- RFID check-in tercatat di sistem dalam < 2 detik setelah kartu ditap
- FastAPI endpoint laporan PDF berjalan dan menghasilkan file yang valid
- PM2 auto-restart berhasil diverifikasi (matikan proses manual, cek PM2 menghidupkan kembali)
- Dashboard Vue.js menampilkan sesi aktif real-time dan data historis 7 hari

**Tingkat Kesulitan:** ⭐⭐⭐⭐

---

### Proyek 6 — Sistem Irigasi Pertanian Cerdas

**Judul Proyek:** IrigasiPintar — Manajemen Irigasi Otomatis Berbasis IoT untuk Lahan Pertanian Skala Menengah

---

**Cerita / Skenario:**

Koperasi Tani Maju Jaya di Kabupaten Blitar mengelola 12 petak sawah dengan total luas 8 hektare yang ditanami cabai dan tomat. Selama ini, jadwal irigasi ditentukan oleh mandor berdasarkan perkiraan visual dan pengalaman, bukan data ilmiah. Hal ini menyebabkan beberapa petak kadang kelebihan air (waterlogging) yang memicu penyakit jamur, sementara petak lain kekurangan air di musim kemarau.

Pak Slamet, ketua koperasi, pernah mengikuti pelatihan pertanian presisi yang menekankan pentingnya pengukuran kadar air tanah dan pemberian air sesuai kebutuhan tanaman. Ia ingin setiap petak sawah dipasangi sensor kelembaban tanah yang terhubung ke sistem irigasi tetes otomatis dengan solenoid valve. Sistem harus bisa diprogram jadwal irigasi, dioverride secara manual dari ponsel, dan memberikan laporan penggunaan air bulanan untuk perencanaan anggaran.

Proyek ini didanai oleh hibah digitalisasi pertanian dari Kementerian Pertanian dan dikerjakan bersama tim peneliti dari universitas setempat.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 3 node (masing-masing mengelola 4 petak) dengan sensor kelembaban kapasitif × 4, sensor suhu tanah DS18B20 × 4, relay 4-channel untuk solenoid valve; publish data MQTT setiap 20 detik, subscribe command MQTT untuk buka/tutup valve |
| Python / Laptop Edge Role | Subscriber MQTT → decision engine irigasi (soil moisture + jadwal) → publish command valve → logging volume air (estimasi dari durasi valve terbuka × flow rate) |
| Backend Technology | **Java Spring Boot** — REST API, Spring Scheduler untuk jadwal irigasi otomatis, endpoint konfigurasi jadwal |
| Frontend Technology | **Angular** + Leaflet.js — peta petak sawah interaktif, kontrol valve per petak, kalender jadwal irigasi |
| Database | **MySQL** (data sensor, log irigasi, jadwal, pengguna) |
| Deployment Method | **Nginx + Certbot** — Spring Boot di-deploy di VPS lokal kampus, HTTPS dengan Let's Encrypt sehingga petani bisa akses dari ponsel 4G |

**Fitur Wajib:**
1. Peta interaktif petak sawah (Leaflet.js): setiap petak berwarna berdasarkan kadar air tanah (merah/kuning/hijau)
2. Penjadwalan irigasi dengan kalender: bisa atur hari, jam, dan durasi per petak, tersimpan di MySQL
3. Override manual: tombol "Buka Valve" / "Tutup Valve" per petak dari dashboard, dengan konfirmasi
4. Estimasi volume air yang digunakan per petak per bulan (berdasarkan durasi valve terbuka × flow rate kalibrasi)
5. Notifikasi "Tanah Terlalu Kering" jika kadar air < 25% selama > 2 jam tanpa irigasi terjadwal

**Kriteria Keberhasilan:**
- Jadwal irigasi tersimpan di MySQL dan Spring Scheduler berhasil memicu command MQTT sesuai waktu
- Override manual dari Angular berhasil membuka/menutup relay ESP32 dalam < 5 detik
- Peta Leaflet.js menampilkan status warna yang berubah sesuai data sensor terkini
- Certbot berhasil issue sertifikat dan dashboard dapat diakses via HTTPS

**Tingkat Kesulitan:** ⭐⭐⭐⭐⭐

---

### Proyek 7 — Manajemen Parkir Real-Time

**Judul Proyek:** ParkSmart — Sistem Informasi Parkir Real-Time dengan Navigasi Slot Berbasis IoT

---

**Cerita / Skenario:**

Mal Ciputra World Surabaya memiliki gedung parkir 7 lantai dengan 1.200 slot kendaraan. Setiap hari terutama di akhir pekan, pengunjung membuang waktu rata-rata 12 menit berkeliling mencari slot kosong, menyebabkan kemacetan di dalam gedung dan emisi gas buang yang tidak perlu. Manajer fasilitas, Ibu Dewi Kusuma, ingin memperbarui sistem parkir manual (petugas yang menghitung kendaraan) dengan sistem sensor otomatis yang menampilkan slot tersedia secara real-time di LED signboard dan di aplikasi web pengunjung.

Ide sistem yang diinginkan: setiap slot dipasangi sensor ultrasonik HC-SR04 yang mendeteksi ada/tidaknya kendaraan. Data agregat per zona (A1–A10, B1–B10, dst.) ditampilkan di dashboard besar di pintu masuk dan di aplikasi web yang bisa dibuka dari ponsel pengunjung sebelum masuk gedung. Sistem juga mencatat data historis untuk analisis pola puncak parkir, membantu manajemen mengoptimalkan tenaga petugas dan strategi harga parkir dinamis.

Tim mahasiswa membangun prototipe dengan skala 24 slot (2 zona × 12 slot) menggunakan ESP32 dan model miniatur.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 2 node (zona A dan zona B) masing-masing dengan 12 sensor ultrasonik HC-SR04 via multiplexer CD74HC4067; LED WS2812 per slot (hijau=kosong, merah=terisi); publish status tiap 3 detik via MQTT |
| Python / Laptop Edge Role | Subscriber MQTT → agregasi occupancy per zona → update Redis → simpan snapshot historis setiap 5 menit ke MongoDB |
| Backend Technology | **Node.js Express** + Socket.io — real-time push status ke frontend, REST API untuk data historis |
| Frontend Technology | **React** + Framer Motion — visualisasi denah parkir animasi, counter slot tersedia, grafik ocupancy historis |
| Database | **Redis** (state parkir real-time, TTL 10 detik) + **MongoDB** (snapshot historis, analitik) |
| Deployment Method | **PM2** — Node.js server dijalankan dengan PM2, cluster mode 2 instance untuk high-availability |

**Fitur Wajib:**
1. Denah parkir visual real-time: setiap slot divisualisasikan sebagai kotak hijau/merah, update otomatis tanpa reload
2. Counter besar di header dashboard: "Zona A: 5/12 Tersedia | Zona B: 3/12 Tersedia"
3. Grafik historis occupancy rate per jam (hari ini dan 7 hari terakhir) untuk analisis pola puncak
4. API publik `GET /api/parking/status` yang mengembalikan JSON status semua zona (untuk integrasi pihak ketiga)
5. Panel admin: reset manual status slot (untuk menangani sensor error), lihat log perubahan status

**Kriteria Keberhasilan:**
- Perubahan status slot (dari kosong ke terisi atau sebaliknya) muncul di dashboard React dalam < 3 detik
- Redis menyimpan state terkini dan dapat di-query dengan latensi < 10 ms
- MongoDB menyimpan snapshot 2 jam dan query agregasi per jam berjalan dengan benar
- PM2 cluster mode berjalan dengan 2 instance, PM2 status menunjukkan keduanya "online"

**Tingkat Kesulitan:** ⭐⭐⭐⭐

---

### Proyek 8 — Pemantauan Rantai Dingin (Cold Chain)

**Judul Proyek:** ColdTrack — Sistem Pemantauan Suhu dan Lokasi Rantai Dingin untuk Industri Farmasi

---

**Cerita / Skenario:**

PT. Farma Prima Distribusi adalah distributor produk farmasi berpendingin (vaksin, insulin, reagen laboratorium) yang melayani 150 apotek dan rumah sakit di Jawa Timur. Pak Rizal, manajer logistik, menghadapi masalah serius: beberapa kali terjadi klaim dari apotek bahwa produk yang diterima sudah rusak karena rantai dingin terputus selama pengiriman. Namun perusahaan tidak memiliki bukti rekaman suhu selama perjalanan untuk membantah klaim tersebut, menyebabkan kerugian finansial dan reputasi.

Pak Rizal membutuhkan sistem yang dipasang di setiap armada pendingin: sensor suhu presisi (DS18B20) di kompartemen kargo, GPS tracker untuk posisi kendaraan, dan data dikirim ke server pusat via MQTT over 4G LTE. Jika suhu melewati batas aman (2°C–8°C untuk produk farmasi), sistem harus segera mengirim alert ke manajer dan driver, dengan lokasi GPS kejadian tersimpan sebagai bukti audit.

Tim mahasiswa bertugas membangun versi prototipe dengan skala 3 kendaraan virtual (menggunakan GPS module NEO-6M pada ESP32 yang digerakkan di sekitar kampus).

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 3 node (simulasi 3 armada) masing-masing dengan DS18B20 (suhu, waterproof), GPS NEO-6M (koordinat), DHT22 (suhu kabin pengemudi sebagai referensi); publish data MQTT every 15 detik dengan payload JSON {suhu, lat, lon, vehicle_id} |
| Python / Laptop Edge Role | Subscriber MQTT → validasi suhu terhadap batas SOP farmasi (2°C–8°C) → trigger alert jika violations → simpan ke PostgreSQL |
| Backend Technology | **C# ASP.NET Core** — REST API + SignalR Hub untuk live tracking, background service untuk agregasi data |
| Frontend Technology | **Angular** + Leaflet.js — peta live tracking 3 armada, timeline suhu per kendaraan, laporan pengiriman |
| Database | **PostgreSQL** (semua data: perjalanan, suhu, alert, laporan) |
| Deployment Method | **PM2 + Nginx** — ASP.NET Core dikompilasi sebagai self-contained, dijalankan dengan PM2, Nginx reverse proxy |

**Fitur Wajib:**
1. Peta live tracking: 3 ikon armada bergerak di peta Leaflet, warna berubah ke merah jika ada pelanggaran suhu aktif
2. Timeline suhu per kendaraan: grafik suhu vs waktu, area merah jika di luar batas 2–8°C
3. Alert pelanggaran suhu: muncul di dashboard sebagai popup + dicatat di database dengan lokasi GPS kejadian
4. Laporan pengiriman per kendaraan: durasi perjalanan, jumlah pelanggaran suhu, suhu rata-rata/min/maks
5. Export laporan PDF audit cold chain (minimal 1 halaman per kendaraan per perjalanan)

**Kriteria Keberhasilan:**
- Data suhu + GPS dari 3 node ESP32 terpublikasi ke MQTT dan tersimpan di PostgreSQL secara bersamaan
- Peta Leaflet menampilkan posisi terkini setiap kendaraan dengan update ≤ 20 detik
- Alert pelanggaran suhu muncul di dashboard dalam < 5 detik setelah sensor membaca nilai di luar batas
- SignalR berhasil push update ke Angular tanpa polling

**Tingkat Kesulitan:** ⭐⭐⭐⭐⭐

---

### Proyek 9 — Sistem Kontrol HVAC Gedung

**Judul Proyek:** ClimateIQ — Platform Otomasi dan Monitoring Sistem HVAC Gedung Berbasis IoT

---

**Cerita / Skenario:**

Gedung Rektorat Universitas Nusantara Jaya memiliki 5 lantai dengan 40 ruangan ber-AC. Setiap bulan, tagihan listrik gedung mencapai Rp 45 juta, dan Wakil Rektor Bidang Umum, Prof. Andika, menduga konsumsi listrik untuk pendinginan ruangan adalah kontributor terbesar. Masalahnya, AC sering dibiarkan menyala meskipun ruangan kosong karena pengguna lupa mematikan, dan tidak ada sistem sentralisasi yang memberi gambaran kondisi termal seluruh gedung.

Prof. Andika ingin memasang sensor suhu dan kelembaban di setiap lantai, sensor gerak PIR untuk deteksi keberadaan manusia, dan mengintegrasikannya dengan kontrol AC melalui IR blaster (ESP32 mengirim sinyal infrared ke AC yang sudah ada). Sistem harus bisa menampilkan peta termal gedung secara real-time, mematikan AC otomatis jika tidak ada orang dalam 20 menit, dan memberikan laporan penghematan energi bulanan.

Proyek ini berpotensi dipresentasikan ke manajemen universitas sebagai solusi efisiensi energi dengan ROI yang terukur dari penghematan tagihan listrik.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 5 node (satu per lantai) dengan DHT22 × 2 (suhu & kelembaban), PIR HC-SR501 × 2 (deteksi okupansi), IR LED + modul TSOP untuk kontrol AC (simulasi dengan LED indikator jika AC nyata tidak tersedia), publish data MQTT setiap 20 detik + event PIR instan |
| Python / Laptop Edge Role | Subscriber MQTT → algoritma okupansi (PIR + timer 20 menit) → keputusan kontrol AC → publish command MQTT → log ke MongoDB |
| Backend Technology | **Python FastAPI** — REST API async, WebSocket untuk streaming peta termal, endpoint statistik penghematan |
| Frontend Technology | **Vue.js** + D3.js — heatmap suhu gedung (SVG denah), status AC per ruangan, grafik tren suhu & energi |
| Database | **MongoDB** (time-series suhu + log kontrol AC + sesi okupansi) |
| Deployment Method | **ngrok** — expose FastAPI lokal agar Prof. Andika bisa memantau dari ponsel saat rapat di luar kampus |

**Fitur Wajib:**
1. Heatmap termal gedung real-time: denah tiap lantai dengan warna gradasi suhu (biru–kuning–merah), update via WebSocket
2. Status AC per lantai: indikator visual ON/OFF dengan informasi suhu setpoint dan mode (cooling/fan)
3. Logika auto-off: AC otomatis dimatikan jika tidak ada deteksi PIR selama 20 menit, dengan countdown timer di dashboard
4. Grafik perbandingan suhu vs status AC per lantai (time-series 24 jam)
5. Laporan efisiensi: estimasi jam operasi AC yang terhemat dari fitur auto-off per hari/minggu

**Kriteria Keberhasilan:**
- Heatmap D3.js diperbarui via WebSocket dalam < 5 detik setelah data baru masuk
- Auto-off logic berfungsi: command MQTT untuk matikan AC terkirim setelah 20 menit tanpa PIR (dapat disimulasikan dengan mengatur threshold waktu ke 1 menit untuk pengujian)
- MongoDB menyimpan minimal 200 data point per node dan query filter per lantai berjalan benar
- ngrok tunnel aktif dan dashboard dapat diakses dari jaringan eksternal

**Tingkat Kesulitan:** ⭐⭐⭐⭐

---

### Proyek 10 — Platform Telemetri Multi-Robot

**Judul Proyek:** RoboTelemetry Hub — Platform Pemantauan dan Komando Multi-Robot Otonom Berbasis IoT

---

**Cerita / Skenario:**

Startup teknologi PT. Reka Robotika Indonesia sedang mengembangkan armada robot otonom untuk keperluan inspeksi gudang di PT. Logistik Andalan Nusantara. Tiga prototipe robot telah selesai dibangun dan siap diuji di gudang seluas 5.000 m². Masing-masing robot dilengkapi ESP32 sebagai on-board computer yang membaca data encoder roda (kecepatan), sensor jarak ultrasonik (deteksi rintangan), IMU MPU-6050 (orientasi), dan indikator baterai.

CEO PT. Reka Robotika, Mas Yoga, membutuhkan sebuah "command center" berbasis web yang dapat memantau telemetri semua robot secara bersamaan: posisi (dead reckoning dari encoder), kecepatan, orientasi (yaw dari IMU), status baterai, dan event rintangan terdeteksi. Selain memantau, operator harus bisa mengirim perintah navigasi sederhana (maju, mundur, belok kiri, belok kanan, berhenti) ke robot tertentu melalui dashboard. Semua data telemetri dan perintah harus dilog untuk analisis performa robot dan debugging.

Proyek ini akan menjadi portofolio utama tim dan akan dipresentasikan di pameran teknologi nasional INATECH 2026.

---

**Spesifikasi Teknis:**

| Parameter | Spesifikasi |
|-----------|------------|
| ESP32 Role | 3 node (robot 1, 2, 3) masing-masing dengan encoder simulasi (rotary encoder atau timer interrupt), HC-SR04 (obstacle), MPU-6050 (IMU via I2C), voltage divider untuk baterai; publish telemetri MQTT setiap 200 ms (5 Hz), subscribe command topic untuk navigasi |
| Python / Laptop Edge Role | Subscriber telemetri MQTT semua robot → dead reckoning kalkulasi posisi (x, y, θ) → normalisasi data → re-publish ke topic terproses → buffer ke PostgreSQL setiap 1 detik |
| Backend Technology | **Java Spring Boot** — REST API + WebSocket (STOMP over SockJS) untuk streaming telemetri ke dashboard, endpoint command forward ke MQTT |
| Frontend Technology | **React** + Three.js / Canvas API — peta 2D top-view gudang, posisi robot real-time, panel kontrol per robot, grafik telemetri |
| Database | **PostgreSQL** (log telemetri + log command + sesi robot) dengan TimescaleDB extension untuk query time-series efisien |
| Deployment Method | **PM2 + Nginx + Certbot** — Spring Boot JAR + React build di-serve via Nginx dengan HTTPS, PM2 menjaga proses Java tetap hidup |

**Fitur Wajib:**
1. Peta 2D top-view gudang: 3 ikon robot bergerak sesuai kalkulasi posisi dead reckoning, update 5 Hz via WebSocket
2. Panel kontrol per robot: tombol maju/mundur/kiri/kanan/stop yang mengirim command MQTT dengan robot ID
3. Dashboard telemetri per robot: gauge kecepatan, kompas orientasi (yaw), indikator baterai, counter obstacle detected
4. Log command: setiap command yang dikirim operator tercatat dengan timestamp, robot target, dan perintah
5. Replay session: pilih sesi dari database, lihat ulang gerakan robot di peta (playback historis dead reckoning)

**Kriteria Keberhasilan:**
- Telemetri 3 robot terpublikasi bersamaan ke MQTT pada 5 Hz dan diterima backend tanpa data loss signifikan (< 5% packet loss)
- Peta React diperbarui real-time dan menampilkan pergerakan robot yang koheren dengan encoder ESP32
- Command dari React berhasil diteruskan ke MQTT dan dieksekusi oleh ESP32 (LED/serial debug) dalam < 200 ms
- HTTPS via Certbot aktif dan dashboard dapat diakses dari browser mobile

**Tingkat Kesulitan:** ⭐⭐⭐⭐⭐

---

## C. PANDUAN UMUM PENGERJAAN PROYEK

### C.1 Arsitektur Sistem yang Harus Diimplementasikan

Setiap proyek **wajib** mengimplementasikan arsitektur berikut secara end-to-end:

```
┌──────────────────────────────────────────────────────────────────┐
│  EDGE LAYER                                                      │
│  ┌─────────────┐     MQTT Publish      ┌──────────────────────┐  │
│  │   ESP32     │ ─────────────────────►│   MQTT Broker        │  │
│  │  + Sensor   │ ◄─────────────────────│  (Mosquitto/HiveMQ)  │  │
│  │  + Actuator │     MQTT Subscribe    └──────────────────────┘  │
│  └─────────────┘                                  │              │
│                                                   │              │
│  ┌─────────────────────────────────────────────── │ ───────────┐ │
│  │  LAPTOP EDGE (Python)          Subscribe       │            │ │
│  │  - paho-mqtt subscriber   ◄───────────────────►│            │ │
│  │  - Data processing / rule engine               │            │ │
│  │  - Alert logic                                 │            │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                              │
                    HTTP / WebSocket
                              │
┌──────────────────────────────────────────────────────────────────┐
│  SERVER LAYER                                                    │
│  ┌──────────────────┐         ┌───────────────────────────────┐  │
│  │  Backend API     │ ◄──────►│  Database                     │  │
│  │  (REST + WS)     │         │  (Time-series / Relational /  │  │
│  └──────────────────┘         │   Document / Cache)           │  │
│          │                    └───────────────────────────────┘  │
│          │ Serve / Proxy                                          │
│  ┌───────▼──────────────────────────────────────────────────┐    │
│  │  Frontend Dashboard (Vue.js / React / Angular)           │    │
│  │  - Real-time visualisasi                                 │    │
│  │  - Kontrol actuator                                      │    │
│  │  - Laporan historis                                      │    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
                              │
                    Deployment (PM2/Nginx/ngrok/certbot)
```

### C.2 Struktur Folder Proyek yang Disarankan

```
proyek-modul04-kelompok-XX/
├── esp32/                          # Kode PlatformIO ESP32
│   ├── src/
│   │   └── main.cpp
│   ├── include/
│   └── platformio.ini
├── python-edge/                    # Script Python edge processing
│   ├── mqtt_subscriber.py
│   ├── rule_engine.py
│   └── requirements.txt
├── backend/                        # Backend API (Spring Boot / FastAPI / Node.js / dll)
│   ├── src/
│   └── (build files sesuai platform)
├── frontend/                       # Frontend (Vue.js / React / Angular)
│   ├── src/
│   └── package.json
├── docs/
│   ├── arsitektur.png
│   └── demo.mp4                    # Video demo sistem berjalan
└── README.md                       # Instruksi setup & menjalankan sistem
```

### C.3 Pembagian Tugas yang Disarankan

| No | Anggota | Tanggung Jawab Utama |
|----|---------|---------------------|
| 1 | | ESP32 firmware (PlatformIO): sensor reading, MQTT publish/subscribe, actuator control |
| 2 | | Python edge: MQTT subscriber, data processing, rule engine, alert logic |
| 3 | | Backend API + Database: endpoint REST, WebSocket, schema database, query |
| 4 | | Frontend dashboard: UI/UX, visualisasi real-time, integrasi API, deployment |

*Catatan: Pada kelompok < 4 orang, tanggung jawab dapat digabung. Dokumentasikan pembagian tugas aktual di laporan.*

---

## D. DELIVERABLES (YANG HARUS DIKUMPULKAN)

### D.1 File Digital

| No | File / Artefak | Format | Keterangan |
|----|---------------|--------|-----------|
| 1 | Source code lengkap | Folder ZIP / GitHub repo link | Semua lapisan: ESP32, Python, backend, frontend |
| 2 | Video demo sistem berjalan | MP4, maks. 5 menit | Tunjukkan alur end-to-end dari sensor hingga dashboard |
| 3 | Laporan teknis kelompok | PDF, maks. 20 halaman | Lihat D.2 |
| 4 | File README.md | Markdown | Instruksi setup dan menjalankan sistem dari awal |
| 5 | Skema wiring ESP32 | PNG / PDF | Diagram koneksi sensor dan aktuator ke ESP32 |

### D.2 Isi Laporan Teknis

1. Cover: judul proyek, nama kelompok, anggota + NIM
2. Latar belakang dan skenario masalah (ringkasan cerita proyek)
3. Diagram arsitektur sistem lengkap
4. Penjelasan setiap lapisan: ESP32, Python edge, backend, frontend, database
5. Skema wiring dan daftar komponen hardware
6. Screenshot dashboard dalam kondisi berjalan (minimal 5 screenshot)
7. Penjelasan fitur wajib yang berhasil diimplementasikan (checklist)
8. Kendala yang ditemui selama pengerjaan dan solusinya
9. Pembagian tugas aktual per anggota
10. Kesimpulan dan saran pengembangan lanjutan

---

## E. RUBRIK PENILAIAN

**Total: 100 poin**

| No | Kriteria | Bobot | Indikator |
|----|---------|-------|----------|
| 1 | Fungsionalitas sistem end-to-end (ESP32 → MQTT → Backend → Frontend) | 30 | Semua alur data berjalan tanpa error saat demo |
| 2 | Implementasi seluruh fitur wajib (5 fitur per proyek) | 25 | Checklist fitur, dibuktikan di demo/screenshot |
| 3 | Kualitas kode (struktur, komentar, error handling) | 15 | Review source code |
| 4 | Kualitas dashboard / UX frontend | 10 | Responsif, informatif, estetis |
| 5 | Deployment berjalan sesuai metode yang dipilih | 10 | Nginx/PM2/ngrok aktif, dapat diakses dari luar localhost |
| 6 | Laporan teknis (kelengkapan, kejelasan, diagram) | 10 | Sesuai format D.2 |
| **TOTAL** | | **100** | |

---

## F. REFERENSI TEKNOLOGI

| Teknologi | Dokumentasi Resmi |
|-----------|------------------|
| ESP32 + PlatformIO | https://docs.platformio.org |
| Mosquitto MQTT Broker | https://mosquitto.org/documentation |
| paho-mqtt Python | https://eclipse.dev/paho/index.php?page=clients/python/index.php |
| Python FastAPI | https://fastapi.tiangolo.com |
| Java Spring Boot | https://spring.io/projects/spring-boot |
| Node.js Express | https://expressjs.com |
| C# ASP.NET Core | https://learn.microsoft.com/en-us/aspnet/core |
| Vue.js | https://vuejs.org |
| React | https://react.dev |
| Angular | https://angular.dev |
| InfluxDB | https://docs.influxdata.com/influxdb/v2 |
| PostgreSQL | https://www.postgresql.org/docs |
| MongoDB | https://www.mongodb.com/docs |
| Redis | https://redis.io/docs |
| PM2 | https://pm2.keymetrics.io/docs |
| Nginx | https://nginx.org/en/docs |
| ngrok | https://ngrok.com/docs |
| Certbot (Let's Encrypt) | https://certbot.eff.org |

---

*Dokumen ini dibuat untuk Praktikum Mekatronika dan Robotika — Modul 04 IoT WebServer MQTT ESP32. Hubungi dosen pengampu jika ada pertanyaan terkait pemilihan proyek atau spesifikasi teknis.*
