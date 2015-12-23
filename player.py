#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function

import tensorflow as tf
import numpy as np

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

	#def __delete__(self):
	#	pass

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

	def get_tf_work(self):
		# Position played is a softmax regression of ( (W * initial_position) + b)
		calcul = tf.nn.softmax(tf.matmul(self.initial_position, self.W) + self.b)
		return ([calcul, self.initial_position])

	def convert_result(self, result):
		move = result.argmax()
		x = (int)(move / 3)
		y = move%3
		return (x, y)

	def play(self, board):
		[calcul, placeholder] = self.get_tf_work()
		result = self.sess.run(calcul, feed_dict={placeholder: board})
		return self.convert_result(result)
