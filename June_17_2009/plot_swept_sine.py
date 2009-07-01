from pylab import *
from scipy import *

import txt_data_processing

DS = txt_data_processing.Data_Set('swept_sine_no_sat_amp=75_stopn=10000_test_*.txt')
DS.Overlay_Time_Plots(labels=['u'], \
                      fignum=1)
DS.Overlay_Time_Plots(labels=['v'], \
                      fignum=2)
DS.Overlay_Time_Plots(labels=['theta'], \
                      fignum=3)


u = DS.u[:,0]
t = DS.t

import controls
from controls import TransferFunction

T = 0.5
fd = 1.0/T
w = fd*2*pi
z = 0.25
fz = 3.0
wz = 2*pi*fz
zz = 0.2
p = 2.0*pi*1.5
pso = poly1d(wz**2*array([1, 2*z*w, w**2]))
pfo = poly1d([1, p])
den = pso*pfo
TF = controls.TransferFunction(p*w**2*array([1, 2*zz*wz, wz**2]), \
                               den)
                               

def simple_model(X):
    wn = X[0]
    z = X[1]
    TF = TransferFunction(wn**2, [1, 2*z*wn, wn**2])
    return TF


y_exp = DS.theta[:,0]

y_sim = TF.lsim(u,t)

figure(3)
plot(t, y_sim, label='simple model')
legend()

show()
