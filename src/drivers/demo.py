class Demo:
	def __init__(self,support):
		self.initialize(support)
		self.version="0.1"
		
	def initialize(self,support):
		from peripherals.discrete_gpio import Discrete
		from peripherals.distance_uart import Distance
		#create a Dicerete object and save the pointer to that instance
		#  in <self> (the current class: Demo)
		self.discrete=Discrete(support)
		self.distance=Distance(support)
		
	def build_test(self):
		print("-- Main demo start --")
		print("Build version: "+self.version)
		self.discrete.build_test()
		self.distance.build_test()
		print("-- Main demo done --")
		
if __name__ == "__main__":
	from peripherals.support_library import Support
	support=Support()
	demo=Demo(support)
	demo.build_test()

#TODO: lasers
