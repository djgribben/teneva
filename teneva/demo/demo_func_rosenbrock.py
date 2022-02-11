"""Package teneva, module demo.demo_func_rosenbrock: function.

This module contains class that implements analytical Rosenbrock function
for demo and tests.

"""
import numpy as np
from scipy.optimize import rosen


from .demo_func import DemoFunc


class DemoFuncRosenbrock(DemoFunc):
    def __init__(self, d):
        """Rosenbrock function for demo and tests.

        See https://www.sfu.ca/~ssurjano/rosen.html for details.

        Args:
            d (int): number of dimensions.

        """
        super().__init__(d, 'Rosenbrock')

        self.set_lim(-2.048, +2.048)
        self.set_min([1.]*self.d, 0.)

    def _calc(self, x):
        return rosen(x)

    def _comp(self, X):
        return rosen(X.T)
