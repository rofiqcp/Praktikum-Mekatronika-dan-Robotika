# PROJECT MODUL 05: IoT PLC AI MODBUS – 10 OPSI PROJECT

**Program Studi:** Teknik Mekatronika dan Robotika  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 05 – IoT PLC AI Modbus  
**Pengerjaan:** Per Kelompok (Maks. 4 Orang)  
**Batas Waktu:** Sesuai jadwal dosen

---

## INSTRUKSI UMUM

Setiap kelompok memilih **satu project** dari 10 opsi berikut. Project merupakan pengembangan dan improvisasi dari percobaan-percobaan yang telah dilakukan pada sesi praktikum. Setiap project harus:

1. **Menggunakan PLC** (Schneider TM221 atau Omron CP2E) sebagai kontroler lapangan
2. **Menggunakan edge device** (MiniPC Python dan/atau ESP32 PlatformIO) sebagai gateway
3. **Mengirim data ke server** (MQTT broker dan/atau REST API)
4. **Menampilkan dashboard** visualisasi data secara real-time
5. **Memiliki fitur monitoring dan kontrol** dari jarak jauh (remote monitoring/control)

---

## RUBRIK PENILAIAN PROJECT

| Aspek | Bobot | Deskripsi |
|-------|-------|-----------|
| Fungsionalitas | 35% | Sistem bekerja sesuai spesifikasi project |
| Integrasi PLC-Edge-Server | 25% | Komunikasi Modbus, pengiriman data ke server berjalan |
| Inovasi dan kompleksitas | 20% | Fitur tambahan di luar percobaan dasar |
| Dokumentasi dan presentasi | 10% | Laporan teknis + demo |
| Keandalan sistem | 10% | Sistem stabil dalam demo selama 10 menit |

---

## PROJECT 1 – SISTEM MONITORING KUALITAS AIR INDUSTRI

### Latar Belakang

PT Aquapure Indonesia adalah perusahaan pengolahan air bersih yang memasok air industri ke pabrik-pabrik di kawasan industri. Saat ini sistem monitoring kualitas air di 5 titik pengukuran masih dilakukan secara manual: teknisi harus berkeliling setiap 2 jam untuk mencatat nilai pH, turbiditas, klorin, dan debit aliran di setiap titik. Akibatnya, insiden air tidak memenuhi standar baru diketahui 2–3 jam setelah terjadi.

### Tugas Kelompok

Anda diminta merancang sistem monitoring kualitas air berbasis IoT untuk PT Aquapure. Sistem harus mampu:

1. **PLC TM221/CP2E:** Membaca sensor pH (4–20 mA), sensor turbiditas (0–10V), dan sensor debit (pulse counter) yang terhubung ke input analog dan digital PLC. PLC menjalankan logika alarm: jika pH < 6.5 atau > 8.5, aktifkan output alarm relay.

2. **MiniPC Python:** Berkomunikasi dengan PLC via Modbus RTU, membaca nilai sensor setiap 30 detik, mengkonversi nilai ADC ke satuan fisik (pH, NTU, L/menit), lalu publish ke MQTT broker dengan topic `aquapure/titik{n}/sensor`.

3. **ESP32:** Sebagai remote sensor node tambahan di titik yang tidak memiliki jaringan kabel. ESP32 membaca sensor sederhana (simulasi dengan potensiometer) dan kirim ke MQTT broker via WiFi.

4. **Server dan Dashboard:** Grafana/Node-RED menampilkan: trend pH, turbiditas, dan debit real-time; alert visual jika parameter out-of-range; laporan harian otomatis.

### Spesifikasi Teknis yang Harus Dipenuhi

- Sampling interval: 30 detik
- Trigger alarm jika pH keluar rentang 6.5–8.5 (notifikasi ke MQTT topic `aquapure/alarm`)
- Simpan data 7 hari ke database
- Dashboard menampilkan minimal: 3 gauge, 1 chart time-series, 1 tabel alarm

### Pertanyaan Studi Kasus

1. Bagaimana Anda mengkonversi nilai ADC 0–4095 dari PLC TM221 ke nilai pH 0–14?
2. Apa yang terjadi jika koneksi Modbus terputus? Bagaimana strategi failsafe-nya?
3. Hitung kapasitas storage yang dibutuhkan untuk menyimpan data 7 hari dengan sampling 30 detik dan 5 parameter.

---

## PROJECT 2 – SISTEM KONTROL CONVEYOR OTOMATIS DENGAN REMOTE HMI

### Latar Belakang

PT ElectroPackage adalah pabrik elektronik yang memiliki lini produksi conveyor untuk memindahkan papan PCB antar stasiun kerja. Manajer produksi ingin dapat memantau dan mengendalikan kecepatan conveyor serta menghitung throughput (jumlah produk per jam) dari ruang kontrol yang terletak 50 meter dari lantai produksi — bahkan dari smartphone saat perjalanan dinas.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Program Ladder mengontrol kecepatan motor conveyor melalui VFD (simulasikan dengan nilai analog output 0–10V atau PWM). PLC menghitung counter produk dari sensor proximity (%IW pulse counter). Kecepatan setpoint disimpan di %MW0 (dapat diubah dari Modbus).

2. **MiniPC Python:** Gateway Modbus TCP → MQTT. Baca status conveyor, kecepatan aktual, counter produk setiap 1 detik. Publish ke MQTT. Terima perintah dari MQTT topic `conveyor/cmd` untuk mengubah setpoint kecepatan dan start/stop.

3. **ESP32:** Sebagai HMI portabel dengan OLED display yang menampilkan status conveyor dan counter. ESP32 subscribe ke MQTT dan tampilkan di OLED. Tombol fisik pada ESP32 untuk emergency stop (publish ke `conveyor/cmd/estop`).

4. **Web Dashboard:** REST API FastAPI menyediakan endpoint untuk frontend web sederhana (HTML/JS) yang bisa diakses dari browser smartphone — menampilkan status real-time dan tombol kontrol.

### Spesifikasi Teknis

- Kontrol kecepatan: 3 level (Lambat 20%, Sedang 60%, Cepat 100%)
- Emergency stop via ESP32 harus merespons dalam < 500 ms
- Counter produk terakumulasi per shift (8 jam), reset otomatis setiap shift
- Simpan log event (start/stop/estop/change speed) ke database

---

## PROJECT 3 – SISTEM MONITORING ENERGI PABRIK TERPADU

### Latar Belakang

PT PowerSave Manufaktur ingin mengurangi konsumsi energi listrik pabriknya sebesar 20% dalam setahun. Namun mereka tidak memiliki data konsumsi energi per mesin. Dengan memasang energy meter pada setiap panel daya dan menghubungkannya ke PLC via Modbus, mereka dapat mengumpulkan data kWh, kW, kVAR, cos φ, dan tegangan setiap mesin secara real-time.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Membaca data dari 3 energy meter (simulasikan dengan holding register 40001–40030) yang terhubung via Modbus RTU (PLC sebagai Modbus Master ke energy meter, sekaligus sebagai Modbus Slave untuk MiniPC). Hitung total kW dari 3 mesin dan simpan di %MW50.

2. **MiniPC Python:** Baca data dari PLC (kW, kVAR, kWh per mesin) setiap 5 detik. Kalkulasi Power Factor: `cos_phi = kW / sqrt(kW²+kVAR²)`. Publish ke MQTT. Deteksi anomali konsumsi: jika kW mesin melebihi baseline 20%, kirim alert.

3. **ESP32:** Menampilkan total konsumsi kW saat ini pada display 7-segment atau OLED. LED merah berkedip jika total daya > threshold yang diset.

4. **Dashboard Grafana:** Panel: kW per mesin (stacked area chart), total kWh per hari (bar chart), power factor trend, alert anomali. Tambahkan perhitungan estimasi biaya listrik (Rp/kWh × kWh).

### Fitur Tambahan (Nilai Bonus)

Implementasikan algoritma deteksi anomali konsumsi energi menggunakan Isolation Forest (scikit-learn) yang ditraining dengan data historis 7 hari. Model diinferensikan setiap 5 menit oleh MiniPC Python.

---

## PROJECT 4 – SISTEM GREENHOUSE CERDAS BERBASIS PLC-IoT

### Latar Belakang

Koperasi Petani Hortikultura "Agro Maju" ingin mengotomasi sistem pertanian greenhouse mereka. Selama ini penyiraman, pengaturan suhu, dan kontrol ventilasi dilakukan manual, mengakibatkan produktivitas tidak konsisten. Dengan anggaran terbatas, mereka meminta solusi IoT berbasis PLC bekas (TM221) yang sudah mereka miliki.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Program kontrol otomatis:
   - Penyiraman: aktifkan pompa (Q0.0) jika kelembaban tanah < 40% (%MW0 < 1638)
   - Ventilasi: buka kipas (Q0.1) jika suhu > 30°C (%MW1 > sensor threshold)
   - Pencahayaan: nyalakan lampu grow (Q0.2) jika intensitas cahaya < 500 lux, hanya pada jam 06:00–18:00 (gunakan RTC PLC)
   - Semua nilai threshold dapat diubah via Modbus (holding register)

2. **MiniPC Python:** Gateway + analisis. Baca 5 sensor: suhu, kelembaban udara, kelembaban tanah, cahaya, CO2 (simulasi dengan potentiometer/angka acak berpolanya). Kirim ke MQTT. Setiap hari pada pukul 23:00, generate laporan harian PDF/CSV tentang kondisi lingkungan.

3. **ESP32:** Node sensor otonom. ESP32 membaca DHT22 (suhu & kelembaban) dan kirim ke MiniPC via MQTT. Setiap 10 menit ESP32 juga mengirim heartbeat. Jika heartbeat tidak diterima > 30 menit, MiniPC kirim alert.

4. **Dashboard:** Node-RED dengan tampilan: peta greenhouse (layout blok tanaman), indikator status setiap aktuator, trend 24 jam semua sensor.

### Pertanyaan Studi Kasus

Bagaimana mengimplementasikan logika waktu di PLC TM221 untuk mematikan lampu grow secara otomatis setelah pukul 18:00? Jelaskan blok fungsi apa yang digunakan.

---

## PROJECT 5 – SISTEM PENGOLAHAN AIR LIMBAH INDUSTRI REAL-TIME

### Latar Belakang

Perusahaan kimia PT ChemClean diwajibkan oleh regulasi untuk memantau kualitas air limbah sebelum dibuang ke sungai. Inspektur lingkungan sewaktu-waktu dapat mengakses data monitoring secara online. Jika parameter melebihi baku mutu (pH > 9 atau COD > 100 mg/L), sistem harus otomatis menutup valve pembuangan dan mengirim notifikasi ke regulator.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Kontrol valve pembuangan (Q0.0) dan pompa sirkulasi (Q0.1). Baca nilai pH dan COD (simulasi dengan potentiometer) dari AI. Logika: jika pH > 9 ATAU nilai COD register > 100 (dalam satuan yang disepakati), tutup valve dan aktifkan alarm (Q0.2).

2. **MiniPC Python:** Gateway + compliance reporting. Setiap pembacaan di luar baku mutu, catat timestamp, nilai, dan durasi kejadian ke database PostgreSQL/SQLite. Generate laporan bulanan otomatis (format JSON/CSV) yang dapat didownload oleh regulator.

3. **ESP32:** Panel kontrol fisik darurat di pintu pabrik. Tampilkan status: AMAN (LED hijau) atau PELANGGARAN (LED merah berkedip + buzzer). ESP32 subscribe ke MQTT topic `chemclean/status`.

4. **REST API + Webhook:** Ketika terjadi pelanggaran, MiniPC Python mengirim HTTP POST webhook ke URL yang telah dikonfigurasi (simulasikan dengan Webhook.site atau ntfy.sh) sebagai notifikasi ke regulator.

---

## PROJECT 6 – SISTEM PREDICTIVE MAINTENANCE MOTOR INDUSTRI

### Latar Belakang

PT MetalCraft memiliki 6 motor listrik 3 fasa yang menggerakkan mesin-mesin produksi. Dalam setahun terakhir, 3 kali terjadi kerusakan motor mendadak yang menyebabkan downtime produksi total 72 jam dengan kerugian Rp 500 juta. Engineering manager ingin sistem yang dapat memprediksi kerusakan motor 24–48 jam sebelum terjadi berdasarkan data arus, getaran, dan suhu.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Baca nilai arus motor (dari current transformer, via AI 4–20mA), status on/off motor, dan suhu motor (dari thermocouple via modul AI). Simpan ke holding register. Hitung running hours motor (counter di PLC).

2. **MiniPC Python:** 
   - **Fase training (offline):** Kumpulkan data baseline 7 hari saat motor normal → train Isolation Forest model → simpan model ke file pickle.
   - **Fase monitoring (online):** Baca data real-time dari PLC setiap 1 detik, inferensikan model → jika anomali terdeteksi lebih dari 5× dalam 10 menit, publish alert ke MQTT `maintenance/alert`.

3. **ESP32:** Node sensor getaran (gunakan MPU6050 accelerometer). Baca RMS getaran setiap detik, kirim ke MQTT. MiniPC Python mengintegrasikan data getaran ESP32 dengan data arus dari PLC sebagai fitur gabungan untuk deteksi anomali.

4. **Dashboard:** Grafana menampilkan: health score motor (0–100%), trend arus dan getaran, riwayat alert, prediksi waktu service berikutnya.

### Fitur AI yang Harus Diimplementasikan

Model Isolation Forest dengan minimal 3 fitur input: `[arus_rms, suhu_motor, getaran_rms]`. Tampilkan confusion matrix dari validasi model menggunakan data historis.

---

## PROJECT 7 – SISTEM MANAJEMEN PARKIR OTOMATIS

### Latar Belakang

Gedung perkantoran "Tower Nusantara" memiliki 3 lantai parkir dengan total 150 slot. Pengelola parkir mengeluh karena sering terjadi penumpukan kendaraan di pintu masuk karena tidak ada informasi slot kosong. Pemilik gedung meminta sistem manajemen parkir otomatis yang menampilkan informasi slot kosong di display outdoor dan dapat dipantau via aplikasi mobile.

### Tugas Kelompok

1. **PLC TM221/CP2E:** 
   - Baca sensor loop induktif (simulasi dengan DI) dari 10 slot parkir (gunakan 10 input digital)
   - Counter kendaraan masuk (%MW0++) saat sensor looping input aktif
   - Counter kendaraan keluar (%MW1++) saat sensor looping output aktif
   - Slot tersedia = total - counter masuk + counter keluar, simpan di %MW2
   - Kontrol barrier gate (Q0.0 = buka, Q0.1 = tutup) berdasarkan perintah Modbus

2. **MiniPC Python:** Gateway Modbus TCP → MQTT. Publish status setiap slot, counter, dan slot tersedia. Terima perintah buka/tutup gate dari MQTT. Simpan log entry/exit kendaraan ke database.

3. **ESP32 (Display Unit):** ESP32 dengan 7-segment atau OLED menampilkan "SLOT TERSEDIA: XX". Subscribe ke MQTT dan update display secara real-time. Letakkan di pintu masuk parkir.

4. **Web App Dashboard:** FastAPI + HTML/JS sederhana yang menampilkan layout visual 10 slot parkir (hijau = kosong, merah = terisi), counter real-time, dan tombol kontrol gate. Dapat diakses dari browser smartphone.

---

## PROJECT 8 – SISTEM MONITORING TANGKI DAN DISTRIBUSI BAHAN BAKAR

### Latar Belakang

PT LogistikEnergi mengelola 4 tangki bahan bakar (solar/biodiesel) dengan kapasitas berbeda untuk memasok truk-truk armadanya. Pengiriman bahan bakar dari supplier harus diorder sebelum tangki mencapai level kritis. Selama ini monitoring level tangki masih manual dengan tongkat ukur setiap pagi. Akibatnya, 3 kali dalam setahun armada truk tidak dapat beroperasi karena BBM habis mendadak.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Baca level tangki dari 4 sensor level (simulasi: 4 potentiometer ke AI). Konversi nilai ADC ke liter sesuai kalibrasi tangki masing-masing. Hitung total volume tersedia. Jika salah satu tangki < 20% kapasitas, aktifkan output alarm (Q0.x). Simpan nilai liter di holding register.

2. **MiniPC Python:** Gateway + forecasting. Baca level setiap 5 menit. Hitung laju konsumsi harian (moving average 7 hari). Prediksi kapan tangki akan mencapai level kritis (linear extrapolation atau simple regression). Publish prediksi ke MQTT `fuel/prediction`.

3. **ESP32:** Panel display di ruang dispatcher. OLED menampilkan level 4 tangki dalam format bar graph. LED merah untuk tangki yang < 20%. Tombol untuk request resupply yang mengirim pesan ke MQTT `fuel/resupply_request`.

4. **Alert System:** Ketika sistem memprediksi tangki akan habis dalam < 48 jam, kirim notifikasi HTTP ke ntfy.sh atau email (via SMTP) ke manajer logistik secara otomatis.

---

## PROJECT 9 – SISTEM KONTROL DAN MONITORING HVAC GEDUNG

### Latar Belakang

Gedung kantor "Green Office Center" ingin mengoptimalkan konsumsi energi sistem HVAC (Heating, Ventilation, Air Conditioning). Saat ini AC di setiap ruangan beroperasi pada suhu yang sama (20°C) sepanjang hari tanpa memperhatikan occupancy. Dengan sistem kontrol cerdas, suhu dapat diatur berdasarkan jumlah orang di ruangan dan jam kerja, menghemat energi 30–40%.

### Tugas Kelompok

1. **PLC TM221/CP2E:** Kontrol 4 zona HVAC (simulasi: 4 output relay untuk 4 AC split). Baca suhu setiap zona dari sensor (simulasi: potentiometer ke AI). Setpoint suhu per zona dapat diubah via Modbus holding register. Logika: Kompressor ON/OFF berdasarkan selisih suhu aktual vs setpoint ± 0.5°C.

2. **MiniPC Python:** Scheduling + gateway. Terapkan jadwal otomatis:
   - 08:00–09:00: ramp up (suhu turun dari 26°C ke 22°C)
   - 09:00–17:00: mode kerja (setpoint 22°C)
   - 17:00–18:00: ramp down (suhu naik ke 26°C)
   - 18:00–08:00: standby (setpoint 28°C)
   Kirim setpoint ke PLC via Modbus sesuai jadwal.

3. **ESP32 (Room Controller):** ESP32 dengan sensor DHT22 sebagai termostat lokal. Tampilkan suhu dan setpoint di OLED. Tombol +/- untuk adjust setpoint secara lokal (override sementara 2 jam). Kirim override request ke MQTT.

4. **Dashboard Energi:** Hitung estimasi penghematan energi: bandingkan kWh mode manual vs mode cerdas (simulasi dengan data historis). Tampilkan di Grafana sebagai "savings dashboard".

---

## PROJECT 10 – SISTEM SCADA MINI UNTUK WATER TREATMENT PLANT

### Latar Belakang

PDAM Kabupaten Maju sedang membangun Instalasi Pengolahan Air (IPA) skala kecil (kapasitas 20 L/detik) untuk melayani desa-desa terpencil. Dengan anggaran terbatas, mereka tidak dapat membeli sistem SCADA komersial yang harganya ratusan juta rupiah. Tim engineer-nya meminta solusi SCADA open-source berbasis PLC TM221 + Raspberry Pi + Grafana yang bisa dibangun sendiri.

### Tugas Kelompok

Rancang dan implementasikan sistem SCADA mini untuk water treatment plant dengan:

1. **PLC TM221/CP2E – Kontrol Proses:**
   - Pompa intake (Q0.0): on/off berdasarkan level bak penampungan awal
   - Pompa dosing klorin (Q0.1): proportional terhadap debit (PWM analog output)
   - Pompa distribusi (Q0.2): on/off berdasarkan level tandon distribusi
   - Valve bypass (Q0.3): otomatis buka saat fault
   - 4 sensor level tangki (AI 0–3): baca level dan konversi ke %
   - 1 flow meter (pulse counter DI): hitung debit L/menit

2. **MiniPC Python – SCADA Core:**
   - Polling semua data dari PLC via Modbus TCP setiap 1 detik
   - Publish ke MQTT untuk dashboard
   - Simpan ke InfluxDB atau SQLite
   - State machine: NORMAL, WARNING (level < 30%), ALARM (level < 10%), FAULT
   - Transition logic: NORMAL→WARNING→ALARM→FAULT dan kembali ke NORMAL
   - Log semua state transition dengan timestamp

3. **ESP32 – Remote I/O Node:**
   - Baca sensor klorin residual (simulasi: potentiometer)
   - Baca sensor turbiditas outlet (simulasi: potentiometer)
   - Kirim ke MQTT topic `wtp/quality`
   - Terima perintah dari MiniPC untuk LED status lokal

4. **Dashboard SCADA:**
   - Node-RED atau Grafana dengan tampilan P&ID (Piping and Instrumentation Diagram) sederhana
   - Semua pompa dan valve ditampilkan dengan indikator on/off
   - Level tangki ditampilkan sebagai icon tangki dengan fill level
   - Trend kualitas air (pH, klorin, turbiditas) 24 jam terakhir
   - Panel alarm: semua active alarm dan history 7 hari
   - Kontrol manual: tombol override untuk start/stop pompa dari dashboard

### Deliverable Wajib

1. Laporan teknis: arsitektur sistem, flowchart logika kontrol, register map Modbus
2. Source code: semua program (PLC, Python, ESP32, Node-RED flow)
3. Demo live: sistem berjalan minimal 10 menit tanpa error di hadapan dosen
4. Video demo: rekaman demo 5 menit
5. Presentasi: 10 menit + 5 menit Q&A

---

## TEMPLATE LAPORAN PROJECT

Setiap kelompok menyerahkan laporan dengan struktur:

```
BAB I: PENDAHULUAN
  1.1 Latar Belakang (sesuai skenario project yang dipilih)
  1.2 Rumusan Masalah
  1.3 Tujuan Project
  1.4 Batasan Masalah

BAB II: TINJAUAN PUSTAKA
  2.1 Protokol Modbus RTU dan TCP
  2.2 PLC [sesuai yang digunakan]
  2.3 MQTT dan REST API
  2.4 Dashboard IoT

BAB III: PERANCANGAN SISTEM
  3.1 Arsitektur Sistem
  3.2 Hardware Architecture (block diagram)
  3.3 Software Architecture
  3.4 Register Map Modbus
  3.5 Flowchart Program PLC
  3.6 Flowchart Program Edge Device

BAB IV: IMPLEMENTASI
  4.1 Konfigurasi PLC
  4.2 Program PLC (listing dengan penjelasan)
  4.3 Program MiniPC Python (listing dengan penjelasan)
  4.4 Program ESP32 PlatformIO (listing dengan penjelasan)
  4.5 Konfigurasi Server (Mosquitto/FastAPI/Node-RED)
  4.6 Dashboard

BAB V: PENGUJIAN DAN ANALISIS
  5.1 Hasil Pengujian Komunikasi Modbus
  5.2 Hasil Pengujian Pengiriman Data ke Server
  5.3 Hasil Pengujian Dashboard
  5.4 Analisis Performa Sistem
  5.5 Analisis Masalah yang Ditemukan dan Solusinya

BAB VI: KESIMPULAN DAN SARAN

DAFTAR PUSTAKA

LAMPIRAN
  - Source code lengkap
  - Foto/Screenshot dokumentasi
  - Video link (QR code atau URL)
```

---

## JADWAL PROJECT

| Tahap | Kegiatan | Waktu |
|-------|---------|-------|
| Week 1 | Pemilihan project, pembagian tugas, perancangan awal | 2 jam |
| Week 2 | Konfigurasi PLC dan program Ladder | 4 jam |
| Week 3 | Program edge device (Python + ESP32) | 4 jam |
| Week 4 | Integrasi server (MQTT/REST) + dashboard | 4 jam |
| Week 5 | Pengujian, debugging, perbaikan | 4 jam |
| Week 6 | Finalisasi laporan + demo presentasi | 4 jam |

---

*Project ini merupakan tugas resmi Modul 05 Praktikum Mekatronika dan Robotika.*  
*Plagiarisme dan kecurangan akan mengakibatkan nilai 0 untuk seluruh anggota kelompok.*
