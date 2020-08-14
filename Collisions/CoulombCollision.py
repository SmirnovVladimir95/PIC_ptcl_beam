from numpy import sqrt, linalg, random, log, sin, cos, arange, any
from scipy.constants import pi, e, epsilon_0

def coulomb_collision(ptcl_beam, n_total, dt, gas, it):
    gas_vel=gas.gen_vel_vector(n_total)
    Vt=ptcl_beam.get_velocity()-gas_vel
    vel_norm=linalg.norm(Vt,axis=0)
    srhi=(e)**4/(2*pi*(epsilon_0)**2)*gas.n*dt*gas.coullog/(gas.mass*ptcl_beam.mass/(gas.mass+ptcl_beam.mass))**2/vel_norm**3  
    phi=random.rand(n_total)*2*pi  
    hi=sqrt(-2*srhi*log(random.rand(n_total)))
    dVx=Vt[0]/sqrt(Vt[0]**2+Vt[1]**2)*Vt[2]*sin(hi)*cos(phi)-Vt[1]/sqrt(Vt[0]**2+Vt[1]**2)*linalg.norm(Vt, axis=0)*sin(hi)*sin(phi)-Vt[0]*(1-cos(hi))
    dVy=Vt[1]/sqrt(Vt[0]**2+Vt[1]**2)*Vt[2]*sin(hi)*cos(phi)+Vt[0]/sqrt(Vt[0]**2+Vt[1]**2)*linalg.norm(Vt, axis=0)*sin(hi)*sin(phi)-Vt[1]*(1-cos(hi))
    dVz=-sqrt(Vt[0]**2+Vt[1]**2)*sin(hi)*cos(phi)-Vt[2]*(1-cos(hi))       
    Vt[0]=dVx
    Vt[1]=dVy
    Vt[2]=dVz
    new_vel=ptcl_beam.get_velocity()+gas.mass/(gas.mass+ptcl_beam.mass)*Vt
    ptcl_beam.set_velocity(new_velocity=new_vel)