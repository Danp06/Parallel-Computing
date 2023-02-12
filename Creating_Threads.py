import time
from threading import Thread


def do_work(thread_name, count):
    print("Comienza el trabajo por el {}".format(thread_name))
    i = 0
    for _ in range(count):
        i += 1
    print("{} terminó de contar hasta {}".format(thread_name, count))


def count_to_n_number(num_threads):
    threads = []
    count = 20000000

    for i in range(num_threads):
        thread_name = "hilo {}".format(i + 1)
        thread = Thread(target = do_work, args = (thread_name, count))
        threads.append(thread)
        thread.start()


    for thread in threads:
        thread.join()

    print("Todos los hilos han terminado.")



Hilos = [1, 2, 4, 8, 16, 32, 64]
Tiempo = []

for i in range(7):
    start = time.time()
    count_to_n_number(Hilos[i])
    end = time.time()
    Tiempo.append(end - start)
    print(f"Tiempo de ejecucion con {Hilos[i]} hilo tomo {end - start} segundos\n")

for i in Tiempo:
    print('-', i)
