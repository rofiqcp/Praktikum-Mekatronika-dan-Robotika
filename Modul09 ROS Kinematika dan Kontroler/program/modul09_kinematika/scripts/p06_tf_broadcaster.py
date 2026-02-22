#!/usr/bin/env python3
"""
P06 - TF Broadcaster di ROS Python
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Mempublish transformasi antar frame koordinat menggunakan TF ROS.
Frame hierarchy:
  world -> link1 -> link2

Sudut joint berubah secara sinusoidal seiring waktu.
Jalankan: rosrun modul09_kinematika p06_tf_broadcaster.py
Visualisasi: buka RViz, tambahkan TF display, set Fixed Frame = world
"""

import rospy
import tf
import tf.transformations
import math


def main():
    rospy.init_node("p06_tf_broadcaster", anonymous=False)
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(50)  # 50 Hz

    rospy.loginfo("P06: TF Broadcaster started. Visualize in RViz (Fixed Frame: world)")

    # Parameter robot
    L1 = 0.5   # panjang lengan 1
    L2 = 0.3   # panjang lengan 2

    t_start = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():
        t = rospy.Time.now().to_sec() - t_start

        # Sudut joint berubah sinusoidal
        theta1 = math.radians(45) * math.sin(0.5 * t)       # -45° ~ +45°
        theta2 = math.radians(30) * math.sin(0.3 * t + 1.0)  # -30° ~ +30°

        now = rospy.Time.now()

        # Transformasi: world -> link1
        # Rotasi sekitar sumbu Z sebesar theta1
        q1 = tf.transformations.quaternion_from_euler(0, 0, theta1)
        br.sendTransform(
            translation=(0, 0, 0),   # origin di world
            rotation=q1,
            time=now,
            child="link1",
            parent="world"
        )

        # Transformasi: link1 -> link2
        # Translasi L1 ke arah X, rotasi sekitar Z sebesar theta2
        q2 = tf.transformations.quaternion_from_euler(0, 0, theta2)
        br.sendTransform(
            translation=(L1, 0, 0),  # ujung lengan 1
            rotation=q2,
            time=now,
            child="link2",
            parent="link1"
        )

        # Transformasi: link2 -> end_effector
        # Translasi L2 ke arah X
        q_ident = tf.transformations.quaternion_from_euler(0, 0, 0)
        br.sendTransform(
            translation=(L2, 0, 0),  # ujung lengan 2
            rotation=q_ident,
            time=now,
            child="end_effector",
            parent="link2"
        )

        rospy.loginfo_throttle(
            2.0,
            f"θ₁={math.degrees(theta1):.1f}°  θ₂={math.degrees(theta2):.1f}°"
        )

        rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
