# TUGAS VIDEO MODUL 09: ROS KINEMATIKA DAN KONTROLER

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 09 – ROS Kinematika dan Kontroler  
**Sifat:** Individu (setiap mahasiswa wajib membuat video sendiri)  
**Format:** Screen recording + narasi suara + tampilan layar  
**Durasi:** 15–25 menit  
**Deadline:** ___________________

---

## A. DESKRIPSI TUGAS

Mahasiswa diwajibkan membuat video **screen recording** yang menjelaskan materi teori Modul 09 sekaligus mendemokan **semua percobaan praktikum (P01–P15)** dan **percobaan project**. Video bersifat individual dan mencerminkan pemahaman pribadi mahasiswa.

### Format Pengumpulan
- **File video:** MP4, resolusi minimal 1280×720 (720p), 30 fps
- **Nama file:** `NIM_Nama_Modul09_TugasVideo.mp4`
- **Upload ke:** Google Drive kelompok / LMS (sesuai instruksi dosen)
- **Tanpa cut berlebihan:** Video boleh diedit ringan tetapi tidak boleh mengganti isi percobaan

---

## B. STRUKTUR VIDEO YANG HARUS DISAMPAIKAN

Video harus mencakup **11 bagian** berikut secara berurutan:

---

### BAGIAN 1 – Pembukaan dan Identitas (1–2 menit)

**Mahasiswa harus menyampaikan:**
- Salam pembuka dan perkenalan diri (nama, NIM, kelas)
- Nama modul: "Modul 09 – ROS Kinematika dan Kontroler"
- Platform yang digunakan: sistem operasi, versi ROS, spesifikasi komputer
- Gambaran singkat isi video (overview 30 detik)

**Tampilan layar saat ini:**
- Desktop Ubuntu dengan terminal terbuka
- Jalankan `rosversion -d` untuk menampilkan versi ROS
- Tampilkan `lsb_release -a` untuk menampilkan versi Ubuntu

---

### BAGIAN 2 – Penjelasan Konsep Kinematika (3–5 menit)

**Mahasiswa harus menyampaikan (dengan kata-kata sendiri):**

1. **Forward Kinematics:**
   - Definisi FK: hubungan joint space → Cartesian space
   - Persamaan FK robot 2-DOF (tulis di whiteboard virtual atau screen annotation)
   - Contoh: hitung manual untuk θ₁=30°, θ₂=45°, L₁=0.5, L₂=0.3

2. **Parameter Denavit-Hartenberg:**
   - Jelaskan 4 parameter: a, α, d, θ
   - Tunjukkan tabel DH untuk robot 2-DOF atau 3-DOF
   - Jelaskan matriks transformasi homogen T(4×4)

3. **Inverse Kinematics:**
   - Perbedaan IK vs FK (arah perhitungan)
   - Dua solusi IK: elbow-up dan elbow-down
   - Konsep singularitas: kapan robot kehilangan derajat kebebasan?

4. **Jacobian:**
   - Definisi J: hubungan kecepatan joint → kecepatan Cartesian
   - Rumus Jvi = zi-1 × (pn - pi-1)
   - Aplikasi: velocity control, force control, IK numerik

**Tampilan layar saat ini:**
- File materi.md terbuka (scroll ke bagian yang relevan)
- Atau diagram/rumus yang digambar menggunakan tool anotasi layar

---

### BAGIAN 3 – Penjelasan PID Controller (2–3 menit)

**Mahasiswa harus menyampaikan:**

1. **Rumus PID:** `u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt`
2. **Fungsi setiap komponen:**
   - P: proporsional dengan error saat ini (gambar diagram blok)
   - I: eliminasi steady-state error (jelaskan integral windup)
   - D: prediksi perubahan error (jelaskan derivative kick)
3. **Efek mengubah Kp, Ki, Kd** pada grafik respons step
4. **Metode tuning:** Ziegler-Nichols atau trial-and-error
5. **Anti-windup:** mengapa diperlukan dan bagaimana mengatasinya

**Tampilan layar saat ini:**
- Buka file `p08_pid_velocity.py` di editor
- Tunjukkan kode PID dan jelaskan struktur kode

---

### BAGIAN 4 – Penjelasan ROS TF dan ros_control (2–3 menit)

**Mahasiswa harus menyampaikan:**

1. **TF Tree ROS:**
   - Tujuan TF: mengelola relasi frame koordinat
   - Hierarki frame standar: world → map → odom → base_link → sensor_frames
   - Cara broadcast TF (TransformBroadcaster)
   - Cara listen TF (TransformListener)

2. **ros_control Framework:**
   - Arsitektur: Controller Manager → Hardware Interface → Joint Interface
   - Tipe controller: JointPositionController, JointVelocityController, DiffDriveController
   - Cara konfigurasi controllers.yaml
   - Controller Manager service: list, load, switch controller

3. **diff_drive_controller:**
   - Parameter utama: wheel_separation, wheel_radius, publish_rate
   - Subscribe `/cmd_vel`, publish `/odom`, broadcast TF odom→base_link

**Tampilan layar saat ini:**
- Buka file `controllers.yaml` dan jelaskan setiap parameter
- Jalankan `rosrun rqt_tf_tree rqt_tf_tree` untuk menampilkan TF tree

---

### BAGIAN 5 – Demo Percobaan P01 hingga P05 (Kinematika) (4–5 menit)

**Mahasiswa harus mendemonstrasikan setiap percobaan:**

#### P01 – FK Robot 2-DOF
- Jalankan: `rosrun modul09_kinematika p01_fk_2dof.py`
- Tunjukkan output terminal dengan nilai FK untuk berbagai input joint angles
- Verifikasi satu nilai secara manual (hitung di depan kamera/layar)

#### P02 – FK dengan Parameter DH
- Tunjukkan tabel DH yang dibuat
- Jalankan kode dan tunjukkan matriks T_total
- Identifikasi posisi end-effector dari kolom ke-4 matriks

#### P03 – IK Analitik 2-DOF
- Jalankan kode dengan target (0.5, 0.3)
- Tunjukkan dua solusi: elbow-up dan elbow-down
- Lakukan verifikasi: masukkan sudut hasil IK ke FK, bandingkan dengan target asli

#### P04 – IK Numerik Jacobian
- Jalankan kode dengan learning rate berbeda (α=0.1 vs α=0.5)
- Bandingkan jumlah iterasi dan error konvergensi
- Tunjukkan grafik konvergensi jika tersedia

#### P05 – Jacobian
- Tunjukkan matriks Jacobian untuk beberapa konfigurasi
- Hitung manipulability index dan identifikasi konfigurasi singular (μ ≈ 0)
- Tunjukkan grafik μ vs θ₁

---

### BAGIAN 6 – Demo Percobaan P06 dan P07 (TF dan URDF) (2–3 menit)

#### P06 – TF Broadcaster
- Jalankan: `rosrun modul09_kinematika p06_tf_broadcaster.py`
- Buka RViz, tambahkan TF display
- Tunjukkan frame yang bergerak dinamis (link1 dan link2 berputar)
- Jalankan `rosrun tf tf_echo world link2` dan tunjukkan output

#### P07 – URDF Robot
- Jalankan: `roslaunch modul09_kinematika p07_urdf.launch`
- Tunjukkan model robot di RViz (base + 2 roda)
- Demonstrasikan slider joint_state_publisher_gui: geser slider → roda berputar di RViz
- Tampilkan TF tree dengan `rosrun rqt_tf_tree rqt_tf_tree`

---

### BAGIAN 7 – Demo Percobaan P08 (PID) (3–4 menit)

**Mahasiswa harus mendemonstrasikan:**

1. Jalankan node PID: `rosrun modul09_kinematika p08_pid_velocity.py`
2. Buka rqt_reconfigure: `rosrun rqt_reconfigure rqt_reconfigure`
3. Buka rqt_plot dan tambahkan topik `/setpoint`, `/process_value`, `/error`
4. **Demo perubahan gain secara live:**
   - Set Kp=1.0, Ki=0, Kd=0 → tunjukkan respons P-only (ada steady-state error)
   - Tambahkan Ki=0.3 → tunjukkan integral menghilangkan steady-state error
   - Tambahkan Kd=0.05 → tunjukkan penurunan overshoot
5. Tunjukkan grafik sebelum dan sesudah tuning (side-by-side screenshot)
6. **Jelaskan:**
   - Mengapa P-only masih ada steady-state error?
   - Apa yang terjadi jika Ki terlalu besar?

---

### BAGIAN 8 – Demo Percobaan P09 hingga P11 (Kontroler Mobile) (3–4 menit)

#### P09 – Go-to-Goal Controller
- Jalankan: `roslaunch modul09_kinematika p09_go_to_goal.launch`
- Buka RViz dan Gazebo side-by-side
- Kirim target dengan rostopic pub
- Tunjukkan robot bergerak menuju target di Gazebo
- Tunjukkan trajectory di RViz (jika ada Odometry display)

#### P10 – Odometri (jika hardware tersedia, atau simulasi)
- Tunjukkan data `/odom` dengan `rostopic echo /odom`
- Jelaskan field-field penting: pose.pose.position, pose.pose.orientation, twist

#### P11 – diff_drive_controller
- Jalankan launch file ros_control
- Tunjukkan `rosservice call /controller_manager/list_controllers`
- Kirim cmd_vel dan amati `/diff_drive_controller/odom`
- Tampilkan TF tree: odom → base_link

---

### BAGIAN 9 – Demo Percobaan P12 hingga P15 (3–4 menit)

#### P12 – Validasi FK di Gazebo
- Tunjukkan perbandingan pose dari `/odom` vs kalkulasi FK dari joint states
- Ukur error dan jelaskan sumbernya

#### P13 – Cascade Controller
- Tunjukkan dua PID (outer position + inner velocity) bekerja bersamaan
- Plot kedua setpoint dan process value di rqt_plot
- Tunjukkan keunggulan: outer loop memilih kecepatan yang tepat

#### P14 – Omni Kinematics
- Tunjukkan output IK untuk berbagai input (maju, geser, putar)
- Verifikasi: FK(IK(input)) = input

#### P15 – Integrasi Sistem
- Jalankan sistem lengkap dari satu launch file
- Demonstrasikan robot multi-waypoint: A → B → C → D
- Tunjukkan semua topik aktif di `rostopic list`
- Screenshot RViz menampilkan robot, TF, dan trajectory

---

### BAGIAN 10 – Demo Percobaan Project (4–6 menit)

**Mahasiswa menjelaskan dan mendemokan project yang dipilih kelompoknya:**

1. **Penjelasan project (1 menit):**
   - Nama project dan cerita latar belakang masalah
   - Komponen yang diimplementasikan (FK/IK, kontroler, odometri, dsb.)
   - Inovasi dibanding percobaan dasar

2. **Penjelasan kode kunci (1–2 menit):**
   - Buka file utama project di editor
   - Jelaskan fungsi/kelas utama
   - Tunjukkan integrasi komponen (subscriber, publisher, callback)

3. **Demo live project (2–3 menit):**
   - Jalankan sistem project (launch file)
   - Demonstrasikan fungsionalitas utama
   - Tunjukkan parameter evaluasi yang berhasil dicapai

---

### BAGIAN 11 – Kesimpulan dan Penutup (1–2 menit)

**Mahasiswa harus menyampaikan:**

1. **Ringkasan pembelajaran** (3–5 poin utama yang dipelajari dari modul ini)
2. **Poin kesulitan** yang dihadapi dan cara mengatasinya
3. **Refleksi project:** apa yang berhasil, apa yang bisa ditingkatkan
4. **Saran untuk mahasiswa berikutnya** yang akan mengerjakan modul ini
5. Ucapan terima kasih dan salam penutup

---

## C. PANDUAN TEKNIS SCREEN RECORDING

### Software yang Disarankan

| OS | Software | Cara Akses |
|----|---------|-----------|
| Ubuntu | OBS Studio | `sudo apt install obs-studio` |
| Ubuntu | Kazam | `sudo apt install kazam` |
| Ubuntu | SimpleScreenRecorder | `sudo apt install simplescreenrecorder` |
| Windows (WSL2) | OBS Studio | Download dari obsproject.com |

### Setup Rekaman yang Dianjurkan

1. **Resolusi:** 1920×1080 (Full HD) atau minimal 1280×720
2. **Frame rate:** 30 fps
3. **Audio:** Aktifkan mikrofon dan pastikan narasi suara jelas
4. **Layout:**
   - Layar utama: terminal + editor code + RViz/Gazebo
   - Opsional: webcam kecil di sudut kanan bawah
5. **Font terminal:** Ukuran minimal 14pt agar terbaca di video
6. **Kecerahan layar:** Cukup terang untuk dokumentasi

### Tips Rekaman

- **Lakukan persiapan:** Uji semua kode sebelum merekam
- **Gunakan split terminal:** buka 2–3 terminal bersamaan agar efisien
- **Anotasi layar:** Gunakan tool seperti Gromit-MPX untuk menggambar di layar saat menjelaskan
- **Jeda yang cukup:** Beri jeda 2–3 detik setiap selesai demo satu percobaan
- **Narasi jelas:** Bicaralah langsung ke mikrofon, jelaskan apa yang sedang dilakukan

---

## D. RUBRIK PENILAIAN VIDEO

### Komponen dan Bobot

| No | Komponen Penilaian | Bobot | Indikator |
|----|-------------------|-------|----------|
| 1  | **Kelengkapan Konten** | 30% | Semua 11 bagian ada, semua P01-P15 tercover |
| 2  | **Kedalaman Penjelasan Teori** | 25% | Penjelasan FK/IK/PID/TF benar dan mendalam |
| 3  | **Demo Percobaan** | 20% | Semua kode berjalan, output ditampilkan dengan jelas |
| 4  | **Kualitas Teknis Video** | 10% | Resolusi cukup, suara jelas, tidak ada gangguan |
| 5  | **Penyampaian dan Pemahaman** | 10% | Mahasiswa menjelaskan dengan kata-kata sendiri |
| 6  | **Demo Project** | 5% | Project berjalan dan dijelaskan dengan baik |
| **Total** | | **100%** | |

---

### Detail Rubrik Per Komponen

#### Komponen 1 – Kelengkapan Konten (30%)

| Skor | Kriteria |
|------|---------|
| 90–100 | Semua 11 bagian hadir, semua P01–P15 dan project terdemonstrasikan |
| 75–89 | Minimal 10 bagian hadir, minimal P01–P12 terdemonstrasikan |
| 60–74 | Minimal 8 bagian hadir, minimal P01–P09 terdemonstrasikan |
| 40–59 | Kurang dari 8 bagian, atau banyak percobaan tidak terdemonstrasikan |
| 0–39 | Konten sangat tidak lengkap atau tidak relevan |

#### Komponen 2 – Kedalaman Penjelasan Teori (25%)

| Skor | Kriteria |
|------|---------|
| 90–100 | Penjelasan FK/IK/PID/TF sangat akurat, menggunakan bahasa sendiri, mampu menjawab pertanyaan "mengapa" |
| 75–89 | Penjelasan akurat dan cukup mendalam, sedikit membaca dari catatan |
| 60–74 | Penjelasan benar tetapi dangkal, banyak membaca dari catatan/layar |
| 40–59 | Penjelasan ada tetapi terdapat kesalahan konsep |
| 0–39 | Penjelasan sangat dangkal atau banyak kesalahan konsep |

#### Komponen 3 – Demo Percobaan (20%)

| Skor | Kriteria |
|------|---------|
| 90–100 | Semua kode berjalan tanpa error, output ditampilkan dan dijelaskan dengan baik |
| 75–89 | Hampir semua kode berjalan, satu atau dua minor error yang segera diatasi |
| 60–74 | Sebagian besar kode berjalan, beberapa percobaan hanya ditampilkan screenshotnya |
| 40–59 | Beberapa percobaan tidak berjalan, bergantung pada screenshot statis |
| 0–39 | Demo tidak berjalan atau tidak relevan |

#### Komponen 4 – Kualitas Teknis Video (10%)

| Skor | Kriteria |
|------|---------|
| 90–100 | Resolusi 1080p, suara jernih, teks terminal terbaca, durasi 15–25 menit |
| 75–89 | Resolusi 720p, suara cukup jelas, teks terbaca sebagian besar waktu |
| 60–74 | Resolusi di bawah 720p atau suara kurang jelas di beberapa bagian |
| 40–59 | Kualitas video/audio buruk yang mengganggu pemahaman |
| 0–39 | Video tidak dapat ditonton atau didengar |

#### Komponen 5 – Penyampaian dan Pemahaman (10%)

| Skor | Kriteria |
|------|---------|
| 90–100 | Berbicara dengan percaya diri, penjelasan sistematis, tidak membaca skrip |
| 75–89 | Penyampaian baik, sesekali melihat catatan, pemahaman terlihat |
| 60–74 | Banyak membaca catatan, tetapi konten masih tersampaikan |
| 40–59 | Terlalu bergantung pada catatan, kurang menunjukkan pemahaman |
| 0–39 | Hanya membaca skrip tanpa pemahaman |

#### Komponen 6 – Demo Project (5%)

| Skor | Kriteria |
|------|---------|
| 90–100 | Project berjalan sempurna, penjelasan inovasi jelas, mencapai semua parameter evaluasi |
| 75–89 | Project berjalan dengan minor issue, inovasi dijelaskan |
| 60–74 | Project berjalan sebagian, inovasi kurang dijelaskan |
| 40–59 | Project tidak berjalan tetapi ada penjelasan konsep |
| 0–39 | Tidak ada demo project |

---

## E. CHECKLIST MAHASISWA SEBELUM SUBMIT

Pastikan video Anda mencakup semua poin berikut:

### Bagian Teori
- [ ] Menjelaskan Forward Kinematics dengan rumus dan contoh numerik
- [ ] Menjelaskan tabel DH dan matriks transformasi homogen
- [ ] Menjelaskan Inverse Kinematics analitik vs numerik
- [ ] Menjelaskan Jacobian dan manipulability
- [ ] Menjelaskan PID controller (P, I, D, anti-windup)
- [ ] Menjelaskan TF tree ROS dan hierarchy frame
- [ ] Menjelaskan ros_control dan diff_drive_controller

### Demo Percobaan
- [ ] P01: FK 2-DOF berjalan, output ditampilkan
- [ ] P02: FK DH berjalan, matriks T ditampilkan
- [ ] P03: IK analitik berjalan, dua solusi ditampilkan
- [ ] P04: IK numerik berjalan, iterasi ditampilkan
- [ ] P05: Jacobian dihitung, manipulability ditampilkan
- [ ] P06: TF broadcaster berjalan, RViz menampilkan frame bergerak
- [ ] P07: URDF di RViz dengan slider joint_state_publisher_gui
- [ ] P08: PID tuning live dengan rqt_reconfigure + rqt_plot
- [ ] P09: Go-to-goal di Gazebo, robot bergerak ke target
- [ ] P10: Odometri dipublish, `rostopic echo /odom` ditampilkan
- [ ] P11: diff_drive_controller RUNNING, robot dikontrol via cmd_vel
- [ ] P12: Validasi FK vs /odom ditunjukkan
- [ ] P13: Cascade controller berjalan, dua PID loop terlihat
- [ ] P14: Omni IK/FK diverifikasi untuk berbagai mode gerak
- [ ] P15: Sistem lengkap berjalan, multi-waypoint demo

### Demo Project
- [ ] Project dipilih dan dijelaskan latar belakangnya
- [ ] Kode utama project ditunjukkan
- [ ] Demo project berjalan di Gazebo

### Teknis Video
- [ ] Resolusi minimal 720p
- [ ] Narasi suara jelas di seluruh video
- [ ] Durasi 15–25 menit
- [ ] Nama file sesuai format: `NIM_Nama_Modul09_TugasVideo.mp4`

---

## F. CONTOH TIMELINE VIDEO

| Menit | Konten |
|-------|--------|
| 0:00 – 1:30 | Pembukaan: perkenalan diri, setup, overview |
| 1:30 – 5:00 | Penjelasan teori kinematika (FK, IK, DH, Jacobian) |
| 5:00 – 7:30 | Penjelasan PID, TF, ros_control |
| 7:30 – 11:00 | Demo P01–P05 (kinematika) |
| 11:00 – 13:00 | Demo P06–P07 (TF, URDF) |
| 13:00 – 15:30 | Demo P08 (PID tuning) |
| 15:30 – 17:30 | Demo P09–P11 (kontroler mobile) |
| 17:30 – 19:30 | Demo P12–P15 (integrasi) |
| 19:30 – 23:00 | Demo project |
| 23:00 – 25:00 | Kesimpulan dan penutup |

---

## G. KEBIJAKAN AKADEMIK

- **Orisinalitas:** Video harus dibuat sendiri. Mahasiswa yang menampilkan video orang lain sebagai miliknya akan mendapat nilai 0
- **Deadline:** Video yang terlambat mendapat pengurangan nilai 10 poin per hari
- **Revisi:** Tidak ada revisi setelah deadline, kecuali ada persetujuan dosen
- **Bahasa:** Diperbolehkan menggunakan Bahasa Indonesia atau Bahasa Inggris
- **Privasi:** Video yang diupload bersifat pribadi (tidak dipublikasikan tanpa izin)
