
#class for interfacing with TFMini Distance Sensor UART
#  for RPi
#spec sheet: https://cdn.sparkfun.com/assets/5/e/4/7/b/benewake-tfmini-datasheet.pdf
#product page: https://www.sparkfun.com/products/14588
#C driver: https://github.com/opensensinglab/tfmini/blob/master/src/TFMini.cpp
#TODO precon? disable uart acting as serial console... https://raspberry-projects.com/pi/command-line/io-pins-command-line/uart-transmit-from-the-command-line
class Distance:
	TFMINI_MAXBYTESBEFOREHEADER=30
	TFMINI_FRAME_SIZE=7
	def __init__(self,support):
		serial_name='/dev/ttyS0'
		serial_baud=115200
		self.initInterface(support,serial_name,serial_baud)
		
	def initInterface(self,support,serial_name,serial_baud):
		self.serial=support.serial
	
	def setStandardOutputMode(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x01,0x06])
		
	def setConfigMode(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x00,0x01,0x02])
		
	def setSingleScanMode(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x00,0x00,0x40])
		
	def externalTrigger(self):
		self.serial.write([0x42,0x57,0x02,0x00,0x00,0x00,0x00,0x41])
	
	def takeMeasurement(self):
		self.serial.reset_input_buffer()#flush current contents of input buffer to minize issue of stale data
		#1. wait for serial header
		numCharsRead = 0
		lastChar = 0x00
		str_cat=""
		endChar=b'Y'
		while(1):
			curChar=self.__read_byte()
			if(not curChar is None):
				if(lastChar==endChar and curChar==endChar):
					break;
				else:
					lastChar=curChar
					numCharsRead+=1
			if(numCharsRead>self.TFMINI_MAXBYTESBEFOREHEADER):
				raise Exception("No TFMini header found")
				return -1
		#2. Read one frame from target
		byte_list=bytearray()
		checksum=0x59+0x59
		for rep in range(0,self.TFMINI_FRAME_SIZE):
			while(not self.serial.inWaiting()): pass #wait for byte to be available
			read_byte=self.__read_byte()[0]
			byte_list.append(read_byte)
			if(rep<(self.TFMINI_FRAME_SIZE-2)):
				checksum+=byte_list[rep]
		checksum%=256
		#verify checksum
		if(checksum!=byte_list[self.TFMINI_FRAME_SIZE-1]):
			raise ValueError("Invalid TFMini checksum: "+str(checksum)+" vs "+str(byte_list[self.TFMINI_FRAME_SIZE-1]))
		#unpack data into human-readable format
		distance_cm=(byte_list[1]<<8)+byte_list[0]
		strength=(byte_list[3]<<8)+byte_list[2]
		return distance_cm,strength
			
	def __str2hex(self,s):
		return ":".join("{:02x}".format(ord(c)) for c in s)
			
	def __read_byte(self):
		if(self.serial.inWaiting()):
			return self.serial.read()
		return None #no byte to read OR timeout.  TODO: deal with timeouts
			
	def __read_str(self):
		out=self.__read_byte()
		if(out is None): return out
		try:
			return str(out,'utf-8')
		except UnicodeDecodeError:
			pass
		return None
			
	def uart_loopback_test(self):
		print("-- UART loopback test start --")
		# -- configure --
		import time
		RUN_TIME_SEC=3
		MESSAGE_DURATION_SEC=1
		time_start_sec=time.time()
		last_message_sec=0
		bytes_found=0
		while((time_start_sec+RUN_TIME_SEC)>time.time()):
			if((last_message_sec+MESSAGE_DURATION_SEC)<time.time()):
				#if more than 1 second has elapsed since last message, then send one
				self.serial.write('Loopback Test: PASS\n'.encode())
				last_message_sec=time.time()
			if(self.serial.inWaiting()):
				this_char=self.__read_str()
				if(not this_char is None):
					print(this_char,end='')
					bytes_found+=1
		if(bytes_found<=0):
			print("Loopback Test: FAIL")
		print("-- UART loopback test done --")
			
	def uart_arduino_test(self):
		print("-- UART Arduino test start --")
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
		print("-- UART Arduino test done --")
		
	
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
			distance_cm,strength=self.takeMeasurement()
			print("Distance: "+str(distance_cm)+" cm, strength: "+str(strength))
			#time.sleep(1)
		
		
		print("-- TFMini discrete demo done --")

if __name__ == "__main__":
	from support_library import Support
	support=Support()
	distance=Distance(support)
	distance.build_test()
	support.dispose()
