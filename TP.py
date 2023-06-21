from pymoo.core.problem import Problem
from typing import final
from epyt import epanet
from FO import FuncaoObjetivo
import random
from datetime import datetime

try:
    import numpy as np
except:
    exit()

NUMBEROFPIPES: final = 8

class TesteProb(Problem):
    def __init__(self, **kwargs):
        self.Xmin = []
        self.Xmax = []
        self.NumberOfVariables = NUMBEROFPIPES

        for i in range(self.NumberOfVariables):
            self.Xmin.append(0)
            self.Xmax.append(13)

        super().__init__(n_var = self.NumberOfVariables, n_obj = 2, xl = self.Xmin, xu= self.Xmax, vtype = int, **kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        res = []
        for design in x:
            res.append(FuncaoObjetivo(design))

        out["F"] = np.array(res)
