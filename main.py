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