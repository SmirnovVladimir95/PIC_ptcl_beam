from numpy.random import uniform
from scipy.constants import pi
from numpy import cos, sin, array


def gen_positions(pos, sub_width, n_total):
    phi = uniform(0, 2 * pi, size=n_total)
    r = uniform(0, 0.5 * sub_width, size=n_total)
    init_x = pos[0] + r * cos(phi)
    init_y = pos[1] + r * sin(phi)
    return array([init_x, init_y, [pos[2]] * n_total])


if __name__ == '__main__':
    from matplotlib.pyplot import scatter, show, figure, close
    positions = gen_positions(pos=(0, 0, 0), sub_width=0.1, n_total=int(1e4))
    figure(figsize=(5, 5))
    scatter(positions[0], positions[1])
    show()
    close()
    scatter(positions[0], positions[2])
    show()