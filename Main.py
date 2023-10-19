# from pymoo.core.problem import StarmapParallelization
import random
from pymoo.optimize import minimize
from pymoo.config import Config
import AlgorithmSelection
import time
from EPANETProblem import EPANETProblem
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

    seed = int(time.time())

    print("Running...")

    # Workbook for spreadsheet
    wb = xlwt.Workbook()

    if(allOfThem):

        for currentAlgorithm in AlgorithmSelection.REF:
            problem = EPANETProblem(counter = counter)

            print(currentAlgorithm)

            algorithm = AlgorithmSelection.SelectAlgorithm(currentAlgorithm)

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
            ws.write(n, 0,"Seed")
            n += 1
            ws.write(n, 0, seed)

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