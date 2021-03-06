import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np
import cProfile

style.use('ggplot')


class SupportVectorMachine:
    def __init__(self, visualization=True):
        self.visualization = visualization
        self.colors = {1: 'r', -1: 'b'}
        if self.visualization:
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(1, 1, 1)

    # train
    def fit(self, data):
        self.data = data
        #  { ||w||: [w, b] }
        opt_dict = {}

        transforms = [[1, 1],
                      [-1, 1],
                      [-1, -1],
                      [1, -1]]


        #  Refer to move semantics in python to improve performance
        all_data = []
        for yi in self.data:
            for featureSet in self.data[yi]:
                for feature in featureSet:
                    all_data.append(feature)

        self.max_feature_value = max(all_data)
        self.min_feature_value = min(all_data)
        all_data = None # Removing all_data from memory

        # Support vectors yi(xi.w+b) = 1

        step_sizes = [self.max_feature_value * 5,
                      self.max_feature_value * 4,
                      self.max_feature_value * 3,
                      self.max_feature_value * 2,
                      self.max_feature_value * 1,
                      self.max_feature_value * 0.5,
                      self.max_feature_value * 0.3,
                      self.max_feature_value * 0.1,
                      self.max_feature_value * 0.01,
                      # Point of expense
                      self.max_feature_value * 0.001,
                      ]

        # Point of expense
        b_range_multiple = 2

        b_multiple = 5
        # latest_optimum_multiplier = 10
        latest_optimum = self.max_feature_value * 10

        for step in step_sizes:
            w = np.array([latest_optimum, latest_optimum])
            optimized = False
            while not optimized:
                for b in np.arange(-1 * (self.max_feature_value * b_range_multiple),
                                   self.max_feature_value * b_range_multiple,
                                   step * b_multiple):
                    for transformation in transforms:
                        w_t = w * transformation
                        found_option = True

                        for i in self.data:
                            for xi in self.data[i]:
                                yi = i
                                if not yi * (np.dot(w_t, xi) + b) >= 1:
                                    found_option = False

                        if found_option:
                            opt_dict[np.linalg.norm(w_t)] = [w_t, b]

                if w[0] < 0:
                    optimized = True
                    print('Optimized a step')
                else:
                    w = w - step
                    print(w)

            norms = sorted([n for n in opt_dict])
            #  ||w|| : [w, b]
            opt_choice = opt_dict[norms[0]]
            self.w = opt_choice[0]
            self.b = opt_choice[1]
            latest_optimum = opt_choice[0][0] + step * 2

        for yi in self.data:
            for xi in self.data[yi]:
                print(xi, ':', yi * (np.dot(self.w, xi) + self.b))

    def predict(self, features):
        #  sign(Xi . w + b)
        classifier_result = np.sign(np.dot(np.array(features), self.w) + self.b)
        if classifier_result != 0 and self.visualization:
            self.ax.scatter(features[0], features[1], s=25, marker='>',
                            c=self.colors[classifier_result])
        return classifier_result

    def visualize(self):
        [[self.ax.scatter(x[0], x[1], s=25, color=self.colors[i])
          for x in data_set[i]] for i in data_set]

        # hyperplane = x.w+b
        # v = x.w+b
        # psv = 1
        # nsv = -1
        # dec = 0
        def hyperplane(x, w, b, v):
            return (-w[0] * x - b + v) / w[1]

        datarange = (self.min_feature_value * 0.9, self.max_feature_value * 1.1)
        hyp_x_min = datarange[0]
        hyp_x_max = datarange[1]

        # (w.x+b) = 1
        # positive support vector hyperplane
        psv1 = hyperplane(hyp_x_min, self.w, self.b, 1)
        psv2 = hyperplane(hyp_x_max, self.w, self.b, 1)
        self.ax.plot([hyp_x_min, hyp_x_max], [psv1, psv2], 'k', label='+_h.p.')

        # (w.x+b) = -1
        # negative support vector hyperplane
        nsv1 = hyperplane(hyp_x_min, self.w, self.b, -1)
        nsv2 = hyperplane(hyp_x_max, self.w, self.b, -1)
        self.ax.plot([hyp_x_min, hyp_x_max], [nsv1, nsv2], 'k', label='-_sep_h.p.')

        # (w.x+b) = 0
        # positive support vector hyperplane
        db1 = hyperplane(hyp_x_min, self.w, self.b, 0)
        db2 = hyperplane(hyp_x_max, self.w, self.b, 0)
        self.ax.plot([hyp_x_min, hyp_x_max], [db1, db2], 'y--', label='sep_h.p.')

        plt.legend(loc=4)
        plt.show()


data_set = {-1: np.array([[1, 7],
                          [2, 8],
                          [3, 8], ]),

            1: np.array([[5, 1],
                         [6, -1],
                         [7, 3], ])}


clf = SupportVectorMachine()
cProfile.run('clf.fit(data=data_set)') #  Runs training and displays runtime


predict_us = [[0,10],
              [1,3],
              [3,4],
              [3,5],
              [5,5],
              [5,6],
              [6,-5],
              [5,8]]

for j in predict_us:
    clf.predict(j)

clf.visualize()
