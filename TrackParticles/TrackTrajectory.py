"""
This file containes tool to track ptcls
"""
import numpy as np


class TrackTraj(object):
    def __init__(self, ptcl, ptcl_idx=None, track_vel=False):
        """
        ptcl: ptcl object
            object of ptcl class
        ptcl_idx: int
            index of ptcl
        """
        self.ptcl = ptcl
        self.ptcl_idx = ptcl_idx or np.arange(ptcl.n_total)
        self.traj_x = []
        self.traj_y = []
        self.traj_z = []
        self.track_vel = track_vel
        self.traj_vx = [] if self.track_vel else None
        self.traj_vy = [] if self.track_vel else None
        self.traj_vz = [] if self.track_vel else None
        for _ in range(len(self.ptcl_idx)):
            self.traj_x.append([])
            self.traj_y.append([])
            self.traj_z.append([])
            if self.track_vel:
                self.traj_vx.append([])
                self.traj_vy.append([])
                self.traj_vz.append([])

    def track_traj(self):
        """
        method track ptcls
        """
        x = self.ptcl.get_position()[0][self.ptcl_idx]
        y = self.ptcl.get_position()[1][self.ptcl_idx]
        z = self.ptcl.get_position()[2][self.ptcl_idx]
        vx = self.ptcl.get_velocity()[0][self.ptcl_idx] if self.track_vel else None
        vy = self.ptcl.get_velocity()[1][self.ptcl_idx] if self.track_vel else None
        vz = self.ptcl.get_velocity()[2][self.ptcl_idx] if self.track_vel else None
        for idx in range(x.shape[0]):
            self.traj_x[idx].append(x[idx])
            self.traj_y[idx].append(y[idx])
            self.traj_z[idx].append(z[idx])
            if self.track_vel:
                self.traj_vx[idx].append(vx[idx])
                self.traj_vy[idx].append(vy[idx])
                self.traj_vz[idx].append(vz[idx])

    def get_traj(self):
        return self.traj_x, self.traj_y, self.traj_z

    def get_traj_numpy(self):
        return np.array([self.traj_x, self.traj_y, self.traj_z])

    def get_vel(self):
        return self.traj_vx, self.traj_vy, self.traj_vz

    def get_vel_numpy(self):
        return np.array([self.traj_vx, self.traj_vy, self.traj_vz])

    def save_traj(self, filename):
        np.save(filename, np.array([self.traj_x, self.traj_y, self.traj_z]))

    def savetxt_traj(self, filename):
        np.savetxt(filename, np.array([self.traj_x, self.traj_y, self.traj_z]))

    def save_vel(self, filename):
        np.save(filename, np.array([self.traj_vx, self.traj_vy, self.traj_vz]))

    def savetxt_vel(self, filename):
        np.savetxt(filename, np.array([self.traj_vx, self.traj_vy, self.traj_vz]))


def save_txt(x, y, z, filename):
    with open(filename, 'w') as f:
        f.write('x y z\n')
        for it in range(len(x)):
            f.write(str(x[it])+' '+str(y[it])+' '+str(z[it])+'\n')
