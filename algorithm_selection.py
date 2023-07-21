from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.algorithms.moo.unsga3 import UNSGA3
from pymoo.operators.crossover.sbx import SBX
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.mutation.pm import PM

def select_algorithm(name):
    population_size = 200
    sampling = IntegerRandomSampling()
    crossover = SBX(prob = 0.8, vtype = int)
    mutation = PM(prob = 0.050, vtype = int)

    n_objectives = 2
    n_dimensions = n_objectives
    n_partitions = 12
    # n_points = factorial(n_objectives + n_partitions - 1)/(factorial(n_objectives + n_partitions - 1)*factorial(n_partitions))
    ref_dirs = get_reference_directions("das-dennis", n_dimensions, n_partitions=n_partitions, seed = 1)

    REF = {
        "NSGA2": NSGA2,
        "NSGA3": NSGA3,
        "UNSGA3": UNSGA3
    }

    if name not in REF:
        raise Exception("Reference directions factory not found.")

    if name.endswith("NSGA3"):

        return REF[name](ref_dirs = ref_dirs, pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    else:
        return REF[name](pop_size = population_size, sampling = sampling, crossover = crossover, mutation = mutation)
    