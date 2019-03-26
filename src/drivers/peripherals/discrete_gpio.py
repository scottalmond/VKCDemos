class Discrete:
	def __init__(self):
		#One design philosophy is to always separate your initialization code from
		#  your class constructor so that you can call your initialization code
		#  again later without having to create a new class instance
		self.initInterface()
		
	def initInterface(self):
		#I find it problematic to use the defaul Python approach of performing all imports
		#globally (before the class definition).
		#This causes confusion later in a large (especially multi-threaded) 
		#projects when it's unclear which class is performing the import,
		#what the scope of the library is, etc.  I favor performing the import explictly
		#within the constructor and accessing it directly through self.<library>
		import wiringpi as wpi
		self.wpi=wpi
		#use physical pin numbering, ie pin 1 is 3.3V, pin 39 is ground, pin 7 is GPIO4
		self.wpi.wiringPiSetupPhys()

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

	def build_test(self):
		print("-- Discrete demo start --")
		
		# -- configure --
		import time
		PIN_BLINK=7
		PIN_TOGGLE_1=11
		PIN_TOGGLE_2=16
		discrete=Discrete()
		discrete.pinMode(PIN_BLINK,False)
		discrete.pinMode(PIN_TOGGLE_1,False)
		discrete.pinMode(pin_number=PIN_TOGGLE_2,is_input=False)#Another more explicit way of passing parameters to methods in Python

		print("-- Discrete blink LED demo --")
		for iter in range(4):
			discrete.digitalWrite(PIN_BLINK,1) #write 1 = 3.3V
			time.sleep(1) #sleep 1 second
			discrete.digitalWrite(PIN_BLINK,0) #turn LED OFF
			time.sleep(1)
			
		print("-- Discrete toggle LED demo --")
		for iter in range(4):
			discrete.digitalWrite(PIN_TOGGLE_1,1)
			discrete.digitalWrite(PIN_TOGGLE_2,0)
			time.sleep(1)
			discrete.digitalWrite(PIN_TOGGLE_1,0)
			discrete.digitalWrite(PIN_TOGGLE_2,1)
			time.sleep(1)
			
		# -- clean up --
		discrete.digitalWrite(PIN_TOGGLE_1,0)
		discrete.digitalWrite(PIN_TOGGLE_2,0)
		print("-- Discrete demo done --")
		

#build test executes when "python3 Discrete.py" is called
#  from the command line, but not when another Python class
#  "import Discrete from Discrete"
if __name__ == "__main__":
	discrete=Discrete()
	discrete.build_test()
