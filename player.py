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
	name = None
	
	def __init__(self, name):
		self.W = tf.Variable(np.random.rand(9,9))
		self.b = tf.Variable(np.random.rand(9))
		self.initial_position = tf.placeholder(tf.float64, shape=(1, 9))
		self.name = name

	def load_player(self):
		pass

	def play(self, board):
		init = tf.initialize_all_variables()
		# Position played is a softmax regression of ( (W * initial_position) + b)
		played = tf.nn.softmax(tf.matmul(self.initial_position, self.W) + self.b)
		with tf.Session() as sess:
			sess.run(init, feed_dict={self.initial_position: board})
			result = sess.run(played, feed_dict={self.initial_position: board})
		move = result.argmax()
		x = (int)(move / 3)
		y = move%3
		return (x, y)


def main ():
	from tictactoe import TicTacToe
	board = TicTacToe()

	# Create two players
	player1 = Player("First")
	player2 = Player("Second")

	# Play
	(winner, result) = board.autoPlay(player1, player2)
		
	board.display()
	print (result)


if __name__ == "__main__":
	main()