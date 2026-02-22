#!/usr/bin/env python3
"""
P11 - ros_control Test: diff_drive_controller
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Script pengujian diff_drive_controller.
Mengirimkan sequence perintah kecepatan dan memverifikasi odometri.

Pastikan diff_drive_controller sudah berjalan:
  roslaunch modul09_kinematika p11_ros_control.launch
  rosservice call /controller_manager/list_controllers

Jalankan test:
  rosrun modul09_kinematika p11_ros_control_test.py
"""

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion


class RosControlTest:
    def __init__(self):
        rospy.init_node("p11_ros_control_test", anonymous=False)

        self.odom_x     = 0.0
        self.odom_y     = 0.0
        self.odom_theta = 0.0

        # Topik diff_drive_controller standar
        self.cmd_pub = rospy.Publisher(
            "/diff_drive_controller/cmd_vel", Twist, queue_size=10
        )
        rospy.Subscriber(
            "/diff_drive_controller/odom", Odometry, self.odom_callback
        )

        rospy.sleep(1.0)
        rospy.loginfo("P11: ros_control test dimulai")

    def odom_callback(self, msg):
        self.odom_x = msg.pose.pose.position.x
        self.odom_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        _, _, self.odom_theta = euler_from_quaternion([q.x, q.y, q.z, q.w])

    def send_velocity(self, v_linear, v_angular, duration_s):
        """Kirim kecepatan selama duration_s detik."""
        cmd = Twist()
        cmd.linear.x  = v_linear
        cmd.angular.z = v_angular
        rate = rospy.Rate(20)
        t_end = rospy.Time.now() + rospy.Duration(duration_s)
        while rospy.Time.now() < t_end and not rospy.is_shutdown():
            self.cmd_pub.publish(cmd)
            rate.sleep()
        self.cmd_pub.publish(Twist())  # stop

    def print_pose(self, label):
        rospy.loginfo(f"  [{label}] x={self.odom_x:.3f}m  "
                      f"y={self.odom_y:.3f}m  θ={math.degrees(self.odom_theta):.1f}°")

    def run_test_sequence(self):
        rospy.loginfo("=" * 55)
        rospy.loginfo("P11: Sequence Test diff_drive_controller")
        rospy.loginfo("=" * 55)

        self.print_pose("Awal")

        # Test 1: Maju 0.2 m/s selama 5 detik
        rospy.loginfo("Test 1: Maju lurus (v=0.2 m/s, 5s)...")
        self.send_velocity(0.2, 0.0, 5.0)
        rospy.sleep(0.5)
        self.print_pose("Setelah maju")

        # Test 2: Putar kiri 90 derajat
        rospy.loginfo("Test 2: Putar kiri 90° (w=0.5 rad/s)...")
        duration_rotate = (math.pi / 2.0) / 0.5  # waktu untuk 90 derajat
        self.send_velocity(0.0, 0.5, duration_rotate)
        rospy.sleep(0.5)
        self.print_pose("Setelah putar 90°")

        # Test 3: Maju lagi
        rospy.loginfo("Test 3: Maju lurus lagi (v=0.2 m/s, 5s)...")
        self.send_velocity(0.2, 0.0, 5.0)
        rospy.sleep(0.5)
        self.print_pose("Setelah maju kedua")

        rospy.loginfo("P11: Test selesai.")
        rospy.loginfo("     Cek output /diff_drive_controller/odom dengan:")
        rospy.loginfo("     rostopic echo /diff_drive_controller/odom")


def main():
    node = RosControlTest()
    node.run_test_sequence()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
