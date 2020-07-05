from numpy import floor
from numba import njit


@njit(cache=True)
def linear_interp_numba(x, y, z, values, interp_points, interp_values):
    dx, dy, dz = x[1] - x[0], y[1] - y[0], z[1] - z[0]
    volume = dx * dy * dz
    for i in range(len(interp_values)):
        x_i = int(floor((interp_points[i][0] - x[0]) / dx))
        y_i = int(floor((interp_points[i][1] - y[0]) / dy))
        z_i = int(floor((interp_points[i][2] - z[0]) / dz))
        interp_values[i] = (values[x_i, y_i, z_i] * (x[x_i + 1] - interp_points[i][0]) *
                            (y[y_i + 1] - interp_points[i][1]) *
                            (z[z_i + 1] - interp_points[i][2]) +
                            values[x_i, y_i, z_i + 1] * (x[x_i + 1] - interp_points[i][0]) *
                            (y[y_i + 1] - interp_points[i][1]) *
                            (interp_points[i][2] - z[z_i]) +
                            values[x_i, y_i + 1, z_i] * (x[x_i + 1] - interp_points[i][0]) *
                            (interp_points[i][1] - y[y_i]) *
                            (z[z_i + 1] - interp_points[i][2]) +
                            values[x_i, y_i + 1, z_i + 1] * (x[x_i + 1] - interp_points[i][0]) *
                            (interp_points[i][1] - y[y_i]) *
                            (interp_points[i][2] - z[z_i]) +
                            values[x_i + 1, y_i, z_i] * (interp_points[i][0] - x[x_i]) *
                            (y[y_i + 1] - interp_points[i][1]) *
                            (z[z_i + 1] - interp_points[i][2]) +
                            values[x_i + 1, y_i, z_i + 1] * (interp_points[i][0] - x[x_i]) *
                            (y[y_i + 1] - interp_points[i][1]) *
                            (interp_points[i][2] - z[z_i]) +
                            values[x_i + 1, y_i + 1, z_i] * (interp_points[i][0] - x[x_i]) *
                            (interp_points[i][1] - y[y_i]) *
                            (z[z_i + 1] - interp_points[i][2]) +
                            values[x_i + 1, y_i + 1, z_i + 1] * (interp_points[i][0] - x[x_i]) *
                            (interp_points[i][1] - y[y_i]) *
                            (interp_points[i][2] - z[z_i])) / volume
