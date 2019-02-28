from cell import Cell
from colored import fg, bg, attr


class Board:

	def __init__(self, dimension_x=7, dimension_y=7):
		self.dimension_x = dimension_x
		self.dimension_y = dimension_y
		self.data = list()
		for i in range(self.dimension_x):
			self.data.append([])
			for j in range(self.dimension_y):
				self.data[i].append(Cell())

	def print(self):
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				print("%s%3s%s" % (fg(self.data[i][j].color), self.data[i][j].resident, attr('reset')), end=" ")
			print("")

	def check_board(self):
		flag = True
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):		
				if (self.data[i][j].resident == 0):
					flag = False
					break
		return flag 

	def set_hole(self, x=0, y=0):
		self.hole_cell = Cell(x,y,-1, "black")
		self.data[self.hole_cell.x][self.hole_cell.y] = self.hole_cell

	def get_hole(self):
		return self.hole_cell

	def get_pieces(self):
		onboard = []
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				if (self.data[i][j].resident > 0) and (self.data[i][j].resident not in onboard):
					onboard.append(self.data[i][j].resident)
		return onboard

	def sub_goal(self, count=2):
		return len(onboard)==2

	def copy(self):
		b = Board(self.dimension_x, self.dimension_y)
		for i in range(self.dimension_x):
			b.data.append([])
			for j in range(self.dimension_y):
				b.data[i].append(Cell(i,j,self.data[i][j].resident, self.data[i][j].color))
		return b
