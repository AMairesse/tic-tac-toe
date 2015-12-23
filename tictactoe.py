#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function


class TicTacToe():
	"""docstring for ClassName"""

	# Public attribute
	moves = 0
	board = [[0,0,0],
			 [0,0,0],
			 [0,0,0]]

	# Clear the board for a new game
	def clear(self):
		self.moves = 0
		self.board = [[0,0,0],
					  [0,0,0],
					  [0,0,0]]

	# Autoplay two AI and return :
	#  - the winner
	#  - number of turns played
	#  - the win condition (text to display)
	def autoPlay(self, playerX, playerO):
		# Play the 8 first moves
		for x in xrange(0,4):
			# Player 'X' plays
			(x, y) = playerX.play(self.readBoard())
			valid_move = self.play('X', x, y)
			if not valid_move:
				return (playerO, self.moves, "X made an invalid move")
			elif self.isThereWinner() != None :
				return (playerX, self.moves, "Game won by X")

			# Player 'O' plays
			(x, y) = playerO.play(self.readBoard())
			valid_move = self.play('O', x, y)
			if not valid_move:
				return (playerX, self.moves, "O made an invalid move")
			elif self.isThereWinner() != None :
				return (playerO, self.moves, "Game won by O")

		# Play the last move
		(x, y) = playerX.play(self.readBoard())
		valid_move = self.play('X', x, y)
		if not valid_move:
			return (playerO, self.moves, "X made an invalid move")
		elif self.isThereWinner() != None :
			return (playerX, self.moves, "Game won by X")
		else:
			return (None, self.moves, "Draw game")

	# Make a move on the board
	def play(self, sign, x, y):
		# Check first if the spot if free
		if self.board[x][y] != 0:
			return False
		if sign == 'X':
			self.board[x][y] = 1
		elif sign == 'O':
			self.board[x][y] = -1
		else:
			return False
		self.moves = self.moves + 1
		return True

	# Print the board on the screen
	def display(self):
		print("_______")
		for x in range(3):
			for y in range(3):
				print ("|", end="")
				if self.board[x][y] == 0:
					print (" ", end="")
				elif self.board[x][y] == 1:
					print ("X", end="")
				else:
					print ("O", end="")
			print ("|")
		print("-------")

	# Export the board in a single row and
	# values between 0 and 1(for AI players)
	def readBoard(self):
		result = []
		for x in xrange(0,3):
			for y in xrange(0,3):
				if self.board[x][y] == 0:
					result.append(0)
				elif self.board[x][y] == -1:
					result.append(0.5)
				else:
					result.append(1)
		return ([result])

	# Check if there is a winner and return which sign won
	def isThereWinner(self):
		# Lines
		for x in range(3):
			line = self.board[x][0] + self.board[x][1] + self.board[x][2]
			if line == 3 :
				return('X')
			elif line == -3 :
				return('O')
		# Columns
		for x in range(3):
			column = self.board[0][x] + self.board[1][x] + self.board[2][x]
			if column == 3 :
				return('X')
			elif column == -3 :
				return('O')
		# Diagonals
		diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
		if diag == 3 :
			return('X')
		elif diag == -3 :
			return('O')
		diag = self.board[2][0] + self.board[1][1] + self.board[0][2]
		if diag == 3 :
			return('X')
		elif diag == -3 :
			return('O')
		# There is no winner
		return(None)
