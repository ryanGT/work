'''
This file will fit some bode data.
I dont know if I care right now I just want to test git.
'''

from pylab import *
from scipy import *
from scipy import optimize

import pylab_util

import os
import controls
reload(controls)
import txt_data_processing
reload(txt_data_processing)

import rwkbode
reload(rwkbode)

from IPython.Debugger import Pdb
#from txt_data_processing import load_avebode_data_set, \
#     load_time_domain_data_set, merge_trunc_ave_data_sets

data_dir = 'June_17_2009'
import sys
if data_dir not in sys.path:
    sys.path.append(data_dir)

log_ds_name = 'log_compressed_data_June_17_2009'
log_data_set = txt_data_processing.load_avebode_data_set(log_ds_name)

ol_act_bode = log_data_set.find_bode('theta','v')
ol_act_bode.phase = squeeze(ol_act_bode.phase)
ol_act_bode.mag = squeeze(ol_act_bode.mag)
f = log_data_set.f

raw_name = 'closed_loop_swept_sine_no_accel_fb_avebodes'
raw_data_set = txt_data_processing.load_avebode_data_set(raw_name)
raw_act_bode = raw_data_set.find_bode('theta','v')
raw_cl_bode = raw_data_set.find_bode('theta','u')
raw_a_theta_d_bode = raw_data_set.find_bode('a','u')
f_raw = raw_data_set.f

def my_ol_model(X):
    g = X[0]
    zero = X[1]
    zeta_z = X[2]
    pole = X[3]
    zeta_p = X[4]
    tau = X[5]
    num = g*tau*pole**2*poly1d([1, 2*zeta_z*zero, zero**2])
    den = poly1d([1, 2*zeta_p*pole, pole**2, 0])*(zero**2)
    fo_term = poly1d([1, tau])
    den2 = den*fo_term
    TF = controls.TransferFunction(num, den2)
    return TF

def bad_ol_model(X):
    g = X[0]
    tau = X[1]
    num = g*tau
    den = poly1d([1, tau, 0])
    TF = controls.TransferFunction(num, den)
    return TF

def _build_fit_bode(X):
    TF = my_ol_model(X)
    bode = rwkbode.Bode_From_TF(TF, f, input='v', output='theta')
    return bode

def phase_error(X):
    bode = _build_fit_bode(X)
    phase_evect = (bode.phase-ol_act_bode.phase)**2
    return phase_evect

def my_cost(X):
    TF = my_ol_model(X)
    bode = rwkbode.Bode_From_TF(TF, f, input='v', output='theta')
    dB_evect = (bode.dBmag()-ol_act_bode.dBmag())**2
    dB_cost = dB_evect.sum()
    phase_evect = (bode.phase-ol_act_bode.phase)**2
    phase_cost = phase_evect.sum()
    return dB_cost+0.1*phase_cost

g = 10.0
zero = 2.3*2*pi
zeta_z = 0.05
pole = 3.5*2*pi
zeta_p = 0.25
tau = 1.5*2*pi

f2 = logspace(-1, 2, 500)
Xinit = [g, zero, zeta_z, pole, zeta_p, tau]
#Xinit = array([ 11.51421791,  15.64938367,   0.02199073,  19.95702445,
#         0.36492724,  21.87454853])

oltf = my_ol_model(Xinit)
oltf_bode = rwkbode.Bode_From_TF(oltf, f2, input='v', output='theta')

badtf = bad_ol_model([g, tau])
bad_bode = rwkbode.Bode_From_TF(badtf, f2, input='v', output='theta')


rerun = 0
if rerun:
    Xfit = optimize.fmin(my_cost, Xinit)
else:
    Xfit = array([ 11.49441915,  15.5654225 ,   0.02112513,  19.31316775,
         0.33893801,  20.98121053])

fit_tf = my_ol_model(Xfit)
fit_bode = rwkbode.Bode_From_TF(fit_tf, f2, input='v', output='theta')
                     
freqlim = [0.1, 30]

act_fignum = 10

rwkbode.GenBodePlot(act_fignum, f_raw, raw_act_bode)
rwkbode.GenBodePlot(act_fignum, f, ol_act_bode, linetype='o', clear=False)
rwkbode.GenBodePlot(act_fignum, f2, oltf_bode, clear=False)
#rwkbode.GenBodePlot(act_fignum, f2, bad_bode, clear=False)
rwkbode.GenBodePlot(act_fignum, f2, fit_tf, linetype='k-', clear=False)

pylab_util.SetAllXlims(act_fignum, freqlim)
pylab_util.SetPhaseLim(act_fignum, [-200, 10])

#Theta Feedback Verification
cltf = controls.feedback(fit_tf*1.0)
cltf_bode = rwkbode.Bode_From_TF(cltf, f2, input='u', output='theta')


cl_fignum = 11
rwkbode.GenBodePlot(cl_fignum, f_raw, raw_cl_bode)
rwkbode.GenBodePlot(cl_fignum, f2, cltf_bode, linetype='k-', clear=False)
pylab_util.SetAllXlims(cl_fignum, freqlim)
pylab_util.SetMagLim(cl_fignum, [-40, 10])
pylab_util.SetPhaseLim(cl_fignum, [-200, 10])


#accel/theta system ID
def a_theta_tf(X):
    g = X[0]
    wn = X[1]
    z = X[2]
    den = [1, 2*wn*z, wn**2]
    num = [g*wn**2,0,0]
    TF = controls.TransferFunction(num,den)
    return TF

def _build_a_theta_fit_bode(X, f_in=f):
    TF = a_theta_tf(X)
    bode = rwkbode.Bode_From_TF(TF, f_in, input='theta', output='a')
    return bode

def my_a_theta_cost(X):
    bode = _build_a_theta_fit_bode(X)
    dB_evect = (bode.dBmag()-a_theta_fit_bode.dBmag())**2
    dB_cost = dB_evect.sum()
    phase_evect = (bode.phase-a_theta_fit_bode.phase)**2
    phase_cost = phase_evect.sum()
    return dB_cost+0.1*phase_cost

a_theta_fit_bode = log_data_set.find_bode('a','theta')
a_theta_fit_bode.phase = squeeze(a_theta_fit_bode.phase)
a_theta_fit_bode.mag = squeeze(a_theta_fit_bode.mag)

a_theta_fignum = 12
a_theta_bode =  raw_data_set.find_bode('a','theta')
rwkbode.GenBodePlot(a_theta_fignum, f_raw, a_theta_bode)
Xa_ig = [0.35e-2, 2.5*2*pi, 0.02]
ig_a_theta_bode = _build_a_theta_fit_bode(Xa_ig, f_in=f_raw)
rerun_theta_a = 0
if rerun_theta_a:
    Xa_fit = optimize.fmin(my_a_theta_cost, Xa_ig)
else:
    Xa_fit = array([  3.43130384e-03,   1.56045083e+01,   1.99006751e-02])
a_theta_bode_fit_res = _build_a_theta_fit_bode(Xa_fit, f_in=f_raw)
a_theta_fit_TF = a_theta_tf(Xa_fit)
rwkbode.GenBodePlot(a_theta_fignum, f, a_theta_fit_bode, \
                    linetype='go', clear=False)
#rwkbode.GenBodePlot(a_theta_fignum, f_raw, ig_a_theta_bode, \
#                    linetype='g-', clear=False)
rwkbode.GenBodePlot(a_theta_fignum, f_raw, a_theta_bode_fit_res, \
                    linetype='k-', clear=False)
pylab_util.SetAllXlims(a_theta_fignum, freqlim)
pylab_util.SetMagLim(a_theta_fignum, [-20, 30])
pylab_util.SetPhaseLim(a_theta_fignum, [-10, 200])

#a/theta_d Verification
a_theta_d_TF = cltf*a_theta_fit_TF
a_theta_d_bode = rwkbode.Bode_From_TF(a_theta_d_TF, f_raw, \
                                      input='theta_d', output='a')
a_theta_d_fignum = 13
rwkbode.GenBodePlot(a_theta_d_fignum, f_raw, raw_a_theta_d_bode)
rwkbode.GenBodePlot(a_theta_d_fignum, f_raw, a_theta_d_bode, \
                    linetype='k-', clear=False)
pylab_util.SetAllXlims(a_theta_d_fignum, freqlim)
pylab_util.SetMagLim(a_theta_d_fignum, [-30, 20])
pylab_util.SetPhaseLim(a_theta_d_fignum, [-200, 200])



#Time Domain Verification
#td_ds_name = 'closed_loop_swept_sine_no_accel_fb_time_domain'
#time_domain_data_set = txt_data_processing.load_time_domain_data_set(td_ds_name)
step_name = 'step_response_no_sat_test_1_SLFR_RTP_P_control_kp=1.0_uend=50.txt'
step_path = os.path.join(data_dir, step_name)
step_td = txt_data_processing.Data_File(step_path)
step_fignum = 20
step_td.Time_Plot(fignum=step_fignum)
t = step_td.t
u = step_td.u
a = step_td.a
theta_step_cl_model = cltf.lsim(u, t)
figure(step_fignum)
plot(t, theta_step_cl_model)

a_step_cl_model = a_theta_fit_TF.lsim(theta_step_cl_model, t)
plot(t, a_step_cl_model)
#filter accel exp signal
from scipy import signal
B, A = signal.filter_design.butter(2, 50.0/250)#f_c/f_Nyquist
a_filt = signal.lfilter(B, A, a, axis=-1)

figure(100)
plot(t,a)
plot(t,a_filt, label='$a_{filtered}$')
plot(t,a_step_cl_model, label='$a_{model}$')

show()
