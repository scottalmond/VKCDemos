"""
   Copyright 2018 Scott Almond
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
     http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
Purpose: 
Command LittleArm Big, and camera mount, servos
Usage:
troubleshoot i2c device addresses:
i2cdetect -y 1
run main program:
python3 pwm.py
Connections:
servos on channels 0 and 1 on PWM Adafruit HAT
brown wire is GND
red is VCC
orange is signal
DMM on channel 2
channel 3 to ENABLE pin on H-bridge
other h-bridge connections are per discrete.py
"""

class PWM:
	
	PWM_FREQUENCY_HZ=60 #frequency at which updates are sent to all servos
	I2C_ADDRESS=0x40
	I2C_REGISTER_MODE1=0x00
	I2C_REGISTER_PRESCALE=0xFE
	I2C_REGISTER_LED0_ON_L = 0x06
	I2C_REGISTER_LED0_ON_H = 0x07
	I2C_REGISTER_LED0_OFF_L = 0x08
	I2C_REGISTER_LED0_OFF_H = 0x09
	
	def __init__(self):
		self.initInterface()
		
	def initInterface(self):
		import wiringpi as wpi
		self.wpi=wpi
		self.wpi.wiringPiSetupPhys()
		self.file_descriptor=wpi.wiringPiI2CSetup(self.I2C_ADDRESS)
		self.set_pwm_freq(self.PWM_FREQUENCY_HZ)
		
	#configuration helper function
	# sets the frequency of the PWM control duty cycle
	# as well as performs initial boot up of the pwm hat chip
	def set_pwm_freq(self, freq_hz):
		import math
		import time
		#paragraph 7.3.5, PCA9685.pdf:
		prescaleval = 25000000.0    # 25MHz
		prescaleval /= 4096.0       # 12-bit
		prescaleval /= float(freq_hz)
		prescaleval -= 1.0
		prescale = int(math.floor(prescaleval + 0.5))
		#paragraph 7.3.1.1, PCA9685.pdf:
		#put to sleep so prescale can be written
		oldmode=self.wpi.wiringPiI2CReadReg8(self.file_descriptor,self.I2C_REGISTER_MODE1)
		newmode_3=oldmode | 0x10
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_MODE1, newmode_3)
		#set prescale
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_PRESCALE, prescale)
		#1. read MODE1 register
		oldmode=self.wpi.wiringPiI2CReadReg8(self.file_descriptor,self.I2C_REGISTER_MODE1)
		print("PWM.set_pwm_freq: oldmode: ",bin(oldmode))
		#2. check that bit 7 (RESTART) is a logic 1
		#If it is clear bit 4 (SLEEP)
		newmode = oldmode & 0xEF #1110 1111 --> clear bit 4
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_MODE1, newmode)
		#Allow time for oscillator to stabalize (500 us)
		time.sleep(500.0e-6) #500 us
		#3. write logic 1 to bit 7 of MODE1 register.  All PWM channels will restart and the RESTART bit will clear
		newmode_2 = newmode | 0x80 #1000 0000 --> set bit 4 HIGH
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_MODE1, newmode_2)
		
	#low-level helper function
	#each command requires three inputs: a channel [0,15]
	# an on_counts (number of prescale ticks before channel goes HIGH)
	# and off_counts (number of prescale ticks before channel goes LOW) - measured from START, NOT from after the transition HIGH
	# reference PCA9658 documentation for timing details
	def set_pwm(self, channel, on_counts, off_counts): #from adafruit PCA9685.py, modified for wpi
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_LED0_ON_L+4*channel, on_counts & 0xFF)
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_LED0_ON_H+4*channel, on_counts >> 8)
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_LED0_OFF_L+4*channel, off_counts & 0xFF)
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_LED0_OFF_H+4*channel, off_counts >> 8)
	
	#given a channel in the range [0,15]
	# given an angle in the range [0.0,180.0]
	# set the PWM control for the servo
	def set_servo(self,channel,angle_degrees):
		ratio=angle_degrees/180.0
		servo_min=150
		servo_max=600
		counts=int(ratio*(servo_max-servo_min)+servo_min)
		self.set_pwm(channel,0,counts)
	
	#given a ratio between [0,1], set the PWM output with corresponding duty cycle
	def set_dimmer(self,channel,ratio):
		if(ratio<=0.0): #special values when ALWAYS ON or ALWAYS OFF
			self.set_pwm(channel,0,4096)
		elif(ratio>=1.0):
			self.set_pwm(channel,4096,0)
		else:
			self.set_pwm(channel,0,int(4096*ratio))#int varies between (0,4096)
		
	#enable sleep bit	
	def dispose(self):
		oldmode=self.wpi.wiringPiI2CReadReg8(self.file_descriptor,self.I2C_REGISTER_MODE1)
		newmode_3=oldmode | 0x10
		self.wpi.wiringPiI2CWriteReg8(self.file_descriptor,self.I2C_REGISTER_MODE1, newmode_3)
	
	#note channels will retain last state upon program exit
	@staticmethod
	def build_test(loop_count):
		print("PWM Build Test...")
		print("Instantiate PWM class...")
		pwm=PWM()
		print("PWM file_descriptor: ",pwm.file_descriptor)
		print("Run movement/dimming test...")
		import time
		servo_list=[0,1]
		dimmer_list=[8]
		while(not loop_count==0):
			for servo_channel in servo_list:
				for angle_degrees in [70,110,90]:
					print('PWM set servo: ',servo_channel,' to ',angle_degrees,' degrees')
					pwm.set_servo(servo_channel,angle_degrees)
					time.sleep(2)
			for dimmer_channel in dimmer_list:
				for dim_level in [1.0,0.9,0.3,0.1,0.0]:#3.3V, 2.97V, 0.99V, 0.33V, 0.0V
					print('PWM set channel: ',dimmer_channel,' to ',int(dim_level*1000)/10.0,' %')
					pwm.set_dimmer(dimmer_channel,dim_level)
					time.sleep(2)
			loop_count-=1
		pwm.dispose()
		
	@staticmethod
	def build_test_2():
		#move hand servo
		import time
		pwm=PWM()
		servo_channel=3
		angle_degrees=-100
		while(angle_degrees<1000):
			
		#for angle_degrees in range(1):#[0:10:180]:
			print(angle_degrees)
			pwm.set_servo(servo_channel,angle_degrees)
			time.sleep(0.2)
			angle_degrees+=10
		

if __name__ == "__main__":
	print("START")
	loop_count=1#-1 for infinite loop
	PWM.build_test(loop_count)
	#PWM.build_test_2()
	print("DONE")
