from NeuralNetwork import *

class Player:
    def __init__(self, sign='O'):
        self.nn = NeuralNetwork(9, 27, 9)
        self.sign = sign
    
    def mutate(self, chance, delta):
        self.nn.mutate(chance, delta)
    
    def duplicate(self):
        return copy.deepcopy(self)
    
    def set_sign(self, sign):
        self.sign = sign
    
    def get_sign(self):
        return self.sign
    
    def play(self, board):
        if board.is_full() == True:
            return
        
        state = board.get_state_flattened()

        if self.sign == 'O':
            for i in range(9):
                if state[0][i] == 1:
                    state[0][i] == -1
                elif state[0][i] == -1:
                    state[0][i] == 1

        prediction = self.nn.predict(state)
        prediction = prediction.reshape((3, 3))

        #self.nn.print_weights()
        #print(prediction)
        #print(prediction.max())
        
        max_value = prediction.max()
        max_index = np.where(prediction == max_value)
        max_index = (max_index[0][0], max_index[1][0])
        move_made = False

        attempts = 0

        while not move_made:
            if board.is_empty(max_index):
                if self.sign == 'X':
                    board.mark_X(max_index)
                elif self.sign == 'O':
                    board.mark_O(max_index)
                move_made = True
            else:
                prediction[max_index[0]][max_index[1]] = max_value - 1

                max_value = prediction.max()
                max_index = np.where(prediction == max_value)
                max_index = (max_index[0][0], max_index[1][0])

                attempts += 1

                if attempts == 9:
                    print("Hello world")
                    return