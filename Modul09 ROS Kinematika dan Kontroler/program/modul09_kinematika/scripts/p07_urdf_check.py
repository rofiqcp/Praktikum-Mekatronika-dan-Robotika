#!/usr/bin/env python3
"""
P07 - URDF Robot Check (tanpa hardware)
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Script helper untuk verifikasi URDF robot difensial.
Launch URDF visualization menggunakan launch file:
  roslaunch modul09_kinematika p07_urdf.launch

Script ini hanya mencetak petunjuk penggunaan.
"""

import subprocess
import os
import sys


def main():
    print("=" * 65)
    print("P07 - URDF Robot Sederhana - Petunjuk")
    print("=" * 65)
    print("""
Untuk memvisualisasikan URDF robot di RViz:

  Terminal 1 (roscore):
    roscore

  Terminal 2 (launch robot + RViz):
    roslaunch modul09_kinematika p07_urdf.launch

Perintah berguna lainnya:
  # Lihat TF tree:
    rosrun tf view_frames
    rosrun rqt_tf_tree rqt_tf_tree

  # Verifikasi URDF:
    rosrun urdfdom check_urdf /path/to/robot.urdf

  # Tampilkan joint states:
    rostopic echo /joint_states

Deskripsi URDF yang dibuat:
  - base_link      : body utama robot (box 0.3 x 0.2 x 0.1 m)
  - left_wheel     : roda kiri (silinder, r=0.05m)
  - right_wheel    : roda kanan (silinder, r=0.05m)
  - laser_link     : frame sensor LiDAR (di atas body)

TF Tree yang diharapkan:
  odom
    └── base_link
          ├── left_wheel   (joint: continuous, axis Y)
          ├── right_wheel  (joint: continuous, axis Y)
          └── laser_link   (joint: fixed)
""")

    # Cek apakah URDF file ada
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_dir = os.path.join(script_dir, "..", "urdf")
    urdf_file = os.path.join(urdf_dir, "diff_robot.urdf.xacro")

    if os.path.exists(urdf_file):
        print(f"  ✓ URDF file ditemukan: {urdf_file}")
    else:
        print(f"  ⚠ URDF file tidak ditemukan: {urdf_file}")
        print("    Pastikan file urdf/diff_robot.urdf.xacro ada di package.")


if __name__ == "__main__":
    main()
