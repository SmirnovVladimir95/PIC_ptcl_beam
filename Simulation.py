"""
This file containes function for simulation
of ion beam in constant electric and magnetic fields
with mass, energy, angle velocity distributions
"""
import numpy as np
from scipy.constants import e, N_A, pi
import time
from Particle.Particle import Particle
from Field.LoadField import load_phi_data, load_B_data
from Tools.GenerateBeamConditions import gen_mass, gen_velocities, gen_positions
from Tools.TrackParticles import TrackTraj
from Tools.VisualizeBeam import plot_traj
from Collisions.Collisions import IonNeutralElasticCollision
from Collisions.NeutralGas import NeutralGas
    

def simulation(Ntot, init_pos, energy_range, theta_range, charge, it_num,
         dt, phi_data='PenningPotencial.xlsx', B_data='B_data_full.npy',
         collisions=False, seed=None):
    """
    Parameters
    ----------
    Ntot: int
        number of ptcls in the system
    init_pos: numpy.array with shape (3, Ntot)
        initial positions of particles
    energy_range: tuple
        energy bounds for ptcls
    theta_range: tuple
        angle bounds in spherical coordinate system
    charge: float
        ptcls charge
    it_num: int
        number of time iterations
    dt: float
        time integration step
    phi_data: str
        filepath to electric potencial data
    B_data: str
        filepath to magnetic field data
    collisions: bool
        activate (True) or deactivate (False) ptcls collisions
    seed: int
        random seed
    """
    #---------------------------Particles-----------------------------------
    assert Ntot % 3 == 0
    if seed:
        np.random.seed(seed)
    m_Uranium = 0.235/N_A
    m_235 = np.ones(Ntot/3)*m_Uranium
    m_135 = gen_mass(mean=0.140/N_A, sigma=0.005/N_A, Ntot=Ntot/3)
    m_95 = gen_mass(mean=0.095/N_A, sigma=0.005/N_A, Ntot=Ntot/3)
    m = np.concatenate((m_235, m_135, m_95))
    
    vel = gen_velocities(E_range=energy_range, m=m, theta=theta_range)
    pos = gen_positions(pos=init_pos, sub_width=0.01, Ntot=Ntot)
    ptcl_beam = Particle(mass=m, charge=e, pos=pos, vel=vel)
    #-----------------------------------------------------------------------
    #------------------------------Field------------------------------------
    r, phi = load_phi_data(filepath=phi_data)
    ptcl_beam.set_E(phi=phi, r=r)
    grid, B = load_B_data(filepath=B_data)
    ptcl_beam.set_B(B=B, grid=grid)
    #-----------------------------------------------------------------------
    #---------------------------Collisions----------------------------------
    if collisions:
        #gas = NeutralGas(T=300, n=1e20, mass=6.6e-26)
        #collision_obj = IonNeutralElasticCollision(sigma, dt, gas, 
        #                   ions=ptcl_beam) #init collisions
        pass
    #-----------------------------------------------------------------------
    #-----------------------------Main_Loop---------------------------------
    obj_traj = TrackTraj(ptcl_beam)
    ptcl_beam.vel_push(dt=-0.5*dt)
    t0 = time.time()
    for it in range(it_num):
        ptcl_beam.push(dt)
        if collisions:
            #collision_obj.vel_update()
            pass
        ptcl_beam.E_interp()
        ptcl_beam.B_interp()
        obj_traj.track_traj()
    print time.time() - t0
    #-----------------------------------------------------------------------
    #---------------------------Visualize_Beam------------------------------
    x, y, z = obj_traj.get_traj()
    plot_traj(z, x, alpha=0.3, xlabel='x, meter', ylabel='y, meter', 
          savefig=False)
    #-----------------------------------------------------------------------
    
import cProfile
    
if __name__ == '__main__':
    simulation(Ntot=999, init_pos=[0.3, 0., -0.5],
          energy_range=(1*e, 20*e), theta_range=(0, pi/6),
          charge=e, it_num=120, dt=1e-6, seed=20)
