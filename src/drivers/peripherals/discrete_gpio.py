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
		
	#precon: pin must first be declared an input
	def digitalRead(self,pin_number):
		return self.wpi.digitalRead(pin_number)

	#ref. https://www.jameco.com/Jameco/workshop/circuitnotes/raspberry_pi_circuit_note_fig2a.jpg
	#LED 1: pin 1 (3.3V) to pin 39 (GND)
	#LED 2: pin 7 (GPIO 4) to pin 39 (GND)
	#LED 3: pin 11 (GPIO 17) to pin 39 (GND)
	#Button 1: pin 16 (GPIO 23)
	#Button 2: pin 18 (GPIO 24)
	#//LED 3: pin 11 (GPIO 7) to pin pin 16 (GPIO 23)
	#//LED 4: pin pin 16 (GPIO 23) to pin 11 (GPIO 7) 
	def build_test(self):
		print("-- Discrete demo start --")
		# -- configure --
		import time
		PIN_LED_1=7
		PIN_LED_2=11
		PIN_BUTTON_1=16
		PIN_BUTTON_2=18
		self.pinMode(pin_number=PIN_LED_1,is_input=False,is_pull_up=None)
		self.pinMode(pin_number=PIN_LED_2,is_input=False,is_pull_up=None)
		self.pinMode(pin_number=PIN_BUTTON_1,is_input=True,is_pull_up=True)
		self.pinMode(pin_number=PIN_BUTTON_2,is_input=True,is_pull_up=True)
			
		print("-- Discrete toggle LED demo --")
		for iter in range(4):
			self.digitalWrite(PIN_LED_1,1)
			self.digitalWrite(PIN_LED_2,0)
			print("  Toggle 1 is ON,  Toggle 2 is OFF")
			time.sleep(1)
			self.digitalWrite(PIN_LED_1,0)
			self.digitalWrite(PIN_LED_2,1)
			print("  Toggle 1 is OFF, Toggle 2 is ON")
			time.sleep(1)
			self.digitalWrite(PIN_LED_1,0)
			self.digitalWrite(PIN_LED_2,0)
			print("  Toggle 1 is OFF, Toggle 2 is OFF")
			time.sleep(1)
			
		#TODO: add button reading (input) to this demo
			
		# -- clean up --
		self.digitalWrite(PIN_LED_1,0)
		self.digitalWrite(PIN_LED_2,0)
		print("  All LEDs are OFF")
		
		print("  Press breadboard buttons to control lights (Ctrl+C to exit)")
		while(True):
			#buttons have an internal pull-up
			#  they will read 1 if the button is NOT pressed, and 0 when pressed
			#  so to have LED respond when button is pressed, negate the result of a button read operation
			self.digitalWrite(PIN_LED_1,not self.digitalRead(PIN_BUTTON_1))
			self.digitalWrite(PIN_LED_2,not self.digitalRead(PIN_BUTTON_2))
		
		print("-- Discrete demo done --")
		

#build test executes when "python3 Discrete.py" is called
#  from the command line, but not when another Python class
#  "import Discrete from Discrete"
if __name__ == "__main__":
	from support_library import Support
	support=Support()
	discrete=Discrete(support)
	discrete.build_test()
