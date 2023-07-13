from pymoo.core.problem import Problem
from pymoo.core.problem import ElementwiseProblem
from typing import final
from epyt import epanet
from FO import FuncaoObjetivo
import random
from datetime import datetime
from multiprocessing.pool import ThreadPool
import threading
import numpy as np

NUMBEROFPIPES: final = 8

# pool = ThreadPool(5)

class TesteProb(Problem):
    def __init__(self, **kwargs):
        self.Xmin = []
        self.Xmax = []
        self.NumberOfVariables = NUMBEROFPIPES

        for i in range(self.NumberOfVariables):
            self.Xmin.append(0)
            self.Xmax.append(13)

        super().__init__(n_var = self.NumberOfVariables, n_obj = 2, xl = self.Xmin, xu= self.Xmax, vtype = int, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
    # Monothread solution

        res = []

        for design in X:
            res.append(FuncaoObjetivo(design))

        out["F"] = np.array(res)

    # Multithread solution

        # out["F"] = FuncaoObjetivo(X)
