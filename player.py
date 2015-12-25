#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function

import tensorflow as tf
import numpy as np
import random

class Player():
	"""docstring for Player"""

	# Public attribute
	W = None
	b = None
	
	def __init__(self):
		self.W = None
		self.b = None

	def init_from_random(self):
		# Randomize between -1 and 1
		self.W = np.random.rand(9,9)*2-1
		self.b = np.random.rand(9)*2-1

	def init_from_parents(self, player1, player2, mode = "averageAndMutation"):
		if mode == "average":
			self.W = (player1.W + player2.W) / 2.0
			self.b = (player1.b + player2.b) / 2.0
		elif mode == "oneofeach":
			self.W = self.mergeArrays(player1.W, player2.W)
			self.b = self.mergeArrays(player1.b, player2.b)
		elif mode == "oneofeachAndMutation":
			self.W = self.mutation(self.mergeArrays(player1.W, player2.W))
			self.b = self.mutation(self.mergeArrays(player1.b, player2.b))
		elif mode == "averageAndMutation":
			self.W = self.mutation((player1.W + player2.W) / 2.0)
			self.b = self.mutation((player1.b + player2.b) / 2.0)
			

	def mergeArrays(self, A, B):
		Atemp = np.ravel(A)
		Btemp = np.ravel(B)
		result = []
		for x in range(0,Atemp.__len__()):
			if x%2:
				result.append(Atemp[x])
			else:
				result.append(Btemp[x])
		result = np.array(result).reshape(A.shape)
		return(result)

	def mutation(self, A):
		Atemp = np.ravel(A)
		result = []
		for x in range(0,Atemp.__len__()):
			if random.SystemRandom() <= 0.01:
				result.append(random.SystemRandom())
			else:
				result.append(Atemp[x])
		result = np.array(result).reshape(A.shape)
		return(result)

	def convert_result(self, result):
		move = result.argmax()
		x = (int)(move / 3)
		y = move%3
		return (x, y)

	def play(self, game, tf_session = None):
		if tf_session == None:
			sess = tf.Session()
		else:
			sess = tf_session

		with sess.as_default():
			# Position played is a softmax regression of ( (W * initial_position) + b)
			board = tf.placeholder(tf.float64, shape=(1, 9))
			W = tf.placeholder(tf.float64, shape=(9, 9))
			b = tf.placeholder(tf.float64, shape=(9))
			calcul = tf.nn.softmax(tf.matmul(board, W) + b)
			result = sess.run(calcul, feed_dict={board: game, W: self.W, b: self.b})

		if tf_session == None:
			sess.close()
		return self.convert_result(result)
