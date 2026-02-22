#!/usr/bin/env python3
"""
P01 - Forward Kinematics Robot 2-DOF
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Menghitung posisi end-effector robot 2-DOF planar dari sudut sendi theta1, theta2.
Formula:
  x = L1*cos(theta1) + L2*cos(theta1+theta2)
  y = L1*sin(theta1) + L2*sin(theta1+theta2)
  phi = theta1 + theta2  (total orientasi)
"""

import math
import sys

# Panjang lengan robot (meter)
L1 = 0.5
L2 = 0.3


def forward_kinematics_2dof(theta1_deg, theta2_deg, l1=L1, l2=L2):
    """
    Hitung Forward Kinematics robot 2-DOF planar.

    Args:
        theta1_deg (float): Sudut sendi 1 dalam derajat
        theta2_deg (float): Sudut sendi 2 dalam derajat
        l1 (float): Panjang lengan 1 (meter)
        l2 (float): Panjang lengan 2 (meter)

    Returns:
        tuple: (x, y, phi) posisi dan orientasi end-effector
    """
    theta1 = math.radians(theta1_deg)
    theta2 = math.radians(theta2_deg)

    x = l1 * math.cos(theta1) + l2 * math.cos(theta1 + theta2)
    y = l1 * math.sin(theta1) + l2 * math.sin(theta1 + theta2)
    phi = theta1 + theta2  # orientasi total dalam radian

    return x, y, phi


def print_result(theta1, theta2, x, y, phi):
    print(f"  theta1={theta1:6.1f}°  theta2={theta2:6.1f}° "
          f"| x={x:7.4f}m  y={y:7.4f}m  phi={math.degrees(phi):7.2f}°")


def main():
    print("=" * 70)
    print("P01 - Forward Kinematics Robot 2-DOF")
    print(f"  Panjang lengan: L1={L1}m, L2={L2}m")
    print("=" * 70)

    # Kasus uji dari tabel jobsheet
    test_cases = [
        (0,   0,   L1, L2),
        (30,  45,  L1, L2),
        (90,  -30, L1, L2),
        (45,  90,  L1, L2),
        (60,  60,  0.4, 0.4),
    ]

    print(f"{'theta1':>8} {'theta2':>8} {'x (m)':>10} {'y (m)':>10} {'phi (°)':>10}")
    print("-" * 55)

    for theta1_d, theta2_d, l1, l2 in test_cases:
        x, y, phi = forward_kinematics_2dof(theta1_d, theta2_d, l1, l2)
        print(f"{theta1_d:>8.1f} {theta2_d:>8.1f} "
              f"{x:>10.4f} {y:>10.4f} {math.degrees(phi):>10.2f}")

    print("\n--- Verifikasi Manual (theta1=30°, theta2=45°, L1=0.5, L2=0.3) ---")
    theta1 = math.radians(30)
    theta2 = math.radians(45)
    x_manual = L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2)
    y_manual = L1 * math.sin(theta1) + L2 * math.sin(theta1 + theta2)
    print(f"  x = {L1}*cos({30}°) + {L2}*cos({30+45}°)")
    print(f"  x = {L1}*{math.cos(theta1):.4f} + {L2}*{math.cos(theta1+theta2):.4f}")
    print(f"  x = {x_manual:.4f} m")
    print(f"  y = {y_manual:.4f} m")

    # Input interaktif
    print("\n--- Input Manual ---")
    try:
        t1 = float(input("Masukkan theta1 (derajat): "))
        t2 = float(input("Masukkan theta2 (derajat): "))
        x, y, phi = forward_kinematics_2dof(t1, t2)
        print(f"  Hasil FK: x={x:.4f}m, y={y:.4f}m, phi={math.degrees(phi):.2f}°")
    except (ValueError, EOFError):
        pass  # skip jika bukan mode interaktif


if __name__ == "__main__":
    main()
