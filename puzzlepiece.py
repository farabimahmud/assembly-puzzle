
from cell import Cell


class PuzzlePiece:

	def __init__(self, d=[], id=0 , color="red"):
		self.cells = list()
		self.data = d.copy()
		for i in range(len(d)):			
			c = Cell(d[i][0], d[i][1], id, color)
			self.cells.append(c)
		self.color = color 
		self.id = id
		self.length = (len(self.cells))

	def rotate(self, n=0):
		n = n%4 
		for j in range(n):
			for i in range(len(self.cells)):
				self.cells[i].l_rotate()
		return self 

	def r_rotate(self):
		for i in range(len(self.cells)):
			self.cells[i].r_rotate()
		return self

	def translate(self, delx=0, dely=0):
		for i in range(len(self.cells)):
			self.cells[i].x = self.cells[i].x + delx 
			self.cells[i].y = self.cells[i].y + dely
		return self

	def print(self):
		for cell in self.cells:
			print("%i,%i"% (cell.x, cell.y), end=" ")
		print("")

	def copy(self):
		t = PuzzlePiece(self.data,self.id,self.color)
		return t

	def __repr__(self):
		ret = "|"
		for i in range(len(self.cells)):
			if i == len(self.cells)-1:
				ret = ret + str(self.cells[i])+" "
			else:
				ret = ret + str(self.cells[i])+", "
									
		ret = ret + "|"
		return ret 