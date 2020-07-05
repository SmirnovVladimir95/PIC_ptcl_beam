from numpy.random import randn


def gen_normal_mass(mean, std, n_total):
    return std * randn(n_total) + mean


if __name__ == '__main__':
    from matplotlib.pyplot import hist, show, close
    m = gen_normal_mass(mean=1, std=0.3, n_total=int(1e4))
    hist(m, bins=100)
    show()
    close()
