#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function

import tensorflow as tf
import numpy as np
import random
import ast
import argparse
import json

# Constants (ok, not a constant for Python but anyway that's the idea)
BATCH_SIZE = 1000

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
			
	def load(self, f):
		try:
			data = f.readlines()
			self.W = ast.literal_eval(data[0])
			self.b = ast.literal_eval(data[1])
		except:
			return False
		return True

	def save(self, f):
		try:
			f.write(json.dumps(self.W))
			f.write("\n")
			f.write(json.dumps(self.b))
		except:
			return False
		return True


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
			if random.random() <= 0.01:
				result.append(random.random())
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

	def get_learning_batch(self, data, size, index = None):
		batch_xs = []
		batch_ys = []
		data_size = data.__len__()

		for x in range(0, size):
			if index == None:
				line_nb = random.randint(0, data_size - 1)
			else:
				line_nb = index + x
			line = ast.literal_eval(data[line_nb])
			batch_xs.append(line[0])
			ys = [0., 0., 0., 0., 0., 0., 0., 0., 0.]
			ys[line[1]] = 1.
			batch_ys.append(ys)
		return batch_xs, batch_ys


	def learn(self, data, deep, not_random = False, verbose = False, tf_session = None):
		if tf_session == None:
			sess = tf.Session()
		else:
			sess = tf_session

		with sess.as_default():
			# Placeholders for the board and our "brain"
			board = tf.placeholder(tf.float32, [None, 9])
			W = tf.Variable(tf.zeros([9, 9]))
			b = tf.Variable(tf.zeros([9]))
			# Build our brain
			y = tf.nn.softmax(tf.matmul(board, W) + b)
			# Placeholder for the real moves we want our brain to obtain
			y_ = tf.placeholder(tf.float32, [None, 9])
			# Learning function we will apply (the error between our brain result and optimal result)
			cross_entropy = -tf.reduce_sum(y_*tf.log(y))
			# A step of training is to minimize cross_entropy by 1%
			train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
			# Initialize all variables
			init = tf.initialize_all_variables()
			sess.run(init)
			# Start training
			for i in range(0, deep):
				# Read a batch of values and train
				if not_random:
					batch_xs, batch_ys = self.get_learning_batch(data, BATCH_SIZE, i*BATCH_SIZE)
				else:
					batch_xs, batch_ys = self.get_learning_batch(data, BATCH_SIZE)
				sess.run(train_step, feed_dict={board: batch_xs, y_: batch_ys})
				# If verbose mode then print accuracy level for each batch
				if verbose and ((i+1)%10 == 0):
					print("Trained batch n°", i+1)
					correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
					accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
					batch_xs, batch_ys = self.get_learning_batch(data, 100)
					print("Player accuracy : ", sess.run(accuracy, feed_dict={board: batch_xs, y_: batch_ys}))

			# Save our "brain"
			array = sess.run(W)
			self.W = array.tolist()
			array = sess.run(b)
			self.b = array.tolist()

		if tf_session == None:
			sess.close()
		return True

parser = argparse.ArgumentParser(description='AI Player of Tic-Tac-Toe')
subparsers = parser.add_subparsers(dest='action')
# create the parser for the "learn" command
parser_learn = subparsers.add_parser('learn')
parser_learn.add_argument('--learn-file', type=argparse.FileType('r'), required=True)
parser_learn.add_argument('--player-file', type=argparse.FileType('w'), required=True)
parser_learn.add_argument('--deep', type=int, default=2)
parser_learn.add_argument('-v', action='store_true')
parser_learn.add_argument('--not-random', action='store_true')


if __name__ == "__main__":
	args = parser.parse_args()
	cmdline_args = vars(args)
	if (cmdline_args['action'] == 'learn'):
		# Read learning data
		f = cmdline_args['learn_file']
		data = f.readlines()
		f.close()
		
		# Create a player and teach it
		p = Player()
		deep = cmdline_args['deep']
		not_random = cmdline_args['not_random']
		# if not_random then check deep size
		if not_random:
			max_size = data.__len__()
			if deep * BATCH_SIZE >= max_size:
				print("Error : deep is too high for '--not-random' mode.")
				exit()
		verbose = cmdline_args['v']
		p.learn(data, deep, not_random = not_random, verbose = verbose)

		# Save trained player
		f = cmdline_args['player_file']
		p.save(f)
		f.close()