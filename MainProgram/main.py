import TP
import time
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize

dimensao_populacao: int

if __name__ == '__main__':

    start = time.time()

    print("\nRodando...")

    time.sleep(1)

    print("\nTempo: ", (time.time() - start), " segundos")
    print("\n", TP.Problem.n_populacao)

    algorithm = NSGA2(pop_size = 200, crossover = SBX(prob = 0.8), mutation = PM(prob = 0.050))

    stop_criteria = ('n_gen', 1000)

    res = minimize(problem, algorithm, stop_criteria, seed = 1, verbose = False)