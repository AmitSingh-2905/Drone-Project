import rclpy
from rclpy.node import Node
from my_drone_interfaces.msg import GpsData
# from gpssensor import *
import subprocess
from gps import *

def run_gpsd():
    command="sudo gpsd /dev/serial0 -F /var/run/gpsd.sock"
    subprocess.run(command,shell=True)
    print("i am here")

def getPositionData(gps):
    
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        
        
        # print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        return latitude,longitude
    else:
        return 1.0,2.0
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
class Gps(Node):
    def __init__(self):
        super().__init__('gps')
        

        self.pub=self.create_publisher(GpsData,'/gpsdata',10)
        self.msg=GpsData()
        run_gpsd()
    def get_valid_position_data(self):
        
        
            latitude, longitude = getPositionData(gpsd)
            
            
            return latitude, longitude   
    

def main(args=None):
    rclpy.init(args=args)
    node =Gps()
    while rclpy.ok():
        latitude, longitude = node.get_valid_position_data()
        if latitude!="Unknown" and longitude!="Unknown" :
            node.msg.latitude = float(latitude)
            node.msg.longitude = float(longitude)
            
            node.pub.publish(node.msg)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()
