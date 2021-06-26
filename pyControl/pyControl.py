import numpy as np
import plotter as plt


# denumerator and numerator coefficients must be given in a specific order:
#   a1*s^n + a2*s^(n-1) + a3*s^(n-2) + a4*s^(n-3) + ... =>  [a1, a2, a3, a4,...]

class sys:
    def __init__(self):
        self.A = np.array()
        self.B = np.array()
        self.C = np.array()
        self.D = np.array()
        self.TFnumerator = np.array([])
        self.TFdenumerator = np.array([])

    # diagonal form
    def diag(self):
        eigVals, eigVecs = np.linalg.eig(self.A)
        P = np.array()  # transformation matrix
        for eigenVector in eigVecs:
            P = np.append(P, np.array(eigenVector).transpose(), axis=1)
        invP = np.linalg.inv(P)
        A = invP * self.A * P
        B = invP * self.B
        C = self.C * P
        return A, B, C

    # observable canonical form of SISO system
    # highest power of the s in denumerator must be bigger than highest power in the numerator
    # highest power of s in denumerator must have coefficient equal 1
    def obsv(self):
        numRows, numCols = self.TFnumerator.shape()
        denRows, denCols = self.TFdenumerator.shape()
        if denCols > numCols:
            tempArr = np.array()
            np.append(tempArr, np.zeros(denCols - numCols))
            np.append(tempArr, self.TFnumerator)
            self.TFnumerator = tempArr
        elif denCols < numCols:
            raise Exception('denumerator must be higher order than numerator')
        obsvA = np.array()
        obsvB = np.array()
        obsvC = np.array()
        obsvA = np.append(obsvA, -1 * self.TFdenumerator.transpose(), axis=1)
        subMat = np.identity(denCols - 1)
        np.append(subMat, np.zeros(denCols - 1), axis=0)
        obsvA = np.append(obsvA, subMat, axis=1)
        obsvB = np.append(obsvB, self.TFnumerator.transpose(), axis=1)
        obsvC = np.append(obsvC, np.array([1]), axis=1)
        obsvC = np.append(obsvC, np.zeros(denCols - 1), axis=1)
        return obsvA, obsvB, obsvC

    # controllable canonical form of SISO system
    # highest power of the s in denumerator must be bigger than highest power in the numerator
    # highest power of s in denumerator must have coefficient equal 1
    def contr(self):
        numRows, numCols = self.TFnumerator.shape()
        denRows, denCols = self.TFdenumerator.shape()
        if denCols > numCols:
            tempArr = np.array()
            np.append(tempArr, np.zeros(denCols - numCols))
            np.append(tempArr, self.TFnumerator)
            self.TFnumerator = tempArr
        elif denCols < numCols:
            raise Exception('denumerator must be higher order than numerator')
        contA = np.array()
        contB = np.array()
        contC = np.array()
        contA = np.append(contA, np.zeros(denCols - 1).transpose(), axis=1)
        subMat = np.identity(denCols - 1)
        np.append(contA, subMat, axis=1)
        np.append(contA, -1 * self.TFdenumerator, axis=0)
        contB = np.zeros(denCols - 1).transpose()
        np.append(contB, np.array([1]), axis=0)
        contC = np.array(self.TFnumerator)
        return contA, contB, contC


class ss(sys):
    def __init__(self, A, B, C, D):
        super().__init__()
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.D = np.array(D)


class tf(sys):
    def __init__(self, num, denum):
        super().__init__()
        self.TFnumerator = np.array(num)
        self.TFdenumerator = np.array(denum)


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
