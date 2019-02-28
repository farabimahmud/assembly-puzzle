class Cell:
	def __init__(self, x=0, y=0, r=0, c="white"):
		self.x, self.y = x, y
		self.resident = r 
		self.color = c


	#x' = x cos T - y sin T
	#y' = y cos T + x sin T
	def l_rotate(self):
		oldx, oldy = self.x, self.y
		self.x, self.y = -1 * oldy, oldx   

	def r_rotate(self):
		oldx, oldy = self.x, self.y 
		self.x, self.y = oldy, -1 * oldx 

	def __repr__(self):
		return str(self.x)+" "+str(self.y)+" "+str(self.resident)