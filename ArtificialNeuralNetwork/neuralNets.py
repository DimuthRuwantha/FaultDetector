import numpy as np
from . import util
from datetime import datetime as dt

from sklearn.neural_network import multilayer_perceptron as nn


def get_matrices(training_set=[]):
    matrix_list = []
    output_list = []
    for lst in training_set:
        matrix_list.append(lst[:-1])
        output_list.append(lst[6])
    output_array = process_output_matrix(output_list)
    input_array = np.array(matrix_list)
    return input_array, output_array


def process_output_matrix(output_list=[]):
    out = []
    for fault in output_list:

        if fault == "A to B to Grd":
            out.append([1, 1, 0, 1])

        elif fault == 'A to B':
            out.append([1, 1, 0, 0])

        elif fault == 'C to A':
            out.append([1, 0, 1, 0])

        elif fault == 'A to Grd':
            out.append([1, 0, 0, 1])

        elif fault == 'B to C to Grd':
            out.append([0, 1, 1, 1])

        elif fault == 'B to C':
            out.append([0, 1, 1, 0])

        elif fault == 'B to Grd':
            out.append([0, 1, 0, 1])

        elif fault == 'C to Grd':
            out.append([0, 0, 1, 1])

        elif fault == 'A to C to Grd':
            out.append([1, 0, 1, 1])

        elif fault == 'no Fault':
            out.append([0, 0, 0, 0])
        else:
            out.append([1, 1, 1, 1])
    return np.array(out)


def check_accuracy(results, output):
    accuracy = 0
    output_length = len(output)
    for i in range(output_length):
        k = 0
        for j in range(len(output[i])):
            if results[i][j] == output[i][j]:
                k += 1
            if k == 4:
                accuracy += 1
    print('total no of inputs : ', output_length)
    print("Accurately predicted : ", accuracy)
    return accuracy, (accuracy / output_length) * 100


def run(algorithm='lbfgs', h_l_size=7, ratio=50, test_accuracy=True):
    print('Printing django')
    start = dt.now()
    training, testing, classes = util.file_reader(ratio=ratio)
    tr_in_matrix1, tr_out_matrix1 = get_matrices(training)
    tst_in_matrix1, tst_out_matrix1 = get_matrices(testing)
    end = dt.now()

    clf = nn.MLPClassifier(solver=algorithm, alpha=1e-5, hidden_layer_sizes=h_l_size, random_state=1)
    clf.fit(tr_in_matrix1, tr_out_matrix1)

    print("time elapsed to load data : ", end - start)

    if test_accuracy:
        a = clf.predict(tst_in_matrix1)
        print(a)
        predicted_correct, accuracy = check_accuracy(a, tst_out_matrix1)
        print(accuracy)
        return len(training), len(testing), predicted_correct, accuracy

    return len(training), len(testing)


if __name__ == '__main__':
    tr, tst, pred, acc = run(algorithm='lbfgs', h_l_size=7, ratio=50, test_accuracy=True)
    print(tr)
    print(tst)
    print(pred)
    print(acc)