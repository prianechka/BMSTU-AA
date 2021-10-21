from time import process_time_ns

def levenshtein_rec(str_1, str_2):
    N1, N2 = len(str_1), len(str_2)
    if (N1 == 0) or (N2 == 0):
        return N1 + N2
    else:
        flag = int(str_1[N1 - 1] != str_2[N2 - 1])
        return min(
            levenshtein_rec(str_1[:N1 - 1], str_2) 
            + 1, 
            levenshtein_rec(str_1, str_2[:N2 - 1]) 
            + 1, 
            levenshtein_rec(str_1[:N1 - 1]
            , str_2[:N2 - 1]) + flag)

def levenshtein_rec_matrix(str_1, str_2):

    def recursion(str_1, str_2, matrix):
        N1, N2 = len(str_1), len(str_2)
        if matrix[N1][N2] == -1:
            if (N1 == 0) or (N2 == 0):
                matrix[N1][N2] = N1 + N2
            else:
                flag =int(str_1[N1 - 1] != str_2[N2 - 1])
                matrix[N1][N2] = min(
                            recursion(str_1[:N1-1],
                            str_2, matrix) + 1,
                            recursion(str_1, 
                            str_2[:N2-1], matrix) + 1,
                            recursion(str_1[:N1-1], 
                            str_2[:N2-1], matrix) + flag
                            )
        return matrix[N1][N2]
    
    N1, N2 = len(str_1), len(str_2)
    matrix = [[-1] * (N2 + 1) for i in range(N1 + 1)]
    result = recursion(str_1, str_2, matrix)
    print("Рекурсивный вариант (с матрицей) Левенштайна: {}".format(result))
    print("Итоговая матрица: ")
    for i in range(N1 + 1):
        for j in range(N2 + 1):
            print(" {} ".format(matrix[i][j]), end = '')
        print()
    return result

def levenshtein_not_rec(str_1, str_2):
    N1, N2 = len(str_1), len(str_2)
    array_1 = [i for i in range(N2 + 1)]
    array_2 = [1] + [0] * N2

    for i in range(1, N1 + 1):
        for j in range(1, N2 + 1):
            var1 = array_1[j] + 1
            var2 = array_2[j - 1] + 1
            var3 = array_1[j - 1]

            if (str_1[i - 1] != str_2[j - 1]):
                var3 += 1
            array_2[j] = min(var1, var2, var3)
        
        array_1, array_2 = array_2, [i + 1] + [0] * N2
    return array_1[N2]

def damerau_levenshtein(str_1, str_2):
    
    def recursion(str_1, str_2, matrix):
        N1, N2 = len(str_1), len(str_2)
        if matrix[N1][N2] == -1:
            if (N1 == 0) or (N2 == 0):
                matrix[N1][N2] = N1 + N2
            else:
                flag = int(str_1[N1 - 1] != str_2[N2 - 1])
                if (N1 > 1 and N2 > 1 and 
                    str_1[N1 - 2] == str_2[N2 - 1]
                    and str_1[N1 - 1] == str_2[N2 - 2]):
                    matrix[N1][N2] = min(
                                    recursion(str_1[:N1-1], 
                                    str_2, matrix) + 1,
                                    recursion(str_1, 
                                    str_2[:N2-1], matrix) + 1,
                                    recursion(str_1[:N1-1], 
                                    str_2[:N2-1], matrix)
                                    + flag, 
                                    recursion(str_1[:N1-2], 
                                    str_2[:N2-2], matrix) + 1)
                else:
                    matrix[N1][N2] = min(
                                    recursion(str_1[:N1-1],
                                    str_2, matrix) + 1,
                                    recursion(str_1, 
                                    str_2[:N2-1], matrix) + 1,
                                    recursion(str_1[:N1-1], 
                                    str_2[:N2-1], matrix)
                                    + flag)
        return matrix[N1][N2]
    
    N1, N2 = len(str_1), len(str_2)
    matrix = [[-1] * (N2 + 1) for i in range(N1 + 1)]
    result = recursion(str_1, str_2, matrix)
    print("Расстояние Дамерау-Левенштайна (с матрицей): {}".format(result))
    print("Итоговая матрица: ")
    for i in range(N1 + 1):
        for j in range(N2 + 1):
            print(" {} ".format(matrix[i][j]), end = '')
        print()
    return result

def test_lev_rec(str_1, str_2):
    N = 100
    time = process_time_ns()
    for i in range(N):
        levenshtein_rec(str_1, str_2)
    print("Рекурсионный: {}".format((process_time_ns() - time)/N))

def test_lev_rec_matr(str_1, str_2):
    N = 100
    time = process_time_ns()
    for i in range(N):
        levenshtein_rec_matrix(str_1, str_2)
    print("Рекурсионный с матрицей: {}".format((process_time_ns() - time)/N))

def test_lev_matr(str_1, str_2):
    N = 100
    time = process_time_ns()
    for i in range(N):
        levenshtein_not_rec(str_1, str_2)
    print("Матричный алгоритм: {}".format((process_time_ns() - time)/N))

def test_damer(str_1, str_2):
    N = 100
    time = process_time_ns()
    for i in range(N):
        damerau_levenshtein(str_1, str_2)
    print("Дамерау: {}".format((process_time_ns() - time)/N))

def test(str_1, str_2):
    print("N = ", len(str_1))
    test_lev_matr(str_1, str_2)
    test_lev_rec_matr(str_1, str_2)
    #test_lev_rec(str_1, str_2)
    test_damer(str_1, str_2)
    print("--------------")

def test1(str_1, str_2):
    print("-------------------------")
    print("Строка 1:", str_1)
    print("Строка 2:", str_2)
    print("Рекурсивный вариант Левенштайна: {}".format(levenshtein_rec(str_1, str_2)))
    levenshtein_rec_matrix(str_1, str_2)
    print("Нерекурсивный вариант Левенштайна: {}".format(levenshtein_not_rec(str_1, str_2)))
    damerau_levenshtein(str_1, str_2)
    print("--------------------------")

s1 = input("Введите строку 1: ")
s2 = input("Введите строку 2: ")

test1(s1, s2)

'''
test("a" * 15, "a" * 7 + "BCaV" + "b" * 4)
test("a" * 20, "a" * 14 + "BCaV" + "b" * 2)
test("a" * 25, "a" * 18 + "BCaV" + "b" * 3)
test("a" * 30, "a" * 20 + "BCaV" + "b" * 6)
test("a" * 35, "a" * 29 + "BCaV" + "b" * 2)
test("a" * 40, "a" * 34 + "BCaV" + "b" * 2)
test("a" * 45, "a" * 39 + "BCaV" + "b" * 2)
test("a" * 50, "a" * 45 + "BCaV" + "b")
test("a" * 60, "a" * 55 + "BCaV" + "b")
test("a" * 70, "a" * 63 + "BCaV" + "b" * 2)
test("a" * 80, "a" * 71 + "BCaV" + "b" * 4)
test("a" * 90, "a" * 80 + "BCaV" + "b" * 6)
test("a" * 100, "a" * 92 + "BCaV" + "b" * 4)
test("test", "Test")
test("", "")
test("A", "B")
test("AC", "CD")
test("RET", "TER")
test("XYZZ", "ZYXT")
test("QWERTY", "ASDFGH")
test("1234567", "CVF54FD")
test("CCCCCCCO", "OCOCOCOO")
test("1234567891", "1234567892")
test("скат", "кот")
test("развлечение", "увлечения")
test("хотдог", "каток")
test("общага", "общага")
test("АААААА", "ББББББ")
test("", "")
test("привет", "пока")
test("Привет", "пока")
test("привет", "првиет")
'''