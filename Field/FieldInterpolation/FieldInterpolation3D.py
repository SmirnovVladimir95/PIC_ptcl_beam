from scipy.interpolate import RegularGridInterpolator
from numpy import array
from Interpolation.RegularGridInterpolator3D import RegularGridInterpolator3D


class FieldInterpolation3D(object):
    def __init__(self, grid, field, kind='linear'):
        assert grid[0].shape[0] == field.shape[1]
        assert grid[1].shape[0] == field.shape[2]
        assert grid[2].shape[0] == field.shape[3]
        '''
        self._interp_func = (RegularGridInterpolator(grid, field[0]),
                             RegularGridInterpolator(grid, field[1]),
                             RegularGridInterpolator(grid, field[2]))
        '''
        self._interp_func = (RegularGridInterpolator3D(grid, field[0]),
                             RegularGridInterpolator3D(grid, field[1]),
                             RegularGridInterpolator3D(grid, field[2]))

    def interp_func(self, position, field=None):
        if field is None:
            field_x = self._interp_func[0](position.T)
            field_y = self._interp_func[1](position.T)
            field_z = self._interp_func[2](position.T)
            return array([field_x, field_y, field_z])
        else:
            field[0, :] = self._interp_func[0](position.T)
            field[1, :] = self._interp_func[1](position.T)
            field[2, :] = self._interp_func[2](position.T)
