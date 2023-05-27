# from TP import Problem
import sys
from epyt import epanet

def FuncaoObjetivo(diameter_pattern):
    d = epanet('EPANETSources/Alperovits_Shamir.inp')

    max1:int = sys.maxsize

    Nnodes = d.getNodeCount()
    Nlinks = d.getLinkCount()
    Nres_tanks = d.getNodeTankCount()
    Njunctions = Nnodes - Nres_tanks

    diameter = []
    pipe_cost = [Nlinks]

    finput = open('MainProgram/Tabela_Custos.txt', 'rt')

    number_diameters = int(finput.readline().split()[0])

    diameter_base = []
    cost_base = []


    next(finput)

    for line in finput:
        current = line.split()
        obs1 = current[0]
        obs2 = current[1]
        obs3 = current[2]

        diameter_base.append(float(obs2))
        cost_base.append(float(obs3))

    print(diameter_base)
    print(cost_base)
    print(number_diameters)

    finput.close()

    for i in range(Nlinks):
        aux = diameter_pattern[i]
        diameter.append(diameter_base[aux])
        #


#--------------------------------------------------

if __name__ == '__main__':
    FuncaoObjetivo()



# NumNodes: int
# Numtanks: int
# NumTanksEpanet: int
# NumLinks: int
# NumRes: int

# NetworkFile: str
# TypeObjective1: str
# TypeObjective2: str

# NumberofPumps: int
# NumberofTanks: int
# MinimumRange: int
# MaximumRange: int
# SimulationPeriod: int
# NumberofObjectives: int
# InitialPopulation: int
# Generations: int

# CrossoverProb: float
# MutationProb: float
# InitTaxTime: float
# FinTaxTime: float

# def InicializarProblema():
#     NetworkFile = "Alperovits_Shamir.inp"

#     NumberofObjectives = 2

#     InitialPopulation = 200
#     MutationProb = 0.050
#     CrossoverProb = 0.80
#     Generations = 1000

#     TP.Problem.n_populacao = InitialPopulation
#     TP.Problem.n_geracao = Generations

# def FuncaoObjetivo(diameter_pattern, FO1, FO2):
#     i: int
#     aux: int
#     obs1: float
#     obs2: float
#     obs3: float
#     max1:int = sys.maxsize

#     Nlinks: int

#     Nnodes: int
#     Nres_tanks: int
#     Njunctions: int

#     t: float

#     number_diameters: int
#     pipe_length: int
#     total_cost:int = 0

#     junction_pressure: float
#     junction_demant: float
#     sum_RI: float = 0.0
#     aux1: float
#     aux2: float
#     A: float = 0.0
#     B: float = 0.0
#     Hmin: float = 10.0
    