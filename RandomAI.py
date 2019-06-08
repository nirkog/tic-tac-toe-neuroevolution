import numpy as np

class RandomAI:
    def __init__(self, sign='O'):
        self.sign = sign
    
    def set_sign(self, sign):
        self.sign = sign
    
    def play(self, board):
        empty_positions = board.get_empty_positions()
        index = int(round(max(0, np.random.rand(1, 1)[0][0] * len(empty_positions) - 1)))
        position = empty_positions[index]

        if self.sign == 'O':
            board.mark_O(position)
        elif self.sign == 'X':
            board.mark_X(position)