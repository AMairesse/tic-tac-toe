#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function
from operator import itemgetter
import copy
import json
import argparse

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
		# Display the first board if there is only one
		# Otherwise it is not usefull
		if self.board.__len__() == 1:
			index = 0
		else:
			index = 1

		for board_number in range(index,self.board.__len__()):
			print("_______  ", end="")
		print("")

		for x in range(3):
			for board_number in range(index,self.board.__len__()):
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

		for board_number in range(index,self.board.__len__()):
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
	def best_move(self, playing_sign):
		result = []
		for x in range(0,3):
			for y in range(0,3):
				if self.board[-1][x][y] == 0:
					score = self.score(x, y, playing_sign)
					result.append([x,y,score])
		if result == []:
			return (None, None)
		else:
			result.sort(key=itemgetter(2), reverse=True)
			return (result[0][0], result[0][1])

	def score(self, x, y, winner_sign, playing_sign = None, score = 0, deep = 1.0):
		# Default playing_sign to winner_sign
		if playing_sign == None:
			playing_sign = winner_sign
		# Create a working board from the current one
		working_board = TicTacToe()
		working_board.writeBoard(self.readBoard())
		# Play the move
		result = working_board.play(playing_sign, x, y, False)
		# If the move is invalid, we exit with score - 1
		if result == False:
			return (score - 1 * deep)
		# If there is a winner, we exit with score + 2
		if working_board.isThereWinner() != None:
			if winner_sign == playing_sign:
				return (score + 2 * deep)
			else:
				return (score - 2 * deep)
		if playing_sign == 'X':
			new_playing_sign = 'O'
		else:
			new_playing_sign = 'X'
		# Play every other moves
		saved_board = working_board.readBoard()
		temp_score = 0
		for new_x in range(0,3):
			for new_y in range(0,3):
				if working_board.board[-1][new_x][new_y] == 0:
					temp_score = working_board.score(new_x, new_y, winner_sign, new_playing_sign, temp_score, deep / 2)
					working_board.writeBoard(saved_board)
		return (score + temp_score * deep)

	def play_a_game(self, player = None):
		while self.moves <= 9:
			self.display()
			while True:
				x_str = input("Line ? ")
				y_str = input("Column ? ")
				played = self.play('X', int(x_str), int(y_str))
				if played:
					break
				else:
					print("Bad input, please retry.")
			self.display()
			if self.isThereWinner() != None:
				print("You win !")
				break
			else:
				if player == None:
					# Brute force playing
					(x, y) = self.best_move('O')
				else:
					(x, y) = player.play(self.readBoard())
				if x == None:
					# No more solutions
					break
				else:
					is_valid_move = self.play('O', x, y)
					if not is_valid_move:
						# AI player made an invalid move, human player win
						print("AI made an invalid move. You win !")
					if self.isThereWinner() != None:
						self.display()
						print("You lose !")
						break

	def solve(self, boards, best_moves, x = None, y = None, sign = 'X'):
		# Create a working board from the current one
		working_board = TicTacToe()
		working_board.writeBoard(self.readBoard())
		# If called without values then scan all availables combinations
		new_boards = boards
		new_best_moves = best_moves
		if ((x == None) and (y == None)):
			for x in range(0,3):
				for y in range(0,3):
					new_boards, new_best_moves = working_board.solve(new_boards, new_best_moves, x, y, sign)
			return new_boards, new_best_moves
		# Play the move for the current player
		result = working_board.play(sign, x, y, False)
		# If the move is invalid, we exit
		if result == False:
			return new_boards, new_best_moves
		# Change current player
		if sign == 'X':
			sign = 'O'
		else:
			sign = 'X'
		# Get the next best move
		(best_x, best_y) = working_board.best_move(sign)
		# If there is no more available moves we exit
		if best_x == None:
			return new_boards, new_best_moves
		# Append the board and the best_move if not already exist
		current_board = working_board.readBoard()
		if current_board in new_boards:
			# This board has already been explored by another path
			return new_boards, new_best_moves
		# Append this new combination
		new_boards.append(current_board)
		new_best_moves.append(best_x*3+best_y)
		# If there is a winner, we exit here
		if working_board.isThereWinner() != None:
			return new_boards, new_best_moves
		# Play every other moves
		for new_x in range(0,3):
			for new_y in range(0,3):
				if working_board.board[-1][new_x][new_y] == 0:
					new_boards, new_best_moves = working_board.solve(new_boards, new_best_moves, new_x, new_y, sign)
					working_board.writeBoard(current_board)
		return new_boards, new_best_moves


parser = argparse.ArgumentParser(description='Play TicTacToe')
subparsers = parser.add_subparsers(dest='action')
# create the parser for the "play" command
parser_learn = subparsers.add_parser('play')
parser_learn.add_argument('--player-file', type=argparse.FileType('r'), required=False)
# create the parser for the "solve" command
parser_solve = subparsers.add_parser('solve')
parser_solve.add_argument('--export-file', type=argparse.FileType('w'), required=True)


if __name__ == "__main__":
	args = parser.parse_args()
	cmdline_args = vars(args)
	if (cmdline_args['action'] == 'play'):
		board = TicTacToe()
		player_file = cmdline_args['player_file']
		if player_file != None:
			from player import Player
			p = Player()
			p.load(player_file)
		else:
			p=None
		board.play_a_game(p)
	elif (cmdline_args['action'] == 'solve'):
		board = TicTacToe()
		boards_list, best_moves_list = board.solve([], [])
		f = cmdline_args['export_file']
		for i, data in enumerate(boards_list):
			result = data
			result.append(best_moves_list[i])
			f.write(json.dumps(result))
			f.write("\n")
		f.close()