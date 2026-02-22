#!/usr/bin/env python3
"""
P08 - PID Kontroler Kecepatan Motor (dengan simulasi plant motor DC)
Modul 09: ROS Kinematika dan Kontroler
Prodi Teknologi Rekayasa Otomasi

Mengimplementasikan PID kontroler untuk kecepatan motor DC.
Plant disimulasikan sebagai sistem orde-1:
  tau * dy/dt + y = K_m * u
  dengan tau=0.5s, K_m=100 (RPM/PWM)

Parameter PID dapat diubah real-time via rqt_reconfigure.
Jalankan:
  rosrun modul09_kinematika p08_pid_velocity.py
  rosrun rqt_reconfigure rqt_reconfigure
  rosrun rqt_plot rqt_plot /setpoint:data /process_value:data /error:data
"""

import rospy
from std_msgs.msg import Float64
from dynamic_reconfigure.server import Server

# Import config class (dibuat dari file .cfg – gunakan default jika tidak ada)
try:
    from modul09_kinematika.cfg import PIDConfig
    HAS_DYNREC = True
except ImportError:
    HAS_DYNREC = False


class MotorPlant:
    """Simulasi plant motor DC orde-1: tau*dy/dt + y = Km*u"""

    def __init__(self, tau=0.5, Km=100.0, dt=0.02):
        self.tau = tau
        self.Km = Km
        self.dt = dt
        self.y = 0.0  # kecepatan motor (RPM)

    def update(self, u):
        """Integrasi Euler satu langkah."""
        u_clamped = max(-255.0, min(255.0, u))
        dy = (self.Km * u_clamped - self.y) / self.tau
        self.y += dy * self.dt
        return self.y


class PIDController:
    """Kontroler PID diskrit dengan anti-windup."""

    def __init__(self, Kp=1.0, Ki=0.1, Kd=0.01, dt=0.02,
                 out_min=-255.0, out_max=255.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.out_min = out_min
        self.out_max = out_max

        self.setpoint = 0.0
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, process_value):
        error = self.setpoint - process_value

        P = self.Kp * error

        self.integral += error * self.dt
        I = self.Ki * self.integral

        derivative = (error - self.prev_error) / self.dt
        D = self.Kd * derivative

        output = P + I + D
        output_clamped = max(self.out_min, min(self.out_max, output))

        # Anti-windup: rollback integral jika output tersaturasi
        if output_clamped != output:
            self.integral -= error * self.dt

        self.prev_error = error
        return output_clamped, error


class PIDNode:
    def __init__(self):
        rospy.init_node("p08_pid_velocity", anonymous=False)

        # Parameter dari ROS param server
        self.pid = PIDController(
            Kp=rospy.get_param("~Kp", 1.0),
            Ki=rospy.get_param("~Ki", 0.1),
            Kd=rospy.get_param("~Kd", 0.01),
            dt=0.02
        )
        self.plant = MotorPlant(tau=0.5, Km=100.0, dt=0.02)
        self.pid.setpoint = rospy.get_param("~setpoint", 100.0)

        # Publishers
        self.pub_pv  = rospy.Publisher("/process_value", Float64, queue_size=10)
        self.pub_sp  = rospy.Publisher("/setpoint",      Float64, queue_size=10)
        self.pub_err = rospy.Publisher("/error",         Float64, queue_size=10)
        self.pub_out = rospy.Publisher("/controller_output", Float64, queue_size=10)

        # dynamic_reconfigure jika tersedia
        if HAS_DYNREC:
            self.srv = Server(PIDConfig, self.dyn_rec_callback)
            rospy.loginfo("P08: dynamic_reconfigure aktif. "
                          "Buka: rosrun rqt_reconfigure rqt_reconfigure")
        else:
            rospy.logwarn("P08: dynamic_reconfigure tidak tersedia. "
                          "Edit parameter via rosparam set /p08_pid_velocity/Kp <value>")

        self.timer = rospy.Timer(rospy.Duration(0.02), self.control_loop)
        rospy.loginfo(f"P08: PID aktif. Kp={self.pid.Kp}, Ki={self.pid.Ki}, "
                      f"Kd={self.pid.Kd}, Setpoint={self.pid.setpoint} RPM")

    def dyn_rec_callback(self, config, level):
        self.pid.Kp = config["Kp"]
        self.pid.Ki = config["Ki"]
        self.pid.Kd = config["Kd"]
        self.pid.setpoint = config["setpoint"]
        rospy.loginfo(f"P08: Updated PID: Kp={self.pid.Kp}, Ki={self.pid.Ki}, "
                      f"Kd={self.pid.Kd}, SP={self.pid.setpoint}")
        return config

    def control_loop(self, event):
        output, error = self.pid.compute(self.plant.y)
        rpm = self.plant.update(output)

        self.pub_pv.publish(Float64(data=rpm))
        self.pub_sp.publish(Float64(data=self.pid.setpoint))
        self.pub_err.publish(Float64(data=error))
        self.pub_out.publish(Float64(data=output))


def main():
    node = PIDNode()
    rospy.spin()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
