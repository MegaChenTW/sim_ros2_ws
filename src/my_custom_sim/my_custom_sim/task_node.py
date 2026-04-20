#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from example_interfaces.srv import Trigger
import time

# 建立一個輔助函數，用來生成 PoseStamped
def create_pose(navigator, x, y, yaw=0.0):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    # 這裡省略了四元數轉換，假設面向前方。正式環境建議用 tf_transformations 轉 yaw
    pose.pose.orientation.w = 1.0 
    return pose

def main(args=None):
    rclpy.init(args=args)

    # 1. 初始化 Nav2 導航器
    navigator = BasicNavigator()

    # 定義場地上的座標字典 (你需要根據你的 Gazebo 實體座標來修改)
    waypoints = {
        'a': create_pose(navigator, 0.5, 0.0),   # 預設起點/辨識區
        'b': create_pose(navigator, 0.53, 0.67),
        'c': create_pose(navigator, 1.08, -0.38),
        'd': create_pose(navigator, 0.52, -1.50)
    }

    # 等待 Nav2 系統完全啟動
    navigator.waitUntilNav2Active()

    # ==========================================
    # 任務一：前往 A 點
    # ==========================================
    print("🚀 任務開始：前往 A 點")
    navigator.goToPose(waypoints['a'])

    # 等待抵達 A 點
    while not navigator.isTaskComplete():
        time.sleep(0.5) # 不要讓迴圈把 CPU 吃滿

    if navigator.getResult() != TaskResult.SUCCEEDED:
        print("❌ 無法抵達 A 點，任務中止！")
        return

    print("✅ 已抵達 A 點！")

    # ==========================================
    # 任務二：呼叫 Service 獲取位址列表
    # ==========================================
    print("🔍 正在呼叫 /check_sign 獲取下一個目標...")
    
    # 建立一個臨時的 ROS Node 來發送 Service Request
    service_node = rclpy.create_node('temp_service_client')
    client = service_node.create_client(Trigger, 'check_sign')
    
    while not client.wait_for_service(timeout_sec=1.0):
        print('等待 /check_sign service 上線中...')
        
    req = Trigger.Request()
    future = client.call_async(req)
    # 阻塞等待 Service 回傳
    rclpy.spin_until_future_complete(service_node, future)
    
    response = future.result()
    service_node.destroy_node() # 用完即丟

    if not response.success:
        print("❌ 視覺辨識失敗！")
        return

    # 解析回傳的字串 "b,c,d" 變成 list ['b', 'c', 'd']
    address_list = response.message.split(',')
    print(f"🎯 獲取目標列表：{address_list}")

    # ==========================================
    # 任務三：遍歷列表，依序前往
    # ==========================================
    for target in address_list:
        if target not in waypoints:
            print(f"⚠️ 找不到目標 {target} 的座標，跳過！")
            continue

        print(f"🚀 正在前往目標：{target}")
        navigator.goToPose(waypoints[target])

        while not navigator.isTaskComplete():
            # 你可以在這裡加入取消條件，例如遇到緊急狀況
            time.sleep(0.5)

        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"✅ 成功抵達 {target}")
        elif result == TaskResult.CANCELED:
            print(f"⚠️ 前往 {target} 的任務被取消")
        elif result == TaskResult.FAILED:
            print(f"❌ 無法抵達 {target}")

    print("🎉 所有任務執行完畢！")
    rclpy.shutdown()

if __name__ == '__main__':
    main()