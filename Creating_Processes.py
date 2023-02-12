import time
import multiprocessing
from multiprocessing import Process


def do_work(process_name, count):
    print("Comienza el trabajo por el {}".format(process_name))
    i = 0
    for _ in range(count):
        i += 1
    print("{} terminó de contar hasta {}".format(process_name, count))


def count_to_n_number(num_processes):
    processes = []
    count = 20000000

    for i in range(num_processes):
        process_name = "hilo {}".format(i + 1)
        process = Process(target=do_work, args=(process_name, count))
        processes.append(process)
        process.start()


    for process in processes:
        process.join()

    print("Todos los hilos han terminado.")


if __name__ == '__main__':
    Proceso = [1, 2, 4, 8, 16, 32, 64]
    Tiempo = []
    multiprocessing.set_start_method('spawn')

    for i in range(7):
        start = time.time()
        count_to_n_number(Proceso[i])
        end = time.time()
        Tiempo.append(end - start)
        print(f"Tiempo de ejecucion con {Proceso[i]} proceso tomo {end - start} segundos\n")

    for i in Tiempo:
        print('-', i)
