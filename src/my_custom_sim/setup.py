import os
from glob import glob
from setuptools import setup

package_name = 'my_custom_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
        # ▼▼▼ 重點新增這裡 ▼▼▼
        # 將 launch 資料夾內的所有 .py 檔，安裝到 share/my_custom_sim/launch 底下
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
        
        # 將 worlds 資料夾內的所有 .world 檔，安裝到 share/my_custom_sim/worlds 底下
        (os.path.join('share', package_name, 'worlds'), glob(os.path.join('worlds', '*.world'))),
        # ▲▲▲ 重點新增這裡 ▲▲▲
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mega',
    maintainer_email='mega@todo.todo',
    description='My custom simulation environment for JetRover',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'task_node = my_custom_sim.task_node:main',
            'dummy_node = my_custom_sim.dummy_node:main',
        ],
    },
)
