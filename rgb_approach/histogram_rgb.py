from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


class HistogramRGB:
    def __init__(self):
        self.bins = dict()
        self.count = 0

    def get_probability(self, uv):
        uv_count = self.bins.get(uv, 0)
        return uv_count / self.count

    def fill_bin(self, uv):
        uv_count = self.bins.get(uv, 0)
        uv_count += 1
        self.bins[uv] = uv_count
        self.count += 1

    def print_prob_distr(self):
        sum = 0
        for key in list(self.bins.keys()):
            count = self.bins[key]
            prob = count / self.count
            print(key, ' P(key): ', prob)
            sum += prob
        print('sum of probabilities: ', sum)

    def plot(self):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y = self.prepare_values()
        # x /= 8.0
        # y /= 8.0
        # print(y)
        hist, xedges, yedges = np.histogram2d(x, y, bins=(32, 32))
        xpos, ypos = np.meshgrid(xedges[:-1] + xedges[1:], yedges[:-1] + yedges[1:])

        xpos = xpos.flatten() / 2.
        ypos = ypos.flatten() / 2.
        zpos = np.zeros_like(xpos)

        dx = xedges[1] - xedges[0]
        dy = yedges[1] - yedges[0]
        dz = hist.flatten()

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
        plt.xlabel("U")
        plt.ylabel("V")

        plt.show()

    def prepare_values(self):
        x = []
        y = []
        for key in list(self.bins.keys()):
            count = self.bins[key]
            print(key[0], key[1], count)
            for foo in range(1,count):
                x.append(key[0])
                y.append(key[1])
            # print(y)

        return np.asarray(x), np.asarray(y)
