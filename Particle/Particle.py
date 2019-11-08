"""
This file determines class with particle data
"""
import numpy as np
from ParticlePusher import ParticlePush, UpdateVelocity
from ElectricFieldInterpolation import compute_Er, E_interp_on_ptcls
from MagneticFieldInterpolation import B_interp_on_ptcls
from scipy.interpolate import interp1d, RegularGridInterpolator


class Particle:
    def __init__(self, mass, charge, pos, vel):
        """
        Parameters
        ----------
        mass: 1D numpy.array
            particles mass
        charge: float
            particles charge
        pos: 2D numpy.array with shape (3, number_of_particles)
            particle initial positions
        vel: 2D numpy.array with shape (3, number_of_particles)
            particle initial velocities
        """
        self.charge = charge
        self.mass = mass
        self.x, self.y, self.z = pos
        self.vx, self.vy, self.vz = vel
        self.Ntot = len(mass)
        
    def set_E(self, phi=None, r=None, E_const=None, kind='linear'):
        """
        Parameters
        ----------
        phi_data: 2d numpy.array with shape (2, number_of_points)
            phi_data contains information about radial potencial
            phi_data[0] - array of r values
            phi_data[1] - array of phi values
        E_const: 1d numpy.array with shape (3,)
            const value for Field in 
            !should be used if phi_data is not specified!
        kind: string (default linear)
            kind of interpolation to be used for phi_data
        """
        if phi is not None and r is not None:
            Er = compute_Er(phi, r)
            self.Er_interp_func = interp1d(r, Er, kind=kind)
            self.Ex, self.Ey = E_interp_on_ptcls(self.Er_interp_func, 
                                   self.x, self.y)
            self.Ez = np.zeros_like(self.x)
        elif E_const is not None:
            Ntot = self.x.shape[0]
            self.Ex = np.ones(Ntot)*E_const[0]
            self.Ey = np.ones(Ntot)*E_const[1]
            self.Ez = np.ones(Ntot)*E_const[2]
        else:
            raise TypeError("function takes 2 arguments: (phi, r)"+ 
                      "or one argument: E_const")
            
    def set_B(self, B=None, grid=None, B_const=None):
        """
        Parameters
        ----------
        B: tuple containing three 3d numpy.arrays - Bx, By, Bz
        grid: tuple containing three 3d numpy.arrays - gridx, gridy, gridz
            each array contains the points defining 
            the regular grid in 3 dimensions for Bx, By, Bz respectively
        B_const: 1d numpy.array with shape (3,)
            const value for Field in 
            should be used if B and grid are not specified
        """
        if B is not None and grid is not None:
            self.B_interp_func = (RegularGridInterpolator(grid, B[0],
                          bounds_error = False), 
                          RegularGridInterpolator(grid, B[1],
                          bounds_error = False),
                          RegularGridInterpolator(grid, B[2],
                          bounds_error = False))
            _B = B_interp_on_ptcls(self.x, self.y, self.z,
                           self.B_interp_func)
            self.Bx, self.By, self.Bz = _B
        elif B_const is not None:
            Ntot = self.x.shape[0]
            self.Bx = np.ones(Ntot)*B_const[0]
            self.By = np.ones(Ntot)*B_const[1]
            self.Bz = np.ones(Ntot)*B_const[2]
        else:
            raise TypeError("function takes 2 arguments: (B, grid)")
    
    def E_interp(self):
        """
        Interpolate field from grid to particles
        """
        E_interp_on_ptcls(self.Er_interp_func, self.x, self.y, 
                   self.Ex, self.Ey)
        
    def B_interp(self):
        """
        Interpolate field from grid to particles
        """
        B_interp_on_ptcls(self.x, self.y, self.z,
                   self.B_interp_func, 
                   self.Bx, self.By, self.Bz)
    
    def vel_push(self, dt):
        """
        velocity pusher
        Parameters
        ----------
        dt: float
            time integration step
        """
        UpdateVelocity(self.vx, self.vy, self.vz, 
                 self.Ex, self.Ey, self.Ez, self.Bx, 
                 self.By, self.Bz, dt, self.charge, self.mass, 
                 self.x.shape[0])
        
    def push(self, dt):
        """
        coordinate pusher
        Parameters
        ----------
        dt: float
            time integration step
        """
        ParticlePush(self.x, self.y, self.z, 
                self.vx, self.vy, self.vz,
                self.Ex, self.Ey, self.Ez,
                self.Bx, self.By, self.Bz, dt, 
                self.charge, self.mass, 
                self.x.shape[0])
        
    def set_vel(self, vel, idx):
        """
        Parameters
        ----------
        vel: 1d numpy.array
            specify velocity for a ptcl with ptcl_idx=idx
        idx: int
            ptcl index
        """
        self.vx[idx] = vel[0]
        self.vy[idx] = vel[1]
        self.vz[idx] = vel[2]
        
    def get_pos(self):
        """
        return: tuple with shape (3,), containing 
            three 1d numpy.arrays with ptcls positions 
        """
        return self.x, self.y, self.z
    
    def get_vel(self, idx=None):
        """
        Parameters
        ----------
        idx: int
            ptcl index
        return: tuple with shape (3,), containing 
            three 1d numpy.arrays with ptcls velocities 
        """
        if idx:
            return np.array([self.vx[idx], self.vy[idx], 
                      self.vz[idx]])
        return self.vx, self.vy, self.vz
        
    def get_E(self):
        """
        return: tuple with shape (3,), containing 
            three 1d numpy.arrays with ptcls electric field 
        """
        return self.Ex, self.Ey, self.Ez
    
    def get_B(self):
        """
        return: tuple with shape (3,), containing 
            three 1d numpy.arrays with ptcls magnetic field
        """
        return self.Bx, self.By, self.Bz
        

if __name__ == '__main__':
    Ntot = 10
    ptcl = Particle(mass=np.ones(Ntot), charge=-1, pos=np.ones((3, Ntot)),
              vel=np.ones((3, Ntot)))