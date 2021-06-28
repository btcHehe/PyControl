import numpy as np
from scipy.integrate import odeint, solve_ivp
import plotter as plt


# denumerator and numerator coefficients must be given in a specific order:
#   numerator: a1*s^n + a2*s^(n-1) + a3*s^(n-2) + a4*s^(n-3) + ... =>  [a1, a2, a3, a4,...]
#   denumerator: s^n + a1*s^(n-1) + a2*s^(n-2) + a3*s^(n-3) + ... => [a1, a2, a3, ...]

class sys:
    def __init__(self):
        self.A = np.array([])
        self.B = np.array([])
        self.C = np.array([])
        self.D = np.array([])
        self.TFnumerator = np.array([])
        self.TFdenumerator = np.array([])
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
    # highest power of the s in denumerator must be bigger than highest power in the numerator
    # highest power of s in denumerator must have coefficient equal 1
    def obsv(self):
        numCols = np.size(self.TFnumerator)
        denCols = np.size(self.TFdenumerator)
        if denCols > numCols:  # making numerator and denumerator equal length filling with 0
            tempArr = np.zeros(denCols)
            tempArr[denCols - numCols:] = self.TFnumerator
            self.TFnumerator = tempArr
        elif denCols < numCols:
            raise Exception('denumerator must be higher order than numerator')
        obsvA = -1 * self.TFdenumerator.transpose()  # column of minus denumerator values
        subMat = np.identity(denCols - 1)  # identity matrix
        subMat = np.vstack((subMat, np.zeros(denCols - 1)))  # row of 0 added to identity matrix
        obsvA = np.append(obsvA, subMat, axis=1)
        obsvB = self.TFnumerator[..., None]  # column of numerator values
        obsvC = np.array([1])
        obsvC = np.append(obsvC, np.zeros(denCols - 1), axis=0)  # row of 0
        return obsvA, obsvB, obsvC

    # controllable canonical form of SISO system
    # highest power of the s in denumerator must be bigger than highest power in the numerator
    # highest power of s in denumerator must have coefficient equal 1
    def contr(self):
        numCols = np.size(self.TFnumerator)
        denCols = np.size(self.TFdenumerator)
        if denCols > numCols:  # making numerator and denumerator equal length filling with 0
            tempArr = np.zeros(denCols)
            tempArr[denCols - numCols:] = self.TFnumerator
            self.TFnumerator = tempArr
        elif denCols < numCols:
            raise Exception('denumerator must be higher order than numerator')
        contA = np.zeros(denCols - 1)[..., None]  # column of 0
        subMat = np.identity(denCols - 1)  # identity matrix
        contA = np.append(contA, subMat, axis=1)
        contA = np.append(contA, -1 * self.TFdenumerator, axis=0)  # row of minus denumerator values
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
        self.B = np.array(B)
        self.C = np.array(C)
        self.D = np.array(D)
        if np.size(np.array(stCond)) < np.size(A, axis=0):  # if starting conditions vector is too short
            self.startCond = np.array(stCond)
            for i in range(np.size(A, axis=0) - np.size(self.startCond)):
                np.append(self.startCond, np.array([0]))
        else:
            raise Exception('number of starting conditions must be equal to the order of the system')


class tf(sys):
    def __init__(self, num, denum):
        super().__init__()
        self.TFnumerator = np.array([num])
        self.TFdenumerator = np.array([denum])


def tfToss(system):
    if isinstance(system, tf):
        A, B, C = system.obsv()
        D = np.array([0])
        systemSS = ss(A, B, C, D)
        return systemSS
    else:
        raise Exception('you need to pass tf system as the argument')


def step(system):
    if isinstance(system, tf):
        systemSS = tfToss(system)
        step(systemSS)
    elif isinstance(system, ss):
        pass
    else:
        raise Exception('argument must be an instance of tf or ss class')
