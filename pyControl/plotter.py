from PyOpenGL.GLUT import *
from PyOpenGL.GL import *
from PyOpenGL.GLU import *
import numpy as np
import sys

_x = np.array([])
_y = np.array([])
_xmin = _xmax = _ymin = _ymax = 0
_xlabel = ""
_ylabel = ""
_title = ""

def __init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    gluOrtho2D(_xmin, _xmax, 2*_ymin, 2*_ymax)

def __plotting():
    global _title
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(400,400)
    glutInitWindowPosition(700,700)
    glutCreateWindow(_title)
    glutDisplayFunc(__plotFunc)
    __init()
    glutMainLoop()

def __plotFunc():
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(_xmin, 0.0)
    glVertex2f(_xmax, 0.0)
    glVertex2f(0.0, 2*_ymax)
    glVertex2f(0.0, 2*_ymin)
    glEnd()
    glFlush()

    for j in range(np.size(_x)-1):
        glBegin(GL_LINES)
        glVertex2f(_x[j],_y[j])
        glVertex2f(_x[j+1],_y[j+1])
        glEnd()
        glFlush()

def plot(x,y,xlabel="x",ylabel="y",title="plot of y(x)"):
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    global _xlabel
    global _ylabel
    global _title
    _x = np.copy(x)
    _y = np.copy(y)
    _xmin = np.amin(_x)
    _xmax = np.amax(_x)
    _ymin = np.amin(_y)
    _ymax = np.amax(_y)
    _xlabel = xlabel
    _ylabel = ylabel
    _title = title
    __plotting()

def plotMore(xvect,yvect,xlabelvect=[],ylabelvect=[],title="multiple plots"):   #TODO  plot multiple functions at one plane
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    global _xlabel
    global _ylabel
    global _title
    if np.size(xlabelvect) < np.size(xvect):
        for i in range(np.size(xvect)-np.size(xlabelvect)):
            np.append(xlabelvect,f'x{i+1}')
    if  np.size(ylabelvect) < np.size(yvect):
        for j in range(np.size(yvect)-np.size(ylabelvect)):
            np.append(ylabelvect,f'y{j+1}')
    



x = np.array([])
y = np.array([])

x = np.arange(-100.0, 100.0, 0.01)
for i in range(np.size(x)):
    y = np.append(y, np.sin(x[i]))

plot(x,y)
