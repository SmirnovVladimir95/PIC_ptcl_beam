"""
This file contains functions for magnetic field interpolation 
from grid on ptcls
"""
import numpy as np


def B_interp_on_ptcl(x, y, z, B_interp_func):
    """
    Field interpolation from cartesian grid on a single ptcl
    Parameters
    ----------
    x, y, z: float
        single ptcl position
    B_interp_func: tuple containing three function objects
        each function object is 1d interpolation function
    return: tuple of floats
        interpolated field components for a single ptcl position
    """
    Bx = B_interp_func[0]((x, y, z))
    By = B_interp_func[1]((x, y, z))
    Bz = B_interp_func[2]((x, y, z))
    return Bx, By, Bz


def B_interp_on_ptcls(x, y, z, B_interp_func, Bx=None, By=None, Bz=None):
    """
    Field interpolation from cartesian grid on a single ptcl
    Parameters
    ----------
    x, y, z: float
        single ptcl position
    B_interp_func: tuple containing three function objects
        each function object is 1d interpolation function
    return: tuple of 1d numpy.arrays
        interpolated field components for ptcls positions
    """
    if Bx is None and By is None and Bz is None:
        Bx = np.zeros_like(x)
        By = np.zeros_like(x)
        Bz = np.zeros_like(x)
    #print Bx
    for idx in range(Bx.shape[0]):
        Bx[idx], By[idx], Bz[idx] = B_interp_on_ptcl(
                            x[idx], y[idx], z[idx], 
                            B_interp_func)
    return Bx, By, Bz