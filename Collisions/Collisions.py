"""
This file containes class for Elastic MonteCarlo collisions
between ptcls in ion beam and buffer gas
"""
import numpy as np
from numpy.linalg import norm
from numpy.random import uniform


class MonteCarloCollision(object):
    def __init__(self, sigma, dt, gas):
        """
        Parameters
        ----------
        sigma - reaction cross section
        n - the concentration of neutral gas
        dt - the integration step at which the collision 
            probability is estimated
        mass - mass of neutral gas
        """
        self.sigma = sigma
        self.gas = gas
        self.dt = dt

class IonNeutralElasticCollision(MonteCarloCollision):
    
    """Elastic collision"""
    
    def __init__(self, sigma, dt, gas, ions):
        """
        ions: ptcl object
            incident ptcls
        """
        super(IonNeutralElasticCollision, self).__init__(sigma, dt, gas)
        self.ptcls = ions
        
    def _single_vel_update(self, ptcl_idx):
        """
        update velocity for single ptcl with idx: ptcl_idx
        Parameters
        ----------
        ptcl_idx: int
            index of ptcl
        """
        gas_vel = self.gas.gen_vel_vector()
        R = self._isotropic_vector(1)
        ion_vel = self.ptcls.get_vel(ptcl_idx)
        delta_p = norm(ion_vel - gas_vel)*self.gas.mass*R
        new_ion_vel = (delta_p + self.ptcls.mass*ion_vel + self.gas.mass*gas_vel) / (self.ptcls.mass + self.gas.mass)
        self.ptcls.set_vel(ptcl_idx=ptcl_idx, vel=new_ion_vel)
    
    def vel_update(self):
        """
        update velocity for all ptcls
        """
        for ptcl_idx in xrange(self.ptcls.Ntot):
            v = norm(self.ptcls.get_vel(ptcl_idx))
            if self.sigma*self.gas.n*self.dt*v > uniform(0, 1):
                self._single_vel_update(self, ptcl_idx)
    
    @staticmethod
    def _isotropic_vector(vector_module):
        """
        generate isotropic velocity
        Parameters
        ----------
        vector_module: float
            velocity module
        return: 1d numpy.array 
            velocity vector
        """
        vector = np.zeros(3)
        theta = np.pi*np.random.uniform(-1., 1.)
        phi = np.pi*np.random.uniform(-1., 1.)
        vector[0] = vector_module*np.cos(theta)*np.cos(phi)
        vector[1] = vector_module*np.cos(theta)*np.sin(phi)
        vector[2] = vector_module*np.sin(theta)
        return vector