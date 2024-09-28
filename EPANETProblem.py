from ObjectiveFunction import ObjectiveFunction
from pymoo.core.problem import Problem
from datetime import datetime
from typing import final
from epyt import epanet
import numpy as np
import Globals
import random

class EPANETProblem(Problem):
    def __init__(self, counter = False, **kwargs):
        self.Xmin = []
        self.Xmax = []
        self.NumberOfVariables = Globals.NUMBER_OF_PIPES
        self.allowcounter = counter
        self.overallSuccesses = 0
        if self.allowcounter == True:
            self.counter = 0

        for i in range(self.NumberOfVariables):
            self.Xmin.append(0)
            self.Xmax.append(Globals.AVAILABLE_DIAMETERS - 1)

        super().__init__(n_var = self.NumberOfVariables, n_obj = 2, xl = self.Xmin, xu= self.Xmax, vtype = int, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
        res = []

        for design in X:
            if self.allowcounter == True:
                self.counter = self.counter + 1
                
            res.append(ObjectiveFunction(design))
            
            if (res[len(res) - 1][0] <= 430000):
                self.overallSuccesses += 1

        out["F"] = np.array(res)
