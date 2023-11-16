# from pymoo.core.problem import StarmapParallelization
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from EPANETProblem import EPANETProblem
from pymoo.optimize import minimize
from pymoo.config import Config
import AlgorithmSelection
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import csv
import os
import Loops
import docker

#Parallelization
from multiprocessing.pool import ThreadPool
# import multiprocessing
from pymoo.core.problem import StarmapParallelization

# from threading import Lock

# mutex = Lock()

diametersLabels = []
for it in range(8):
    diametersLabels += [f"Diameter {it + 1}"]

allOfThem: bool = True
selectedAlgorithm: str = "NSGA3"

counter: bool = True

#Parameters

sampling = IntegerRandomSampling()
generations = 100
stop_criteria = ('n_gen', generations)

n_objectives = 2
n_dimensions = n_objectives

currentRound = 0

saveState:bool = False

def ExecuteAlgorithms(**kwargs):
    global currentRound
    global counter
    global n_objectives
    global n_dimensions
    global counter
    global sampling
    global diametersLabels
    global allOfThem
    global selectedAlgorithm
    global generations
    global stop_criteria
    global saveState
    
    seed = kwargs["seed"]
    seedRound = kwargs["seedRound"]
    mutationRate = kwargs["mutationRate"]
    crossoverRate = kwargs["crossoverRate"]
    populationSize = kwargs["populationSize"]
    
    if(saveState):
        f = open(".savestate",'r')
        content = f.readlines()
        
        if (seedRound != int(content[0])):
            f.close()
            return
        if (mutationRate != float(content[1])):
            f.close()
            return
        if (crossoverRate != float(content[2])):
            f.close()
            return
        if (populationSize != float(content[3])):
            f.close()
            return
        f.close()

#Threads
    # n_threads = 100
    # pool = ThreadPool(n_threads)
# #Processes
    # n_proccess = 100
    # pool = multiprocessing.Pool(n_proccess)
    
    # runner = StarmapParallelization(pool.starmap)

    # --------------------------------------------- #

    ref_dirs = get_reference_directions("das-dennis", n_dimensions, n_partitions = populationSize - 1, seed = seed)

    mutation = PM(prob = mutationRate, vtype = int)

    crossover = SBX(prob = crossoverRate, vtype = int)

    currentRound += 1

    if(allOfThem):
        for currentAlgorithm in AlgorithmSelection.REF:
            if(saveState):
                f = open(".savestate",'r')
                content = f.readlines()
                if (currentAlgorithm != content[4][:-1]):
                    f.close()
                else:
                    f.close()
                    saveState = False
            else:
                # problem = EPANETProblem(counter = counter, elementwise_runner = runner)
                problem = EPANETProblem(counter = counter)

                print(currentAlgorithm)

                algorithm = AlgorithmSelection.SelectAlgorithm(name = currentAlgorithm, pop_size = populationSize, samp = sampling, co = crossover, mt = mutation, no = n_objectives, nd = n_dimensions, rd = ref_dirs)
        
                currentAlgoStart = time.time()

                res = minimize(problem, algorithm, stop_criteria, seed = seed, verbose = False)

                currentAlgoEnd = (time.time() - start)

                if not os.path.exists(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}"): 
                    os.makedirs(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}")

                currentWriter = csv.writer(open(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}/{seed}.csv", 'w', encoding = "utf-8"))
                currentWriter.writerow([currentAlgorithm])
                currentWriter.writerow(["Seed", seed])
                currentWriter.writerow(["Generations", generations])
                currentWriter.writerow(["Population size", populationSize])
                currentWriter.writerow(["Crossover chance", crossoverRate])
                currentWriter.writerow(["Mutation chance", mutationRate])
                successes = 0
                for line in res.F:
                    if (line[0] <= 430000):
                        successes += 1
                currentWriter.writerow(["Successes", successes])
                currentWriter.writerow(["Overall successes", problem.overallSuccesses])
                currentWriter.writerow(["Quality(success rate)", successes/len(res.F)])
                currentWriter.writerow(["Overall quality(success rate)", (problem.overallSuccesses)/(problem.counter)])
                if (counter == True):
                    currentWriter.writerow(["Objective Function Calls", problem.counter])
                    currentWriter.writerow(["Eficiency", (successes/len(res.F))/(problem.counter)])
                currentEndMin = int(currentAlgoEnd/60)
                currentWriter.writerow(["Minutes", currentEndMin, "Seconds", currentAlgoEnd - (currentEndMin * 60)])

                minimumCost:int = 1000000000
                maximumRI:int = 0
                for line in res.F:
                    if (line[0] < minimumCost):
                        minimumCost = line[0]
                    if ((line[1])*(-1) > maximumRI):
                        maximumRI = (line[1])*(-1)
                currentWriter.writerow(["Minimmum cost", minimumCost])
                currentWriter.writerow(["Maximum RI", maximumRI])

                currentWriter.writerow(diametersLabels + ["Cost", "SumRI"])
                resultsList = list(zip(res.X, res.F))
                for element in resultsList:
                    element[1][1] = element[1][1]*(-1)
                    row = np.concatenate((element[0], element[1]), axis = None)
                    if(element[1][0] <= 430000):
                        row = np.concatenate((row, ["1"]), axis = None)
                    else:
                        row = np.concatenate((row, ["0"]), axis = None)
                    currentWriter.writerow(row)
            
                del problem
                del algorithm
                del resultsList
                del res
                del currentWriter
            
                f = open(".savestate", 'w')
                f.write(f"{seedRound}\n")
                f.write(f"{mutationRate}\n")
                f.write(f"{crossoverRate}\n")
                f.write(f"{populationSize}\n")
                f.write(f"{currentAlgorithm}\n")
                f.write(f"{seed}\n")
                f.close()

    else:
        currentAlgorithm = selectedAlgorithm
        # problem = EPANETProblem(counter = counter, elementwise_runner = runner)
        problem = EPANETProblem(counter = counter)

        print(currentAlgorithm)

        algorithm = AlgorithmSelection.SelectAlgorithm(name = currentAlgorithm, pop_size = populationSize, samp = sampling, co = crossover, mt = mutation, no = n_objectives, nd = n_dimensions, rd = ref_dirs)

        currentAlgoStart = time.time()

        res = minimize(problem, algorithm, stop_criteria, seed = seed, verbose = False)

        currentAlgoEnd = (time.time() - start)

        if not os.path.exists(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}"): 
            os.makedirs(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}")

        currentWriter = csv.writer(open(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}/{seed}.csv", 'w', encoding = "utf-8"))
        currentWriter.writerow([currentAlgorithm])
        currentWriter.writerow(["Seed", seed])
        currentWriter.writerow(["Generations", generations])
        currentWriter.writerow(["Population size", populationSize])
        currentWriter.writerow(["Crossover chance", crossoverRate])
        currentWriter.writerow(["Mutation chance", mutationRate])
        successes = 0
        for line in res.F:
            if (line[0] <= 430000):
                successes += 1
        currentWriter.writerow(["Successes", successes])
        currentWriter.writerow(["Overall successes", problem.overallSuccesses])
        currentWriter.writerow(["Quality(success rate)", successes/len(res.F)])
        currentWriter.writerow(["Overall quality(success rate)", (problem.overallSuccesses)/(problem.counter)])
        if (counter == True):
            currentWriter.writerow(["Objective Function Calls", problem.counter])
            currentWriter.writerow(["Eficiency", (successes/len(res.F))/(problem.counter)])
        currentEndMin = int(currentAlgoEnd/60)
        currentWriter.writerow(["Minutes", currentEndMin, "Seconds", currentAlgoEnd - (currentEndMin * 60)])

        minimumCost:int = 1000000000
        maximumRI:int = 0
        for line in res.F:
            if (line[0] < minimumCost):
                minimumCost = line[0]
            if ((line[1])*(-1) > maximumRI):
                maximumRI = (line[1])*(-1)
        currentWriter.writerow(["Minimmum cost", minimumCost])
        currentWriter.writerow(["Maximum RI", maximumRI])

        currentWriter.writerow(diametersLabels + ["Cost", "SumRI"])
        resultsList = list(zip(res.X, res.F))
        for element in resultsList:
            element[1][1] = element[1][1]*(-1)
            row = np.concatenate((element[0], element[1]), axis = None)
            if(element[1][0] <= 430000):
                row = np.concatenate((row, ["1"]), axis = None)
            else:
                row = np.concatenate((row, ["0"]), axis = None)
            currentWriter.writerow(row)
    
        del problem
        del algorithm
        del resultsList
        del res
        del currentWriter
        
        f = open(".savestate", 'w')
        f.write(f"{seedRound}\n")
        f.write(f"{mutationRate}\n")
        f.write(f"{crossoverRate}\n")
        f.write(f"{populationSize}\n")
        f.write(f"{currentAlgorithm}\n")
        f.close()

    # pool.close()

if __name__ == '__main__':

    Config.warnings['not_compiled'] = False

    start = time.time()

    print("Running...")
    
    client = docker.from_env()
    client.images.build(path = "./EpanetDocker/", tag = "epanet-docker", rm = True, nocache = False)
    
    
    saveState = os.path.isfile(".savestate")

    Loops.SeedLoop(Loops.PopulationLoop, Loops.MutationRateLoop, Loops.CrossoverRateLoop, ExecuteAlgorithms)

    end = (time.time() - start)
    endmin = int(end/60)
    print("Time: ", endmin, " minutes and ", end - (endmin * 60), " seconds")
    
    if os.path.exists(".savestate"):
        os.remove(".savestate")