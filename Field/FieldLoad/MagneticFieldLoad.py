from numpy import load
from os.path import join


def load_magnetic_field_3d(dirpath):
    grid = load(join(dirpath, 'grid.npy'), allow_pickle=True)
    mf = load(join(dirpath, 'B.npy'))
    return grid, mf


if __name__ == '__main__':
    grid, mf = load_magnetic_field_3d('MagneticField_2_coils')

    print grid.shape
    print grid[0]
    #print grid[2]
    import matplotlib.pyplot as plt
    from numpy import arange
    print mf.shape
    plt.plot(grid[2], mf[2][46, 46, :])
    plt.show()
    plt.close()
