from Collisions.NeutralGas import NeutralGas
from scipy.constants import k
import numpy as np
import math

class IonizedGas(NeutralGas):
    def __init__(self, T, n, mass, Z, name=None):
        super(IonizedGas, self).__init__(T, n, mass, name)
        self.coullog = math.log(743*((1.5*k*T*6.242e+18)**1.5)/4.8e-8/math.sqrt(n)/Z)
        print(self.coullog)
   
    def gen_vel_vector(self):
        sigma = math.sqrt(k*self.T/self.mass)
        return np.random.randn(3,120) * sigma