# JOBSHEET MODUL 09: ROS KINEMATIKA DAN KONTROLER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 09 – ROS Kinematika dan Kontroler  
**Platform:** ROS Noetic / Ubuntu 20.04  
**Pertemuan:** 1–4 (4 × 2 SKS)  
**Tanggal:** ___________________  
**Nama Kelompok:** ___________________  
**Anggota:**

| No | Nama | NIM |
|----|------|-----|
| 1  |      |     |
| 2  |      |     |
| 3  |      |     |
| 4  |      |     |

---

## A. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menghitung Forward Kinematics (FK) robot 2-DOF dan 3-DOF menggunakan matriks transformasi homogen dan parameter DH
2. Menghitung Inverse Kinematics (IK) robot 2-DOF secara analitik dan numerik menggunakan Jacobian pseudoinverse
3. Membangun dan mem-publish TF tree di ROS menggunakan Python
4. Membuat dan memvisualisasikan URDF robot sederhana di RViz
5. Merancang dan mengimplementasikan kontroler PID untuk kecepatan motor
6. Mengimplementasikan Go-to-Goal controller untuk robot mobile di Gazebo
7. Mempublish data odometri dari encoder menggunakan rosserial
8. Mengonfigurasi diff_drive_controller menggunakan framework ros_control
9. Mengimplementasikan kinematika robot omni-directional 3 roda
10. Mengintegrasikan seluruh komponen dalam sistem kontrol robot yang lengkap

---

## B. CPMK (CAPAIAN PEMBELAJARAN MATA KULIAH)

| Kode | Capaian Pembelajaran | Indikator Ketercapaian |
|------|---------------------|----------------------|
| CPMK-1 | Mampu menghitung dan mengimplementasikan FK dan IK robot | Kode Python berjalan, hasil verifikasi FK↔IK benar |
| CPMK-2 | Mampu membangun TF tree dan URDF di ROS | TF tree terpublish, RViz menampilkan robot model |
| CPMK-3 | Mampu merancang dan menyetel kontroler PID | Grafik respons step PID dengan overshoot < 10% |
| CPMK-4 | Mampu mengimplementasikan kontroler robot mobile di Gazebo | Robot mencapai target pose dengan error < 5 cm |
| CPMK-5 | Mampu mengintegrasikan seluruh komponen sistem ROS | Sistem terintegrasi berjalan stabil selama 60 detik |

---

## C. ALAT DAN BAHAN

### Perangkat Lunak

| No | Software | Versi | Cara Instalasi |
|----|---------|-------|---------------|
| 1 | Ubuntu | 20.04 LTS | Dual boot / VM / WSL2 |
| 2 | ROS Noetic | Full Desktop | `sudo apt install ros-noetic-desktop-full` |
| 3 | Gazebo | 11 (bundled) | Termasuk dalam ros-noetic-desktop-full |
| 4 | Python | 3.8+ | Bawaan Ubuntu 20.04 |
| 5 | NumPy | latest | `pip3 install numpy` |
| 6 | Matplotlib | latest | `pip3 install matplotlib` |
| 7 | Visual Studio Code | latest | `snap install code --classic` |

### Package ROS yang Diperlukan

```bash
sudo apt install ros-noetic-ros-control \
                 ros-noetic-ros-controllers \
                 ros-noetic-diff-drive-controller \
                 ros-noetic-gazebo-ros-pkgs \
                 ros-noetic-gazebo-ros-control \
                 ros-noetic-robot-state-publisher \
                 ros-noetic-joint-state-publisher \
                 ros-noetic-joint-state-publisher-gui \
                 ros-noetic-teleop-twist-keyboard \
                 ros-noetic-rosserial-python \
                 ros-noetic-rosserial-arduino \
                 ros-noetic-tf2-tools \
                 ros-noetic-rqt-reconfigure \
                 ros-noetic-rqt-plot
```

### Hardware (Opsional – untuk Percobaan P08 dan P10)

| No | Komponen | Spesifikasi | Fungsi |
|----|---------|------------|--------|
| 1 | Mini PC / Laptop | Intel i5+, RAM 8GB, Ubuntu 20.04 | ROS Master |
| 2 | Arduino Mega / ESP32 | ATmega2560 / ESP32-WROOM | Bridge ROS–Hardware |
| 3 | Motor DC + Gearbox | 12V, encoder 500PPR | Aktuator roda |
| 4 | Motor Driver L298N | Dual H-bridge, 2A/channel | Driver motor |
| 5 | Kabel USB-Serial | CP2102 / CH340 | Komunikasi rosserial |
| 6 | Power Supply | 12V 3A | Daya motor + Arduino |

> **Catatan:** Percobaan P01–P07, P09, P11–P15 dapat diselesaikan **tanpa hardware** (pure software/simulation).

---

## D. PERSIAPAN WORKSPACE

### D.1 Buat Catkin Workspace

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
source devel/setup.bash
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

### D.2 Buat Package untuk Modul 09

```bash
cd ~/catkin_ws/src
catkin_create_pkg modul09_kinematika rospy std_msgs geometry_msgs \
    nav_msgs sensor_msgs tf tf2_ros urdf xacro \
    gazebo_ros gazebo_plugins
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### D.3 Struktur Direktori Package

```
modul09_kinematika/
├── CMakeLists.txt
├── package.xml
├── config/
│   └── controllers.yaml
├── launch/
│   ├── p01_fk.launch
│   ├── p07_urdf.launch
│   ├── p09_go_to_goal.launch
│   └── p11_ros_control.launch
├── scripts/            ← file Python executable
│   ├── p01_fk_2dof.py
│   ├── p02_fk_dh.py
│   ├── p03_ik_analytic.py
│   ├── p04_ik_numerical.py
│   ├── p05_jacobian.py
│   ├── p06_tf_broadcaster.py
│   ├── p08_pid_velocity.py
│   ├── p09_go_to_goal.py
│   ├── p10_odometry.py
│   ├── p13_cascade_controller.py
│   ├── p14_omni_kinematics.py
│   └── p15_integration.py
└── urdf/
    ├── p07_robot.urdf.xacro
    └── p12_robot_gazebo.urdf.xacro
```

---

## E. LANGKAH KERJA

---

### PERCOBAAN P01 – Forward Kinematics Robot 2-DOF

**Tujuan:** Menghitung FK robot 2-DOF menggunakan Python dan NumPy

**Langkah Kerja:**

1. Buat file `~/catkin_ws/src/modul09_kinematika/scripts/p01_fk_2dof.py`
2. Isi dengan kode berikut, kemudian jalankan:

```bash
rosrun modul09_kinematika p01_fk_2dof.py
```

**Tabel Observasi P01:**

| No | θ₁ (°) | θ₂ (°) | L₁ (m) | L₂ (m) | x_hitung (m) | y_hitung (m) | x_kode (m) | y_kode (m) |
|----|--------|--------|--------|--------|-------------|-------------|-----------|-----------|
| 1  | 0      | 0      | 0.5    | 0.3    |             |             |           |           |
| 2  | 30     | 45     | 0.5    | 0.3    |             |             |           |           |
| 3  | 90     | -30    | 0.5    | 0.3    |             |             |           |           |
| 4  | 45     | 90     | 0.5    | 0.3    |             |             |           |           |
| 5  | 60     | 60     | 0.4    | 0.4    |             |             |           |           |

**Pertanyaan Analisa P01:**
1. Apakah hasil perhitungan manual sesuai dengan output kode? Jelaskan perbedaan jika ada.
2. Pada konfigurasi θ₁=0°, θ₂=0°, di mana posisi end-effector? Mengapa?
3. Apa yang terjadi pada FK jika θ₁+θ₂ = 180°?

---

### PERCOBAAN P02 – FK dengan Parameter Denavit-Hartenberg

**Tujuan:** Membangun tabel DH dan menghitung FK dengan matriks transformasi homogen

**Langkah Kerja:**

1. Buat tabel DH untuk robot 3-DOF dengan dimensi: L₁=0.1m, L₂=0.25m, L₃=0.20m
2. Implementasikan fungsi `dh_matrix()` dan `forward_kinematics_dh()` di Python
3. Verifikasi hasil dengan FK manual untuk satu konfigurasi

```bash
rosrun modul09_kinematika p02_fk_dh.py
```

**Tabel DH Robot 3-DOF (isi oleh mahasiswa):**

| Sendi i | θᵢ (variabel) | dᵢ (m) | aᵢ (m) | αᵢ (°) |
|---------|--------------|-------|-------|-------|
| 1       | θ₁           |       |       |       |
| 2       | θ₂           |       |       |       |
| 3       | θ₃           |       |       |       |

**Tabel Observasi P02:**

| No | θ₁ | θ₂ | θ₃ | px (m) | py (m) | pz (m) | Screenshot Matrix T |
|----|----|----|-----|-------|-------|-------|-------------------|
| 1  | 0° | 0° | 0°  |       |       |       |                   |
| 2  | 30°| 45°| 0°  |       |       |       |                   |
| 3  | 0° | 90°| -45°|       |       |       |                   |

---

### PERCOBAAN P03 – Inverse Kinematics Analitik 2-DOF

**Tujuan:** Menghitung IK secara analitik dan memvalidasi dengan FK

**Langkah Kerja:**

1. Implementasikan fungsi IK analitik 2-DOF berdasarkan persamaan:
   - `cos(θ₂) = (x² + y² - L₁² - L₂²) / (2·L₁·L₂)`
   - `θ₁ = atan2(y,x) - atan2(L₂·sin(θ₂), L₁+L₂·cos(θ₂))`
2. Jalankan dan verifikasi: masukkan target, dapatkan sudut, lakukan FK dengan sudut tersebut, bandingkan dengan target asli

```bash
rosrun modul09_kinematika p03_ik_analytic.py
```

**Tabel Observasi P03:**

| No | x_target | y_target | θ₁ elbow-up | θ₂ elbow-up | θ₁ elbow-down | θ₂ elbow-down | Verifikasi FK |
|----|---------|---------|------------|------------|--------------|--------------|--------------|
| 1  | 0.5     | 0.3     |            |            |              |              |               |
| 2  | 0.7     | 0.1     |            |            |              |              |               |
| 3  | 0.2     | 0.7     |            |            |              |              |               |
| 4  | 0.1     | 0.1     |            |            |              |              |               |
| 5  | 0.9     | 0.0     |            |            |              |              |               |

**Pertanyaan Analisa P03:**
1. Target mana yang berada di luar workspace? Bagaimana program menanganinya?
2. Apa perbedaan konfigurasi elbow-up vs elbow-down? Kapan Anda memilih yang mana?
3. Error FK vs target: apakah hasilnya sama persis? Mengapa?

---

### PERCOBAAN P04 – IK Numerik dengan Jacobian Pseudoinverse

**Tujuan:** Mengimplementasikan IK numerik dan membandingkan dengan IK analitik

**Langkah Kerja:**

1. Implementasikan algoritma iteratif Jacobian pseudoinverse untuk IK
2. Variasikan learning rate α (0.01, 0.1, 0.5, 1.0) dan amati konvergensi
3. Bandingkan jumlah iterasi dan akurasi dengan metode analitik

```bash
rosrun modul09_kinematika p04_ik_numerical.py
```

**Tabel Observasi P04:**

| α (learning rate) | Target (x,y) | Iterasi | Error Akhir | Waktu (ms) | Konvergen? |
|------------------|-------------|---------|------------|-----------|-----------|
| 0.01             | (0.5, 0.3)  |         |            |           |           |
| 0.1              | (0.5, 0.3)  |         |            |           |           |
| 0.5              | (0.5, 0.3)  |         |            |           |           |
| 1.0              | (0.5, 0.3)  |         |            |           |           |
| 0.1              | (0.7, 0.1)  |         |            |           |           |

**Pertanyaan Analisa P04:**
1. Bagaimana hubungan antara learning rate dan kecepatan konvergensi?
2. Apa keunggulan dan kekurangan IK numerik dibanding IK analitik?
3. Apa yang terjadi jika α terlalu besar?

---

### PERCOBAAN P05 – Komputasi dan Visualisasi Jacobian

**Tujuan:** Menghitung matriks Jacobian dan menganalisis manipulability

**Langkah Kerja:**

1. Implementasikan fungsi `compute_jacobian()` menggunakan kolom zi dan pi dari FK parsial
2. Hitung manipulability index: `μ = sqrt(det(J·Jᵀ))`
3. Plot manipulability sebagai fungsi θ₁ (θ₂ tetap) untuk mengidentifikasi singularitas

```bash
rosrun modul09_kinematika p05_jacobian.py
```

**Tabel Observasi P05:**

| θ₁ (°) | θ₂ (°) | J[0,0] | J[0,1] | J[1,0] | J[1,1] | det(J) | μ (manip.) |
|--------|--------|-------|-------|-------|-------|--------|-----------|
| 0      | 0      |       |       |       |       |        |           |
| 30     | 45     |       |       |       |       |        |           |
| 90     | 0      |       |       |       |       |        |           |
| 0      | 180    |       |       |       |       |        |           |
| 45     | 135    |       |       |       |       |        |           |

**Pertanyaan Analisa P05:**
1. Pada konfigurasi mana μ mendekati nol? Apa artinya secara fisik?
2. Bagaimana hubungan antara Jacobian dan kecepatan end-effector?
3. Plot grafik μ vs θ₁ dan identifikasi konfigurasi singular.

---

### PERCOBAAN P06 – TF Broadcaster di ROS Python

**Tujuan:** Mempublish transformasi antar frame koordinat menggunakan TF

**Langkah Kerja:**

1. Buat TF broadcaster untuk robot 2-DOF dengan 3 frame: `world`, `link1`, `link2`
2. Publish transformasi berdasarkan sudut joint yang berubah secara sinusoidal
3. Visualisasi frame di RViz

```bash
# Terminal 1:
roscore
# Terminal 2:
rosrun modul09_kinematika p06_tf_broadcaster.py
# Terminal 3:
rviz  # tambahkan display TF
# Terminal 4 (opsional):
rosrun tf tf_echo world link2
```

**Tabel Observasi P06:**

| Waktu (s) | θ₁ (rad) | θ₂ (rad) | Trans link1→link2 (x,y,z) | Rot (qx,qy,qz,qw) |
|-----------|---------|---------|--------------------------|------------------|
| 0.0       |         |         |                          |                  |
| 1.0       |         |         |                          |                  |
| 2.0       |         |         |                          |                  |
| 3.14      |         |         |                          |                  |

**Checklist Observasi P06:**
- [ ] Frame `world` terlihat di RViz
- [ ] Frame `link1` berputar terhadap `world`
- [ ] Frame `link2` berputar terhadap `link1`
- [ ] `tf_echo world link2` menampilkan transformasi yang berubah secara dinamis

---

### PERCOBAAN P07 – Membuat URDF Robot Sederhana

**Tujuan:** Membuat file URDF robot diferensial dan memvisualisasikan di RViz

**Langkah Kerja:**

1. Buat file `p07_robot.urdf.xacro` dengan komponen: base_link, left_wheel, right_wheel, laser_link
2. Jalankan dengan robot_state_publisher dan joint_state_publisher_gui

```bash
roslaunch modul09_kinematika p07_urdf.launch
```

**Checklist Verifikasi P07:**
- [ ] RViz menampilkan model robot (base + 2 roda)
- [ ] Joint state publisher GUI menampilkan slider untuk setiap joint
- [ ] Menggeser slider menggerakkan roda di RViz
- [ ] TF tree menampilkan: world → base_link → left_wheel, right_wheel, laser_link
- [ ] Tidak ada error di terminal

**Screenshot yang harus dilampirkan:**
1. Screenshot RViz dengan model robot dan TF frame
2. Screenshot joint_state_publisher_gui
3. Screenshot rqt_tf_tree menampilkan tree lengkap

---

### PERCOBAAN P08 – PID Kontroler Kecepatan Motor

**Tujuan:** Mengimplementasikan dan menyetel kontroler PID untuk kecepatan motor DC

> **Mode A (Dengan Hardware):** Gunakan Arduino/ESP32 + motor DC + encoder  
> **Mode B (Simulasi):** Gunakan model motor DC di Python (tanpa hardware)

**Langkah Kerja (Mode B – Simulasi):**

1. Jalankan node PID yang menyimulasikan plant motor DC orde 1
2. Ubah-ubah parameter Kp, Ki, Kd melalui rqt_reconfigure
3. Amati respons step dan catat metrik

```bash
# Terminal 1:
roscore
# Terminal 2:
rosrun modul09_kinematika p08_pid_velocity.py
# Terminal 3:
rosrun rqt_reconfigure rqt_reconfigure
# Terminal 4:
rosrun rqt_plot rqt_plot /setpoint:data /process_value:data /error:data
```

**Tabel Observasi P08 – Respons Step (Setpoint = 100 RPM):**

| Percobaan | Kp  | Ki   | Kd    | Rise Time (s) | Overshoot (%) | Settling Time (s) | SS Error |
|-----------|-----|------|-------|--------------|--------------|------------------|---------|
| 1 (P only)| 1.0 | 0    | 0     |              |              |                  |         |
| 2         | 2.0 | 0    | 0     |              |              |                  |         |
| 3 (PI)    | 1.5 | 0.3  | 0     |              |              |                  |         |
| 4 (PID)   | 1.5 | 0.3  | 0.05  |              |              |                  |         |
| 5 (tuned) |     |      |       |              |              |                  |         |

**Pertanyaan Analisa P08:**
1. Jelaskan pengaruh setiap komponen PID pada respons step yang Anda amati!
2. Apa nilai Kp, Ki, Kd optimal yang Anda temukan? Bagaimana proses tuning Anda?
3. Apa yang terjadi jika Ki terlalu besar? Jelaskan fenomena integral windup!

---

### PERCOBAAN P09 – Go-to-Goal Controller di Gazebo

**Tujuan:** Mengimplementasikan kontroler go-to-goal untuk robot mobile di simulasi Gazebo

**Langkah Kerja:**

1. Launch Gazebo dengan robot diferensial
2. Jalankan node go_to_goal yang mensubscribe `/odom` dan mempublish `/cmd_vel`
3. Berikan target koordinat dan amati pergerakan robot

```bash
# Terminal 1:
roslaunch modul09_kinematika p09_go_to_goal.launch
# Terminal 2:
rosrun modul09_kinematika p09_go_to_goal.py
# Terminal 3 (kirim target):
rostopic pub /goal geometry_msgs/Point "x: 2.0 y: 1.5 z: 0.0"
```

**Tabel Observasi P09:**

| No | Target (x,y) | Kρ  | Kα  | Jarak Awal (m) | Error Posisi Akhir (m) | Waktu Capai (s) | Overshoot Path? |
|----|-------------|-----|-----|---------------|----------------------|----------------|----------------|
| 1  | (2.0, 0.0)  | 0.5 | 1.0 |               |                      |                |                |
| 2  | (2.0, 2.0)  | 0.5 | 1.0 |               |                      |                |                |
| 3  | (0.0, 3.0)  | 0.5 | 1.0 |               |                      |                |                |
| 4  | (2.0, 0.0)  | 1.0 | 1.0 |               |                      |                |                |
| 5  | (2.0, 0.0)  | 0.5 | 2.0 |               |                      |                |                |

**Pertanyaan Analisa P09:**
1. Bagaimana pengaruh Kρ terhadap kecepatan robot mendekati target?
2. Bagaimana pengaruh Kα terhadap ketepatan orientasi robot saat mendekati target?
3. Apa batas controller ini? (Tidak bisa menghindari obstacle)

---

### PERCOBAAN P10 – Odometri dari Encoder dengan rosserial

**Tujuan:** Mempublish odometri robot diferensial dari data encoder menggunakan rosserial

> **Mode A (Dengan Hardware):** Gunakan Arduino/ESP32 + encoder fisik  
> **Mode B (Simulasi):** Simulasikan encoder pulse dengan Python

**Langkah Kerja (Mode A – Hardware):**

1. Upload kode Arduino yang membaca encoder dan mempublish `/encoder_ticks`
2. Jalankan rosserial untuk menghubungkan Arduino ke ROS
3. Jalankan node odometry yang mengkonversi encoder ticks ke nav_msgs/Odometry

```bash
# Terminal 1:
roscore
# Terminal 2:
rosrun rosserial_python serial_node.py /dev/ttyUSB0 _baud:=57600
# Terminal 3:
rosrun modul09_kinematika p10_odometry.py
# Terminal 4:
rostopic echo /odom
```

**Tabel Observasi P10:**

| Gerakan Robot | Jarak Diukur (m) | Δx Odometri (m) | Δy Odometri (m) | Error (%) |
|--------------|-----------------|----------------|----------------|---------|
| Maju lurus 1m |                |                |                |         |
| Maju lurus 2m |                |                |                |         |
| Putar 90°    |                |                |                |         |
| Putar 360°   |                |                |                |         |

---

### PERCOBAAN P11 – diff_drive_controller dengan ros_control

**Tujuan:** Mengonfigurasi dan menjalankan diff_drive_controller menggunakan framework ros_control

**Langkah Kerja:**

1. Buat file `config/controllers.yaml` dengan konfigurasi controller
2. Buat launch file yang memuat controller menggunakan controller_manager
3. Kirim perintah kecepatan dan verifikasi odometri

```bash
roslaunch modul09_kinematika p11_ros_control.launch
# Kirim perintah:
rostopic pub /diff_drive_controller/cmd_vel geometry_msgs/Twist \
  "linear: {x: 0.2} angular: {z: 0.0}" -r 10
```

**Checklist Observasi P11:**
- [ ] `rosservice call /controller_manager/list_controllers` menampilkan `diff_drive_controller` RUNNING
- [ ] `rostopic echo /diff_drive_controller/odom` menampilkan pose robot berubah
- [ ] `rosrun tf tf_echo odom base_link` menampilkan transformasi berubah
- [ ] Robot bergerak maju di Gazebo saat menerima cmd_vel

**Tabel Perbandingan P11:**

| Parameter | diff_drive_controller | Implementasi manual P09 | Selisih |
|-----------|----------------------|------------------------|---------|
| Kecepatan update odometri (Hz) | | | |
| Error posisi setelah 1m (cm) | | | |

---

### PERCOBAAN P12 – Validasi FK dan IK di Gazebo

**Tujuan:** Memvalidasi implementasi FK/IK terhadap ground truth di Gazebo

**Langkah Kerja:**

1. Launch robot di Gazebo
2. Pindahkan robot ke posisi tertentu dengan `/cmd_vel`
3. Bandingkan pose dari `/odom` dengan kalkulasi FK dari `/joint_states`

```bash
roslaunch modul09_kinematika p12_gazebo_validation.launch
```

**Tabel Validasi P12:**

| Joint State (θ₁,θ₂,θ₃) | FK Terhitung (x,y,z) | Pose dari /odom (x,y,z) | Selisih (m) |
|------------------------|---------------------|------------------------|------------|
|                        |                     |                        |            |
|                        |                     |                        |            |
|                        |                     |                        |            |

---

### PERCOBAAN P13 – Cascade Controller

**Tujuan:** Mengimplementasikan kontroler cascade (outer: posisi, inner: kecepatan)

**Langkah Kerja:**

1. Implementasikan dua PID: `pid_position` (outer loop) dan `pid_velocity` (inner loop)
2. Outer loop menerima target posisi, menghasilkan referensi kecepatan
3. Inner loop menerima referensi kecepatan, menghasilkan sinyal kontrol motor

```bash
rosrun modul09_kinematika p13_cascade_controller.py
```

**Tabel Observasi P13:**

| Target Posisi (m) | Kp_pos | Kp_vel | Ki_vel | Overshoot (%) | Settling Time (s) | Error Akhir (cm) |
|------------------|--------|--------|--------|--------------|------------------|----------------|
| 1.0              | 1.0    | 2.0    | 0.5    |              |                  |                |
| 1.0              | 2.0    | 2.0    | 0.5    |              |                  |                |
| 1.0              | 1.0    | 4.0    | 0.5    |              |                  |                |
| 2.0              | 1.0    | 2.0    | 0.5    |              |                  |                |

**Pertanyaan Analisa P13:**
1. Apa keunggulan cascade controller dibanding single PID?
2. Bagaimana hubungan bandwidth outer loop dan inner loop yang ideal?

---

### PERCOBAAN P14 – Kinematika Robot Omni-Directional 3 Roda

**Tujuan:** Mengimplementasikan kinematika robot omni 3 roda

**Langkah Kerja:**

1. Implementasikan fungsi `omni_ik(vx, vy, omega_z)` → `[ω₁, ω₂, ω₃]`
2. Implementasikan fungsi `omni_fk(ω₁, ω₂, ω₃)` → `[vx, vy, omega_z]` (pseudoinverse)
3. Verifikasi: IK → FK → bandingkan dengan input awal

```bash
rosrun modul09_kinematika p14_omni_kinematics.py
```

**Tabel Observasi P14:**

| Input (vx, vy, ωz) | ω₁ (rad/s) | ω₂ (rad/s) | ω₃ (rad/s) | FK vx | FK vy | FK ωz | Error |
|--------------------|-----------|-----------|-----------|-------|-------|-------|-------|
| (0.2, 0.0, 0.0) – maju | | | | | | | |
| (0.0, 0.2, 0.0) – geser | | | | | | | |
| (0.0, 0.0, 0.5) – putar | | | | | | | |
| (0.2, 0.2, 0.0) – diagonal | | | | | | | |
| (0.1, -0.1, 0.3) – complex | | | | | | | |

---

### PERCOBAAN P15 – Integrasi Sistem Lengkap

**Tujuan:** Mengintegrasikan FK, TF, kontroler PID, odometri, dan Go-to-Goal dalam satu sistem

**Langkah Kerja:**

1. Launch sistem lengkap:

```bash
roslaunch modul09_kinematika p15_integration.launch
```

2. Sistem terdiri dari:
   - Gazebo dengan robot diferensial
   - diff_drive_controller (ros_control)
   - Odometri publisher
   - TF broadcaster (odom → base_link)
   - robot_state_publisher (FK)
   - Go-to-Goal controller
   - RViz untuk monitoring

3. Uji skenario lengkap:
   a. Kirim target pose A → tunggu robot tiba
   b. Kirim target pose B → tunggu robot tiba
   c. Kirim target pose C → tunggu robot tiba

**Tabel Observasi P15 – Trajectory Multi-Waypoint:**

| Waypoint | Target (x,y) | Pose Tiba (x,y) | Error (cm) | Waktu Tempuh (s) |
|---------|-------------|----------------|-----------|----------------|
| A       | (1.0, 0.0)  |                |           |                |
| B       | (1.0, 1.0)  |                |           |                |
| C       | (0.0, 1.0)  |                |           |                |
| D       | (0.0, 0.0)  |                |           |                |

**Checklist Sistem Terintegrasi P15:**
- [ ] roscore berjalan
- [ ] Gazebo berjalan dengan robot
- [ ] RViz menampilkan: robot model, TF, odometri path, laser scan
- [ ] `/cmd_vel` dipublish oleh go-to-goal node
- [ ] `/odom` dipublish oleh diff_drive_controller
- [ ] TF tree lengkap: odom → base_link → laser_frame
- [ ] Robot berhasil mengunjungi semua waypoint

---

## F. ANALISA

### Analisa Umum

Jawablah pertanyaan-pertanyaan berikut berdasarkan seluruh percobaan yang telah dilakukan:

1. **Hubungan FK-IK:** Jelaskan hubungan FK dan IK! Mengapa keduanya diperlukan dalam sistem robotika?

2. **Akurasi Metode IK:** Bandingkan akurasi IK analitik (P03) vs IK numerik (P04)! Dalam kondisi apa Anda akan memilih masing-masing?

3. **Pentingnya TF:** Mengapa ROS menggunakan sistem TF alih-alih mengirimkan koordinat absolut secara langsung?

4. **Tuning PID:** Berdasarkan Percobaan P08, buatlah grafik yang menunjukkan efek Kp, Ki, Kd terhadap rise time, overshoot, dan settling time!

5. **Odometri vs Ground Truth:** Seberapa akurat odometri? Faktor apa yang paling besar memengaruhi akurasinya? (Berdasarkan P10 atau P12)

6. **Keunggulan ros_control:** Apa keunggulan menggunakan framework ros_control (P11) dibandingkan implementasi controller manual (P09)?

7. **Analisa Sistem Terintegrasi:** Dari P15, faktor apa yang membatasi akurasi go-to-goal controller Anda?

---

## G. KESIMPULAN

Tuliskan kesimpulan praktikum berdasarkan hasil percobaan. Pastikan kesimpulan:
- Menjawab tujuan pembelajaran (poin A)
- Berdasarkan data yang diperoleh (tabel observasi)
- Memuat nilai numerik yang relevan (misalnya: "PID dengan Kp=1.5, Ki=0.3 menghasilkan overshoot 8% dengan settling time 2.1 detik")
- Menyebutkan keterbatasan dan saran perbaikan

**Contoh format kesimpulan:**

> Percobaan P01 membuktikan bahwa FK robot 2-DOF dapat dihitung dengan persamaan trigonometri sederhana. Hasil kode Python konsisten dengan perhitungan manual dengan error < 0.001 m (akibat pembulatan floating point). FK dengan parameter DH (P02) memberikan metode yang lebih sistematis dan dapat digeneralisasi ke n-DOF...

---

## H. REFERENSI

1. Craig, J.J. (2018). *Introduction to Robotics: Mechanics and Control* (4th ed.). Pearson.
2. Siciliano, B., et al. (2010). *Robotics: Modelling, Planning and Control*. Springer.
3. Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.
4. ROS Wiki – tf package: http://wiki.ros.org/tf
5. ROS Wiki – ros_control: http://wiki.ros.org/ros_control
6. ROS Wiki – diff_drive_controller: http://wiki.ros.org/diff_drive_controller
7. ROS Wiki – robot_state_publisher: http://wiki.ros.org/robot_state_publisher
8. Corke, P. (2017). *Robotics, Vision and Control* (2nd ed.). Springer.
9. Siegwart, R., et al. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.
10. Astrom, K.J., & Hagglund, T. (2006). *Advanced PID Control*. ISA Press.
