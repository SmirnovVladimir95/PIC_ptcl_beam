from Collisions.NeutralGas import NeutralGas
from scipy.constants import k
import math
import numpy as np

class IonizedGas(NeutralGas):
    def __init__(self, T, n, mass, name=None):
        super(IonizedGas, self).__init__(T, n, mass, name)
        self.coullog = math.log(7430*10/4.8e-10/math.sqrt(n))
        
    def gen_vel_vector(self):
        sigma = math.sqrt(k*self.T/self.mass)
        return np.random.randn(3,120) * sigma