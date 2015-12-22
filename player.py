#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function

import tensorflow as tf
import numpy as np

class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		

class Player():
	"""docstring for Player"""

	# Public attribute
	W = None
	b = None
	initial_position = None
	sess = None
	
	def __init__(self, session):
		self.W = tf.Variable(tf.zeros([9,9], tf.float64))
		self.b = tf.Variable(tf.zeros([9], tf.float64))
		self.initial_position = tf.placeholder(tf.float64, shape=(1, 9))
		self.sess = session

	def init_from_random(self):
		op = self.W.assign(np.random.rand(9,9))
		self.sess.run(op)
		op = self.b.assign(np.random.rand(9))
		self.sess.run(op)

	def init_from_parents(self, player1, player2):
		op = self.W.assign((player1.W + player2.W) / 2.0)
		self.sess.run(op)
		op = self.b.assign((player1.b + player2.b) / 2.0)
		self.sess.run(op)

	def play(self, board):
		# Position played is a softmax regression of ( (W * initial_position) + b)
		played = tf.nn.softmax(tf.matmul(self.initial_position, self.W) + self.b)
		result = self.sess.run(played, feed_dict={self.initial_position: board})
		move = result.argmax()
		x = (int)(move / 3)
		y = move%3
		return (x, y)




def main ():
	from tictactoe import TicTacToe
	board = TicTacToe()

	# Create a TensorFlow session
	session = tf.InteractiveSession()

	# Create a generation of players (each with a score)
	generation = []
	for x in xrange(1,10):
		player = Player(session)
		player.init_from_random()
		generation.append([player, 0])

	# Everyone plays against each other
	# Winner earn a point
	for x in xrange(0,generation.__len__()):
		for y in xrange(x+1,generation.__len__()):
			board.clear()
			(winner, result) = board.autoPlay(generation[x][0], generation[y][0])
			board.display()
			print(result)
			if winner == generation[x][0]:
				generation[x][1] = generation[x][1] + 1
			else:
				generation[y][1] = generation[y][1] + 1

	# Display results
	for x in xrange(0,generation.__len__()):
		print ("Player n°", x, "scores ", generation[x][1])

	#child = Player(session)
	#child.init_from_parents(player1, player2)

if __name__ == "__main__":
	main()