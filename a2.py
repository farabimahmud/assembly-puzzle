# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 00:26:28 2019

@author: Farabi
"""
from colored import fg, bg, attr

#make blank 7x7 block




# https://pypi.org/project/colored/ for color list
# unit list start at 0,0 top left. use coords as if the piece were encapsulated
# by a rectangle with that coordinate system.
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

def place_piece_on_board(piece, board):
	if count_overlap(piece, board) == 0 and in_boundary(piece, board):  
		for cell in piece.cells:	
			board.data[cell.x][cell.y] = cell
		return True
	else:
		return False

def remove_piece_from_board(piece,board):
	onboard = board.get_pieces()
	if piece.id not in onboard:
		return False 
	else:
		for cell in piece.cells:
			board.data[cell.x][cell.y] = Cell(cell.x, cell.y) # blank white cell
		return True


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


def is_goal_state(board):
	return len(board.get_pieces()) == 9

def generate_possible_options(piece, board):
	possible = []
	for i in range(board.dimension_x):
		for j in range(board.dimension_y):
			for k in range(4):
				cur_piece = piece.copy()
				cur_piece = cur_piece.rotate(k).translate(i,j)
				if in_boundary(cur_piece,board) and count_overlap(cur_piece, board) == 0:
					possible.append(cur_piece)
	return possible

def initial_options(board, pieces):
	pieces.sort(key=lambda x: x.length, reverse = True)
	domain = [] #list containing all valid pieces configuration 
				#including rotations and translations within boundary
	i = 0
	for p in pieces:
		domain.append([])
		
		for result in generate_possible_options(p,board):
			domain[i].append(result)
		i = i + 1
	return domain



def search(board, pieces, hole):
	for piece in pieces:
		options = generate_possible_options(piece, board)
		for o in options:
			place_piece_on_board(o, board)
	return board 


# driver program

b = Board()
pieces = []
pieces.append(PuzzlePiece([[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]], 1, "red"))
pieces.append(PuzzlePiece([[0,0], [0,1], [1,1], [1,2], [2,2]], 2, "light_yellow"))
pieces.append(PuzzlePiece([[0,1], [0,2], [1,0], [1,1], [1,2], [2,1], [2,2], [2,3]], 3, "green"))
pieces.append(PuzzlePiece([[0,0], [1,0], [2,0], [3,0], [4,0]], 4, "cyan"))
pieces.append(PuzzlePiece([[0,0], [0,1]], 5, "dark_goldenrod"))
pieces.append(PuzzlePiece([[0,1], [1,0], [1,1], [2,0], [2,1], [3,1]], 6, "orange_3"))
pieces.append(PuzzlePiece([[0,0], [1,0], [1,1], [2,0], [2,1], [2,2]], 7, "dark_blue"))
pieces.append(PuzzlePiece([[0,1], [1,0], [1,1], [1,2]], 8, "violet"))
pieces.append(PuzzlePiece([[0,0], [0,1], [0,2], [0,3],[1,2]], 9, "light_blue"))

hole = Cell(6,0,-1,"black")
board.set_hole(hole.x, hole.y)
pieces.sort(key=lambda x: x.length, reverse=True)	

search(b, pieces, hole)
# search(b, pieces, 0)
# print(is_goal_state(b))