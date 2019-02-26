# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 00:26:28 2019

@author: Farabi
"""
from colored import fg, bg, attr

#make blank 7x7 block


#numbered the same as in the assignment
H = [[0,0], [0,3], 
	 [1,0], [1,4], [1,5], 
	 [3,2], [3,3], 
	 [4,1], [4,4], [4,6], 
	 [5,3], 
	 [6,0], [6,4], [6,5]]

# https://pypi.org/project/colored/ for color list
# unit list start at 0,0 top left. use coords as if the piece were encapsulated
# by a rectangle with that coordinate system.
class Cell:
	resident = ""
	x = ""
	y = ""
	color = ""

	def __init__(self, x=0, y=0, r=0, c="red"):
		self.x, self.y = x, y
		self.resident = r 
		self.color = c

	def l_rotate(self):
		self.x, self.y = -1 * self.y, self.x 

	def r_rotate(self):
		self.x, self.y = self.y, -1 * self.x 


class Board:
	dimension_x = 7
	dimension_y = 7
	data = []
	hole_cell = ""
	def __init__(self):
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


class PuzzlePiece:
	color = "red"
	cells = list()
	id = 0 

	def __init__(self, d=[], id=0 , color="red"):
		self.cells = list()
		for i in range(len(d)):			
			c = Cell(d[i][0], d[i][1], id, color)
			self.cells.append(c)
		self.color = color 
		self.id = id

	def l_rotate(self):
		for i in range(len(self.cells)):
			self.cells[i].l_rotate()

	def r_rotate(self):
		for i in range(len(self.cells)):
			self.cells[i].r_rotate()

	def translate(self, delx=0, dely=0):
		for i in range(len(self.cells)):
			self.cells[i].x = self.cells[i].x + delx 
			self.cells[i].y = self.cells[i].y + dely
	def print(self):
		for cell in self.cells:
			print("%i,%i"% (cell.x, cell.y), end=" ")
		print("")

def place_piece_on_board(piece, board):
	if count_overlap(piece, board) == 0 and in_boundary(piece, board):  
		for cell in piece.cells:	
			board.data[cell.x][cell.y] = cell
		return True
	else:
		return False

def in_boundary(piece, board):
	flag = True 
	for cell in piece.cells:
		if cell.x <0 or cell.x >= board.dimension_x or cell.y <0 or cell.y >=board.dimension_y:
			flag = False
			break
	return flag

#helper function to count how many cells overlap existing pieces on the board
def count_overlap(piece, board):
	overlap = 0
	for cell in piece.cells:
		if board.data[cell.x][cell.y].resident != 0:
			# print(cell.x, cell.y, board.data[cell.x][cell.y].resident, piece.id)
			if board.data[cell.x][cell.y].resident != piece.id:
				# print(cell.x, cell.y, board.data[cell.x][cell.y].resident, piece.id)
				overlap = overlap + 1 
	return overlap

def print_overlap(piece, board):
	for cell in piece.cells:
		if board.data[cell.x][cell.y].resident != 0:
			# print(cell.x, cell.y, board.data[cell.x][cell.y].resident, piece.id)
			if board.data[cell.x][cell.y].resident != piece.id:
				print(cell.x, cell.y, board.data[cell.x][cell.y].resident, piece.id)

# hole = Piece('black',[[0,0]])
# pieces = [
#   Piece('red', [[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]]),
#   Piece('light_yellow', [[0,0], [0,1], [1,1], [1,2], [2,2]]),
#   Piece('green', [[0,1], [0,2], [1,0], [1,1], [1,2], [2,1], [2,2], [2,3]]),
#   Piece('cyan', [[0,0], [1,0], [2,0], [3,0], [4,0]]),
#   Piece('dark_goldenrod', [[0,0], [1,0]]),
#   Piece('orange_3', [[0,1], [1,0], [1,1], [2,0], [2,1], [3,1]]),
#   Piece('dark_blue', [[0,0], [1,0], [1,1], [2,0], [2,1], [2,2]]),
#   Piece('violet', [[0,1], [1,0], [1,1], [1,2]]),
#   Piece('light_blue', [[0,0], [0,1], [0,2], [0,3],[1,2]])
# ]  


#how to use it
#hole
b = Board()
b.set_hole(0,0)

p = PuzzlePiece([[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]], 1, "white")
q = PuzzlePiece([[2,1]], 3, "blue")
r = PuzzlePiece([[3,1]], 4 , "green")

print(place_piece_on_board(p, b))
print_overlap(q, b)
b.print()