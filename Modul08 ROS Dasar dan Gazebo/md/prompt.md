# PROMPT NOTEBOOKLLM – MODUL 08: ROS DASAR DAN GAZEBO
## 45 Slide Presentasi – Panduan Prompt Lengkap

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 08 – ROS Dasar dan Gazebo  
**Tujuan:** Menghasilkan materi presentasi 45 slide menggunakan NotebookLLM

---

> **Cara Penggunaan:**
> 1. Upload file `materi.md` modul ini ke NotebookLLM sebagai sumber (source)
> 2. Gunakan setiap prompt di bawah ini secara berurutan untuk menghasilkan konten setiap slide
> 3. Sesuaikan output dengan template presentasi yang digunakan (PowerPoint/Google Slides/Canva)
> 4. Setiap prompt dirancang untuk menghasilkan konten 1 slide lengkap

---

## BAGIAN 1: PENGANTAR ROS (Slide 1–5)

---

### PROMPT SLIDE 1 – COVER / JUDUL

```
Buatkan konten untuk slide pembuka (cover) presentasi dengan informasi berikut:

Judul utama: "ROS DASAR DAN GAZEBO"
Sub-judul: "Pengantar Robot Operating System dan Simulasi Robot"
Informasi tambahan:
- Mata Kuliah: Praktikum Mekatronika dan Robotika
- Program Studi: Teknologi Rekayasa Otomasi
- Modul 08

Sertakan juga:
- Tagline singkat yang menarik tentang ROS (maksimal 1 kalimat)
- Daftar topik utama yang akan dibahas (5-7 poin bullet)

Format output: teks untuk judul, sub-judul, tagline, dan bullet list topik.
```

---

### PROMPT SLIDE 2 – APA ITU ROS?

```
Buatkan konten slide berjudul "Apa itu ROS (Robot Operating System)?" dengan:

1. Definisi ROS dalam 2-3 kalimat yang jelas dan mudah dipahami mahasiswa
2. Jelaskan bahwa ROS bukan sistem operasi sungguhan, melainkan middleware/framework
3. Tiga komponen utama yang disediakan ROS:
   - Infrastruktur komunikasi
   - Tools dan libraries
   - Konvensi dan standar
4. Analogi yang mudah dipahami: bandingkan ROS dengan "Android untuk robot"
5. Satu gambar/diagram konseptual yang bisa dibuat: Tanpa ROS vs Dengan ROS

Gunakan bahasa Indonesia yang formal namun mudah dipahami. Maksimal 8 bullet point.
```

---

### PROMPT SLIDE 3 – SEJARAH DAN VERSI ROS

```
Buatkan konten slide berjudul "Sejarah dan Versi ROS" dengan:

1. Timeline singkat perkembangan ROS:
   - 2007: Dikembangkan Willow Garage
   - 2010: ROS 1.0 dirilis
   - 2020: ROS Noetic (versi terakhir ROS 1, LTS)
   - 2022: ROS 2 Humble (LTS terkini)

2. Tabel perbandingan versi utama yang relevan untuk praktikum:
   Kolom: Versi | Tahun | Ubuntu | Status
   Isi: ROS Melodic, ROS Noetic, ROS 2 Humble

3. Highlight: Modul ini menggunakan ROS Noetic di Ubuntu 20.04

4. Perbedaan kunci ROS 1 vs ROS 2 dalam 3 poin singkat

Sertakan visual: garis waktu (timeline) dan tabel versi.
```

---

### PROMPT SLIDE 4 – MENGAPA ROS DIGUNAKAN?

```
Buatkan konten slide berjudul "Mengapa ROS Digunakan di Industri dan Riset?" dengan:

1. Daftar keuntungan utama ROS (minimal 6 poin):
   - Open source dan gratis
   - Komunitas besar (ribuan package)
   - Hardware abstraction
   - Modularitas (setiap komponen terpisah)
   - Tools siap pakai (RViz, rqt, Gazebo)
   - Digunakan NASA, Boston Dynamics, dll

2. Statistik penggunaan ROS di industri (data dari Open Robotics):
   - >3.000 package di ROS Index
   - Digunakan di 50+ negara
   - >17 juta download per tahun

3. Contoh aplikasi nyata yang menggunakan ROS:
   - PR2 Robot (Willow Garage)
   - TurtleBot (platform edukasi)
   - Fetch Robot (logistik)
   - NASA K-Rex Rover

Format: poin-poin dengan ikon, statistik di kotak highlight.
```

---

### PROMPT SLIDE 5 – ARSITEKTUR ROS: GAMBARAN UMUM

```
Buatkan konten slide berjudul "Arsitektur ROS: Gambaran Umum" dengan:

1. Diagram berlapis arsitektur ROS dari bawah ke atas:
   Layer 4: Aplikasi Robot (navigation, manipulation, perception)
   Layer 3: Package ROS (driver, algoritma, tools)
   Layer 2: ROS Middleware (komunikasi, parameter server)
   Layer 1: Sistem Operasi (Linux Ubuntu)
   Layer 0: Hardware (sensor, aktuator, komputer)

2. Penjelasan singkat setiap layer (1 kalimat per layer)

3. Highlight: "ROS berperan di Layer 2 dan 3"

4. Komponen kunci yang akan dipelajari:
   - Nodes
   - Topics & Messages
   - Services
   - Parameter Server
   - Launch Files

Buat diagram ASCII atau deskripsi visual yang bisa dibuat di PowerPoint.
```

---

## BAGIAN 2: KOMPONEN DASAR ROS (Slide 6–12)

---

### PROMPT SLIDE 6 – NODE

```
Buatkan konten slide berjudul "Node: Unit Komputasi ROS" dengan:

1. Definisi node dalam 1-2 kalimat
2. Karakteristik node:
   - Satu node = satu tugas spesifik
   - Berjalan sebagai proses terpisah
   - Identifikasi dengan nama unik

3. Analogi: node seperti "aplikasi" di smartphone - setiap aplikasi punya tugas sendiri

4. Tabel contoh node dalam sistem robot:
   Node Name | Fungsi
   /lidar_driver | Membaca sensor lidar
   /slam_node | Membangun peta
   /navigation_node | Merencanakan jalur
   /motor_controller | Kontrol kecepatan motor
   /camera_node | Mengambil gambar

5. Perintah untuk melihat node aktif:
   rosnode list
   rosnode info /node_name

Gunakan tabel dan code block untuk perintah.
```

---

### PROMPT SLIDE 7 – TOPICS DAN MESSAGES

```
Buatkan konten slide berjudul "Topics dan Messages: Komunikasi Publish-Subscribe" dengan:

1. Diagram alur publish-subscribe:
   Publisher Node → /topic_name → Subscriber Node
   Sifat: asinkron, one-to-many, loose coupling

2. Definisi:
   - Topic: kanal komunikasi bernama (e.g., /scan, /cmd_vel)
   - Message: tipe data yang dikirim (e.g., sensor_msgs/LaserScan)

3. Tabel tipe message umum:
   Message Type | Keterangan | Contoh Penggunaan
   std_msgs/String | Teks | Log pesan
   geometry_msgs/Twist | Kecepatan | Kontrol robot
   sensor_msgs/LaserScan | Data lidar | Mapping
   nav_msgs/Odometry | Posisi robot | Navigasi

4. Perintah:
   rostopic list
   rostopic echo /cmd_vel
   rostopic hz /scan
   rostopic pub /cmd_vel geometry_msgs/Twist "..."

Sertakan diagram visual dan tabel.
```

---

### PROMPT SLIDE 8 – PUBLISHER DAN SUBSCRIBER

```
Buatkan konten slide berjudul "Membuat Publisher dan Subscriber (Python)" dengan:

1. Kode Publisher minimal yang benar (Python):
   - init_node
   - Publisher object
   - Loop dengan rate.sleep()

2. Kode Subscriber minimal yang benar (Python):
   - init_node
   - Subscriber dengan callback
   - rospy.spin()

3. Penjelasan setiap bagian kode dalam poin:
   - anonymous=True: hindari konflik nama node
   - queue_size: buffer pesan
   - rospy.Rate: kontrol frekuensi
   - rospy.spin(): jaga node tetap hidup

4. Diagram alur eksekusi subscriber (event-driven)

Gunakan code block dengan syntax highlighting. Kode harus singkat dan jelas.
```

---

### PROMPT SLIDE 9 – SERVICES

```
Buatkan konten slide berjudul "Services: Komunikasi Request-Response" dengan:

1. Perbandingan Topic vs Service dalam tabel:
   Aspek | Topic | Service
   Tipe | Publish-Subscribe | Request-Response
   Sifat | Asinkron | Sinkron
   Arah | Satu arah | Dua arah
   Penggunaan | Data sensor kontinu | Operasi sekali

2. Diagram service:
   Client → [Request] → Server
   Client ← [Response] ← Server

3. Contoh penggunaan service di dunia nyata:
   - Reset odometri
   - Mulai/hentikan recording
   - Query status baterai
   - Pindah ke posisi tertentu

4. Contoh kode minimal service client (Python):
   rospy.wait_for_service('/reset_odom')
   proxy = rospy.ServiceProxy('/reset_odom', ResetOdom)
   response = proxy(confirm=True)

5. Perintah:
   rosservice list
   rosservice call /reset_odom "confirm: true"
```

---

### PROMPT SLIDE 10 – ACTIONS

```
Buatkan konten slide berjudul "Actions: Komunikasi untuk Tugas Berlangsung Lama" dengan:

1. Motivasi: mengapa perlu Actions selain Service?
   - Service memblokir sampai selesai
   - Action non-blocking dan bisa dibatalkan
   - Action memberikan feedback berkala

2. Struktur Action (3 bagian):
   - Goal: apa yang ingin dicapai
   - Feedback: progress berkala (selama proses)
   - Result: hasil akhir (sekali selesai)

3. Diagram interaksi:
   Client → Goal → Server
   Client ← Feedback ← Server (berulang)
   Client ← Result ← Server (sekali)
   Client → Cancel → Server (opsional)

4. Contoh use case Actions:
   - Navigasi ke koordinat (feedback: jarak tersisa)
   - Lengan robot mengambil objek (feedback: % selesai)
   - Foto panorama 360° (feedback: sudut saat ini)

5. Package yang digunakan: actionlib
```

---

### PROMPT SLIDE 11 – PARAMETER SERVER

```
Buatkan konten slide berjudul "Parameter Server: Konfigurasi Terpusat ROS" dengan:

1. Definisi Parameter Server (1-2 kalimat)
2. Analogi: seperti "registry" atau "config file global" untuk semua node

3. Operasi dasar dengan contoh perintah:
   Set:   rosparam set /max_speed 0.5
   Get:   rosparam get /max_speed
   List:  rosparam list
   Dump:  rosparam dump config.yaml
   Load:  rosparam load config.yaml

4. Private vs Global parameter:
   ~param_name → parameter private (per node)
   /param_name → parameter global (semua node bisa akses)

5. Kode Python:
   rospy.get_param('~max_speed', 1.0)  # dengan default
   rospy.set_param('~status', 'running')

6. Kapan menggunakan parameter:
   - Kecepatan maksimal robot
   - Threshold sensor
   - Nama topik yang bisa dikonfigurasi
```

---

### PROMPT SLIDE 12 – LAUNCH FILES

```
Buatkan konten slide berjudul "Launch Files: Menjalankan Banyak Node Sekaligus" dengan:

1. Masalah tanpa launch file:
   Terminal 1: roscore
   Terminal 2: rosrun pkg node1
   Terminal 3: rosrun pkg node2
   ... (tidak praktis)

2. Solusi dengan launch file:
   roslaunch my_robot full_system.launch
   (semua node berjalan sekaligus)

3. Elemen-elemen utama launch file XML:
   <node> - menjalankan node
   <param> - set parameter
   <rosparam> - load YAML
   <include> - import launch lain
   <arg> - argumen yang bisa diubah
   <group> - namespace grouping

4. Contoh launch file singkat (5-8 baris XML)

5. Tips penting:
   - Selalu set output="screen" untuk melihat log
   - Gunakan <arg> untuk fleksibilitas
   - <include> untuk modularitas
```

---

## BAGIAN 3: WORKSPACE DAN PACKAGE (Slide 13–15)

---

### PROMPT SLIDE 13 – WORKSPACE CATKIN

```
Buatkan konten slide berjudul "Catkin Workspace: Struktur Proyek ROS" dengan:

1. Definisi workspace catkin dan fungsinya

2. Diagram struktur direktori workspace:
   catkin_ws/
   ├── build/    (hasil kompilasi)
   ├── devel/    (libraries & headers)
   └── src/      (SOURCE CODE di sini)
       ├── CMakeLists.txt
       └── my_package/

3. Perintah setup workspace:
   mkdir -p ~/catkin_ws/src
   cd ~/catkin_ws && catkin_make
   source devel/setup.bash

4. Aturan penting:
   - Hanya edit file di folder src/
   - Selalu jalankan "catkin_make" setelah buat package baru
   - "source devel/setup.bash" wajib di setiap terminal baru

5. Tips: tambahkan "source ~/catkin_ws/devel/setup.bash" ke ~/.bashrc
```

---

### PROMPT SLIDE 14 – MEMBUAT PACKAGE ROS

```
Buatkan konten slide berjudul "Membuat Package ROS Baru" dengan:

1. Perintah membuat package:
   cd ~/catkin_ws/src
   catkin_create_pkg nama_pkg rospy std_msgs geometry_msgs

2. Isi package setelah dibuat:
   nama_pkg/
   ├── CMakeLists.txt
   ├── package.xml
   └── src/

3. Penjelasan package.xml (struktur singkat):
   - <name>: nama package
   - <version>: versi
   - <description>: deskripsi
   - <build_depend>: dependensi build
   - <exec_depend>: dependensi runtime

4. Perintah setelah membuat package:
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash

5. Cek package berhasil dibuat:
   rospack list | grep nama_pkg
   roscd nama_pkg
```

---

### PROMPT SLIDE 15 – PERINTAH-PERINTAH PENTING ROS

```
Buatkan konten slide berjudul "Cheatsheet: Perintah ROS yang Sering Digunakan" dengan:

Format tabel dua kolom: Perintah | Fungsi

Kelompokkan dalam 4 kategori:

A. Manajemen Node:
- roscore → Jalankan ROS Master
- rosrun → Jalankan satu node
- roslaunch → Jalankan launch file
- rosnode list → Daftar node aktif
- rosnode kill → Matikan node

B. Topics:
- rostopic list → Daftar topics
- rostopic echo → Tampilkan data
- rostopic hz → Frekuensi topic
- rostopic pub → Publish manual

C. Services & Params:
- rosservice list / call
- rosparam list / get / set

D. Debugging:
- rqt_graph → Visualisasi grafik
- rqt_plot → Plot data real-time
- rosbag record / play → Rekam/putar data
- roswtf → Diagnosa masalah

Gunakan tabel yang rapi dan mudah dibaca.
```

---

## BAGIAN 4: TF DAN URDF (Slide 16–19)

---

### PROMPT SLIDE 16 – TRANSFORM FRAMES (TF)

```
Buatkan konten slide berjudul "TF: Sistem Koordinat Robot" dengan:

1. Masalah yang diselesaikan TF:
   "Di mana posisi sensor kamera relatif terhadap roda robot?"
   "Bagaimana mengkonversi posisi dari frame map ke frame robot?"

2. Hirarki frame robot tipikal:
   map → odom → base_link → sensor_frames

3. Diagram tree:
   map
    └── odom
         └── base_link
              ├── base_laser
              ├── base_camera
              └── imu_link

4. TF Broadcaster vs TF Listener:
   - Broadcaster: mempublish transformasi
   - Listener: membaca transformasi

5. Perintah:
   rosrun tf view_frames → Tampilkan semua TF tree
   rosrun rviz rviz → Visualisasi TF di RViz
   rosrun tf tf_echo /odom /base_link → Lihat transformasi

6. Package: tf2_ros (versi terbaru)
```

---

### PROMPT SLIDE 17 – URDF: DESKRIPSI ROBOT

```
Buatkan konten slide berjudul "URDF: Mendefinisikan Model Robot" dengan:

1. Definisi URDF (Unified Robot Description Format)
   - Format XML untuk deskripsi fisik robot
   - Digunakan RViz dan Gazebo untuk visualisasi dan simulasi

2. Dua komponen utama URDF:
   A. LINK: bagian fisik robot
      - Visual geometry (tampilan)
      - Collision geometry (fisika)
      - Inertial properties (massa, inersia)
   
   B. JOINT: penghubung antar link
      - Tipe: fixed, revolute, continuous, prismatic

3. Tabel jenis joint:
   Tipe | Keterangan | Contoh
   fixed | Tidak bergerak | Chassis ke sensor
   continuous | Rotasi bebas | Roda
   revolute | Rotasi terbatas | Sendi lengan
   prismatic | Gerak linier | Lift, slider

4. Hierarki link-joint robot sederhana:
   base_link
    ├──[joint]── wheel_left
    ├──[joint]── wheel_right
    └──[joint]── laser_link

5. Cek URDF:
   check_urdf robot.urdf
   urdf_to_graphiz robot.urdf
```

---

### PROMPT SLIDE 18 – XACRO: URDF YANG LEBIH BAIK

```
Buatkan konten slide berjudul "Xacro: Menulis URDF yang Lebih Efisien" dengan:

1. Masalah URDF biasa:
   - Copy-paste berulang (misal dua roda identik)
   - Nilai hardcoded susah diubah
   - File panjang dan sulit dibaca

2. Solusi Xacro:
   - Macro: buat template yang bisa dipanggil ulang
   - Property: variabel/konstanta
   - If/unless: kondisional

3. Contoh property:
   <xacro:property name="wheel_radius" value="0.05"/>

4. Contoh macro sederhana:
   <xacro:macro name="wheel" params="prefix side">
     <link name="${prefix}_wheel">...</link>
     <joint name="${prefix}_joint">...</joint>
   </xacro:macro>
   
   Penggunaan:
   <xacro:wheel prefix="left" side="1"/>
   <xacro:wheel prefix="right" side="-1"/>

5. Perintah konversi Xacro ke URDF:
   xacro robot.urdf.xacro > robot.urdf
   rosrun xacro xacro robot.urdf.xacro

6. Keuntungan: file lebih pendek, mudah modifikasi
```

---

### PROMPT SLIDE 19 – ROBOT STATE PUBLISHER

```
Buatkan konten slide berjudul "robot_state_publisher: Mempublish TF dari URDF" dengan:

1. Fungsi robot_state_publisher:
   - Membaca URDF dari parameter /robot_description
   - Membaca joint states dari /joint_states
   - Mempublish transformasi (TF) semua link secara otomatis

2. Alur kerja:
   URDF → /robot_description parameter
   Encoder/simulasi → /joint_states topic
   robot_state_publisher → /tf topic
   RViz/Gazebo → menampilkan model robot

3. Cara menjalankan:
   Di launch file:
   <param name="robot_description" command="xacro robot.urdf.xacro"/>
   <node pkg="robot_state_publisher" type="robot_state_publisher" name="rsp"/>

4. joint_state_publisher_gui:
   - Untuk pengujian tanpa hardware/simulasi
   - Slider GUI untuk menggerakkan setiap joint
   - Install: sudo apt install ros-noetic-joint-state-publisher-gui

5. Verifikasi:
   rosrun rviz rviz → tambahkan display RobotModel dan TF
```

---

## BAGIAN 5: RVIZ DAN VISUALISASI (Slide 20–22)

---

### PROMPT SLIDE 20 – PENGENALAN RVIZ

```
Buatkan konten slide berjudul "RViz: Visualisasi 3D Robot dan Sensor" dengan:

1. Definisi RViz dan fungsinya

2. Apa yang bisa ditampilkan RViz:
   - Model robot 3D (dari URDF)
   - Data laser scan (titik-titik merah)
   - Peta (occupancy grid)
   - Kamera feed
   - Odometri dan path
   - TF coordinate frames
   - Marker kustom

3. Cara membuka RViz:
   rviz
   rviz -d config.rviz  (dengan konfigurasi tersimpan)

4. Area utama interface RViz:
   - Panel kiri: daftar display
   - Tengah: viewport 3D
   - Kanan atas: navigasi view
   - Bawah: status bar

5. Langkah pertama setup:
   1. Set Fixed Frame (e.g., odom atau map)
   2. Add → RobotModel
   3. Add → TF
   4. Add → LaserScan → set topic /scan
   5. Simpan konfigurasi: File > Save Config
```

---

### PROMPT SLIDE 21 – MENAMPILKAN DATA DI RVIZ

```
Buatkan konten slide berjudul "Menampilkan Berbagai Data di RViz" dengan:

1. Tabel Display Types yang paling sering digunakan:
   Display Type | Topic Umum | Keterangan
   RobotModel | - | Model URDF robot
   TF | - | Coordinate frames
   LaserScan | /scan | Titik-titik lidar
   Image | /camera/image_raw | Feed kamera
   Odometry | /odom | Jejak robot
   Map | /map | Peta occupancy
   Path | /move_base/.../plan | Jalur navigasi
   MarkerArray | /visualization_marker | Marker kustom

2. Tips Fixed Frame:
   - map: gunakan jika ada peta
   - odom: gunakan saat eksplorasi
   - base_link: tampilan dari sudut pandang robot

3. Cara mengubah warna point cloud lidar:
   LaserScan → Color Transformer → FlatColor atau Intensity

4. Menyimpan dan memuat konfigurasi RViz:
   File > Save Config As → robot_view.rviz
   rviz -d $(find my_robot)/rviz/robot_view.rviz

5. Contoh screenshot RViz dengan robot dan laser scan
```

---

### PROMPT SLIDE 22 – rqt TOOLS

```
Buatkan konten slide berjudul "rqt Tools: Dashboard Debugging ROS" dengan:

1. rqt adalah framework GUI modular ROS

2. Plugin-plugin rqt yang paling berguna:
   Tool | Perintah | Fungsi
   rqt_graph | rqt_graph | Visualisasi node-topic
   rqt_plot | rqt_plot | Plot data real-time
   rqt_console | rqt_console | Log viewer
   rqt_image_view | rqt_image_view | Lihat gambar kamera
   rqt_bag | rqt_bag | GUI rosbag player/recorder
   rqt_topic | - | Monitor topics
   rqt_service_caller | - | Panggil service manual

3. Cara membuka rqt dengan semua plugin:
   rqt

4. Cara menggunakan rqt_graph:
   rqt_graph
   → pilih "All" di dropdown
   → centang "Dead sinks" dan "Leaf topics"
   → panah menunjukkan aliran data

5. rqt_plot untuk monitoring:
   rqt_plot /odom/pose/pose/position/x /odom/pose/pose/position/y
   Berguna untuk memantau pergerakan robot secara real-time
```

---

## BAGIAN 6: SIMULASI DENGAN GAZEBO (Slide 23–30)

---

### PROMPT SLIDE 23 – PENGENALAN GAZEBO

```
Buatkan konten slide berjudul "Gazebo: Simulator Robot 3D" dengan:

1. Definisi Gazebo dan mengapa diperlukan:
   - Simulasi fisika realistis sebelum uji ke hardware nyata
   - Hemat biaya (tidak perlu hardware mahal)
   - Aman (bisa crash virtual tanpa rusak robot)
   - Reproducible (kondisi yang sama bisa diulang)

2. Kemampuan Gazebo:
   - Fisika: gravitasi, gesekan, tabrakan (ODE/Bullet)
   - Sensor: kamera, lidar, IMU, GPS, sonar
   - Model 3D realistis
   - Lingkungan dinamis (objek bisa bergerak)
   - Integrasi penuh dengan ROS

3. Versi:
   - Gazebo Classic (Gazebo 11) → digunakan modul ini
   - Ignition Gazebo / Gazebo Sim → generasi berikutnya

4. Menjalankan Gazebo dengan ROS:
   roslaunch gazebo_ros empty_world.launch

5. Topics yang otomatis ada saat Gazebo + ROS:
   /clock, /gazebo/model_states, /gazebo/link_states
```

---

### PROMPT SLIDE 24 – ARSITEKTUR GAZEBO

```
Buatkan konten slide berjudul "Arsitektur Gazebo" dengan:

1. Komponen utama Gazebo:
   A. World: lingkungan simulasi
      - Gravity, magnetic field, atmosfer
      - Light sources
      - Static dan dynamic models
   
   B. Model: objek dalam simulasi
      - Links (rigid body)
      - Joints
      - Sensors
      - Plugins
   
   C. Physics Engine (ODE):
      - Collision detection
      - Dynamics calculation
   
   D. Rendering Engine (OGRE):
      - Tampilan 3D
      - Ray casting untuk sensor

2. Format file Gazebo:
   .world → deskripsi environment
   .sdf → deskripsi model (SDF format)
   URDF → bisa digunakan dengan gazebo extensions

3. Alur data Gazebo ↔ ROS:
   ROS Node → [/cmd_vel] → Gazebo Plugin → Model Physics
   Gazebo Sensor → Plugin → ROS Topic → ROS Node
```

---

### PROMPT SLIDE 25 – WORLD FILE DAN MODEL

```
Buatkan konten slide berjudul "World File: Mendefinisikan Lingkungan Simulasi" dengan:

1. Struktur file .world (SDF):
   <world name="my_world">
     <include> sun / ground_plane </include>
     <model> dinding, meja, obstacle </model>
     <physics> ODE settings </physics>
   </world>

2. Model built-in Gazebo yang siap pakai:
   - model://sun
   - model://ground_plane
   - model://aws_robomaker_warehouse_*
   - model://cafe_table

3. Cara menambah obstacle:
   <model name="box_1">
     <static>true</static>
     <pose>2 0 0.5 0 0 0</pose>
     <link name="link">
       <collision> box 1x1x1 </collision>
       <visual> box dengan warna </visual>
     </link>
   </model>

4. Menyimpan world baru:
   Gazebo GUI → File > Save World As → my_world.world

5. Direktori model:
   ~/.gazebo/models/ → model kustom lokal
   /usr/share/gazebo-11/models/ → model bawaan
```

---

### PROMPT SLIDE 26 – SPAWN ROBOT DI GAZEBO

```
Buatkan konten slide berjudul "Menampilkan Robot di Gazebo (Spawn)" dengan:

1. Proses spawn robot:
   Step 1: Load URDF ke parameter /robot_description
   Step 2: Jalankan spawn_model node
   Step 3: Gazebo menampilkan robot

2. Cara spawn melalui launch file:
   <!-- Load URDF dari xacro -->
   <param name="robot_description"
          command="xacro $(find my_robot)/urdf/robot.urdf.xacro"/>

   <!-- Spawn ke Gazebo -->
   <node pkg="gazebo_ros" type="spawn_model" name="spawn_robot"
         args="-urdf -model my_robot -param robot_description
               -x 0 -y 0 -z 0.1"/>

3. Parameter spawn:
   -x, -y, -z → posisi awal
   -R, -P, -Y → orientasi awal (roll, pitch, yaw)
   -model → nama model di Gazebo
   -urdf → format URDF (bukan SDF)

4. Verifikasi berhasil:
   rostopic list → seharusnya muncul /odom, /scan, dll
   rosservice call /gazebo/get_model_state ...

5. Masalah umum dan solusi:
   "model already exists" → spawn dengan nama berbeda
   Robot jatuh/terbenam → cek z awal dan ukuran collision
```

---

### PROMPT SLIDE 27 – GAZEBO PLUGINS

```
Buatkan konten slide berjudul "Gazebo Plugins: Jembatan ROS dan Simulasi" dengan:

1. Apa itu Gazebo plugin?
   File .so (shared library) yang menghubungkan Gazebo ke ROS.
   Tanpa plugin, Gazebo tidak mengirim/menerima data ke/dari ROS.

2. Tabel plugin paling penting:
   Plugin | Filename .so | Fungsi
   Differential Drive | libgazebo_ros_diff_drive.so | Kontrol robot 2 roda
   Laser | libgazebo_ros_laser.so | Publish /scan
   Camera | libgazebo_ros_camera.so | Publish /image_raw
   IMU | libgazebo_ros_imu_sensor.so | Publish /imu
   P3D Odometry | libgazebo_ros_p3d.so | Ground truth odometry
   Skid Steer | libgazebo_ros_skid_steer_drive.so | Robot 4 roda

3. Cara menambahkan plugin ke URDF/Xacro:
   <gazebo>
     <plugin name="nama" filename="libgazebo_ros_diff_drive.so">
       <commandTopic>cmd_vel</commandTopic>
       ...
     </plugin>
   </gazebo>

4. Catatan: plugin diletakkan di dalam elemen <gazebo> pada URDF
   Bukan di dalam <link> atau <joint>
```

---

### PROMPT SLIDE 28 – DIFFERENTIAL DRIVE PLUGIN

```
Buatkan konten slide berjudul "Differential Drive Plugin: Mengontrol Robot 2 Roda" dengan:

1. Konsep kinematika differential drive:
   v = (v_kanan + v_kiri) / 2       (kecepatan linear)
   ω = (v_kanan - v_kiri) / L       (kecepatan angular, L=wheel separation)

2. Konfigurasi plugin diff drive (parameter penting):
   <commandTopic>cmd_vel</commandTopic>     → terima /cmd_vel
   <odometryTopic>odom</odometryTopic>      → publish /odom
   <leftJoint>joint_wheel_left</leftJoint>  → nama joint kiri
   <rightJoint>joint_wheel_right</rightJoint>
   <wheelSeparation>0.23</wheelSeparation>   → jarak antar roda (m)
   <wheelDiameter>0.10</wheelDiameter>       → diameter roda (m)
   <updateRate>50.0</updateRate>             → Hz

3. Topics yang dihasilkan:
   /cmd_vel → INPUT kecepatan (Twist)
   /odom → OUTPUT odometri (Odometry)
   /tf → TF odom→base_link otomatis dipublish

4. Uji pergerakan:
   rostopic pub /cmd_vel geometry_msgs/Twist \
   "{linear: {x: 0.3}, angular: {z: 0.0}}"

5. Tips: pastikan nama joint di plugin = nama joint di URDF
```

---

### PROMPT SLIDE 29 – SENSOR LASER DI GAZEBO

```
Buatkan konten slide berjudul "Simulasi Sensor Laser (Lidar) di Gazebo" dengan:

1. Jenis lidar yang umum disimulasikan:
   - Hokuyo UTM-30LX (270°, 30m)
   - SICK LMS-511 (190°, 80m)
   - Velodyne VLP-16 (3D, 16 channel)
   - Generic 360° 2D laser

2. Konfigurasi sensor laser di URDF:
   Parameter penting:
   - samples: jumlah sinar (misal 360 untuk 1°/sinar)
   - min_angle / max_angle: sudut scan
   - min/max range: jarak minimum/maksimum
   - noise: gaussian noise (stddev ~0.01 realistis)

3. Plugin yang digunakan:
   libgazebo_ros_laser.so
   → Mempublish ke /scan (sensor_msgs/LaserScan)

4. Visualisasi:
   - Di Gazebo: aktifkan "Visualize" pada sensor
   - Di RViz: Add → LaserScan → topic /scan

5. Topik yang dihasilkan:
   /scan → LaserScan (360 nilai jarak dalam meter)
   Fields: header, angle_min/max, range_min/max, ranges[], intensities[]

6. Contoh membaca data laser:
   rostopic echo /scan/ranges  → array panjang
   Indeks 0 = sudut paling kiri (angle_min)
```

---

### PROMPT SLIDE 30 – SIMULASI KAMERA DI GAZEBO

```
Buatkan konten slide berjudul "Simulasi Sensor Kamera di Gazebo" dengan:

1. Tipe kamera yang bisa disimulasikan:
   - Kamera monokuler (RGB)
   - Kamera stereo
   - Depth camera (RGBD, seperti Kinect)
   - Wide angle camera

2. Parameter kamera penting:
   - horizontal_fov: field of view (1.3962 rad ≈ 80°)
   - image width/height: resolusi (640x480)
   - format: R8G8B8 untuk RGB
   - clip near/far: jarak render (0.02 - 300m)

3. Plugin: libgazebo_ros_camera.so
   Topics yang dihasilkan:
   /camera/image_raw → sensor_msgs/Image
   /camera/camera_info → sensor_msgs/CameraInfo

4. Melihat gambar kamera:
   rqt_image_view
   → pilih topic /camera/image_raw

5. Untuk depth camera (Kinect-like):
   Plugin: libgazebo_ros_openni_kinect.so
   Topics: /camera/rgb/image_raw
           /camera/depth/image_raw
           /camera/depth/points (PointCloud2)

6. Aplikasi:
   - Line following (deteksi garis)
   - Object detection
   - Visual odometry
```

---

## BAGIAN 7: PERCOBAAN PRAKTIKUM (Slide 31–38)

---

### PROMPT SLIDE 31 – OVERVIEW 20 PERCOBAAN

```
Buatkan konten slide berjudul "20 Percobaan Praktikum: Overview" dengan:

Tabel lengkap 20 percobaan:
No | Judul Percobaan | Tujuan Singkat
1 | Instalasi ROS Noetic | Setup environment ROS
2 | Setup Catkin Workspace | Membuat workspace & package pertama
3 | Hello World ROS | Publisher & Subscriber pertama
4 | Custom Messages | Membuat tipe data kustom
5 | Simulasi Gerakan dengan cmd_vel | Kontrol gerak dengan topik
6 | Services – Reset Odometri | Membuat service server & client
7 | Parameter Server | Konfigurasi node dengan parameter
8 | Launch Files | Automatisasi menjalankan sistem
9 | URDF Robot Model | Membuat model robot 3D
10 | Xacro: URDF Modular | Parametrisasi model robot
11 | RViz: Visualisasi Robot | Menampilkan model dan TF
12 | Gazebo: Setup Simulasi Pertama | Environment dan world file
13 | Spawn Robot di Gazebo | Menampilkan URDF di Gazebo
14 | Differential Drive Plugin | Kontrol robot 2 roda
15 | Simulasi Sensor Laser | Membaca data lidar virtual
16 | Simulasi Kamera | Mengambil gambar dari kamera virtual
17 | Simulasi IMU | Membaca data orientasi robot
18 | Wall Avoidance | Hindari dinding dengan sensor laser
19 | rosbag: Record & Replay | Merekam dan memutar data
20 | Integrasi Penuh | Sistem lengkap robot di Gazebo

Format: tabel 3 kolom. Highlight percobaan 13-20 sebagai topik lanjutan.
```

---

### PROMPT SLIDE 32 – PERCOBAAN 1–5: DASAR ROS

```
Buatkan konten slide berjudul "Percobaan 1–5: Fondasi ROS" dengan:

Untuk setiap percobaan, sertakan:
- Tujuan
- Langkah utama (3-5 poin)
- Output yang diharapkan

Percobaan 1: Instalasi ROS Noetic
- Tujuan: ROS terinstall dan berjalan
- Output: roscore berjalan, rosversion menampilkan "noetic"

Percobaan 2: Setup Workspace
- Tujuan: catkin_ws siap dengan package pertama
- Output: package muncul di rospack list

Percobaan 3: Hello World ROS
- Tujuan: Publisher kirim "Hello" ke topic, Subscriber menerima
- Output: rostopic echo menampilkan pesan

Percobaan 4: Custom Messages
- Tujuan: Membuat dan menggunakan SensorData.msg
- Output: rostopic echo menampilkan data custom

Percobaan 5: Gerak Robot Virtual
- Tujuan: Kirim cmd_vel ke robot simulator sederhana
- Output: Robot bergerak mengikuti perintah

Format: 5 kotak kecil dengan warna berbeda.
```

---

### PROMPT SLIDE 33 – PERCOBAAN 6–10: KOMUNIKASI DAN MODEL

```
Buatkan konten slide berjudul "Percobaan 6–10: Services, Parameters, dan Model Robot" dengan:

Percobaan 6: Services
- Input: request reset_odometry
- Output: posisi robot kembali ke (0,0,0)

Percobaan 7: Parameter Server
- Demo: ubah max_speed via rosparam, robot mengikuti
- Output: node membaca parameter dan menggunakannya

Percobaan 8: Launch Files
- Jalankan: roslaunch my_robot full_system.launch
- Output: 3+ node berjalan sekaligus

Percobaan 9: URDF Robot
- Buat: diff_robot.urdf dengan base + 2 roda + sensor
- Output: check_urdf pass, tampil di RViz

Percobaan 10: Xacro
- Konversi URDF ke Xacro dengan macro untuk roda
- Output: File lebih pendek, fungsi identik

Sertakan diagram/gambar untuk setiap percobaan jika relevan.
```

---

### PROMPT SLIDE 34 – PERCOBAAN 11–15: RVIZ DAN GAZEBO DASAR

```
Buatkan konten slide berjudul "Percobaan 11–15: RViz dan Gazebo" dengan:

Percobaan 11: RViz Visualisasi
- Tampilkan: RobotModel + TF + LaserScan di RViz
- Output: screenshot RViz dengan robot 3D

Percobaan 12: Gazebo World
- Buat: simple_world.world dengan 4 dinding
- Output: Gazebo terbuka dengan arena kotak

Percobaan 13: Spawn Robot
- Spawn diff_robot.urdf ke Gazebo
- Output: robot muncul di tengah arena

Percobaan 14: Differential Drive
- Konfigurasi plugin diff_drive di URDF
- Kirim cmd_vel → robot bergerak
- Output: robot maju/belok di Gazebo

Percobaan 15: Sensor Laser
- Tambahkan sensor laser ke robot
- Output: /scan topic muncul, visualisasi di RViz

Format deskriptif dengan gambar expected output.
```

---

### PROMPT SLIDE 35 – PERCOBAAN 16–20: SENSOR DAN INTEGRASI

```
Buatkan konten slide berjudul "Percobaan 16–20: Sensor Lanjutan dan Integrasi" dengan:

Percobaan 16: Simulasi Kamera
- Tambahkan kamera ke robot Gazebo
- Output: /camera/image_raw tersedia, tampil di rqt_image_view

Percobaan 17: Simulasi IMU
- Tambahkan sensor IMU ke robot
- Output: /imu topic, data orientasi real-time

Percobaan 18: Wall Avoidance
- Algoritma: jika /scan < 0.5m → belok, else maju
- Output: robot menghindari dinding secara otomatis

Percobaan 19: rosbag
- Record: rosbag record /scan /odom /cmd_vel
- Replay: rosbag play experiment.bag
- Output: data identik saat replay

Percobaan 20: Integrasi Penuh
- Sistem: URDF + Gazebo + laser + kamera + wall avoidance
- Launch: roslaunch my_robot full_demo.launch
- Output: robot otonom bergerak menghindari dinding

Highlight percobaan 20 sebagai puncak pembelajaran modul.
```

---

## BAGIAN 8: PROJECT DAN PENILAIAN (Slide 36–40)

---

### PROMPT SLIDE 36 – PROJECT MODUL 08

```
Buatkan konten slide berjudul "Project Modul 08: Robot Simulator ROS-Gazebo" dengan:

1. Deskripsi umum project:
   Setiap kelompok membangun sistem robot lengkap berbasis ROS dan Gazebo
   yang menyelesaikan satu tugas otomasi dunia nyata.

2. Tiga kategori project yang tersedia:
   A. Mobile Robot Navigation
      - Robot mencari dan mengambil objek
   B. Industrial Inspection Robot
      - Robot memeriksa area pabrik secara otonom
   C. Swarm Robot Coordination
      - 2-3 robot bekerja sama menyelesaikan tugas

3. Komponen wajib setiap project:
   - Robot model URDF/Xacro
   - Environment Gazebo kustom
   - Minimum 2 sensor (lidar + kamera)
   - Algoritma kontrol autonomous (bukan manual)
   - Visualisasi di RViz
   - Launch file lengkap

4. Deliverables:
   - Source code (ROS package)
   - Video demo (screen recording)
   - Laporan teknis
```

---

### PROMPT SLIDE 37 – RUBRIK PENILAIAN

```
Buatkan konten slide berjudul "Rubrik Penilaian Modul 08" dengan:

Tabel penilaian komprehensif:

A. Percobaan Praktikum (40%)
   - Completion 20 percobaan
   - Jobsheet terisi lengkap
   - Analisa dan jawaban pertanyaan

B. Project (35%)
   - Fungsionalitas (robot berjalan sesuai spec)
   - Kualitas kode (struktur, komentar)
   - Kompleksitas solusi
   - Inovasi dan improvisasi

C. Tugas Video (25%)
   - Kelengkapan konten yang dijelaskan
   - Akurasi teknis
   - Kualitas presentasi

Total: 100 poin

Grade:
A: 85-100 (Sangat Baik)
B: 70-84  (Baik)
C: 55-69  (Cukup)
D: 40-54  (Kurang)
E: <40    (Tidak Lulus)
```

---

### PROMPT SLIDE 38 – TIMELINE DAN JADWAL

```
Buatkan konten slide berjudul "Timeline Modul 08" dengan:

Tabel jadwal per pertemuan:

Pertemuan 1 (3 jam):
- Instalasi ROS Noetic
- Setup workspace
- Percobaan 1-2

Pertemuan 2 (3 jam):
- Nodes, Topics, Messages
- Percobaan 3-5

Pertemuan 3 (3 jam):
- Services, Parameters, Launch
- Percobaan 6-8

Pertemuan 4 (3 jam):
- URDF, Xacro, RViz
- Percobaan 9-11

Pertemuan 5 (3 jam):
- Gazebo: setup, spawn, drive
- Percobaan 12-14

Pertemuan 6 (3 jam):
- Sensor simulasi: laser, kamera, IMU
- Percobaan 15-17

Pertemuan 7 (3 jam):
- Wall avoidance, rosbag, integrasi
- Percobaan 18-20

Pertemuan 8-10 (project):
- Pengerjaan project kelompok
- Bimbingan dosen

Pertemuan 11-12 (ujian):
- Presentasi project
- Demo simulasi

Presentasikan dalam bentuk Gantt chart atau tabel berwarna.
```

---

## BAGIAN 9: TIPS DAN TROUBLESHOOTING (Slide 39–43)

---

### PROMPT SLIDE 39 – TIPS EFEKTIF MENGGUNAKAN ROS

```
Buatkan konten slide berjudul "Tips dan Best Practices ROS" dengan:

Kategori A: Organisasi Kode
- Gunakan class-based node (bukan prosedural)
- Satu file = satu node
- Gunakan parameter untuk nilai yang mungkin berubah
- Beri nama topic yang deskriptif (/robot/cmd_vel bukan /cmd)

Kategori B: Debugging
- Gunakan rqt_graph untuk melihat koneksi
- rostopic echo untuk verifikasi data
- rospy.loginfo/logwarn/logerr untuk logging terstruktur
- roswtf untuk diagnosa otomatis

Kategori C: Performa
- queue_size=1 untuk data real-time (bukan queue besar)
- Jangan publish di dalam subscriber callback jika bisa dihindari
- Gunakan rospy.Rate untuk kontrol frekuensi yang tepat

Kategori D: Gazebo
- Mulai dengan world sederhana (tambah kompleksitas bertahap)
- Set <real_time_factor>1.0</real_time_factor> untuk simulasi real-time
- Gunakan <static>true</static> untuk objek yang tidak bergerak
```

---

### PROMPT SLIDE 40 – TROUBLESHOOTING UMUM ROS

```
Buatkan konten slide berjudul "Troubleshooting: Masalah Umum ROS dan Solusinya" dengan:

Format tabel: Masalah | Penyebab | Solusi

1. "Unable to connect to master"
   Penyebab: roscore belum berjalan
   Solusi: Terminal baru → roscore

2. "Cannot import rospy"
   Penyebab: ROS belum di-source
   Solusi: source /opt/ros/noetic/setup.bash

3. "Package not found"
   Penyebab: Package belum build atau belum source devel
   Solusi: catkin_make && source devel/setup.bash

4. "Topic tidak ada data"
   Penyebab: Publisher belum jalan atau nama topic salah
   Solusi: rosnode list, rostopic list, cek nama topic

5. Robot tidak bergerak di Gazebo
   Penyebab: Plugin diff_drive salah konfigurasi
   Solusi: Cek nama joint di plugin = nama joint di URDF

6. RViz: "No transform from [base_link] to [odom]"
   Penyebab: robot_state_publisher tidak jalan
   Solusi: Jalankan robot_state_publisher di launch file

7. Gazebo crash saat spawn
   Penyebab: URDF syntax error
   Solusi: check_urdf robot.urdf terlebih dahulu

Gunakan ikon ⚠️ untuk masalah dan ✅ untuk solusi.
```

---

### PROMPT SLIDE 41 – TROUBLESHOOTING GAZEBO

```
Buatkan konten slide berjudul "Troubleshooting Gazebo: Masalah Umum" dengan:

1. Gazebo berjalan sangat lambat:
   - Cek: htop → apakah CPU penuh?
   - Solusi: kurangi update_rate sensor
   - Solusi: gunakan <real_time_factor>0.5</real_time_factor>
   - Solusi: matikan visualisasi sensor

2. Robot "melayang" atau "tenggelam":
   - Penyebab: z-offset spawn tidak tepat
   - Solusi: spawn dengan z = wheel_radius + 0.01

3. Robot "bergetar" atau tidak stabil:
   - Penyebab: massa dan inersia tidak realistis
   - Solusi: hitung ulang inertia dari datasheet

4. Sensor tidak muncul di ROS:
   - Cek: rostopic list (apakah topic sensor ada?)
   - Solusi: pastikan plugin .so ada dan nama benar

5. Model tidak ditemukan saat spawn:
   - Penyebab: GAZEBO_MODEL_PATH tidak diset
   - Solusi: export GAZEBO_MODEL_PATH=~/catkin_ws/src/my_robot/models

6. Camera plugin tidak bekerja:
   - Cek: apakah rqt_image_view bisa dibuka?
   - Solusi: pastikan frameName di plugin sesuai nama link kamera
```

---

### PROMPT SLIDE 42 – RESOURCE DAN REFERENSI BELAJAR

```
Buatkan konten slide berjudul "Sumber Belajar ROS dan Gazebo" dengan:

Format tabel: Sumber | URL | Keterangan

Dokumentasi Resmi:
- ROS Wiki | wiki.ros.org | Referensi lengkap semua package
- ROS Answers | answers.ros.org | Forum Q&A komunitas
- Gazebo Tutorials | classic.gazebosim.org/tutorials | Tutorial step-by-step

Kursus Online:
- The Construct | theconstructsim.com | Kursus ROS terlengkap online
- ROS Robot Programming | edu.robotis.com | Buku + course gratis
- Udemy: ROS for Beginners | udemy.com | Pemula dengan contoh praktis

Video Tutorial:
- Robotics Back-End | YouTube | Tutorial ROS/Gazebo sangat jelas
- The Construct YouTube | YouTube | Channel resmi ROS
- Articulated Robotics | YouTube | Gazebo + ROS2

Package ROS:
- ROS Index | index.ros.org | Cari package ROS
- GitHub ros-planning | github.com/ros-planning | Navigation stack

Buku:
- Programming Robots with ROS (O'Reilly)
- ROS Robot Programming (ROBOTIS)
- Mastering ROS for Robotics Programming (Packt)
```

---

### PROMPT SLIDE 43 – EKOSISTEM ROS YANG LEBIH LUAS

```
Buatkan konten slide berjudul "Ekosistem ROS: Beyond the Basics" dengan:

1. ROS Navigation Stack:
   - move_base: perencanaan jalur
   - AMCL: localization
   - Costmap: representasi rintangan
   - Terhubung ke modul: ROS SLAM dan Navigasi (Modul 11)

2. MoveIt! (Robot Arm):
   - Motion planning untuk lengan robot
   - Collision avoidance
   - Terhubung ke modul: ROS Robot ARM (Modul 12)

3. ROS-Industrial:
   - Integrasi ROS dengan robot industri (ABB, KUKA, Fanuc)
   - Package untuk PLC dan komunikasi industri

4. ROS 2 (masa depan):
   - DDS middleware (lebih robust)
   - Real-time support
   - Tanpa rosmaster
   - Modul akan diupdate ke ROS 2 Humble

5. Kaitan antar modul:
   Modul 8 (ROS Dasar) → Modul 9 (Kinematika) → Modul 10 (OpenCV+YOLO) →
   Modul 11 (SLAM+Nav) → Modul 12 (Robot ARM)

Tampilkan roadmap pembelajaran ROS.
```

---

## BAGIAN 10: PENUTUP (Slide 44–45)

---

### PROMPT SLIDE 44 – RINGKASAN MODUL 08

```
Buatkan konten slide berjudul "Ringkasan: Yang Telah Dipelajari di Modul 08" dengan:

Format: daftar checklist terstruktur

✅ Konsep Dasar ROS:
   □ Arsitektur node-topic-service
   □ Publisher dan Subscriber
   □ Services dan Actions
   □ Parameter Server
   □ Launch Files

✅ Model Robot:
   □ URDF: mendefinisikan geometri robot
   □ Xacro: modularisasi URDF
   □ TF: sistem koordinat antar frame

✅ Visualisasi dan Simulasi:
   □ RViz: visualisasi 3D robot dan sensor
   □ Gazebo: simulasi fisika realistis
   □ Plugin: integrasi ROS-Gazebo

✅ Sensor Virtual:
   □ Lidar: data /scan
   □ Kamera: data /image_raw
   □ IMU: data /imu

✅ Tools dan Debugging:
   □ rqt_graph, rqt_plot
   □ rosbag record/play
   □ roswtf, rosnode, rostopic

Tambahkan kalimat penutup yang memotivasi.
```

---

### PROMPT SLIDE 45 – TUGAS DAN TINDAK LANJUT

```
Buatkan konten slide berjudul "Tugas dan Tindak Lanjut" dengan:

1. Tugas Individu (Jobsheet):
   - Selesaikan 20 percobaan di jobsheet
   - Isi semua tabel pengamatan dan analisa
   - Jawab semua pertanyaan analisis
   - Deadline: [sesuai jadwal dosen]

2. Tugas Video (Individual):
   - Screen record penjelasan materi + demo percobaan
   - Durasi: 15-25 menit
   - Format: MP4, minimal HD 720p
   - Upload ke platform yang ditentukan dosen

3. Project (Kelompok, maks 4 orang):
   - Pilih satu dari 10 opsi project
   - Kembangkan sistem robot otonom di Gazebo
   - Deliverables: source code + video demo + laporan
   - Presentasi di pertemuan 11-12

4. Persiapan Modul Berikutnya (Modul 09):
   - Pastikan ROS Noetic terinstall dan berjalan
   - Pahami konsep URDF dan TF
   - Install: sudo apt install ros-noetic-urdf-tutorial

5. Kontak Dosen/Asisten untuk Pertanyaan:
   [isi informasi kontak]

Format: 5 kotak dengan warna berbeda dan ikon yang relevan.
```

---

## CATATAN PENGGUNAAN PROMPT

### Tips Menggunakan Prompt Ini dengan NotebookLLM

1. **Upload materi.md terlebih dahulu** sebagai sumber NotebookLLM sebelum menggunakan prompt
2. **Gunakan prompt secara berurutan** dari Slide 1 hingga Slide 45
3. **Tambahkan konteks** jika diperlukan, contoh: "Tambahkan contoh untuk mahasiswa Teknologi Rekayasa Otomasi yang belajar di Indonesia"
4. **Iterasi output**: jika hasil kurang detail, tambahkan "Perluas penjelasan pada poin X" atau "Tambahkan contoh kode untuk poin Y"
5. **Sesuaikan dengan template** presentasi yang digunakan (PowerPoint, Google Slides, Canva)

### Struktur Slide yang Disarankan

| Elemen | Rekomendasi |
|--------|------------|
| Font judul | 32–40pt, Bold |
| Font konten | 20–24pt |
| Warna tema | Biru ROS (#22314E) + Orange (#FF6B35) |
| Gambar/diagram | 1 per slide minimum |
| Bullet maksimal | 6-7 poin per slide |
| Durasi per slide | 1.5–2 menit presentasi |

### Estimasi Waktu Presentasi

- Slide 1–5 (Pengantar): ~10 menit
- Slide 6–12 (Komponen Dasar): ~15 menit
- Slide 13–15 (Workspace): ~7 menit
- Slide 16–19 (TF/URDF): ~10 menit
- Slide 20–22 (RViz/rqt): ~8 menit
- Slide 23–30 (Gazebo): ~20 menit
- Slide 31–38 (Percobaan/Project): ~15 menit
- Slide 39–43 (Tips/Troubleshooting): ~10 menit
- Slide 44–45 (Penutup): ~5 menit
- **Total: ~100 menit (2 pertemuan)**

---

*Prompt ini disusun untuk menghasilkan materi presentasi Modul 08 ROS Dasar dan Gazebo.*  
*Program Studi Teknologi Rekayasa Otomasi | Versi 1.0 | 2026*
