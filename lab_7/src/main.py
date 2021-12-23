from time import process_time, process_time_ns
import matplotlib.pyplot as plt 

def print_value(dict, count):
    print('-' * 20)
    print("Найден человек с таким паспортом: ")
    print(list(dict.items())[count])

def full_search(dict, find_key, output = True):
    count = 0
    result = -1
    for key in dict.keys():
        if key == find_key:
            result = 0
            if (output):
                print_value(dict, count)
            break
        else:
            count += 1
    if (result == -1):
        count = -1
    return count

def sort_dict(my_dict):
    keys = list(my_dict.keys())
    keys.sort()

    tmp_dict = dict()

    for key in keys:
        tmp_dict[key] = my_dict[key]

    return tmp_dict

def binary_search(sort_dict, find_key, output = True):
    count = 0
    result = -1

    keys = list(sort_dict.keys())

    left = 0 
    right = len(keys) - 1
    middle = len(keys) // 2
    while (left <= right):
        count += 1

        key = keys[middle]
        if (key == find_key):
            if (output):
                print_value(sort_dict, middle)
            result = 0
            break

        elif (key < find_key):
            left = middle + 1
        else:
            right = middle - 1
        middle = (left + right) // 2
    if (result == -1):
        count = -1
    return count

def sort_value(my_dict):
    sorted_dict = dict()

    items = list(my_dict.items())
    items.sort(key = lambda k: k[1], reverse = True)

    for elem in items:
        sorted_dict[elem[0]] = elem[1]

    return sorted_dict

def make_segments(my_dict):
    temp_dict = {i: 0 for i in "0123456789"}

    for key in my_dict:
        temp_dict[key[0]] += 1

    # Получаем словарь, в котором самые часто встречаемые первые буквы ключа идут по убыванию
    temp_dict = sort_value(temp_dict)

    # В том же порядке создаём ключ
    segmented_dict = {i: dict() for i in temp_dict}

    # Проходим по словарю и добавляем в новый словарь по ключу - первая буква
    for key in my_dict:
        segmented_dict[key[0]].update({key: my_dict[key]})
    
    for key in segmented_dict:
        segmented_dict[key] = sort_dict(segmented_dict[key])

    return segmented_dict

    
def segment_search(segmented_dict, key, output = True):
    count = 0
    keys = list(segmented_dict.keys())
    for key_letter in keys:
        count += 1
        if (key[0] == key_letter):
            count_search = binary_search(segmented_dict[key_letter], key, output)
            if (count_search == -1):
                count = -1
            else:
                count += count_search
            break
    return count

def load_csv(filename):
    file = open(filename, "r")

    data = []
    file.readline()
    for line in file.readlines():
        tmp = line.replace("\n", ",").split(",")[1:5]
        data.append(tmp)

    file.close()

    global_dict = {}
    for i in range(len(data)):
        key = data[i][0]
        value = [data[i][1], data[i][2], data[i][3]]

        global_dict[key] = value
    return global_dict

def process_full_search(global_dict):
    find_key = input("Введите ключ для поиска: ")
    result = full_search(global_dict, find_key)
    print(result)
    if (result == -1):
        print("Ключ не был обнаружен")

def process_binary_search(global_dict):
    find_key = input("Введите ключ для поиска: ")
    sorted_dict = sort_dict(global_dict)
    result = binary_search(sorted_dict, find_key)
    print(result)
    if (result == -1):
        print("Ключ не был обнаружен")

def process_segment_search(global_dict):
    find_key = input("Введите ключ для поиска: ")
    segmented_dict = make_segments(global_dict)
    result = segment_search(segmented_dict, find_key)
    print(result)
    if (result == -1):
        print("Ключ не был обнаружен")

def process_print_dict(global_dict):
    keys = list(global_dict.keys())[:20]
    print("Первые 20 записей: ")
    for el in keys:
        print(el + ":", global_dict[el])

def process_measure_time(global_dict):
    keys = list(global_dict.keys())
    X = list(range(len(keys)))
    full_search_time = []
    binary_search_time = []
    segment_search_time = []

    for i in range(len(keys)):

        tmp_full = 0
        tmp_binary = 0
        tmp_segm = 0
        sorted_dict = sort_dict(global_dict)
        segmented_dict = make_segments(global_dict)
        for j in range(30):
            start = process_time_ns()
            full_search(global_dict, keys[i], output=False)
            tmp_full += (process_time_ns() - start)

            start = process_time_ns()
            binary_search(sorted_dict, keys[i], output=False)
            tmp_binary += (process_time_ns() - start)

            start = process_time_ns()
            segment_search(segmented_dict, keys[i], output=False)
            tmp_segm += (process_time_ns() - start)
        
        tmp_full /= 30
        tmp_binary /= 30
        tmp_segm /= 30
        
        full_search_time.append(tmp_full)
        binary_search_time.append(tmp_binary)
        segment_search_time.append(tmp_segm)
    
    plt.plot(X, full_search_time, label = "Поиск полным перебором")
    plt.plot(X, binary_search_time, label="Бинарный поиск")
    plt.plot(X, segment_search_time, label="Поиск сегментами")

    plt.legend()
    plt.grid()
    plt.title("Временные характеристики")
    plt.ylabel("Затраченное время (нс)")
    plt.xlabel("Индекс ключа")
    
    plt.show()

    

def print_menu():
    print('-' * 20)
    print("Меню работы со словарём: номер паспорта - ФИО человека")
    print("1 - поиск по ключу полным перебором")
    print("2 - поиск по ключу бинарным поиском")
    print("3 - поиск по ключу с помощью сегментов")
    print("4 - сравнение по поиску")
    print("5 - вывести первые 20 элементов словаря (всего - 20000)")
    print("0 - выход\n")

def run(global_dict):
    res = -1
    while (res != 0):
        print_menu()
        try:
            res = int(input("Выбор: "))
            if (res == 1):
                process_full_search(global_dict)
            elif (res == 2):
                process_binary_search(global_dict)
            elif (res == 3):
                process_segment_search(global_dict)
            elif (res == 4):
                process_measure_time(global_dict)
            elif (res == 5):
                process_print_dict(global_dict)
            elif (res == 0):
                exit()
            else:
                print("Такого пункта в меню нет :(")
        except ValueError:
            print("Ввод был осуществлён некорректно!")
    

global_dict = load_csv("table_drivers.csv")
run(global_dict)
