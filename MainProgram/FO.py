# from TP import Problem
import sys
from epyt import epanet

def FuncaoObjetivo(diameter_pattern):

    total_cost:int = 0
    sum_RI: float = 0.0
    A: float = 0.0
    B: float = 0.0
    Hmin: float = 10.0

    d = epanet('../EPANETSources/Alperovits_Shamir.inp')
    d.openHydraulicAnalysis()
    d.initializeHydraulicAnalysis(0)


    max1:int = sys.maxsize

    Nnodes = d.getNodeCount()
    Nlinks = d.getLinkCount()
    Nres_tanks = d.getNodeTankReservoirCount()
    Njunctions = Nnodes - Nres_tanks

    diameter = []
    pipe_cost = []

    finput = open('./Tabela_Custos.txt', 'rt')

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

    finput.close()

    for i in range(Nlinks):
        aux = diameter_pattern[i]
        diameter.append(diameter_base[aux])
        d.api.ENsetlinkvalue(i + 1, d.ToolkitConstants.EN_DIAMETER, diameter[i])
        pipe_length = d.api.ENgetlinkvalue(i + 1, d.ToolkitConstants.EN_LENGTH)
        pipe_cost.append(cost_base[aux]*pipe_length)
        total_cost += pipe_cost[i]
        
    # Hydraulic Analysis
    t = d.runHydraulicAnalysis()

    Warning6 = False
    
    for i in range(Njunctions):

        junction_pressure = d.api.ENgetnodevalue(i + 1, d.ToolkitConstants.EN_PRESSURE)

        if (junction_pressure < Hmin):
            Warning6 = True
            total_cost = 10000000.0
            sum_RI = 0.0
            print('Warning 6')
            break

        junction_demand = d.api.ENgetnodevalue(i + 1, d.ToolkitConstants.EN_DEMAND)
        aux1 = junction_demand * (junction_pressure-Hmin)
        A += aux1
        aux2 = junction_demand * Hmin
        B += aux2

    if (Warning6 == False):
        sum_RI = 100*(A / B)

    d.closeHydraulicAnalysis()

    d.saveHydraulicsOutputReportingFile()

    d.setReportFormatReset()
    d.setReport('FILE Output.rpt')
    d.setReport('STATUS YES')
    d.setReport('SUMMARY YES')
    d.setReport('MESSAGES YES')
    d.writeReport()

    d.unload()

    return total_cost, sum_RI
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

#     junction_pressure: float
#     junction_demant: float

    