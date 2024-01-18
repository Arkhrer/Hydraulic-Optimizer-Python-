from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.algorithms.moo.rnsga3 import RNSGA3
from pymoo.algorithms.moo.age2 import AGEMOEA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.algorithms.moo.sms import SMSEMOA
from pymoo.algorithms.moo.age import AGEMOEA
from pymoo.algorithms.moo.moead import MOEAD
from pymoo.algorithms.moo.ctaea import CTAEA
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.moo.rvea import RVEA
from pymoo.operators.mutation.pm import PM
import numpy as np
# from math import factorial

REF = {
        #"AGEMOEA2": AGEMOEA2,
        #"SMSEMOA": SMSEMOA,
        #"AGEMOEA": AGEMOEA,
        "UNSGA3": UNSGA3,
        "RNSGA3": RNSGA3,
        "NSGA2": NSGA2,
        "NSGA3": NSGA3,
        "MOEAD": MOEAD,
        "CTAEA": CTAEA
        ,"RVEA": RVEA
    }

def SelectAlgorithm(name, pop_size = 10, samp = IntegerRandomSampling(), co = SBX(prob = 0.8, vtype = int), mt = PM(prob = 0.050, vtype = int), no = 2, nd = 2,  rd = get_reference_directions("das-dennis", 2, n_partitions = 10 - 1, seed = 1)):
    #Parameters
    population_size = pop_size
    sampling = samp
    crossover = co
    mutation = mt

    n_objectives = no
    n_dimensions = nd
    # n_points = factorial(n_objectives + n_partitions - 1)/(factorial(n_objectives + n_partitions - 1)*factorial(n_partitions))
    ref_dirs = rd
    ref_points = np.array([[0.1, 0.5], [0.7, 0.3], [0.5, 0.5]])

    if name not in REF:
        raise Exception("Reference directions factory not found.")

    if name == "NSGA3" or name == "UNSGA3":
        return REF[name](ref_dirs = ref_dirs, pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "RNSGA3":
        # Uncertain about parameters
        return REF[name](ref_points = ref_points, pop_per_ref_point = 20, mu = 0.1, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "NSGA2":
        return REF[name](pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "MOEAD":
        # Uncertain about parameters
        return REF[name](ref_dirs = ref_dirs, n_neighbors = 20, prob_neighbor_mating = 0.8, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "SMSEMOA":
        return REF[name](pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "AGEMOEA":
        return REF[name](pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "AGEMOEA2":
        return REF[name](pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "CTAEA":
        return REF[name](ref_dirs = ref_dirs, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "RVEA":
        return REF[name](ref_dirs = ref_dirs, pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)