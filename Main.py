# from pymoo.core.problem import StarmapParallelization
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from EPANETProblem import EPANETProblem
from pymoo.optimize import minimize
from pymoo.config import Config
import AlgorithmSelection
import random
import time
import xlwt
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

    allOfThem: bool = True
    selectedAlgorithm: str = "RNSGA3"

    counter: bool = True

    stop_criteria = ('n_gen', 100)

    #Parameters

    seed = int(time.time())

    population_size = 10
    sampling = IntegerRandomSampling()
    crossover_chance = 0.8
    crossover = SBX(prob = crossover_chance, vtype = int)
    mutation_chance = 0.05
    mutation = PM(prob = mutation_chance, vtype = int)

    n_objectives = 2
    n_dimensions = n_objectives
    ref_dirs = get_reference_directions("das-dennis", n_dimensions, n_partitions = population_size - 1, seed = seed)


    print("Running...")

    # Workbook for spreadsheet
    wb = xlwt.Workbook()

    ws = wb.add_sheet("General data")
    ws.write(0, 0, "Population Size")
    ws.write(0, 1, population_size)

    ws.write(1, 0, "Seed")
    ws.write(1, 1, seed)

    ws.write(2, 0, "Crossover probability")
    ws.write(2, 1, crossover_chance)

    ws.write(3, 0, "Mutation probability")
    ws.write(3, 1, mutation_chance)

    #ws.write(4, 0, "Reference directions")
    #ws.write(4, 1, ref_dirs)

    if(allOfThem):

        for currentAlgorithm in AlgorithmSelection.REF:
            problem = EPANETProblem(counter = counter)

            print(currentAlgorithm)

            algorithm = AlgorithmSelection.SelectAlgorithm(name = currentAlgorithm, pop_size = population_size, samp = sampling, co = crossover, mt = mutation, no = n_objectives, nd = n_dimensions, rd = ref_dirs)
    

            currentAlgoStart = time.time()

            res = minimize(problem, algorithm, stop_criteria, seed = seed, verbose = False)

            currentAlgoEnd = (time.time() - start)

            ws = wb.add_sheet(currentAlgorithm)
            n: int = 0
            successes:int = 0

            ws.write(n, 0, "Populations")

            for line in res.X:
                n += 1
                for i in range(8):
                    ws.write(n, i, line[i].item())

            n += 1
            ws.write(n, 0, "Avaliation results")
            for line in res.F:
                n += 1

                ws.write(n, 0, line[0].item())
                ws.write(n, 1, line[1] * (-1.))

                if (line[0].item() <= 430000):
                    ws.write(n, 2, "Success")
                    successes += 1
                else:
                    ws.write(n, 2, "Failure")

            n += 1
            ws.write(n, 0, "Successes")
            ws.write(n, 1, successes)

            n += 1
            ws.write(n, 0, "Overall Successes")
            ws.write(n, 1, problem.overallSuccesses)

            n += 1
            ws.write(n, 0, "Success rate")
            ws.write(n, 1, successes/len(res.F))

            n += 1
            ws.write(n, 0, "Overall Success rate")
            ws.write(n, 1, problem.overallSuccesses / problem.counter)

            if counter == True:
                n += 1
                ws.write(n, 0,"Number of calls")
                n += 1
                ws.write(n, 0, problem.counter)

            n += 1
            currentEndMin = int(currentAlgoEnd/60)
            ws.write(n, 0, "Minutes:")
            ws.write(n, 1, currentEndMin)
            n += 1
            ws.write(n, 0, "Seconds")
            ws.write(n, 1, currentAlgoEnd - (currentEndMin * 60))
            
            del problem
            del algorithm

    else:
        # problem = TP.TesteProb(elementwise_runner = runner)
        problem = EPANETProblem(counter = counter)

        algorithm = AlgorithmSelection.SelectAlgorithm(selectedAlgorithm)

        res = minimize(problem, algorithm, stop_criteria, seed = seed, verbose = False)

        ws = wb.add_sheet(selectedAlgorithm)
        n: int = 0

        ws.write(n, 0, "Populations")

        for line in res.X:
            n += 1
            for i in range(8):
                ws.write(n, i, line[i].item())

        n += 1
        ws.write(n, 0, "Avaliation results")
        for line in res.F:
            n += 1

            ws.write(n, 0, line[0].item())
            ws.write(n, 1, line[1] * (-1.))

        if counter == True:
            n += 1
            ws.write(n, 0,"Number of calls")
            n += 1
            ws.write(n, 0, problem.counter)

    wb.save("results.xls")

    end = (time.time() - start)
    endmin = int(end/60)
    print("Time: ", endmin, " minutes and ", end - (endmin * 60), " seconds")