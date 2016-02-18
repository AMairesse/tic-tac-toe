#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import unittest, tictactoe

class TicTacToetestCase(unittest.TestCase):
	# Public attribute
	game = None

	def setUp(self):
		self.game = tictactoe.TicTacToe()

	def testNoWinner(self):
		self.game.clear()
		self.assertEqual(self.game.isThereWinner(), None)

	def testFirstLineWithX(self):
		self.game.clear()
		self.game.play('X', 0, 0)
		self.game.play('X', 0, 1)
		self.game.play('X', 0, 2)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testSecondLineWithX(self):
		self.game.clear()
		self.game.play('X', 1, 0)
		self.game.play('X', 1, 1)
		self.game.play('X', 1, 2)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testThirdLineWithX(self):
		self.game.clear()
		self.game.play('X', 2, 0)
		self.game.play('X', 2, 1)
		self.game.play('X', 2, 2)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testFirstLineWithO(self):
		self.game.clear()
		self.game.play('O', 0, 0)
		self.game.play('O', 0, 1)
		self.game.play('O', 0, 2)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testSecondLineWithO(self):
		self.game.clear()
		self.game.play('O', 1, 0)
		self.game.play('O', 1, 1)
		self.game.play('O', 1, 2)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testThirdLineWithO(self):
		self.game.clear()
		self.game.play('O', 2, 0)
		self.game.play('O', 2, 1)
		self.game.play('O', 2, 2)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testFirstColumnWithX(self):
		self.game.clear()
		self.game.play('X', 0, 0)
		self.game.play('X', 1, 0)
		self.game.play('X', 2, 0)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testSecondColumnWithX(self):
		self.game.clear()
		self.game.play('X', 0, 1)
		self.game.play('X', 1, 1)
		self.game.play('X', 2, 1)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testThirdColumnWithX(self):
		self.game.clear()
		self.game.play('X', 0, 2)
		self.game.play('X', 1, 2)
		self.game.play('X', 2, 2)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testFirstColumnWithO(self):
		self.game.clear()
		self.game.play('O', 0, 0)
		self.game.play('O', 1, 0)
		self.game.play('O', 2, 0)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testSecondColumnWithO(self):
		self.game.clear()
		self.game.play('O', 0, 1)
		self.game.play('O', 1, 1)
		self.game.play('O', 2, 1)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testThirdColumnWithO(self):
		self.game.clear()
		self.game.play('O', 0, 2)
		self.game.play('O', 1, 2)
		self.game.play('O', 2, 2)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testFirstDiagWithX(self):
		self.game.clear()
		self.game.play('X', 0, 0)
		self.game.play('X', 1, 1)
		self.game.play('X', 2, 2)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testFirstDiagWithO(self):
		self.game.clear()
		self.game.play('O', 0, 0)
		self.game.play('O', 1, 1)
		self.game.play('O', 2, 2)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testSecondDiagWithX(self):
		self.game.clear()
		self.game.play('X', 0, 2)
		self.game.play('X', 1, 1)
		self.game.play('X', 2, 0)
		self.assertEqual(self.game.isThereWinner(), 'X')

	def testSecondDiagWithO(self):
		self.game.clear()
		self.game.play('O', 0, 2)
		self.game.play('O', 1, 1)
		self.game.play('O', 2, 0)
		self.assertEqual(self.game.isThereWinner(), 'O')

	def testPlayControls(self):
		self.game.clear()
		self.assertTrue(self.game.play('O', 0, 0))
		self.assertFalse(self.game.play('X', 0, 0))

	def testReadBoard(self):
		self.game.clear()
		self.game.play('O', 0, 0)
		self.game.play('X', 2, 2)
		self.assertEqual(self.game.readBoard(), [[0.5, 0, 0, 0, 0, 0, 0, 0, 1]])

	def testBestMove(self):
		self.game.clear()
		(x, y) = self.game.best_move('X')
		self.assertEqual(x, 1)
		self.assertEqual(y, 1)

	def testScore(self):
		self.game.clear()
		self.game.play('X', 1, 1)
		score = self.game.score(0,0,'O')
		self.assertEqual(score, -0.8445357084274292)

if __name__ == '__main__':
    unittest.main()