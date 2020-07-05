"""
This file containes class for a buffer gas
"""
import numpy as np
from scipy.constants import k
import math


class NeutralGas(object):
    def __init__(self, T, n, mass, name=None):
        self.T = T
        self.n = n
        self.mass = mass
        self.name = name or 'default_name'

    def gen_vel_vector(self):
        sigma = math.sqrt(k*self.T/self.mass)
        return np.random.randn(3) * sigma
