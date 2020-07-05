from numpy.random import random_sample
from numpy import sin, cos, array, zeros
from scipy.constants import pi


def gen_velocity(vel_module, phi, theta):
    theta_rand = (theta[1] - theta[0]) * random_sample() + theta[0]
    phi_rand = (phi[1] - phi[0]) * random_sample() + phi[0]
    vel_x = vel_module * sin(theta_rand) * cos(phi_rand)
    vel_y = vel_module * sin(theta_rand) * sin(phi_rand)
    vel_z = vel_module * cos(theta_rand)
    return array([vel_x, vel_y, vel_z])


def gen_velocities(energy_range, mass, theta, phi=(0, 2*pi)):
    n_total = len(mass)
    energy = energy_range[0] + random_sample(n_total) * (energy_range[1] - energy_range[0])
    vel_module = (2 * energy / mass) ** 0.5
    vel = zeros((3, n_total))
    for i in range(n_total):
        vel[:, i] = gen_velocity(vel_module[i], phi, theta)
    return vel


if __name__ == '__main__':
    from numpy import ones
    from scipy.constants import pi
    from matplotlib.pyplot import hist, show, close
    n_total = int(1e4)
    velocity = gen_velocities(energy_range=(0, 10),
                              mass=ones(n_total),
                              theta=(0, pi/6),
                              )
    hist(velocity[0]**2+velocity[1]**2+velocity[2]**2, bins=100)
    show()
    close()
