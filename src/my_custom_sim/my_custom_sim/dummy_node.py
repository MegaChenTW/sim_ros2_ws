#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger

class DummySignNode(Node):
    def __init__(self):
        super().__init__('dummy_sign_node')
        # 建立一個 Service Server，名稱為 check_sign
        self.srv = self.create_service(Trigger, 'check_sign', self.check_sign_callback)
        self.get_logger().info('假的視覺辨識 Service (/check_sign) 已經啟動！')

    def check_sign_callback(self, request, response):
        self.get_logger().info('收到辨識請求，正在假裝處理...')
        
        # 假裝辨識出要前往的地點 b, c, d
        response.success = True
        response.message = "b,c,d"  # 這裡用字串傳遞，之後你可以換成自訂的 srv 陣列
        
        self.get_logger().info(f'辨識完成，回傳目標列表: {response.message}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = DummySignNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()