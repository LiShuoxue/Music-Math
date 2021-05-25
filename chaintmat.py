# chaintmat
# Author: Yuhan Zhou <zhouyuhan_@outlook.com>
#         Shuoxue Li <1620480103@qq.com>

import numpy as np
import random as rm


def tmat2chain(tmat, dim, maxlength:int, start:int):
    """
    Build a random chain with transition matrix established.
    Attributes:
        tmat:   transition matrix               numpy array
        dim:    dimension of matrix             integer
        length: length of Markov chain          numpy array
        start:  initial state, -1 for random    integer
        end:    eventual state, -1 for random   integer
    """
    space = range(dim)
    chain = []
    if start == -1: start = rm.choices(range(dim), weights = [(lambda x: int(np.sum(tmat[x]) > 0))(x) for x in range(dim)], k=1)[0]
    chain.append(start)
    for x in range(maxlength - 1):
        try: chain.append(rm.choices(space, weights=tmat[chain[x]].tolist(), k=1)[0])
        except ValueError: break
    return chain


class ChainTmat:
    """
    Create State Transfer Matrix (STM) from certain series, and generate Markov chain from STM.
    """
    def __init__(self, dim:int):
        self.seq = [] # series of "index" in state space
        self.dim = dim
        self._matrix = np.zeros([self.dim, self.dim])
    
    def reset(self):
        self.seq = []
        self._matrix = np.zeros([self.dim, self.dim])

    def append(self, series): self.seq.append(series)

    def chain2tmat(self):
        for i in range(len(self.seq)):
            for j in range(len(self.seq[i]) - 1):
                x, y = self.seq[i][j], self.seq[i][j+1]
                self._matrix[x][y] += 1
        for i in range(self.dim):
            if np.sum(self._matrix[i]) != 0: self._matrix[i] /= np.sum(self._matrix[i])

    def tmat2chain(self, maxlength:int, start=-1):
        return tmat2chain(self._matrix, self.dim, maxlength, start)

    @property
    def matrix(self):
        if self._matrix.sum() == 0:
            raise ValueError('matrix has not been generated, use `generateMat` first')
        return self._matrix
