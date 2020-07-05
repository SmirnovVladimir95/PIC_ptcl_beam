from pandas import read_excel, to_numeric
from numpy import zeros_like


def compute_efr(r, phi):
    efr = zeros_like(r)
    dr2 = r[2:] - r[:-2]
    # central difference, not right on walls
    efr[1:-1] = (phi[:-2] - phi[2:]) / dr2
    # one sided difference on boundaries
    efr[0] = (phi[0] - phi[1]) / (r[1] - r[0])
    efr[-1] = (phi[-2] - phi[-1]) / (r[-1] - r[-2])
    return r, efr


def load_radial_electric_field(filepath):
    data = read_excel(filepath, index_col=0)
    data.astype(float)
    r, efr = compute_efr(data.r.values, data.phi.values)
    return r, efr
