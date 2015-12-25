#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function
import operator
import tensorflow as tf
from tictactoe import TicTacToe
from player import Player

class Generation():
	"""docstring fos Generation"""

	# Public attribute
	generation = []

	def __init__(self, size):
		for x in range(0, size):
			player = Player()
			player.init_from_random()
			self.generation.append([player, 0])

	def playTournament(self, tf_session = None):
		# Everyone plays against each other
		if tf_session == None:
			sess = tf.Session()
		else:
			sess = tf_session

		board = TicTacToe()
		with sess.as_default():
			for x in range(0,self.generation.__len__()):
				for y in range(x+1,self.generation.__len__()):
					[winner, moves, result] = self.playGame(self.generation[x][0], self.generation[y][0], board, sess)
					if winner == self.generation[x][0]:
						self.generation[x][1] = self.generation[x][1] + (0.1 * moves)
						self.generation[y][1] = self.generation[y][1] + (0.1 * moves) + 0.5
					elif winner == self.generation[y][0]:
						self.generation[x][1] = self.generation[x][1] + (0.1 * moves) + 0.5
						self.generation[y][1] = self.generation[y][1] + (0.1 * moves)
					elif winner == None:
						# We have a drawn game, each player earns max moves and a little bonus.
						self.generation[x][1] = self.generation[x][1] + (0.1 * moves) + 0.25
						self.generation[y][1] = self.generation[y][1] + (0.1 * moves) + 0.25
					board.clear()
		# Close TensorFlow session if it was created inside the function
		if tf_session == None:
			sess.close()
		del board

	def sort_by_score(self):
		# Order players in the current generation by score
		self.generation.sort(key=operator.itemgetter(1), reverse=True)

	def playGame(self, playerX, playerO, input_board = None, tf_session = None):
		# Play a board game between two players
		if input_board == None:
			board = TicTacToe()
		else:
			board = input_board

		if tf_session == None:
			sess = tf.Session()
		else:
			sess = tf_session

		with sess.as_default():
			# Play the 8 first moves
			for x in range(0,4):
				# First player
				(pos_x, pos_y) = playerX.play(board.readBoard(), sess)
				valid_move = board.play('X', pos_x, pos_y)
				if not valid_move:
					return (playerO, board.moves, "X made an invalid move")
				elif board.isThereWinner() != None :
					return (playerX, board.moves, "Game won by X")

				# Player 'O' plays
				(pos_x, pos_y) = playerO.play(board.readBoard(), sess)
				valid_move = board.play('O', pos_x, pos_y)
				if not valid_move:
					return (playerX, board.moves, "O made an invalid move")
				elif board.isThereWinner() != None :
					return (playerO, board.moves, "Game won by O")

			# Play the last move
			(pos_x, pos_y) = playerX.play(board.readBoard(), sess)
			valid_move = board.play('X', pos_x, pos_y)
			if not valid_move:
				return (playerO, board.moves, "X made an invalid move")
			elif board.isThereWinner() != None :
				return (playerX, board.moves, "Game won by X")
			else:
				return (None, board.moves, "Draw game")
		# Close TensorFlow session if it was created inside the function
		if tf_session == None:
			sess.close()
		if input_board == None:
			del board

	def evolve(self, display=False):
		generation_length = self.generation.__len__()

		if display:
			print("Ending scores : ", end="")
			for x in range(0,generation_length):
				print(self.generation[x][1], " ", end="")
			print("***** New generation created *****")

		# Second half of new generation is made from 1 with 2, 3 with 4, etc.
		# Start by the end and replace starting with the last one
		for x in range(0,generation_length/2):
			self.generation[generation_length-1-x][0].init_from_parents(self.generation[generation_length-1-(2*x)][0], self.generation[generation_length-2-(2*x)][0])
		# First half of new generation is made from best ones from previous generation untouched
		# So we just set the scores to 0 to everyone
		for x in range(0,generation_length):
			self.generation[x][1] = 0
			
def main ():
	# Create a generation of players (each with a score)
	g = Generation(50)

	for x in range(0,20):
		# Let the current generation play
		g.playTournament()
		# Sort the winners
		g.sort_by_score()
		# Show a demo
		board = TicTacToe()
		[a, b, result] = g.playGame(g.generation[0][0], g.generation[1][0], board)
		board.display()
		print(result)
		# Evolve to next generation
		g.evolve(display=True)

	g.playTournament()
	g.sort_by_score()
	# Show a demo
	board = TicTacToe()
	[a, b, result] = g.playGame(g.generation[0][0], g.generation[1][0], board)
	board.display()
	print(result)
	
	print("Ending scores : ", end="")
	for x in range(0,g.generation.__len__()):
		print(g.generation[x][1], " ", end="")
	print("")

if __name__ == "__main__":
	main()