# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 00:26:28 2019

@author: Farabi
"""
from stack import Stack
from cell import Cell
from board import Board
from random import *
from puzzlepiece import PuzzlePiece
#make blank 7x7 block



class Graph:
	def __init__(self, domain):		
		self.node = list()
		self.edge = list()
		for i in domain:
			for j in i:
				self.node.append(j)

		for i in range(len(self.node)):
			self.edge.append([])
			for j in self.node:
				if self.node[i].id != j.id:
					self.edge[i].append(j)



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
	if check_island(board):
		return possible
	else:
		for i in range(board.dimension_x):
			for j in range(board.dimension_y):
				for k in range(4):
					cur_piece = piece.copy()
					cur_piece = cur_piece.rotate(k).translate(i,j)
					if in_boundary(cur_piece,board) and (count_overlap(cur_piece, board) == 0):
						possible.append(cur_piece)
	return possible

def check_island(board):

	for i in range(board.dimension_x):
		for j in range(board.dimension_y):
			if i != 0 and j != 0 and i!= board.dimension_x-1 and j != board.dimension_y-1: 
				if board.data[i][j].resident == 0 	\
				and board.data[i-1][j-1].resident != 0 	\
				and board.data[i-1][j].resident != 0 		\
				and board.data[i-1][j+1].resident != 0	\
				and board.data[i][j-1].resident != 0		\
				and board.data[i][j+1].resident != 0		\
				and board.data[i+1][j-1].resident != 0	\
				and board.data[i+1][j].resident != 0		\
				and board.data[i+1][j+1].resident != 0:
					return True
			elif i == 0 and j!=0 and j!=board.dimension_y-1:
				if board.data[i][j].resident == 0 	\
				and board.data[i][j-1].resident != 0		\
				and board.data[i][j+1].resident != 0		\
				and board.data[i+1][j-1].resident != 0	\
				and board.data[i+1][j].resident != 0		\
				and board.data[i+1][j+1].resident != 0:
					return True
			elif j==0 and i!=0 and  i!= board.dimension_x-1:
				if board.data[i][j].resident == 0 	\
				and board.data[i-1][j].resident != 0 		\
				and board.data[i-1][j+1].resident != 0	\
				and board.data[i][j+1].resident != 0		\
				and board.data[i+1][j].resident != 0		\
				and board.data[i+1][j+1].resident != 0:
					return True				
			elif i == 0 and j == 0:
				if board.data[i][j].resident == 0 	\
				and board.data[i][j+1].resident != 0		\
				and board.data[i+1][j].resident != 0		\
				and board.data[i+1][j+1].resident != 0:
					return True

	return False

def generate_all_possible_options(board, pieces):
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
	stack = Stack()
	used = []

	pieces.sort(key=lambda x: x.length, reverse=True)
	board.set_hole(hole.x, hole.y)
	domain = generate_all_possible_options(board, pieces)
	g = Graph(domain)

	for i in range(len(g.node)):
		used.append(0)
	
	init_node = randint(0,len(domain[0])-1) #randomly select initial node

	stack.push(init_node)

	while(not stack.isEmpty()):
		u_piece = stack.pop()
		if (used[u] == False):
			used[u] = True
			for elem in g.edge[u]:
				stack.push(elem)


	# print(len(g.node), len(g.edge))
	# print(g.edge)
	return board 


def brute_solution(board, pieces):
	board.set_hole(6,0)
	pieces.sort(key=lambda x: x.length, reverse= True)

	p = list()
	p.append(generate_possible_options(pieces[0],board))
	solutions = []

	for p0_cur in p[0]:
		place_piece_on_board(p0_cur,board)
		# board.print()
		p.append(generate_possible_options(pieces[1], board))
		print(check_island(board))
		if len(p[1]) != 0 : #solution exists
			for p1_cur in p[1]:
				place_piece_on_board(p1_cur, board)
				# board.print()
				p.append(generate_possible_options(pieces[2], board))
				if len(p[2]) != 0: #solution exists
					for p2_cur in p[2]:
						place_piece_on_board(p2_cur, board)
						p.append(generate_possible_options(pieces[3], board))
						if len(p[3]) != 0: #solution exists
							for p3_cur in p[3]:
								place_piece_on_board(p3_cur, board)
								p.append(generate_possible_options(pieces[4], board))
								if len(p[4]) != 0: #solution exists
									for p4_cur in p[4]:
										place_piece_on_board(p4_cur, board)
										p.append(generate_possible_options(pieces[5], board))
										if len(p[5]) != 0: #solution exists
											for p5_cur in p[5]:
												place_piece_on_board(p5_cur, board)
												p.append(generate_possible_options(pieces[6], board))
												if len(p[6]) != 0: #solution exists
													for p6_cur in p[6]:
														place_piece_on_board(p6_cur, board)
														p.append(generate_possible_options(pieces[7], board))
														if len(p[7]) != 0: #solution exists
															for p7_cur in p[7]:
																place_piece_on_board(p7_cur, board)
																# board.print()
																p.append(generate_possible_options(pieces[8], board))
																if len(p[8]) != 0: #solution exists
																	for p8_cur in p[8]:
																		place_piece_on_board(p8_cur, board)
																		board.print()
																		solutions.append(board.copy())
																		remove_piece_from_board(p8_cur,board)
																else:
																	pass
																remove_piece_from_board(p7_cur,board)
																del p[8]

														else:
															pass
														remove_piece_from_board(p6_cur,board)
														del p[7]

												else:
													pass
												remove_piece_from_board(p5_cur,board)
												del p[6]

										else:
											pass
										remove_piece_from_board(p4_cur,board)
										del p[5]
								else:
									pass
								remove_piece_from_board(p3_cur,board)
								del p[4]

						else:
							pass
						remove_piece_from_board(p2_cur,board)
						del p[3]
				else:
					pass
				remove_piece_from_board(p1_cur,board)
				del p[2]
		else:
			pass

		remove_piece_from_board(p0_cur, board)
		del p[1]



	




# driver program

b = Board()
print(check_island(b))
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
b.set_hole(6,0)
place_piece_on_board(pieces[4],b)
remove_piece_from_board(pieces[4], b)
# search(b, pieces, hole)


brute_solution(b,pieces)
# search(b, pieces, 0)
# b.print()
# print(is_goal_state(b))