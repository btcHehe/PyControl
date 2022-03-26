from PyControl.models import *

# model of planet satellite with changing angle of its antenna
# more about modelling process in README.md inside the same directory

# parameters:
# I - satellite inertia
# theta - angle between antenna and planet gravitational force vector (perpendicular to planet surface)
# M - planet mass
# G - gravitational constant
# T - torque acting on satellite

I = 1500    # [kg * m^2]

A = [[0, 0],
     [1, 0]]
B = [1/I, 0]
C = [0, 1]
D = [0]

model = ss(A, B, C, D)

modelTF = tf([1/I],[0,0])

print(model)
print(modelTF)

Y, T, X = pulse(model)              # you can utilize the response, time and state array
                                    # to do so just dont pass plot parameter (default plot=False)

bode(modelTF, plot=True)            # bode plots

