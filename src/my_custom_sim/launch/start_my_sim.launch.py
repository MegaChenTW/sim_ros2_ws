import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

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
            'moveit_unite': 'true'
        }.items()
    )

    # 2. 指定你的 場地 Xacro 檔案路徑
    field_xacro_path = os.path.join(field_dir, 'urdf', 'Field.xacro')

    # 3. 使用 xacro 套件將 .xacro 動態轉換為純 URDF 格式的 XML 字串
    field_urdf_xml = xacro.process_file(field_xacro_path).toxml()

    # 4. 使用「新版 Gazebo (ros_gz_sim)」的生成節點，而非舊版的 gazebo_ros
    spawn_field_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_field',
            '-string', field_urdf_xml,  # 直接傳入轉換好的 XML 字串
            '-x', '0.0', 
            '-y', '0.0', 
            '-z', '0.0'
        ],
        output='screen'
    )

    return LaunchDescription([
        start_gazebo_cmd,
        spawn_field_node
    ])