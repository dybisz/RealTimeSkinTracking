import cv2

from uv_approach.histogram_uv import HistogramUV
from uv_approach.prob_distr_uv import ProbDist
import numpy as np

class SkinClassifierUV:
    def __init__(self):
        self.skin_histogram = HistogramUV()
        self.non_skin_histogram = HistogramUV()
        self.skin_dist = ProbDist()
        self.theta_max = 0.4
        self.lower_boundary_skin = [0, 0, 0]
        self.upper_boundary_skin = [255, 255, 255]
        self.masks = []

    def load_rgb(self, url):
        return cv2.imread(url, 1)

    def load_yuv(self, url):
        img_in = cv2.imread(url, 1)
        img_out = cv2.cvtColor(img_in, cv2.COLOR_BGR2YUV)
        return img_out

    def learn_from_database(self):
        for i in range(1,60):
            # img_name = 'img (' + str(i) + ').jpg'
            img_name = 'img (' + str(i) + ').jpg'
            img_original = self.load_rgb("sfa_database/original/" + img_name)
            img_skin = self.load_rgb("sfa_database/skin_extracted/" + img_name)
            img_yuv = self.load_yuv("sfa_database/original/" + img_name)

            height, width, channels = img_original.shape
            v, u, y = cv2.split(img_yuv)

            for i in range(0, width):
                for j in range(0, height):
                    key = u[j][i]//8, v[j][i]//8
                    if self.is_background_color(img_skin[j][i]):
                        self.non_skin_histogram.fill_bin(key)
                    else:
                        self.skin_histogram.fill_bin(key)

            print("[LEARNING] " + img_name + " loaded")

        self.calculate_prob_dist()
        self.calculate_boundaries()

    def is_background_color(self, color):
        return color[0] == 0 and color[1] == 0 and color[2] == 0

    def calculate_prob_dist(self):
        for u in range(0,32):
            for v in range (0, 32):
                key = u, v
                is_skin = self.skin_histogram.get_probability(key)
                is_non_skin = self.non_skin_histogram.get_probability(key)

                if is_skin == 0 or is_non_skin == 0:
                    continue

                T_skin = self.skin_histogram.count / (self.skin_histogram.count + self.non_skin_histogram.count)
                T_non_skin = 1.0 - T_skin
                result = (is_skin * T_skin) / (is_skin * T_skin + is_non_skin * T_non_skin)
                self.skin_dist.fill_bin(key,result)
                print('bin: ', u, v, 'prob', result)

    def calculate_boundaries(self):
        self.masks = []
        U_min_bin = 0
        U_max_bin = 32
        V_min_bin = 0
        V_max_bin = 32
        U_skin_bins = []
        V_skin_bins = []
        temp = []

        # Collect bins with skin colors
        for u in range(0,32):
            for v in range(0,32):
                key = u, v
                if self.skin_dist.get_probability(key) > self.theta_max:
                    U_skin_bins.append(u)
                    V_skin_bins.append(v)
                    temp.append([u,v])

        U_min_bin = min(int(s) for s in U_skin_bins)
        V_min_bin = min(int(s) for s in V_skin_bins)
        U_max_bin = max(int(s) for s in U_skin_bins)
        V_max_bin = max(int(s) for s in V_skin_bins)

        # print('mins: ', U_min_bin, V_min_bin, 'maxs: ', U_max_bin, V_max_bin)
        # print(temp)

        for mask in temp:
            lower = np.array([mask[1]*8, mask[0]*8,0])
            upper = np.array([mask[1]*8 + 8, mask[0]*8 + 8,255])
            self.masks.append([lower, upper])

        # print(self.masks)

    def test(self):
        for i in range(57,65):
            img_name = 'img (' + str(i) + ').jpg'
            print('[TESTING]',img_name)
            img_yuv = self.load_yuv("sfa_database/original/" + img_name)

            height, width, channels = img_yuv.shape
            v, u, y = cv2.split(img_yuv)

            for i in range(0, width):
                for j in range(0, height):
                    key = u[j][i]//8, v[j][i]//8
                    prob = self.skin_dist.get_probability(key)
                    if(prob > self.theta_max):
                        img_yuv[j][i] = [255, 255, 255]

            cv2.imshow('image',img_yuv)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    def mark_skin(self, img_rgb):

        img_yuv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2YUV)
        # e1 = cv2.getTickCount()
        ############## TEST ########################
        # just for one mask
        new_masks = []
        for mask in self.masks:
            new_masks.append(cv2.inRange(img_yuv, mask[0], mask[1]))

        final_mask = new_masks[0]
        for i in range(1, len(new_masks)):
            final_mask = cv2.bitwise_or(final_mask, new_masks[i])

        img_rgb = cv2.bitwise_and(img_rgb,img_rgb, mask = final_mask)

        # e2 = cv2.getTickCount()
        # t = (e2 - e1)/cv2.getTickFrequency()
        # print(t)

        return img_rgb

    def increase_theta(self):
        self.theta_max += 0.1
        print('theta_max:',self.theta_max)