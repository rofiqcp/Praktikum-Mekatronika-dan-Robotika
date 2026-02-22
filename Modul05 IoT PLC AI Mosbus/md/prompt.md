# PROMPT NOTEBOOKLM – MODUL 05: IoT PLC AI MODBUS
## Slide 1–45: Komunikasi Modbus PLC dengan Edge Device dan Server

**Tujuan Penggunaan:**  
Prompt ini digunakan untuk membuat presentasi/slide interaktif menggunakan NotebookLLM (Google NotebookLM) berdasarkan materi Modul 05. Salin setiap prompt ke NotebookLLM sesuai urutan slide.

---

### SLIDE 1 – JUDUL DAN OVERVIEW

**Prompt:**
```
Buatkan slide judul untuk presentasi dengan judul:
"KOMUNIKASI MODBUS PLC DENGAN EDGE DEVICE DAN SERVER IoT"
Subtitle: Modul 05 Praktikum Mekatronika dan Robotika
Tambahkan poin overview: Modbus RTU, Modbus TCP, PLC Schneider TM221, PLC Omron CP2E, 
MiniPC Python, ESP32 PlatformIO, MQTT, REST API, Dashboard IoT.
Buat menarik dengan ikon industri 4.0.
```

---

### SLIDE 2 – LATAR BELAKANG: INDUSTRI 4.0

**Prompt:**
```
Buat slide tentang latar belakang Industri 4.0 dalam konteks otomasi pabrik.
Jelaskan tantangan integrasi PLC lama (protokol Modbus) dengan sistem cloud modern.
Tampilkan diagram sederhana: PLC → Edge Device → Cloud.
Sertakan statistik: lebih dari 60% PLC di industri masih menggunakan Modbus.
```

---

### SLIDE 3 – APA ITU EDGE DEVICE?

**Prompt:**
```
Buat slide yang menjelaskan konsep Edge Device dalam IIoT (Industrial IoT).
Tampilkan 5 fungsi utama edge device: Protocol Bridge, Data Preprocessing, 
Local Control, Edge AI, Data Buffering.
Gunakan infografik dengan ikon untuk setiap fungsi.
Contoh edge device: Raspberry Pi, ESP32, Industrial PC.
```

---

### SLIDE 4 – ARSITEKTUR SISTEM KESELURUHAN

**Prompt:**
```
Buat slide arsitektur sistem IoT industri lengkap dengan diagram blok:
Lapangan: PLC TM221/CP2E ↔ RS-485/Ethernet ↔ Edge Device (MiniPC/ESP32)
Cloud/Server: MQTT Broker, REST API, Database, Dashboard
Gunakan warna berbeda untuk setiap lapisan (field, edge, cloud).
Tampilkan protokol yang digunakan di setiap koneksi.
```

---

### SLIDE 5 – SEJARAH DAN STANDAR MODBUS

**Prompt:**
```
Buat slide timeline sejarah Modbus:
1979: Dikembangkan oleh Modicon
1996: Modbus TCP/IP
2002: Dipublikasikan sebagai open standard oleh modbus.org
Saat ini: salah satu protokol industri paling populer (>60% instalasi global)
Tampilkan logo/gambar Schneider Electric (pemilik Modicon).
Sertakan alasan Modbus masih relevan: sederhana, open, kompatibel luas, robust.
```

---

### SLIDE 6 – MODEL DATA MODBUS: 4 TIPE REGISTER

**Prompt:**
```
Buat slide tabel model data Modbus dengan 4 jenis tabel:
1. Coil (Boolean R/W, alamat 00001-09999, FC01/05/15)
2. Discrete Input (Boolean R, alamat 10001-19999, FC02)
3. Input Register (16-bit R, alamat 30001-39999, FC04)
4. Holding Register (16-bit R/W, alamat 40001-49999, FC03/06/16)
Gunakan tabel berwarna untuk setiap jenis data.
Tambahkan penjelasan analogi: Coil = saklar lampu, Register = display angka.
```

---

### SLIDE 7 – FUNCTION CODES MODBUS

**Prompt:**
```
Buat slide daftar Function Code Modbus yang paling sering digunakan:
FC01: Read Coils
FC02: Read Discrete Inputs
FC03: Read Holding Registers
FC04: Read Input Registers
FC05: Write Single Coil
FC06: Write Single Register
FC15: Write Multiple Coils
FC16: Write Multiple Registers
Tampilkan dengan tabel bericon, highlight FC03 dan FC06 sebagai yang paling umum.
```

---

### SLIDE 8 – FORMAT FRAME MODBUS RTU

**Prompt:**
```
Buat slide yang menampilkan format frame Modbus RTU secara visual:
[Slave ID | Function Code | Data Address | Data | CRC]
Berikan ukuran setiap field dalam byte.
Tambahkan contoh konkret: request baca 3 register dari slave ID 1 mulai alamat 0.
Frame request: 01 03 00 00 00 03 05 CB
Frame response: 01 03 06 [data] [CRC]
Jelaskan fungsi CRC untuk deteksi error.
```

---

### SLIDE 9 – FORMAT FRAME MODBUS TCP

**Prompt:**
```
Buat slide yang menampilkan format frame Modbus TCP:
MBAP Header: Transaction ID (2B) | Protocol ID (2B=0x0000) | Length (2B) | Unit ID (1B)
PDU: Function Code (1B) | Data (variabel)
Bandingkan dengan Modbus RTU: tidak ada CRC di TCP (digantikan TCP error checking).
Port default: 502
Tampilkan diagram enkapsulasi: PDU Modbus dalam paket TCP/IP.
```

---

### SLIDE 10 – ARSITEKTUR MASTER-SLAVE MODBUS

**Prompt:**
```
Buat slide yang menjelaskan arsitektur Master-Slave Modbus:
- Master (Edge Device): selalu memulai komunikasi
- Slave (PLC): menunggu dan merespons
- 1 jaringan RTU: 1 master, maks 247 slave
- Modbus TCP: bisa multiple master paralel
Tampilkan diagram jaringan dengan 1 master dan 3 slave.
Tampilkan alur request-response dengan panah.
```

---

### SLIDE 11 – RS-485: PHYSICAL LAYER MODBUS RTU

**Prompt:**
```
Buat slide tentang RS-485 sebagai physical layer Modbus RTU:
Karakteristik: differential signal A+/B-, jarak maks 1200m, kecepatan 300bps-10Mbps,
maks 32 perangkat, terminasi 120Ω.
Tampilkan diagram wiring: Master - Slave 1 - Slave 2 ... - Slave N
dengan kabel A(+), B(-), GND.
Tunjukkan posisi resistor terminasi 120Ω di kedua ujung bus.
Bandingkan dengan RS-232: kenapa RS-485 lebih baik untuk industri.
```

---

### SLIDE 12 – PARAMETER KOMUNIKASI SERIAL

**Prompt:**
```
Buat slide tentang parameter serial yang harus identik antara master dan slave:
Baud Rate: 9600, 19200, 38400, 115200 bps
Data Bits: selalu 8 untuk Modbus RTU
Stop Bits: 1 atau 2
Parity: None, Even, atau Odd
Format penulisan: 9600-8-N-1 (baud-data-parity-stop)
Tampilkan tabel contoh konfigurasi yang umum digunakan di industri.
Apa yang terjadi jika parameter tidak sesuai?
```

---

### SLIDE 13 – KONVERTER USB-RS485 DAN WIRING ESP32

**Prompt:**
```
Buat slide yang menampilkan cara menghubungkan edge device ke RS-485:
1. MiniPC: USB-RS485 converter (chip FT232RL/CH340), muncul sebagai /dev/ttyUSB0
2. ESP32: IC MAX485, koneksi GPIO17(TX)→DI, GPIO16(RX)→RO, GPIO4→DE/RE
Tampilkan diagram pin ESP32-MAX485 yang jelas.
Jelaskan fungsi pin DE/RE untuk half-duplex direction control.
Sertakan foto/gambar modul USB-RS485 yang umum digunakan.
```

---

### SLIDE 14 – MODBUS TCP: KONSEP DAN KEUNGGULAN

**Prompt:**
```
Buat slide perbandingan Modbus RTU vs Modbus TCP:
| Aspek | Modbus RTU | Modbus TCP |
| Media | RS-485 kabel | Ethernet/WiFi |
| Jarak | ~1200m | Tidak terbatas |
| Kecepatan | 9600-115200 bps | 10-1000 Mbps |
| Perangkat | Maks 247 | Ratusan |
| Error check | CRC | TCP checksum |
| Latensi | Rendah | Sedikit lebih tinggi |
Kapan pilih RTU vs TCP?
```

---

### SLIDE 15 – PLC SCHNEIDER TM221: GAMBARAN UMUM

**Prompt:**
```
Buat slide pengenalan PLC Schneider Electric Modicon M221 (TM221):
Spesifikasi: CPU 32-bit, 256KB program, 14 DI, 10 DO relay, 2 AI, 
Ethernet RJ45, RS-485 (SL1), Modbus RTU+TCP.
Software: EcoStruxure Machine Expert – Basic (EMEB).
Tampilkan gambar/foto TM221CE24R.
Sebutkan aplikasi industri: conveyor, packaging, HVAC, water treatment.
```

---

### SLIDE 16 – KONFIGURASI MODBUS RTU PADA TM221

**Prompt:**
```
Buat slide langkah-langkah konfigurasi Modbus RTU Slave pada TM221:
1. Buka EcoStruxure Machine Expert – Basic
2. Klik TM221CE24R → tab Configuration
3. Pilih Serial Line → SL1
4. Protocol = Modbus Slave
5. Baud Rate: 9600, Parity: None, Stop Bits: 1
6. Slave Address: 1
Tampilkan screenshot antarmuka EMEB (atau mockup).
Tambahkan tips: selalu test dengan Modbus Poll/Scanner sebelum ke lapangan.
```

---

### SLIDE 17 – PEMETAAN MEMORI MODBUS TM221

**Prompt:**
```
Buat slide tabel pemetaan memori Modbus untuk TM221:
%M0-%M999 → Coil 0-999 (Memory bits)
%Q0.0-%Q0.9 → Coil 2048-2057 (Output relay)
%I0.0-%I0.13 → Discrete Input 0-13 (Input digital)
%MW0-%MW999 → Holding Register 0-999 (Memory words)
%IW0.0 → Input Register 256 (Analog Input 0)
Berikan contoh: untuk baca nilai sensor tekanan di %MW5, 
gunakan FC03 alamat 5 slave 1.
```

---

### SLIDE 18 – PROGRAM LADDER TM221: CONTOH DASAR

**Prompt:**
```
Buat slide yang menampilkan contoh program Ladder Diagram pada TM221:
Rung 1: Start/Stop motor (normaly open START_BTN, normally closed STOP_BTN → MOTOR_OUT)
Rung 2: Copy nilai Analog Input ke Memory Word (%IW0.0 → %MW0)
Rung 3: Timer: motor ON selama 5 detik → aktifkan lampu indikator
Tampilkan dalam format Ladder Diagram yang jelas.
Jelaskan fungsi setiap rung dalam bahasa sederhana.
```

---

### SLIDE 19 – PLC OMRON CP2E: GAMBARAN UMUM

**Prompt:**
```
Buat slide pengenalan PLC Omron CP2E:
Spesifikasi: 32-bit CPU, 10K steps program, 32K words DM, 
36 DI (24VDC), 24 DO transistor, RS-232 built-in, Ethernet (suffix E),
Modbus RTU+TCP, CX-Programmer.
Tampilkan gambar CP2E-N60DT-D.
Bandingkan dengan TM221: tabel singkat perbedaan utama.
Sebutkan kelebihan CP2E: kapasitas lebih besar, instruksi lebih kaya.
```

---

### SLIDE 20 – PEMETAAN MEMORI MODBUS CP2E

**Prompt:**
```
Buat slide tabel pemetaan memori Modbus untuk Omron CP2E:
DM0000-DM9999 → Holding Register 0-9999 (Data Memory)
CIO 000.00-099.15 → Coil 0-1599 (Output/Input bits)
W000.00-W511.15 → Coil 4096-12287 (Work bits)
TIM/CNT → HR 10000+ (Timer/Counter)
Berikan contoh program yang menyimpan nilai sensor ke DM100.
```

---

### SLIDE 21 – PYMODBUS: LIBRARY PYTHON UNTUK MODBUS

**Prompt:**
```
Buat slide pengenalan library pymodbus:
- Library Python open source untuk Modbus RTU/TCP/ASCII
- Mendukung master dan slave
- Versi terbaru: 3.x (API berbeda dari v2.x)
- Instalasi: pip install pymodbus pyserial
Tampilkan contoh minimal kode: connect, read_holding_registers, close.
Sertakan link dokumentasi: https://pymodbus.readthedocs.io
```

---

### SLIDE 22 – BACA DATA PLC VIA MODBUS RTU (PYTHON)

**Prompt:**
```
Buat slide code tutorial: membaca data PLC via Modbus RTU menggunakan Python pymodbus.
Tampilkan kode lengkap dengan penjelasan baris per baris:
- ModbusSerialClient dengan parameter port, baudrate, bytesize, parity, stopbits
- client.connect()
- read_holding_registers(address=0, count=10, slave=1)
- Cek result.isError()
- Akses result.registers
- read_coils(address=2048, count=10, slave=1)
- client.close()
Gunakan syntax highlighting Python.
```

---

### SLIDE 23 – TULIS DATA KE PLC VIA MODBUS RTU (PYTHON)

**Prompt:**
```
Buat slide code tutorial: menulis data ke PLC via Modbus RTU menggunakan Python.
Tampilkan contoh:
- write_register(address=0, value=1500, slave=1) → tulis MW0=1500
- write_coil(address=2048, value=True, slave=1) → aktifkan Q0.0
- write_registers(address=0, values=[100,200,300], slave=1) → tulis beberapa register
Jelaskan use case: setpoint dari HMI ke PLC, remote start/stop motor.
```

---

### SLIDE 24 – BACA DATA PLC VIA MODBUS TCP (PYTHON)

**Prompt:**
```
Buat slide code tutorial: membaca data PLC via Modbus TCP menggunakan Python.
Tampilkan kode ModbusTcpClient dengan host='192.168.1.10', port=502.
Bandingkan perbedaan dengan RTU: hanya ganti client, API baca/tulis sama.
Tampilkan diagram jaringan: MiniPC (192.168.1.20) ↔ Switch ↔ PLC (192.168.1.10).
Tips: gunakan ping dan Modbus TCP scanner untuk verifikasi koneksi.
```

---

### SLIDE 25 – GATEWAY LENGKAP: MODBUS → MQTT (PYTHON)

**Prompt:**
```
Buat slide arsitektur dan kode gateway PLC → MQTT menggunakan Python:
Komponen: ModbusSerialClient + paho-mqtt
Alur: Poll PLC setiap 1 detik → format JSON → publish ke topic "plc/data"
Payload JSON: {timestamp, plc_id, registers[], outputs[]}
Tampilkan kode kelas PLCGateway dengan metode: connect(), read_plc_data(), 
publish_to_mqtt(), run().
Jelaskan pentingnya loop_start() untuk async MQTT.
```

---

### SLIDE 26 – PLATFORMIO: EKOSISTEM EMBEDDED MODERN

**Prompt:**
```
Buat slide pengenalan PlatformIO:
- Plugin VS Code untuk embedded development
- Mendukung 700+ board dan framework
- Manajemen library otomatis
- Build, upload, monitor serial dari satu IDE
Tampilkan tampilan antarmuka PlatformIO di VS Code.
Tunjukkan struktur project: platformio.ini, src/main.cpp, lib/, include/.
Bandingkan dengan Arduino IDE: PlatformIO lebih profesional untuk produksi.
```

---

### SLIDE 27 – KONFIGURASI PLATFORMIO.INI UNTUK ESP32 MODBUS

**Prompt:**
```
Buat slide yang menampilkan contoh file platformio.ini untuk project ESP32 Modbus:
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps:
  emelianov/modbus-esp8266@^4.1.0
  knolleary/PubSubClient@^2.8
  bblanchon/ArduinoJson@^6.21.3
monitor_speed = 115200
Jelaskan setiap baris konfigurasi.
Tunjukkan cara upload library: PlatformIO akan otomatis download.
```

---

### SLIDE 28 – ESP32 MODBUS RTU MASTER (PLATFORMIO)

**Prompt:**
```
Buat slide code tutorial ESP32 sebagai Modbus RTU Master menggunakan library modbus-esp8266:
Tampilkan kode dengan Serial2.begin(9600, SERIAL_8N1, RXD2, TXD2).
mb.begin(&Serial2, DE_RE) untuk setup RS-485 dengan direction control.
mb.master() untuk mode master.
mb.readHreg(slaveID, address, buffer, count, callback) untuk baca register.
mb.task() harus dipanggil di loop().
Tampilkan callback function untuk memproses hasil pembacaan.
```

---

### SLIDE 29 – ESP32 MODBUS TCP CLIENT (PLATFORMIO)

**Prompt:**
```
Buat slide code tutorial ESP32 sebagai Modbus TCP Client:
Tampilkan setup WiFi: WiFi.begin(ssid, password), tunggu WL_CONNECTED.
ModbusTCP mb; mb.client();
mb.connect(plcIP) → mb.readHreg(plcIP, address, buffer, count, callback)
Tampilkan cara cek koneksi: mb.isConnected(plcIP)
Jelaskan perbedaan dengan RTU: tidak perlu Serial/UART, melalui WiFi.
Tambahkan tips: gunakan static IP untuk ESP32 agar tidak berubah.
```

---

### SLIDE 30 – ESP32: MODBUS RTU + MQTT PUBLISHER

**Prompt:**
```
Buat slide kode lengkap ESP32 yang membaca PLC via Modbus RTU lalu 
publish data ke MQTT broker menggunakan PubSubClient dan ArduinoJson:
- Setup WiFi + MQTT connection + Modbus RTU
- Callback Modbus: set flag dataReady = true
- Di loop: jika dataReady → serialize JSON → mqttClient.publish()
- reconnectMQTT() jika koneksi MQTT putus
Tampilkan flow diagram: Modbus Read → JSON → MQTT Publish
```

---

### SLIDE 31 – PILIHAN ARSITEKTUR PENGIRIMAN DATA KE SERVER

**Prompt:**
```
Buat slide yang membandingkan 3 opsi arsitektur pengiriman data:
1. MQTT: Edge → Broker → Subscriber (real-time, bandwidth kecil)
2. REST API: Edge → HTTP POST → Server (data historis, mudah integrasi)
3. Hybrid: Edge → MQTT + REST (produksi industri)
Tampilkan diagram alur untuk setiap opsi.
Tambahkan tabel perbandingan: latency, overhead, use case, kompleksitas.
```

---

### SLIDE 32 – STACK TEKNOLOGI REKOMENDASI

**Prompt:**
```
Buat slide tabel stack teknologi untuk sistem IoT industri:
| Komponen | Open Source | Cloud Service |
| MQTT Broker | Mosquitto, EMQX | HiveMQ Cloud, AWS IoT Core |
| REST API | FastAPI, Flask | AWS Lambda, Railway |
| Database TS | InfluxDB, TimescaleDB | InfluxDB Cloud |
| Database SQL | PostgreSQL, SQLite | Supabase |
| Dashboard | Grafana, Node-RED | Grafana Cloud |
Berikan rekomendasi untuk lab/small factory vs enterprise.
```

---

### SLIDE 33 – KONSEP DAN KOMPONEN MQTT

**Prompt:**
```
Buat slide yang menjelaskan MQTT secara lengkap:
Broker: server pusat yang routing semua pesan (Mosquitto)
Publisher: client yang kirim pesan ke topic
Subscriber: client yang langganan topic dan terima pesan
QoS: 0 (at most once), 1 (at least once), 2 (exactly once)
Topic hierarchy: plc/line1/data, plc/line1/status, plc/+/alarm
Tampilkan diagram pub-sub dengan multiple subscribers.
```

---

### SLIDE 34 – INSTALASI DAN KONFIGURASI MOSQUITTO

**Prompt:**
```
Buat slide panduan instalasi Mosquitto MQTT Broker di Linux:
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto && start
Tampilkan file konfigurasi /etc/mosquitto/mosquitto.conf dasar:
listener 1883, allow_anonymous true, persistence true
Test dengan terminal: mosquitto_sub -t "plc/#" -v & 
mosquitto_pub -t "plc/data" -m '{"test":123}'
Tambahkan perintah melihat log: sudo tail -f /var/log/mosquitto/mosquitto.log
```

---

### SLIDE 35 – SUBSCRIBER MQTT → DATABASE SQLITE (PYTHON)

**Prompt:**
```
Buat slide kode Python subscriber MQTT yang menyimpan data ke SQLite:
- Inisialisasi database: CREATE TABLE IF NOT EXISTS readings
- on_message callback: parse JSON → INSERT INTO database
- client.subscribe("plc/data", qos=1)
- client.loop_forever()
Tampilkan skema tabel: id, timestamp, plc_id, register_index, value.
Jelaskan pentingnya penyimpanan data historis untuk analisis dan audit.
```

---

### SLIDE 36 – REST API DENGAN FASTAPI (PYTHON)

**Prompt:**
```
Buat slide code tutorial membangun REST API dengan FastAPI:
- Model Pydantic: PLCData(plc_id, registers, outputs)
- POST /api/v1/plc/data → terima data dari edge device
- GET /api/v1/plc/{plc_id}/latest → ambil data terbaru
Tampilkan otomatis Swagger UI dari FastAPI di /docs.
Cara menjalankan: uvicorn main:app --host 0.0.0.0 --port 8000
Tambahkan diagram: Edge Device → HTTP POST → FastAPI → SQLite
```

---

### SLIDE 37 – NODE-RED UNTUK DASHBOARD IoT

**Prompt:**
```
Buat slide pengenalan Node-RED untuk IoT Dashboard:
- Low-code flow-based programming
- Instalasi: npm install -g node-red, akses http://localhost:1880
- Flow untuk MQTT ke Dashboard: [MQTT in] → [JSON parse] → [Gauge/Chart/Text]
- Node dashboard: ui_gauge, ui_chart, ui_text, ui_led
Tampilkan screenshot Node-RED editor dengan flow dan dashboard.
Tunjukkan cara import flow via JSON.
```

---

### SLIDE 38 – GRAFANA DAN INFLUXDB UNTUK MONITORING

**Prompt:**
```
Buat slide tentang Grafana + InfluxDB untuk monitoring industri:
InfluxDB: time-series database, cocok untuk data sensor
Grafana: platform visualisasi open source
Alur: Edge Device → InfluxDB Writer → InfluxDB → Grafana Query → Dashboard
Tampilkan contoh dashboard Grafana: panel gauge, time-series chart, alert.
Jelaskan keunggulan Grafana untuk data time-series dibanding Excel/spreadsheet.
```

---

### SLIDE 39 – KEAMANAN SISTEM IoT INDUSTRI

**Prompt:**
```
Buat slide tentang ancaman keamanan dan mitigasinya di sistem IIoT:
Ancaman: unauthorized Modbus access, MQTT tanpa autentikasi, REST tanpa auth, 
Man-in-the-middle attack, DDoS pada MQTT broker.
Mitigasi: network segmentation/VLAN, MQTTS (TLS), HTTPS, API Key/JWT, 
firewall (blokir port 502 dari internet), VPN untuk akses remote.
Tampilkan diagram zona keamanan: OT Zone | DMZ | IT/Cloud Zone.
```

---

### SLIDE 40 – NETWORK SEGMENTATION: OT vs IT

**Prompt:**
```
Buat slide yang menjelaskan pemisahan jaringan OT (Operational Technology) 
dan IT (Information Technology) sebagai best practice keamanan IIoT:
OT Zone: PLC, sensor, actuator (jaringan terisolasi, VLAN khusus)
DMZ Zone: Edge device sebagai gateway (satu kaki di OT, satu di IT)
IT Zone: server, cloud, dashboard (internet-facing)
Tampilkan diagram firewall dengan aturan:
- OT → DMZ: allow Modbus (port 502)
- DMZ → IT: allow MQTT (1883/8883), HTTP (80/443)
- IT → OT: DENY all (tidak ada akses langsung)
```

---

### SLIDE 41 – INTEGRASI AI: USE CASES DI INDUSTRI

**Prompt:**
```
Buat slide tentang 4 use case utama AI dalam sistem IoT PLC:
1. Predictive Maintenance: prediksi kerusakan dari getaran, suhu, arus motor (LSTM, RF)
2. Anomaly Detection: deteksi proses abnormal secara real-time (Isolation Forest)
3. Process Optimization: tuning parameter setpoint otomatis (RL, Bayesian Opt)
4. Quality Control: klasifikasi produk cacat dari data sensor (CNN, Decision Tree)
Tampilkan diagram alur data: PLC → Edge AI → Keputusan/Alert → PLC/Operator
```

---

### SLIDE 42 – DETEKSI ANOMALI DENGAN ISOLATION FOREST (PYTHON)

**Prompt:**
```
Buat slide code tutorial deteksi anomali menggunakan Isolation Forest:
Training: IsolationForest(contamination=0.05).fit(historical_data) → joblib.dump()
Inferensi: joblib.load() → model.predict([new_point]) → -1 berarti anomali
Tampilkan plot scatter: data normal (biru) vs anomali (merah)
Contoh dalam loop edge device:
  registers = baca dari PLC
  if detect_anomaly(registers[:5]):
      send_alert("ANOMALI TERDETEKSI")
      publish_to_mqtt("plc/alarm")
```

---

### SLIDE 43 – STUDI KASUS: SISTEM MONITORING CONVEYOR

**Prompt:**
```
Buat slide studi kasus sistem monitoring conveyor pabrik dengan IoT:
Hardware: PLC TM221 (kontrol motor conveyor), ESP32 (edge gateway), MiniPC (server)
Data yang dimonitor: kecepatan conveyor (Hz), suhu motor (°C), arus motor (A),
jumlah produk (counter), status fault.
Implementasi:
- PLC: program Ladder mengatur kecepatan VFD via analog output
- ESP32: baca 5 register PLC setiap 500ms → publish MQTT
- Server: Grafana dashboard + alert jika suhu > 80°C
Tampilkan screenshot dashboard Grafana-nya.
```

---

### SLIDE 44 – RINGKASAN DAN BEST PRACTICES

**Prompt:**
```
Buat slide ringkasan best practices untuk sistem IoT PLC:
1. Selalu gunakan Modbus RTU untuk koneksi jarak dekat (<100m), Modbus TCP untuk jaringan
2. Konfigurasi parameter serial identik (baud, parity, stop bits)
3. Gunakan terminasi 120Ω di kedua ujung bus RS-485
4. Pisahkan jaringan OT dan IT dengan firewall/VLAN
5. Gunakan QoS 1 atau 2 untuk data kritis pada MQTT
6. Implementasikan retry/reconnect logic pada edge device
7. Simpan data ke buffer lokal jika koneksi server putus
8. Amankan dengan TLS untuk komunikasi ke cloud
Tampilkan sebagai checklist infografik.
```

---

### SLIDE 45 – PENUTUP DAN REFERENSI

**Prompt:**
```
Buat slide penutup untuk presentasi Modul 05 IoT PLC AI Modbus:
Tampilkan peta pembelajaran yang sudah dicapai:
Modbus RTU → Modbus TCP → PLC TM221/CP2E → Python Edge → ESP32 Edge 
→ MQTT → REST API → Dashboard → AI Integration
Referensi utama:
- modbus.org – Modbus Specification
- pymodbus.readthedocs.io
- github.com/emelianov/modbus-esp8266
- mosquitto.org
- fastapi.tiangolo.com
- grafana.com
Tambahkan QR code menuju link repositori praktikum.
Ucapan: "Selamat Berpraktikum! Terapkan IIoT untuk industri yang lebih cerdas."
```

---

## PANDUAN PENGGUNAAN NOTEBOOKLM

1. Buka **Google NotebookLLM** (https://notebooklm.google.com)
2. Buat notebook baru → upload file `materi.md` sebagai sumber
3. Salin satu prompt di atas ke chat
4. Review hasil → minta revisi jika perlu: *"Buat lebih visual/lebih detail/lebih ringkas"*
5. Export ke Google Slides atau PowerPoint

**Tips:**
- Tambahkan konteks: *"Pengguna presentasi adalah mahasiswa teknik mekatronika semester 5"*
- Minta format: *"Buat dalam format poin-poin maksimal 6 baris per slide"*
- Minta visual: *"Tambahkan diagram/tabel/infografik yang relevan"*

---

*Prompt ini dibuat untuk Modul 05 Praktikum Mekatronika dan Robotika.*
