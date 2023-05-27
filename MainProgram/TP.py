from pymoo.core.problem import Problem
from typing import final
from epyt import epanet

NUMBEROFPIPES: Final = 8

class TesteProb(Problem):
    def __init__(self):
        Xmin = []
        Xmax = []

        for i in range(NUMBEROFPIPES):
            Xmin.append(0)
            Xmax.append(13)

        super().__init__(n_var = NUMBEROFPIPES, n_obj = 2, x1 = Xmin, xu= Xmax, vtype = float)

    def __evaluate(self, x, out, *args, **kwargs):
        pass

Problem = TesteProb()