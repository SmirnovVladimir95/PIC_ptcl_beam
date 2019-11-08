"""
This file contains numba functions for particles 
positions and velocities update
"""
import numba
from numba import prange
      

@numba.njit(cache=True, fastmath=True)
def UpdateSingleVelocityBoris(vel_x, vel_y, vel_z, Ex, Ey, Ez,
                              Bx, By, Bz, dt, q, m):
    """
    Parameters
    ----------
    vel_x, vel_y, vel_z: float
        velocity components of a single ptcl
    Ex, Ey, Ez: float
        electric field components of a single ptcl
    Bx, By, Bz: float
        magnetic field components of a single ptcl
    dt: float
        time integration step
    q: float
        ptcl charge
    m: float
        ptcl mass
    return: tuple with shape (3,)
        updated velocities 
    """
    tx = (q/m)*Bx*0.5*dt
    ty = (q/m)*By*0.5*dt
    tz = (q/m)*Bz*0.5*dt
    
    t_mag2 = tx*tx + ty*ty + tz*tz
    sx = 2*tx/(1+t_mag2)
    sy = 2*ty/(1+t_mag2)
    sz = 2*tz/(1+t_mag2)
    # v_minus
    v_minus_x = vel_x + (q/m)*Ex*0.5*dt
    v_minus_y = vel_y + (q/m)*Ey*0.5*dt
    v_minus_z = vel_z + (q/m)*Ez*0.5*dt
    # v_prime
    v_minus_cross_t_x = v_minus_y*tz-v_minus_z*ty
    v_minus_cross_t_y = -1*v_minus_x*tz+v_minus_z*tx
    v_minus_cross_t_z = v_minus_x*tz-v_minus_y*tx
    v_prime_x = v_minus_x + v_minus_cross_t_x
    v_prime_y = v_minus_y + v_minus_cross_t_y
    v_prime_z = v_minus_z + v_minus_cross_t_z
    # v_plus
    v_prime_cross_s_x = v_prime_y*sz-v_prime_z*sy
    v_prime_cross_s_y = -1*v_prime_x*sz+v_prime_z*sx
    v_prime_cross_s_z = v_prime_x*sy-v_prime_y*sx
    v_plus_x = v_minus_x + v_prime_cross_s_x
    v_plus_y = v_minus_y + v_prime_cross_s_y
    v_plus_z = v_minus_z + v_prime_cross_s_z
    # vel n+1/2
    vel_x = v_plus_x + (q/m)*Ex*0.5*dt
    vel_y = v_plus_y + (q/m)*Ey*0.5*dt
    vel_z = v_plus_z + (q/m)*Ez*0.5*dt
    return vel_x, vel_y, vel_z


@numba.njit(cache=True)
def UpdateVelocity(vel_x, vel_y, vel_z, Ex, Ey, Ez, Bx, By, Bz, dt, 
                                       q, m, Ntot):
    """
    Parameters
    ----------
    vel_x, vel_y, vel_z: 1d numpy.array with shape (ptcls_number,)
        velocity components of ptcls
    Ex, Ey, Ez: 1d numpy.array with shape (ptcls_number,)
        electric field components of ptcls
    Bx, By, Bz: 1d numpy.array with shape (ptcls_number,)
        magnetic field components of ptcls
    dt: float
        time integration step
    q: float
        ptcl charge
    m: 1d numpy.array with shape (ptcls_number,)
        ptcls mass
    Ntot: int
        ptcls number
    """
    # Loop over particles
    for ip in range(Ntot):
        vel_x[ip], vel_y[ip], vel_z[ip] = UpdateSingleVelocityBoris(
                           vel_x[ip], vel_y[ip], vel_z[ip], 
                           Ex[ip], Ey[ip], Ez[ip], Bx[ip], 
                           By[ip], Bz[ip], dt, q, m[ip])


@numba.njit(cache=True, fastmath=True)
def UpdatePosition(pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, dt, Ntot):
    """
    Parameters
    ----------
    pos_x, pos_y, pos_z: 1d numpy.array with shape (ptcls_number,)
        position components of ptcls
    dt: float
        time integration step
    q: float
        ptcl charge
    m: 1d numpy.array with shape (ptcls_number,)
        ptcls mass
    Ntot: int
        ptcls number
    """
    # Loop over particles
    for ip in prange(Ntot):
        pos_x[ip] += vel_x[ip]*dt
        pos_y[ip] += vel_y[ip]*dt
        pos_z[ip] += vel_z[ip]*dt   


def ParticlePush(pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, Ex, Ey, Ez, 
                       Bx, By, Bz, dt, q, m, Ntot):
    """
    Parameters
    ----------
    pos_x, pos_y, pos_z: 1d numpy.array with shape (ptcls_number,)
        position components of ptcls
    vel_x, vel_y, vel_z: 1d numpy.array with shape (ptcls_number,)
        velocity components of ptcls
    Ex, Ey, Ez: 1d numpy.array with shape (ptcls_number,)
        electric field components of ptcls
    Bx, By, Bz: 1d numpy.array with shape (ptcls_number,)
        magnetic field components of ptcls
    dt: float
        time integration step
    q: float
        ptcl charge
    m: 1d numpy.array with shape (ptcls_number,)
        ptcls mass
    Ntot: int
        ptcls number
    """
    UpdateVelocity(vel_x, vel_y, vel_z, Ex, Ey, Ez, Bx, By, Bz,
                       dt, q, m, Ntot)
    UpdatePosition(pos_x, pos_y, pos_z, vel_x, vel_y, vel_z, dt, Ntot)