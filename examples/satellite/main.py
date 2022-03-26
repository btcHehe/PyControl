import PyControl as pc

# model of planet satellite with changing angle of its antenna
# more about modelling process in README.md

# parameters:
# I - satellite inertia
# theta - angle between antenna and planet gravitational force vector (perpendicular to planet surface)
# M - planet mass
# G - gravitational constant
# T - torque acting on satellite

A = [[0, 0],
     [1, 0]]
B = [1/I, 0]
C = [0, 1]
D = [0]

model = sys(A, B, C, D)

step(model, plot=True)
