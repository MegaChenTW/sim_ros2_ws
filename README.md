# sim for robosot

1. issue: teb沒有release:

其實應該自己build的，可是因為熟習所以把nav2_param.yaml和navigation.launch.py更換了controller server成
dwb

# TO run
```bash
ros2 launch my_custom_sim start_my_sim.launch.py
# another terminal
ros2 launch robot_gazebo navigation.launch.py map:=RobotSot use_sim_time:=True
```
# 4/20 mod

加入keepout，用Mega Mod查詢

## problem

一碰到keepout就停下