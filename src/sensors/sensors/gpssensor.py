from gps import *
import time
import serial

running = True


def getPositionData(gps):
    nx = gps.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        
        
        
        
        print ("Your position: lon = " + str(longitude) + ", lat = " + str(latitude))
        # prev_lat=latitude
    
        return latitude,longitude 
       
            
    else:
        return 1,2
        # latitude = getattr(nx,'lat', "Unknown")
        # 
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

try:
    print("Application started!")
    while running:
        
       latitude,longitude=getPositionData(gpsd)
       if latitude!=1 and longitude !=2:
           latitude,longitude=getPositionData(gpsd)
           print(latitude,longitude)
           
        # print(latitude,longitude)
        # time.sleep(1.0)

except (KeyboardInterrupt):
    running = False
    print ("Applications closed!")
