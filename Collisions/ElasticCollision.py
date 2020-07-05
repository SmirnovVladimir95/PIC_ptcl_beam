from numpy.random import random

from numpy import zeros_like, sqrt, zeros


def elastic_collision(ptcl_beam, n_total, dt, gas, g_sigma):
    vel = ptcl_beam.get_velocity()
    vel_norm = zeros_like(vel[0])
    for v in vel:
        vel_norm += v ** 2
    vel_norm = sqrt(vel_norm)
    g_sigma_interp = zeros_like(vel_norm)
    idx_1 = 0
    idx_2 = 0

    for m, interp in g_sigma:
        idx_2 += ptcl_beam.mass[ptcl_beam.mass == m].shape[0]
        g_sigma_interp[idx_1:idx_2] = interp(vel_norm[idx_1:idx_2])
        idx_1 = idx_2

    for i in xrange(n_total):
        prob = g_sigma_interp[i] * gas.n * dt
        if prob >= random():
            gas_vel = gas.gen_vel_vector()
            new_vel = (ptcl_beam.get_velocity(i) * ptcl_beam.mass[i] + gas_vel * gas.mass +
                       gas.mass * (gas_vel - ptcl_beam.get_velocity(i))) / (ptcl_beam.mass[i] + gas.mass)
            ptcl_beam.set_velocity(new_velocity=new_vel, idx=i)

        if prob > 0.01:
            print('Warning, probability > 0.01: ', prob)
