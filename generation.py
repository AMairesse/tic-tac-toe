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
	board = None
	sess = None

	def __init__(self, size, session):
		self.sess = session
		self.board = TicTacToe()		
		for x in xrange(0, size):
			player = Player(self.sess)
			player.init_from_random()
			self.generation.append([player, 0])

	def play(self, display=False):
		# Everyone plays against each other
		# Winner earn a point
		for x in xrange(0,self.generation.__len__()):
			for y in xrange(x+1,self.generation.__len__()):
				self.board.clear()
				(winner, result) = self.board.autoPlay(self.generation[x][0], self.generation[y][0])
				if display:
					print (x, "playing against", y)
					self.board.display()
					print(result)
				if winner == self.generation[x][0]:
					self.generation[x][1] = self.generation[x][1] + 1
				else:
					self.generation[y][1] = self.generation[y][1] + 1

	def sort_by_score(self):
		# Order players in the current generation by score
		self.generation.sort(key=operator.itemgetter(1), reverse=True)

	def demo(self):
		# Play a board game between the first ones to see progress
		self.board.clear()
		(winner, result) = self.board.autoPlay(self.generation[0][0], self.generation[1][0])
		self.board.display()
		print(result)

	def evolve(self, display=False):
		generation_length = self.generation.__len__()

		if display:
			print("Ending scores : ", end="")
			for x in xrange(0,generation_length):
				print(self.generation[x][1], " ", end="")
			print("***** New generation created *****")

		# Second half of new generation is made from 1 with 2, 3 with 4, etc.
		# Start by the end and replace starting with the last one
		for x in xrange(0,generation_length/2):
			self.generation[generation_length-1-x][0].init_from_parents(self.generation[generation_length-1-(2*x)][0], self.generation[generation_length-2-(2*x)][0])
		# Second quater of new generation is made random
		for x in xrange(generation_length/4,generation_length/2):
			self.generation[x][0].init_from_random()
		# First quater of new generation is made from best ones from previous generation untouched
		# So we just set the scores to 0 to everyone
		for x in xrange(0,generation_length):
			self.generation[x][1] = 0
			
def main ():
	# Create a TensorFlow session
	session = tf.InteractiveSession()

	# Create a generation of players (each with a score)
	g = Generation(15, session)

	for x in xrange(0,10):
		# Let the current generation play
		g.play()
		# Sort the winners and show a demo
		g.sort_by_score()
		g.demo()
		# Evolve to next generation
		g.evolve(display=True)
		print ("Number of variables in the session :", tf.all_variables().__len__())

	g.play()
	g.sort_by_score()
	print("Ending scores : ", end="")
	for x in xrange(0,g.generation.__len__()):
		print(g.generation[x][1], " ", end="")
	print("")
	print("Last demo")
	g.demo()

if __name__ == "__main__":
	main()