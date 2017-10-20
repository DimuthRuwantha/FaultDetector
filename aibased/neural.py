from ArtificialNeuralNetwork import NeuralNets


def run(algorithm='lbfgs', h_l_size=7, ratio=0.5, test_accuracy=True):

    return NeuralNets.run(algorithm=algorithm, h_l_size=h_l_size, ratio=ratio, test_accuracy=test_accuracy)


# def test():
#     pass
#
#
# if __name__ == '__main__':
#     tr, tst, pred, acc = run(algorithm='lbfgs', h_l_size=7, ratio=50, test_accuracy=True)
#     print(tr)
#     print(tst)
#     print(pred)
#     print(acc)


