#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function


class TicTacToe():
	"""docstring for ClassName"""

	# Public attribute
	board = [[0,0,0],
			 [0,0,0],
			 [0,0,0]]

	def clear(self):
		self.board = [[0,0,0],
					  [0,0,0],
					  [0,0,0]]

	def play(self, player, x, y):
		# Check first if the spot if free
		if self.board[x][y] != 0:
			return False
		if player == 'X':
			self.board[x][y] = 1
		elif player == 'O':
			self.board[x][y] = -1
		else:
			return False
		return True

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

	def readBoard(self):
		return {self.board[0][0], self.board[0][1], self.board[0][2],
				self.board[1][0], self.board[1][1], self.board[1][2],
				self.board[2][0], self.board[2][1], self.board[2][2]}

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


def main ():
	game = TicTacToe()
	game.play('O', 0, 0)
	game.play('O', 0, 1)
	game.play('O', 0, 2)
	game.display()
	print ("Winner is : ", game.isThereWinner())


if __name__ == "__main__":
	main()