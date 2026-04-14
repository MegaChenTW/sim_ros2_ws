cmake_minimum_required(VERSION 3.8)
project(block_A_description) # 例如: project(Field_description)

# 尋找 ROS 2 的編譯工具
find_package(ament_cmake REQUIRED)

# 告訴 ROS 2 要把 meshes 和 urdf 資料夾安裝到系統中
install(
  DIRECTORY meshes urdf
  DESTINATION share/${PROJECT_NAME}
)

# 安裝 package.xml
install(
  FILES package.xml
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
