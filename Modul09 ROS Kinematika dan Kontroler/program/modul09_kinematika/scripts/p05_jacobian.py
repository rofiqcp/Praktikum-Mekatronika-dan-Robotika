#!/usr/bin/env python3
"""
P05 - Komputasi dan Visualisasi Jacobian
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Menghitung matriks Jacobian robot 2-DOF dan menganalisis:
- Determinan Jacobian
- Manipulability index: mu = sqrt(det(J * J^T))
- Singularitas: konfigurasi dengan mu ~ 0
- Plot manipulability vs theta1
"""

import math
import numpy as np

L1 = 0.5
L2 = 0.3


def compute_jacobian_2dof(theta1, theta2, l1=L1, l2=L2):
    """
    Hitung Jacobian analitik untuk robot 2-DOF planar.

    Returns:
        numpy.ndarray: Matriks J (2x2)
    """
    J = np.array([
        [-l1 * math.sin(theta1) - l2 * math.sin(theta1 + theta2),
         -l2 * math.sin(theta1 + theta2)],
        [ l1 * math.cos(theta1) + l2 * math.cos(theta1 + theta2),
          l2 * math.cos(theta1 + theta2)]
    ])
    return J


def manipulability(J):
    """Hitung manipulability index: mu = sqrt(det(J * J^T))"""
    return math.sqrt(max(0.0, np.linalg.det(J @ J.T)))


def main():
    print("=" * 70)
    print("P05 - Komputasi Jacobian dan Manipulability (Robot 2-DOF)")
    print(f"  L1={L1}m, L2={L2}m")
    print("=" * 70)

    # Kasus uji dari tabel jobsheet
    configs = [
        (0, 0),
        (30, 45),
        (90, 0),
        (0, 180),
        (45, 135),
    ]

    print(f"\n{'θ₁(°)':>7} {'θ₂(°)':>7} {'J[0,0]':>9} {'J[0,1]':>9} "
          f"{'J[1,0]':>9} {'J[1,1]':>9} {'det(J)':>9} {'μ':>8}")
    print("-" * 75)

    for t1_d, t2_d in configs:
        t1 = math.radians(t1_d)
        t2 = math.radians(t2_d)
        J = compute_jacobian_2dof(t1, t2)
        det_J = np.linalg.det(J)
        mu = manipulability(J)
        print(f"{t1_d:>7.0f} {t2_d:>7.0f} "
              f"{J[0,0]:>9.4f} {J[0,1]:>9.4f} "
              f"{J[1,0]:>9.4f} {J[1,1]:>9.4f} "
              f"{det_J:>9.4f} {mu:>8.4f}")

    # Scan manipulability vs theta1 (theta2 = 60 deg tetap)
    print("\n--- Scan μ vs θ₁ (θ₂=60° tetap) ---")
    theta2_fixed = math.radians(60)
    print(f"{'θ₁(°)':>8} {'μ':>12} {'Singularitas?':>15}")
    print("-" * 38)
    singular_threshold = 0.01
    for t1_d in range(0, 361, 30):
        t1 = math.radians(t1_d)
        J = compute_jacobian_2dof(t1, theta2_fixed)
        mu = manipulability(J)
        sing = "⚠ Singular!" if mu < singular_threshold else ""
        print(f"{t1_d:>8.0f} {mu:>12.4f} {sing:>15}")

    # Identifikasi konfigurasi singular secara analitik
    print("\n--- Analisis Singularitas ---")
    print("Singularitas terjadi saat det(J) = 0")
    print("Untuk robot 2-DOF: sin(theta2) = 0")
    print("  -> theta2 = 0° (lengan terlipat/terentang penuh) ATAU theta2 = 180°")
    print("\nVerifikasi:")
    for t2_d in [0, 180]:
        t2 = math.radians(t2_d)
        J = compute_jacobian_2dof(math.radians(45), t2)
        mu = manipulability(J)
        print(f"  theta2={t2_d}°: mu={mu:.6f} (singular: {mu < 0.001})")

    print("\n--- Velocity Analysis ---")
    print("Diberikan joint velocity q_dot = [0.1, 0.2] rad/s pada konfigurasi (30°,45°)")
    t1 = math.radians(30)
    t2 = math.radians(45)
    q_dot = np.array([0.1, 0.2])
    J = compute_jacobian_2dof(t1, t2)
    x_dot = J @ q_dot
    print(f"  x_dot = J * q_dot = {x_dot}")
    print(f"  Kecepatan end-effector: vx={x_dot[0]:.4f} m/s, vy={x_dot[1]:.4f} m/s")


if __name__ == "__main__":
    main()
