#Class for reading/writing GPIO pins on RPi
#RPi pinout: https://myelectronicslab.com/wp-content/uploads/2016/06/raspbery-pi-3-gpio-pinout-40-pin-header-block-connector-1-1.png
#precon: execute "pip3 install wiringpi"
#Python3 wrapper for WiringPi library: https://github.com/WiringPi/WiringPi-Python
#Underlying WiringPi C library: http://wiringpi.com/
#precon: beware assigning multiple pins to the same function, ex physcial pin 3 to both GPIO and I2C
class Discrete:
	def __init__(self,support):
		#One design philosophy is to always separate your initialization code from
		#  your class constructor so that you can call your initialization code
		#  again later without having to create a new class instance
		self.initInterface(support)
		
	def initInterface(self,support):
		self.wpi=support.wpi
		#use physical pin numbering, ie pin 1 is 3.3V, pin 39 is ground, pin 7 is GPIO4

	#pin_number is pyhiscal pin number on RPi, ie pin 7 is GPIO4
	#is_input is True for pins used to read inputs, false for sending signals as output
	#is_pull_up, for input pins, this configures the RPi internal resistors
	#  to weakly pull the signal to VCC (3.3V) in the absense of any external input
	#  set to false to weakly drive to ground (0V), or None to disable resistors
	#  (allow input to float).  Value is ignored for output pins
	def pinMode(self,pin_number,is_input,is_pull_up=None):
		self.wpi.pinMode(pin_number,self.wpi.INPUT if is_input else self.wpi.OUTPUT)
		if(is_input):
			if(is_pull_up is None): pud=self.wpi.PUD_OFF
			elif(is_pull_up): pud=self.wpi.PUD_UP
			else: pud=self.wpi.PUD_DOWN
			self.wpi.pullUpDnControl(pin_number,pud)
	
	#simple pass through method to underlying library to write the value (1 = 3.3V, or 0 = 0V)
	#  to the spefied pin.
	#Precon: pin must first be declared an output before using this method
	def digitalWrite(self,pin_number,value):
		self.wpi.digitalWrite(pin_number,value)

	#LED 1: pin 1 (3.3V) to pin 39 (GND)
	#LED 2: pin 7 (GPIO 4) to pin 39 (GND)
	#LED 3: pin 11 (GPIO 7) to pin pin 16 (GPIO 23)
	#LED 4: pin pin 16 (GPIO 23) to pin 11 (GPIO 7) 
	def build_test(self):
		print("-- Discrete demo start --")
		# -- configure --
		import time
		PIN_BLINK=7
		PIN_TOGGLE_1=11
		PIN_TOGGLE_2=16
		self.pinMode(PIN_BLINK,False)
		self.pinMode(PIN_TOGGLE_1,False)
		self.pinMode(pin_number=PIN_TOGGLE_2,is_input=False)#Another more explicit way of passing parameters to methods in Python

		print("-- Discrete blink LED demo --")
		for iter in range(4):
			self.digitalWrite(PIN_BLINK,1) #write 1 = 3.3V
			print("  LED on PIN "+str(PIN_BLINK)+" is ON")
			time.sleep(1) #sleep 1 second
			self.digitalWrite(PIN_BLINK,0) #turn LED OFF
			print("  LED on PIN "+str(PIN_BLINK)+" is OFF")
			time.sleep(1)
			
		print("-- Discrete toggle LED demo --")
		for iter in range(4):
			self.digitalWrite(PIN_TOGGLE_1,1)
			self.digitalWrite(PIN_TOGGLE_2,0)
			print("  Toggle 1 is ON,  Toggle 2 is OFF")
			time.sleep(1)
			self.digitalWrite(PIN_TOGGLE_1,0)
			self.digitalWrite(PIN_TOGGLE_2,1)
			print("  Toggle 1 is OFF, Toggle 2 is ON")
			time.sleep(1)
			
		#TODO: add button reading (input) to this demo
			
		# -- clean up --
		self.digitalWrite(PIN_TOGGLE_1,0)
		self.digitalWrite(PIN_TOGGLE_2,0)
		print("  All LEDs are OFF")
		print("-- Discrete demo done --")
		

#build test executes when "python3 Discrete.py" is called
#  from the command line, but not when another Python class
#  "import Discrete from Discrete"
if __name__ == "__main__":
	from support_library import Support
	support=Support()
	discrete=Discrete(support)
	discrete.build_test()
