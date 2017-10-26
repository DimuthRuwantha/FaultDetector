import numpy as np
from . import util
from datetime import datetime as dt

from sklearn.neural_network import multilayer_perceptron as nn

from ArtificialNeuralNetwork.NeuralNetwork import NeuralNetObject

css = None


class NeuralNets(object):

    clf = None
    x = 0

    def __init__(self, algorithm='lbfgs', h_l_size=7, ratio=0.50):

        self.x += 1
        print('Printing django {0}'.format(self.x))
        start = dt.now()
        self.training, self.testing, self.classes = util.file_reader(ratio=ratio)

        end = dt.now()

        self.clf = nn.MLPClassifier(solver=algorithm, alpha=1e-5, hidden_layer_sizes=h_l_size, random_state=1)
        print("time elapsed to load data : ", end - start)

    def get_matrices(self, training_set=[]):
        matrix_list = []
        output_list = []
        for lst in training_set:
            matrix_list.append(lst[:-1])
            output_list.append(lst[6])
        output_array = self.process_output_matrix(output_list)
        input_array = np.array(matrix_list)
        return input_array, output_array

    @staticmethod
    def process_fault(result_list=[]):
        out = []
        for result in result_list:

            f_value = "{0}{1}{2}{3}".format(result[0], result[1], result[2], result[3])
            b_value = int(f_value, 2)

            if b_value == 13:
                out.append("A to B to Grd")

            elif b_value == 12:
                out.append('A to B')

            elif b_value == 10:
                out.append('C to A')

            elif b_value == 9:
                out.append('A to Grd')

            elif b_value == 7:
                out.append('B to C to Grd')

            elif b_value == 6:
                out.append('B to C')

            elif b_value == 5:
                out.append('B to Grd')

            elif b_value == 3:
                out.append('C to Grd')

            elif b_value == 11:
                out.append('A to C to Grd')

            elif b_value == 0:
                out.append('no Fault')
            else:
                out.append('Anomaly Behaviour')
        return out

    def process_output_matrix(self, output_list=[]):
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

    def check_accuracy(self, results, output):
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
        return accuracy, round((accuracy / output_length) * 100, 2)

    # def run(self, algorithm='lbfgs', h_l_size=7, ratio=0.50, test_accuracy=True, reset=True):
    def run(self, test_accuracy=True, reset=True):
        if reset:
            accuracy = "-"
            predicted_correct = "-"
            tr_in_matrix1 = []
            tr_out_matrix1 = []
            tst_in_matrix1 = []
            tst_out_matrix1 = []
            training = []
            testing = []

        tr_in_matrix1, tr_out_matrix1 = self.get_matrices(self.training)
        tst_in_matrix1, tst_out_matrix1 = self.get_matrices(self.testing)
        self.clf.fit(tr_in_matrix1, tr_out_matrix1)

        NeuralNets.clf = self.clf
        NeuralNets.css = self.clf
        NeuralNetObject.k = self.clf

        if test_accuracy:
            a = self.clf.predict(tst_in_matrix1)
            print(a)
            predicted_correct, accuracy = self.check_accuracy(a, tst_out_matrix1)
            print(accuracy)

        return len(self.training), len(self.testing), predicted_correct, accuracy

    def predict(self, predict_list):

        results = self.clf.predict(predict_list)

        return results

    def get_ann_classifier(self):
        return self.clf
