"""
This file containes tool to track ptcls
"""
import numpy as np


class TrackTraj:
    def __init__(self, ptcl, ptcl_idx=None):
        """
        ptcl: ptcl object
            object of ptcl class
        ptcl_idx: int
            index of ptcl
        """
        self.ptcl = ptcl
        self.ptcl_idx = ptcl_idx or np.arange(ptcl.Ntot)
        self.traj_x = []
        self.traj_y = []
        self.traj_z = []
        for _ in range(len(self.ptcl_idx)):
            self.traj_x.append([])
            self.traj_y.append([])
            self.traj_z.append([])

    def track_traj(self):
        """
        method track ptcls
        """
        x = self.ptcl.get_pos()[0][self.ptcl_idx]
        y = self.ptcl.get_pos()[1][self.ptcl_idx]
        z = self.ptcl.get_pos()[2][self.ptcl_idx]
        for idx in range(x.shape[0]):
            self.traj_x[idx].append(x[idx])
            self.traj_y[idx].append(y[idx])
            self.traj_z[idx].append(z[idx])

    def get_traj(self):
        return self.traj_x, self.traj_y, self.traj_z

    def save_traj(self, filename):
        np.save(filename+'_x', self.traj_x)
        np.save(filename+'_y', self.traj_y)
        np.save(filename+'_z', self.traj_z)