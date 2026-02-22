# PROJECT MODUL 09: ROS KINEMATIKA DAN KONTROLER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 09 – ROS Kinematika dan Kontroler  
**Sifat:** Kelompok (3–4 mahasiswa)  
**Deadline Presentasi:** ___________________

---

## PANDUAN UMUM PROJECT

### Kriteria Project

Project harus:
- Mengintegrasikan minimal **3 komponen utama** dari modul ini: FK/IK, TF/URDF, kontroler (PID/go-to-goal/ros_control), dan odometri
- Berjalan di **simulasi Gazebo** (wajib)
- Disertai **implementasi hardware** pada Mini PC + robot nyata (nilai bonus +20%)
- Memiliki **dokumentasi kode** (komentar inline) dan **laporan project** (pdf, min 10 halaman)
- Dipresentasikan dan didemo secara langsung (live demo)

### Komponen Penilaian Project

| Komponen | Bobot | Indikator |
|---------|-------|----------|
| Implementasi teknis | 40% | Kode berjalan, integrasi komponen benar |
| Inovasi & kompleksitas | 20% | Melebihi percobaan dasar, ada improvisasi |
| Analisa & laporan | 25% | Data kuantitatif, grafik, penjelasan mendalam |
| Presentasi & demo | 15% | Demo live berjalan, presentasi jelas |

---

## 10 OPSI SOAL PROJECT

---

### PROJECT 01 – Autonomous Warehouse Robot

**Soal Cerita:**

PT. Logistik Nusantara memiliki gudang seluas 10×10 meter dengan rak-rak penyimpanan. Robot mobile perlu mengambil paket dari titik pick-up (A) dan mengantarkannya ke titik drop-off (B). Robot harus bergerak secara otonom, menghindari rak statis, dan melaporkan posisinya secara real-time ke sistem manajemen gudang.

**Tugas Implementasi:**

1. Desain URDF robot mobile diferensial dengan dimensi realistis (wheelbase 25cm, diameter roda 10cm)
2. Implementasikan go-to-goal controller dengan path planning sederhana (waypoint sequence)
3. Buat peta Gazebo yang merepresentasikan layout gudang (dengan obstacle rak statis)
4. Implementasikan sistem odometri yang mem-publish pose ke topik `/odom`
5. Buat node `warehouse_manager` yang mengirimkan sequence waypoint: A → B → A → B (loop 3 kali)
6. Tampilkan trajectory robot di RViz dan hitung total error kumulatif posisi

**Improvisasi dari Percobaan Dasar:**
- P09 (go-to-goal) + P11 (ros_control) + P15 (integrasi) → ditambah: obstacle layout, multi-waypoint loop, logging performa

**Parameter Evaluasi:**
- Error posisi rata-rata setiap waypoint < 10 cm
- Siklus A→B berhasil diselesaikan minimal 3 kali berturut-turut
- Tidak menabrak obstacle

**Rekomendasi Hardware:** Mini PC (Beelink SER5 Pro) + robot diferensial custom + RPLidar A1

---

### PROJECT 02 – Robot Arm Pick-and-Place dengan IK MoveIt!

**Soal Cerita:**

Industri manufaktur komponen elektronik memerlukan robot lengan untuk mengambil komponen dari conveyor belt dan menempatkannya di PCB. Robot 3-DOF perlu melakukan kalkulasi IK secara real-time untuk menjangkau posisi komponen yang bervariasi dalam area 30×30cm.

**Tugas Implementasi:**

1. Desain robot arm 3-DOF dengan URDF/Xacro (dengan mass, inertia, limit sendi)
2. Bangun tabel DH dan verifikasi dengan FK Python manual
3. Implementasikan IK analitik untuk 2-DOF planar + 1 DOF rotasi
4. Buat node `pick_and_place` yang:
   - Menerima koordinat target dari topik `/target_position` (geometry_msgs/Point)
   - Menghitung IK untuk mendapatkan joint angles
   - Menggerakkan joint ke target menggunakan trajectory action
5. Simulasikan di Gazebo dengan menggunakan joint_trajectory_controller
6. Visualisasi FK (pose end-effector) secara real-time di RViz sebagai Marker

**Improvisasi dari Percobaan Dasar:**
- P02 (FK DH) + P03 (IK analitik) + P07 (URDF) → ditambah: ros_control joint controllers, action interface, real-time FK marker di RViz

**Parameter Evaluasi:**
- Error IK vs target < 1 mm
- Waktu kalkulasi IK < 10 ms
- Robot mencapai 10 target berbeda berturut-turut tanpa kegagalan

**Rekomendasi Hardware:** Mini PC + robot arm 3-DOF servo (MG996R) + Arduino Mega + rosserial

---

### PROJECT 03 – Convoy Robot System (Leader-Follower)

**Soal Cerita:**

Tim SAR (Search and Rescue) membutuhkan sistem 3 robot yang bergerak dalam formasi convoy melewati area bencana. Robot pertama (leader) dikontrol oleh operator, sementara robot kedua dan ketiga mengikuti secara otomatis dengan menjaga jarak aman 0.5 meter.

**Tugas Implementasi:**

1. Buat 3 instance robot diferensial di Gazebo dengan namespace berbeda (`robot1`, `robot2`, `robot3`)
2. Robot leader (`robot1`) dikontrol manual via `teleop_twist_keyboard`
3. Implementasikan controller follower untuk `robot2`:
   - Subscribe pose `robot1` dari `/robot1/odom`
   - Hitung target pose `robot2` = pose `robot1` dengan offset -0.5m ke belakang
   - Jalankan go-to-goal controller untuk mencapai target pose
4. Robot3 mengikuti Robot2 dengan cara yang sama
5. Broadcast semua pose ke TF (namespace robot1, robot2, robot3)
6. Tampilkan semua robot di RViz secara bersamaan

**Improvisasi dari Percobaan Dasar:**
- P09 (go-to-goal) + P06 (TF) → ditambah: multi-robot, namespace ROS, formation control

**Parameter Evaluasi:**
- Jarak robot2 ke robot1 dipertahankan dalam 0.5 ± 0.1 m
- Tidak terjadi tabrakan antar robot
- Formasi terjaga saat leader berhenti mendadak

**Rekomendasi Hardware:** 3x Mini PC / 1 Mini PC + 2 Raspberry Pi + 3 robot diferensial kecil

---

### PROJECT 04 – Surgical Assistant Robot Simulation

**Soal Cerita:**

Rumah sakit modern menggunakan robot untuk membantu prosedur pembedahan minimal invasif. Robot arm 4-DOF perlu mengikuti trajectory yang ditentukan dokter dengan presisi tinggi (error < 0.1mm) dan respons yang stabil (tanpa osilasi).

**Tugas Implementasi:**

1. Desain robot arm 4-DOF dengan massa sendi bervariasi (simulasi payload)
2. Implementasikan cascade controller (outer: posisi, inner: kecepatan) menggunakan framework ros_control
3. Buat trajectory generator yang menghasilkan path smooth (spline interpolation) antar titik
4. Implementasikan sistem monitoring yang mendeteksi jika error > threshold (emergency stop)
5. Simulasikan disturbance eksternal (impulse force) dan ukur disturbance rejection
6. Log seluruh data (setpoint, actual, error) ke rosbag untuk analisa post-hoc

**Improvisasi dari Percobaan Dasar:**
- P13 (cascade controller) + P02 (FK DH) + P04 (IK numerik) → ditambah: trajectory generation, emergency stop, disturbance rejection analysis

**Parameter Evaluasi:**
- Tracking error < 0.5mm saat mengikuti trajectory predefined
- Settling time < 0.5 detik setelah disturbance
- Overshoot < 5% pada semua sendi

**Rekomendasi Hardware:** Mini PC + robot arm servo presisi + motor encoder resolusi tinggi (>2000 PPR)

---

### PROJECT 05 – Autonomous Delivery Robot (Kampus Smart)

**Soal Cerita:**

Kampus modern ingin mengimplementasikan sistem pengiriman paket otonom menggunakan robot mobile. Robot harus dapat menavigasi dari gedung A ke gedung B melewati lorong kampus, mendeteksi hambatan sementara (orang atau sepeda yang lewat), berhenti sementara, kemudian melanjutkan perjalanan.

**Tugas Implementasi:**

1. Buat peta Gazebo yang merepresentasikan layout lorong kampus (lebar 1.5m, beberapa persimpangan)
2. Implementasikan sistem odometri + TF lengkap (odom → base_link → sensor frames)
3. Buat node `delivery_planner`:
   - Menerima perintah pengiriman: `{"from": "A", "to": "B"}`
   - Mengeksekusi sequence waypoint pre-defined
4. Implementasikan obstacle detection sederhana menggunakan data `/scan` (LaserScan)
5. Jika obstacle terdeteksi < 0.5m, robot berhenti; jika obstacle pergi, lanjutkan
6. Logging: total waktu pengiriman, jarak tempuh, jumlah stop

**Improvisasi dari Percobaan Dasar:**
- P09 (go-to-goal) + P10/P11 (odometri) + P15 (integrasi) → ditambah: laser obstacle detection, stop-and-wait behavior, delivery logging

**Parameter Evaluasi:**
- Berhasil menyelesaikan skenario pengiriman A→B dalam < 60 detik
- Berhenti dalam 0.3m sebelum obstacle
- Melanjutkan perjalanan dalam 2 detik setelah obstacle hilang

**Rekomendasi Hardware:** Mini PC + robot diferensial + RPLidar A1 + chassis robot mobile 4 roda

---

### PROJECT 06 – Drone Kinematic Simulator

**Soal Cerita:**

Tim peneliti membutuhkan simulator kinematika drone quadcopter untuk studi awal sebelum uji terbang fisik. Simulator harus merepresentasikan model kinematika quadcopter secara akurat, merespons perintah roll/pitch/yaw/throttle, dan memvisualisasikan state drone secara real-time.

**Tugas Implementasi:**

1. Implementasikan model kinematika quadcopter:
   - State: [x, y, z, roll, pitch, yaw, vx, vy, vz, p, q, r]
   - Input: [Ω₁, Ω₂, Ω₃, Ω₄] (kecepatan motor)
   - Model fisika: gaya lift, torsi, gravitasi
2. Buat node `quadcopter_sim` yang mengintegrasikan model dengan RK4
3. Publish pose ke `/tf` (world → base_link) dan `/odom`
4. Implementasikan kontroler PID untuk altitude (z) dan heading (yaw)
5. Subscribe `/cmd_vel` untuk menerima perintah pilot (linear.z = throttle, angular.z = yaw rate)
6. Visualisasi drone di RViz menggunakan URDF sederhana

**Improvisasi dari Percobaan Dasar:**
- P06 (TF) + P08 (PID) + P15 (integrasi) → ditambah: model fisika quadcopter, RK4 integrator, altitude+heading control

**Parameter Evaluasi:**
- Drone dapat hover stabil (error z < 2cm, error yaw < 2°) selama 30 detik
- Respons perintah takeoff dari z=0 ke z=1m dalam < 3 detik
- Visualisasi drone di RViz konsisten dengan state simulator

**Rekomendasi Hardware:** Mini PC saja (simulasi murni, tidak perlu hardware tambahan)

---

### PROJECT 07 – Omni-Directional AGV (Automated Guided Vehicle)

**Soal Cerita:**

Pabrik otomotif memerlukan AGV (Automated Guided Vehicle) dengan kemampuan gerak ke segala arah untuk bermanuver di ruang sempit antar lini produksi. Robot omni-directional 3 roda dipilih karena kemampuan holonomic-nya yang superior dibanding robot diferensial.

**Tugas Implementasi:**

1. Desain URDF robot omni 3 roda dengan sudut 120° dan plugin `gazebo_ros_force_based_move`
2. Implementasikan `omni_controller` node:
   - Subscribe `/cmd_vel` (geometry_msgs/Twist): vx, vy, omega_z
   - Hitung IK roda → kecepatan 3 roda motor
   - Publish ke topik `/wheel_velocities`
3. Implementasikan FK odometri dari kecepatan roda ke pose robot
4. Buat demo path:
   - Gerak lateral (±y direction) tanpa rotasi badan
   - Lingkaran sempurna
   - Figure-8 path
5. Plot trajectory di RViz dan bandingkan dengan path ideal

**Improvisasi dari Percobaan Dasar:**
- P14 (omni kinematika) → ditambah: URDF Gazebo, odometri omni, path demo, perbandingan ideal vs aktual

**Parameter Evaluasi:**
- Error trajectory circular < 5cm
- Robot bergerak lateral tanpa rotasi badan (yaw error < 3°)
- Waktu eksekusi figure-8 path < 30 detik

**Rekomendasi Hardware:** Mini PC + chassis omni-wheel custom 3 roda + 3x motor DC encoder + L298N × 2

---

### PROJECT 08 – Robot Inspection System

**Soal Cerita:**

Perusahaan infrastruktur membutuhkan robot patroli otonom untuk memeriksa kondisi dalam gedung secara berkala. Robot harus bergerak mengelilingi perimeter gedung, berhenti di checkpoints predefined, merekam data sensor (simulasi), dan mengirimkan laporan status.

**Tugas Implementasi:**

1. Buat peta Gazebo yang merepresentasikan interior gedung dengan 6 checkpoint
2. Implementasikan `patrol_planner` node:
   - Eksekusi sequence: checkpoint 1 → 2 → 3 → ... → 6 → 1 (loop)
   - Gunakan go-to-goal controller dengan PID heading yang akurat
3. Di setiap checkpoint: berhenti selama 3 detik, "rekam" data sensor (print timestamp + lokasi)
4. Implementasikan state machine: NAVIGATING → ARRIVED → INSPECTING → NAVIGATING
5. Publikasikan status robot: topik `/inspection_status` (std_msgs/String)
6. Log laporan inspeksi ke file CSV: [timestamp, checkpoint_id, duration, pose, status]

**Improvisasi dari Percobaan Dasar:**
- P09 (go-to-goal) + P15 (integrasi) → ditambah: state machine, checkpoint sequence, inspection logging

**Parameter Evaluasi:**
- Robot mengunjungi semua 6 checkpoint dalam satu siklus patroli < 120 detik
- Error posisi di setiap checkpoint < 8 cm
- Laporan CSV ter-generate dengan benar

**Rekomendasi Hardware:** Mini PC + robot diferensial + RPLidar A1 untuk navigasi

---

### PROJECT 09 – Multi-Joint Arm Teleop dengan Kinematika Real-Time

**Soal Cerita:**

Laboratorium robotika membutuhkan interface teleoperasi robot arm 3-DOF yang intuitif. Operator ingin menggerakkan end-effector di ruang Cartesian (x, y, z) menggunakan joystick atau keyboard, sementara sistem secara otomatis menghitung sudut sendi yang diperlukan (IK real-time).

**Tugas Implementasi:**

1. Desain robot arm 3-DOF di Gazebo dengan joint_trajectory_controller
2. Implementasikan Cartesian teleop interface:
   - Keyboard atau gamepad → perintah increment posisi end-effector (Δx, Δy, Δz)
   - Node `cartesian_teleop` mengakumulasikan posisi target
3. Implementasikan IK numerik real-time (Jacobian pseudoinverse, 20 Hz)
4. Implementasikan singularity avoidance: jika μ < threshold, tampilkan warning dan kurangi kecepatan
5. Tampilkan real-time di RViz:
   - Pose end-effector (Marker sphere merah = target, hijau = actual)
   - Workspace boundary (Marker)
   - Nilai manipulability μ (pada terminal)

**Improvisasi dari Percobaan Dasar:**
- P04 (IK numerik) + P05 (Jacobian) + P07 (URDF) → ditambah: Cartesian teleop, singularity detection, real-time RViz feedback

**Parameter Evaluasi:**
- Latency IK < 50ms untuk setiap iterasi
- Warning singularitas muncul ketika μ < 0.05
- End-effector mengikuti perintah keyboard dengan delay < 100ms

**Rekomendasi Hardware:** Mini PC + robot arm servo real (opsional) + gamepad USB

---

### PROJECT 10 – Self-Calibrating Odometry System

**Soal Cerita:**

Robot mobile yang digunakan dalam kompetisi RoboCup mengalami drift odometri yang signifikan setelah 5 menit operasi. Solusinya adalah sistem kalibrasi odometri otomatis yang secara periodik mengkoreksi parameter roda (radius dan wheelbase) berdasarkan perbandingan odometri dengan sensor referensi (ArUco marker atau LiDAR-based localization).

**Tugas Implementasi:**

1. Simulasikan error odometri dengan sengaja menambahkan noise ke parameter roda (radius_error ±5%, wheelbase_error ±3%)
2. Implementasikan node `odometry_publisher` dengan parameter roda yang bisa dikalibrasi
3. Implementasikan prosedur kalibrasi otomatis:
   a. Robot bergerak dalam persegi 1×1m
   b. Bandingkan pose akhir (odometri) dengan pose awal (seharusnya kembali ke titik sama)
   c. Hitung correction factor berdasarkan error
   d. Update parameter roda
4. Ulangi kalibrasi 3 kali dan ukur konvergensi error
5. Implementasikan EKF sederhana untuk fusi odometri + IMU (simulasi)

**Improvisasi dari Percobaan Dasar:**
- P10 (odometri) → ditambah: kalibrasi otomatis, error injection, EKF fusi sensor

**Parameter Evaluasi:**
- Error odometri sebelum kalibrasi: ± 10 cm per meter perjalanan (diinjeksi)
- Error odometri setelah 3 iterasi kalibrasi: < 2 cm per meter perjalanan
- EKF mengurangi variance estimasi pose > 50%

**Rekomendasi Hardware:** Mini PC + robot diferensial + IMU (MPU-6050 via ESP32) + encoder motor

---

## TEMPLATE LAPORAN PROJECT

### Struktur Laporan (Minimal 10 Halaman)

1. **Cover** – Judul project, nama anggota, NIM, tanggal
2. **Deskripsi Project** (1 hal) – Permasalahan, tujuan, ruang lingkup
3. **Landasan Teori** (2 hal) – Teori yang relevan dengan project yang dipilih
4. **Desain Sistem** (2 hal) – Diagram blok, arsitektur ROS, URDF, konfigurasi
5. **Implementasi** (2 hal) – Penjelasan kode kunci, konfigurasi launch, integrasi komponen
6. **Hasil dan Analisa** (2 hal) – Tabel data, grafik, analisa kuantitatif
7. **Kesimpulan dan Saran** (0.5 hal)
8. **Referensi** (minimal 5 sumber)
9. **Lampiran** – Screenshot, grafik tambahan, listing kode lengkap

### Pengumpulan

| Artefak | Format | Deadline |
|--------|--------|---------|
| Laporan Project | PDF | H-3 sebelum presentasi |
| Kode Program | ZIP atau GitHub link | Bersamaan dengan laporan |
| Video Demo | MP4, 3-5 menit | H-1 sebelum presentasi |
| Slide Presentasi | PDF | Hari presentasi |
