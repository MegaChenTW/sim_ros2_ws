import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

#offset_y = 630 + 380/2 = 820
#offset_x = 200 (guessed)
def generate_launch_description():
    robot_gazebo_dir = get_package_share_directory('robot_gazebo')
    field_dir = get_package_share_directory('Field_description')

    # field_dir 的值會是: .../install/Field_description/share/Field_description
    # Ignition 需要的是它的上一層目錄: .../install/Field_description/share
    # =====================================================================
    field_resource_path = os.path.abspath(os.path.join(field_dir, '..'))
    
    if 'IGN_GAZEBO_RESOURCE_PATH' in os.environ:
        os.environ['IGN_GAZEBO_RESOURCE_PATH'] += ':' + field_resource_path
    else:
        os.environ['IGN_GAZEBO_RESOURCE_PATH'] = field_resource_path
    
    # 1. 啟動官方 Gazebo 環境與機器人
    start_gazebo_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_gazebo_dir, 'launch', 'worlds.launch.py')
        ),
        launch_arguments={
            #'moveit_unite': 'true',
            'nav' : 'true',
        }.items()
    )

    # 2. 啟動 ROS-Ignition 橋接器 (新增此區塊)
    # 這是讓 Nav2 的 /cmd_vel 能夠傳遞到 Gazebo 物理引擎的關鍵
    ros_ign_bridge_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(robot_gazebo_dir, 'launch', 'ros_ign_bridge.launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
        }.items(),
    )

    # 3. 指定你的 場地 Xacro 檔案路徑
    field_xacro_path = os.path.join(field_dir, 'urdf', 'Field.xacro')

    # 4. 使用 xacro 套件將 .xacro 動態轉換為純 URDF 格式的 XML 字串
    field_urdf_xml = xacro.process_file(field_xacro_path).toxml()

    # 5. 使用「新版 Gazebo (ros_gz_sim)」的生成節點，而非舊版的 gazebo_ros
    spawn_field_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_field',
            '-string', field_urdf_xml,  # 直接傳入轉換好的 XML 字串
            '-x', '-0.82', 
            '-y', '-0.2', 
            '-z', '0.0'
        ],
        output='screen'
    )

    return LaunchDescription([
        start_gazebo_cmd,
        ros_ign_bridge_launch,  # 將橋接器加入啟動清單
        spawn_field_node
    ])