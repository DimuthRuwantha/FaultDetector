import numpy as np

from ..NeuralNetwork.NeuralNetObject import NeuralNetObject
from ..training.SigmoidFunction import SigmoidFunction


# Created by DimRu on 23-Jun-17


class TrainingNetwork:
    """ After the dummy neural network has been created, training with back propagation is done here """

    def __init__(self):
        self.__input = np.array([[]])
        self.__output = np.array([[]])

        self.__sigmoid = SigmoidFunction()

    def training_network(self, x=list([[]]), y=list([[]])):
        self.__input = np.array(x)
        self.__output = np.array(y)

        neural_object = NeuralNetObject()
        syn0, syn1 = neural_object.create_network(x, y)

        print("Training network")
        j = 0
        while True:
            # Feed forward part of the neural network
            layer_0 = self.__input
            layer_1 = self.__sigmoid.nonlin(np.dot(layer_0, syn0))    # dot product of input and weights to the sigmoid function
            layer_1 = np.insert(layer_1, 0, 1, axis=1)
            layer_2 = self.__sigmoid.nonlin(np.dot(layer_1, syn1))    # dot product of hidden layer and weights to the function

            layer2_error = self.__output - layer_2
            # if abs(layer2_error.max()) < 0.01:
            #     print(layer2_error.max())
                # break
            if j > 60000 and abs(layer2_error.max()) < 0.005:
                print(layer2_error.max())
                break
            elif j > 210000:
                # pass
                break

            if j % 10000 == 0:
                # print(".", sep=' ', end='', flush=True)
                print("Maximum error at iteration {0} = {1}".format(j, layer2_error.max()))

            # back propagation
            layer2_delta = layer2_error * self.__sigmoid.nonlin(layer_2, True)
            layer1_error = layer2_delta.dot(syn1.T)

            l1_delta = layer1_error * self.__sigmoid.nonlin(layer_1, True)

            syn1 += layer_1.T.dot(layer2_delta)
            l1_delta = np.delete(l1_delta, 0, axis=1)
            syn0 += layer_0.T.dot(l1_delta)
            j += 1
        print("Completed j: ", j)

        return layer_2, syn0, syn1
