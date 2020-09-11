from Collisions.NeutralGas import NeutralGas
from scipy.constants import k, epsilon_0	, e, pi
import numpy as np
import math

class IonizedGas(NeutralGas):
    def __init__(self, T, n, mass, Z, name=None):
        super(IonizedGas, self).__init__(T, n, mass, name)
        r_d = (epsilon_0 * k * T / (e**2 * n)) ** 0.5    #n in meters
        self.coullog = np.log(12 * pi * n * r_d ** 3 / Z)
        print(self.coullog)
   
    def gen_vel_vector(self, n_total):
        sigma = math.sqrt(k*self.T/self.mass)
        return np.random.randn(3,n_total) * sigma