#!/usr/bin/env python3
"""
P02 - Forward Kinematics dengan Parameter Denavit-Hartenberg (DH)
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Membangun matriks transformasi homogen menggunakan konvensi DH standar
dan menghitung FK untuk robot 3-DOF.

Konvensi DH standar:
  T(i-1->i) = Rz(theta) * Tz(d) * Tx(a) * Rx(alpha)
"""

import numpy as np
import math


# Tabel DH untuk robot 3-DOF (contoh)
# Format: [theta_offset, d, a, alpha]  theta_offset = offset sudut tetap
# Variabel sendi: theta = joint_angle + theta_offset
DH_TABLE_3DOF = [
    # theta_off  d      a      alpha
    [0.0,        0.10,  0.00,  math.pi / 2],   # Sendi 1
    [0.0,        0.00,  0.25,  0.0],            # Sendi 2
    [0.0,        0.00,  0.20,  0.0],            # Sendi 3
]


def dh_matrix(theta, d, a, alpha):
    """
    Buat matriks transformasi homogen 4x4 menggunakan parameter DH standar.

    T = Rz(theta) * Tz(d) * Tx(a) * Rx(alpha)

    Args:
        theta (float): Sudut rotasi sekitar sumbu z (radian)
        d (float): Translasi sepanjang sumbu z (meter)
        a (float): Translasi sepanjang sumbu x (meter)
        alpha (float): Rotasi sekitar sumbu x (radian)

    Returns:
        numpy.ndarray: Matriks 4x4 transformasi homogen
    """
    ct = math.cos(theta)
    st = math.sin(theta)
    ca = math.cos(alpha)
    sa = math.sin(alpha)

    T = np.array([
        [ct,  -st * ca,   st * sa,  a * ct],
        [st,   ct * ca,  -ct * sa,  a * st],
        [0.0,  sa,         ca,       d     ],
        [0.0,  0.0,         0.0,     1.0   ]
    ])
    return T


def forward_kinematics_dh(joint_angles_rad, dh_table):
    """
    Hitung FK untuk robot n-DOF menggunakan tabel DH.

    Args:
        joint_angles_rad (list): Sudut setiap sendi dalam radian
        dh_table (list): Tabel DH [[theta_off, d, a, alpha], ...]

    Returns:
        tuple: (T_total, T_list) - matriks total dan daftar matriks parsial
    """
    n = len(joint_angles_rad)
    T_total = np.eye(4)
    T_list = [np.eye(4)]   # T_list[i] = transformasi dari frame 0 ke frame i

    for i in range(n):
        theta_off, d, a, alpha = dh_table[i]
        theta = joint_angles_rad[i] + theta_off
        T_i = dh_matrix(theta, d, a, alpha)
        T_total = T_total @ T_i
        T_list.append(T_total.copy())

    return T_total, T_list


def extract_pose(T):
    """Ekstrak posisi dan orientasi (euler ZYX) dari matriks 4x4."""
    position = T[:3, 3]
    R = T[:3, :3]
    # Euler ZYX (yaw-pitch-roll)
    yaw   = math.atan2(R[1, 0], R[0, 0])
    pitch = math.atan2(-R[2, 0], math.sqrt(R[2, 1]**2 + R[2, 2]**2))
    roll  = math.atan2(R[2, 1], R[2, 2])
    return position, (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))


def print_matrix(T, label="T"):
    print(f"  {label}:")
    for row in T:
        print("    " + "  ".join(f"{v:8.4f}" for v in row))


def main():
    print("=" * 70)
    print("P02 - Forward Kinematics dengan Parameter DH (Robot 3-DOF)")
    print("=" * 70)
    print("\nTabel DH:")
    print(f"  {'Sendi':^6} {'theta_off':^10} {'d (m)':^8} {'a (m)':^8} {'alpha (°)':^10}")
    print("  " + "-" * 50)
    for i, (t_off, d, a, alpha) in enumerate(DH_TABLE_3DOF):
        print(f"  {i+1:^6} {math.degrees(t_off):^10.1f} {d:^8.3f} {a:^8.3f} {math.degrees(alpha):^10.1f}")

    # Kasus uji
    test_configs = [
        [0.0,           0.0,            0.0],
        [math.pi/6,     math.pi/4,      0.0],
        [0.0,           math.pi/2,      -math.pi/4],
    ]

    for idx, joints in enumerate(test_configs):
        joints_deg = [math.degrees(j) for j in joints]
        print(f"\n--- Konfigurasi {idx+1}: "
              f"[{', '.join(f'{d:.1f}°' for d in joints_deg)}] ---")

        T_total, T_list = forward_kinematics_dh(joints, DH_TABLE_3DOF)
        pos, ori = extract_pose(T_total)

        print_matrix(T_total, "T_0_3 (Frame 0 → Frame 3)")
        print(f"  Posisi end-effector : x={pos[0]:.4f}m, y={pos[1]:.4f}m, z={pos[2]:.4f}m")
        print(f"  Orientasi (R,P,Y)   : {ori[0]:.2f}°, {ori[1]:.2f}°, {ori[2]:.2f}°")

    print("\n--- Semua matriks parsial untuk konfigurasi 2 ---")
    T_total, T_list = forward_kinematics_dh(test_configs[1], DH_TABLE_3DOF)
    for i, T in enumerate(T_list):
        print_matrix(T, f"T_0_{i}")


if __name__ == "__main__":
    main()
