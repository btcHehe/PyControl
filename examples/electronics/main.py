from PyControl.models import *

# model of simple electronics circuit with passive components
# more about modelling process in README.md inside the same directory

# parameters:
# R - Resistance
# L - Inductunce
# C - Capacitance

R = 10
L = 4
Cond = float(1/1000)

A = [[-R/L, -1/L],
     [1/Cond, 0]]
B = [1/L, 0]
C = [0, 1]
D = [0]

T = np.arange(0, 10, 0.0001)
system = ss(A, B, C, D)

num = [1/(L*Cond)]
den = [R/L, 1/(L*Cond)]
Gp = tf(num, den)

print('State space model: ')
print(system)
print('Transfer function model: ')
print(Gp)

step(system, plot=True, Tpts=T, solver='rk4')

