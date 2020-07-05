from os.path import join
from numpy import array
from numpy import random, ones, concatenate
from scipy.constants import pi, N_A, e
import matplotlib.pyplot as plt

from Field.FieldInterpolation.FieldInterpolation3D import FieldInterpolation3D
from Field.FieldInterpolation.FieldInterpolationRadial import FieldInterpolationRadial
from Particle.Particle import Particle
from InitBeamConditions.GenerateMassDistrbution import gen_normal_mass
from InitBeamConditions.GeneratePositionDistribution import gen_positions
from InitBeamConditions.GenerateVelocityDistribution import gen_velocities
from Field.FieldLoad.ElectricFieldLoad import load_radial_electric_field
from Field.FieldLoad.MagneticFieldLoad import load_magnetic_field_3d
from TrackParticles.TrackTrajectory import TrackTraj
from Visualization.PlotBeamTrajectory import plot_traj_multy_ptcls_type


def simulation(n_total, init_pos, energy_range, vel_theta, dt, it_num, seed=None):
    random.seed(seed)
    m_235 = ones(n_total / 3) * 0.235 / N_A
    m_140 = gen_normal_mass(mean=0.140 / N_A, std=0.006 / N_A, n_total=n_total / 3)
    m_97 = gen_normal_mass(mean=0.097 / N_A, std=0.006 / N_A, n_total=n_total / 3)
    mass = concatenate((m_235, m_140, m_97))
    charge = ones(n_total) * e

    r, efr = load_radial_electric_field(join('FieldData', 'PenningPotentialApproximated.xlsx'))
    efr_interp = FieldInterpolationRadial(radial_grid=r, radial_field=efr)

    grid, mf = load_magnetic_field_3d(dirpath=join('FieldData', 'MagneticField_2_coils'))

    for i in range(mf.shape[0]):
        mf[i] *= 1.5

    mf_interp = FieldInterpolation3D(grid=grid, field=mf)

    beam = Particle(mass=mass,
                    charge=charge,
                    pos=gen_positions(pos=init_pos, sub_width=0.01, n_total=n_total),
                    vel=gen_velocities(energy_range=energy_range, mass=mass, theta=vel_theta),
                    electric_field_interp_func=efr_interp.interp_func,
                    magnetic_field_interp_func=mf_interp.interp_func,
                    )

    track_beam = TrackTraj(beam)
    from time import time
    t0 = time()
    beam.vel_push(dt=-0.5*dt)
    for it in range(it_num):
        beam.push(dt=dt)
        beam.electric_field_interp()
        beam.magnetic_field_interp()
        if it % 100 == 0:
            track_beam.track_traj()
        #print beam.magnetic_field[:, 0]
        #print beam.electric_field[:, 0]

    print 'simulation time:', time() - t0
    x, y, z = track_beam.get_traj()
    plt.figure(figsize=(5, 5))
    plt.xlim((-0.3, 0.3))
    plt.ylim((-0.3, 0.3))
    plot_traj_multy_ptcls_type(x, y, ptcl_type_num=3, colors=('blue', 'green', 'red'),
                               labels=('m = 235', '120 < m < 160', '70 < m < 120'),
                               alpha=0.3, xlabel='x, meter', ylabel='y, meter')
    plt.show()
    return track_beam


if __name__ == '__main__':
    simulation(n_total=120,
               init_pos=[0.25, 0, 0],
               energy_range=(1 * e, 20 * e),
               vel_theta=(0, pi / 6),
               it_num=10000,
               dt=1e-8,
               seed=1,
               )
