import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    robot_gazebo_dir = get_package_share_directory('robot_gazebo')
    field_dir = get_package_share_directory('Field_description')

    # 1. 啟動官方 Gazebo 環境與機器人
    # 這裡不覆蓋 'world' 參數，讓官方腳本去讀它自帶的 empty.sdf
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_gazebo_dir, 'launch', 'worlds.launch.py')
        ),
        launch_arguments={
            'moveit_unite': 'true'
        }.items()
    )

    # 2. 生成我們簡化過 Collision 的場地 (Z 軸設為 0.0)
    field_urdf_path = os.path.join(field_dir, 'urdf', 'Field.urdf')
    spawn_field_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_field', '-file', field_urdf_path, '-x', '0.0', '-y', '0.0', '-z', '0.0'],
        output='screen'
    )

    return LaunchDescription([
        start_gazebo_cmd,
        spawn_field_node
    ])