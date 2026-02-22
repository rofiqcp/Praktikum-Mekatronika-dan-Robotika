#!/usr/bin/env python3
"""
P09 - Go-to-Goal Controller untuk Robot Mobile
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Robot mobile bergerak secara otonom menuju koordinat tujuan
menggunakan proportional go-to-goal controller.

Subscribe: /odom (nav_msgs/Odometry)
           /goal  (geometry_msgs/Point)
Publish:   /cmd_vel (geometry_msgs/Twist)

Jalankan:
  Terminal 1: roscore
  Terminal 2: roslaunch modul09_kinematika p09_go_to_goal.launch
  Terminal 3: rosrun modul09_kinematika p09_go_to_goal.py
  Terminal 4: rostopic pub /goal geometry_msgs/Point "x: 2.0 y: 1.5 z: 0.0"
"""

import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Point
from tf.transformations import euler_from_quaternion


class GoToGoalController:
    # Gain kontroler
    K_RHO = 0.5    # gain kecepatan linear (fungsi jarak)
    K_ALPHA = 1.5  # gain kecepatan angular (fungsi error heading)

    # Batas kecepatan
    V_MAX = 0.3    # m/s
    W_MAX = 1.0    # rad/s

    # Threshold berhenti
    DIST_THRESH = 0.05   # meter

    def __init__(self):
        rospy.init_node("p09_go_to_goal", anonymous=False)

        # State robot
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Target
        self.goal_x = None
        self.goal_y = None

        # Subscribers dan Publishers
        rospy.Subscriber("/odom", Odometry, self.odom_callback)
        rospy.Subscriber("/goal", Point, self.goal_callback)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

        self.rate = rospy.Rate(20)  # 20 Hz
        rospy.loginfo("P09: Go-to-Goal Controller aktif.")
        rospy.loginfo("     Kirim target: rostopic pub /goal geometry_msgs/Point "
                      "'x: 2.0 y: 1.5 z: 0.0'")

    def odom_callback(self, msg):
        """Update pose robot dari odometri."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        _, _, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])
        self.theta = yaw

    def goal_callback(self, msg):
        """Terima tujuan baru."""
        self.goal_x = msg.x
        self.goal_y = msg.y
        rospy.loginfo(f"P09: Target baru → ({self.goal_x:.2f}, {self.goal_y:.2f})")

    def normalize_angle(self, angle):
        """Normalisasi sudut ke rentang (-pi, pi]."""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle <= -math.pi:
            angle += 2 * math.pi
        return angle

    def control(self):
        """Hitung dan publish perintah kecepatan."""
        if self.goal_x is None:
            return

        dx = self.goal_x - self.x
        dy = self.goal_y - self.y
        rho = math.sqrt(dx**2 + dy**2)

        # Cek apakah sudah sampai
        if rho < self.DIST_THRESH:
            rospy.loginfo(f"P09: ✓ Tiba di tujuan! Pose=({self.x:.3f},{self.y:.3f}), "
                          f"error={rho:.4f}m")
            self.cmd_pub.publish(Twist())  # berhenti
            self.goal_x = None
            return

        # Sudut ke tujuan
        angle_to_goal = math.atan2(dy, dx)
        alpha = self.normalize_angle(angle_to_goal - self.theta)

        # Hitung kecepatan
        v = min(self.K_RHO * rho, self.V_MAX)
        w = max(-self.W_MAX, min(self.W_MAX, self.K_ALPHA * alpha))

        # Kurangi kecepatan linear jika error sudut besar
        if abs(alpha) > math.pi / 4:
            v = v * 0.3

        cmd = Twist()
        cmd.linear.x = v
        cmd.angular.z = w
        self.cmd_pub.publish(cmd)

        rospy.loginfo_throttle(
            1.0,
            f"P09: dist={rho:.3f}m  alpha={math.degrees(alpha):.1f}°  "
            f"v={v:.3f}  w={w:.3f}"
        )

    def run(self):
        while not rospy.is_shutdown():
            self.control()
            self.rate.sleep()


def main():
    node = GoToGoalController()
    node.run()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
