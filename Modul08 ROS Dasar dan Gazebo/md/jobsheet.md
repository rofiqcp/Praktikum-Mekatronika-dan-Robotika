# JOBSHEET MODUL 08: ROS DASAR DAN GAZEBO

**Program Studi:** Teknologi Rekayasa Otomasi  
**Mata Kuliah:** Praktikum Mekatronika dan Robotika  
**Modul:** 08 – ROS Dasar dan Gazebo  
**Software:** ROS Noetic, Gazebo 11  
**OS:** Ubuntu 20.04 LTS  
**Pertemuan:** 1–7 (7 × 3 SKS)  
**Nama:** ___________________ **NIM:** ___________________  
**Tanggal:** ___________________ **Kelompok:** ___________________

---

## A. TUJUAN PRAKTIKUM

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menginstal dan mengkonfigurasi ROS Noetic pada Ubuntu 20.04
2. Membuat dan mengelola catkin workspace dan ROS package
3. Membuat node publisher dan subscriber menggunakan Python
4. Menggunakan services untuk komunikasi request-response
5. Mengkonfigurasi parameter server dan membuat launch files
6. Membuat model robot dengan URDF dan Xacro
7. Memvisualisasikan robot dan data sensor menggunakan RViz
8. Menjalankan simulasi robot di Gazebo dengan world custom
9. Mengintegrasikan plugin sensor (laser, kamera, IMU) di Gazebo
10. Mengimplementasikan algoritma wall avoidance sederhana

---

## B. CPMK (CAPAIAN PEMBELAJARAN MATA KULIAH)

| Kode | Capaian Pembelajaran |
|------|---------------------|
| CPMK-1 | Mampu menginstal, mengkonfigurasi, dan menjalankan ROS Noetic |
| CPMK-2 | Mampu membuat node ROS dengan komunikasi topics dan services |
| CPMK-3 | Mampu membuat model robot URDF/Xacro dan memvisualisasikannya |
| CPMK-4 | Mampu menjalankan dan mengkonfigurasi simulasi robot di Gazebo |
| CPMK-5 | Mampu mengintegrasikan sensor virtual dan algoritma kontrol dasar |

---

## C. ALAT DAN BAHAN

| No | Perangkat/Software | Versi/Spesifikasi | Fungsi |
|----|-------------------|------------------|--------|
| 1 | Ubuntu | 20.04 LTS | Sistem Operasi |
| 2 | ROS Noetic | 1.16.x | Framework Robot |
| 3 | Gazebo | 11.x | Simulator |
| 4 | Python | 3.8+ | Bahasa Pemrograman |
| 5 | RViz | 1.14.x | Visualisasi |
| 6 | VS Code / nano | — | Text Editor |
| 7 | Terminal | — | Command Line |
| 8 | rqt | — | GUI Tools |

**Spesifikasi Komputer Minimum:**
- CPU: Intel Core i5 / AMD Ryzen 5 (4 core)
- RAM: 8 GB (disarankan 16 GB)
- Storage: 20 GB kosong
- GPU: Dedicated GPU disarankan untuk Gazebo

---

## D. DASAR TEORI SINGKAT

ROS (Robot Operating System) adalah framework middleware untuk pengembangan perangkat lunak robot. ROS menyediakan abstraksi hardware, driver perangkat, library, tools visualisasi (RViz), dan komunikasi antar proses melalui mekanisme publish-subscribe (topics) dan request-response (services).

**Gazebo** adalah simulator robot 3D open-source yang menyediakan fisika realistis, rendering 3D, dan simulasi sensor. Integrasi ROS-Gazebo memungkinkan pengembangan dan pengujian algoritma robot sebelum diimplementasikan pada hardware nyata.

---

## E. 20 PERCOBAAN PRAKTIKUM

---

### PERCOBAAN 1: INSTALASI ROS NOETIC

**Tujuan:** Menginstal ROS Noetic pada Ubuntu 20.04 dan memverifikasi instalasi.

**Langkah Kerja:**

```bash
# 1. Setup sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu focal main" \
  > /etc/apt/sources.list.d/ros-latest.list'

# 2. Setup keys
sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc \
  | sudo apt-key add -

# 3. Install ROS Noetic Desktop Full
sudo apt update
sudo apt install ros-noetic-desktop-full -y

# 4. Setup environment
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 5. Install tools
sudo apt install python3-rosdep python3-rosinstall build-essential -y
sudo rosdep init && rosdep update
```

**Verifikasi:**
```bash
rosversion -d        # Output: noetic
echo $ROS_DISTRO     # Output: noetic
roscore &            # Harus berjalan tanpa error
```

**Tabel Pengamatan 1:**

| Perintah | Output yang Diperoleh | Status |
|---------|----------------------|--------|
| `rosversion -d` | | ☐ Berhasil ☐ Gagal |
| `echo $ROS_DISTRO` | | ☐ Berhasil ☐ Gagal |
| `roscore` | | ☐ Berhasil ☐ Gagal |

---

### PERCOBAAN 2: SETUP CATKIN WORKSPACE

**Tujuan:** Membuat catkin workspace dan package ROS pertama.

**Langkah Kerja:**

```bash
# 1. Buat workspace
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make

# 2. Source workspace
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 3. Buat package baru
cd ~/catkin_ws/src
catkin_create_pkg praktikum_ros rospy std_msgs geometry_msgs sensor_msgs

# 4. Build workspace
cd ~/catkin_ws
catkin_make

# 5. Verifikasi
rospack list | grep praktikum_ros
```

**Tabel Pengamatan 2:**

| Item | Hasil |
|------|-------|
| Direktori catkin_ws terbuat | ☐ Ya ☐ Tidak |
| catkin_make berhasil | ☐ Ya ☐ Tidak |
| Package praktikum_ros ditemukan | ☐ Ya ☐ Tidak |
| Isi direktori package | |

---

### PERCOBAAN 3: PUBLISHER DAN SUBSCRIBER PERTAMA

**Tujuan:** Membuat node publisher dan subscriber yang saling berkomunikasi.

**Langkah Kerja:**

```bash
cd ~/catkin_ws/src/praktikum_ros/src
```

Buat file `talker.py`:
```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(1)
    counter = 0
    while not rospy.is_shutdown():
        msg = "Hello ROS! Pesan ke-%d" % counter
        rospy.loginfo(msg)
        pub.publish(msg)
        counter += 1
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
```

Buat file `listener.py`:
```python
#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("Diterima: %s", data.data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('chatter', String, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
```

```bash
# Beri izin eksekusi
chmod +x talker.py listener.py

# Terminal 1: roscore
# Terminal 2: rosrun praktikum_ros talker.py
# Terminal 3: rosrun praktikum_ros listener.py
# Terminal 4: rostopic echo /chatter
```

**Tabel Pengamatan 3:**

| Observasi | Hasil |
|-----------|-------|
| Pesan pertama yang dikirim talker | |
| Pesan diterima listener | |
| Frekuensi topic /chatter (Hz) | |
| Output rostopic echo | |

---

### PERCOBAAN 4: CUSTOM MESSAGE

**Tujuan:** Membuat tipe pesan kustom dan menggunakannya.

**Langkah Kerja:**

```bash
mkdir -p ~/catkin_ws/src/praktikum_ros/msg
```

Buat `msg/SensorData.msg`:
```
float32 temperature
float32 humidity
int32 timestamp
string sensor_id
```

Edit `CMakeLists.txt` (tambahkan):
```cmake
find_package(catkin REQUIRED COMPONENTS
  rospy std_msgs message_generation
)
add_message_files(FILES SensorData.msg)
generate_messages(DEPENDENCIES std_msgs)
```

Edit `package.xml` (tambahkan):
```xml
<build_depend>message_generation</build_depend>
<exec_depend>message_runtime</exec_depend>
```

```bash
cd ~/catkin_ws && catkin_make
source devel/setup.bash
rosmsg show praktikum_ros/SensorData
```

**Tabel Pengamatan 4:**

| Item | Hasil |
|------|-------|
| Output `rosmsg show SensorData` | |
| Field yang tersedia | |
| catkin_make berhasil | ☐ Ya ☐ Tidak |

---

### PERCOBAAN 5: PUBLISH DAN SUBSCRIBE CUSTOM MESSAGE

**Tujuan:** Menggunakan custom message SensorData untuk komunikasi.

**Langkah Kerja:**

Buat `sensor_publisher.py`:
```python
#!/usr/bin/env python3
import rospy
import random
from praktikum_ros.msg import SensorData

def sensor_pub():
    pub = rospy.Publisher('/sensor_data', SensorData, queue_size=10)
    rospy.init_node('sensor_publisher')
    rate = rospy.Rate(2)
    while not rospy.is_shutdown():
        msg = SensorData()
        msg.temperature = 25.0 + random.uniform(-2, 2)
        msg.humidity = 60.0 + random.uniform(-5, 5)
        msg.timestamp = int(rospy.Time.now().to_sec())
        msg.sensor_id = "sensor_01"
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    sensor_pub()
```

**Tabel Pengamatan 5:**

| Observasi | Nilai |
|-----------|-------|
| Nilai temperature yang diterima | |
| Nilai humidity yang diterima | |
| Frekuensi topic /sensor_data | Hz |

---

### PERCOBAAN 6: SERVICE SERVER DAN CLIENT

**Tujuan:** Membuat dan menggunakan ROS service.

**Langkah Kerja:**

Buat `srv/ResetCounter.srv`:
```
bool confirm
---
bool success
int32 final_count
string message
```

Buat `counter_server.py`:
```python
#!/usr/bin/env python3
import rospy
from praktikum_ros.srv import ResetCounter, ResetCounterResponse

counter = 0

def handle_reset(req):
    global counter
    if req.confirm:
        old_count = counter
        counter = 0
        return ResetCounterResponse(True, old_count, "Counter direset!")
    return ResetCounterResponse(False, counter, "Reset dibatalkan")

rospy.init_node('counter_server')
rospy.Service('/reset_counter', ResetCounter, handle_reset)
rospy.loginfo("Counter server siap")
rospy.spin()
```

```bash
# Test service:
rosservice call /reset_counter "confirm: true"
```

**Tabel Pengamatan 6:**

| Test | Response |
|------|---------|
| Call dengan confirm=true | |
| Call dengan confirm=false | |

---

### PERCOBAAN 7: PARAMETER SERVER

**Tujuan:** Menggunakan parameter server untuk konfigurasi node.

**Langkah Kerja:**

Buat `param_demo.py`:
```python
#!/usr/bin/env python3
import rospy

rospy.init_node('param_demo')
robot_name = rospy.get_param('~robot_name', 'robot_default')
max_speed   = rospy.get_param('~max_speed', 1.0)
rate_hz     = rospy.get_param('~rate', 5)

rospy.loginfo("Robot: %s | MaxSpeed: %.1f | Rate: %d Hz"
              % (robot_name, max_speed, rate_hz))

rate = rospy.Rate(rate_hz)
while not rospy.is_shutdown():
    rospy.loginfo("Berjalan dengan kecepatan max %.1f m/s" % max_speed)
    rate.sleep()
```

```bash
# Jalankan dengan parameter custom:
rosrun praktikum_ros param_demo.py _robot_name:=robot_01 _max_speed:=0.5

# Ubah parameter saat berjalan:
rosparam set /param_demo/max_speed 1.5
rosparam get /param_demo/max_speed
```

**Tabel Pengamatan 7:**

| Parameter | Nilai Default | Nilai Custom |
|-----------|--------------|-------------|
| robot_name | robot_default | |
| max_speed | 1.0 | |
| rate | 5 | |

---

### PERCOBAAN 8: LAUNCH FILE

**Tujuan:** Membuat launch file untuk menjalankan multiple nodes sekaligus.

**Langkah Kerja:**

```bash
mkdir -p ~/catkin_ws/src/praktikum_ros/launch
```

Buat `launch/sensor_system.launch`:
```xml
<launch>
  <arg name="robot_name" default="robot_01"/>
  <arg name="max_speed" default="0.5"/>

  <param name="use_sim_time" value="false"/>

  <node pkg="praktikum_ros" type="sensor_publisher.py"
        name="sensor_node" output="screen">
    <param name="sensor_id" value="$(arg robot_name)_sensor"/>
  </node>

  <node pkg="praktikum_ros" type="counter_server.py"
        name="counter_server" output="screen"/>

  <node pkg="praktikum_ros" type="param_demo.py"
        name="param_demo" output="screen">
    <param name="robot_name" value="$(arg robot_name)"/>
    <param name="max_speed" value="$(arg max_speed)"/>
  </node>
</launch>
```

```bash
roslaunch praktikum_ros sensor_system.launch
roslaunch praktikum_ros sensor_system.launch robot_name:=robot_02
rosnode list
```

**Tabel Pengamatan 8:**

| Node Aktif | Status |
|------------|--------|
| /sensor_node | ☐ Jalan ☐ Tidak |
| /counter_server | ☐ Jalan ☐ Tidak |
| /param_demo | ☐ Jalan ☐ Tidak |

---

### PERCOBAAN 9: MEMBUAT URDF ROBOT

**Tujuan:** Membuat file URDF untuk robot differential drive sederhana.

**Langkah Kerja:**

```bash
mkdir -p ~/catkin_ws/src/praktikum_ros/urdf
```

Buat `urdf/diff_robot.urdf` dengan struktur:
- base_link (kotak 0.3×0.2×0.1 m, biru)
- wheel_left (silinder r=0.05, panjang=0.03, hitam)
- wheel_right (sama dengan wheel_left)
- laser_link (silinder kecil, merah)

```bash
# Verifikasi URDF
sudo apt install liburdfdom-tools -y
check_urdf ~/catkin_ws/src/praktikum_ros/urdf/diff_robot.urdf

# Tampilkan di RViz
roslaunch urdf_tutorial display.launch \
  model:=$(rospack find praktikum_ros)/urdf/diff_robot.urdf
```

**Tabel Pengamatan 9:**

| Item | Hasil |
|------|-------|
| Output check_urdf | |
| Jumlah links | |
| Jumlah joints | |
| Robot tampil di RViz | ☐ Ya ☐ Tidak |

---

### PERCOBAAN 10: XACRO

**Tujuan:** Mengkonversi URDF ke Xacro dengan macro untuk komponen berulang.

**Langkah Kerja:**

```bash
mkdir -p ~/catkin_ws/src/praktikum_ros/urdf
```

Buat `urdf/diff_robot.urdf.xacro` dengan property dan macro untuk roda:
```xml
<?xml version="1.0"?>
<robot name="diff_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <xacro:property name="wheel_radius" value="0.05"/>
  <xacro:property name="wheel_width"  value="0.03"/>
  <xacro:property name="wheel_sep"    value="0.23"/>

  <xacro:macro name="wheel" params="prefix y_reflect">
    <link name="${prefix}_wheel">
      <visual>
        <origin xyz="0 0 0" rpy="1.5707 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </visual>
      <collision>
        <origin xyz="0 0 0" rpy="1.5707 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.2"/>
        <inertia ixx="0.0002" ixy="0" ixz="0"
                 iyy="0.0002" iyz="0" izz="0.0001"/>
      </inertial>
    </link>
    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="base_link"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="0 ${y_reflect * wheel_sep/2} 0"/>
      <axis xyz="0 1 0"/>
    </joint>
  </xacro:macro>

  <xacro:wheel prefix="left"  y_reflect="1"/>
  <xacro:wheel prefix="right" y_reflect="-1"/>
</robot>
```

```bash
# Konversi ke URDF biasa
xacro urdf/diff_robot.urdf.xacro > /tmp/robot_expanded.urdf
check_urdf /tmp/robot_expanded.urdf
```

**Tabel Pengamatan 10:**

| Item | Jumlah Baris | Status |
|------|-------------|--------|
| File .urdf biasa | | |
| File .urdf.xacro | | Lebih pendek? ☐ Ya |
| Hasil check_urdf | | ☐ Pass |

---

### PERCOBAAN 11: RVIZ VISUALISASI

**Tujuan:** Menampilkan model robot dan data TF di RViz.

**Langkah Kerja:**

Buat `launch/rviz_demo.launch`:
```xml
<launch>
  <param name="robot_description"
         command="xacro $(find praktikum_ros)/urdf/diff_robot.urdf.xacro"/>

  <node name="robot_state_publisher"
        pkg="robot_state_publisher"
        type="robot_state_publisher" output="screen"/>

  <node name="joint_state_publisher_gui"
        pkg="joint_state_publisher_gui"
        type="joint_state_publisher_gui"/>

  <node name="rviz" pkg="rviz" type="rviz"
        args="-d $(find praktikum_ros)/rviz/robot.rviz"/>
</launch>
```

```bash
# Install dependensi
sudo apt install ros-noetic-joint-state-publisher-gui -y

roslaunch praktikum_ros rviz_demo.launch
# Di RViz: Add → RobotModel
# Di RViz: Add → TF
```

**Tabel Pengamatan 11:**

| Display | Status |
|---------|--------|
| RobotModel tampil | ☐ Ya ☐ Tidak |
| TF frames tampil | ☐ Ya ☐ Tidak |
| Nama frames TF yang muncul | |
| Joint bisa digerakkan dari GUI | ☐ Ya ☐ Tidak |

---

### PERCOBAAN 12: SETUP WORLD GAZEBO

**Tujuan:** Membuat world file Gazebo dengan arena sederhana.

**Langkah Kerja:**

```bash
mkdir -p ~/catkin_ws/src/praktikum_ros/worlds
```

Buat `worlds/arena.world` berisi lantai + 4 dinding membentuk kotak 6×6 meter:
```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <world name="arena">
    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    <model name="wall_north">
      <static>true</static>
      <pose>0 3 0.5 0 0 0</pose>
      <link name="link">
        <collision name="col">
          <geometry><box><size>6 0.1 1</size></box></geometry>
        </collision>
        <visual name="vis">
          <geometry><box><size>6 0.1 1</size></box></geometry>
          <material><ambient>0.5 0.5 0.5 1</ambient></material>
        </visual>
      </link>
    </model>
    <!-- Tambahkan wall_south, wall_east, wall_west dengan cara serupa -->
  </world>
</sdf>
```

```bash
# Buka Gazebo dengan world ini
roslaunch gazebo_ros empty_world.launch \
  world_name:=$(rospack find praktikum_ros)/worlds/arena.world
```

**Tabel Pengamatan 12:**

| Item | Hasil |
|------|-------|
| Gazebo berhasil dibuka | ☐ Ya ☐ Tidak |
| Lantai terlihat | ☐ Ya ☐ Tidak |
| Dinding terlihat (jumlah) | |
| Ukuran arena (perkiraan) | m × m |

---

### PERCOBAAN 13: SPAWN ROBOT DI GAZEBO

**Tujuan:** Menampilkan robot URDF di dalam simulasi Gazebo.

**Langkah Kerja:**

Tambahkan Gazebo plugin ke `diff_robot.urdf.xacro`:
```xml
<!-- Gazebo colors -->
<gazebo reference="base_link">
  <material>Gazebo/Blue</material>
</gazebo>
<gazebo reference="left_wheel">
  <material>Gazebo/Black</material>
</gazebo>
```

Buat `launch/gazebo_robot.launch`:
```xml
<launch>
  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name"
         value="$(find praktikum_ros)/worlds/arena.world"/>
    <arg name="paused" value="false"/>
    <arg name="use_sim_time" value="true"/>
  </include>

  <param name="robot_description"
         command="xacro $(find praktikum_ros)/urdf/diff_robot.urdf.xacro"/>

  <node name="spawn_robot" pkg="gazebo_ros" type="spawn_model"
        args="-urdf -model diff_robot -param robot_description
              -x 0 -y 0 -z 0.06"
        output="screen"/>

  <node name="robot_state_publisher"
        pkg="robot_state_publisher"
        type="robot_state_publisher"/>
</launch>
```

```bash
roslaunch praktikum_ros gazebo_robot.launch
rosnode list
rostopic list
```

**Tabel Pengamatan 13:**

| Item | Hasil |
|------|-------|
| Robot muncul di Gazebo | ☐ Ya ☐ Tidak |
| Topic /odom tersedia | ☐ Ya ☐ Tidak |
| Topic /tf tersedia | ☐ Ya ☐ Tidak |
| Posisi robot awal (x,y,z) | |

---

### PERCOBAAN 14: DIFFERENTIAL DRIVE PLUGIN

**Tujuan:** Mengontrol robot dengan plugin differential drive dan cmd_vel.

**Langkah Kerja:**

Tambahkan plugin ke `diff_robot.urdf.xacro`:
```xml
<gazebo>
  <plugin name="diff_drive" filename="libgazebo_ros_diff_drive.so">
    <commandTopic>cmd_vel</commandTopic>
    <odometryTopic>odom</odometryTopic>
    <odometryFrame>odom</odometryFrame>
    <robotBaseFrame>base_link</robotBaseFrame>
    <leftJoint>left_wheel_joint</leftJoint>
    <rightJoint>right_wheel_joint</rightJoint>
    <wheelSeparation>0.23</wheelSeparation>
    <wheelDiameter>0.10</wheelDiameter>
    <wheelAcceleration>1.0</wheelAcceleration>
    <updateRate>50</updateRate>
    <publishOdomTF>true</publishOdomTF>
  </plugin>
</gazebo>
```

```bash
roslaunch praktikum_ros gazebo_robot.launch

# Uji maju lurus
rostopic pub /cmd_vel geometry_msgs/Twist \
  "{linear: {x: 0.3, y: 0, z: 0}, angular: {x: 0, y: 0, z: 0}}" -r 10

# Uji belok kiri
rostopic pub /cmd_vel geometry_msgs/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.5}}" -r 10

# Teleop
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

**Tabel Pengamatan 14:**

| Perintah | Perilaku Robot |
|---------|---------------|
| linear.x = 0.3 | |
| linear.x = -0.3 | |
| angular.z = 0.5 | |
| angular.z = -0.5 | |
| Odometri saat maju 1m | x≈ y≈ |

---

### PERCOBAAN 15: SENSOR LASER DI GAZEBO

**Tujuan:** Menambahkan sensor laser ke robot dan membaca datanya.

**Langkah Kerja:**

Tambahkan link dan joint laser ke xacro, lalu tambahkan plugin sensor:
```xml
<gazebo reference="laser_link">
  <sensor type="ray" name="laser">
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.10</min>
        <max>10.0</max>
      </range>
    </ray>
    <plugin name="laser_plugin" filename="libgazebo_ros_laser.so">
      <topicName>/scan</topicName>
      <frameName>laser_link</frameName>
    </plugin>
  </sensor>
</gazebo>
```

```bash
rostopic echo /scan/ranges | head -20
rostopic hz /scan

# Visualisasi di RViz:
# Add → LaserScan → topic: /scan
```

**Tabel Pengamatan 15:**

| Item | Nilai |
|------|-------|
| Frekuensi /scan (Hz) | |
| Jumlah elemen ranges[] | |
| Nilai minimum ranges (jarak terdekat) | m |
| Nilai saat depan kosong (~1m ke dinding) | m |

---

### PERCOBAAN 16: SIMULASI KAMERA

**Tujuan:** Menambahkan kamera ke robot dan menampilkan gambarnya.

**Langkah Kerja:**

Tambahkan link kamera ke xacro:
```xml
<link name="camera_link">
  <visual>
    <geometry><box size="0.02 0.05 0.02"/></geometry>
  </visual>
</link>
<joint name="camera_joint" type="fixed">
  <parent link="base_link"/>
  <child link="camera_link"/>
  <origin xyz="0.12 0 0.06"/>
</joint>

<gazebo reference="camera_link">
  <sensor type="camera" name="camera">
    <update_rate>15</update_rate>
    <camera>
      <horizontal_fov>1.3962634</horizontal_fov>
      <image><width>320</width><height>240</height></image>
      <clip><near>0.02</near><far>50</far></clip>
    </camera>
    <plugin name="camera_plugin" filename="libgazebo_ros_camera.so">
      <cameraName>camera</cameraName>
      <imageTopicName>image_raw</imageTopicName>
      <frameName>camera_link</frameName>
    </plugin>
  </sensor>
</gazebo>
```

```bash
sudo apt install ros-noetic-rqt-image-view -y
rqt_image_view  # pilih /camera/image_raw
rostopic hz /camera/image_raw
```

**Tabel Pengamatan 16:**

| Item | Nilai |
|------|-------|
| Topic gambar | /camera/image_raw |
| Resolusi gambar | × pixel |
| Frekuensi (Hz) | |
| Gambar tampil di rqt_image_view | ☐ Ya ☐ Tidak |

---

### PERCOBAAN 17: SIMULASI IMU

**Tujuan:** Menambahkan sensor IMU dan membaca data orientasi robot.

**Langkah Kerja:**

Tambahkan IMU ke xacro:
```xml
<link name="imu_link"/>
<joint name="imu_joint" type="fixed">
  <parent link="base_link"/>
  <child link="imu_link"/>
  <origin xyz="0 0 0.05"/>
</joint>

<gazebo reference="imu_link">
  <gravity>true</gravity>
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>50</update_rate>
    <plugin filename="libgazebo_ros_imu_sensor.so" name="imu_plugin">
      <topicName>/imu</topicName>
      <bodyName>imu_link</bodyName>
      <updateRateHZ>50.0</updateRateHZ>
      <frameName>imu_link</frameName>
    </plugin>
  </sensor>
</gazebo>
```

```bash
rostopic echo /imu/data
```

**Tabel Pengamatan 17:**

| Field | Nilai saat Diam | Nilai saat Bergerak |
|-------|----------------|-------------------|
| orientation.z | | |
| orientation.w | | |
| angular_velocity.z | | |
| linear_acceleration.x | | |

---

### PERCOBAAN 18: WALL AVOIDANCE

**Tujuan:** Mengimplementasikan algoritma penghindaran dinding menggunakan data laser.

**Langkah Kerja:**

Buat `wall_avoider.py`:
```python
#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class WallAvoider:
    def __init__(self):
        rospy.init_node('wall_avoider')
        self.safe_dist = rospy.get_param('~safe_distance', 0.5)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber('/scan', LaserScan, self.laser_cb)
        self.min_dist = float('inf')

    def laser_cb(self, msg):
        valid = [r for r in msg.ranges if 0.05 < r < msg.range_max]
        self.min_dist = min(valid) if valid else float('inf')

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            cmd = Twist()
            if self.min_dist > self.safe_dist:
                cmd.linear.x = 0.3
            else:
                cmd.angular.z = 0.5
            self.pub.publish(cmd)
            rate.sleep()

if __name__ == '__main__':
    WallAvoider().run()
```

```bash
roslaunch praktikum_ros gazebo_robot.launch
rosrun praktikum_ros wall_avoider.py
```

**Tabel Pengamatan 18:**

| Skenario | Perilaku Robot |
|---------|---------------|
| Dinding di depan < 0.5m | |
| Tidak ada dinding (> 0.5m) | |
| Jebak di sudut | |
| Jarak safe_distance diubah ke 0.8m | |

---

### PERCOBAAN 19: ROSBAG RECORD DAN PLAY

**Tujuan:** Merekam dan memutar ulang data ROS menggunakan rosbag.

**Langkah Kerja:**

```bash
# Jalankan simulasi terlebih dahulu
roslaunch praktikum_ros gazebo_robot.launch &
rosrun praktikum_ros wall_avoider.py &

# Rekam selama 30 detik
mkdir -p ~/rosbag_data
cd ~/rosbag_data
rosbag record -O percobaan_19 /scan /odom /cmd_vel /tf --duration=30

# Lihat info
rosbag info percobaan_19.bag

# Hentikan robot
rostopic pub /cmd_vel geometry_msgs/Twist "{}" -r 1 &

# Putar ulang
rosbag play percobaan_19.bag

# Putar dengan setengah kecepatan
rosbag play -r 0.5 percobaan_19.bag
```

**Tabel Pengamatan 19:**

| Item | Nilai |
|------|-------|
| Durasi rekaman | detik |
| Ukuran file .bag | MB |
| Topics yang terekam | |
| Jumlah pesan /scan | |
| Jumlah pesan /odom | |
| Data identik saat replay | ☐ Ya ☐ Tidak |

---

### PERCOBAAN 20: INTEGRASI PENUH

**Tujuan:** Menggabungkan semua komponen menjadi sistem robot lengkap.

**Langkah Kerja:**

Buat `launch/full_demo.launch` yang menjalankan:
1. Gazebo dengan world arena
2. Robot dengan laser + kamera + IMU + diff_drive
3. robot_state_publisher
4. RViz dengan konfigurasi lengkap
5. wall_avoider node

```xml
<launch>
  <arg name="safe_distance" default="0.5"/>

  <include file="$(find gazebo_ros)/launch/empty_world.launch">
    <arg name="world_name"
         value="$(find praktikum_ros)/worlds/arena.world"/>
    <arg name="use_sim_time" value="true"/>
  </include>

  <param name="robot_description"
         command="xacro $(find praktikum_ros)/urdf/diff_robot.urdf.xacro"/>

  <node pkg="gazebo_ros" type="spawn_model" name="spawn_robot"
        args="-urdf -model diff_robot -param robot_description
              -x 0 -y 0 -z 0.06"/>

  <node pkg="robot_state_publisher" type="robot_state_publisher"
        name="robot_state_publisher"/>

  <node pkg="praktikum_ros" type="wall_avoider.py" name="wall_avoider"
        output="screen">
    <param name="safe_distance" value="$(arg safe_distance)"/>
  </node>

  <node pkg="rviz" type="rviz" name="rviz"
        args="-d $(find praktikum_ros)/rviz/full_demo.rviz"/>
</launch>
```

```bash
roslaunch praktikum_ros full_demo.launch
roslaunch praktikum_ros full_demo.launch safe_distance:=0.8
```

**Tabel Pengamatan 20:**

| Komponen | Status |
|---------|--------|
| Gazebo berjalan | ☐ Ya |
| Robot tampil di Gazebo | ☐ Ya |
| /scan topic aktif | ☐ Ya |
| /camera/image_raw aktif | ☐ Ya |
| /imu aktif | ☐ Ya |
| Robot bergerak otonom | ☐ Ya |
| RViz menampilkan data | ☐ Ya |

**Deskripsi perilaku robot selama 2 menit:**
```
_______________________________________________
_______________________________________________
```

---

## F. ANALISA

### F.1 Pertanyaan Analisis

1. **Jelaskan** perbedaan antara komunikasi menggunakan Topic dan Service di ROS. Kapan sebaiknya menggunakan masing-masing?

   **Jawaban:**
   _______________________________________________

2. **Mengapa** Xacro lebih disarankan daripada URDF biasa untuk robot yang memiliki komponen berulang? Berikan contoh konkret dari percobaan ini.

   **Jawaban:**
   _______________________________________________

3. **Jelaskan** peran Gazebo plugin dalam integrasi ROS-Gazebo. Apa yang terjadi jika plugin `libgazebo_ros_diff_drive.so` tidak ditambahkan ke URDF?

   **Jawaban:**
   _______________________________________________

4. **Bandingkan** data odometri dari plugin diff_drive dengan posisi robot sesungguhnya di Gazebo (ground truth). Apakah selalu akurat? Jelaskan faktor penyebab error.

   **Jawaban:**
   _______________________________________________

5. **Evaluasi** algoritma wall avoidance yang diimplementasikan di Percobaan 18. Apa kelemahannya dan bagaimana cara memperbaikinya?

   **Jawaban:**
   _______________________________________________

### F.2 Tabel Rekap Percobaan

| No | Percobaan | Berhasil | Catatan |
|----|-----------|---------|---------|
| 1 | Instalasi ROS | ☐ | |
| 2 | Catkin Workspace | ☐ | |
| 3 | Publisher-Subscriber | ☐ | |
| 4 | Custom Message | ☐ | |
| 5 | Publish Custom Msg | ☐ | |
| 6 | Service | ☐ | |
| 7 | Parameter Server | ☐ | |
| 8 | Launch File | ☐ | |
| 9 | URDF | ☐ | |
| 10 | Xacro | ☐ | |
| 11 | RViz | ☐ | |
| 12 | Gazebo World | ☐ | |
| 13 | Spawn Robot | ☐ | |
| 14 | Diff Drive | ☐ | |
| 15 | Sensor Laser | ☐ | |
| 16 | Kamera | ☐ | |
| 17 | IMU | ☐ | |
| 18 | Wall Avoidance | ☐ | |
| 19 | rosbag | ☐ | |
| 20 | Integrasi Penuh | ☐ | |

---

## G. KESIMPULAN

Tuliskan kesimpulan praktikum dalam 5 poin:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
4. _______________________________________________
5. _______________________________________________

---

## H. REFERENSI

1. ROS Wiki – ROS Noetic Documentation. http://wiki.ros.org/noetic
2. Gazebo Classic Tutorials. https://classic.gazebosim.org/tutorials
3. Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. ICRA Workshop.
4. Koenig, N., & Howard, A. (2004). Design and use paradigms for Gazebo. IEEE IROS.
5. Programming Robots with ROS. O'Reilly Media.

---

*Jobsheet ini merupakan dokumen resmi praktikum.*  
**Tanda Tangan Dosen/Asisten:** ___________________ **Tanggal:** ___________________
