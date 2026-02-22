# MATERI MODUL 09: ROS KINEMATIKA DAN KONTROLER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 09 – ROS Kinematika dan Kontroler  
**Platform:** ROS Noetic / ROS 2 Humble, Ubuntu 20.04/22.04  
**Estimasi Waktu Belajar:** 10–14 Jam

---

## DAFTAR ISI

1. [Pendahuluan – Kinematika Robot](#1-pendahuluan--kinematika-robot)
2. [Forward Kinematics](#2-forward-kinematics)
3. [Inverse Kinematics](#3-inverse-kinematics)
4. [Denavit-Hartenberg (DH) Parameters](#4-denavit-hartenberg-dh-parameters)
5. [Jacobian dan Kecepatan Kinematika](#5-jacobian-dan-kecepatan-kinematika)
6. [Kinematika Robot Mobile (Diferensial & Omni)](#6-kinematika-robot-mobile-diferensial--omni)
7. [Sistem Koordinat dan TF di ROS](#7-sistem-koordinat-dan-tf-di-ros)
8. [PID Controller](#8-pid-controller)
9. [Kontroler Posisi dan Kecepatan](#9-kontroler-posisi-dan-kecepatan)
10. [Kontroler pada Robot Mobile di ROS](#10-kontroler-pada-robot-mobile-di-ros)
11. [ros_control dan Controller Manager](#11-ros_control-dan-controller-manager)
12. [Odometri dan State Estimation](#12-odometri-dan-state-estimation)
13. [Implementasi di Simulasi Gazebo](#13-implementasi-di-simulasi-gazebo)
14. [Rekomendasi Hardware Mini PC](#14-rekomendasi-hardware-mini-pc)
15. [Referensi](#15-referensi)

---

## 1. PENDAHULUAN – KINEMATIKA ROBOT

### 1.1 Definisi Kinematika

**Kinematika** adalah cabang mekanika yang mempelajari gerak benda tanpa mempertimbangkan gaya yang menyebabkan gerak tersebut. Dalam robotika, kinematika membahas hubungan antara parameter sendi (joint) robot dengan posisi dan orientasi end-effector (ujung robot) atau chassis robot.

Terdapat dua jenis utama:

| Jenis | Definisi | Arah Perhitungan |
|-------|----------|-----------------|
| **Forward Kinematics (FK)** | Menghitung posisi/orientasi end-effector dari nilai joint | Joint space → Cartesian space |
| **Inverse Kinematics (IK)** | Menghitung nilai joint dari posisi/orientasi end-effector yang diinginkan | Cartesian space → Joint space |

### 1.2 Ruang Kerja Robot

- **Joint Space (Configuration Space / C-Space):** Ruang yang didefinisikan oleh semua nilai sendi robot (θ₁, θ₂, ..., θₙ)
- **Cartesian Space (Task Space / Operational Space):** Ruang 3D tempat end-effector bergerak (x, y, z, roll, pitch, yaw)
- **Workspace:** Volume ruang yang dapat dijangkau oleh end-effector robot

### 1.3 Representasi Posisi dan Orientasi

Posisi end-effector direpresentasikan sebagai vektor posisi **p** = [x, y, z]ᵀ.

Orientasi direpresentasikan menggunakan:
1. **Rotation Matrix R** (3×3)
2. **Euler Angles** (Roll-Pitch-Yaw)
3. **Quaternion** (q₀, q₁, q₂, q₃) — digunakan oleh ROS
4. **Axis-Angle** representation

**Transformasi Homogen** menggabungkan rotasi dan translasi:

```
T = | R  p |  =  | r11 r12 r13 px |
    | 0  1 |     | r21 r22 r23 py |
                 | r31 r32 r33 pz |
                 |  0   0   0   1 |
```

---

## 2. FORWARD KINEMATICS

### 2.1 Konsep Dasar

Forward Kinematics (FK) menghitung **pose** (posisi + orientasi) end-effector berdasarkan nilai semua sendi robot. Untuk robot dengan n sendi:

```
T₀ₙ = T₀₁ · T₁₂ · T₂₃ · ... · T(n-1)n
```

di mana T₀ₙ adalah matriks transformasi homogen dari frame dasar ke frame end-effector.

### 2.2 Contoh: Robot 2-DOF Planar

Robot dengan dua lengan:
- Lengan 1: panjang L₁, sudut θ₁
- Lengan 2: panjang L₂, sudut θ₂

```
x = L₁·cos(θ₁) + L₂·cos(θ₁+θ₂)
y = L₁·sin(θ₁) + L₂·sin(θ₁+θ₂)
```

### 2.3 Pseudo Code Forward Kinematics 2-DOF

```
FUNGSI forwardKinematics2DOF(theta1, theta2, L1, L2):
    // Hitung posisi x end-effector
    x = L1 * cos(theta1) + L2 * cos(theta1 + theta2)
    
    // Hitung posisi y end-effector
    y = L1 * sin(theta1) + L2 * sin(theta1 + theta2)
    
    // Hitung orientasi end-effector (total sudut)
    phi = theta1 + theta2
    
    KEMBALIKAN (x, y, phi)

// Contoh pemakaian:
theta1 = 30°  // konversi ke radian: 0.5236 rad
theta2 = 45°  // konversi ke radian: 0.7854 rad
L1 = 0.5      // meter
L2 = 0.3      // meter
(x, y, phi) = forwardKinematics2DOF(theta1, theta2, L1, L2)
// Hasil: x ≈ 0.539 m, y ≈ 0.462 m, phi = 75°
```

**Penjelasan:**
- Fungsi menerima sudut sendi (theta1, theta2) dalam radian dan panjang lengan (L1, L2)
- Posisi x dihitung dengan jumlah proyeksi horizontal tiap lengan pada sumbu x
- Posisi y dihitung dengan jumlah proyeksi vertikal tiap lengan pada sumbu y
- Orientasi phi adalah total sudut rotasi relatif terhadap frame dasar
- Hasil adalah koordinat Cartesian end-effector

### 2.4 Pseudo Code FK dengan Matriks Transformasi Homogen

```
FUNGSI buildTransformMatrix(theta, d, a, alpha):
    // Matriks DH standar
    T = [ [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta)],
          [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
          [0,           sin(alpha),             cos(alpha),            d           ],
          [0,           0,                      0,                     1           ] ]
    KEMBALIKAN T

FUNGSI forwardKinematicsNDOF(joints[], dhParams[]):
    // joints = [θ1, θ2, ..., θn]
    // dhParams = [(d1,a1,α1), (d2,a2,α2), ..., (dn,an,αn)]
    
    T_total = matriks identitas 4x4
    
    UNTUK i = 0 SAMPAI n-1:
        theta_i = joints[i]
        d_i     = dhParams[i].d
        a_i     = dhParams[i].a
        alpha_i = dhParams[i].alpha
        
        T_i = buildTransformMatrix(theta_i, d_i, a_i, alpha_i)
        T_total = T_total × T_i   // perkalian matriks
    
    // Ekstrak posisi dan orientasi dari T_total
    posisi    = T_total[0:3, 3]   // kolom translasi
    orientasi = T_total[0:3, 0:3] // sub-matriks rotasi
    
    KEMBALIKAN (posisi, orientasi, T_total)
```

**Penjelasan:**
- `buildTransformMatrix` membangun matriks transformasi homogen 4×4 menggunakan konvensi DH
- Parameter DH (d, a, α) adalah tetap untuk setiap sendi; θ adalah variabel
- `forwardKinematicsNDOF` mengalikan berurutan semua matriks transformasi dari frame 0 ke frame n
- Hasilnya berupa matriks T_total yang mengandung posisi (kolom ke-4) dan orientasi (sub-matriks 3×3)

---

## 3. INVERSE KINEMATICS

### 3.1 Konsep Dasar

Inverse Kinematics (IK) adalah kebalikan dari FK: diberikan posisi dan orientasi end-effector yang diinginkan, tentukan nilai sendi yang diperlukan.

**Tantangan IK:**
- **Multiple solutions:** Bisa ada banyak konfigurasi sendi yang menghasilkan pose yang sama
- **No solution:** Pose yang diminta di luar workspace
- **Singularities:** Konfigurasi di mana robot kehilangan derajat kebebasan
- **Non-linearity:** Persamaan trigonometri yang kompleks

### 3.2 Metode Analitik IK (Robot 2-DOF)

Diberikan target (x, y), cari (θ₁, θ₂):

```
cos(θ₂) = (x² + y² - L₁² - L₂²) / (2·L₁·L₂)
sin(θ₂) = ±√(1 - cos²(θ₂))
θ₂ = atan2(sin(θ₂), cos(θ₂))
θ₁ = atan2(y, x) - atan2(L₂·sin(θ₂), L₁ + L₂·cos(θ₂))
```

### 3.3 Pseudo Code IK Analitik 2-DOF

```
FUNGSI inverseKinematics2DOF(x_target, y_target, L1, L2):
    // Hitung cos(theta2) menggunakan hukum cosinus
    cos_theta2 = (x_target² + y_target² - L1² - L2²) / (2 * L1 * L2)
    
    // Validasi: pastikan nilai dalam rentang [-1, 1]
    JIKA cos_theta2 < -1 ATAU cos_theta2 > 1:
        ERROR "Target di luar workspace"
        KEMBALIKAN NULL
    
    // Dua solusi: siku ke atas dan siku ke bawah
    sin_theta2_pos = sqrt(1 - cos_theta2²)   // elbow up
    sin_theta2_neg = -sqrt(1 - cos_theta2²)  // elbow down
    
    theta2_elbow_up   = atan2(sin_theta2_pos, cos_theta2)
    theta2_elbow_down = atan2(sin_theta2_neg, cos_theta2)
    
    // Hitung theta1 untuk setiap solusi
    k1 = L1 + L2 * cos_theta2
    k2_up   = L2 * sin_theta2_pos
    k2_down = L2 * sin_theta2_neg
    
    theta1_elbow_up   = atan2(y_target, x_target) - atan2(k2_up,   k1)
    theta1_elbow_down = atan2(y_target, x_target) - atan2(k2_down, k1)
    
    solusi_1 = (theta1_elbow_up,   theta2_elbow_up)
    solusi_2 = (theta1_elbow_down, theta2_elbow_down)
    
    KEMBALIKAN [solusi_1, solusi_2]

// Contoh:
solusi = inverseKinematics2DOF(0.5, 0.4, 0.5, 0.3)
// Solusi 1 (elbow up):  theta1 ≈ 25.1°, theta2 ≈ 52.3°
// Solusi 2 (elbow down): theta1 ≈ 77.4°, theta2 ≈ -52.3°
```

**Penjelasan:**
- Algoritma menggunakan hukum cosinus untuk mendapatkan θ₂ dari jarak Euclidean target
- Tanda sin(θ₂) menentukan dua konfigurasi: elbow-up dan elbow-down
- θ₁ dihitung menggunakan fungsi atan2 yang mempertimbangkan kuadran
- Validasi range memastikan target berada dalam workspace robot

### 3.4 Pseudo Code IK Numerik (Jacobian Pseudoinverse)

```
FUNGSI ikNumerical(target_pose, joints_initial, max_iter=1000, tol=1e-4):
    joints = joints_initial
    
    UNTUK iter = 1 SAMPAI max_iter:
        // Hitung FK dari posisi sendi saat ini
        current_pose = forwardKinematics(joints)
        
        // Hitung error posisi
        error = target_pose - current_pose
        
        // Cek konvergensi
        JIKA norm(error) < tol:
            KEMBALIKAN joints
        
        // Hitung Jacobian pada konfigurasi saat ini
        J = computeJacobian(joints)
        
        // Hitung pseudoinverse Jacobian: J⁺ = Jᵀ(JJᵀ)⁻¹
        J_pseudo = transpose(J) × inverse(J × transpose(J) + λI)
        
        // Update joints menggunakan Damped Least Squares
        delta_joints = J_pseudo × error
        joints = joints + alpha × delta_joints   // alpha = learning rate
        
        // Clamp joints ke batas sendi yang diizinkan
        UNTUK i = 0 SAMPAI n-1:
            joints[i] = clamp(joints[i], joint_min[i], joint_max[i])
    
    WARNING "IK tidak konvergen setelah max_iter iterasi"
    KEMBALIKAN joints  // solusi terbaik yang ditemukan
```

**Penjelasan:**
- Metode numerik menggunakan iterasi untuk meminimasi error antara pose saat ini dan target
- Jacobian pseudoinverse (J⁺) mengubah error pose menjadi perubahan sudut sendi
- Parameter λ (damping factor) meningkatkan stabilitas numerik mendekati singularitas
- Learning rate α mengontrol kecepatan konvergensi
- Cocok untuk robot multi-DOF yang sulit diselesaikan secara analitik

---

## 4. DENAVIT-HARTENBERG (DH) PARAMETERS

### 4.1 Konvensi DH

Metode **Denavit-Hartenberg (DH)** adalah cara sistematis untuk mendefinisikan frame koordinat pada setiap sendi robot, memungkinkan representasi FK yang terstandarisasi.

Setiap hubungan antar sendi (link) didefinisikan oleh 4 parameter:

| Parameter | Simbol | Definisi |
|-----------|--------|---------|
| Link length | a | Jarak antara dua sumbu Z yang berdekatan (sepanjang sumbu X) |
| Link twist | α (alpha) | Sudut antara dua sumbu Z yang berdekatan (sekitar sumbu X) |
| Link offset | d | Jarak sepanjang sumbu Z dari frame sebelumnya |
| Joint angle | θ (theta) | Sudut rotasi sekitar sumbu Z (variabel untuk sendi revolute) |

### 4.2 Matriks Transformasi DH

```
T(i-1 → i) = Rot_z(θᵢ) · Trans_z(dᵢ) · Trans_x(aᵢ) · Rot_x(αᵢ)

           = | cos(θ)  -sin(θ)cos(α)   sin(θ)sin(α)  a·cos(θ) |
             | sin(θ)   cos(θ)cos(α)  -cos(θ)sin(α)  a·sin(θ) |
             |   0         sin(α)          cos(α)         d    |
             |   0            0               0            1   |
```

### 4.3 Contoh Tabel DH untuk Robot 3-DOF

```
| Sendi | θ    | d    | a    | α     |
|-------|------|------|------|-------|
|   1   | θ₁   | d₁   | 0    | 90°   |
|   2   | θ₂   | 0    | L₂   | 0°    |
|   3   | θ₃   | 0    | L₃   | 0°    |
```

### 4.4 Pseudo Code Tabel DH dan FK

```
// Definisi tabel DH untuk robot 3-DOF (contoh)
STRUKTUR DHParameter:
    theta_offset  // offset sudut tetap
    d             // offset link (meter)
    a             // panjang link (meter)
    alpha         // twist link (radian)

dh_table = [
    DHParameter(theta_offset=0,    d=0.1,  a=0,    alpha=PI/2),
    DHParameter(theta_offset=0,    d=0,    a=0.25, alpha=0),
    DHParameter(theta_offset=0,    d=0,    a=0.20, alpha=0)
]

FUNGSI computeFK_DH(joint_angles[], dh_table[]):
    n = panjang(joint_angles)
    T_total = matriks identitas 4x4
    
    UNTUK i = 0 SAMPAI n-1:
        theta = joint_angles[i] + dh_table[i].theta_offset
        d     = dh_table[i].d
        a     = dh_table[i].a
        alpha = dh_table[i].alpha
        
        // Bangunan matriks DH
        T_i = [
            [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta)],
            [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
            [0,           sin(alpha),             cos(alpha),            d           ],
            [0,           0,                      0,                     1           ]
        ]
        
        T_total = T_total × T_i
    
    KEMBALIKAN T_total

// Pemakaian:
joint_angles = [PI/4, PI/6, PI/3]  // sudut dalam radian
T = computeFK_DH(joint_angles, dh_table)
print("Posisi end-effector:", T[0][3], T[1][3], T[2][3])
```

**Penjelasan:**
- Tabel DH menyimpan parameter geometri tetap robot untuk setiap link
- `theta_offset` memungkinkan penyesuaian antara definisi sendi fisik dan konvensi DH
- Loop mengalikan matriks transformasi berurutan untuk mendapatkan pose kumulatif
- Hasil berupa matriks 4×4 yang berisi posisi (kolom ke-4) dan orientasi (3×3 blok kiri atas)

---

## 5. JACOBIAN DAN KECEPATAN KINEMATIKA

### 5.1 Matriks Jacobian

**Jacobian** adalah matriks turunan parsial yang menghubungkan kecepatan sendi (joint velocity) dengan kecepatan Cartesian end-effector:

```
ẋ = J(q) · q̇
```

di mana:
- **ẋ** = vektor kecepatan Cartesian [vx, vy, vz, ωx, ωy, ωz]ᵀ (6×1)
- **J(q)** = matriks Jacobian (6×n)
- **q̇** = vektor kecepatan sendi (n×1)

### 5.2 Komponen Jacobian

Jacobian terdiri dari dua bagian:
- **Jacobian Linear (Jᵥ):** 3×n, hubungan kecepatan translasi
- **Jacobian Angular (Jω):** 3×n, hubungan kecepatan rotasi

Untuk sendi revolute ke-i:
```
Jᵥᵢ = zᵢ₋₁ × (pₙ - pᵢ₋₁)
Jωᵢ = zᵢ₋₁
```

### 5.3 Pseudo Code Komputasi Jacobian

```
FUNGSI computeJacobian(joint_angles[], dh_table[]):
    n = panjang(joint_angles)
    J = matriks nol 6×n
    
    // Hitung semua transformasi parsial
    T = [matriks identitas 4x4]  // T[0] = T dari frame 0 ke frame 0
    
    UNTUK i = 1 SAMPAI n:
        T_i = buildTransformMatrix(joint_angles[i-1], dh_table[i-1])
        T.append(T[-1] × T_i)   // T[i] = T dari frame 0 ke frame i
    
    // Posisi dan axis z end-effector
    p_n = T[n][0:3, 3]   // posisi end-effector
    
    UNTUK i = 0 SAMPAI n-1:
        // Axis z dari frame i
        z_i = T[i][0:3, 2]   // kolom ke-3 (indeks 2) dari T[i]
        
        // Posisi origin frame i
        p_i = T[i][0:3, 3]
        
        // Kolom Jacobian untuk sendi revolute
        J_linear_i  = crossProduct(z_i, p_n - p_i)
        J_angular_i = z_i
        
        J[0:3, i] = J_linear_i
        J[3:6, i] = J_angular_i
    
    KEMBALIKAN J

// Konversi kecepatan sendi ke kecepatan Cartesian:
FUNGSI jointVelToCartesianVel(joint_vel[], joint_angles[], dh_table[]):
    J = computeJacobian(joint_angles, dh_table)
    cartesian_vel = J × joint_vel
    KEMBALIKAN cartesian_vel
```

**Penjelasan:**
- Posisi dan orientasi semua frame dihitung terlebih dahulu dengan akumulasi matriks transformasi
- Untuk setiap sendi revolute, kontribusi ke Jacobian linear adalah cross product sumbu z dengan vektor dari sendi ke end-effector
- Kontribusi ke Jacobian angular adalah sumbu z sendi itu sendiri
- Hasilnya digunakan untuk velocity control dan force/torque control

---

## 6. KINEMATIKA ROBOT MOBILE (DIFERENSIAL & OMNI)

### 6.1 Kinematika Robot Diferensial Drive

Robot diferensial (dua roda aktif) adalah platform mobile paling umum. Geraknya dikontrol dengan mengatur kecepatan roda kiri (vL) dan kanan (vR).

**Parameter:**
- R = radius roda
- L = jarak antar roda (wheelbase)
- ω = kecepatan sudut roda (rad/s)

**Model Kinematika:**
```
v  = R/2 · (ωR + ωL)          // kecepatan linear
ω  = R/L · (ωR - ωL)          // kecepatan angular
ẋ  = v · cos(θ)
ẏ  = v · sin(θ)
θ̇  = ω
```

### 6.2 Pseudo Code Kinematika Diferensial

```
STRUKTUR DiffDriveRobot:
    wheel_radius    // R (meter)
    wheelbase       // L (meter)
    x, y, theta     // pose saat ini
    dt              // time step (detik)

FUNGSI updateOdometry(robot, omega_left, omega_right):
    R = robot.wheel_radius
    L = robot.wheelbase
    
    // Hitung kecepatan linear dan angular
    v = R / 2.0 * (omega_right + omega_left)
    w = R / robot.L * (omega_right - omega_left)
    
    // Perbarui pose robot menggunakan integrasi Euler
    robot.x     += v * cos(robot.theta) * robot.dt
    robot.y     += v * sin(robot.theta) * robot.dt
    robot.theta += w * robot.dt
    
    // Normalisasi sudut ke [-π, π]
    robot.theta = atan2(sin(robot.theta), cos(robot.theta))
    
    KEMBALIKAN (robot.x, robot.y, robot.theta)

FUNGSI velocityToWheelSpeeds(robot, v_linear, v_angular):
    R = robot.wheel_radius
    L = robot.wheelbase
    
    // Invers kinematika roda
    omega_right = (v_linear + v_angular * L / 2.0) / R
    omega_left  = (v_linear - v_angular * L / 2.0) / R
    
    KEMBALIKAN (omega_left, omega_right)
```

**Penjelasan:**
- `updateOdometry` mengintegrasikan kecepatan roda untuk memperkirakan pose robot (odometri)
- Integrasi Euler sederhana digunakan karena dt kecil (biasanya 10-50 ms)
- Normalisasi sudut memastikan theta tetap dalam rentang yang konsisten
- `velocityToWheelSpeeds` adalah inversi: diberikan kecepatan linear dan angular, hitung kecepatan tiap roda

### 6.3 Kinematika Robot Omni-Directional (3 Roda)

Robot omni dengan 3 roda berjarak 120° dapat bergerak ke segala arah tanpa rotasi badan.

```
| ω₁ |   | -sin(β₁)   cos(β₁)  L | | vx |
| ω₂ | = | -sin(β₂)   cos(β₂)  L | | vy |  × (1/R)
| ω₃ |   | -sin(β₃)   cos(β₃)  L | | ωz |

β₁=90°, β₂=210°, β₃=330°
```

### 6.4 Pseudo Code Omni Drive 3 Roda

```
FUNGSI omniDriveIK(vx, vy, omega_z, L=0.15, R=0.05):
    // Sudut orientasi tiap roda (dalam derajat: 90, 210, 330)
    beta = [PI/2, 7*PI/6, 11*PI/6]
    
    omega_wheels = []
    UNTUK i = 0 SAMPAI 2:
        // Kontribusi kecepatan translasi dan rotasi
        omega_i = (-sin(beta[i]) * vx + cos(beta[i]) * vy + L * omega_z) / R
        omega_wheels.append(omega_i)
    
    KEMBALIKAN omega_wheels  // [ω₁, ω₂, ω₃] dalam rad/s

// Contoh: gerak ke depan dengan vx=0.2 m/s
wheels = omniDriveIK(vx=0.2, vy=0, omega_z=0)
// Hasil: ω₁ ≈ -4.0, ω₂ ≈ 2.0, ω₃ ≈ 2.0 rad/s
```

---

## 7. SISTEM KOORDINAT DAN TF DI ROS

### 7.1 Konsep TF (Transform)

**TF** adalah library ROS yang mengelola relasi koordinat (transformasi) antar frame dalam sistem robot. TF memungkinkan konversi titik dari satu frame ke frame lain secara otomatis, dengan mempertimbangkan waktu.

**Frame standar ROS:**
- **`world`**: Frame global absolut
- **`map`**: Frame peta (hasil SLAM)
- **`odom`**: Frame odometri (drift dari waktu ke waktu)
- **`base_link`**: Frame pusat robot
- **`base_footprint`**: Proyeksi base_link ke bidang lantai
- **`sensor_frame`**: Frame sensor (kamera, LIDAR, dsb.)

### 7.2 TF Tree

```
world
  └── map
        └── odom
              └── base_link
                    ├── base_footprint
                    ├── left_wheel
                    ├── right_wheel
                    ├── laser_frame
                    └── camera_frame
```

### 7.3 Pseudo Code Publish TF di ROS Python

```
// ROS Publisher TF - Python (konseptual)

IMPOR rospy, tf, geometry_msgs

FUNGSI main():
    rospy.init_node('tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(50)  // 50 Hz
    
    SELAMA rospy.is_shutdown() = FALSE:
        // Baca pose robot dari sensor/odometri
        (x, y, theta) = getCurrentPose()
        
        // Konversi theta ke quaternion
        q = quaternionFromEuler(0, 0, theta)  // roll=0, pitch=0, yaw=theta
        
        // Broadcast transformasi odom -> base_link
        br.sendTransform(
            translation = (x, y, 0),
            rotation    = q,
            time        = rospy.Time.now(),
            child_frame = "base_link",
            parent_frame= "odom"
        )
        
        rate.sleep()

// TF Listener - baca transformasi antar frame
FUNGSI listenTF(source_frame, target_frame):
    listener = tf.TransformListener()
    
    listener.waitForTransform(target_frame, source_frame, 
                               rospy.Time(), rospy.Duration(4.0))
    
    (trans, rot) = listener.lookupTransform(target_frame, source_frame,
                                             rospy.Time(0))
    
    KEMBALIKAN (trans, rot)  // translasi dan rotasi (quaternion)
```

**Penjelasan:**
- `TransformBroadcaster` mempublish transformasi ke topik `/tf` dengan frekuensi tinggi (50 Hz+)
- `sendTransform` mendefinisikan hubungan child_frame relatif terhadap parent_frame
- `TransformListener` menerima dan menyimpan semua transformasi yang dipublish
- `lookupTransform` mengambil transformasi terkini atau pada waktu tertentu

---

## 8. PID CONTROLLER

### 8.1 Teori PID

**PID (Proportional-Integral-Derivative)** adalah kontroler umpan balik (feedback) paling banyak digunakan dalam industri dan robotika. PID meminimalkan error antara setpoint (nilai yang diinginkan) dan process variable (nilai pengukuran).

```
u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt
```

| Komponen | Simbol | Fungsi | Efek |
|----------|--------|--------|------|
| Proportional | Kp | Respons proporsional dengan error saat ini | Mempercepat respons, mengurangi rise time |
| Integral | Ki | Akumulasi error masa lalu | Menghilangkan steady-state error |
| Derivative | Kd | Prediksi perubahan error | Meredam osilasi, meningkatkan stabilitas |

### 8.2 Karakteristik Respons

| Parameter | Kp ↑ | Ki ↑ | Kd ↑ |
|-----------|------|------|------|
| Rise Time | Menurun | Menurun | Kecil | 
| Overshoot | Meningkat | Meningkat | Menurun |
| Settling Time | Kecil | Meningkat | Menurun |
| Steady Error | Menurun | Dihilangkan | Tidak berubah |
| Stability | Memburuk | Memburuk | Membaik (jika kecil) |

### 8.3 Pseudo Code PID Controller

```
STRUKTUR PIDController:
    Kp, Ki, Kd           // gain kontroler
    setpoint             // nilai yang diinginkan
    prev_error = 0       // error sebelumnya
    integral   = 0       // akumulasi integral
    output_min = -100    // batas output minimum
    output_max =  100    // batas output maksimum
    dt                   // periode sampling (detik)

FUNGSI compute(pid, process_value):
    // Hitung error
    error = pid.setpoint - process_value
    
    // Komponen Proportional
    P = pid.Kp * error
    
    // Komponen Integral (dengan anti-windup clamp)
    pid.integral += error * pid.dt
    I = pid.Ki * pid.integral
    
    // Komponen Derivative (filter noise dengan EWA)
    derivative = (error - pid.prev_error) / pid.dt
    D = pid.Kd * derivative
    
    // Total output
    output = P + I + D
    
    // Clamp output ke batas yang diizinkan
    output = clamp(output, pid.output_min, pid.output_max)
    
    // Anti-windup: hentikan integrasi jika output tersaturasi
    JIKA output = pid.output_max ATAU output = pid.output_min:
        pid.integral -= error * pid.dt  // rollback integrasi
    
    // Simpan error untuk iterasi berikutnya
    pid.prev_error = error
    
    KEMBALIKAN output

// Contoh: kontroler kecepatan motor
pid_kecepatan = PIDController(Kp=1.5, Ki=0.3, Kd=0.05, dt=0.01)
pid_kecepatan.setpoint = 100  // RPM target

LOOP setiap 10ms:
    rpm_aktual = readEncoderRPM()
    pwm = compute(pid_kecepatan, rpm_aktual)
    setMotorPWM(pwm)
```

**Penjelasan:**
- Komponen P memberikan aksi langsung proporsional dengan error saat ini
- Komponen I mengakumulasi error sepanjang waktu, menghilangkan offset statis
- Komponen D memprediksi tren error untuk mencegah overshoot
- Anti-windup mencegah integral terus bertambah saat output sudah tersaturasi (di batas)
- Clamp memastikan output tidak melampaui kapabilitas aktuator

### 8.4 Tuning PID – Metode Ziegler-Nichols

```
PROSEDUR tuningZieglerNichols():
    // Langkah 1: Set Ki=0, Kd=0; naikkan Kp perlahan
    // Langkah 2: Temukan Ku (Ultimate Gain) saat osilasi berkelanjutan
    // Langkah 3: Catat Pu (Ultimate Period) = periode osilasi
    
    // Tabel rekomendasi gain:
    // Kontroler |  Kp       |  Ki        |  Kd
    // P         |  0.5*Ku   |  -         |  -
    // PI        |  0.45*Ku  |  1.2/Pu    |  -
    // PID       |  0.6*Ku   |  2/Pu      |  Pu/8

    Ku = 2.5   // contoh ultimate gain
    Pu = 0.08  // contoh ultimate period (detik)
    
    Kp = 0.6 * Ku   // = 1.5
    Ki = 2.0 / Pu   // = 25.0
    Kd = Pu / 8.0   // = 0.01
    
    KEMBALIKAN (Kp, Ki, Kd)
```

---

## 9. KONTROLER POSISI DAN KECEPATAN

### 9.1 Kontroler Posisi (Position Control)

Kontroler posisi mengatur robot agar mencapai dan mempertahankan posisi target (x, y, θ).

### 9.2 Pseudo Code Go-to-Goal Controller

```
FUNGSI goToGoalController(robot_pose, goal_pose):
    // Hitung error posisi
    dx = goal_pose.x - robot_pose.x
    dy = goal_pose.y - robot_pose.y
    
    // Jarak ke tujuan
    distance = sqrt(dx² + dy²)
    
    // Sudut ke tujuan
    angle_to_goal = atan2(dy, dx)
    
    // Error orientasi
    heading_error = angle_to_goal - robot_pose.theta
    // Normalisasi ke [-π, π]
    heading_error = atan2(sin(heading_error), cos(heading_error))
    
    // Kontroler proporsional
    v_linear  = Kp_v * distance      // kecepatan linear
    v_angular = Kp_w * heading_error // kecepatan angular
    
    // Jika sudah mendekati tujuan, berhenti
    JIKA distance < 0.05:  // 5 cm threshold
        v_linear  = 0
        v_angular = 0
    
    KEMBALIKAN (v_linear, v_angular)

// Kontroler dua tahap: koreksi arah dulu, baru maju
FUNGSI twoPhaseGoToGoal(robot_pose, goal_pose):
    dx = goal_pose.x - robot_pose.x
    dy = goal_pose.y - robot_pose.y
    distance      = sqrt(dx² + dy²)
    angle_to_goal = atan2(dy, dx)
    heading_error = normalizeAngle(angle_to_goal - robot_pose.theta)
    
    // Fase 1: koreksi orientasi jika error besar
    JIKA abs(heading_error) > 0.1:
        v_linear  = 0
        v_angular = Kp_w * heading_error
    LAINNYA:
        // Fase 2: maju ke tujuan
        v_linear  = Kp_v * distance
        v_angular = Kp_w * heading_error
    
    KEMBALIKAN (v_linear, v_angular)
```

### 9.3 Pseudo Code Cascade Controller (Kecepatan + Posisi)

```
// Kontroler cascade: outer loop posisi, inner loop kecepatan
STRUKTUR CascadeController:
    pid_position  // PID untuk posisi (outer loop)
    pid_velocity  // PID untuk kecepatan (inner loop)

FUNGSI cascadeControl(target_pos, current_pos, current_vel):
    // Outer loop: hitung kecepatan referensi dari error posisi
    vel_ref = pid_position.compute(current_pos)  // setpoint = target_pos
    
    // Inner loop: hitung output aktuator dari error kecepatan
    pid_velocity.setpoint = vel_ref
    motor_cmd = pid_velocity.compute(current_vel)
    
    KEMBALIKAN motor_cmd
```

---

## 10. KONTROLER PADA ROBOT MOBILE DI ROS

### 10.1 Arsitektur Kontrol di ROS

```
[Operator/Planner]
        ↓ geometry_msgs/Twist (/cmd_vel)
[Velocity Controller Node]
        ↓ roda kiri/kanan RPM
[Motor Driver Node]
        ↓ PWM Signal
[Aktuator (Motor DC + Encoder)]
        ↓ encoder pulses
[Odometry Node]
        ↓ nav_msgs/Odometry (/odom)
[State Estimator / TF Broadcaster]
```

### 10.2 Pseudo Code Node Kontroler Kecepatan ROS

```
// ROS Node: velocity_controller.py (konseptual)

IMPOR rospy
IMPOR geometry_msgs.Twist
IMPOR std_msgs.Float32MultiArray

KELAS VelocityController:
    INISIALISASI():
        rospy.init_node('velocity_controller')
        
        // Subscribe ke perintah kecepatan
        subscriber = rospy.Subscriber('/cmd_vel', Twist, self.cmdVelCallback)
        
        // Publisher ke motor driver
        publisher = rospy.Publisher('/motor_cmds', Float32MultiArray, ...)
        
        // PID untuk roda kiri dan kanan
        pid_left  = PIDController(Kp=1.0, Ki=0.1, Kd=0.01, dt=0.02)
        pid_right = PIDController(Kp=1.0, Ki=0.1, Kd=0.01, dt=0.02)
        
        rate = rospy.Rate(50)  // 50 Hz
    
    FUNGSI cmdVelCallback(twist_msg):
        v = twist_msg.linear.x    // m/s
        w = twist_msg.angular.z   // rad/s
        
        // Konversi ke kecepatan roda
        (omega_left, omega_right) = velocityToWheelSpeeds(v, w, L, R)
        
        self.target_left  = omega_left
        self.target_right = omega_right
    
    FUNGSI controlLoop():
        SELAMA rospy.is_shutdown() = FALSE:
            // Baca encoder
            actual_left  = readLeftEncoderSpeed()
            actual_right = readRightEncoderSpeed()
            
            // Hitung sinyal kontrol PID
            pid_left.setpoint  = self.target_left
            pid_right.setpoint = self.target_right
            
            cmd_left  = pid_left.compute(actual_left)
            cmd_right = pid_right.compute(actual_right)
            
            // Publish ke motor
            msg = Float32MultiArray(data=[cmd_left, cmd_right])
            self.publisher.publish(msg)
            
            rate.sleep()
```

---

## 11. ROS_CONTROL DAN CONTROLLER MANAGER

### 11.1 Arsitektur ros_control

**ros_control** adalah framework ROS untuk implementasi kontroler robot yang terstandarisasi dan modular.

```
┌─────────────────────────────────┐
│        Controller Manager       │
│  ┌──────────┐  ┌─────────────┐  │
│  │ JointVel │  │ JointPos    │  │
│  │Controller│  │Controller   │  │
│  └──────────┘  └─────────────┘  │
└────────────┬────────────────────┘
             │ Hardware Interface
┌────────────▼────────────────────┐
│     Hardware Abstraction Layer  │
│    (RobotHW / robot_hw_sim)     │
└─────────────────────────────────┘
```

### 11.2 Jenis Controller Bawaan ros_control

| Controller | Plugin | Kegunaan |
|-----------|--------|---------|
| JointPositionController | position_controllers | Kontrol posisi sendi tunggal |
| JointVelocityController | velocity_controllers | Kontrol kecepatan sendi tunggal |
| JointEffortController | effort_controllers | Kontrol torsi/gaya |
| DiffDriveController | diff_drive_controller | Kontrol robot diferensial |
| JointGroupPositionController | position_controllers | Kontrol posisi multi-sendi |

### 11.3 Pseudo Code Konfigurasi ros_control (YAML)

```yaml
// controllers.yaml (konfigurasi kontroler ros_control)

// Joint State Controller - selalu diperlukan
joint_state_controller:
  type: joint_state_controller/JointStateController
  publish_rate: 50

// Differential Drive Controller
diff_drive_controller:
  type: diff_drive_controller/DiffDriveController
  left_wheel:  ['left_wheel_joint']
  right_wheel: ['right_wheel_joint']
  wheel_separation: 0.20        // L (meter)
  wheel_radius: 0.05            // R (meter)
  pose_covariance_diagonal: [0.001, 0.001, 1e6, 1e6, 1e6, 0.01]
  twist_covariance_diagonal: [0.001, 1e6, 1e6, 1e6, 1e6, 0.01]
  publish_rate: 50
  odom_frame_id: odom
  base_frame_id: base_link
  enable_odom_tf: true
```

---

## 12. ODOMETRI DAN STATE ESTIMATION

### 12.1 Konsep Odometri

**Odometri** adalah estimasi posisi robot berdasarkan pergerakan roda (atau motor). Odometri terakumulasi sepanjang waktu dan mengalami **drift** (kesalahan yang menumpuk).

### 12.2 Pseudo Code Kalman Filter Sederhana untuk Odometri

```
STRUKTUR KalmanFilter:
    x    = [0, 0, 0]    // state: [x, y, theta]
    P    = matriks identitas 3x3 * 0.1   // covariance awal
    Q    = matriks identitas 3x3 * 0.01  // process noise
    R    = matriks identitas 3x3 * 0.05  // measurement noise

FUNGSI predict(kf, v, w, dt):
    theta = kf.x[2]
    
    // Jacobian model gerak (F)
    F = [[1, 0, -v*sin(theta)*dt],
         [0, 1,  v*cos(theta)*dt],
         [0, 0,  1              ]]
    
    // Prediksi state
    kf.x[0] += v * cos(theta) * dt
    kf.x[1] += v * sin(theta) * dt
    kf.x[2] += w * dt
    kf.x[2]  = normalizeAngle(kf.x[2])
    
    // Update covariance
    kf.P = F × kf.P × F_transpose + kf.Q
    
    KEMBALIKAN kf.x

FUNGSI update(kf, z_measurement):
    H = matriks identitas 3x3  // measurement model (diasumsikan langsung)
    
    // Kalman Gain
    S = H × kf.P × H_transpose + kf.R
    K = kf.P × H_transpose × inverse(S)
    
    // Update state dengan pengukuran
    innovation = z_measurement - H × kf.x
    kf.x = kf.x + K × innovation
    
    // Update covariance
    kf.P = (I - K × H) × kf.P
    
    KEMBALIKAN kf.x
```

---

## 13. IMPLEMENTASI DI SIMULASI GAZEBO

### 13.1 Plugin Gazebo untuk Kontrol

Gazebo menyediakan plugin untuk mensimulasikan hardware robot:

| Plugin | Fungsi |
|--------|--------|
| `libgazebo_ros_diff_drive.so` | Simulasi robot diferensial |
| `libgazebo_ros_joint_state_publisher.so` | Publish joint states |
| `libgazebo_ros_imu_sensor.so` | Simulasi IMU |
| `libgazebo_ros_laser.so` | Simulasi LIDAR |

### 13.2 Pseudo Code URDF/Xacro dengan Plugin Gazebo

```xml
<!-- Struktur URDF dasar dengan plugin Gazebo (konseptual) -->
ROBOT "my_robot":
    
    LINK "base_link":
        inertial: mass=2.0, inertia=(Ixx, Iyy, Izz)
        visual: geometry=box(0.3, 0.2, 0.1)
        collision: sama dengan visual
    
    JOINT "left_wheel_joint" revolute:
        parent="base_link"
        child="left_wheel"
        axis=(0, 1, 0)
    
    // Plugin Gazebo Diferensial Drive
    GAZEBO_PLUGIN "libgazebo_ros_diff_drive.so":
        leftJoint:  "left_wheel_joint"
        rightJoint: "right_wheel_joint"
        wheelSeparation: 0.20
        wheelRadius: 0.05
        commandTopic: "/cmd_vel"
        odometryTopic: "/odom"
        odometryFrame: "odom"
        robotBaseFrame: "base_link"
        publishWheelTF: true
        publishWheelJointState: true
        updateRate: 50
```

---

## 14. REKOMENDASI HARDWARE MINI PC

### 14.1 Spesifikasi Minimum Sistem

Untuk menjalankan ROS Noetic/Humble dengan Gazebo dan node kontroler secara real-time:

| Komponen | Minimum | Rekomendasi |
|----------|---------|-------------|
| CPU | Intel Core i5 / AMD Ryzen 5 (4 core) | Intel Core i7 / AMD Ryzen 7 (8 core) |
| RAM | 8 GB | 16 GB |
| Storage | 128 GB SSD | 256 GB NVMe SSD |
| GPU | Onboard (Intel HD/Iris) | NVIDIA GPU (CUDA support) |
| OS | Ubuntu 20.04 LTS | Ubuntu 22.04 LTS |

### 14.2 Rekomendasi Mini PC

| Mini PC | CPU | RAM | Harga (approx) | Catatan |
|---------|-----|-----|----------------|---------|
| **Intel NUC 12 Pro** | Core i7-1260P | up to 64GB | ~$400-600 | Performa terbaik, USB4/TB4 |
| **Beelink SER5 Pro** | Ryzen 7 5800H | up to 32GB | ~$250-350 | Harga terjangkau, GPU onboard kuat |
| **MinisForum UM773** | Ryzen 7 7735HS | up to 32GB | ~$300-450 | Performa tinggi, WiFi 6 |
| **NVIDIA Jetson Nano** | ARM Cortex-A57 | 4GB | ~$150 | CUDA support, ideal robot embedded |
| **NVIDIA Jetson Orin Nano** | 6-core ARM | 8GB | ~$250 | CUDA + AI accelerator, terbaik untuk vision |
| **Raspberry Pi 5** | Cortex-A76 4-core | 8GB | ~$80 | Hemat, cukup untuk ROS 2 ringan |

### 14.3 Perangkat yang Harus Terkoneksi ke Mini PC

#### Sensor Input
| Perangkat | Interface | ROS Package | Kegunaan |
|-----------|-----------|-------------|---------|
| LiDAR (RPLidar A1/A2) | USB (Serial) | `rplidar_ros` | SLAM, obstacle detection |
| Kamera RGB (USB Cam) | USB 2.0/3.0 | `usb_cam` | Visual feedback, YOLO |
| Kamera Depth (RealSense D435) | USB 3.0 | `realsense2_camera` | 3D mapping, depth sensing |
| IMU (MPU-6050 / BNO055) | I2C / USB | `imu_tools` | Orientasi, state estimation |
| Encoder Motor | GPIO / USB | Custom / `rosserial` | Odometri |

#### Aktuator Output
| Perangkat | Interface | Catatan |
|-----------|-----------|---------|
| Motor Driver (L298N/L293D) | GPIO / PWM | Lewat Arduino/ESP32 |
| Servo Motor | PWM | Lewat Arduino/ESP32 |
| ESP32 / Arduino Mega | USB (Serial) | Bridge ROS–Hardware via `rosserial` |

#### Komunikasi
| Kebutuhan | Solusi |
|-----------|--------|
| Wireless robot control | WiFi 802.11ac / USB WiFi adapter |
| ROS multi-machine | Ethernet (100/1000 Mbps) atau WiFi |
| Serial ke mikrokontroler | USB-to-Serial (CP2102/CH340) |

### 14.4 Diagram Koneksi Hardware

```
┌─────────────────────────────────────────────────────────────┐
│                    Mini PC (ROS Master)                     │
│                Ubuntu 20.04 / ROS Noetic                    │
├────────┬────────┬────────┬────────┬────────┬────────────────┤
│ USB    │ USB    │ USB    │ USB    │ Ethernet│ WiFi           │
│ LiDAR  │ Camera │ IMU    │ESP32/  │ Switch  │ Remote Ctrl    │
│RPLidar │USB Cam │USB/I2C │Arduino │ /Router │                │
└────────┴────────┴────────┴───┬────┴─────────┴────────────────┘
                               │ Serial/USB (rosserial)
                    ┌──────────▼──────────┐
                    │    ESP32 / Arduino  │
                    │  Motor Driver (PWM) │
                    │  L298N / L293D      │
                    └──────┬──────────────┘
                           │ DC Motor + Encoder
                    ┌──────▼──────────────┐
                    │   Robot Mobile      │
                    │  Diferensial Drive  │
                    └─────────────────────┘
```

---

## 15. REFERENSI

### Paper Ilmiah (30 Referensi)

1. Craig, J.J. (2005). "Introduction to Robotics: Mechanics and Control." *IEEE Robotics & Automation Magazine*.
2. Siciliano, B., et al. (2009). "Robotics: Modelling, Planning and Control." *Springer*.
3. Quigley, M., et al. (2009). "ROS: an open-source Robot Operating System." *ICRA Workshop on Open Source Software.*
4. Denavit, J., & Hartenberg, R.S. (1955). "A kinematic notation for lower-pair mechanisms based on matrices." *ASME Journal of Applied Mechanics.*
5. Whitney, D.E. (1969). "Resolved motion rate control of manipulators and human prostheses." *IEEE Transactions on Man-Machine Systems.*
6. Buss, S.R. (2004). "Introduction to Inverse Kinematics with Jacobian Transpose, Pseudoinverse and Damped Least Squares methods." *IEEE Journal of Robotics & Automation.*
7. Nakamura, Y., & Hanafusa, H. (1986). "Inverse kinematic solutions with singularity robustness for robot manipulator control." *ASME Journal of Dynamic Systems.*
8. Colome, A., & Torras, C. (2015). "Closed-loop inverse kinematics for redundant robots: Comparative assessment and two enhancements." *IEEE/ASME Transactions on Mechatronics.*
9. Siegwart, R., & Nourbakhsh, I.R. (2011). "Introduction to Autonomous Mobile Robots." *MIT Press.*
10. Thrun, S., Burgard, W., & Fox, D. (2005). "Probabilistic Robotics." *MIT Press.*
11. Astrom, K.J., & Hagglund, T. (2006). "Advanced PID Control." *ISA Press.*
12. Ziegler, J.G., & Nichols, N.B. (1942). "Optimum settings for automatic controllers." *Transactions of the ASME.*
13. Priyambodo, T.K., et al. (2012). "Optimizing PID control of quadrotor using genetic algorithm." *ICICI-BME.*
14. Paden, B., et al. (2016). "A Survey of Motion Planning and Control Techniques for Self-Driving Urban Vehicles." *IEEE Transactions on Intelligent Vehicles.*
15. Corke, P. (2011). "Robotics, Vision and Control: Fundamental Algorithms in MATLAB." *Springer.*
16. Marder-Eppstein, E., et al. (2010). "The Office Marathon: Robust Navigation in an Indoor Office Environment." *ICRA 2010.*
17. Ros, E., et al. (1999). "Velocity control of a mobile robot using fuzzy logic." *IEEE.*
18. Koubaa, A. (2016). "Robot Operating System (ROS): The Complete Reference, Vol 1." *Springer.*
19. Foote, T. (2013). "tf: The transform library." *IEEE International Conference on Technologies for Practical Robot Applications.*
20. Hernandez-Santos, C., et al. (2012). "First Steps in Robot Kinematics and Dynamics Using Simulations in ROS/Gazebo." *ICERI.*
21. Kalman, R.E. (1960). "A new approach to linear filtering and prediction problems." *Journal of Basic Engineering.*
22. Choset, H., et al. (2005). "Principles of Robot Motion: Theory, Algorithms, and Implementation." *MIT Press.*
23. Spong, M.W., Hutchinson, S., & Vidyasagar, M. (2006). "Robot Modeling and Control." *Wiley.*
24. Murray, R.M., Li, Z., & Sastry, S.S. (1994). "A Mathematical Introduction to Robotic Manipulation." *CRC Press.*
25. Andaluz, V.H., et al. (2012). "Nonlinear control of a mobile manipulator." *Robotics and Autonomous Systems.*
26. Martínez, J.L., et al. (2009). "Combining benefits of model-based and model-free approaches for adaptive trajectory tracking control of wheeled mobile robots." *IEEE.*
27. Fox, D., Burgard, W., & Thrun, S. (1997). "The dynamic window approach to collision avoidance." *IEEE Robotics & Automation Magazine.*
28. Simmons, R. (1996). "The curvature-velocity method for local obstacle avoidance." *ICRA.*
29. Borenstein, J., & Koren, Y. (1991). "The vector field histogram–fast obstacle avoidance for mobile robots." *IEEE Transactions on Robotics and Automation.*
30. Arkin, R.C. (1998). "Behavior-Based Robotics." *MIT Press.*

### Buku Referensi (30 Referensi)

1. Craig, J.J. (2018). *Introduction to Robotics: Mechanics and Control* (4th ed.). Pearson.
2. Siciliano, B., Sciavicco, L., Villani, L., & Oriolo, G. (2010). *Robotics: Modelling, Planning and Control*. Springer.
3. Spong, M.W., Hutchinson, S., & Vidyasagar, M. (2006). *Robot Modeling and Control*. Wiley.
4. Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.
5. Siegwart, R., Nourbakhsh, I.R., & Scaramuzza, D. (2011). *Introduction to Autonomous Mobile Robots* (2nd ed.). MIT Press.
6. Corke, P. (2017). *Robotics, Vision and Control: Fundamental Algorithms in Python* (2nd ed.). Springer.
7. Murray, R.M., Li, Z., & Sastry, S.S. (1994). *A Mathematical Introduction to Robotic Manipulation*. CRC Press.
8. Choset, H., Lynch, K.M., Hutchinson, S., Kantor, G., Burgard, W., Kavraki, L.E., & Thrun, S. (2005). *Principles of Robot Motion*. MIT Press.
9. Lynch, K.M., & Park, F.C. (2017). *Modern Robotics: Mechanics, Planning, and Control*. Cambridge University Press.
10. Astrom, K.J., & Hagglund, T. (2006). *Advanced PID Control*. ISA Press.
11. Franklin, G.F., Powell, J.D., & Emami-Naeini, A. (2019). *Feedback Control of Dynamic Systems* (8th ed.). Pearson.
12. Ogata, K. (2010). *Modern Control Engineering* (5th ed.). Prentice Hall.
13. Koubaa, A. (Ed.). (2016). *Robot Operating System (ROS): The Complete Reference, Vol 1*. Springer.
14. Koubaa, A. (Ed.). (2017). *Robot Operating System (ROS): The Complete Reference, Vol 2*. Springer.
15. Lentin, J. (2015). *Mastering ROS for Robotics Programming*. Packt Publishing.
16. Fairchild, C., & Harman, T.L. (2017). *ROS Robotics by Example* (2nd ed.). Packt Publishing.
17. Joseph, L. (2018). *Robot Operating System (ROS) for Absolute Beginners*. Apress.
18. Biggs, G., & MacDonald, B. (2003). *A Survey of Robot Programming Systems*. Proceedings of the Australasian Conference on Robotics and Automation.
19. Latombe, J.C. (1991). *Robot Motion Planning*. Kluwer Academic Publishers.
20. LaValle, S.M. (2006). *Planning Algorithms*. Cambridge University Press.
21. Niku, S.B. (2020). *Introduction to Robotics: Analysis, Control, Applications* (3rd ed.). Wiley.
22. Paul, R.P. (1981). *Robot Manipulators: Mathematics, Programming, and Control*. MIT Press.
23. Luh, J.Y.S., Walker, M.W., & Paul, R.P.C. (1980). *On-line computational scheme for mechanical manipulators*. ASME Journal of Dynamic Systems.
24. Yoshikawa, T. (1990). *Foundations of Robotics: Analysis and Control*. MIT Press.
25. Mason, M.T. (2001). *Mechanics of Robotic Manipulation*. MIT Press.
26. Featherstone, R. (2008). *Rigid Body Dynamics Algorithms*. Springer.
27. Bruyninckx, H. (2001). *Open Robot Control Software: the OROCOS project*. ICRA.
28. Gerkey, B., Vaughan, R.T., & Howard, A. (2003). *The Player/Stage Project: Tools for Multi-Robot and Distributed Sensor Systems*. ICAR.
29. Mahony, R., Kumar, V., & Corke, P. (2012). *Multirotor Aerial Vehicles: Modeling, Estimation, and Control of Quadrotor*. IEEE Robotics & Automation Magazine.
30. Dudek, G., & Jenkin, M. (2010). *Computational Principles of Mobile Robotics* (2nd ed.). Cambridge University Press.
