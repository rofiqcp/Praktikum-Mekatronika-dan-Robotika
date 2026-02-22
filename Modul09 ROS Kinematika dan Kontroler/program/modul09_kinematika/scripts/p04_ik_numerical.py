#!/usr/bin/env python3
"""
P04 - Inverse Kinematics Numerik dengan Jacobian Pseudoinverse
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Menghitung IK secara iteratif menggunakan metode Jacobian pseudoinverse
(Damped Least Squares). Cocok untuk robot dengan jumlah DOF berapapun.

Algoritma:
  1. Hitung FK(q_current) -> pose saat ini
  2. Hitung error = target - current
  3. Cek konvergensi ||error|| < tol
  4. Hitung Jacobian J(q_current)
  5. Hitung J_pseudo = J^T * inv(J*J^T + lambda^2 * I)
  6. Update: q = q + alpha * J_pseudo * error
"""

import numpy as np
import math
import time

L1 = 0.5   # panjang lengan 1 (meter)
L2 = 0.3   # panjang lengan 2 (meter)


def forward_kinematics_2dof(joints):
    """FK 2-DOF: [theta1, theta2] -> [x, y]"""
    theta1, theta2 = joints
    x = L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2)
    y = L1 * math.sin(theta1) + L2 * math.sin(theta1 + theta2)
    return np.array([x, y])


def compute_jacobian_2dof(joints):
    """
    Hitung Jacobian 2x2 untuk robot 2-DOF planar.

    J = | dx/dtheta1  dx/dtheta2 |
        | dy/dtheta1  dy/dtheta2 |
    """
    theta1, theta2 = joints
    J = np.array([
        [-L1 * math.sin(theta1) - L2 * math.sin(theta1 + theta2),
         -L2 * math.sin(theta1 + theta2)],
        [ L1 * math.cos(theta1) + L2 * math.cos(theta1 + theta2),
          L2 * math.cos(theta1 + theta2)]
    ])
    return J


def ik_numerical(target_xy, q_init=None, alpha=0.1, lam=0.01,
                 max_iter=1000, tol=1e-4):
    """
    IK numerik dengan Damped Least Squares (DLS).

    Args:
        target_xy (array-like): Target posisi [x, y]
        q_init (array-like): Sudut awal [theta1, theta2] (radian)
        alpha (float): Learning rate
        lam (float): Damping factor untuk stabilitas
        max_iter (int): Maksimum iterasi
        tol (float): Threshold konvergensi (meter)

    Returns:
        dict: {joints, iterations, final_error, converged, time_ms}
    """
    target = np.array(target_xy, dtype=float)
    q = np.array(q_init if q_init is not None else [0.0, 0.0], dtype=float)

    t_start = time.time()
    converged = False

    for iteration in range(1, max_iter + 1):
        current = forward_kinematics_2dof(q)
        error = target - current
        err_norm = np.linalg.norm(error)

        if err_norm < tol:
            converged = True
            break

        J = compute_jacobian_2dof(q)
        # Damped Least Squares pseudoinverse: J^T * inv(J*J^T + lambda^2 * I)
        JJT = J @ J.T
        J_pseudo = J.T @ np.linalg.inv(JJT + lam**2 * np.eye(2))

        delta_q = J_pseudo @ error
        q = q + alpha * delta_q

    elapsed_ms = (time.time() - t_start) * 1000
    return {
        "joints": q,
        "iterations": iteration,
        "final_error": np.linalg.norm(target - forward_kinematics_2dof(q)),
        "converged": converged,
        "time_ms": elapsed_ms,
    }


def main():
    print("=" * 70)
    print("P04 - IK Numerik Jacobian Pseudoinverse (Robot 2-DOF)")
    print(f"  L1={L1}m, L2={L2}m")
    print("=" * 70)

    target = (0.5, 0.3)
    print(f"\nTarget: x={target[0]}, y={target[1]}")
    print(f"\n{'alpha':>8} {'Iterasi':>8} {'Error (m)':>12} {'Waktu (ms)':>12} {'Konvergen':>10}")
    print("-" * 55)

    for alpha in [0.01, 0.1, 0.5, 1.0]:
        res = ik_numerical(target, alpha=alpha)
        print(f"{alpha:>8.2f} {res['iterations']:>8d} "
              f"{res['final_error']:>12.6f} {res['time_ms']:>12.2f} "
              f"{'Ya' if res['converged'] else 'Tidak':>10}")
        if res["converged"]:
            q = res["joints"]
            print(f"         θ₁={math.degrees(q[0]):.2f}°  θ₂={math.degrees(q[1]):.2f}°")

    print("\n--- Perbandingan berbagai target (alpha=0.1) ---")
    targets = [(0.5, 0.3), (0.7, 0.1), (0.2, 0.7), (0.4, 0.4)]
    for t in targets:
        res = ik_numerical(t, alpha=0.1)
        status = "✓" if res["converged"] else "✗"
        print(f"  {status} Target ({t[0]:.1f},{t[1]:.1f}) → "
              f"iter={res['iterations']}, error={res['final_error']:.6f}m, "
              f"t={res['time_ms']:.2f}ms")


if __name__ == "__main__":
    main()
