"""
This file contains support function to generate 
initial conditions of ptcls beam
"""
import numpy as np
from numpy.random import random_sample, randn
from scipy.constants import pi


def gen_mass(mean, sigma, Ntot):
    """
    Generate mass vector from gauss distribution
    Parameters
    ----------
    mean: float
        mean value of gauss distribution
    sigma: float
        sigma value of gauss distribution
    Ntot: int
        size of mass vector (according to number of ptcls)
    """
    return (sigma*randn(Ntot) + mean)

def gen_velocity(vel_module, phi, theta):
    """
    Generate single velocity vector
    Parameters
    ----------
    vel_module: float
        ptcl velocity module
    phi: tuple
        angle bounds in spherical coordinate system
    theta: tuple
        angle bounds in spherical coordinate system
    return: 1d numpy.array
        single velocity vector
    """
    theta_rand = (theta[1]-theta[0])*random_sample() + theta[0]
    phi_rand = (phi[1]-phi[0])*random_sample() + phi[0]
    vel_x = vel_module*np.sin(theta_rand)*np.cos(phi_rand)
    vel_y = vel_module*np.sin(theta_rand)*np.sin(phi_rand)
    vel_z = vel_module*np.cos(theta_rand)
    return np.array([vel_x, vel_y, vel_z])

def gen_velocities(E_range, m, theta, phi=(0, 2*pi)):
    """
    Generate velocity vectors for ptcls
    Parameters
    ----------
    E_range: tuple
        energy range
    m: 1d numpy.array
        ptclmass vector
    vel_module: float
        ptcl velocity module
    phi: tuple
        angle bounds in spherical coordinate system
    theta: tuple
        angle bounds in spherical coordinate system
    return: 2d numpy.array with shape (3, number_of_ptcls)
        ptcls velocity vector
    """
    Ntot = len(m)
    E = E_range[0] + random_sample(Ntot)*(E_range[1] - E_range[0])
    vel_module = (2*E/m)**(0.5)
    vel = np.zeros((Ntot, 3))
    for i in range(Ntot):
        vel[i, :] = gen_velocity(vel_module[i], phi, theta)
    return vel.T

def gen_positions(pos, sub_width, Ntot):
    """
    Generate ptcls positions
    Parameters
    ----------
    pos: 1d numpy array
        ptcl injection point
    sub_width: float
        size of ptcl region in (x, y) from which 
        ptcls beam is launched
    Ntot: int
        number of ptcls
    """
    init_x = pos[0] - sub_width/2 + random_sample(Ntot)*sub_width
    init_y = pos[1] - sub_width/2 + random_sample(Ntot)*sub_width
    return np.array([init_x, init_y, [pos[2]]*Ntot])