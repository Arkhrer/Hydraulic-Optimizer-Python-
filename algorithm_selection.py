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
# from math import factorial

REF = {
        "AGEMOEA2": AGEMOEA2,
        "SMSEMOA": SMSEMOA,
        "AGEMOEA": AGEMOEA,
        "UNSGA3": UNSGA3,
        "RNSGA3": RNSGA3,
        "NSGA2": NSGA2,
        "NSGA3": NSGA3,
        "MOEAD": MOEAD,
        "CTAEA": CTAEA,
        "RVEA": RVEA
    }

def select_algorithm(name):
    #Parameters
    population_size = 10
    sampling = IntegerRandomSampling()
    crossover = SBX(prob = 0.8, vtype = int)
    mutation = PM(prob = 0.050, vtype = int)

    n_objectives = 2
    n_dimensions = n_objectives
    # n_points = factorial(n_objectives + n_partitions - 1)/(factorial(n_objectives + n_partitions - 1)*factorial(n_partitions))
    ref_dirs = get_reference_directions("das-dennis", n_dimensions, n_partitions = 12, seed = 1)

    if name not in REF:
        raise Exception("Reference directions factory not found.")

    if name == "NSGA3" or name == "UNSGA3":
        return REF[name](ref_dirs = ref_dirs, pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    elif name == "RNGSA3":
        # Uncertain about parameters
        return REF[name](ref_dirs = ref_dirs, pop_per_ref_point = 20, mu = 0.1, sampling = sampling, crossover = crossover, mutation = mutation)
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