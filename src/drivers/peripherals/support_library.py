class Support:
	SERIAL_ADDRESS='/dev/ttyS0'
	UART_BAUD_RATE=115200
	#I find it problematic to use the default Python approach of performing all imports
	#globally (before the class definition).
	#This causes confusion later in a large (especially multi-threaded) 
	#projects when it's unclear which class is performing the import,
	#what the scope of the library is, etc.  I favor performing the import explictly
	#within the constructor and accessing it directly through self.<library>
	def __init__(self):
		import wiringpi as wpi
		self.wpi=wpi
		self.wpi.wiringPiSetupPhys()
		
		import serial
		self.serial=serial.Serial(self.SERIAL_ADDRESS,self.UART_BAUD_RATE,timeout=0.1)

	#close open wiringPi and Serial connections
	def dispose(self):
		self.serial.close()
