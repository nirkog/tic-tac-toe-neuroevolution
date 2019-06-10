import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def mutate_weights(weights, chance, delta):
    for i in range(weights.shape[0]):
        for j in range(weights.shape[1]):
            if np.random.rand(1, 1)[0][0] <= chance:
                sign = -1.0 if np.random.rand(1, 1)[0][0] > 0.5 else 1.0
                change = np.random.rand(1, 1)[0][0] * delta * sign
                weights[i][j] += change

class NeuralNetwork:
    def __init__(self, input_count, hidden_count, output_count):
        self.hidden_weights = np.random.rand(input_count, hidden_count) * 2 - 1
        self.hidden_bias = np.random.rand(1, hidden_count) * 2 - 1
        self.output_weights = np.random.rand(hidden_count, output_count) * 2 - 1
        self.output_bias = np.random.rand(1, output_count) * 2 - 1
    
    def predict(self, inputs):
        z1 = np.dot(inputs, self.hidden_weights) + self.hidden_bias
        a1 = sigmoid(z1)
        z2 = np.dot(a1, self.output_weights) + self.output_bias
        a2 = sigmoid(z2)

        return a2

    def mutate(self, chance, delta):
        mutate_weights(self.hidden_weights, chance, delta)
        mutate_weights(self.hidden_bias, chance, delta)
        mutate_weights(self.output_weights, chance, delta)
        mutate_weights(self.output_bias, chance, delta)
    
    def print_weights(self):
        print('Hidden Weights')
        print(self.hidden_weights)
        print('Hidden Bias')
        print(self.hidden_bias)
        print('Output Weights')
        print(self.output_weights)
        print('Output Bias')
        print(self.output_bias)

    def duplicate(self):
        return copy.deepcopy(self)