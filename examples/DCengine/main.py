from PyControl.models import *

# model of electric DC motor
# more about modelling process in README.md inside the same directory

# parameters:
# R - engine coils resistance
# L - engine coils inductance
# Ke - electromotive constant
# Km - motor torque constant
# Il - inertia of motor load

R = 10
L = 0.5
Km = 0.01
Ke = 0.01
Il = 0.1

A = [[0, Km/Il],
     [-Ke/L, -R/L]]

B = [0, 1/L]
C = [1, 0]

system = ss(A, B, C, [0])   # you can omit D array, for real systems PyControl defaults D=[0]

phasePortrait(system)       # it's also possible to describe variables being plot passing
                            # indexes to attributes var1 and var2
                            # you can also pass vector to Xinit attribute with
                            # initial states


