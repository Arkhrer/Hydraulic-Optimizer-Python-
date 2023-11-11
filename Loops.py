import time

from Main import saveState

seedRounds = 30
populationRounds = 3
mutationRateRounds = 3
crossoverRateRounds = 3

def SeedLoop(NextFunction, *args, **kwargs):
    for i in range(seedRounds):
        if(saveState):
            f = open(".savestate",'r')
            content = f.readlines()
            seed = int(content[5])
        else:
            seed = int(time.time())
        NextFunction(*args, **kwargs, seed = seed, seedRound = i)

def PopulationLoop(NextFunction, *args, **kwargs):
    populationSize = 1
    for i in range(populationRounds):
        populationSize *= 10
        NextFunction(*args, **kwargs, populationSize = populationSize)

def MutationRateLoop(NextFunction, *args, **kwargs):
    for i in range(mutationRateRounds):
        mutationRate = 0.01 + 0.045 * i
        NextFunction(*args, **kwargs, mutationRate = round(mutationRate, 3))

def CrossoverRateLoop(NextFunction, *args, **kwargs):
    for i in range(crossoverRateRounds):
        crossoverRate = 0.1 + 0.4 * i
        NextFunction(*args, **kwargs, crossoverRate = round(crossoverRate, 3))


def PrintOk(**kwargs):
    for key, value in kwargs.items():
        print(f"key: {key}\tvalue: {value}")

if __name__ == "__main__":
    SeedLoop(PopulationLoop,MutationRateLoop,CrossoverRateLoop,PrintOk)