#guide: https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring
#precon: sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
#GPIO18 is pin 12 on RPi 
class LED:
	def __init__(self,led_count):
		self.initInterface(led_count)
		
	def initInterface(self,led_count):
		import board
		import neopixel
		import time
		self.order=neopixel.GRB
		self.neopixel=neopixel
		self.led_count=led_count
		self.pixels = neopixel.NeoPixel(board.D18, led_count)#pin GPIO18 output
		self.time=time
		
	def wheel(self,pos):
		# Input a value 0 to 255 to get a color value.
		# The colours are a transition r - g - b - back to r.
		if pos < 0 or pos > 255:
			r = g = b = 0
		elif pos < 85:
			r = int(pos * 3)
			g = int(255 - pos*3)
			b = 0
		elif pos < 170:
			pos -= 85
			r = int(255 - pos*3)
			g = 0
			b = int(pos*3)
		else:
			pos -= 170
			r = 0
			g = int(pos*3)
			b = int(255 - pos*3)
		return (r, g, b) if self.order == self.neopixel.RGB or self.order == self.neopixel.GRB else (r, g, b, 0)
	 
	def rainbow_cycle(self,wait):
		for j in range(255):
			for i in range(self.led_count):
				pixel_index = (i * 256 // self.led_count) + j
				self.pixels[i] = self.wheel(pixel_index & 255)
			self.pixels.show()
			self.time.sleep(wait)
	 
	def display_time(self):
		time_seconds=self.time.time()
		time_us=int(time_seconds*1e3)
		for led_index in range(0,self.led_count):
			if(0x01 & time_us):
				self.pixels[led_index]=self.wheel((270-led_index*6) & 255)
			else:
				self.pixels[led_index]=(0,0,0)
			time_us=time_us>>1
		self.pixels.show()
	 
	def build_test(self):
		print("-- LED demo start --")
		print("All LEDs Red")
		self.pixels.fill((255, 0, 0)) #all red
		self.pixels.show() #always need to flush changes live to hardware when done setting pixels
		self.time.sleep(1) #wait 1 second
	 
		print("All LEDs Green")
		self.pixels.fill((0, 255, 0)) #all green
		self.pixels.show()
		self.time.sleep(1)
	 
		print("All LEDs Blue")
		self.pixels.fill((0, 0, 255)) #all blue
		self.pixels.show()
		self.time.sleep(1)
	 
		print("All LEDs White")
		self.pixels.fill((255, 255, 255)) #all white
		self.pixels.show()
		self.time.sleep(1)
	 
		print("Rainbow")
		self.rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step
		
		print("Binary counter")
		RUN_TIME_SEC=5
		time_start_sec=self.time.time()
		while((time_start_sec+RUN_TIME_SEC)>self.time.time()):
			self.display_time()
		
		self.pixels.fill((0, 0, 0)) #cleanup by turning all LEDs OFF
		print("-- LED demo done --")
		
if __name__ == "__main__":
	leds=LED(30)
	leds.build_test()
		
