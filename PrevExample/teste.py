from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from deap import benchmarks

try:
    import numpy as np
except:
    exit()

#-----------------------------------------------------------------------------------------

class RDA (Problem):
    def __init__(self, n_obj = 2, **kwargs):
        super().__init__(n_var = 2, n_obj = n_obj, xl = -5., xu = 5., vtype = float, **kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        res = []
        for design in x:
            res.append(benchmarks.kursawe(design))
            
        out["F"] = np.array(res)

problem = RDA(n_obj=2)

algorithm = NSGA2(pop_size=100)

stop_criteria = ('n_gen', 200)

res = minimize(problem, algorithm, stop_criteria, seed=1, verbose=False)