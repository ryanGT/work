from pylab import *
#Need optparse
#mport Real_Time_Python
import SLFR_RTP
reload(SLFR_RTP)
import controls


#batch of steps with multiple kp's and multiple amp's (or a list of 1
#if you prefer).  n steps per set
kp = 1.0
kplist = [1.0]
amplist = [50, 100, 150]

stopn = 2000
N = 3

mytest = SLFR_RTP.P_control_Test(kp)

base = 'step_response_no_sat_test_%s'

for cur_kp in kplist:
    mytest.kp = cur_kp
    for amp in amplist:
        for n in range(N):
            mytest.Reset_Theta()
            mytest.Step_Response(amp=amp, stopn=stopn)#amp is the step amplitude, stopn determines how long the test runs
            mytest.Close_Serial()
            basename = base % (n+1)
            mytest.Save(basename)
            mytest.Step_Response(amp=0, stopn=stopn)

show()
