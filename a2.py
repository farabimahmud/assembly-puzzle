# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 00:26:28 2019

@author: Farabi
"""
from colored import fg, bg, attr
from random import * 
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

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.resident == other.resident 

	def __repr__(self):
		return str(self.x)+" "+str(self.y)+" "+str(self.resident)

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

	def __eq__(self, other):
		if len(self.cells) == len(other.cells):
			p1 = self.translate(0,0).copy()
			p2 = other.translate(0,0).copy()

			t1 = list([p1])
			t2 = list([p2])

			for i in range(4):
				t1.append(t1[i])
				t2.append(t2[i])
				t1[i+1].rotate(1)
				t2[i+1].rotate(1)


			for i in range(4):
				for j in range(4):
					match = 0 
					for k in range(len(t1[i].cells)):
						c1 = t1[i].cells[k]
						c2 = t2[j].cells[k]
						if (c1 == c2):
							match = match + 1
					if match == len(t1[i].cells):
						return True
			return False 
		else:
			return False 


	def __repr__(self):
		res = "|"
		for c in self.cells:
			res = res + repr(c) + ", "

		return res+"|"


class Board:

	def __init__(self, dimension_x=7, dimension_y=7):
		self.dimension_x = dimension_x
		self.dimension_y = dimension_y
		self.data = list()
		self.overlap_count = 0 
		for i in range(self.dimension_x):
			self.data.append([])
			for j in range(self.dimension_y):
				self.data[i].append([Cell()])


	def print(self):
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				print("%s%3s%s" % (fg(self.data[i][j][0].color), self.data[i][j][0].resident, attr('reset')), end=" ")
			print("")

	def check_board(self):
		flag = True
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):		
				if (self.data[i][j][0].resident == 0):
					flag = False
					break
		return flag 

	def set_hole(self, x=0, y=0):
		self.hole_cell = Cell(x,y,-1, "black")
		self.data[self.hole_cell.x][self.hole_cell.y].append(self.hole_cell)

	def get_hole(self):
		return self.hole_cell

	def get_pieces(self):
		onboard = set()
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				for c in self.data[i][j]:
					if (c.resident > 0):
						onboard.add(c.resident)
		return list(onboard)

	def full_print(self):
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				printstr = ""
				for c in self.data[i][j]:
					printstr = printstr + str(c.resident) 

				print("%9s" % (printstr), end=" ")
			print("")

	def print(self):
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				printstr = ""
				for c in self.data[i][j]:
					printstr = printstr + str(c.resident) 

				if printstr == "0":
					print("%9s" % ("0"), end=" ")
				elif printstr[1] == "-":
					print("%9s" % ("-1"), end=" ")
				else:
					print("%9s" % (printstr[1:2]), end=" ")
					
			print("")


	def remove_l_piece(self, piece):	
		for cell in piece.cells:
			try:
				self.data[cell.x][cell.y].remove(cell)
			except:
				print("not in the list")

	def get_board_overlaps(self):
		self.overlap_count = 0
		for i in range(self.dimension_x):
			for j in range(self.dimension_y):
				self.overlap_count = self.overlap_count + len(self.data[i][j]) - 1 
		return self.overlap_count

	def is_goal(self):
		return self.get_board_overlaps() == 0 


def loose_piece_on_board(piece, board):
	if in_boundary(piece, board):  

		for cell in piece.cells:	
			board.data[cell.x][cell.y].append(cell)
		return True
	else:
		return False

def place_piece_on_board(piece, board):
	if count_overlap(piece, board) == 0 and in_boundary(piece, board):  
		for cell in piece.cells:	
			board.data[cell.x][cell.y][0] = cell
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

#helper function to count how many cells overlap existing pieces on the  
def count_overlap(piece, board):
	overlap = 0
	for cell in piece.cells:
		if board.data[cell.x][cell.y].resident != 0:
			# print(cell.x, cell.y, board.data[cell.x][cell.y].resident, piece.id)
			if board.data[cell.x][cell.y].resident != piece.id:
				# print(cell.x, cell.y, board.data[cell.x][cell.y].resident, piece.id)
				overlap = overlap + 1 
	return overlap

def count_loose_overlap(piece, board):
	overlap = 0
	for cell in piece.cells:
		print(cell)
		for c in board.data[cell.x][cell.y]:
			if (c.resident != piece.id):
				if (c.resident == 0):
					pass
				else:
					overlap = overlap +1 
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
#				if in_boundary(cur_piece,board) and count_overlap(cur_piece, board) == 0:
				if in_boundary(cur_piece, board):
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



def random_search(board, pieces, hole):
	iteration = 0

	while(not is_goal_state(board)):
		shuffle(pieces)
		for piece in pieces:
			options = generate_possible_options(piece,board)
			if (len(options) == 0):
				break
			else:
				selected_piece = choice(options)
				while(not place_piece_on_board(selected_piece,board)):
					selected_piece = choice(options)

		iteration = iteration + 1
		# print("current iteration: ", iteration)
		# board.print()
		if is_goal_state(board):
			return board 
		else:
			del board
			board = Board()
			board.set_hole(6,0)
	return board 

def init_population(size, board, pieces, hole):
	boards = list()
	for i in range(size):
		boards.append(Board())
		boards[i].set_hole(hole.x, hole.y)
		for p in pieces:
			options = generate_possible_options(p, boards[i])
			loose_piece_on_board(choice(options), boards[i])
	return boards

def evaluate(boards):
	minimum_overlap = 99999
	best = ""
	for b in boards:
		oc = b.get_board_overlaps()
		if oc < minimum_overlap:
			minimum_overlap = oc 
			best = b
	return b


def ge_search(board, pieces, hole):
	ps = [p.copy() for p in pieces]
	iteration = 0 
	print(ps)

	population = init_population(10, board, pieces, hole)
	population.sort(key=lambda x: x.overlap_count)
	best = evaluate(population)
	return best 
	
# driver program
def dfs(board, pieces, hole):
	stack = []
	vertices = initial_options(board, pieces)
	




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
b.set_hole(hole.x, hole.y)
pieces.sort(key=lambda x: x.length, reverse=True)	

# b = random_search(b, pieces, hole)

# b.print()
# loose_piece_on_board(pieces[0],b)

# loose_piece_on_board(pieces[2],b)
# # place_piece_on_board(pieces[0],b.print)
# print(count_loose_overlap(pieces[8],b))
b = ge_search(b, pieces,hole)
b.full_print()


# b.print()

# place_piece_on_board(pieces[4],b)
# print(b.get_pieces())
# search(b, pieces, 0)
# print(is_goal_state(b))