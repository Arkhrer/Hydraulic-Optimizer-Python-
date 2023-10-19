from pymoo.core.problem import Problem
from pymoo.core.problem import ElementwiseProblem
from typing import final
from epyt import epanet
from ObjectiveFunction import ObjectiveFunction
import random
from datetime import datetime
from multiprocessing.pool import ThreadPool
import threading
import numpy as np

NUMBEROFPIPES: final = 8

# pool = ThreadPool(5)

class EPANETProblem(Problem):
    def __init__(self, counter = False, **kwargs):
        self.Xmin = []
        self.Xmax = []
        self.NumberOfVariables = NUMBEROFPIPES
        self.allowcounter = counter
        self.overallSuccesses = 0
        if self.allowcounter == True:
            self.counter = 0

        for i in range(self.NumberOfVariables):
            self.Xmin.append(0)
            self.Xmax.append(13)

        super().__init__(n_var = self.NumberOfVariables, n_obj = 2, xl = self.Xmin, xu= self.Xmax, vtype = int, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
    # Monothread solution

        res = []

        for design in X:
            if self.allowcounter == True:
                self.counter = self.counter + 1
            res.append(ObjectiveFunction(design))
            if (res[len(res) - 1][0] <= 430000):
                self.overallSuccesses += 1

        out["F"] = np.array(res)

    # Multithread solution

        # out["F"] = ObjectiveFunction(X)
