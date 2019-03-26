class Demo:
	def __init__(self):
		self.initialize()
		
	def initialize(self):
		from peripherals.discrete_gpio import Discrete
				#create a Dicerete object and save the pointer to that instance
		#  in <self> (the current class: Demo)
		self.discrete=Discrete()
		
	def build_test(self):
		print("-- Main demo start --")
		self.discrete.build_test()
		print("-- Main demo done --")
		
if __name__ == "__main__":
	demo=Demo()
	demo.build_test()


