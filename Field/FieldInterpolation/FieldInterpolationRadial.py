from numpy import sqrt, zeros_like, array
from scipy.interpolate import interp1d


class FieldInterpolationRadial(object):
    def __init__(self, radial_grid, radial_field, kind='linear'):
        assert radial_grid.ndim == radial_field.ndim == 1
        self._interp_func = interp1d(radial_grid, radial_field, kind=kind, copy=False)

    def interp_func(self, position):
        radius = sqrt(position[0]**2 + position[1]**2)
        efr = self._interp_func(radius)
        cos_phi = position[0] / radius
        sin_phi = position[1] / radius
        return array([efr * cos_phi, efr * sin_phi, zeros_like(efr)])


if __name__ == '__main__':
    def new_func(interp_func):
        print interp_func(array([[1., 1., 1.], [2., 2., 2.]]))


    r = array([1, 2, 3])
    field_ = array([100, 30, 200])
    interp = FieldInterpolationRadial(radial_grid=r, radial_field=field_)

    print(interp.interp_func(position=array([[1], [0]])))
    new_func(interp_func=interp.interp_func)
