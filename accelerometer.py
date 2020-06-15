import smbus
import math
from time import sleep

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


def init():
	#write to sample rate register
	bus.write_byte_data(device_address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(device_address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(device_address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(device_address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(device_address, INT_ENABLE, 1)

def read_raw_data(addr):
	#Accelero and Gyro value are 16-bit
	high = bus.read_byte_data(device_address, addr)
	low = bus.read_byte_data(device_address, addr+1)

	#concatenate higher and lower value
	value = ((high << 8) | low)
	
	#to get signed value from mpu6050
	if(value > 32768):
			value = value - 65536
	return value


bus = smbus.SMBus(1)
# MPU6050 device address
device_address = 0x68

init()

def get_value():
	#Read Accelerometer raw value
	acc_x = read_raw_data(ACCEL_XOUT_H)
	acc_y = read_raw_data(ACCEL_YOUT_H)
	acc_z = read_raw_data(ACCEL_ZOUT_H)
	
	#Full scale range +/- 250 degree/C as per sensitivity scale factor
	ax = acc_x/16384.0
	ay = acc_y/16384.0
	az = acc_z/16384.0
	
	acc = math.sqrt(ax*ax + ay*ay + az*az)
	return acc * 9.8


if __name__ == "__main__":
	while True:
		print(get_value())
		sleep(0.1)