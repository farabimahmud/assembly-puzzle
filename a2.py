# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 00:26:28 2019

@author: Farabi
"""
from colored import fg, bg, attr
#B = [1 for x in range(7)]
#A = [B for x in range(7)]
#print(A)
#make blank 7x7 block
A = [ [10*y+x for x in range(7)] for y in range(7)]


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
	cells = []
	def __init__(self, data=[], color="red"):
		for i in range(len(data)):
			self.cells.append(Cell(data[i][0], data[i][1], i, color))
		self.color = color 

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
 




class Piece:
    def __init__(self, color, unit_list):
        self.color = color
        self.unit_list = unit_list
        self.unit_count = len(unit_list)
  
    def zeroup(self):
        xmin = min(x[0] for x in self.unit_list)
        ymin = min(x[1] for x in self.unit_list)
        if min([xmin, ymin, 0]) != 0:      
          if xmin < ymin:
            self.unit_list = [[t[0] - xmin, t[1]] for t in self.unit_list]
          else:
            self.unit_list = [[t[0], t[1] - ymin] for t in self.unit_list]
  
    def sevendown(self):
        xmax = max(x[0] for x in self.unit_list)
        ymax = max(x[1] for x in self)
    
    #rotate 90 degrees counterclockwise
    def rotate90(self):
        for i, item in enumerate(self.unit_list):
          x = item[0]
          y = item[1]
          self.unit_list[i][0] = -1 * y
          self.unit_list[i][1] = x
        self.zeroup()
  
    #rotate 90 degrees clockwise
    def antirotate90(self):
        for i, item in enumerate(self.unit_list):
          x = item[0]
          y = item[1]
          self.unit_list[i][0] = y
          self.unit_list[i][1] = -1 * x
        self.zeroup()

    def rotate(self, turns):
        turns = turns % 4
        if turns > 0:
          for i in range(turns):
            self.rotate90()
        else:
          turns = turns * -1
          for i in range(turns):
            self.antirotate90()
        return self

hole = Piece('black',[[0,0]])
pieces = [
  Piece('red', [[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]]),
  Piece('light_yellow', [[0,0], [0,1], [1,1], [1,2], [2,2]]),
  Piece('green', [[0,1], [0,2], [1,0], [1,1], [1,2], [2,1], [2,2], [2,3]]),
  Piece('cyan', [[0,0], [1,0], [2,0], [3,0], [4,0]]),
  Piece('dark_goldenrod', [[0,0], [1,0]]),
  Piece('orange_3', [[0,1], [1,0], [1,1], [2,0], [2,1], [3,1]]),
  Piece('dark_blue', [[0,0], [1,0], [1,1], [2,0], [2,1], [2,2]]),
  Piece('violet', [[0,1], [1,0], [1,1], [1,2]]),
  Piece('light_blue', [[0,0], [0,1], [0,2], [0,3],[1,2]])
]  

def willFit(board, piece, location):
  for unit in piece.unit_list:
    if board[location[0]+unit[0]][location[1]+unit[1]] != 1:
      return False
  return True

def validLocation(x,y):
  return x >= 0 and x < 7 and y >=0 and y < 7

def placePiece(board, piece, location):
  #if willFit(board, piece, location):
  for unit in piece.unit_list:
    if validLocation(location[0]+unit[0],location[1]+unit[1]):
      board[location[0]+unit[0]][location[1]+unit[1]] = (piece.unit_count, piece.color)
  return board



def printBoard(A):
  for line in A:
    for item in line:
      if isinstance(item, tuple):
        (block, color) = item
        print('%s%s%i %s' % (fg(color), bg(color), block, attr('reset')), end='')
      else:
        print('%s%s %2i%s' % (fg('black'), bg('white'), item, attr('reset')), end='')
    print(' ')


#how to use it
#hole
b = Board()
b.set_hole(0,0)
p = PuzzlePiece([[0,0], [0,1], [1,0], [1,1], [2,0], [2,1], [1,2]], "white")
b.print()


# A = placePiece(A, hole, H[11])
# #printBoard(A)
# #red 3x3
# A = placePiece(A, pieces[0].rotate(0), [1,0])
# # printBoard(A)
# ##print(' ')
# ###yellow 3x3
# A = placePiece(A, pieces[1].rotate(0), [1,3])
# ##printBoard(A)
# ##print(' ')
# ###green 3x4
# A = placePiece(A, pieces[2].rotate(1), [3,0])
# ##printBoard(A)
# ##print(' ')
# ###teal 1x5
# A = placePiece(A, pieces[3].rotate(1), [6,2])
# ##printBoard(A)
# ##print(' ')
# ###orange 1x2
# A = placePiece(A, pieces[4].rotate(1), [5,4])
# ##printBoard(A)
# ##print(' ')
# ###red 2x4 
# A = placePiece(A, pieces[5].rotate(2), [2,3])
# ##printBoard(A)
# ##print(' ')
# ###purple 3x3
# A = placePiece(A, pieces[6].rotate(2), [0,4])
# ##printBoard(A)
# ##print(' ')
# ###purple 2x3 
# A = placePiece(A, pieces[7].rotate(1), [3,5])
# ##printBoard(A)
# ##print(' ')
# ###blue 2x4
# A = placePiece(A, pieces[8].rotate(0), [0,0])
###print to terminal
# printBoard(A)
