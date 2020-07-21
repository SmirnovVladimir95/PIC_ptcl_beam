"""
This file determines class with particle data
"""
from numpy import ndarray, array, zeros_like
from MotionIntegration import ParticlePush, UpdateVelocity


class Particle(object):
    def __init__(self, mass, charge, pos, vel, name='default_name', electric_field=None, magnetic_field=None,
                 electric_field_interp_func=None, magnetic_field_interp_func=None):
        assert isinstance(pos, ndarray)
        assert pos.shape[0] == 3
        assert isinstance(vel, ndarray)
        assert vel.shape[0] == 3
        assert pos.shape == vel.shape
        assert mass.shape == charge.shape
        assert pos.shape[1] == mass.shape[0] == charge.shape[0]

        self.mass = mass
        self.charge = charge
        self.position = pos
        self.velocity = vel
        self.name = name
        self.n_total = len(mass)
        self.dim = pos.shape[0]

        self.ef_interp_func = electric_field_interp_func
        if self.ef_interp_func is not None:
            self.electric_field = electric_field_interp_func(pos)
        elif electric_field is not None:
            self.electric_field = electric_field
        else:
            self.electric_field = zeros_like(pos)

        self.mf_interp_func = magnetic_field_interp_func
        if self.mf_interp_func is not None:
            self.magnetic_field = magnetic_field_interp_func(pos)
        elif magnetic_field is not None:
            self.magnetic_field = magnetic_field
        else:
            self.magnetic_field = zeros_like(pos)

        assert self.electric_field.shape == self.magnetic_field.shape == self.position.shape

    def push(self, dt):
        ParticlePush(pos_x=self.position[0],
                     pos_y=self.position[1],
                     pos_z=self.position[2],
                     vel_x=self.velocity[0],
                     vel_y=self.velocity[1],
                     vel_z=self.velocity[2],
                     Ex=self.electric_field[0],
                     Ey=self.electric_field[1],
                     Ez=self.electric_field[2],
                     Bx=self.magnetic_field[0],
                     By=self.magnetic_field[1],
                     Bz=self.magnetic_field[2],
                     dt=dt,
                     q=self.charge,
                     m=self.mass,
                     Ntot=self.n_total,
                     )

    def vel_push(self, dt):
        UpdateVelocity(vel_x=self.velocity[0],
                       vel_y=self.velocity[1],
                       vel_z=self.velocity[2],
                       Ex=self.electric_field[0],
                       Ey=self.electric_field[1],
                       Ez=self.electric_field[2],
                       Bx=self.magnetic_field[0],
                       By=self.magnetic_field[1],
                       Bz=self.magnetic_field[2],
                       dt=dt,
                       q=self.charge,
                       m=self.mass,
                       Ntot=self.n_total,
                       )

    def electric_field_interp(self):
        if self.ef_interp_func is not None:
            self.electric_field[:] = self.ef_interp_func(self.position)
        else:
            print "Warning: No interpolation function is specified for electric field"

    def magnetic_field_interp(self):
        if self.mf_interp_func is not None:
            self.magnetic_field[:] = self.mf_interp_func(self.position)
            #self.mf_interp_func(self.position, self.magnetic_field)
        else:
            print "Warning: No interpolation function is specified for magnetic field"

    def get_position(self, idx=None):
        if idx is not None:
            return self.position[:, idx].copy()
        return self.position.copy()

    def get_velocity(self, idx=None):
        if idx is not None:
            return self.velocity[:, idx].copy()
        return self.velocity.copy()

    def set_velocity(self, new_velocity, idx=None):
        if idx is not None:
            self.velocity[:, idx] = new_velocity
        self.velocity = new_velocity

if __name__ == '__main__':
    electron = Particle(mass=array([1, 1]),
                        charge=array([1, 1]),
                        pos=array([[1, 2], [1, 2], [1, 2]]),
                        vel=array([[1, 2], [1, 2], [1, 2]]),
                        name='default_name',
                        electric_field=None,
                        magnetic_field=None,
                        electric_field_interp_func=None,
                        magnetic_field_interp_func=None)
    pos = electron.get_position(1)
    vel = electron.get_velocity(0)
    electron.set_velocity([1, 20, 1], 0)
    print 'pos before get():', pos
    pos[0] += 1
    print 'pos after get():', electron.get_position(1)
    print electron.get_velocity(0)
    print pos
