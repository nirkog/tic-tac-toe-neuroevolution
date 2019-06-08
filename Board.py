import numpy as np

class Board:
    def __init__(self):
        self.state = np.zeros((3, 3))
    
    def mark_X(self, pos):
        # X is 1
        
        self.state[pos[0]][pos[1]] = 1
    
    def mark_O(self, pos):
        # O is -1
        
        self.state[pos[0]][pos[1]] = -1
    
    def get_state(self):
        return self.state

    def get_state_flattened(self):
        return self.state.reshape((1, 9))
    
    def print_state(self):
        for i in range(3):
            to_print = ''
            for j in range(3):
                to_print += 'X' if self.state[i][j] == 1 else 'O' if self.state[i][j] == -1 else '-'
                to_print += ' '
            print(to_print)
    
    def is_empty(self, pos):
        if self.state[pos[0]][pos[1]] == 0:
            return True
        else:
            return False
    
    def is_full(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return False
        return True
    
    def pos_to_sign(self, pos):
        return 'X' if self.state[pos[0]][pos[1]] == 1 else 'O' if self.state[pos[0]][pos[1]] == -1 else '-'
    
    def check_for_win(self):
        for row in range(3):
            if not self.is_empty((row, 0)):
                if self.state[row][0] == self.state[row][1] and self.state[row][1] == self.state[row][2]:
                    return self.pos_to_sign((row, 0))
        
        for column in range(3):
            if not self.is_empty((0, column)):
                if self.state[0][column] == self.state[1][column] and self.state[1][column] == self.state[2][column]:
                    return self.pos_to_sign((0, column))
        
        if not self.is_empty((0, 0)):
            if self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]:
                return self.pos_to_sign((1, 1))

        if not self.is_empty((0, 2)):
            if self.state[0][2] == self.state[1][1] and self.state[1][1] == self.state[2][0]:
                return self.pos_to_sign((1, 1))
        
        return False
    
    def clear(self):
        for i in range(3):
            for j in range(3):
                self.state[i][j] = 0
    
    def get_empty_positions(self):
        positions = []

        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    positions.append((i, j))
        
        return positions