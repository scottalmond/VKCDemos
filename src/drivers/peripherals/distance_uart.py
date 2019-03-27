
#class for interfacing with TFMini Distance Sensor UART
#  for RPi
#spec sheet: https://cdn.sparkfun.com/assets/5/e/4/7/b/benewake-tfmini-datasheet.pdf
#product page: https://www.sparkfun.com/products/14588
#C driver: https://github.com/opensensinglab/tfmini/blob/master/src/TFMini.cpp
#TODO precon? disable uart acting as serial console... https://raspberry-projects.com/pi/command-line/io-pins-command-line/uart-transmit-from-the-command-line
class Distance:
	TFMINI_MAXBYTESBEFOREHEADER=30
	def __init__(self,support):
		serial_name='/dev/ttyS0'
		serial_baud=115200
		self.initInterface(support,serial_name,serial_baud)
		
	def initInterface(self,support,serial_name,serial_baud):
		self.serial=support.serial
	
	def setStandardOutputMode(self):
		print('send 7 bytes')
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x01,0x06])
		
	def setConfigMode(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x00,0x01,0x02])
		
	def setSingleScanMode(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x00,0x00,0x40])
		
	def externalTrigger(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x00,0x00,0x41])
	
	def takeMeasurement(self):
		#1. wait for serial header
		numCharsRead = 0
		lastChar = 0x00
		str_cat=""
		endChar='Y'
		while(1):
			curChar=self.__read_str()
			if(not curChar is None):
				str_cat+=curChar
				if(lastChar==endChar and curChar==endChar):
					break;
				else:
					lastChar=curChar
					numCharsRead+=1
			if(numCharsRead>self.TFMINI_MAXBYTESBEFOREHEADER):
				print(self.__str2hex(str_cat))
				raise Exception("No TFMini header found")
				return -1
		#2. Read one frame from target
		
		return 0
			
	def __str2hex(self,s):
		return ":".join("{:02x}".format(ord(c)) for c in s)
			
	def __read_byte(self):
		if(self.serial.inWaiting()):
			return self.serial.read()
		return None
			
	def __read_str(self):
		out=self.__read_byte()
		if(out is None): return out
		try:
			return str(out,'utf-8')
		except UnicodeDecodeError:
			pass
		return None
			
	def uart_test(self):
		print("-- UART test start --")
		# -- configure --
		import time
		
		RUN_TIME_SEC=5
		time_start_sec=time.time()
		while((time_start_sec+RUN_TIME_SEC)>time.time()):
			this_str=""
			while(self.serial.inWaiting()):
				try:
					this_char=str(self.serial.read(),'utf-8')
					this_str+=this_char
				except UnicodeDecodeError:
					print("error")
			if(len(this_str)>0):
				print(this_str,end='')
				self.serial.write([0x65,0x66])#write 'ef' to UART
		print("-- UART test done --")
		
	
	#red wire to 5V (pin 2)
	#black to GND (pin 39)
	#white TFMini RX, RPi TX (pin 8)
	#green TFMini TX, RPi RX (pin 10)
	def build_test(self):
		print("-- TFMini distance demo start --")
		# -- configure --
		import time
		
		RUN_TIME_SEC=5
		time_start_sec=time.time()
		while((time_start_sec+RUN_TIME_SEC)>time.time()):
			self.setStandardOutputMode()
			dist=self.takeMeasurement()
			time.sleep(1)
		
		
		print("-- TFMini discrete demo done --")

if __name__ == "__main__":
	from support_library import Support
	support=Support()
	distance=Distance(support)
	distance.uart_test()
	support.dispose()
