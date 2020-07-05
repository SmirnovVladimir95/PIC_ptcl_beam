from Collisions.NeutralGas import NeutralGas


class IonizedGas(NeutralGas):
    def __init__(self, T, n, mass, coullog, name=None):
        super(IonizedGas, self).__init__(T, n, mass, name)
        self.coullog = coullog


if __name__ == '__main__':
    ions = IonizedGas(T=300., n=1e13, mass=6.6335209E-26, coullog=1, name='Ar')
    print ions.gen_vel_vector(), ions.gen_vel_vector()
