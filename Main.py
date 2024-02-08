# from pymoo.core.problem import StarmapParallelization
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from EPANETProblem import EPANETProblem
from pymoo.optimize import minimize
import matplotlib.pyplot as plt
from pymoo.config import Config
import AlgorithmSelection
import numpy as np
import docker
import random
import Loops
import time
import csv
import os
import gc

import Globals
from UDPClient import UDPclient


#Parallelization
from multiprocessing.pool import ThreadPool
# import multiprocessing
from pymoo.core.problem import StarmapParallelization

# diametersLabels = []
# for it in range(8):
#     diametersLabels += [f"Diameter {it + 1}"]

allOfThem: bool = True
selectedAlgorithm: str = "RVEA"

counter: bool = True

NUMBER_OF_PIPES = 8

#Parameters

sampling = IntegerRandomSampling()
generations = 1000
stop_criteria = ('n_gen', generations)

n_objectives = 2
n_dimensions = n_objectives

currentRound = 0

def SingleExecution(seed, populationSize, mutationRate, mutation, crossoverRate, crossover, currentAlgorithm, runner, ref_dirs, seedRound):
    global counter
    global n_objectives
    global n_dimensions
    global sampling
    # global diametersLabels
    global generations
    global stop_criteria
    global NUMBER_OF_PIPES

    # CRIAR N(NUMERO DE THREADS) DOCKERS QUE ABRIRÃO SERVIDORES UDP

    for i in range(2 * Globals.numberOfThreads):
        Globals.dockers[Globals.availablePorts[i]] = Globals.client.containers.run("epanet-docker", "app/Main.py", mem_limit = "128m", network_mode = "host", environment = [f"PORT={Globals.availablePorts[i]}"], detach = True)

    time.sleep(5)
    
    problem = EPANETProblem(counter = counter, elementwise_runner = runner)

    print(currentAlgorithm)

    algorithm = AlgorithmSelection.SelectAlgorithm(name = currentAlgorithm, pop_size = populationSize, samp = sampling, co = crossover, mt = mutation, no = n_objectives, nd = n_dimensions, rd = ref_dirs)

    currentAlgoStart = time.time()

    res = minimize(problem, algorithm, stop_criteria, seed = seed, verbose = False)

    currentAlgoEnd = (time.time() - currentAlgoStart)

    # if not os.path.exists(f"results/{populationSize}_{crossoverRate}_{mutationRate}"): 
    #     os.makedirs(f"results/{populationSize}_{crossoverRate}_{mutationRate}")

    if not os.path.exists(f"results"): 
        os.makedirs(f"results")

    # currentWriter = csv.writer(open(f"results/{populationSize}_{crossoverRate}_{mutationRate}/{currentAlgorithm}.csv", 'w', encoding = "utf-8"))
    currentWriter = csv.writer(open(f"results/{currentAlgorithm}.csv", 'a', encoding = "utf-8"))
    
    # Labels
    
    labelsRow = np.concatenate(("Current algorithm", "Seed"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Generations"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Population size"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Crossover chance"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Mutation chance"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Successes"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Overall successes"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Quality(success rate)"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Overall quality(success rate)"), axis = None)
    
    if (counter == True):
        labelsRow = np.concatenate((labelsRow, "Objective Function Calls"), axis = None)
        labelsRow = np.concatenate((labelsRow, "Eficiency"), axis = None)
        
    labelsRow = np.concatenate((labelsRow, "Minutes"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Seconds"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Minimmum cost"), axis = None)
    labelsRow = np.concatenate((labelsRow, "Maximum RI"), axis = None)
    
    for i in range(len(res.X)):
        diametersLabels = []
        for it in range(NUMBER_OF_PIPES):
            diametersLabels += [f"Diameter {i} . {it + 1}"]
        labelsRow = np.concatenate((labelsRow, diametersLabels), axis = None)
        labelsRow = np.concatenate((labelsRow, ["Cost", "SumRI"]), axis = None)
        labelsRow = np.concatenate((labelsRow, "Success"), axis = None)
    
    currentWriter.writerow(labelsRow)
    
    #Values
    
    valuesRow = np.concatenate((currentAlgorithm, str(seed)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(generations)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(populationSize)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(crossoverRate)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(mutationRate)), axis = None)
    
    successes = 0
    for line in res.F:
        if (line[0] <= 430000):
            successes += 1
            
    valuesRow = np.concatenate((valuesRow, str(successes)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(problem.overallSuccesses)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(successes/len(res.F))), axis = None)
    valuesRow = np.concatenate((valuesRow, str((problem.overallSuccesses)/(problem.counter))), axis = None)
    if (counter == True):
        valuesRow = np.concatenate((valuesRow, str(problem.counter)), axis = None)
        valuesRow = np.concatenate((valuesRow, str((successes/len(res.F))/(problem.counter))), axis = None)
    currentEndMin = currentAlgoEnd // 60
    valuesRow = np.concatenate((valuesRow, str(currentEndMin)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(currentAlgoEnd - (currentEndMin * 60))), axis = None)
    
    minimumCost:int = 1000000000
    maximumRI:int = 0
    for line in res.F:
        if (line[0] < minimumCost):
            minimumCost = line[0]
        if ((line[1])*(-1) > maximumRI):
            maximumRI = (line[1])*(-1)
    
    valuesRow = np.concatenate((valuesRow, str(minimumCost)), axis = None)
    valuesRow = np.concatenate((valuesRow, str(maximumRI)), axis = None)
    
    resultsList = list(zip(res.X, res.F))
    for element in resultsList:
        element[1][1] = element[1][1]*(-1)
        row = np.concatenate((element[0], element[1]), axis = None)
        if(element[1][0] <= 430000):
            row = np.concatenate((row, ["1"]), axis = None)
        else:
            row = np.concatenate((row, ["0"]), axis = None)
        valuesRow = np.concatenate((valuesRow, row), axis = None)
    
    currentWriter.writerow(valuesRow)

    f = open(".savestate", 'w')
    f.write(f"{seedRound}\n")
    f.write(f"{mutationRate}\n")
    f.write(f"{crossoverRate}\n")
    f.write(f"{populationSize}\n")
    f.write(f"{currentAlgorithm}\n")
    f.write(f"{seed}\n")
    f.close()

    del problem
    del algorithm
    del resultsList
    del res
    del currentWriter
    del valuesRow
    del f
    del row

    for i in range(2 * Globals.numberOfThreads):
        UDPclient("127.0.0.1", Globals.availablePorts[i], "Exit")
        Globals.dockers[Globals.availablePorts[i]].kill()
        Globals.dockers[Globals.availablePorts[i]].remove(force = True)

    gc.collect()

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
    
    seed = kwargs["seed"]
    seedRound = kwargs["seedRound"]
    mutationRate = kwargs["mutationRate"]
    crossoverRate = kwargs["crossoverRate"]
    populationSize = kwargs["populationSize"]
    
    if(Globals.saveState):
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
    n_threads = Globals.numberOfThreads
    pool = ThreadPool(n_threads)
    #Processes
    # n_proccess = 100
    # pool = multiprocessing.Pool(n_proccess)
    
    runner = StarmapParallelization(pool.starmap)

    # --------------------------------------------- #

    ref_dirs = get_reference_directions("das-dennis", n_dimensions, n_partitions = populationSize - 1, seed = seed)

    mutation = PM(prob = mutationRate, vtype = int)

    crossover = SBX(prob = crossoverRate, vtype = int)

    currentRound += 1

    if(allOfThem):
        for currentAlgorithm in AlgorithmSelection.REF:
            if(Globals.saveState):
                f = open(".savestate",'r')
                content = f.readlines()
                if (currentAlgorithm != content[4][:-1]):
                    f.close()
                else:
                    f.close()
                    Globals.saveState = False
            else:
                SingleExecution(seed, populationSize, mutationRate, mutation, crossoverRate, crossover, currentAlgorithm, runner, ref_dirs, seedRound)

    else:
        currentAlgorithm = selectedAlgorithm
        Globals.saveState = False
        
        SingleExecution(seed, populationSize, mutationRate, mutation, crossoverRate, crossover, currentAlgorithm, runner, ref_dirs, seedRound)

    pool.close()


if __name__ == '__main__':

    Config.warnings['not_compiled'] = False

    Globals.initialize()
    
    Globals.client = docker.from_env()
    Globals.client.images.build(path = "./EpanetDocker/", tag = "epanet-docker", rm = True, nocache = False)

    # CRIAR N(NUMERO DE THREADS) DOCKERS QUE ABRIRÃO SERVIDORES UDP

    # for i in range(2 * Globals.numberOfThreads):
    #     Globals.dockers[Globals.availablePorts[i]] = Globals.client.containers.run("epanet-docker", "app/Main.py", mem_limit = "128m", network_mode = "host", environment = [f"PORT={Globals.availablePorts[i]}"], detach = True)

    # time.sleep(5)

    start = time.time()

    print("Running...")
    
    Globals.saveState = os.path.isfile(".savestate")

    Loops.SeedLoop(Loops.PopulationLoop, Loops.MutationRateLoop, Loops.CrossoverRateLoop, ExecuteAlgorithms)

    end = (time.time() - start)
    endmin = end // 60
    print("Time: ", endmin, " minutes and ", end - (endmin * 60), " seconds")
    
    if os.path.exists(".savestate"):
        os.remove(".savestate")

    # for i in range(2 * Globals.numberOfThreads):
    #     UDPclient("127.0.0.1", Globals.availablePorts[i], "Exit")
    #     Globals.dockers[Globals.availablePorts[i]].kill()
    #     Globals.dockers[Globals.availablePorts[i]].remove(force = True)