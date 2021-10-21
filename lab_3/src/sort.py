# Сортировка пузырьком
def bubble_sort(array):
    N = len(array)
    for i in range(N - 1):
        for j in range(N - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = \
                    array[j + 1], array[j]
    return array

# Сортировка вставками
def insertion_sort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >=0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key 
    return array

# Сортировка выбором
def select_sort(array):
    N = len(array)
    for i in range(N):
        minIndex = i
        for j in range(i, N):
            if (array[j] < array[minIndex]):
                minIndex = j
        array[i], array[minIndex] = \
            array[minIndex], array[i]
    
    return array