from pylab import *
from scipy import *

import os

import txt_data_processing
#reload(txt_data_processing)

#from txt_data_processing import load_avebode_data_set, \
#     load_time_domain_data_set, merge_trunc_ave_data_sets

data_dir = '/home/ryan/siue/Research/PSoC_Research/SLFR_RTP/SRF_2009/June_17_2009'
import sys
if data_dir not in sys.path:
    sys.path.append(data_dir)

ds_name = 'closed_loop_swept_sine_no_accel_fb_avebodes'
data_set = txt_data_processing.load_avebode_data_set(ds_name)
figs = data_set.Bode_Plot2()

inds, mask, flog = data_set.Log_Compress_Data([0.5,1.5,4.0,10],[20,70,20])

data_set.Bode_Plot2(attr='compressed_avebodes', \
                    f_attr='compressed_f', figs=figs, \
                    clear=False, linetype='o')

data_set.save_as(os.path.join(data_dir, 'log_compressed_data_June_17_2009'))

show()
