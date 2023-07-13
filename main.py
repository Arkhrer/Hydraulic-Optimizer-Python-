from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.core.problem import StarmapParallelization
from pymoo.operators.crossover.sbx import SBX
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.config import Config
from math import factorial
import time
import TP
#Parallelization
from multiprocessing.pool import ThreadPool
import multiprocessing

from threading import Lock

# mutex = Lock()

if __name__ == '__main__':

#Threads
    # n_threads = 5
    # pool = ThreadPool(n_threads)
    # runner = StarmapParallelization(pool.starmap)

#Processes
#     n_proccess = 8
#     pool = multiprocessing.Pool(n_proccess)
#     runner = StarmapParallelization(pool.starmap)

    # --------------------------------------------- #

    Config.warnings['not_compiled'] = False

    start = time.time()

    print("\nRodando...")
    # problem = TP.TesteProb(elementwise_runner = runner)

    n_objectives = 2

    n_dimensions = n_objectives
    
    n_partitions = 12

    # n_points = factorial(n_objectives + n_partitions - 1)/(factorial(n_objectives + n_partitions - 1)*factorial(n_partitions))

    ref_dirs = get_reference_directions("das-dennis", n_dimensions, n_partitions=n_partitions, seed = 1)

    problem = TP.TesteProb()

    algorithm = UNSGA3(ref_dirs=ref_dirs, pop_size = 200, sampling = IntegerRandomSampling(), crossover = SBX(prob = 0.8, vtype = int), mutation = PM(prob = 0.050, vtype = int))
    stop_criteria = ('n_gen', 1000)
    res = minimize(problem, algorithm, stop_criteria, seed = 1, verbose = False)

    end = (time.time() - start)
    endmin = int(end/60)

    print("\nTempo: ", endmin, " minutos e ", end - (endmin * 60), " segundos")

    out = open("resultadosnsga.txt", "w")

    out.write("Populacoes\n")
    n = 1
    for line in res.X:
        out.write('%d' %n)
        out.write(".)")
        for i in range(8):
            out.write(line[i].astype(str))
            out.write("\t")
        out.write("\n")
        n= n + 1

    out.write("\n---------------------\n")

    out.write("Resultados de avaliacao\n")
    n = 1
    for line in res.F:
        out.write('%d' %n)
        out.write(".)")
        out.write(line[0].astype(str))
        out.write("\t")
        out.write('%f' %((-1.)*line[1]))
        out.write("\n")
        n = n + 1

    out.close()