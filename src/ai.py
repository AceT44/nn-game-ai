import numpy as np


class NeuralNetwork:
    def __init__(self):
        self.weights = np.random.random((3, 1))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def predict(self, inputs):
        weighted_sum = np.dot(inputs, self.weights)
        output = self.sigmoid(weighted_sum)

        return output

    def train(self):
        pass
