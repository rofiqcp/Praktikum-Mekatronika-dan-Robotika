# PROMPT MODUL 09: ROS KINEMATIKA DAN KONTROLER
## 45 Slide Prompts untuk NotebookLLM

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 09 – ROS Kinematika dan Kontroler

---

> **Petunjuk Penggunaan:**  
> Salin setiap prompt di bawah ke NotebookLLM. Setiap prompt dirancang untuk menghasilkan satu slide presentasi yang lengkap, informatif, dan terstruktur. Urutkan slide 1–45 untuk mendapatkan materi presentasi lengkap.

---

## BAGIAN 1: PENGANTAR DAN KONSEP DASAR (Slide 1–6)

---

### Slide 01 – Cover & Pendahuluan Modul

```
Buatkan slide cover presentasi akademik untuk Modul 09 "ROS Kinematika dan Kontroler" dengan informasi berikut:
- Judul utama: "ROS Kinematika dan Kontroler"
- Sub-judul: "Pemodelan, Analisis, dan Implementasi Sistem Kontrol Robot"
- Program Studi: Teknologi Rekayasa Otomasi
- Mata Kuliah: Praktikum Mekatronika dan Robotika
- Modul: 09
- Platform: ROS Noetic / Ubuntu 20.04

Tambahkan deskripsi singkat (2–3 kalimat) tentang pentingnya kinematika dan kontroler dalam robotika modern. Sertakan ikon atau simbol robot, diagram lengan robot sederhana, dan layout visual yang profesional dan modern.
```

---

### Slide 02 – Peta Konsep Modul

```
Buatkan slide peta konsep (mind map) untuk Modul 09 "ROS Kinematika dan Kontroler". Peta konsep harus mencakup 5 cabang utama:
1. Kinematika (FK, IK, DH Parameters, Jacobian)
2. Kontroler (PID, Position Control, Velocity Control, Cascade)
3. Robot Mobile (Differential Drive, Omni Drive, Odometri)
4. ROS Toolchain (TF, ros_control, Gazebo Plugin, URDF)
5. Implementasi (15 Percobaan, Hardware Setup, Mini PC)

Setiap cabang memiliki 3–4 sub-cabang. Gunakan warna berbeda untuk setiap cabang utama. Format visual sebagai mind map yang jelas dan mudah dibaca.
```

---

### Slide 03 – Tujuan Pembelajaran (CPMK)

```
Buatkan slide tujuan pembelajaran untuk Modul 09 "ROS Kinematika dan Kontroler" dengan format CPMK (Capaian Pembelajaran Mata Kuliah). Tujuan pembelajaran terdiri dari:

CPMK-1: Mahasiswa mampu menghitung forward kinematics dan inverse kinematics robot 2-DOF dan 3-DOF secara analitik dan numerik
CPMK-2: Mahasiswa mampu membangun parameter DH dan matriks transformasi homogen untuk robot serial
CPMK-3: Mahasiswa mampu merancang dan mengimplementasikan kontroler PID untuk robot mobile di ROS
CPMK-4: Mahasiswa mampu menggunakan framework ros_control dan TF tree di ROS
CPMK-5: Mahasiswa mampu mensimulasikan sistem kontrol robot di Gazebo dengan plugin diferensial drive

Presentasikan dalam tabel atau daftar terstruktur dengan indikator ketercapaian untuk setiap CPMK.
```

---

### Slide 04 – Apa itu Kinematika Robot?

```
Buatkan slide edukatif tentang "Definisi dan Ruang Lingkup Kinematika Robot" dengan konten berikut:

1. Definisi kinematika: mempelajari gerak tanpa mempertimbangkan gaya penyebabnya
2. Dua jenis utama kinematika robotika:
   - Forward Kinematics (FK): dari nilai sendi → posisi end-effector
   - Inverse Kinematics (IK): dari posisi end-effector → nilai sendi
3. Perbedaan antara Joint Space dan Cartesian Space/Task Space
4. Contoh ilustrasi: robot lengan 2-DOF dengan diagram arrow yang jelas
5. Mengapa kinematika penting? (3 aplikasi nyata: pick-and-place, surgical robot, mobile robot navigation)

Sertakan diagram visual sederhana dan persamaan matematika dasar. Gunakan bahasa Indonesia yang jelas.
```

---

### Slide 05 – Representasi Posisi dan Orientasi

```
Buatkan slide tentang "Representasi Posisi dan Orientasi dalam Robotika" dengan cakupan:

1. Representasi posisi: vektor kolom p = [x, y, z]ᵀ
2. Tiga cara merepresentasikan orientasi:
   a. Matriks Rotasi R (3×3) – jelaskan aturan tangan kanan
   b. Euler Angles (Roll-Pitch-Yaw) – gunakan notasi ZYX
   c. Quaternion (q0, q1, q2, q3) – mengapa ROS menggunakan ini (menghindari gimbal lock)
3. Matriks Transformasi Homogen T (4×4) – gabungkan rotasi dan translasi
4. Perbandingan keunggulan dan kelemahan setiap representasi dalam tabel
5. Contoh konversi: dari Euler (30°, 45°, 60°) ke matriks rotasi R

Sertakan visualisasi 3D frame koordinat (X merah, Y hijau, Z biru) sesuai standar ROS REP-103.
```

---

### Slide 06 – Pengantar ROS untuk Kinematika

```
Buatkan slide tentang "Ekosistem ROS untuk Kinematika Robot" yang menjelaskan:

1. Package ROS relevan untuk kinematika:
   - tf / tf2: manajemen transformasi antar frame
   - robot_state_publisher: publish transformasi dari URDF + joint states
   - joint_state_publisher: simulasi nilai joint
   - MoveIt!: planning library dengan FK/IK solver
   - kdl_parser: parsing URDF untuk KDL (Kinematics and Dynamics Library)

2. Alur data kinematika di ROS:
   /joint_states → robot_state_publisher → /tf → visualization (RViz)

3. Message type yang relevan:
   - sensor_msgs/JointState
   - geometry_msgs/Transform
   - geometry_msgs/Pose

4. Contoh rqt_graph sederhana yang menunjukkan hubungan antar node kinematika

Tampilkan diagram alur data yang jelas dengan warna berbeda untuk setiap layer.
```

---

## BAGIAN 2: FORWARD KINEMATICS (Slide 7–11)

---

### Slide 07 – Konsep Forward Kinematics

```
Buatkan slide konsep "Forward Kinematics (FK)" dengan konten:

1. Definisi formal FK: diberikan vektor sudut sendi q = [θ1, θ2, ..., θn], hitung pose end-effector T₀ₙ
2. Formula umum: T₀ₙ = T₀₁ · T₁₂ · T₂₃ · ... · T(n-1)n
3. Ilustrasi visual: robot 2-DOF planar dengan label:
   - θ1 = sudut sendi 1 (shoulder)
   - θ2 = sudut sendi 2 (elbow)
   - L1 = panjang lengan 1
   - L2 = panjang lengan 2
4. Persamaan FK 2-DOF:
   x = L1·cos(θ1) + L2·cos(θ1+θ2)
   y = L1·sin(θ1) + L2·sin(θ1+θ2)
5. Contoh numerik: θ1=30°, θ2=45°, L1=0.5m, L2=0.3m → x=?, y=?
6. Aplikasi FK: robot arm pick-and-place, validasi workspace

Gunakan diagram animasi atau multi-langkah untuk menunjukkan proses kalkulasi.
```

---

### Slide 08 – Matriks Transformasi Homogen

```
Buatkan slide detail tentang "Matriks Transformasi Homogen dalam FK" mencakup:

1. Struktur matriks T (4×4):
   T = | R(3×3)  p(3×1) |
       | 0(1×3)    1    |
   di mana R = matriks rotasi, p = vektor translasi

2. Tiga matriks rotasi dasar:
   - Rx(α): rotasi terhadap sumbu X
   - Ry(β): rotasi terhadap sumbu Y  
   - Rz(γ): rotasi terhadap sumbu Z
   Tampilkan matriks lengkap dengan elemen cos dan sin

3. Sifat matriks transformasi homogen:
   - T⁻¹ = [Rᵀ  -Rᵀ·p; 0  1]
   - Komposisi: T₀n = T₀₁ · T₁₂ · ... · T(n-1)n

4. Contoh perhitungan: hitung T₀₂ untuk robot 2-DOF dengan nilai konkret
5. Visualisasi: animasi frame koordinat yang bergerak mengikuti transformasi

Gunakan tabel berwarna untuk menunjukkan elemen matriks yang berbeda.
```

---

### Slide 09 – Parameter Denavit-Hartenberg (DH)

```
Buatkan slide komprehensif tentang "Parameter Denavit-Hartenberg (DH)" dengan:

1. Definisi 4 parameter DH:
   - a (link length): jarak antara zi-1 dan zi sepanjang xi
   - α (link twist): sudut antara zi-1 dan zi sekitar xi
   - d (link offset): jarak antara xi-1 dan xi sepanjang zi-1
   - θ (joint angle): sudut antara xi-1 dan xi sekitar zi-1

2. Matriks DH standar (tampilkan penuh 4×4):
   T = Rz(θ) · Tz(d) · Tx(a) · Rx(α)

3. Aturan penempatan frame DH (step by step dengan diagram):
   Langkah 1: Identifikasi sumbu sendi (zi)
   Langkah 2: Temukan xi (tegak lurus ke zi-1 dan zi)
   Langkah 3: Ukur parameter a, α, d, θ

4. Tabel DH untuk robot 2-DOF (contoh)
5. Contoh tabel DH untuk robot 3-DOF (UR-like)
6. Tips dan kesalahan umum dalam penerapan konvensi DH

Sertakan diagram 3D yang menunjukkan hubungan antar frame dengan label parameter DH.
```

---

### Slide 10 – Implementasi FK di ROS Python

```
Buatkan slide teknis "Implementasi Forward Kinematics di ROS dengan Python" yang menampilkan:

1. Cara membangun FK menggunakan tf.transformations:
   - euler_matrix(ai, aj, ak, axes='sxyz')
   - quaternion_from_euler(roll, pitch, yaw)
   - quaternion_multiply(q1, q2)

2. Kode Python lengkap untuk FK robot 2-DOF:
   import numpy as np
   def dh_matrix(theta, d, a, alpha):
       # buat matriks 4x4 DH
       ...
   def forward_kinematics(joint_angles, dh_params):
       T = np.eye(4)
       for i, q in enumerate(joint_angles):
           T = T @ dh_matrix(q + dh_params[i][0], ...)
       return T

3. Cara publish hasil FK sebagai TF di ROS
4. Cara visualisasi FK di RViz dengan marker
5. Contoh output: posisi end-effector dari input joint angles [0.5, 1.0, 0.3] rad

Gunakan syntax highlighting dan penjelasan per baris kode. Tampilkan screenshot RViz.
```

---

### Slide 11 – Visualisasi FK di RViz

```
Buatkan slide panduan "Visualisasi Forward Kinematics di RViz" yang mencakup:

1. Setup RViz untuk visualisasi robot:
   - Add display: RobotModel (memerlukan URDF di /robot_description)
   - Add display: TF (untuk melihat frame koordinat)
   - Add display: Marker (untuk visualisasi custom)

2. Cara menjalankan robot_state_publisher:
   rosrun robot_state_publisher robot_state_publisher
   atau via launch file dengan parameter robot_description

3. Cara menjalankan joint_state_publisher_gui untuk kontrol slider:
   rosrun joint_state_publisher_gui joint_state_publisher_gui

4. Interpretasi hasil visualisasi:
   - Frame world (sumbu besar)
   - Frame tiap sendi
   - Frame end-effector
   - Model visual URDF

5. Contoh langkah kerja: dari URDF sederhana ke visualisasi FK interaktif
6. Screenshot RViz yang menunjukkan robot dengan joint_state_publisher_gui

Sertakan gambar screenshot RViz dan perintah terminal yang diperlukan.
```

---

## BAGIAN 3: INVERSE KINEMATICS (Slide 12–16)

---

### Slide 12 – Konsep Inverse Kinematics

```
Buatkan slide "Konsep Inverse Kinematics (IK)" yang menjelaskan:

1. Definisi IK: diberikan posisi/orientasi target end-effector, cari konfigurasi sendi yang memenuhinya
2. Tantangan IK dibanding FK:
   - Multiple solutions (banyak solusi)
   - No solution (di luar workspace)
   - Singularities (konfigurasi degenerate)
   - Non-linear problem

3. Klasifikasi metode IK:
   a. Analitik/Closed-form: cepat, exact, hanya untuk robot tertentu
   b. Numerik/Iteratif: umum, lebih lambat, bisa diverge
   c. Geometric/Trigonometric: intuitif, untuk robot planar

4. Ilustrasi "elbow up vs elbow down" untuk robot 2-DOF
5. Konsep workspace: reachable workspace vs dexterous workspace
6. Contoh aplikasi: mengapa IK lebih sulit dari FK dalam autonomous robot arm?

Gunakan diagram visual yang kontras antara FK (mudah) dan IK (kompleks).
```

---

### Slide 13 – IK Analitik Robot 2-DOF

```
Buatkan slide step-by-step "Inverse Kinematics Analitik Robot 2-DOF" dengan:

1. Masalah: diberikan target (x_t, y_t), cari (θ₁, θ₂)
2. Langkah 1 – Cari θ₂ dengan hukum cosinus:
   cos(θ₂) = (x² + y² - L₁² - L₂²) / (2·L₁·L₂)
   θ₂ = atan2(±√(1 - cos²θ₂), cos θ₂)
3. Langkah 2 – Cari θ₁:
   θ₁ = atan2(y, x) - atan2(L₂·sin θ₂, L₁ + L₂·cos θ₂)
4. Dua solusi (elbow up/down):
   Solusi 1: θ₂ > 0 (elbow up / counter-clockwise)
   Solusi 2: θ₂ < 0 (elbow down / clockwise)
5. Validasi: substitusi kembali ke FK untuk cek
6. Contoh numerik: x=0.5, y=0.4, L1=0.5, L2=0.3 → θ₁=?, θ₂=?
7. Kasus singularitas: kapan tidak ada solusi?

Tampilkan diagram geometris yang jelas untuk setiap langkah derivasi.
```

---

### Slide 14 – IK Numerik: Jacobian Pseudoinverse

```
Buatkan slide teknis "IK Numerik dengan Metode Jacobian Pseudoinverse" mencakup:

1. Mengapa perlu metode numerik? Robot >3-DOF, posisi + orientasi
2. Konsep dasar: minimasi error pose secara iteratif
   Δq = J⁺ · Δx
   di mana J⁺ = pseudoinverse dari Jacobian J

3. Algoritma iterasi:
   Loop:
   - Hitung FK(q_current) → x_current
   - Hitung error: e = x_target - x_current
   - Cek konvergensi: jika ||e|| < ε, berhenti
   - Hitung J(q_current)
   - Update: q_new = q_current + α·J⁺·e

4. Metode Damped Least Squares (DLS) untuk stabilitas:
   J⁺_DLS = Jᵀ(JJᵀ + λ²I)⁻¹
   Parameter λ (damping) mencegah divergensi dekat singularitas

5. Perbandingan metode:
   | Metode | Kecepatan | Stabilitas | Untuk |
   | Jacobian Transpose | Cepat | Rendah | Real-time |
   | Pseudoinverse | Sedang | Sedang | General |
   | DLS | Lebih lambat | Tinggi | Dekat singularitas |

6. Implementasi di Python menggunakan numpy.linalg.pinv()

Gunakan diagram alur algoritma dan visualisasi konvergensi iterasi.
```

---

### Slide 15 – IK dengan MoveIt! di ROS

```
Buatkan slide panduan "Inverse Kinematics dengan MoveIt! di ROS" yang menampilkan:

1. Apa itu MoveIt!? Package planning robot di ROS dengan IK solver built-in
2. IK Solver yang tersedia di MoveIt!:
   - KDL (default): Jacobian-based numerik
   - TRAC-IK: lebih cepat dan robust dari KDL
   - IKFast (OpenRAVE): analitik, sangat cepat
   - BioIK: metaheuristic, untuk redundant robots

3. Cara memanggil IK service di ROS:
   rosservice call /compute_ik ...
   atau via Python API:
   move_group.set_pose_target(target_pose)
   plan = move_group.plan()
   move_group.execute(plan)

4. Setup MoveIt! untuk robot sederhana:
   - Jalankan MoveIt! Setup Assistant
   - Definisikan planning group
   - Konfigurasi IK plugin

5. Cara mengintegrasikan MoveIt! IK dalam node ROS kustom
6. Contoh demo: robot arm menjangkau target pose dengan MoveIt!

Tampilkan diagram alur MoveIt! dan screenshot RViz dengan trajectory planning.
```

---

### Slide 16 – Singularitas dan Workspace

```
Buatkan slide "Singularitas Robot dan Analisis Workspace" yang mencakup:

1. Definisi singularitas: konfigurasi sendi di mana robot kehilangan satu atau lebih derajat kebebasan
   Matematika: rank(J) < min(m, n) atau det(J·Jᵀ) ≈ 0

2. Tiga tipe singularitas pada robot serial:
   a. Boundary singularity: end-effector di batas workspace (lengan terentang/terlipat penuh)
   b. Interior singularity: dua sumbu sendi kolinear
   c. Wrist singularity: tiga sumbu wrist bersinggungan

3. Dampak singularitas:
   - Kecepatan sendi → tak terhingga saat singularitas
   - IK numerik diverge
   - Kehilangan kontrol arah tertentu

4. Cara deteksi: manipulability index = √(det(J·Jᵀ))
5. Analisis workspace:
   - Reachable workspace: semua pose yang bisa dicapai (1 konfigurasi sendi apapun)
   - Dexterous workspace: pose yang bisa dicapai dengan semua orientasi

6. Cara plot workspace di Python menggunakan Monte Carlo sampling FK
7. Strategi menghindari singularitas dalam trajectory planning

Sertakan visualisasi 2D/3D workspace dan diagram singularitas yang jelas.
```

---

## BAGIAN 4: JACOBIAN DAN KINEMATIKA DIFERENSIAL (Slide 17–19)

---

### Slide 17 – Matriks Jacobian

```
Buatkan slide mendalam tentang "Matriks Jacobian dalam Kinematika Robot" mencakup:

1. Definisi Jacobian: J(q) menghubungkan kecepatan sendi q̇ dengan kecepatan Cartesian ẋ:
   ẋ = J(q) · q̇
   di mana ẋ = [vx, vy, vz, ωx, ωy, ωz]ᵀ (6D), J adalah 6×n

2. Dua bagian Jacobian:
   - Jacobian Linear Jv (3×n): untuk kecepatan translasi
   - Jacobian Angular Jω (3×n): untuk kecepatan rotasi
   Untuk sendi revolute ke-i: Jvi = zi-1 × (pn - pi-1), Jωi = zi-1

3. Cara komputasi kolom Jacobian dari matriks FK:
   Step 1: Hitung semua T₀ᵢ (FK parsial)
   Step 2: Ekstrak zi dan pi dari setiap T₀ᵢ
   Step 3: Hitung cross product dan susun kolom

4. Hubungan Jacobian dengan:
   - Velocity kinematics: ẋ = J·q̇
   - Force/torque: τ = Jᵀ·F (principle of virtual work)
   - Singularitas: det(JJᵀ) = 0
   - Manipulability: μ = √(det(J·Jᵀ))

5. Contoh Jacobian untuk robot 2-DOF planar (tampilkan matriks 2×2)

Gunakan derivasi bertahap yang jelas dengan diagram geometris.
```

---

### Slide 18 – Kinematika Robot Diferensial Drive

```
Buatkan slide "Kinematika Robot Mobile Diferensial Drive" yang menjelaskan:

1. Geometri robot diferensial:
   - Dua roda aktif (kiri/kanan)
   - Satu atau dua roda kastor (passive)
   - Parameter: radius roda R, wheelbase L

2. Model kinematika:
   v  = R/2 · (ωR + ωL)      -- kecepatan linear (m/s)
   ω  = R/L · (ωR - ωL)      -- kecepatan angular (rad/s)
   ẋ  = v·cos(θ), ẏ = v·sin(θ), θ̇ = ω

3. Invers kinematika roda:
   ωR = (v + ωL/2) / R = (2v + ωL) / (2R)
   ωL = (v - ωL/2) / R = (2v - ωL) / (2R)

4. Matriks kinematika (bentuk kompak):
   [v]   = R/2 · [1  1] · [ωL]
   [ω]           [1 -1]   [ωR]  × 1/L terms

5. Odometri:
   Δx = Δs·cos(θ + Δθ/2)
   Δy = Δs·sin(θ + Δθ/2)
   Δθ = (ΔsR - ΔsL) / L

6. Sumber error odometri dan cara mitigasinya
7. Penerapan di ROS: /cmd_vel Twist → DiffDriveController → encoder feedback

Sertakan diagram geometri robot dan tabel contoh nilai numerik.
```

---

### Slide 19 – Kinematika Robot Omni-Directional

```
Buatkan slide "Kinematika Robot Omni-Directional (3 Roda & 4 Roda Mecanum)" mencakup:

1. Keunggulan robot omni vs diferensial: holonomic (gerak ke semua arah tanpa rotasi badan)
2. Robot 3 roda omni (sudut 120°):
   Matriks kinematika invers (IK roda):
   | ω1 |   1   | -sin(β1)  cos(β1)  L | | vx |
   | ω2 | = --- | -sin(β2)  cos(β2)  L | | vy |
   | ω3 |   R   | -sin(β3)  cos(β3)  L | | ωz |
   β1=90°, β2=210°, β3=330°

3. Robot 4 roda Mecanum:
   Roda Mecanum: roller bersudut 45° memungkinkan gerak lateral
   ω1 = (1/R)(vx - vy - (lx+ly)·ωz)
   ω2 = (1/R)(vx + vy + (lx+ly)·ωz)  [dst]

4. FK omni (dari kecepatan roda → kecepatan robot):
   Gunakan pseudoinverse dari matriks IK roda

5. Implementasi di ROS: paket omnidirectional_controller atau custom node
6. Perbandingan tiga jenis robot mobile:
   | Tipe | Holonomic | Kompleksitas | Traksi |
   | Diferensial | Tidak | Rendah | Baik |
   | Omni 3-roda | Ya | Sedang | Sedang |
   | Mecanum | Ya | Tinggi | Rendah |

Sertakan diagram roda omni/mecanum dan simulasi gerak.
```

---

## BAGIAN 5: SISTEM KOORDINAT DAN TF ROS (Slide 20–22)

---

### Slide 20 – TF Tree di ROS

```
Buatkan slide komprehensif "TF Tree: Manajemen Frame Koordinat di ROS" yang mencakup:

1. Apa itu TF dan mengapa diperlukan?
   - Robot memiliki banyak komponen dengan frame koordinat berbeda
   - TF otomatis menangani konversi antar frame + waktu

2. Struktur TF Tree standar robot mobile:
   world → map → odom → base_link → base_footprint
                               ↕ laser_frame
                               ↕ camera_frame
                               ↕ left_wheel
                               ↕ right_wheel

3. Perbedaan frame penting:
   - map: frame global dari SLAM (bisa loncat)
   - odom: frame kontinyu dari odometri (drift)
   - base_link: pusat robot
   - base_footprint: proyeksi ke lantai

4. Tool visualisasi TF:
   rosrun tf view_frames  → generate PDF TF tree
   rosrun rqt_tf_tree rqt_tf_tree  → GUI
   rviz → TF display

5. Perintah debug TF:
   rostopic echo /tf
   rosrun tf tf_echo odom base_link
   rosrun tf tf_monitor

6. Konsep stamped transform: setiap transform memiliki timestamp

Tampilkan diagram TF tree visual dan contoh output tf_echo.
```

---

### Slide 21 – Broadcast dan Listen TF

```
Buatkan slide teknis "Cara Broadcast dan Listen TF di ROS Python" dengan:

1. Static vs Dynamic TF:
   - Static TF: transformasi tidak berubah (misal: kamera → base_link)
     rosrun tf2_ros static_transform_publisher x y z yaw pitch roll parent child
   - Dynamic TF: berubah seiring waktu (misal: odom → base_link)

2. Kode Python TF Broadcaster (dynamic):
   import rospy, tf
   br = tf.TransformBroadcaster()
   # Dalam loop:
   br.sendTransform((x, y, 0),
                    tf.transformations.quaternion_from_euler(0, 0, theta),
                    rospy.Time.now(),
                    "base_link", "odom")

3. Kode Python TF Listener:
   listener = tf.TransformListener()
   listener.waitForTransform("target", "source", rospy.Time(), rospy.Duration(4))
   (trans, rot) = listener.lookupTransform("target", "source", rospy.Time(0))

4. Konversi koordinat menggunakan TF:
   point_in_map = listener.transformPoint("map", point_in_odom)

5. Error umum dan solusinya:
   - "Lookup would require extrapolation" → gunakan rospy.Time(0)
   - "Transform not found" → cek TF tree dan waktu

6. Perbedaan tf (ROS 1) dan tf2 (ROS 2 / modern ROS 1)

Gunakan kode berwarna dan penjelasan per blok.
```

---

### Slide 22 – URDF dan robot_state_publisher

```
Buatkan slide panduan "URDF dan robot_state_publisher untuk FK Otomatis" mencakup:

1. Apa itu URDF (Unified Robot Description Format)?
   - XML file mendefinisikan struktur robot: link, joint, sensor
   - Digunakan oleh ROS untuk FK, collision, visualization

2. Komponen utama URDF:
   - <link>: geometri, inersia, visual, collision
   - <joint>: tipe (revolute/prismatic/fixed/continuous), parent, child, axis, limits
   - <transmission>: mapping joint ke hardware interface

3. Contoh URDF minimal untuk robot diferensial:
   <robot name="diff_robot">
     <link name="base_link"> ... </link>
     <link name="left_wheel"> ... </link>
     <joint name="left_wheel_joint" type="continuous">
       <parent link="base_link"/>
       <child link="left_wheel"/>
       <axis xyz="0 1 0"/>
     </joint>
   </robot>

4. Cara launch robot_state_publisher:
   <param name="robot_description" command="$(find xacro) robot.urdf.xacro"/>
   <node name="robot_state_publisher" pkg="robot_state_publisher" type="robot_state_publisher"/>

5. Alur kerja FK otomatis:
   URDF → robot_state_publisher → /tf (FK setiap saat)
   /joint_states → robot_state_publisher → /tf

6. Xacro: URDF dengan macro – lebih modular dan reusable

Tampilkan diagram alur URDF → TF dan screenshot RViz dengan TF markers.
```

---

## BAGIAN 6: PID CONTROLLER (Slide 23–27)

---

### Slide 23 – Teori PID Controller

```
Buatkan slide komprehensif "Teori PID Controller" yang menjelaskan:

1. Struktur PID Controller:
   u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·de(t)/dt
   di mana e(t) = setpoint - process_variable

2. Penjelasan setiap komponen:
   - P (Proportional): aksi langsung, proporsional dengan error saat ini
     → Mempercepat respons tapi meningkatkan overshoot
   - I (Integral): akumulasi error historis
     → Menghilangkan steady-state error tapi bisa menyebabkan osilasi
   - D (Derivative): prediksi perubahan error
     → Meredam osilasi tapi sensitif terhadap noise

3. Diagram blok PID (Plant + Controller + Feedback)
4. Persamaan diskrit (untuk implementasi digital):
   u[k] = Kp·e[k] + Ki·T·Σe + Kd/T·(e[k]-e[k-1])

5. Parameter penting:
   - Kp: proportional gain
   - Ti = Kp/Ki: integral time
   - Td = Kd/Kp: derivative time

6. Karakteristik respons sistem (Rise Time, Overshoot, Settling Time, Steady Error)
7. Trade-off antara Kp, Ki, Kd dengan tabel efek perubahan gain

Gunakan diagram blok yang profesional dan grafik respons step input.
```

---

### Slide 24 – Tuning PID: Metode Manual dan Ziegler-Nichols

```
Buatkan slide panduan "Tuning PID: Metode Manual dan Ziegler-Nichols" dengan:

1. Mengapa tuning penting? Gain yang salah → osilasi, overshoot besar, sistem tidak stabil
2. Prosedur tuning manual (heuristik):
   Step 1: Set Ki=0, Kd=0; Naikkan Kp sampai respons cukup cepat
   Step 2: Tambah Ki sedikit demi sedikit hingga steady-state error hilang
   Step 3: Tambah Kd jika masih terjadi overshoot berlebih

3. Metode Ziegler-Nichols:
   - Set Ki=0, Kd=0
   - Naikkan Kp sampai osilasi berkelanjutan → Ku (Ultimate Gain)
   - Catat Pu (Ultimate Period)
   - Gunakan tabel: Kp=0.6Ku, Ti=0.5Pu, Td=0.125Pu

4. Metode Step Response (Open-loop):
   Dari kurva respons step, identifikasi:
   - K (proses gain)
   - L (dead time / lag)
   - T (time constant)
   Formula: Kp = 1.2T/(K·L), Ti = 2L, Td = 0.5L

5. Perbandingan metode tuning:
   | Metode | Akurasi | Kemudahan | Aplikasi |
   | Manual | Sedang | Mudah | Umum |
   | Ziegler-Nichols | Sedang | Sedang | Standar |
   | Auto-tune | Tinggi | Otomatis | Industri |

6. Demo: grafik before/after tuning PID

Sertakan grafik respons yang menunjukkan perbedaan hasil tuning.
```

---

### Slide 25 – Anti-Windup dan Derivative Kick

```
Buatkan slide teknis "Masalah Implementasi PID: Anti-Windup dan Derivative Kick" mencakup:

1. Masalah Integral Windup:
   - Terjadi saat output sudah tersaturasi (mencapai batas maksimum/minimum)
   - Integral terus bertambah meskipun tidak berpengaruh → overshoot besar saat saturasi selesai
   - Visualisasi: grafik integral windup vs normal

2. Strategi Anti-Windup:
   a. Clamping: hentikan integrasi saat output tersaturasi
   b. Back-calculation: kurangi integral proportional dengan saturasi
   c. Integral Separation: aktifkan integral hanya jika error kecil

3. Masalah Derivative Kick:
   - Ketika setpoint berubah tiba-tiba, derivatif error berlonjak besar
   - Menyebabkan spike pada output aktuator

4. Solusi Derivative Kick: Derivative on Measurement (bukan derivative on error)
   u_D = -Kd · d(process_value)/dt  ← gunakan ini
   (bukan: u_D = Kd · d(error)/dt)

5. Low-pass filter pada derivatif untuk meredam noise:
   D_filtered = α·D_prev + (1-α)·D_new   (α ≈ 0.7-0.9)

6. Kode pseudo untuk PID dengan anti-windup dan derivative filter

Tampilkan diagram perbandingan PID biasa vs PID dengan perbaikan.
```

---

### Slide 26 – PID di ROS: dynamic_reconfigure

```
Buatkan slide "Tuning PID Real-time dengan dynamic_reconfigure di ROS" yang mencakup:

1. Apa itu dynamic_reconfigure?
   - Package ROS untuk mengubah parameter node saat runtime (tanpa restart)
   - Sangat berguna untuk tuning PID secara interaktif

2. Cara membuat parameter PID yang dapat dikonfigurasi:
   a. Buat file .cfg (Python):
      gen = ParameterGenerator()
      gen.add("Kp", double_t, 0, "Proportional gain", 1.0, 0, 100)
      gen.add("Ki", double_t, 0, "Integral gain", 0.1, 0, 100)
      gen.add("Kd", double_t, 0, "Derivative gain", 0.01, 0, 10)
   b. Tambahkan callback di node
   c. Compile dengan catkin_make

3. Menggunakan rqt_reconfigure GUI:
   rosrun rqt_reconfigure rqt_reconfigure

4. Alur kerja tuning interaktif:
   - Jalankan robot + PID node
   - Buka rqt_reconfigure
   - Ubah Kp/Ki/Kd dan lihat respons di rqt_plot
   - Catat nilai optimal

5. Integrasi dengan rqt_plot untuk monitoring real-time:
   - Plot /setpoint, /process_value, /error secara bersamaan
   - Identifikasi overshoot, steady-state error

6. Contoh workflow lengkap: dari launch sampai tuning PID berhasil

Sertakan screenshot rqt_reconfigure dan rqt_plot.
```

---

### Slide 27 – Implementasi PID di ROS Python

```
Buatkan slide kode "Implementasi Node PID Controller di ROS Python" yang menampilkan:

1. Struktur file PID controller node (pid_controller.py)
2. Kode lengkap Python:
   #!/usr/bin/env python3
   import rospy
   from std_msgs.msg import Float64
   from geometry_msgs.msg import Twist

   class PIDController:
       def __init__(self):
           self.Kp = rospy.get_param('~Kp', 1.0)
           self.Ki = rospy.get_param('~Ki', 0.1)
           self.Kd = rospy.get_param('~Kd', 0.01)
           self.setpoint = 0.0
           self.integral = 0.0
           self.prev_error = 0.0
           # subscriber, publisher, timer

       def compute(self, process_value):
           error = self.setpoint - process_value
           # P, I, D, anti-windup
           return output

3. Cara integrasi dengan hardware melalui rosserial (Arduino/ESP32)
4. Launch file untuk menjalankan PID node dengan parameter
5. Cara test dengan rostopic pub dan monitoring dengan rqt_plot
6. Contoh output: grafik respons step yang menunjukkan PID bekerja

Gunakan syntax highlighting Python dan penjelasan per bagian kode.
```

---

## BAGIAN 7: KONTROLER ROBOT MOBILE DI ROS (Slide 28–32)

---

### Slide 28 – Arsitektur Kontrol Robot Mobile ROS

```
Buatkan slide "Arsitektur Lengkap Kontrol Robot Mobile di ROS" yang menampilkan:

1. Diagram layered architecture kontrol robot mobile:
   Layer 5: Mission Planning (goal setting)
   Layer 4: Path Planning (global planner)
   Layer 3: Trajectory Planning (local planner)
   Layer 2: Motion Control (velocity controller + PID)
   Layer 1: Hardware Interface (motor driver, encoder)

2. Alur message ROS:
   /move_base_goal → /cmd_vel → /motor_cmds → [Hardware] → /joint_states → /odom

3. Node-node utama dalam sistem:
   - move_base: navigation stack
   - velocity_controller: PID untuk kecepatan roda
   - odometry_node: estimasi pose dari encoder
   - tf_broadcaster: publish odom → base_link
   - robot_state_publisher: publish FK dari URDF

4. Topik ROS yang terlibat dengan tipe message-nya
5. Diagram rqt_graph yang khas untuk robot mobile ROS
6. Bottleneck umum dan cara optimasinya

Buat diagram layered yang visual dan informatif dengan warna berbeda per layer.
```

---

### Slide 29 – diff_drive_controller

```
Buatkan slide panduan "Konfigurasi dan Penggunaan diff_drive_controller" mencakup:

1. Apa itu diff_drive_controller?
   - Bagian dari ros_control
   - Menangani kontrol kecepatan robot diferensial secara lengkap
   - Subscribe /cmd_vel, publish /odom, broadcast TF odom→base_link

2. Instalasi:
   sudo apt install ros-noetic-diff-drive-controller

3. File konfigurasi YAML lengkap:
   diff_drive_controller:
     type: diff_drive_controller/DiffDriveController
     left_wheel: ['left_wheel_joint']
     right_wheel: ['right_wheel_joint']
     wheel_separation: 0.20
     wheel_radius: 0.05
     publish_rate: 50
     odom_frame_id: odom
     base_frame_id: base_link
     enable_odom_tf: true

4. Launch file untuk memuat controller:
   <rosparam file="$(find pkg)/config/controllers.yaml"/>
   <node name="controller_manager" pkg="controller_manager" type="spawner"
         args="joint_state_controller diff_drive_controller"/>

5. Cara kirim perintah:
   rostopic pub /cmd_vel geometry_msgs/Twist "linear: {x: 0.2} angular: {z: 0.1}"
   atau dengan teleop_twist_keyboard

6. Monitoring output: rostopic echo /odom, tf_echo odom base_link

Sertakan diagram alur controller manager dan contoh output terminal.
```

---

### Slide 30 – Go-to-Goal Controller

```
Buatkan slide algoritma "Go-to-Goal Controller untuk Robot Mobile" yang menjelaskan:

1. Problem: robot perlu bergerak dari pose awal ke pose target (x, y, θ)
2. Algoritma Proportional Go-to-Goal:
   - Hitung jarak: ρ = √(dx² + dy²)
   - Hitung sudut ke tujuan: α = atan2(dy, dx) - θ_robot
   - Hitung error orientasi tujuan: β = θ_goal - θ_robot - α
   - Kontrol: v = Kρ·ρ, ω = Kα·α + Kβ·β

3. Kondisi berhenti: jika ρ < ε (threshold jarak)

4. Masalah: robot bisa berputar terus jika berorientasi salah
5. Solusi Two-Phase Controller:
   Fase 1 (koreksi arah): jika |α| > threshold → hanya putar (v=0)
   Fase 2 (maju): jika |α| ≤ threshold → kombinasi v dan ω

6. Pseudo code dalam Python (go_to_goal_node.py):
   Mensubscribe: /odom
   Mempublish: /cmd_vel
   Callback: hitung error, jalankan kontroler, publish Twist

7. Demo simulasi: robot bergerak dari (0,0) ke (2,1.5) di Gazebo
8. Batas: tidak menghindari obstacle (perlu dikombinasi dengan obstacle avoidance)

Tampilkan diagram geometris go-to-goal dan grafik trajectory robot.
```

---

### Slide 31 – Odometri dan State Estimation

```
Buatkan slide "Odometri dan State Estimation Robot Mobile" yang mencakup:

1. Apa itu odometri? Estimasi pose dari integrasi kecepatan roda
2. Rumus odometri diferensial:
   ΔsR = 2π·R·ΔtickR / ticks_per_rev
   ΔsL = 2π·R·ΔtickL / ticks_per_rev
   Δs = (ΔsR + ΔsL) / 2    ← jarak tempuh rata-rata
   Δθ = (ΔsR - ΔsL) / L    ← perubahan sudut
   Δx = Δs·cos(θ + Δθ/2)
   Δy = Δs·sin(θ + Δθ/2)

3. Sumber error odometri:
   - Slip roda (terutama di permukaan licin)
   - Resolusi encoder (quantization error)
   - Ketidakakuratan parameter R dan L
   - Akumulasi error (drift)

4. Cara mengurangi drift:
   - Fusi sensor: gabungkan odometri + IMU + GPS/LiDAR (EKF/UKF)
   - Kalibrasi akurat parameter roda
   - Gunakan encoder resolusi tinggi (>1000 PPR)

5. Pesan nav_msgs/Odometry di ROS:
   - header, child_frame_id
   - pose (posisi + orientasi + covariance)
   - twist (kecepatan + covariance)

6. Cara publish odometri dari encoder (node Python)
7. Visualisasi: path odometri di RViz vs ground truth Gazebo

Tampilkan diagram geometris odometri dan grafik drift akumulasi.
```

---

### Slide 32 – ros_control Framework

```
Buatkan slide arsitektur "Framework ros_control untuk Kontrol Robot" yang menjelaskan:

1. Mengapa ros_control?
   - Standarisasi interface antara kontroler dan hardware
   - Swap kontroler saat runtime
   - Pisahkan logika kontrol dari hardware

2. Lapisan arsitektur ros_control:
   ┌──────────────────────────────┐
   │     Controller Manager       │
   │  ┌──────────┐ ┌───────────┐  │
   │  │ PID Vel  │ │ Diff Drive│  │
   │  └──────────┘ └───────────┘  │
   ├──────────────────────────────┤
   │     Hardware Interface       │
   │  (RobotHW / RobotHWSim)     │
   └──────────────────────────────┘

3. Tipe Joint Interface:
   - JointCommandInterface (effort/velocity/position)
   - JointStateInterface (read-only)
   - VelocityJointInterface (untuk roda)

4. Tipe Controller:
   | Controller | Package | Kegunaan |
   | JointPositionController | position_controllers | Posisi sendi |
   | JointVelocityController | velocity_controllers | Kecepatan sendi |
   | DiffDriveController | diff_drive_controller | Robot diferensial |

5. Cara spawn controller:
   rosservice call /controller_manager/load_controller "diff_drive_controller"
   rosservice call /controller_manager/switch_controller ...

6. Cara tulis Hardware Interface kustom untuk Arduino/ESP32

Gunakan diagram hierarki yang jelas dan berwarna.
```

---

## BAGIAN 8: SIMULASI GAZEBO (Slide 33–36)

---

### Slide 33 – Setup Robot di Gazebo

```
Buatkan slide panduan "Setup Robot Mobile di Simulasi Gazebo" yang mencakup:

1. Mengapa simulasi Gazebo? Test tanpa hardware, repeat-able, safe
2. Komponen setup Gazebo untuk robot mobile:
   a. URDF/Xacro dengan elemen Gazebo (<gazebo> tags)
   b. Plugin Gazebo untuk kontrol dan sensor
   c. World file (.world)
   d. Launch file

3. Elemen <gazebo> penting dalam URDF:
   - <material>: warna/texture di Gazebo
   - <mu1>, <mu2>: friction coefficient
   - <plugin>: load plugin sensor/controller

4. Plugin DiffDrive lengkap dalam URDF:
   <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
     <leftJoint>left_wheel_joint</leftJoint>
     <rightJoint>right_wheel_joint</rightJoint>
     <wheelSeparation>0.20</wheelSeparation>
     <wheelRadius>0.05</wheelRadius>
     <commandTopic>/cmd_vel</commandTopic>
     <odometryTopic>/odom</odometryTopic>
   </plugin>

5. Launch file untuk spawn robot di Gazebo:
   - Muat world + Gazebo
   - Load robot_description (URDF)
   - Spawn model
   - Load controllers

6. Cara mengontrol robot di Gazebo: teleop_twist_keyboard

Tampilkan screenshot Gazebo dengan robot dan terminal launch.
```

---

### Slide 34 – Plugin Sensor Gazebo

```
Buatkan slide "Plugin Sensor di Gazebo untuk Robot Mobile" yang menjelaskan:

1. Sensor LiDAR (Laser Scanner):
   Plugin: libgazebo_ros_laser.so atau libgazebo_ros_ray_sensor.so
   Output: sensor_msgs/LaserScan pada topik /scan

2. Sensor Kamera:
   Plugin: libgazebo_ros_camera.so
   Output: sensor_msgs/Image pada /camera/image_raw

3. Sensor IMU:
   Plugin: libgazebo_ros_imu_sensor.so
   Output: sensor_msgs/Imu pada /imu/data

4. Sensor Encoder (melalui joint_state_publisher):
   Plugin: libgazebo_ros_joint_state_publisher.so
   Output: sensor_msgs/JointState pada /joint_states

5. Cara menambahkan LIDAR ke URDF/Xacro:
   <sensor type="ray" name="lidar">
     <ray><scan>...</scan></ray>
     <plugin filename="libgazebo_ros_laser.so">
       <topicName>/scan</topicName>
       <frameName>laser_frame</frameName>
     </plugin>
   </sensor>

6. Visualisasi sensor di RViz:
   - LaserScan display
   - Camera display
   - IMU display

7. Ground truth vs sensor data: perbandingan di Gazebo

Tampilkan screenshot Gazebo dengan sensor active dan RViz visualization.
```

---

### Slide 35 – Simulasi Kontroler di Gazebo

```
Buatkan slide "Simulasi dan Validasi Kontroler di Gazebo" mencakup:

1. Alur lengkap simulasi kontroler:
   Gazebo (physics) → Plugin DiffDrive → /odom + /joint_states
   /cmd_vel → Plugin DiffDrive → Simulasi gerak roda

2. Cara simulasi kontroler PID di Gazebo:
   - Gunakan ros_control + diff_drive_controller
   - Atau buat custom controller node
   - Monitor dengan rqt_plot

3. Skenario pengujian kontroler:
   a. Step response: kirim /cmd_vel konstan, ukur respons
   b. Go-to-goal: berikan koordinat target
   c. Trajectory tracking: ikuti path yang telah direncanakan
   d. Disturbance rejection: tambahkan gangguan eksternal

4. Cara mencatat data simulasi:
   rosbag record -a  ← record semua topik
   rosbag play bagfile.bag  ← replay data
   rosbag info bagfile.bag  ← informasi file

5. Cara export data ke CSV untuk analisis:
   rostopic echo -b bagfile.bag -p /odom > odom_data.csv

6. Perbandingan hasil simulasi vs model teoritik
7. Cara debugging kontroler: rqt_console, /rosout

Tampilkan diagram alur simulasi dan contoh grafik analisis data.
```

---

### Slide 36 – Integrasi RViz dan Gazebo

```
Buatkan slide "Integrasi Visualisasi RViz dengan Simulasi Gazebo" yang menjelaskan:

1. Peran masing-masing tool:
   - Gazebo: simulasi fisika, lingkungan robot
   - RViz: visualisasi data ROS (sensor, path, TF, URDF)
   Keduanya berjalan bersamaan dan berbagi data melalui ROS topics

2. Setup RViz untuk monitoring robot Gazebo:
   - Add RobotModel (dari /robot_description + /tf)
   - Add TF (tree lengkap)
   - Add LaserScan (dari /scan)
   - Add Odometry (dari /odom)
   - Add Path (dari planner)
   - Fixed Frame: odom atau map

3. Cara launch keduanya sekaligus:
   <include file="$(find gazebo_ros)/launch/empty_world.launch"/>
   <node name="rviz" pkg="rviz" type="rviz" args="-d $(find pkg)/rviz/config.rviz"/>

4. Cara save dan load konfigurasi RViz (.rviz file)
5. Plugin RViz kustom untuk visualisasi tambahan
6. Screenshot side-by-side Gazebo dan RViz untuk demonstrasi

Tampilkan screenshot side-by-side Gazebo + RViz dengan penjelasan setiap panel.
```

---

## BAGIAN 9: HARDWARE DAN SETUP (Slide 37–40)

---

### Slide 37 – Rekomendasi Hardware Mini PC

```
Buatkan slide panduan "Rekomendasi Hardware Mini PC untuk ROS Robot" yang mencakup:

1. Kriteria pemilihan Mini PC untuk ROS:
   - CPU multi-core (minimal 4 core, 8 lebih baik)
   - RAM minimal 8GB (16GB disarankan)
   - Storage SSD (bukan HDD)
   - Port USB 3.0 (untuk LiDAR, kamera depth)
   - WiFi untuk komunikasi wireless
   - Daya rendah (robot mobile butuh efisiensi baterai)

2. Tabel perbandingan 6 opsi Mini PC:
   | Mini PC | CPU | RAM | Harga | Keunggulan |
   | Intel NUC 12 Pro | Core i7-1260P | 64GB max | ~$500 | Performa tertinggi |
   | Beelink SER5 Pro | Ryzen 7 5800H | 32GB max | ~$300 | Harga terbaik |
   | MinisForum UM773 | Ryzen 7 7735HS | 32GB max | ~$350 | Baru, performa tinggi |
   | NVIDIA Jetson Nano | ARM A57 | 4GB | ~$150 | CUDA, ideal robot |
   | Jetson Orin Nano | ARM 6-core | 8GB | ~$250 | AI accelerator |
   | Raspberry Pi 5 | Cortex-A76 | 8GB | ~$80 | Hemat, komunitas besar |

3. Rekomendasi untuk lab/kelas: Beelink SER5 Pro (keseimbangan harga-performa)
4. Rekomendasi untuk riset AI/vision: Jetson Orin Nano
5. Tips memilih: pertimbangkan TDP, USB port, RAM expandability

Buat tabel perbandingan visual dengan rating bintang untuk setiap kriteria.
```

---

### Slide 38 – Diagram Koneksi Hardware

```
Buatkan slide diagram "Skema Koneksi Hardware Lengkap Robot ROS" yang menampilkan:

1. Diagram koneksi hierarkis:
   Mini PC (ROS Master)
   ├── USB: RPLidar A1 (via USB-Serial)
   ├── USB: Intel RealSense D435 (USB 3.0)
   ├── USB: ESP32/Arduino (via USB-Serial rosserial)
   │     ├── I2C: MPU-6050 IMU
   │     ├── PWM: L298N Motor Driver → Motor DC kiri
   │     ├── PWM: L298N Motor Driver → Motor DC kanan
   │     └── ADC: Encoder kiri + Encoder kanan
   ├── Ethernet/WiFi: Router/Switch untuk remote control
   └── HDMI/USB: Monitor + Keyboard (setup awal)

2. Tabel perangkat + interface + ROS package:
   | Perangkat | Interface | Package | Topik Output |
   | RPLidar A1 | USB-Serial | rplidar_ros | /scan |
   | RealSense D435 | USB 3.0 | realsense2_camera | /camera/depth |
   | MPU-6050 | I2C via ESP32 | rosserial | /imu/data |
   | L298N Motor | PWM via ESP32 | rosserial | via /motor_cmd |
   | Encoder | GPIO via ESP32 | rosserial | /joint_states |

3. Pentingnya USB hub aktif untuk banyak device
4. Pertimbangan daya: baterai LiPo + regulator 5V/3.3V
5. Cara setup WiFi untuk ROS multi-machine (ROS_MASTER_URI)

Tampilkan diagram visual yang jelas dan berwarna untuk setiap koneksi.
```

---

### Slide 39 – Setup ROS di Mini PC

```
Buatkan slide panduan "Setup ROS Noetic di Mini PC (Ubuntu 20.04)" yang mencakup:

1. Instalasi ROS Noetic (langkah ringkas):
   sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list'
   sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
   sudo apt update
   sudo apt install ros-noetic-desktop-full
   source /opt/ros/noetic/setup.bash
   echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc

2. Package tambahan yang diperlukan untuk Modul 09:
   sudo apt install ros-noetic-diff-drive-controller
   sudo apt install ros-noetic-ros-control ros-noetic-ros-controllers
   sudo apt install ros-noetic-gazebo-ros-pkgs
   sudo apt install ros-noetic-robot-state-publisher
   sudo apt install ros-noetic-joint-state-publisher-gui
   sudo apt install ros-noetic-teleop-twist-keyboard
   sudo apt install ros-noetic-rplidar-ros

3. Setup catkin workspace:
   mkdir -p ~/catkin_ws/src && cd ~/catkin_ws
   catkin_make && source devel/setup.bash

4. Konfigurasi multi-machine ROS:
   export ROS_MASTER_URI=http://MINI_PC_IP:11311
   export ROS_IP=THIS_MACHINE_IP

5. Checklist verifikasi setup: roscore, rosrun, rostopic

Tampilkan terminal dengan output perintah setup yang berhasil.
```

---

### Slide 40 – rosserial: Bridge ROS ke Arduino/ESP32

```
Buatkan slide teknis "Menggunakan rosserial untuk Bridge ROS-Arduino/ESP32" yang menjelaskan:

1. Apa itu rosserial?
   - Library yang memungkinkan Arduino/ESP32 menjadi ROS node
   - Komunikasi via USB Serial (atau WiFi dengan rosserial_server)
   - Mendukung: std_msgs, sensor_msgs, geometry_msgs, custom msgs

2. Instalasi rosserial:
   sudo apt install ros-noetic-rosserial-arduino
   cd ~/Arduino/libraries
   rosrun rosserial_arduino make_libraries.py .

3. Kode Arduino/ESP32 untuk kontrol motor + encoder:
   #include <ros.h>
   #include <geometry_msgs/Twist.h>
   #include <sensor_msgs/JointState.h>
   
   ros::NodeHandle nh;
   
   void cmdVelCallback(const geometry_msgs::Twist& msg) {
     float v = msg.linear.x;
     float w = msg.angular.z;
     // Konversi ke PWM motor...
   }
   ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel", cmdVelCallback);
   
   sensor_msgs::JointState joint_state_msg;
   ros::Publisher joint_pub("/joint_states", &joint_state_msg);

4. Cara menjalankan rosserial:
   rosrun rosserial_python serial_node.py /dev/ttyUSB0

5. Debugging: rostopic echo, rqt_serial_console

Tampilkan kode Arduino dengan syntax highlighting dan diagram koneksi.
```

---

## BAGIAN 10: PERCOBAAN PRAKTIKUM (Slide 41–43)

---

### Slide 41 – Overview 15 Percobaan Praktikum

```
Buatkan slide ringkasan "15 Percobaan Praktikum Modul 09: ROS Kinematika dan Kontroler" dalam format tabel:

| No | Nama Percobaan | Tujuan | Tools |
|----|---------------|--------|-------|
| P01 | FK Robot 2-DOF Manual | Hitung FK dengan Python | NumPy |
| P02 | FK dengan DH Parameters | Implementasi tabel DH | tf.transformations |
| P03 | IK Analitik 2-DOF | Cari sudut sendi dari target | SciPy |
| P04 | IK Numerik Jacobian | IK iteratif pseudoinverse | NumPy/SciPy |
| P05 | Jacobian Computation | Hitung dan plot Jacobian | NumPy |
| P06 | TF Broadcaster Python | Publish transformasi custom | tf library |
| P07 | URDF Robot Sederhana | Buat dan visualisasi URDF | robot_state_publisher |
| P08 | PID Kecepatan Motor | Tuning PID untuk DC motor | rqt_plot, rqt_reconfigure |
| P09 | Go-to-Goal Controller | Robot bergerak ke target | Gazebo, RViz |
| P10 | Odometri dari Encoder | Publish /odom dari encoder | rosserial, nav_msgs |
| P11 | diff_drive_controller | Setup ros_control | ros_control |
| P12 | Simulasi FK+IK Gazebo | Validasi kinematics di Gazebo | Gazebo, RViz |
| P13 | Cascade Kontroler | Kontrol posisi + kecepatan | rqt_plot |
| P14 | Kinematika Robot Omni | Implementasi 3-roda omni | NumPy, Gazebo |
| P15 | Integrasi Sistem Lengkap | Gabungkan semua komponen | Full ROS stack |

Gunakan warna berbeda untuk kategori: Kinematika (biru), Kontroler (hijau), Hardware (oranye).
```

---

### Slide 42 – Alur Kerja Percobaan Praktikum

```
Buatkan slide "Alur Kerja Standar Setiap Percobaan Praktikum" yang menjelaskan:

1. Template alur kerja 8 langkah yang digunakan setiap percobaan:
   Step 1: Baca tujuan percobaan dan koneksi teori
   Step 2: Setup workspace dan cek dependencies
   Step 3: Buat/download kode awal (template)
   Step 4: Implementasi kode sesuai instruksi
   Step 5: Jalankan kode dan observasi output
   Step 6: Variasikan parameter dan catat hasil
   Step 7: Analisis hasil dengan grafik/data
   Step 8: Isi tabel observasi di jobsheet

2. Checklist pre-percobaan:
   ☐ ROS workspace ter-source (source devel/setup.bash)
   ☐ roscore berjalan
   ☐ Hardware terhubung (jika diperlukan)
   ☐ Gazebo terbuka (untuk percobaan simulasi)

3. Common errors dan cara mengatasinya:
   - "Package not found" → catkin_make + source
   - "Topic not published" → cek rosnode list, rostopic list
   - "Transform lookup failed" → cek TF tree

4. Format pelaporan: screenshot terminal, grafik, tabel data
5. Panduan debugging: rqt_console, rosnode info, rostopic hz

Buat checklist visual yang menarik dan mudah diikuti.
```

---

### Slide 43 – Percobaan P08 dan P09 (Detail)

```
Buatkan slide detail dua percobaan kunci: "P08 PID Kecepatan Motor dan P09 Go-to-Goal Controller":

PERCOBAAN P08 – PID Kecepatan Motor:
1. Tujuan: mahasiswa mampu tuning PID untuk kontrol kecepatan motor DC
2. Setup: Mini PC → rosserial → Arduino/ESP32 → L298N → Motor DC + Encoder
3. Parameter yang divariasikan: Kp (0.5 – 3.0), Ki (0 – 1.0), Kd (0 – 0.1)
4. Metrik pengukuran: rise time, overshoot %, settling time, steady-state error
5. Tugas: plot respons step untuk 5 kombinasi gain berbeda

PERCOBAAN P09 – Go-to-Goal Controller:
1. Tujuan: robot mobile bergerak menuju koordinat tujuan yang diberikan
2. Setup: Gazebo + diff_drive_controller + go_to_goal_node
3. Parameter: Kρ (gain jarak), Kα (gain sudut), threshold berhenti
4. Skenario: 3 target berbeda (jarak pendek, jauh, dan dengan putaran besar)
5. Tugas: plot trajectory aktual vs ideal, ukur error posisi akhir
6. Observasi: apa yang terjadi jika Kρ > Kα? (jelaskan matematika)

Untuk masing-masing: tampilkan diagram setup, pseudocode ringkas, dan form observasi.
```

---

## BAGIAN 11: PROJECT DAN EVALUASI (Slide 44–45)

---

### Slide 44 – Project: Sistem Kontrol Robot Terintegrasi

```
Buatkan slide "Project Akhir Modul 09: Sistem Kontrol Robot Terintegrasi" yang menampilkan:

1. Deskripsi umum 10 opsi project (ringkasan):
   a. Autonomous Warehouse Robot: navigasi warehouse dengan FK/IK + PID
   b. Robot Arm Pick-and-Place: kontrol lengan dengan IK MoveIt!
   c. Convoy Robot System: 3 robot mengikuti robot leader
   d. Surgical Assistant Simulation: kontrol presisi tinggi dengan cascade controller
   e. Autonomous Delivery Robot: integrasi odometri + go-to-goal + obstacle avoidance
   f. Drone Kinematic Simulator: model kinematika quadcopter di ROS
   g. Omni-directional AGV: robot omni dengan kontroler holonomic
   h. Robot Inspection System: robot patroli dengan LiDAR + PID
   i. Multi-joint Arm Teleop: control lengan robot 3-DOF real-time
   j. Self-Calibrating Odometry: sistem koreksi otomatis parameter odometri

2. Kriteria project:
   - Minimal 3 komponen teori diimplementasikan (FK/IK + kontroler + odometri)
   - Berjalan di simulasi Gazebo (wajib) + hardware (nilai plus)
   - Dokumentasi kode dan laporan akhir

3. Timeline project (4 minggu):
   Minggu 1: Desain sistem dan review literatur
   Minggu 2: Implementasi komponen dasar
   Minggu 3: Integrasi dan pengujian
   Minggu 4: Finishing, demo, dan presentasi

Tampilkan roadmap project dengan milestone yang jelas.
```

---

### Slide 45 – Evaluasi, Rubrik, dan Penutup

```
Buatkan slide penutup "Evaluasi, Rubrik Penilaian, dan Kesimpulan Modul 09" dengan:

1. Komponen Penilaian Modul 09:
   | Komponen | Bobot | Deskripsi |
   | Laporan Percobaan (P01-P15) | 30% | Jobsheet lengkap + analisa |
   | Tugas Video | 25% | Screen record penjelasan + demo |
   | Project Akhir | 35% | Sistem terintegrasi + presentasi |
   | Keaktifan Praktikum | 10% | Partisipasi dan kehadiran |

2. Rubrik Penilaian Teknis (per percobaan):
   | Kriteria | Bobot | Indikator |
   | Ketepatan implementasi | 40% | Kode berjalan benar sesuai tujuan |
   | Analisa hasil | 30% | Penjelasan grafik/data bermakna |
   | Variasi parameter | 20% | Eksplorasi dampak perubahan gain/parameter |
   | Format laporan | 10% | Rapi, lengkap, sesuai template |

3. Kesimpulan kunci Modul 09:
   ✓ FK menghitung pose end-effector dari sudut sendi (matriks transformasi homogen)
   ✓ IK adalah invers FK: analitik (cepat) atau numerik (umum)
   ✓ PID adalah fondasi kontroler robotika: P mengejar target, I menghilangkan offset, D meredam osilasi
   ✓ ROS menyediakan ekosistem lengkap: TF, ros_control, Gazebo, RViz
   ✓ Odometri robot diferensial: integrasi kecepatan roda untuk estimasi pose

4. Referensi utama (5 buku dan 5 paper terpenting)
5. QR code menuju repository GitHub modul dan referensi digital

Buat slide penutup yang profesional dan inspiratif.
```
