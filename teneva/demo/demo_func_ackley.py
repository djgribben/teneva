"""Package teneva, module demo.demo_func_ackley: function.

This module contains class that implements analytical Ackley function
for demo and tests.

"""
import numpy as np


from .demo_func import DemoFunc


class DemoFuncAckley(DemoFunc):
    def __init__(self, d, a=20., b=0.2, c=2.*np.pi):
        """Ackley function for demo and tests.

        See https://www.sfu.ca/~ssurjano/ackley.html for details.

        Args:
            d (int): number of dimensions.
            a (float): parameter of the function.
            b (float): parameter of the function.
            c (float): parameter of the function.

        """
        super().__init__(d, 'Ackley')

        self.par_a = a
        self.par_b = b
        self.par_c = c

        self.set_lim(-32.768, +32.768)
        self.set_min([0.]*self.d, 0.)

    def _calc(self, x):
        y1 = np.sqrt(np.sum(x**2) / self.d)
        y1 = - self.par_a * np.exp(-self.par_b * y1)

        y2 = np.sum(np.cos(self.par_c * x))
        y2 = - np.exp(y2 / self.d)

        y3 = self.par_a + np.exp(1.)

        return y1 + y2 + y3

    def _comp(self, X):
        y1 = np.sqrt(np.sum(X**2, axis=1) / self.d)
        y1 = - self.par_a * np.exp(-self.par_b * y1)

        y2 = np.sum(np.cos(self.par_c * X), axis=1)
        y2 = - np.exp(y2 / self.d)

        y3 = self.par_a + np.exp(1.)

        return y1 + y2 + y3
