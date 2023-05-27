import TP
import time

if __name__ == '__main__':

    start = time.time()

    print("\nRodando...")

    time.sleep(1)

    print("\nTempo: ", (time.time() - start), " segundos")
    print("\n", TP.Problem.n_populacao)