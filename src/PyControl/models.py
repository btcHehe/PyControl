import numpy as np
import matplotlib.pyplot as plt
import PyControl.time_response as tresp
from math import log


# TODO:
# -root locus func
# -nyquist plots
# -function for model recognition
# -ss2tf
# -controlability and observability
# -L and K matrices

# denominator and numerator coefficients must be given in a specific order:
#   numerator: a1*s^n + a2*s^(n-1) + a3*s^(n-2) + a4*s^(n-3) + ... + an =>  [a1, a2, a3, a4, ..., an]
#   denominator: s^n + b1*s^(n-1) + b2*s^(n-2) + b3*s^(n-3) + ... + bn => [b1, b2, b3, ..., bn]


class sys:
    def __init__(self):
        self.A = np.array([])
        self.B = np.array([])
        self.C = np.array([])
        self.D = np.array([])
        self.TFnumerator = np.array([])
        self.TFdenominator = np.array([])
        self.startCond = np.array([])

    # diagonal form
    def diag(self):  # TODO fix this
        eigVals, eigVecs = np.linalg.eig(self.A)
        P = np.empty((np.size(eigVals), 0))  # transformation matrix
        for eigenVector in eigVecs:
            P = np.column_stack((P, eigenVector))
        invP = np.linalg.inv(P)
        A = np.matmul(invP, np.matmul(self.A, P))
        B = np.matmul(invP, self.B)
        C = np.matmul(self.C, P)
        return A, B, C

    # observable canonical form of SISO system
    # highest power of the s in denominator must be bigger than highest power in the numerator
    # highest power of s in denominator must have coefficient equal 1
    def obsv(self):
        if self.TFdenominator[0][0] == 1:
            self.TFdenominator = self.TFdenominator[0][1:]
        numCols = np.size(self.TFnumerator)
        denCols = np.size(self.TFdenominator)
        if denCols > numCols:  # making numerator and denominator equal length filling with 0
            tempArr = np.zeros(denCols)
            tempArr[denCols - numCols:] = self.TFnumerator
            self.TFnumerator = tempArr
        elif denCols < numCols:
            raise Exception('denominator must be higher order than numerator')
        obsvA = np.array([-1 * self.TFdenominator]).transpose()  # column of minus denumerator values
        subMat = np.identity(denCols - 1)  # identity matrix
        subMat = np.vstack((subMat, np.zeros(denCols - 1)))  # row of 0 added to identity matrix
        obsvA = np.append(obsvA, subMat, axis=1)
        obsvB = self.TFnumerator[..., None]  # column of numerator values
        obsvC = np.array([1])
        obsvC = np.append(obsvC, np.zeros(denCols - 1), axis=0)  # row of 0
        return obsvA, obsvB, obsvC

    # controllable canonical form of SISO system
    # highest power of the s in denominator must be bigger than highest power in the numerator
    # highest power of s in denominator must have coefficient equal 1
    def contr(self):
        numCols = np.size(self.TFnumerator)
        denCols = np.size(self.TFdenominator)
        if denCols > numCols:  # making numerator and denominator equal length filling with 0
            tempArr = np.zeros(denCols)
            tempArr[denCols - numCols:] = self.TFnumerator
            self.TFnumerator = tempArr
        elif denCols < numCols:
            raise Exception('denominator must be higher order than numerator')
        contA = np.zeros(denCols - 1)[..., None]  # column of 0
        subMat = np.identity(denCols - 1)  # identity matrix
        contA = np.append(contA, subMat, axis=1)
        contA = np.append(contA, -1 * self.TFdenominator, axis=0)  # row of minus denumerator values
        contB = np.zeros(denCols - 1)[..., None]  # column of 0
        contB = np.vstack((contB, np.array([1])))
        contC = np.array(self.TFnumerator)  # row of numerator values
        return contA, contB, contC


class ss(sys):
    def __init__(self, A, B, C, D, stCond=None):
        super().__init__()
        if stCond is None:
            stCond = []
        self.A = np.array(A)
        tempB = np.array(B)
        self.B = np.reshape(tempB, (np.shape(tempB)[0], 1))
        self.C = np.array(C)
        self.D = np.array(D)
        if np.size(np.array(stCond)) < np.size(A, axis=0):  # if starting conditions vector is too short
            self.startCond = np.array(stCond)
            for i in range(np.size(A, axis=0) - np.size(self.startCond)):
                np.append(self.startCond, np.array([0]))
        else:
            raise Exception('number of starting conditions must be equal to the order of the system')

    def __str__(self):
        strA = str(self.A)
        strB = str(self.B)
        strC = str(self.C)
        strD = str(self.D)
        strRes = 'A = ' + strA + '\n' + 'B = ' + strB + '\n' + 'C = ' + strC + '\n' + 'D = ' + strD + '\n'
        return strRes


class tf(sys):
    def __init__(self, num, denum):
        super().__init__()
        self.TFnumerator = np.array(num)
        self.TFdenominator = np.array(denum)

    def __str__(self):
        numerator = ''
        denominator = ''
        line = ''
        strRes = ''
        for n, num in enumerate(self.TFnumerator):
            if n == np.size(self.TFnumerator) - 1:
                numerator += ' + ' + str(num)
            else:
                if n == 0:
                    pass
                else:
                    numerator += ' + '
                numerator += str(num) + f's^{np.size(self.TFnumerator) - n - 1}'
        denominator += f's^{np.size(self.TFdenominator)}'
        for n, num in enumerate(self.TFdenominator):
            if n == np.size(self.TFdenominator) - 1:
                denominator += ' + ' + str(num)
            else:
                denominator += ' + ' + str(num) + f's^{np.size(self.TFdenominator) - n - 1}'

        largestLength = max(len(numerator), len(denominator))
        for i in range(largestLength):
            line += '-'
        line += '--\n'
        strRes += numerator + '\n' + line + denominator + '\n'
        return strRes


# returns ss system in a observable canonical form based on given tf
def tf2ss(system):
    if isinstance(system, tf):
        if system.TFdenominator[0][0] != 1:
            system.TFnumerator = system.TFnumerator / system.TFdenominator[0][
                0]  # keeping the coefficient of the highest s (s^n) equal to 1
            system.TFdenominator = system.TFdenominator / system.TFnumerator[0][0]
        A, B, C = system.obsv()
        D = np.array([0])
        systemSS = ss(A, B, C, D)
        return systemSS
    else:
        raise Exception('you need to pass tf system as the argument')


def ss2tf(system):
    if isinstance(system, ss):
        pass
    else:
        raise Exception('you need to pass ss system as the argument')


# returns array of poles of system
def poles(system):
    roots = np.array([])
    if isinstance(system, tf):
        roots = np.roots(system.TFdenominator)
    elif isinstance(system, ss):
        roots, eigvecs = np.linalg.eig(system.A)
    else:
        raise Exception('argument must be tf or ss system')
    return roots


# returns array of zeros of system
def zeros(system):
    if isinstance(system, tf):
        roots = np.roots(system.TFnumerator)
    elif isinstance(system, ss):
        roots, eigvecs = np.linalg.eig(system.A)
    else:
        raise Exception('argument must be tf or ss system')
    return roots


# draws phase portrait on phase plane of min 2nd order system, var1 and var2 describes which state variables need to be plot:
# 0 - x1
# 1 - x2 etc.
def phasePortrait(system, var1=0, var2=1, plot=False, Xinit=None):
    if Xinit is None:
        Xinit = [1, 3, 5, 7]
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        phasePortrait(systemSS, var1, var2)
    elif isinstance(system, ss):
        if np.shape(system.A)[0] >= 2:
            Xinit = np.array(Xinit)
            Y = T = Xtmp = X = np.array([[]])
            for i in range(len(Xinit)):
                Y, T, Xtmp = tresp.solveTrap(system, 0, Xinit[i])
                if i == 0:
                    X = Xtmp
                else:
                    X = np.vstack((X, Xtmp))  # adding rows to state trajectory matrix
            stateNum = np.shape(system.A)[0]
            XrowsNum = np.shape(X)[0]
            if stateNum >= var1 or stateNum >= var2:
                fig = plt.figure()
                ax = fig.add_subplot()
                plt.grid(linestyle='--')
                for k in range(0, XrowsNum, stateNum):
                    ax.plot(X[k + var1], X[k + var2])
                ax.set_ylabel(f'x{var1 + 1}(t)')
                ax.set_xlabel(f'x{var2 + 1}(t)')
                ax.set_title('Phase portrait')
                legendList = []
                for xo in Xinit:
                    legendList.append(f'xo={xo}')
                plt.legend(legendList)
                plt.show()
            else:
                raise Exception("system doesn't have that many state variables. Lower var1 or var2")
        else:
            raise Exception('system needs to be at least 2nd order')


# takes system and returns tuple of vectors (Y,T,X) - response and time vectors and state trajectory matrix
def step(system, Tpts=None, plot=False, solver='trap'):
    Y = T = X = np.array([])
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        step(systemSS)
    elif isinstance(system, ss):
        if solver == 'ee':  # explicit (forward) Euler
            Y, T, X = tresp.solveEE(system, 1)
        elif solver == 'ie':  # implicit (backward) Euler
            Y, T, X = tresp.solveIE(system, 1)
        elif solver == 'trap':  # trapezoidal
            Y, T, X = tresp.solveTrap(system, 1)
        elif solver == 'rk4':
            Y, T, X = tresp.solveRK4(system, 1)
        else:
            raise Exception('wrong solver chosen, choose: ee, ie, trap or rk4')
        if Tpts is not None:
            Yi = np.interp(Tpts, T, Y)
            Y = Yi
            T = Tpts
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.plot(T, Y)
            ax.set_title('Step response')
            ax.set_ylabel('y(t)')
            ax.set_xlabel('t [s]')
            plt.show()
        else:
            return Y, T, X
    else:
        raise Exception('argument must be a tf or ss system')


# takes system and returns tuple of vectors (Y,T) - response and time vectors
def pulse(system, plot=False, solver='trap'):
    Y = T = X = np.array([])
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        step(systemSS)
    elif isinstance(system, ss):
        if solver == 'ee':  # explicit (forward) Euler
            Y, T, X = tresp.solveEE(system, 'delta')
        elif solver == 'ie':  # implicit (backward) Euler
            Y, T, X = tresp.solveIE(system, 'delta')
        elif solver == 'trap':  # trapezoidal
            Y, T, X = tresp.solveTrap(system, 'delta')
        elif solver == 'rk4':
            Y, T, X = tresp.solveRK4(system, 'delta')
        else:
            raise Exception('wrong solver chosen, choose: ee, ie, trap or rk4')
        if plot:
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.plot(T, Y)
            ax.set_title('Impulse response')
            ax.set_ylabel('y(t)')
            ax.set_xlabel('t [s]')
            plt.show()
        else:
            return (Y, T, X)
    else:
        raise Exception('argument must be a tf or ss system')


# python's pow() function couldn't handle complex numbers and was trying to cast it into something else
def __imagPow(base, power):
    res = 1
    for i in range(power - 1):
        res *= base
    return res


# creates sinusodial transfer function G(jw)
def __sinTF(system):
    num = []
    den = []
    if isinstance(system, tf):
        for i in range(len(system.TFnumerator)):
            num.append(complex(system.TFnumerator[i], 0))
        for i in range(len(system.TFdenominator)):
            den.append(complex(system.TFdenominator[i], 0))
        for i in range(len(num)):
            num[i] = num[i] * __imagPow(1j, len(num) - i)
        for k in range(len(den)):
            den[k] = den[k] * __imagPow(1j, len(den) - k)
        return (num, den)
    elif isinstance(system, ss):
        systemTF = ss2tf(system)
        __sinTF(systemTF)


# draws bode diagrams for system
def bode(system):
    n, d = __sinTF(system)
    num = den = 0
    Gvec = np.array([])
    Phvec = np.array([])
    Wvec = np.array([])
    # calculating the amplitude and phase characteristics
    for w in np.linspace(0.1, 1000, 20000):
        for i in range(len(n)):
            num += n[i] * pow(w, len(n) - i)
        for k in range(len(d)):
            den += d[k] * pow(w, len(d) - k)
        G = 20 * log(abs(num / den))
        Ph = np.angle((num / den), deg=True)
        Wvec = np.append(Wvec, w)
        Gvec = np.append(Gvec, G)
        Phvec = np.append(Phvec, Ph)
    fig, ax = plt.subplots(2)
    plt.grid(linestyle='--')
    ax[0].set_title('Bode diagrams')
    ax[0].set_ylabel('Magnitude [dB]')
    ax[0].set_xlabel('ω [rad/s]')
    ax[0].set_xscale('log')
    ax[1].set_ylabel('Phase shift [°]')
    ax[1].set_xlabel('ω [rad/s]')
    ax[1].set_xscale('log')
    ax[0].plot(Wvec, Gvec)
    ax[1].plot(Wvec, Phvec)
    plt.show()


# draws nyquist plot of system
# FIXME weird plots (a bit different to matlab/octave)
def nyquist(system):
    n, d = __sinTF(system)
    num = den = 0
    Pvec = np.array([])
    Qvec = np.array([])
    Wvec = np.array([])
    for w in np.linspace(0.1, 1000, 40000):
        for i in range(len(n)):
            num += n[i] * pow(w, len(n) - i)
        for k in range(len(d)):
            den += d[k] * pow(w, len(d) - k)
        P = abs(num / den)
        Q = (num / den).imag
        Wvec = np.append(Wvec, w)
        Pvec = np.append(Pvec, P)
        Qvec = np.append(Qvec, Q)
    fig = plt.figure()
    plt.grid(linestyle='--')
    ax = fig.add_subplot()
    ax.set_title('Nyquist plot G(jω) = P(ω) + jQ(ω)')
    ax.set_ylabel('Q(ω)')
    ax.set_xlabel('P(ω)')
    ax.plot(Pvec, Qvec)
    ax.plot(Pvec, -1 * Qvec)
    plt.show()


def rlocus(system, CLtf=tf([1], [1])):
    if isinstance(system, tf):
        k = 0
        OLpoles = np.roots(system.TFdenominator)
        OLzeros = np.roots(system.TFnumerator)
        temp1 = np.polynomial.polynomial.polymul(CLtf.TFdenominator, system.TFdenominator)
        temp2 = np.polynomial.polynomial.polymul(CLtf.TFnumerator, system.TFnumerator)
        CLdenominator = np.polynomial.polynomial.polyadd(temp1, temp2)
        CLnumerator = np.polynomial.polynomial.polymul(CLtf.TFdenominator, system.TFnumerator)
        CLpoles = np.roots(CLdenominator)
        CLzeros = np.roots(CLnumerator)
    # continue

    elif isinstance(system, ss):
        pass
    else:
        pass



def __setupArrs(system, U, initX = 0, time = 5, h = 0.001, to = 0):
    A = B = C = D = np.array([])
    if isinstance(system, tf):
        systemSS = tf2ss(system)
        A = systemSS.A
        B = systemSS.B
        C = systemSS.C
        D = systemSS.D
    else:
        A = system.A
        B = system.B
        C = system.C
        D = system.D
    Xo = np.array([])
    rowNum = np.shape(A)[0]
    X = np.full((rowNum, 1), 0)
    if isinstance(initX, np.ndarray):
        Xo = initX
    else:                                                                   #if you assign number into initX it would be the initial value for all the state variables
        temp = np.full((rowNum, 1), initX)
        Xo = temp
    X = Xo
    Y = np.array([])
    Yo = np.dot(C,Xo)+D
    Y = np.append(Y,Yo)
    T = np.array([])
    T = np.append(T, to)
    t = to
    N = int((time - to)/h)                                                  #number of simulation steps
    return (A,B,C,D,X,Y,T,N,t)


#calculating time domain response and state trajectory of LTI system using Explicit (Forward) Euler method [time in seconds]
def solveEE(system, U, initX = 0, time = 5, h = 0.001, to = 0):
    A,B,C,D,X,Y,T,N,t = __setupArrs(system, U, initX, time, h, to)
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:,[i]]                                                    #ith column of X
        Xnext = Xprev + h*(np.dot(A,Xprev) + np.dot(B,U))                   #Forward Euler formula
        X = np.c_[X,Xnext]                                                  #adding new column
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return (Y,T,X)



#calculating time domain response and state trajectory of LTI system using Implicit (Backward) Euler method
def solveIE(system, U, initX = 0, time = 5, h = 0.001, to = 0):
    A,B,C,D,X,Y,T,N,t = __setupArrs(system, U, initX, time, h, to)
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:,[i]]
        XFE = Xprev + h*(np.dot(A,Xprev) + np.dot(B,U))                     #takes Implicit Euler method's step for approximation 
        Xnext = Xprev + h*(np.dot(A,XFE) + np.dot(B,U))
        X = np.c_[X,Xnext]
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return (Y,T,X)


#calculating time domain response and state trajectory of LTI system using Trapezoidal method
def solveTrap(system, U, initX = 0, time = 5, h = 0.001, to = 0):
    A,B,C,D,X,Y,T,N,t = __setupArrs(system, U, initX, time, h, to)
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:,[i]]
        Xnprim = np.dot(A,Xprev) + np.dot(B,U)
        XFE = Xprev + h*(Xnprim)
        Xnext = Xprev + (h/2)*(Xnprim + (np.dot(A,XFE) + np.dot(B,U)))      #takes average of the slopes from IE and EE methods
        X = np.c_[X,Xnext]
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return (Y,T,X)


#calculating time domain response and state trajectory of LTI system using Runge-Kutta 4 method
# X' = f(X) => X' = A*X + B*U
def solveRK4(system, U, initX = 0, time = 5, h = 0.001, to = 0):
    A,B,C,D,X,Y,T,N,t = __setupArrs(system, U, initX, time, h, to)
    k1 = k2 = k3 = k4 = np.array([])
    Udlt = False
    if U == 'delta':
        U = 1
        Udlt = True
    for i in range(N):
        t += h
        Xprev = X[:,[i]]
        f = np.dot(A,Xprev) + np.dot(B,U)
        k1 = h*f
        k2 = h*(f + k1/2)
        k3 = h*(f + k2/2)
        k4 = h*(f + k3)
        Xnext = Xprev + (k1 + 2*k2 + 2*k3 +k4)/6
        X = np.c_[X,Xnext]
        Ytemp = np.dot(C, Xnext)
        Y = np.append(Y, Ytemp)
        T = np.append(T, t)
        if Udlt:
            U = 0
            Udlt = False
    return (Y,T,X)




