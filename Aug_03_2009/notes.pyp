s: Overview

This testing was done with the beam of the SLFR completely removed.  I
am trying to first design a PID controller for the motor by itself,
ignoring saturation and the effects of the flexible beam and then see
what happens as I add in each complication one at a time.

My concern is that if I don't have an integral term, I won't have
overshoot problems with saturation and then I won't need my input
shaping idea.  So, I hope to develop a PI controller to help with
small steps and steady-state errors.  I will then combine that design
with a PD controller for the fast response.


s: Short Term Plan

My short term plan is to fit the data for the motor by itself and then
design a PI controller for it.


s: Switching Mode Controller

It seems like this problem is ripe for a switching mode controller or
some other intelligent approach.  If the error is large, use a
high-gain P or PD to get near the desired stopping point quickly.
This controller could probably saturate the motor without too much
trouble except possibly messing up any vibration suppression.  Once
the controller is near the desired stopping point, switch to the PI
controller or whatever approach is best for eliminating small
steady-state errors due to friction.  Vibration suppression could
possibly even be swithced off until the system is near the final
desired stopping position.