# from threading import Lock
from threading import Semaphore

# lock = Lock()

counterSemaphore = Semaphore(1)

numberOfThreads:int

def initialize():
    global numberOfThreads
    global availablePorts
    availablePorts = []
    currentPort = 0
    numberOfThreads = 100
    for i in range(numberOfThreads):
        availablePorts.append(9000 + i)


