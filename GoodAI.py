from Board import *
import math
import random

COMP = 1
PLAYER = -1

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False

def empty_cells(state):
    cells = []

    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                cells.append([i, j])
    
    return cells

def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, PLAYER):
        score = -1
    else:
        score = 0

    return score
    
def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -math.inf]
    else:
        best = [-1, -1, +math.inf]

    if depth == 0 or wins(state, PLAYER) or wins(state, COMP):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score
        else:
            if score[2] < best[2]:
                best = score

    return best

class GoodAI:
    def __init__(self, sign='O'):
        self.sign = sign
        self.opp_sign = 'X' if self.sign == 'O' else 'O'
    
    def set_sign(self, sign):
        self.sign = sign
        self.opp_sign = 'X' if self.sign == 'O' else 'O'
    
    def play(self, board, index=None):
        if self.sign == 'O':
            state = board.get_state_flipped()
        else:
            state = board.get_state()

        empty = empty_cells(state)
        depth = len(empty)
        
        if depth == 9:
            best_move = (random.randint(0, 2), random.randint(0, 2))
        elif depth == 8 and not [1, 1] in empty:
            corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
            empty_corners = []
            
            for corner in corners:
                if corner in empty:
                   empty_corners.append(corner)

            if index == None:
                index = random.randint(0, len(empty_corners) - 1)
                best_move = empty_corners[index]
            else:
                best_move = empty_corners[min(index, len(empty_corners) - 1)]
        elif depth == 8:
            best_move = [1, 1]
        else:
            best_move = minimax(state, depth, COMP)

        if self.sign == 'X':
            board.mark_X((best_move[0], best_move[1]))
        elif self.sign == 'O':
            board.mark_O((best_move[0], best_move[1]))