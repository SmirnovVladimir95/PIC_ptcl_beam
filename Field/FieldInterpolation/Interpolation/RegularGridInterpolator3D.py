from numpy import zeros
from LinearInterpolationNumba import linear_interp_numba


class RegularGridInterpolator3D:
    def __init__(self, points, values):
        self._x, self._y, self._z = points
        self._dx = points[0][1] - points[0][0]
        self._dy = points[1][1] - points[1][0]
        self._dz = points[2][1] - points[2][0]
        self._values = values

    def __call__(self, points, values=None):
        return self._linear_interp(points, values)

    def _linear_interp(self, interp_points, interp_values=None):
        interp_values = zeros(len(interp_points)) if interp_values is None else interp_values
        linear_interp_numba(self._x, self._y, self._z, self._values, interp_points, interp_values)
        return interp_values
