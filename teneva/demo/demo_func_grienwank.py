"""Package teneva, module demo.demo_func_grienwank: function.

This module contains class that implements analytical Grienwank function
for demo and tests.

"""
import numpy as np


from .demo_func import DemoFunc


class DemoFuncGrienwank(DemoFunc):
    def __init__(self, d):
        """Grienwank function for demo and tests.

        See https://www.sfu.ca/~ssurjano/griewank.html for details.

        Args:
            d (int): number of dimensions.

        """
        super().__init__(d, 'Grienwank')

        self.set_lim(-600., +600.)
        self.set_min([0.]*self.d, 0.)

    def _calc(self, x):
        y1 = np.sum(x**2) / 4000

        y2 = np.cos(x / np.sqrt(np.arange(self.d) + 1.))
        y2 = - np.prod(y2)

        y3 = 1.

        return y1 + y2 + y3

    def _comp(self, X):
        y1 = np.sum(X**2, axis=1) / 4000

        y2 = np.cos(X / np.sqrt(np.arange(self.d) + 1))
        y2 = - np.prod(y2, axis=1)

        y3 = 1.

        return y1 + y2 + y3
