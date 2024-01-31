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
    global saveState
    saveState = False
    threadState = {}
    dockers = {}
    availablePorts = []
    currentPort = 0
    numberOfThreads = 50
    for i in range(numberOfThreads * 2):
        availablePorts.append(4000 + i)


