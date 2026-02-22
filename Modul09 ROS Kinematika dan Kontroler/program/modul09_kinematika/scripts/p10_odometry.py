#!/usr/bin/env python3
"""
P10 - Odometri dari Encoder dengan rosserial
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Mempublish odometri robot diferensial dari data encoder.
Mengkonversi encoder ticks ke nav_msgs/Odometry dan mempublish TF.

Subscribe: /encoder_ticks (std_msgs/Int32MultiArray) [tick_left, tick_right]
Publish:   /odom (nav_msgs/Odometry)
           TF: odom -> base_link

Mode simulasi (jika tidak ada hardware):
  Encoder ticks disimulasikan dari /cmd_vel

Jalankan (mode hardware):
  rosrun rosserial_python serial_node.py /dev/ttyUSB0 _baud:=57600
  rosrun modul09_kinematika p10_odometry.py

Jalankan (mode simulasi):
  rosrun modul09_kinematika p10_odometry.py _sim:=true
  rostopic pub /cmd_vel geometry_msgs/Twist "linear: {x: 0.2}"
"""

import rospy
import math
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist


class OdometryNode:
    # Parameter robot (sesuaikan dengan robot fisik)
    WHEEL_RADIUS = 0.05          # meter
    WHEEL_BASE   = 0.20          # meter
    TICKS_PER_REV = 500          # encoder pulses per revolusi roda

    METERS_PER_TICK = (2 * math.pi * WHEEL_RADIUS) / TICKS_PER_REV

    def __init__(self):
        rospy.init_node("p10_odometry", anonymous=False)

        self.sim_mode = rospy.get_param("~sim", False)

        # State robot
        self.x     = 0.0
        self.y     = 0.0
        self.theta = 0.0

        # Encoder state
        self.prev_tick_left  = 0
        self.prev_tick_right = 0
        self.tick_left       = 0
        self.tick_right      = 0

        # Simulasi encoder dari cmd_vel
        self.sim_vl = 0.0
        self.sim_vr = 0.0

        # TF broadcaster
        self.br = tf.TransformBroadcaster()

        # Publishers
        self.odom_pub = rospy.Publisher("/odom", Odometry, queue_size=50)

        # Subscribers
        if self.sim_mode:
            rospy.Subscriber("/cmd_vel", Twist, self.cmdvel_callback)
            rospy.loginfo("P10: Mode simulasi aktif. Subscribe /cmd_vel")
        else:
            rospy.Subscriber("/encoder_ticks", Int32MultiArray,
                             self.encoder_callback)
            rospy.loginfo("P10: Mode hardware aktif. Subscribe /encoder_ticks")

        self.timer = rospy.Timer(rospy.Duration(0.02), self.odometry_loop)
        rospy.loginfo("P10: Odometry node aktif. Publish ke /odom")

    def cmdvel_callback(self, msg):
        """Simulasikan encoder dari cmd_vel."""
        v = msg.linear.x
        w = msg.angular.z
        R = self.WHEEL_RADIUS
        L = self.WHEEL_BASE
        self.sim_vr = (v + w * L / 2.0) / R  # rad/s
        self.sim_vl = (v - w * L / 2.0) / R  # rad/s

    def encoder_callback(self, msg):
        """Terima data encoder dari hardware (via rosserial)."""
        if len(msg.data) >= 2:
            self.tick_left  = msg.data[0]
            self.tick_right = msg.data[1]

    def odometry_loop(self, event):
        dt = 0.02  # 20ms

        if self.sim_mode:
            # Hitung delta ticks dari simulasi kecepatan roda
            dl = self.sim_vl * dt * self.TICKS_PER_REV / (2 * math.pi)
            dr = self.sim_vr * dt * self.TICKS_PER_REV / (2 * math.pi)
        else:
            dl = self.tick_left  - self.prev_tick_left
            dr = self.tick_right - self.prev_tick_right
            self.prev_tick_left  = self.tick_left
            self.prev_tick_right = self.tick_right

        # Konversi ticks ke meter
        dist_left  = dl * self.METERS_PER_TICK
        dist_right = dr * self.METERS_PER_TICK

        # Kinematika diferensial
        delta_s     = (dist_right + dist_left) / 2.0
        delta_theta = (dist_right - dist_left) / self.WHEEL_BASE

        # Update pose (integrasi Euler)
        self.x     += delta_s * math.cos(self.theta + delta_theta / 2.0)
        self.y     += delta_s * math.sin(self.theta + delta_theta / 2.0)
        self.theta += delta_theta
        # Normalisasi sudut
        self.theta  = math.atan2(math.sin(self.theta), math.cos(self.theta))

        now = rospy.Time.now()

        # Publish TF odom -> base_link
        q = tf.transformations.quaternion_from_euler(0, 0, self.theta)
        self.br.sendTransform(
            (self.x, self.y, 0),
            q,
            now,
            "base_link",
            "odom"
        )

        # Publish Odometry message
        odom = Odometry()
        odom.header.stamp    = now
        odom.header.frame_id = "odom"
        odom.child_frame_id  = "base_link"

        odom.pose.pose.position.x  = self.x
        odom.pose.pose.position.y  = self.y
        odom.pose.pose.orientation = Quaternion(*q)

        v_linear  = delta_s / dt
        v_angular = delta_theta / dt
        odom.twist.twist.linear.x  = v_linear
        odom.twist.twist.angular.z = v_angular

        # Diagonal covariance (simplified)
        odom.pose.covariance[0]  = 0.001
        odom.pose.covariance[7]  = 0.001
        odom.pose.covariance[35] = 0.01
        odom.twist.covariance[0]  = 0.001
        odom.twist.covariance[35] = 0.01

        self.odom_pub.publish(odom)

        rospy.loginfo_throttle(
            2.0,
            f"P10: x={self.x:.3f}m  y={self.y:.3f}m  "
            f"θ={math.degrees(self.theta):.1f}°"
        )


def main():
    node = OdometryNode()
    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
