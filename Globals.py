# from threading import Lock
from threading import Semaphore

# lock = Lock()

counterSemaphore = Semaphore(1)

def initialize():
    global threadState
    global dockers
    global numberOfThreads
    global availablePorts
    global client
    threadState = {}
    dockers = {}
    availablePorts = []
    currentPort = 0
    numberOfThreads = 100
    for i in range(numberOfThreads):
        availablePorts.append(9000 + i)


