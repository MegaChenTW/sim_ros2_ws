import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/mega/JetRover/sim/ros2_ws/install/robot_gazebo'
