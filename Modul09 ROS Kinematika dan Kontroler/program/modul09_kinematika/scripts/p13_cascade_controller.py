#!/usr/bin/env python3
"""
P13 - Cascade Controller (Posisi + Kecepatan)
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Mengimplementasikan kontroler cascade dua loop:
  Outer Loop (Position): setpoint_pos → error_pos → PID_pos → setpoint_vel
  Inner Loop (Velocity): setpoint_vel → error_vel → PID_vel → motor_command

Plant: simulasi sistem motor DC orde-1 dengan integrasi posisi.

Subscribe: /target_position (std_msgs/Float64) - target posisi dalam meter
Publish:   /cascade/position    (std_msgs/Float64) - posisi aktual
           /cascade/velocity    (std_msgs/Float64) - kecepatan aktual
           /cascade/vel_setpoint (std_msgs/Float64) - setpoint kecepatan (output outer)

Jalankan:
  rosrun modul09_kinematika p13_cascade_controller.py
  rosrun rqt_reconfigure rqt_reconfigure
  rosrun rqt_plot rqt_plot /cascade/position:data /cascade/velocity:data
  rostopic pub /target_position std_msgs/Float64 "data: 1.0"
"""

import rospy
from std_msgs.msg import Float64
import math


class PID:
    """Kontroler PID diskrit dengan anti-windup."""

    def __init__(self, Kp=1.0, Ki=0.0, Kd=0.0, dt=0.02,
                 out_min=-float("inf"), out_max=float("inf")):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.out_min = out_min
        self.out_max = out_max

        self.setpoint   = 0.0
        self.integral   = 0.0
        self.prev_error = 0.0

    def compute(self, process_value):
        error = self.setpoint - process_value
        P = self.Kp * error
        self.integral += error * self.dt
        I = self.Ki * self.integral
        D = self.Kd * (error - self.prev_error) / self.dt

        output = P + I + D
        clamped = max(self.out_min, min(self.out_max, output))
        if clamped != output:
            self.integral -= error * self.dt   # anti-windup
        self.prev_error = error
        return clamped, error


class DrivetrainPlant:
    """
    Plant sederhana: motor DC orde-1 + integrasi posisi.
      tau * dv/dt + v = Km * u   (kecepatan)
      dp/dt = v                  (posisi)
    """

    def __init__(self, tau=0.3, Km=1.0, dt=0.02):
        self.tau = tau
        self.Km  = Km
        self.dt  = dt
        self.velocity = 0.0
        self.position = 0.0

    def update(self, u):
        dv = (self.Km * u - self.velocity) / self.tau
        self.velocity += dv * self.dt
        self.position += self.velocity * self.dt
        return self.position, self.velocity


class CascadeController:
    def __init__(self):
        rospy.init_node("p13_cascade_controller", anonymous=False)

        dt = 0.02  # 20ms

        # Outer loop: posisi → kecepatan referensi
        self.pid_pos = PID(
            Kp=rospy.get_param("~Kp_pos", 1.0),
            Ki=rospy.get_param("~Ki_pos", 0.0),
            Kd=rospy.get_param("~Kd_pos", 0.0),
            dt=dt,
            out_min=-1.0, out_max=1.0
        )

        # Inner loop: kecepatan → sinyal motor
        self.pid_vel = PID(
            Kp=rospy.get_param("~Kp_vel", 2.0),
            Ki=rospy.get_param("~Ki_vel", 0.5),
            Kd=rospy.get_param("~Kd_vel", 0.0),
            dt=dt,
            out_min=-10.0, out_max=10.0
        )

        self.plant = DrivetrainPlant(tau=0.3, Km=1.0, dt=dt)

        # Publishers
        self.pub_pos = rospy.Publisher("/cascade/position",    Float64, queue_size=10)
        self.pub_vel = rospy.Publisher("/cascade/velocity",    Float64, queue_size=10)
        self.pub_vsp = rospy.Publisher("/cascade/vel_setpoint", Float64, queue_size=10)
        self.pub_err = rospy.Publisher("/cascade/pos_error",   Float64, queue_size=10)

        # Subscriber untuk target posisi
        rospy.Subscriber("/target_position", Float64, self.target_callback)

        self.timer = rospy.Timer(rospy.Duration(dt), self.control_loop)
        rospy.loginfo("P13: Cascade Controller aktif.")
        rospy.loginfo("     Kirim target: rostopic pub /target_position "
                      "std_msgs/Float64 'data: 1.0'")

    def target_callback(self, msg):
        self.pid_pos.setpoint = msg.data
        rospy.loginfo(f"P13: Target posisi = {msg.data:.3f} m")

    def control_loop(self, event):
        pos, vel = self.plant.position, self.plant.velocity

        # Outer loop: hitung kecepatan referensi dari error posisi
        vel_ref, pos_error = self.pid_pos.compute(pos)

        # Inner loop: hitung perintah motor dari error kecepatan
        self.pid_vel.setpoint = vel_ref
        motor_cmd, _ = self.pid_vel.compute(vel)

        # Update plant
        new_pos, new_vel = self.plant.update(motor_cmd)

        # Publish
        self.pub_pos.publish(Float64(data=new_pos))
        self.pub_vel.publish(Float64(data=new_vel))
        self.pub_vsp.publish(Float64(data=vel_ref))
        self.pub_err.publish(Float64(data=pos_error))


def main():
    node = CascadeController()
    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
