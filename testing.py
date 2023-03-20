
import unittest
from tictactoe import Board
class TestComputer(unittest.TestCase):
    def test_board(self): # position to look at
        # x x _
        # o o x
        # o _ _
        state = [['x','x','_'],['o','o','x'],['o','_','_']]
        board = Board(state=state)
        self.assertEqual(board.best_move(), 3)

    def test_board0(self): # computer plays win, playing x
        # x x _
        # o o _
        # _ _ _
        state0 = [['x','x','_'],['o','o','_'],['_','_','_']]
        board0 = Board(state=state0)
        self.assertEqual(board0.best_move(), 3)

    def test_board1(self): #computer blocks win, playing o
        # x x o
        # o o x
        # _ x _
        state1 = [['x','x','o'],['o','o','x'],['_','x','_']]
        board1 = Board(state=state1)
        self.assertEqual(board1.best_move(), 7)

    def test_board2(self): #computer plays win, playing o
        # x x _
        # o o _
        # x _ _
        state2 = [['x','x','_'],['o','o','_'],['x','_','_']]
        board2 = Board(state=state2)
        self.assertEqual(board2.best_move(), 6)

    def test_board3(self): # computer blocks win, playing o
        # x x _
        # o _ _
        # x o _
        board3 = Board(state=[['x','x','_'],['o','_','_'],['x','o','_']])
        self.assertEqual(board3.best_move(), 3)

    def test_board4(self):
        # x _ _
        # _ _ _ 
        # _ _ _
        state4 = [['x','_','_'],['_','_','_'],['_','_','_']]
        board4 = Board(state=state4)
        self.assertEqual(board4.best_move(), 5)

    def test_board5(self):
        # x _ o
        # x _ _ 
        # o _ _
        state7 = [['x','_','o'],['x','_','_'],['o','_','_']]
        board7 = Board(state=state7)
        self.assertEqual(board7.best_move(), 5)

    def test_board6(self):
        # _ _ _
        # _ _ _ 
        # _ _ _
        state8 = [['_','_','_'],['_','_','_'],['_','_','_']]
        board8 = Board(state=state8)
        self.assertIn(board8.best_move(), (1,2,3,4,5,6,7,8,9))

    def test_board7(self):
        # _ _ _
        # _ x _ 
        # _ _ _
        state9 = [['_','_','_'],['_','x','_'],['_','_','_']]
        board9 = Board(state=state9)
        self.assertIn(board9.best_move(), (1,3,7,9))

if __name__ == '__main__': unittest.main()