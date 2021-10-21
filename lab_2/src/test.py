from time import process_time_ns
import matplotlib.pyplot as plt
from algs import classic, vinograd, optvinograd
from random import randint

def measure_func(matrix_1, matrix_2, func, N):
    tm = process_time_ns()
    for i in range(N):
        func(matrix_1, matrix_2)
    return ((process_time_ns() - tm) / N)

def measure_time():
    classic_time = []
    vinograd_time = []
    optvinograd_time = []
    # N = [1, 3, 5, 9, 15, 31, 51, 75, 101, 201, 401]
    N = [2, 4, 6, 10, 16, 30, 50, 76, 100, 200, 400]
    for n_elem in N:
        print(n_elem)
        matrix_1 = [[randint(-50, 50) for i in range(n_elem)] for j in range(n_elem)]
        matrix_2 = [[randint(-50, 50) for i in range(n_elem)] for j in range(n_elem)]

        k = 500
        if (n_elem > 20):
            k = 15
        if (n_elem > 100):
            k = 5
        if (n_elem > 150):
            k = 1
        classic_time.append(measure_func(matrix_1, matrix_2, classic, k))
        vinograd_time.append(measure_func(matrix_1, matrix_2, vinograd, k))
        optvinograd_time.append(measure_func(matrix_1, matrix_2, optvinograd, k))
    
    plt.title("Измерение времени для чётных N")
    plt.xlabel("Размер квадратной матрицы")
    plt.ylabel("Время работы в нс")
    plt.plot(N, classic_time, label = "classic")
    plt.plot(N, vinograd_time, label = "vinograd")
    plt.plot(N, optvinograd_time, label = "opt_vinograd")

    plt.legend()
    plt.show()
    return classic_time, vinograd_time, optvinograd_time

classic_time, vinograd_time, optvinograd_time = measure_time()
print(classic_time)
print(vinograd_time)
print(optvinograd_time)