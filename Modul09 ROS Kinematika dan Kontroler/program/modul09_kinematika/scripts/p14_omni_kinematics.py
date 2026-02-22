#!/usr/bin/env python3
"""
P14 - Kinematika Robot Omni-Directional 3 Roda
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Implementasi Forward Kinematics dan Inverse Kinematics
untuk robot omni-directional dengan 3 roda Omni-wheel.

Posisi roda: sudut beta = 90°, 210°, 330° (120° terpisah)

IK (Body → Roda):
  omega_i = (1/R) * [-sin(beta_i)*vx + cos(beta_i)*vy + L*omega_z]

FK (Roda → Body) = pseudoinverse dari matriks IK:
  [vx, vy, omega_z] = pseudoinverse(M) @ [omega1, omega2, omega3] * R

Jalankan:
  rosrun modul09_kinematika p14_omni_kinematics.py
  atau sebagai node ROS (subscribe /cmd_vel, publish /wheel_speeds)
"""

import math
import numpy as np

try:
    import rospy
    from geometry_msgs.msg import Twist
    from std_msgs.msg import Float32MultiArray
    HAS_ROS = True
except ImportError:
    HAS_ROS = False


# Parameter robot omni 3 roda
WHEEL_RADIUS   = 0.05   # R - radius roda (meter)
ROBOT_RADIUS   = 0.15   # L - jarak dari pusat robot ke roda (meter)
BETA_DEGREES   = [90.0, 210.0, 330.0]   # sudut orientasi tiap roda


def build_ik_matrix(beta_list_deg, L=ROBOT_RADIUS):
    """
    Buat matriks IK untuk robot omni n-roda.

    Matriks M (n x 3) di mana baris ke-i adalah:
      [-sin(beta_i), cos(beta_i), L]

    Returns:
        numpy.ndarray: Matriks M (n x 3)
    """
    M = []
    for b_deg in beta_list_deg:
        b = math.radians(b_deg)
        M.append([-math.sin(b), math.cos(b), L])
    return np.array(M)


def omni_ik(vx, vy, omega_z, R=WHEEL_RADIUS, L=ROBOT_RADIUS,
            beta_deg=None):
    """
    IK robot omni: kecepatan body → kecepatan roda.

    Args:
        vx (float): Kecepatan linear sumbu X (m/s)
        vy (float): Kecepatan linear sumbu Y (m/s)
        omega_z (float): Kecepatan angular (rad/s)
        R (float): Radius roda
        L (float): Jarak pusat ke roda
        beta_deg (list): Sudut roda dalam derajat

    Returns:
        numpy.ndarray: Kecepatan angular setiap roda [omega1, omega2, omega3] (rad/s)
    """
    if beta_deg is None:
        beta_deg = BETA_DEGREES
    M = build_ik_matrix(beta_deg, L)
    body_vel = np.array([vx, vy, omega_z])
    wheel_omega = (1.0 / R) * (M @ body_vel)
    return wheel_omega


def omni_fk(wheel_omega, R=WHEEL_RADIUS, L=ROBOT_RADIUS, beta_deg=None):
    """
    FK robot omni: kecepatan roda → kecepatan body.
    Menggunakan pseudoinverse dari matriks IK.

    Args:
        wheel_omega (array-like): Kecepatan angular roda [omega1, omega2, omega3] (rad/s)

    Returns:
        numpy.ndarray: Kecepatan body [vx, vy, omega_z]
    """
    if beta_deg is None:
        beta_deg = BETA_DEGREES
    M = build_ik_matrix(beta_deg, L)
    # FK = R * pseudoinverse(M) * wheel_omega
    M_pinv = np.linalg.pinv(M)
    body_vel = R * (M_pinv @ np.array(wheel_omega))
    return body_vel


def verify_ik_fk(vx, vy, omega_z):
    """Verifikasi: FK(IK(input)) ≈ input."""
    wheel_omega = omni_ik(vx, vy, omega_z)
    body_vel_recovered = omni_fk(wheel_omega)
    error = np.linalg.norm(body_vel_recovered - np.array([vx, vy, omega_z]))
    return wheel_omega, body_vel_recovered, error


class OmniController:
    """ROS node untuk omni controller (opsional jika ROS tersedia)."""

    def __init__(self):
        rospy.init_node("p14_omni_controller", anonymous=False)

        self.pub = rospy.Publisher("/wheel_speeds", Float32MultiArray, queue_size=10)
        rospy.Subscriber("/cmd_vel", Twist, self.cmd_callback)
        rospy.loginfo("P14: Omni Controller aktif. Subscribe /cmd_vel, "
                      "Publish /wheel_speeds")

    def cmd_callback(self, msg):
        vx = msg.linear.x
        vy = msg.linear.y
        wz = msg.angular.z

        wheels = omni_ik(vx, vy, wz)

        out = Float32MultiArray()
        out.data = [float(w) for w in wheels]
        self.pub.publish(out)

        rospy.loginfo_throttle(
            1.0,
            f"P14: vx={vx:.2f} vy={vy:.2f} wz={wz:.2f} | "
            f"ω=[{wheels[0]:.2f},{wheels[1]:.2f},{wheels[2]:.2f}] rad/s"
        )


def standalone_demo():
    """Demo tanpa ROS."""
    print("=" * 70)
    print("P14 - Kinematika Robot Omni-Directional 3 Roda")
    print(f"  R={WHEEL_RADIUS}m, L={ROBOT_RADIUS}m")
    print(f"  Sudut roda: {BETA_DEGREES}°")
    print("=" * 70)

    print(f"\n{'Perintah':^35} {'ω₁':>8} {'ω₂':>8} {'ω₃':>8} "
          f"{'FK_vx':>8} {'FK_vy':>8} {'FK_wz':>8} {'Error':>8}")
    print("-" * 100)

    test_inputs = [
        (0.2,  0.0,  0.0,  "Maju (+X)"),
        (0.0,  0.2,  0.0,  "Geser (+Y)"),
        (0.0,  0.0,  0.5,  "Putar CCW"),
        (0.2,  0.2,  0.0,  "Diagonal (+X+Y)"),
        (0.1, -0.1,  0.3,  "Gerak kompleks"),
    ]

    for vx, vy, wz, label in test_inputs:
        wheels, body_rec, err = verify_ik_fk(vx, vy, wz)
        print(f"  {label:30s} "
              f"{wheels[0]:>8.3f} {wheels[1]:>8.3f} {wheels[2]:>8.3f} "
              f"{body_rec[0]:>8.3f} {body_rec[1]:>8.3f} {body_rec[2]:>8.3f} "
              f"{err:>8.6f}")

    print("\n--- Matriks IK ---")
    M = build_ik_matrix(BETA_DEGREES)
    print("  M = ")
    for row in M:
        print("    " + "  ".join(f"{v:8.4f}" for v in row))

    print("\n--- Pseudoinverse M⁺ ---")
    M_pinv = np.linalg.pinv(M)
    for row in M_pinv:
        print("    " + "  ".join(f"{v:8.4f}" for v in row))


def main():
    if HAS_ROS:
        try:
            rospy.init_node("p14_omni_check", anonymous=True)
            # Jika dipanggil sebagai ROS node, jalankan standalone demo dulu
            standalone_demo()
            # Kemudian jalankan controller jika diperlukan
        except Exception:
            standalone_demo()
    else:
        standalone_demo()


if __name__ == "__main__":
    main()
