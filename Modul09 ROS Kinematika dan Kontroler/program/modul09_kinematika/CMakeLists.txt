cmake_minimum_required(VERSION 3.0.2)
project(modul09_kinematika)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  geometry_msgs
  nav_msgs
  sensor_msgs
  tf
  tf2_ros
  urdf
  xacro
)

catkin_package()

install(PROGRAMS
  scripts/p01_fk_2dof.py
  scripts/p02_fk_dh.py
  scripts/p03_ik_analytic.py
  scripts/p04_ik_numerical.py
  scripts/p05_jacobian.py
  scripts/p06_tf_broadcaster.py
  scripts/p07_urdf_check.py
  scripts/p08_pid_velocity.py
  scripts/p09_go_to_goal.py
  scripts/p10_odometry.py
  scripts/p11_ros_control_test.py
  scripts/p12_gazebo_validation.py
  scripts/p13_cascade_controller.py
  scripts/p14_omni_kinematics.py
  scripts/p15_integration.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch config urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
