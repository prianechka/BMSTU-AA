from itertools import permutations
from random import random, sample
from time import process_time_ns
import numpy as np

# Полный перебор
def full_research(matrix, size):
    
    all_combinations = permutations(range(size))
    min_dist = float("inf")
    best_way = []
    for combination in all_combinations:
        combination = list(combination)
        combination.append(combination[0])
        sum = 0
        for i in range(size):
            sum += matrix[combination[i]][combination[i + 1]]
        if (sum < min_dist):
            min_dist = sum
            best_way = combination
    
    print("Полный перебор: ")
    print("Минимальный путь: ", best_way)
    print("Его длина: ", min_dist)

def create_promixity_table(matrix, size):
    promixity_table = [[0] * size for i in range(size)]
    for i in range(size):
        for j in range(size):
            if (matrix[i][j] != 0):
                promixity_table[i][j] = 1 / matrix[i][j]
            else:
                promixity_table[i][j] = 0
    return promixity_table

def count_wishes_table(promixity_table, size, a, b, pheromon_table):
    wishes_table =  [[0] * size for i in range(size)]

    for i in range(size):
        for j in range(size):
            wishes_table[i][j] = pow(promixity_table[j][i], a) * pow(pheromon_table[j][i], b)
    
    return wishes_table
    

def count_all_possibity_ant(wishes_table, current_city, size, root):
    result_possibilities = []

    for i in range(size):
        if i in root:
            result_possibilities.append(0)
        else:
            current_prob = wishes_table[current_city][i]
            result_possibilities.append(current_prob)
    
    sum_probs = sum(result_possibilities)
    
    if (sum_probs != 0):
        for i in range(size):
            result_possibilities[i] /= sum_probs
    
    return result_possibilities

def count_way(matrix, root):
    N = len(root) - 1
    sum_way = 0

    for i in range(N):
        sum_way += matrix[root[i]][root[i + 1]]
    
    return sum_way
    

def ant_iteration(promixity_table, size, a, b, q, p, pheromon_table, min_route, len_min_route, matrix):

    wishes_table = count_wishes_table(promixity_table, size, a, b, pheromon_table)
    pheromon_adds = [[0] * size for i in range(size)]

    for i in range(size):
        route = [i]
        for j in range(size - 1):
            temp_probs = count_all_possibity_ant(wishes_table, route[-1], size, route)

            prob = random()
            temp_sum = 0
            k = 0
            while k < size:
                if (temp_probs[k] != 0):
                    temp_sum += temp_probs[k]
                    if (temp_sum > prob):
                        break
                k += 1
            if (k == size):
                k = size - 1
            route.append(k)
        
        route.append(route[0])

        route_len = count_way(matrix, route)
        if (route_len < len_min_route):
            len_min_route = route_len
            min_route = route

        for v in range(size):
            pheromon_adds[route[v]][route[v + 1]] += q / route_len
    
    for i in range(size):
        for j in range(size):
            pheromon_table[i][j] *= (1 - p)
            pheromon_table[i][j] += pheromon_adds[i][j]
    
    return pheromon_table, min_route, len_min_route

def ant(matrix, size, a, b, q, p, time):
    promixity_table = create_promixity_table(matrix, size)
    pheromon_table = [[0.2] * size for i in range(size)]
    min_route = []
    len_min_route = float("inf")

    for i in range(time):
        pheromon_table, min_route, len_min_route = ant_iteration(promixity_table, size, a, b, q, p, pheromon_table, min_route, len_min_route, matrix)
    
    # print("Муравьиный алгоритм: ")
    print("Минимальный путь: ", min_route)
    print("Его длина: ", len_min_route)

    return len_min_route

def read_file_matrix(file_name):

    file = open("data/" + file_name, "r")
    size = len(file.readline().split())
    file.seek(0)

    matrix = [[0] * size for i in range(size)]
    
    i = 0

    for line in file.readlines():
        j = 0

        for num in line.split():
            matrix[i][j] = int(num)
            j += 1

        i += 1

    file.close()

    return matrix, size

def generate_matrix(size):

    A = np.random.randint(1, 300, (size, size))

    for i in range(size):
        for j in range(size):
            if i == j:
                A[i][j] = 0
            elif j > i:
                A[i][j] = A[j][i]

    filename = "data/mtr.txt"  
    f = open(filename, 'w')
    for i in range(size):
        for j in range(size):
            f.write(str(A[i][j]))
            f.write(" ")
        f.write("\n")

    f.close() 



def demonstrate():
    filename = input("Введите файл, в котором лежит матрица расстояний между городами: ")
    try:
        matrix, size = read_file_matrix(filename)
        print('-'* 100)
        print("Исходная матрица: ")
        for i in range(size):
            for j in range(size):
                print(matrix[i][j], end = " ")
            print()
        print('-'* 100)
        full_research(matrix, size)
        print('-'* 100)
        a = float(input("Введите параметр alpha для муравьиного алгоритма: "))
        b = float(input("Введите параметр beta для муравьиного алгоритма: "))
        q = float(input("Введите параметр Q для муравьиного алгоритма: "))
        p = float(input("Введите параметр p для муравьиного алгоритма: "))
        t_max = int(input("Введите максимальное число итераций для муравьиного алгоритма: "))
        print('-' * 100)
        ant(matrix, size, a, b, q, p, t_max)
    
    except:
        print("Возникла ошибка ввода!")

def time():
    a = 1
    b = 1
    q = 10
    p = 0.5
    t_max = 1000

    search = []
    ant_ = []
    X = range(2, 12, 1)
    for _size in X:
        generate_matrix(_size)
        filename = "mtr.txt"
        matrix, size = read_file_matrix(filename)
        tm = process_time_ns()
        full_research(matrix, size)
        search.append(process_time_ns() - tm)

        tm = process_time_ns()
        ant(matrix, size, a, b, q, p, t_max)
        ant_.append(process_time_ns() - tm)

    for i in range(len(search)):
        print(X[i], search[i], ant_[i])


def check_params():
    alpha = [1, 2, 3]
    beta = [1, 2, 3]
    Q = [1, 3, 5, 10]
    p = 0.5
    t_max = [10, 100, 1000]

    # generate_matrix(14)
    filename = "mtr.txt"
    matrix, size = read_file_matrix(filename)

    f = open("result.txt", "w")

    for a in alpha:
        for b in beta:
            for q in Q:
                for t in t_max:
                    f.write(str(a) + " & " + str(b) + " & " + str(q) + " & " + str(p) + " & " + str(t))
                    ex = ant(matrix, size, a, b, q, p, t)
                    f.write(" & " + str(ex) + " & " + str(ex- 592) + " \\ " + "\n")
    f.close()

demonstrate()
                        



