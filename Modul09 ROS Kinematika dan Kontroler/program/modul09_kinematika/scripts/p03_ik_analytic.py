#!/usr/bin/env python3
"""
P03 - Inverse Kinematics Analitik Robot 2-DOF
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Menghitung sudut sendi theta1 dan theta2 dari posisi target end-effector
menggunakan metode analitik (trigonometri/geometri).

Formula:
  cos(theta2) = (x^2 + y^2 - L1^2 - L2^2) / (2*L1*L2)
  theta2      = atan2(+/-sqrt(1 - cos(theta2)^2), cos(theta2))
  theta1      = atan2(y, x) - atan2(L2*sin(theta2), L1 + L2*cos(theta2))
"""

import math
import sys

L1 = 0.5   # panjang lengan 1 (meter)
L2 = 0.3   # panjang lengan 2 (meter)


def forward_kinematics_2dof(theta1, theta2, l1=L1, l2=L2):
    """FK 2-DOF untuk verifikasi IK."""
    x = l1 * math.cos(theta1) + l2 * math.cos(theta1 + theta2)
    y = l1 * math.sin(theta1) + l2 * math.sin(theta1 + theta2)
    return x, y


def inverse_kinematics_analytic(x_target, y_target, l1=L1, l2=L2):
    """
    IK analitik robot 2-DOF planar.

    Args:
        x_target (float): Target posisi x (meter)
        y_target (float): Target posisi y (meter)
        l1 (float): Panjang lengan 1
        l2 (float): Panjang lengan 2

    Returns:
        list of tuples: [(theta1_up, theta2_up), (theta1_down, theta2_down)]
                        Kosong jika target di luar workspace.
    """
    # Hitung cos(theta2) menggunakan hukum cosinus
    c2 = (x_target**2 + y_target**2 - l1**2 - l2**2) / (2.0 * l1 * l2)

    # Validasi workspace
    if c2 < -1.0 or c2 > 1.0:
        return []   # tidak ada solusi

    s2_pos = math.sqrt(1.0 - c2**2)   # elbow up
    s2_neg = -s2_pos                   # elbow down

    solutions = []
    for s2 in [s2_pos, s2_neg]:
        theta2 = math.atan2(s2, c2)
        theta1 = math.atan2(y_target, x_target) - math.atan2(
            l2 * s2, l1 + l2 * c2
        )
        solutions.append((theta1, theta2))

    return solutions


def verify_ik(theta1, theta2, x_target, y_target):
    """Verifikasi IK dengan FK, kembalikan error."""
    x_fk, y_fk = forward_kinematics_2dof(theta1, theta2)
    error = math.sqrt((x_fk - x_target)**2 + (y_fk - y_target)**2)
    return x_fk, y_fk, error


def main():
    print("=" * 75)
    print("P03 - Inverse Kinematics Analitik Robot 2-DOF")
    print(f"  L1={L1}m, L2={L2}m  |  Workspace: 0 <= r <= {L1+L2}m")
    print("=" * 75)

    # Kasus uji dari tabel jobsheet
    test_targets = [
        (0.5, 0.3),
        (0.7, 0.1),
        (0.2, 0.7),
        (0.1, 0.1),
        (0.9, 0.0),   # di batas workspace
        (1.0, 0.0),   # di luar workspace
    ]

    for x_t, y_t in test_targets:
        r = math.sqrt(x_t**2 + y_t**2)
        solutions = inverse_kinematics_analytic(x_t, y_t)

        print(f"\nTarget: x={x_t}, y={y_t}  (r={r:.3f}m)")

        if not solutions:
            print("  ❌ Tidak ada solusi – target di luar workspace!")
            continue

        labels = ["Elbow-up (θ₂>0)", "Elbow-down (θ₂<0)"]
        for label, (theta1, theta2) in zip(labels, solutions):
            x_fk, y_fk, err = verify_ik(theta1, theta2, x_t, y_t)
            print(f"  [{label}]")
            print(f"    θ₁={math.degrees(theta1):7.2f}°  "
                  f"θ₂={math.degrees(theta2):7.2f}°")
            print(f"    FK verifikasi: x={x_fk:.4f}m, y={y_fk:.4f}m  "
                  f"error={err:.6f}m")

    # Input interaktif
    print("\n--- Input Manual ---")
    try:
        x_in = float(input("Masukkan x target (m): "))
        y_in = float(input("Masukkan y target (m): "))
        sols = inverse_kinematics_analytic(x_in, y_in)
        if sols:
            for lbl, (t1, t2) in zip(["Elbow-up", "Elbow-down"], sols):
                print(f"  {lbl}: θ₁={math.degrees(t1):.2f}°, "
                      f"θ₂={math.degrees(t2):.2f}°")
        else:
            print("  Tidak ada solusi!")
    except (ValueError, EOFError):
        pass


if __name__ == "__main__":
    main()
