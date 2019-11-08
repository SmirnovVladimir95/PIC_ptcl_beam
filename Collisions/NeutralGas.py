"""
This file containes class for a buffer gas
"""
import numpy as np
from scipy.constants import k
import math

class NeutralGas:
    def __init__(self, T, n, mass):
        self.T = T
        self.n = n
        self.mass = mass
    
    def gen_vel_vector(self):
        sigma = math.sqrt(k*self.T/self.mass)
        return sigma * np.random.randn(3)