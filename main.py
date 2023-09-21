# from pymoo.core.problem import StarmapParallelization
import random
from pymoo.optimize import minimize
from pymoo.config import Config
import algorithm_selection
import time
from EPANETProblem import EPANETProblem
#Parallelization
# from multiprocessing.pool import ThreadPool
# import multiprocessing

# from threading import Lock

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

    counter = True
    problem = EPANETProblem(counter = counter)

    algorithm = algorithm_selection.select_algorithm("RVEA")

    stop_criteria = ('n_gen', 1000)
    res = minimize(problem, algorithm, stop_criteria, seed = int(time.time()), verbose = False)

    end = (time.time() - start)
    endmin = int(end/60)

    print("\nTempo: ", endmin, " minutos e ", end - (endmin * 60), " segundos")

    out = open("resultados.txt", "w")

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

    if counter == True:
        out.write("\n Numero de chamadas: %d" %problem.counter)
    out.close()