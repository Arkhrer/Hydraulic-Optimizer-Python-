from pymoo.core.problem import Problem
from typing import Final
import FO

NUMBEROFPIPES: Final = 8

class TesteProb(Problem):
    def __init__(self, n_obj = 2, **kwargs):
        FO.InicializarProblema()

        self.NumberOfVariables: int
        self.n_populacao: int
        self.n_geracao: int
        self.saida = [100]

        self.NumberOfVariables = NUMBEROFPIPES

        self.Xmin = []
        self.Xmax = []
        for i in range(self.NumberOfVariables):
            self.Xmin.append(0)
            self.Xmax.append(13)

        self.Objectives = []


        super().__init__(n_var = self.NumberOfVariables, n_obj = NUMBEROFPIPES)
    
    def _evaluate(self, x, out, *args, **kwargs):
        pass

Problem = TesteProb()