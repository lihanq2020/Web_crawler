import numpy as np
import sys
import math


class LogisticRegression:
    def __init__(self, sents_vec, label):
        self.theta = np.zeros(sents_vec.shape[1])
        self.bias = 0
        self.sents_vec = sents_vec
        self.label = label
        self.cost = 0

    def train(self, lr, num_iterations):
        for i in range(num_iterations):
            sigmoid = lambda t: 1 / (1 + math.e ** -t)
            p = sigmoid(np.dot(self.theta, self.sents_vec.transpose()) + self.bias).astype('float64')
            m = self.sents_vec.shape[0]
            self.cost = -(np.dot(self.label, np.log(p)) + np.dot(1 - self.label, np.log(1 - p))) / m
            self.theta = self.theta - lr * (np.dot(p - self.label, self.sents_vec) / m)
            self.bias = self.bias - lr * (np.sum(p - self.label) / m)
            if i % 100 == 0:
                print('cost value is ' + str(self.cost))

    def predict(self, test_x, test_y):
        sigmoid = lambda t: 1 / (1 + math.e ** -t)
        p = sigmoid(np.dot(self.theta, test_x.transpose()) + self.bias).astype('float64')
        error = np.sum(np.abs(test_y - (p/0.5).astype(np.int))) / test_x.shape[0]
        print("正确率为%s%%" % ((1-error)*100))
        return (p/0.5).astype(np.int)


if __name__ == '__main__':
    l = LogisticRegression()
