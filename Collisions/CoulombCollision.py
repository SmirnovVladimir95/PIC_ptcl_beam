from numpy.random import random

from numpy import sqrt, linalg
from scipy.constants import pi, e, epsilon_0
import math
import numba


#@numba.njit(cache=True)
def coulomb_collision(ptcl_beam, n_total, dt, gas, it):
    for i in xrange(n_total):
         gas_vel=gas.gen_vel_vector()
         #print(linalg.norm(gas_vel))
         Vt=ptcl_beam.get_velocity(i)-gas_vel
         vel_norm=linalg.norm(Vt)     
         srhi=(e)**4/(2*pi*(epsilon_0)**2)*gas.n*gas.ion*dt*gas.coullog/(gas.mass*ptcl_beam.mass[i]/(gas.mass+ptcl_beam.mass[i]))**2/vel_norm**3
#         if (srhi>0.1):
#             print(it)
#             print(srhi)
#             print(linalg.norm(Vt))
#             print(gas.mass*ptcl_beam.mass[i]/(gas.mass+ptcl_beam.mass[i]))
        # if (i==5):
        #     mmmm=linalg.norm(ptcl_beam.get_velocity(i))
         phi=random()*2*pi
         hi=sqrt(-2*srhi*math.log(random()))             
         dVx=Vt[0]/sqrt(Vt[0]**2+Vt[1]**2)*Vt[2]*math.sin(hi)*math.cos(phi)-Vt[1]/sqrt(Vt[0]**2+Vt[1]**2)*linalg.norm(Vt)*math.sin(hi)*math.sin(phi)-Vt[0]*(1-math.cos(hi))
         dVy=Vt[1]/sqrt(Vt[0]**2+Vt[1]**2)*Vt[2]*math.sin(hi)*math.cos(phi)+Vt[0]/sqrt(Vt[0]**2+Vt[1]**2)*linalg.norm(Vt)*math.sin(hi)*math.sin(phi)-Vt[1]*(1-math.cos(hi))
         dVz=-sqrt(Vt[0]**2+Vt[1]**2)*math.sin(hi)*math.cos(phi)-Vt[2]*(1-math.cos(hi))       
         Vt[0]=dVx
         Vt[1]=dVy
         Vt[2]=dVz
         new_vel=ptcl_beam.get_velocity(i)+gas.mass/(gas.mass+ptcl_beam.mass[i])*Vt
         ptcl_beam.set_velocity(new_velocity=new_vel, idx=i)
         #if (i==5):
         #    print(linalg.norm(ptcl_beam.get_velocity(i))-mmmm)
         #    print()
