import smbus  
import math
import time
import mpu
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
g = 9.80665
bus = smbus.SMBus(1)
Device_Address = 0x68

def mpu_init():
	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)
        
def read_raw_data(addr):

	#Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    
    #concatenate higher and lower value
    value = ((high << 8) | low)
        
    #to get signed value from mpu6050
    if(value > 32768):
                value = value - 65536
    return value

def gyro_calibration(self):

    for rate_calibration_number in  range(0,2001):

        self.RateCalibrationRoll += mpu.gyro[0]
        self.RateCalibrationPitch +=mpu.gyro[1]
        self.RateCalibrationYaw +=mpu.gyro[2]

        rate_calibration_number += 1

        time.sleep(0.001)
    self.RateCalibrationRoll /= 2000
    self.RateCalibrationPitch /= 2000
    self.RateCalibrationYaw /= 2000


def mpu_msg():

    # while True:
	    #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)
        
        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)
        
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        AccX = (acc_x/16384.0)*g
        AccY = (acc_y/16384.0)*g
        AccZ = (acc_z/16384.0)*g
        
        RateRoll = gyro_x/131.0
        RatePitch = gyro_y/131.0
        RateYaw = gyro_z/131.0

        AngleRoll = math.atan(AccY/math.sqrt(AccX**2+AccZ**2))*(180/math.pi)
        AnglePitch = math.atan(AccX/math.sqrt(AccY**2+AccZ**2))*(180/math.pi)
        print(AngleRoll,AnglePitch)
      
        return AngleRoll,AnglePitch
        

