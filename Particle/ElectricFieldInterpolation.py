"""
This file contains functions for electric field interpolation
from grid on ptcls
"""
import numpy as np


def compute_Er(phi, r):
    """
    Parameters
    ----------
    phi: 1d numpy.array
        data of radial electric potencial distribution
    r: 1d numpy.array
        data of radius corresponding to potencial phi
    return: 1d numpy.array
        radial electric field
    """
    Er = np.zeros_like(r)
    dr2 = r[2:] - r[:-2]
    #central difference, not right on walls
    Er[1:-1] = (phi[:-2] - phi[2:]) / (dr2)
    #one sided difference on boundaries
    Er[0] = (phi[0] - phi[1]) / (r[1] - r[0])
    Er[-1] = (phi[-2] - phi[-1]) / (r[-1] - r[-2])
    return Er


def E_interp_on_ptcl(Er_interp_func, x, y):
    """
    Field interpolation from radial grid on a single ptcl
    Parameters
    ----------
    Er_interp_func: function object
        1d interpolation function
    x, y: float
        point in which electric field should be approximated
    return: tuple containing two floats
        Ex, Ey - cartesian components of 
        the radial field in position (x, y)
    """
    r_point = np.linalg.norm([x, y])
    if r_point < 1e-8:
        Ex = 0.
        Ey = 0.
        return Ex, Ey
    Er = Er_interp_func(r_point)
    Ex = Er * x / r_point
    Ey = Er * y / r_point
    return Ex, Ey


def E_interp_on_ptcls(Er_interp_func, ptcls_x, ptcls_y, Ex=None, Ey=None):
    """
    Field interpolation from radial grid on ptcls
    Parameters
    ----------
    Er_interp_func: function object
        1d interpolation function
    ptcls_x, ptcls_y: 1d numpy.arrays
        points in which electric field should be approximated
    Ex, Ey: 1d numpy.arrays
        initial cartesian components of the radial field in
        ptcl positions (ptcls_x, ptcls_y)
    return: tuple containing two 1d numpy.arrays 
        Ex, Ey containing cartesian components of 
        the radial field in ptcl positions (ptcls_x, ptcls_y)
    """
    if Ex is None and Ey is None:
        Ex = np.zeros_like(ptcls_x)
        Ey = np.zeros_like(ptcls_y)
    for idx in range(ptcls_x.shape[0]):
        Ex[idx], Ey[idx] = E_interp_on_ptcl(Er_interp_func, 
                               ptcls_x[idx], ptcls_y[idx])
    return Ex, Ey