import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    # 1. 取得各個 package 的路徑
    my_sim_dir = get_package_share_directory('my_custom_sim')
    robot_gazebo_dir = get_package_share_directory('robot_gazebo')
    field_dir = get_package_share_directory('Field_description')
    
    # 2. 指定你的空白 World 檔案路徑
    world_file = os.path.join(my_sim_dir, 'worlds', 'empty_light.world')

    # 3. 啟動 Gazebo 並載入你的 World
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(robot_gazebo_dir, 'launch', 'gazebo.launch.py')),
        launch_arguments={'world': world_file}.items()
    )

    # 4. 解析你的場地 URDF (Xacro)
    field_urdf_path = os.path.join(field_dir, 'urdf', 'field.urdf') # 請確認你的 urdf 檔名
    
    # 5. 生成場地 (Spawn Field)
    spawn_field_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_field', '-file', field_urdf_path, '-x', '0.0', '-y', '0.0', '-z', '0.0'],
        output='screen'
    )

    # 6. 生成 JetRover 機器人 (直接呼叫官方的生成腳本)
    # 記得要在終端機先 export MACHINE_TYPE="JetRover_Mecanum"
    spawn_robot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(robot_gazebo_dir, 'launch', 'spawn_robot.launch.py'))
        # 如果需要結合 MoveIt2，也可以在這裡將對應參數傳入
    )

    # 7. (可選) 依樣畫葫蘆，生成你的 Block A
    # block_a_urdf = os.path.join(get_package_share_directory('block_A_description'), 'urdf', 'block_A.urdf')
    # spawn_block_a = Node(...)

    return LaunchDescription([
        start_gazebo_cmd,
        spawn_field_node,
        spawn_robot_cmd
        # spawn_block_a
    ])
