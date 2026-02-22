#!/usr/bin/env python3
"""
P15 - Integrasi Sistem Lengkap
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Sistem terintegrasi yang menggabungkan:
1. FK dari /joint_states
2. TF broadcaster (odom → base_link)
3. Go-to-Goal controller
4. Odometri dari encoder (simulasi)
5. Monitoring dan logging

Node ini bertindak sebagai supervisor yang mengorkestrasi semua komponen.

Subscribe: /joint_states (sensor_msgs/JointState)
           /odom         (nav_msgs/Odometry)
Publish:   /cmd_vel      (geometry_msgs/Twist)
           /fk_pose      (geometry_msgs/PoseStamped)
           /system_status (std_msgs/String)

Jalankan:
  roslaunch modul09_kinematika p15_integration.launch
  rosrun modul09_kinematika p15_integration.py

Kirim waypoint:
  rostopic pub /waypoints std_msgs/String '{"waypoints": [[1,0],[1,1],[0,1],[0,0]]}'
"""

import rospy
import math
import json
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion, quaternion_from_euler


# ─── Modul FK (disederhanakan untuk robot mobile) ─────────────────────────────

def compute_robot_pose_fk(joint_states):
    """
    Untuk robot mobile, FK = akumulasi odometri dari kecepatan roda.
    Di sini kita hanya meneruskan pose dari /odom sebagai 'FK'.
    Fungsi ini adalah placeholder untuk integrasi dengan FK arm.
    """
    return None


# ─── PID ──────────────────────────────────────────────────────────────────────

class PID:
    def __init__(self, Kp, Ki, Kd, dt, out_min=-float("inf"), out_max=float("inf")):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.dt = dt
        self.out_min, self.out_max = out_min, out_max
        self.setpoint = 0.0
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, pv):
        e = self.setpoint - pv
        P = self.Kp * e
        self.integral += e * self.dt
        I = self.Ki * self.integral
        D = self.Kd * (e - self.prev_error) / self.dt
        out = max(self.out_min, min(self.out_max, P + I + D))
        if out in (self.out_min, self.out_max):
            self.integral -= e * self.dt
        self.prev_error = e
        return out


# ─── Integrated System Node ───────────────────────────────────────────────────

class IntegratedSystem:
    # Kontroler parameter
    K_RHO   = 0.5
    K_ALPHA = 1.5
    V_MAX   = 0.3
    W_MAX   = 1.0
    DIST_THRESH = 0.06

    def __init__(self):
        rospy.init_node("p15_integration", anonymous=False)

        # Robot state
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # Waypoint queue
        self.waypoints = []
        self.current_wp_idx = 0

        # TF broadcaster
        self.tf_br = tf.TransformBroadcaster()

        # Publishers
        self.cmd_pub    = rospy.Publisher("/cmd_vel",        Twist,        queue_size=10)
        self.fk_pub     = rospy.Publisher("/fk_pose",        PoseStamped,  queue_size=10)
        self.status_pub = rospy.Publisher("/system_status",  String,       queue_size=10)

        # Subscribers
        rospy.Subscriber("/odom",        Odometry,   self.odom_cb)
        rospy.Subscriber("/waypoints",   String,     self.waypoints_cb)

        # Default waypoints (kotak 1×1 m)
        self.waypoints = [(1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]

        self.control_timer = rospy.Timer(rospy.Duration(0.05), self.control_loop)

        rospy.loginfo("P15: Sistem Terintegrasi AKTIF")
        rospy.loginfo("     Waypoints: " + str(self.waypoints))
        rospy.loginfo("     Status: rostopic echo /system_status")

    # ── Callbacks ──────────────────────────────────────────────────────────────

    def odom_cb(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        _, _, self.theta = euler_from_quaternion([q.x, q.y, q.z, q.w])

    def waypoints_cb(self, msg):
        try:
            data = json.loads(msg.data)
            self.waypoints = [tuple(wp) for wp in data.get("waypoints", [])]
            self.current_wp_idx = 0
            rospy.loginfo(f"P15: Waypoints baru: {self.waypoints}")
        except Exception as e:
            rospy.logwarn(f"P15: Gagal parse waypoints: {e}")

    # ── Utilities ──────────────────────────────────────────────────────────────

    @staticmethod
    def normalize_angle(a):
        while a >  math.pi: a -= 2 * math.pi
        while a <= -math.pi: a += 2 * math.pi
        return a

    def publish_tf(self):
        q = quaternion_from_euler(0, 0, self.theta)
        self.tf_br.sendTransform(
            (self.x, self.y, 0),
            q,
            rospy.Time.now(),
            "base_link",
            "odom"
        )

    def publish_fk_pose(self):
        pose = PoseStamped()
        pose.header.stamp    = rospy.Time.now()
        pose.header.frame_id = "odom"
        pose.pose.position.x = self.x
        pose.pose.position.y = self.y
        q = quaternion_from_euler(0, 0, self.theta)
        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]
        self.fk_pub.publish(pose)

    # ── Go-to-Goal ─────────────────────────────────────────────────────────────

    def go_to_goal(self, gx, gy):
        dx = gx - self.x
        dy = gy - self.y
        rho = math.sqrt(dx**2 + dy**2)

        if rho < self.DIST_THRESH:
            return True   # tiba

        angle_to_goal = math.atan2(dy, dx)
        alpha = self.normalize_angle(angle_to_goal - self.theta)

        v = min(self.K_RHO * rho, self.V_MAX)
        w = max(-self.W_MAX, min(self.W_MAX, self.K_ALPHA * alpha))

        if abs(alpha) > math.pi / 4:
            v *= 0.3

        cmd = Twist()
        cmd.linear.x  = v
        cmd.angular.z = w
        self.cmd_pub.publish(cmd)
        return False

    # ── Main Control Loop ──────────────────────────────────────────────────────

    def control_loop(self, event):
        # Publish TF dan FK pose
        self.publish_tf()
        self.publish_fk_pose()

        if not self.waypoints:
            self.cmd_pub.publish(Twist())
            return

        # Navigasi ke waypoint saat ini
        if self.current_wp_idx < len(self.waypoints):
            wp = self.waypoints[self.current_wp_idx]
            arrived = self.go_to_goal(wp[0], wp[1])

            if arrived:
                dist_err = math.sqrt((self.x - wp[0])**2 + (self.y - wp[1])**2)
                rospy.loginfo(
                    f"P15: ✓ WP {self.current_wp_idx+1}/{len(self.waypoints)} "
                    f"({wp[0]:.1f},{wp[1]:.1f}) tercapai. "
                    f"error={dist_err:.3f}m | "
                    f"Pose=({self.x:.3f},{self.y:.3f})"
                )
                self.cmd_pub.publish(Twist())  # berhenti
                self.current_wp_idx += 1
                rospy.sleep(0.5)  # jeda sebentar

            status_txt = (
                f"NAVIGATING | WP={self.current_wp_idx+1}/{len(self.waypoints)} "
                f"| Pose=({self.x:.2f},{self.y:.2f}) "
                f"| Target=({wp[0]},{wp[1]})"
            )
        else:
            self.cmd_pub.publish(Twist())
            status_txt = f"MISSION_COMPLETE | Pose=({self.x:.2f},{self.y:.2f})"
            rospy.loginfo_once("P15: ✓ Semua waypoint selesai!")

        self.status_pub.publish(String(data=status_txt))


def main():
    node = IntegratedSystem()
    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
