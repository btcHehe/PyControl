from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

_x = np.array([])
_y = np.array([])
_xmin = _xmax = _ymin = _ymax = 0
_xlabel = ""
_ylabel = ""
_title = ""
_fastMode = False
_sampleRate = 0


def __init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    gluOrtho2D(_xmin, _xmax, 2 * _ymin, 2 * _ymax)


def __plotting():
    global _title
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(400, 400)
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
    global _fastMode
    global _sampleRate
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)

    # making plot axis
    glBegin(GL_LINES)
    glVertex2f(_xmin, 0.0)  # x axis
    glVertex2f(_xmax, 0.0)
    glVertex2f(0.0, 2 * _ymax)  # y axis
    glVertex2f(0.0, 2 * _ymin)

    glVertex2f(0.0, 2 * _ymax)  # y axis arrow
    glVertex2f(0.0 - _xmax / 40, 2 * (_ymax - _ymax / 30))
    glVertex2f(0.0, 2 * _ymax)
    glVertex2f(0.0 + _xmax / 40, 2 * (_ymax - _ymax / 30))

    glVertex2f(_xmax, 0.0)  # x axis arrow
    glVertex2f(_xmax - _xmax / 30, 0.0 + _ymax / 30)
    glVertex2f(_xmax, 0.0)
    glVertex2f(_xmax - _xmax / 30, 0.0 - _ymax / 30)

    glEnd()
    glFlush()

    glColor3f(0.0, 0.0, 1.0)
    if _fastMode:
        j = 0
        while j < np.size(_x):
            glBegin(GL_POINTS)
            glVertex2f(_x[j], _y[j])
            glEnd()
            glFlush()
            j += _sampleRate  # skip size
    else:
        for j in range(np.size(_x) - 1):
            glBegin(GL_LINES)
            glVertex2f(_x[j], _y[j])
            glVertex2f(_x[j + 1], _y[j + 1])
            glEnd()
            glFlush()


def plot(x, y, xlabel="x", ylabel="y", title="plot of y(x)", fastMode=False, sampleRate=0):
    global _x
    global _y
    global _xmin
    global _xmax
    global _ymin
    global _ymax
    global _xlabel
    global _ylabel
    global _title
    global _fastMode
    global _sampleRate
    _x = np.copy(x)
    _y = np.copy(y)
    _xmin = np.amin(_x)
    _xmax = np.amax(_x)
    _ymin = np.amin(_y)
    _ymax = np.amax(_y)
    _xlabel = xlabel
    _ylabel = ylabel
    _title = title
    _fastMode = fastMode
    if sampleRate == 0 and fastMode:
        raise Exception("you've chosen fastMode so you need to specify sampling rate with sampleRate argument")
    else:
        _sampleRate = sampleRate
    __plotting()


def plotMore(xvect, yvect, xlabelvect=None, ylabelvect=None,
             title="multiple plots"):  # TODO  plot multiple functions at one plane
    if ylabelvect is None:
        ylabelvect = []
    if xlabelvect is None:
        xlabelvect = []
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
        for i in range(np.size(xvect) - np.size(xlabelvect)):
            np.append(xlabelvect, f'x{i + 1}')
    if np.size(ylabelvect) < np.size(yvect):
        for j in range(np.size(yvect) - np.size(ylabelvect)):
            np.append(ylabelvect, f'y{j + 1}')
