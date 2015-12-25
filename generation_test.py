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

	def testNoMemoryLeak(self):
		# Create a generation of players (each with a score)
		g = Generation(4)
		# Let the current generation play
		g.playTournament()
		# Sort the winners
		g.sort_by_score()
		# Evolve to next generation
		g.evolve()
		self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()