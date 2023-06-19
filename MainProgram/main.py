import TP
import time
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.config import Config
from pymoo.operators.sampling.rnd import IntegerRandomSampling

if __name__ == '__main__':
    problem = TP.TesteProb()

    Config.warnings['not_compiled'] = False

    start = time.time()

    print("\nRodando...")

    algorithm = NSGA2(pop_size = 200, sampling = IntegerRandomSampling(), crossover = SBX(prob = 0.8, vtype = int), mutation = PM(prob = 0.050, vtype = int))
    stop_criteria = ('n_gen', 2)
    res = minimize(problem, algorithm, stop_criteria, seed = 1, verbose = False)

    print("\nTempo: ", (time.time() - start), " segundos")

    out = open("resultadosnsga.txt", "w")

    for line in res.F:
        out.write(line[0].astype(str))
        out.write("\t")
        out.write(line[1].astype(str))
        out.write("\n")

    out.close()