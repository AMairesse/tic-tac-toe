#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# Use "print" in the Python3 way even if used with Python2
from __future__ import print_function
import tensorflow as tf
from generation import Generation
import unittest

class GenerationtestCase(unittest.TestCase):
	# Public attribute
	session = None

	def setUp(self):
		# Create a TensorFlow session
		self.session = tf.InteractiveSession()

	def testNoMemoryLeak(self):
		# Create a generation of players (each with a score)
		g = Generation(4)
		memory_objects_start = tf.all_variables().__len__()
		# Let the current generation play
		g.playTournament(self.session)
		# Sort the winners
		g.sort_by_score()
		# Evolve to next generation
		g.evolve()
		memory_objects_end = tf.all_variables().__len__()
		self.assertEqual(memory_objects_start, memory_objects_end)

if __name__ == '__main__':
    unittest.main()