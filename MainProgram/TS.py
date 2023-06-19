import TP
import FO
import random
from datetime import datetime


Problem = TP.TesteProb()

class TesteSol():
    def __init__(self):
        random.seed(datetime.now().timestamp())
        self.X = []
        v = []
        for i in range(Problem.NumberOfVariables):
            self.X.append(random.randint(Problem.Xmin[i], Problem.Xmax[i]))
            v.append(self.X[i])
        
        fitness1: float
        fitness2: float
        fitness1, fitness2 = FO.FuncaoObjetivo(v)

        self.ObjectiveValues = []

        self.ObjectiveValues.append(fitness1)
        self.ObjectiveValues.append(fitness2)

if __name__ == '__main__':
    teste = TesteSol()
    print (teste.ObjectiveValues[0], " ", teste.ObjectiveValues[1])