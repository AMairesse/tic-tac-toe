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
	sess = None

	def __init__(self, size, session):
		self.sess = session
		for x in range(0, size):
			player = Player(self.sess)
			player.init_from_random()
			self.generation.append([player, 0])

	def play(self, display=False):
		# Everyone plays against each other
		# Winner earn a point

		# Prepare boards and players
		tournament = []
		for x in range(0,self.generation.__len__()):
			for y in range(x+1,self.generation.__len__()):
				board = TicTacToe()
				tournament.append([board, x, y, True])

		# Prepare
		sign = 'X'
		player_turn = 1
		player_not_playing = 2
		while True:
			fetches = []
			feed_dict = {}
			for x in range(0,tournament.__len__()):
				game = tournament[x]
				if game[3] == True :
					player = self.generation[game[player_turn]][0]
					[move, static] = player.get_tf_work()
					fetches.append(move)
					feed_dict[static] = game[0].readBoard()

			# If all tournament are done then exit
			if fetches == []:
				break

			# Play in parallel
			list_result = self.sess.run(fetches, feed_dict=feed_dict)

			# Apply resulting moves
			for x in range(0,tournament.__len__()):
				game = tournament[x]
				if game[3] == True :
					player = self.generation[game[player_turn]][0]
					(pos_x, pos_y) = player.convert_result(list_result.pop(0))
					allowed_move = game[0].play(sign, pos_x, pos_y)
					if not allowed_move:
						# Current player loose, get points to the two players and remove this game from tournament (set last value to False)
						self.generation[game[player_turn]][1] = self.generation[game[player_turn]][1] + (0.1 * game[0].moves)
						self.generation[game[player_not_playing]][1] = self.generation[game[player_not_playing]][1] + (0.1 * game[0].moves) + 0.5
						game[3] = False
					elif game[0].isThereWinner() != None:
						# Current player won, get points to the two players and remove this game from tournament (set last value to False)
						self.generation[game[player_turn]][1] = self.generation[game[player_turn]][1] + (0.1 * game[0].moves) + 0.5
						self.generation[game[player_not_playing]][1] = self.generation[game[player_not_playing]][1] + (0.1 * game[0].moves)
						game[3] = False
					elif game[0].moves == 9:
						# We have a drawn game, each player earns max moves and a little bonus.
						# Also remove this game from tournament (set last value to False)
						self.generation[game[player_turn]][1] = self.generation[game[player_turn]][1] + (0.1 * game[0].moves) + 0.25
						self.generation[game[player_not_playing]][1] = self.generation[game[player_not_playing]][1] + (0.1 * game[0].moves) + 0.25
						game[3] = False
					# else do nothing and game will continue

			# Revert sign and players turn for next round
			if sign == 'X':
				sign = 'O'
				player_turn = 2
				player_not_playing = 1
			else:
				sign = 'X'
				player_turn = 1
				player_not_playing = 2

	def sort_by_score(self):
		# Order players in the current generation by score
		self.generation.sort(key=operator.itemgetter(1), reverse=True)

	def demo(self):
		# Play a board game between the first ones to see progress
		board = TicTacToe()
		(winner, moves, result) = board.autoPlay(self.generation[0][0], self.generation[1][0])
		board.display()
		print(result)

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
	# Create a TensorFlow session
	session = tf.InteractiveSession()

	# Create a generation of players (each with a score)
	g = Generation(16, session)

	for x in range(0,10):
		# Let the current generation play
		g.play()
		# Sort the winners and show a demo
		g.sort_by_score()
		g.demo()
		# Evolve to next generation
		g.evolve(display=True)

	g.play()
	g.sort_by_score()
	print("Ending scores : ", end="")
	for x in range(0,g.generation.__len__()):
		print(g.generation[x][1], " ", end="")
	print("")
	print("Last demo")
	g.demo()

if __name__ == "__main__":
	main()