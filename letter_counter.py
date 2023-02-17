import urllib.request
import time
from threading import Thread
import matplotlib.pyplot as plt


def count_letters_single(url, frequency, vocabulary):
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    for i in txt:
        letter = i.lower()
        if letter in frequency:
            frequency[letter] += 1
        # Con esta condicion si no encuentra un caracter que este en el vocabulario lo agrega
        # y comienza la contar su frecuencia con la exepcion que que no sea un espacio.
        elif letter not in vocabulary and letter != " ":
            frequency[letter] = 1

finished_count = 0

def count_letters_threads(url, frequency, vocabulary):
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    for i in txt:
        letter = i.lower()
        if letter in frequency:
            frequency[letter] += 1
        # Con esta condicion si no encuentra un caracter que este en el vocabulario lo agrega
        # y comienza la contar su frecuencia con la exepcion que que no sea un espacio.
        elif letter not in vocabulary and letter != " ":
            frequency[letter] = 1
    global finished_count
    finished_count += 1


def work_single():
    frequency = {}
    vocabulary = "abcdefghijklmnopqrstuvwxyz1234567890"
    for c in vocabulary:
        frequency[c] = 0
    start = time.time()
    # Mi codigo es 59772, debido a que en los documentos no se encuentra el rango entre 9772 y 9792
    # use el siguiente rango entre 5977 y 5997
    for i in range(5977, 5997):
        count_letters_single(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency, vocabulary)
    end = time.time()
    timefinal = end - start

    return frequency, timefinal


def work_threads():
    frequency = {}
    vocabulary = "abcdefghijklmnopqrstuvwxyz1234567890"
    for c in vocabulary:
        frequency[c] = 0
    start = time.time()
    # Mi codigo es 59772, debido a que en los documentos no se encuentra el rango entre 9772 y 9792
    # use el siguiente rango entre 5977 y 5997
    for i in range(5977, 5997):
        Thread(target = count_letters_threads,
               args = (f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency, vocabulary)).start()
    while True:
        if finished_count == 20:
            break
    time.sleep(0.2)
    end = time.time()
    timefinal = end - start

    return frequency, timefinal


def graphic(frequency, total):
    # Se crean dos listas donde se encuentran las letras y las frecuencias
    letters = []
    frequencies = []

    print("Frecuencia de cada caracter normalizado (porcentaje)")
    # Se está recorriendo el diccionario frequency con un bucle for y, para cada par de clave-valor en el diccionario,
    # está calculando la frecuencia normalizada y multiplicándolo por 100 para expresarlo como porcentaje y
    # agregándola a las listas letters y frequencies.
    for letter, count in frequency.items():
        letters.append(letter)
        frequencies.append(((count / total) * 100))
        print(f"{letter}: {(count / total) * 100:.3f}%")

    # Se crea un grafico
    plt.bar(letters, frequencies)

    plt.title('Frecuencia de letras')
    plt.xlabel('Letras')
    plt.ylabel('Frecuencia normalizada')

    plt.xticks(fontsize = 6)
    plt.show()


def main():
    # Se declaran como variables globales frequency_single y frequency_threads para acceder a ellas, adicionalmente
    # se crean dos listas para cada uno de los procesos con el objetivo de medir los tiempos y obtener un promedio
    global frequency_single, frequency_threads
    times_single = []
    times_threads = []
    # Se itera 30 veces y se obtiene lo tiempos para cada uno de los procesos.
    for i in range(30):
        global finished_count
        finished_count = 0
        frequency_single, timefinal_single = work_single()
        frequency_threads, timefinal_threads = work_threads()
        times_single.append(timefinal_single)
        times_threads.append(timefinal_threads)

    # Calculamos los promedios
    average_time_single = sum(times_single) / len(times_single)
    average_time_threads = sum(times_threads) / len(times_threads)
    # Calculamos el speed up
    speed_up = average_time_single / average_time_threads
    # Calculamos la sumatoria de todas las frecuencias para cada caracter
    total = sum(frequency_threads.values())
    # Se llama la funcion graphic para obtener el diagrama de barra
    graphic(frequency_threads, total)

    print("El tiempo promedio del conteo en serie es: ", average_time_single)
    print("El tiempo promedio del conteo en paralelo es: ", average_time_threads)
    print(f"Hubo un speed up de {speed_up:.3} lo que indica que el conteo en paralelo fue "
          f"{speed_up:.3} mas rapido.")


main()
