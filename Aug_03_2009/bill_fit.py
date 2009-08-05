from scipy import *
import systemid
reload(systemid)
from systemid import *
from pylab import savefig
import txt_data_processing

#frfn = 'swept_sine_no_sat_amp=50_stopn=20000_test_1_SLFR_RTP_P_control_kp=1.0.txt'
#self.f,self.dbM,self.phase
#usecols = (0,2,3)

#freq_data = frequency_data_file_in_db_w_phase(frfn)
#freq_data.read(usecols,skiprows=1)
log_ds_mod = 'swept_sine_amp_50_Aug_03_2009_log_downsampled'
ave_data_set = txt_data_processing.load_avebode_data_set(log_ds_mod)
theta_v_bode = ave_data_set.avebodes[0]
f = ave_data_set.f
freq_data = frequency_data_from_rwkbode(f, theta_v_bode)

num = 'g*p'
den = 's*(s+p)'
ig_dict = {'g':10.0,'p':10.0*2*pi}
model = Model(num, den, ig_dict)

model.calc_freq_data(freq_data.f)

opt_dict = fit_freq(model,freq_data)
opt_model = model.copy(var_dict=opt_dict)
opt_model.calc_freq_data(freq_data.f)

freq_data.plot_bode(label='exp',clear=True)
model.plot_bode(label='initial guess',clear=False)
opt_model.plot_bode(label='optimized',clear=False)

#savefig('2dof_plot')

sdfn = 'ol_step_response_amp=50_test_1_SLFR_RTP_OL_Test_uend=50.txt'
usecols = (0,3,4)
step_data = data.time_data_file(sdfn)
step_data.read(usecols,skiprows=2)

step_data.plot_output(fignum=2,label='Exp.')
opt_model.plot_resp(step_data.t,step_data.input,fignum=2,\
                    clear=False,label='Opt. Model')
time_opt_dict = fit_time(model, step_data)

#savefig('2dof_step_plot')

show()

