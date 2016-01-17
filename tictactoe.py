#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function
import copy
import json

class TicTacToe():
	"""docstring for ClassName"""

	# Public attribute
	moves = None
	board = None

	def __init__(self):
		self.moves = 0
		self.board = [[[0,0,0],
					  [0,0,0],
					  [0,0,0]]]

	# Clear the board for a new game
	def clear(self):
		self.moves = 0
		self.board = [[[0,0,0],
					   [0,0,0],
					   [0,0,0]]]

	# Make a move on the board
	def play(self, sign, x, y, history = True):
		if history == True:
			# Take the last version of the board
			new_move = copy.deepcopy(self.board[-1])
		else:
			new_move = self.board[-1]
		# Check first if the spot if free
		if new_move[x][y] != 0:
			return False
		if sign == 'X':
			new_move[x][y] = 1
		elif sign == 'O':
			new_move[x][y] = -1
		else:
			return False
		self.moves = self.moves + 1
		if history == True:
			self.board.append(new_move)
		return True

	# Print the board on the screen
	def display(self):
		for board_number in range(1,self.board.__len__()):
			print("_______  ", end="")
		print("")

		for x in range(3):
			for board_number in range(1,self.board.__len__()):
				for y in range(3):
					print ("|", end="")
					if self.board[board_number][x][y] == 0:
						print (" ", end="")
					elif self.board[board_number][x][y] == 1:
						print ("X", end="")
					else:
						print ("O", end="")
				print ("|  ", end="")
			print("")

		for board_number in range(1,self.board.__len__()):
			print("-------  ", end="")
		print("")

	# Export the board in a single row and
	# values between 0 and 1(for AI players)
	def readBoard(self):
		# Take the last version of the board
		last_move = self.board[-1]
		result = []
		for x in range(0,3):
			for y in range(0,3):
				if last_move[x][y] == 0:
					result.append(0)
				elif last_move[x][y] == -1:
					result.append(0.5)
				else:
					result.append(1)
		return ([result])

	# Init the board with a saved position
	def writeBoard(self, data):
		self.clear()
		for i in range(0,9):
			if data[0][i] == 0.5:
				self.board[-1][i//3][i%3] = -1
			else:
				self.board[-1][i//3][i%3] = data[0][i]

	# Check if there is a winner and return which sign won
	def isThereWinner(self):
		# Take the last version of the board
		last_move = self.board[-1]
		# Lines
		for x in range(3):
			line = last_move[x][0] + last_move[x][1] + last_move[x][2]
			if line == 3 :
				return('X')
			elif line == -3 :
				return('O')
		# Columns
		for x in range(3):
			column = last_move[0][x] + last_move[1][x] + last_move[2][x]
			if column == 3 :
				return('X')
			elif column == -3 :
				return('O')
		# Diagonals
		diag = last_move[0][0] + last_move[1][1] + last_move[2][2]
		if diag == 3 :
			return('X')
		elif diag == -3 :
			return('O')
		diag = last_move[2][0] + last_move[1][1] + last_move[0][2]
		if diag == 3 :
			return('X')
		elif diag == -3 :
			return('O')
		# There is no winner
		return(None)

	# Return the best theorical move
	def best_move(self, weigth, deep):
		if deep == 0:
			pass
		return (x,y)

def recurs_move(f, board, x, y, sign):
	# Play the move
	result = board.play(sign, x, y, False)
	# If the move is invalid, we exit
	if result == False:
		return True
	# Write the current board status in the file
	f.write(json.dumps(board.readBoard()))
	f.write("\n")
	# If there is a winner, we exit
	if board.isThereWinner() != None:
		return True
	if sign == 'X':
		sign = 'O'
	else:
		sign = 'X'
	# Play every other moves
	saved_board = board.readBoard()
	for new_x in range(0,3):
		for new_y in range(0,3):
			if board.board[-1][new_x][new_y] == 0:
				recurs_move(f, board, new_x, new_y, sign)
				board.writeBoard(saved_board)
	return True

def main ():
	# Open file
	f = open('boards_list.txt', 'w')
	board = TicTacToe()
	recurs_move(f, board, 0, 0, 'X')
#	recurs_move(f, board, 0, 1, 'X')
#	recurs_move(f, board, 0, 2, 'X')
#	recurs_move(f, board, 1, 0, 'X')
#	recurs_move(f, board, 1, 1, 'X')
#	recurs_move(f, board, 1, 2, 'X')
#	recurs_move(f, board, 2, 0, 'X')
#	recurs_move(f, board, 2, 1, 'X')
#	recurs_move(f, board, 2, 2, 'X')

if __name__ == "__main__":
	main()

