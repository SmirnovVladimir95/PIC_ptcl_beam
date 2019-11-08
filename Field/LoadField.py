"""
This file contains functions to load magnetic and electric field data
and preprocess it
"""
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def load_phi_data(filepath, average_step=None):
    """
    Parameters
    ----------
    filepath: str
        filepath to electric potencial data
    average_step: float
        step to smooth electric potencial data
        (used only for Penning+beam field data)
    return: tuple
        tuple[0]: 1d numpy.array
            grid for radial potencial
        tuple[1]: 1d numpy.array
            approximated radial potencial
    """
    data = pd.read_excel(filepath, header=None, 
                 names=['r', 'Phi'])
    if 'PenningPotencial.xlsx' in filepath:
        phi = data.Phi.values
        phi_side = (phi[2:12] + phi[-1:11:-1])/2.
        phi_average = np.concatenate((phi[:2], phi_side, 
                           phi_side[::-1], phi[:2][::-1]))
        r_average = np.concatenate((data.r.values, 
                         -1*data.r.values[:2][::-1]))
        phi_cubic = interp1d(r_average/100., phi_average, kind='cubic')
        r = np.arange(0, 0.46, 0.01)
        return r, phi_cubic(r)
    if 'Penning+beam.xlsx' in filepath:
        average_step = float(average_step) or 1.
        r = np.arange(0, int(data.r.iloc[-1])+average_step, 
                 average_step)
        phi = np.zeros_like(r)
        for idx, item in enumerate(r):
            phi[idx] = data[(data.r >= item) & 
                     (data.r < item + average_step)].Phi.mean()
        phi[0] = phi[1] = phi[2]
        r[1:] += average_step/2
        r /= 100.
        phi_cubic = interp1d(r, phi, kind='cubic')
        r = np.linspace(0., r[-1], 100, endpoint=True)
        return r, phi_cubic(r)
    
def load_B_data(filepath):
    """
    Parameters
    ----------
    filepath: str
        filepath to magnetic field data
    return: tuple
        tuple[0]: tuple with shape (3,)
            grid containing three 1d numpy.array 
        tuple[1]: tuple with shape (3,)
            approximated magnetic field data
    """
    B_data = np.load(filepath)
    B = (B_data[0], B_data[1], B_data[2])
    grid = (np.arange(-0.45, 0.46, 0.01),
         np.arange(-0.45, 0.46, 0.01),
         np.arange(-1., 1.01, 0.01))
    return grid, B

if __name__ == '__main__':
    r, phi = load_phi_data(filepath='Penning+beam.xlsx', average_step=1)
    plt.plot(r, phi)
    grid, B = load_B_data(filepath='B_data_full.npy')