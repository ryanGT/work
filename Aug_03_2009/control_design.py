from pylab import *
from scipy import *
import controls

opt_dict = {'g': 14.357956593401092, 'p': 28.981055660081886}

g = opt_dict['g']
p = opt_dict['p']

k_vect = arange(1, 5.5, 1)

Gp = controls.TransferFunction(g*p,[1,p,0])

t = arange(0,0.5,0.002)

figure(10)
clf()

for k in k_vect:
    cltf = controls.feedback(Gp*k)
    cltf.step_response(t=t, amp=50, fignum=10, clear=False)

show()
