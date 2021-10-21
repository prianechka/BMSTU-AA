from time import process_time_ns
from sort import select_sort, insertion_sort, bubble_sort
from random import choices
import matplotlib.pyplot as plt

def test_all(array):
    print("Начальный массив:          ", array)
    print("Отсортированный массив:    ", sorted(array))
    print()
    print("Сортировка пузырьком:      ", bubble_sort(array))
    print("Сортировка выбором:        ", select_sort(array))
    print("Сортировка вставками:      ", insertion_sort(array))

def test_equal(array, func):
    right_array = sorted(array)
    my_array = func(array)

    N = len(array)
    result = True
    for i in range(len(N)):
        if (my_array[i] != right_array[i]):
            result = False
            break
    
    return result

def measure_time(array, func, N):
    time = process_time_ns()
    for i in range(N):
        func(array[:])
    return (process_time_ns() - time) / N

def measure_time_all():
    N = [1, 5, 10, 20, 50, 75, 100, 250, 500, 1000]
    
    bubble_array = []
    select_array = []
    insert_array = []
    for n_elem in N:
        print(n_elem)
        array = choices(range(0, 1001, 1), k = n_elem)
        # array = list(range(n_elem))
        if n_elem < 100:
            k = 10000
        elif n_elem < 200:
            k = 1000
        elif n_elem < 500:
            k = 200
        else:
            k = 100
        bubble_array.append(measure_time(array, bubble_sort, k))
        select_array.append(measure_time(array, select_sort, k))
        insert_array.append(measure_time(array, insertion_sort, k))
    
    plt.semilogy(N, bubble_array, label = "Сортировка пузырьком")
    plt.semilogy(N, select_array, label = "Сортировка выбором")
    plt.semilogy(N, insert_array, label = "Сортировка вставками")

    plt.xlabel("Количество элементов")
    plt.ylabel("Время на сортировку (в нс)")
    plt.legend()
    plt.show()

    plt.xlabel("Количество элементов")
    plt.ylabel("Время на сортировку (в нс)")
    plt.plot(N, bubble_array, label = "Сортировка пузырьком")
    plt.plot(N, select_array, label = "Сортировка выбором")
    plt.legend()
    plt.show()

    return bubble_array, select_array, insert_array

def test_user():
    N = int(input("Введите размер массива: "))
    array = []
    for i in range(N):
        array.append(int(input("Введите элемент массива: ")))
    
    print("-" * 20)
    print("Начальный массив:          ", array)
    print("Отсортированный массив:    ", sorted(array))
    print("-" * 20)
    print("Сортировка пузырьком:      ", bubble_sort(array[:]))
    print("Сортировка выбором:        ", select_sort(array[:]))
    print("Сортировка вставками:      ", insertion_sort(array[:]))

# bubble_array, select_array, insert_array = measure_time_all()
# print(bubble_array)
# print(select_array)
# print(insert_array)

array = choices(range(-100, 100, 1), k = 12)
test_all(array)

# test_user()

