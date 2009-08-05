from pylab import *
#Need optparse
#mport Real_Time_Python
import SLFR_RTP
reload(SLFR_RTP)
import controls


#batch of steps with multiple kp's and multiple amp's (or a list of 1
#if you prefer).  n steps per set

amplist = [50, 100, 150]

stopn = 500
N = 3

mytest = SLFR_RTP.OL_Test()

base = 'ol_step_response_amp=%s_test_%s'

for amp in amplist:
    for n in range(N):
        mytest.Reset_Theta()
        mytest.Step_Response(amp=amp, stopn=stopn)#amp is the step amplitude, stopn determines how long the test runs
        mytest.Close_Serial()
        basename = base % (amp, n+1)
        mytest.Save(basename)

show()
