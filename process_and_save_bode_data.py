from pylab import *
from scipy import *

import os

import txt_data_processing
reload(txt_data_processing)

from txt_data_processing import Bode_Options, Bode_Data_Set
#import rst_creator
#reload(rst_creator)


def create_data_set(data_dir, file_pat):
    pat = os.path.join(data_dir, file_pat)
    
    bode1 = Bode_Options('v', 'theta', seedfreq=1.0, \
                         seedphase=-100., phaselim=[-200,0], \
                         maglim=[-40, 20])

    bode2 = Bode_Options('v', 'a', seedfreq=1.0, \
                         seedphase=60., phaselim=[-200,200], \
                         maglim=[-30, 30])

    bode3 = Bode_Options('u','theta', seedfreq=1.0, \
                         seedphase=-40., phaselim=[-200,10], \
                         maglim=[-30,10])
                                         
    bode4 = Bode_Options('u','a', seedfreq=1.0, \
                         seedphase=150., phaselim=[-200,200], \
                         maglim=[-50, 20])

    bode5 = Bode_Options('theta','a', seedfreq=1.0, \
                         seedphase=180., phaselim=[-200,200], \
                         maglim=[-40, 30])

    title_dict={'u':'$\\theta_d$', 'theta':'$\\theta$', \
                'a':'$\\ddot{x}_{tip}$'}

    data_set = Bode_Data_Set(pat, bode_list=[bode1, bode2, \
                                             bode3, bode4, \
                                             bode5], \
                             title_dict=title_dict)
    data_set.Calc_Bodes()
    data_set.Calc_Ave_Bodes()

    return data_set






if __name__ == '__main__':
    resave_figs=1
    report_dir='initial_system_id'

    data_dir1 = 'June_17_2009'
    file_pat1 = 'swept_sine_no_sat_amp=75_stopn=10000_test_*_SLFR_RTP_P_control_kp=1.0.txt'
    bn1 = 'closed_loop_swept_sine_no_accel_fb'
    ds1 = create_data_set(data_dir1, file_pat1)
    #ds1.Bode_Plot2()
    ds1.Truncate_and_Review(0.5, 10.0, fignum=1)
    bp1 = os.path.join(data_dir1, bn1)
    ds1.save_bodes_and_time_domain(bp1)

##     data_dir2 = 'April_14_09'
##     file_pat2 = 'swept_sine_mode2_comp_04_14_09_test*.txt'
##     bn2 = 'mid_freq_swept_sine'
##     ds2 = create_data_set(data_dir2, file_pat2)
##     ds2.Truncate_and_Review(7.1, 30.0, fignum=101)
##     bp2 = os.path.join(data_dir2, bn2)
##     ds2.save_bodes_and_time_domain(bp2)
    
    show()

