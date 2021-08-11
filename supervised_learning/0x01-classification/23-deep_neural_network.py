#!/usr/bin/env python3
"""a deep neural network performing binary classification"""
import numpy as np
import matplotlib.pyplot as plt


class DeepNeuralNetwork:
    """a deep neural network performing binary classification"""

    def __init__(self, nx, layers):
        """nx is the number of input features to the neuron
        layers is a list representing the number of nodes in each layer"""
        if not isinstance(nx, int):
            raise TypeError("nx must be an integer")
        elif nx < 1:
            raise ValueError("nx must be a positive integer")
        if not isinstance(layers, list) or layers == []:
            raise TypeError("layers must be a list of positive integers")
        self.__L = len(layers)
        self.__cache = {}
        self.__weights = {}
        for i in range(self.__L):
            if not isinstance(layers[i], int) or layers[i] <= 0:
                raise TypeError("layers must be a list of positive integers")
            if i == 0:
                a = nx
            else:
                a = layers[i - 1]
            self.__weights['W' + str(i + 1)
                           ] = np.random.randn(layers[i], a) * np.sqrt(2 / a)
            self.__weights['b' + str(i + 1)] = np.zeros((layers[i], 1))

    @property
    def L(self):
        return self.__L

    @property
    def cache(self):
        return self.__cache

    @property
    def weights(self):
        return self.__weights

    def forward_prop(self, X):
        """Calculates the forward propagation of the neuron
        X: numpy.ndarray with shape (nx, m) that contains the input data"""
        self.__cache['A0'] = X
        for i in range(self.__L):
            self.__cache['A' +
                         str(i +
                             1)] = self.sig(np.dot(self.__weights["W" +
                                                                  str(i +
                                                                      1)],
                                                   self.__cache["A" +
                                                                str(i)]) +
                                            self.__weights["b" +
                                                           str(i +
                                                               1)])
        return self.cache["A" + str(self.__L)], self.__cache

    @staticmethod
    def sig(x):
        """sigmoid function"""
        return 1.0 / (1.0 + np.exp(-x))

    def cost(self, Y, A):
        """Calculates the cost of the model using logistic regression
        Y is a numpy.ndarray containing the correct labels for the input data
        A is a numpy.ndarray containing the activated output"""
        (a, m) = np.shape(Y)
        cost = -1 / m * np.sum(Y * np.log(A) + (1 - Y) *
                               (np.log(1.0000001 - A)))
        return cost

    def evaluate(self, X, Y):
        """Evaluates the neuron’s predictions
        X is a numpy.ndarray tcontaining the input data
        Y is a numpy.ndarray containing the correct labels"""
        pred1, pred2 = self.forward_prop(X)
        predic2 = np.where(pred2["A" + str(self.__L)] >= 0.5, 1, 0)
        return predic2, self.cost(Y, pred2["A" + str(self.__L)])

    def gradient_descent(self, Y, cache, alpha=0.05):
        """calculates one pass of gradient descent on the neuron
          X is a numpy.ndarray containing the input data
          Y is a num py.ndarray containing the correct labels
          A is a numpy.ndarray containing the activated output
          alpha is the learning rate"""
        (nx, m) = np.shape(Y)
        grad = cache["A" + str(self.__L)] - Y
        for i in range(self.__L, 0, -1):
            grada = np.matmul(grad, cache["A" + str(i - 1)].T) / m
            gradb = np.sum(grad, axis=1, keepdims=True) / m
            grad = np.matmul(self.__weights["W" + str(i)].T, grad) * (
                cache["A" + str(i - 1)] * (1 - cache["A" + str(i - 1)]))
            self.__weights["W" + str(i)] -= alpha * grada
            self.__weights["b" + str(i)] -= alpha * gradb

    def train(
            self,
            X,
            Y,
            iterations=5000,
            alpha=0.05,
            verbose=True,
            graph=True,
            step=100):
        """Trains the neuron"""
        if not isinstance(iterations, int):
            raise TypeError("iterations must be an integer")
        elif iterations < 0:
            raise ValueError("iterations must be a positive integer")
        if not isinstance(alpha, float):
            raise TypeError("alpha must be a float")
        elif alpha < 0:
            raise ValueError("alpha must be positive")
        if verbose or graph:
            if not isinstance(step, int):
                raise TypeError("step must be an integer")
            elif step < 0 or step > iterations:
                raise ValueError("step must be positive and <= iterations")
        x = []
        y = []
        for i in range(iterations + 1):
            A, c = self.forward_prop(X)
            self.gradient_descent(Y, self.__cache, alpha)
            if verbose is True and i % step == 0:
                print(
                    "Cost after {} iterations: {}".format(
                        i, self.cost(
                            Y, A)))
                if graph:
                    x.append(self.cost(Y, A))
                    y.append(i)
        if graph is True:
            plt.plot(y, x, color="blue")
            plt.xlabel('iteration')
            plt.ylabel('cost')
            plt.title("Training Cost")
            plt.show()
        return self.evaluate(X, Y)
