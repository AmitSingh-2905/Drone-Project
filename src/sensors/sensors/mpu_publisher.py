import rclpy
from rclpy.node import Node
from my_drone_interfaces.msg import Mpu
from mpu_data import *


class MpuData(Node):
    def __init__(self):
        super().__init__("mpudata")

        self.pub=self.create_publisher(Mpu,'/angles',10)
        self.msg=Mpu()

    



def main(args=None):
    rclpy.init(args=args)
    node=MpuData()
    while rclpy.ok():
        node.msg.angle_roll,node.msg.angle_pitch=mpu_msg()
        node.pub.publish(node.msg)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__=="__main__":
    main()
