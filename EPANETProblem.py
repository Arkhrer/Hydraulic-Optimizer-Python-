from pymoo.core.problem import Problem
from pymoo.core.problem import ElementwiseProblem
from typing import final
from epyt import epanet
import random
from datetime import datetime
from multiprocessing.pool import ThreadPool
import threading
import numpy as np
from UDPClient import UDPclient
from TCPServer import TCPserver

import Globals

# from PortHandler import lock


NUMBEROFPIPES: final = 8

# pool = ThreadPool(5)

class EPANETProblem(ElementwiseProblem):
    def __init__(self, counter = False, **kwargs):
        self.Xmin = []
        self.Xmax = []
        self.NumberOfVariables = NUMBEROFPIPES
        self.allowcounter = counter
        self.overallSuccesses = 0
        if self.allowcounter == True:
            self.counter = 0

        for i in range(self.NumberOfVariables):
            self.Xmin.append(0)
            self.Xmax.append(13)

        super().__init__(n_var = self.NumberOfVariables, n_obj = 2, xl = self.Xmin, xu= self.Xmax, vtype = int, **kwargs)

    def _evaluate(self, X, out, *args, **kwargs):
    # Monothread solution

        # res = []

        # for design in X:
        #     if self.allowcounter == True:
        #         self.counter = self.counter + 1
                
                
        #     client = docker.from_env()
        #     diameter_pattern:str = "" + str(design[0])
        #     for i in range(1, len(design)):
        #         diameter_pattern+="," + str(design[i])
                
        #     result = str(client.containers.run("epanet-docker", "app/ObjectiveFunction.py", environment = [f"DIAMETER_PATTERN={diameter_pattern}"]), encoding = "utf-8").split()
            
        #     print(self.counter)
            
        #     currentRes = [float(result[0]), float(result[1])]
            
        #     res.append(currentRes)
            
        #     if (res[len(res) - 1][0] <= 430000):
        #         self.overallSuccesses += 1

        # out["F"] = np.array(res)

    # Multithread solution

        diameter_pattern:str = "" + str(X[0])
        for i in range(1, len(X)):
            diameter_pattern+="," + str(X[i])
            
        # result = str(client.containers.run("epanet-docker", "app/ObjectiveFunction.py", environment = [f"DIAMETER_PATTERN={diameter_pattern}"], auto_remove = True), encoding = "utf-8").split()

        Globals.counterSemaphore.acquire()

        thisPort = Globals.availablePorts.pop(0)

        Globals.counterSemaphore.release()

        # ENVIAR SINAL COMO CLIENTE UDP
        UDPclient("localhost", thisPort, diameter_pattern)

        # ABRIR SERVIDOR TCP QUE ESPERA A RESPOSTA
        result = TCPserver("localhost", thisPort + 500).split(' ')


        Globals.counterSemaphore.acquire()

        Globals.availablePorts.append(thisPort)

        Globals.counterSemaphore.release()
                
        currentRes = [float(result[0]), float(result[1])]
            
        if (currentRes[0] <= 430000):
            self.overallSuccesses += 1
        
        if self.allowcounter == True:
            self.counter = self.counter + 1
            # print(self.counter)

        out["F"] = currentRes
