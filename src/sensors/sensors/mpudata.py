from mpu_data import *
angleroll,anglepitch=mpu_msg()
for i in range(1000000):
    print(angleroll,anglepitch)