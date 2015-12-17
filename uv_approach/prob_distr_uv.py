class ProbDist:
    def __init__(self):
        self.values = dict()

    def get_probability(self, uv):
        prob = self.values.get(uv, 0)
        return prob

    def fill_bin(self, uv, prob):
        self.values[uv] = prob
