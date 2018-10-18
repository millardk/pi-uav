from altimu10v5.lsm6ds33 import LSM6DS33
from altimu10v5.lps25h import LPS25H
from altimu10v5.lis3mdl import LIS3MDL
from time import sleep

lsm6ds33 = LSM6DS33()
lsm6ds33.enable()

lps25h = LPS25H()
lps25h.enable()

lis3mdl = LIS3MDL()
lis3mdl.enable()

while True:
    print(lsm6ds33.get_accelerometer_g_forces())
    print(lsm6ds33.get_gyro_angular_velocity())
    print(lps25h.get_barometer_raw())
    print(lis3mdl.get_magnetometer_raw())
    
    sleep(1)