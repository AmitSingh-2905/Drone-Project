import time
import rclpy
from rclpy.node import Node
from my_drone_interfaces.msg import Bmp180
from bmpsensor import *
import subprocess



# Call the function whenever your code runs



class Bmp(Node):
    def __init__(self):
        super().__init__("bmp180")
        self.altitude=Bmp180()
        self.publisher=self.create_publisher(Bmp180,'/altitude',10)
        
            
def main(args=None):
    rclpy.init(args=args)
    node=Bmp()
    while rclpy.ok():
        t,_,node.altitude.altitude=readBmp180()

        node.publisher.publish(node.altitude)
        print(node.altitude.altitude)

    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()


 
if __name__=="__main__":
    main()

