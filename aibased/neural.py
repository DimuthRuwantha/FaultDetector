from ArtificialNeuralNetwork import neuralNets


def run(algorithm='lbfgs', h_l_size=7, ratio=0.5, test_accuracy=True):
    return neuralNets.run(algorithm=algorithm, h_l_size=h_l_size, ratio=ratio, test_accuracy=test_accuracy)

def test():
    pass


if __name__ == '__main__':
    tr, tst, pred, acc = neuralNets.run(algorithm='lbfgs', h_l_size=7, ratio=50, test_accuracy=True)
    print(tr)
    print(tst)
    print(pred)
    print(acc)


