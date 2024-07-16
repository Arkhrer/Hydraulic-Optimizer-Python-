# from threading import Lock
from threading import Semaphore

# lock = Lock()

counterSemaphore = Semaphore(1)

def initialize():
    global NUMBER_OF_PIPES
    global threadState
    global dockers
    global numberOfThreads
    global availablePorts
    global client
    global saveState
    global AVAILABLE_DIAMETERS

    AVAILABLE_DIAMETERS = 6

    NUMBER_OF_PIPES = 34

    saveState = False
    threadState = {}
    dockers = {}
    availablePorts = []
    currentPort = 0
    numberOfThreads = 50
    for i in range(numberOfThreads * 2):
        availablePorts.append(8000 + i)


