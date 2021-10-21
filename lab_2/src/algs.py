import numpy as np

def check_sizes(N1, M1, N2, M2):
    result = True
    if (N1 == 0) or (M1 == 0) or (N2 == 0) or (M2 == 0):
        result = False
    elif (M1 != N2):
        result = False
    return result

def classic(matrix_1, matrix_2):
    N1, M1 = len(matrix_1), len(matrix_1[0])
    N2, M2 = len(matrix_2), len(matrix_2[0])

    result_matrix = []
    check = check_sizes(N1, M1, N2, M2)

    if (check):
        result_matrix = [[0] * N1 for i in range(M2)]
        for i in range(N1):
            for j in range(M2):
                for k in range(M1):
                    result_matrix[i][j] += (matrix_1[i][k] * \
                                          matrix_2[k][j])
    return result_matrix

def vinograd(matrix_1, matrix_2):
    N1, M1 = len(matrix_1), len(matrix_1[0])
    N2, M2 = len(matrix_2), len(matrix_2[0])

    result_matrix = []
    check = check_sizes(N1, M1, N2, M2)

    if (check):
        result_matrix = [[0] * N1 for i in range(M2)]

        M = N1
        N = M1
        Q = M2

        row = [0] * M
        for i in range(M):
            for j in range(N//2):
                row[i] += (matrix_1[i][2 * j] * \
                            matrix_1[i][2 * j + 1])
        
        col = [0] * Q
        for i in range(Q):
            for j in range(N // 2):
                col[i] += (matrix_2[2 * j][i] * \
                            matrix_2[2 * j + 1][i])
        
        for i in range(M):
            for j in range(Q):
                result_matrix[i][j] += (-row[i] -col[j])
                for k in range(N//2):
                    result_matrix[i][j] += \
                        (matrix_1[i][2*k + 1] + matrix_2[2*k][j])* \
                        (matrix_1[i][2*k] + matrix_2[2*k + 1][j])
        
        if (N % 2 == 1):
            for i in range(M):
                for j in range(Q):
                    result_matrix[i][j] += \
                        (matrix_1[i][N - 1] * matrix_2[N - 1][j])
        return result_matrix

def optvinograd(matrix_1, matrix_2):
    N1, M1 = len(matrix_1), len(matrix_1[0])
    N2, M2 = len(matrix_2), len(matrix_2[0])

    result_matrix = []
    check = check_sizes(N1, M1, N2, M2)

    if (check):
        result_matrix = [[0] * N1 for i in range(M2)]

        M = N1
        N = M1
        Q = M2

        row = [0] * M
        for i in range(M):
            for j in range(0, N - 1, 2):
                row[i] += (matrix_1[i][j] * \
                            matrix_1[i][j + 1])
        
        col = [0] * Q
        for i in range(Q):
            for j in range(0, N - 1, 2):
                col[i] += (matrix_2[j][i] * \
                            matrix_2[j + 1][i])
        
        flag = N % 2
        for i in range(M):
            for j in range(Q):
                result_matrix[i][j] += (-row[i] -col[j])
                for k in range(0, N - 1, 2):
                    result_matrix[i][j] += \
                        (matrix_1[i][k + 1] + matrix_2[k][j]) *  \
                        (matrix_1[i][k] + matrix_2[k + 1][j])
                if (flag):
                    result_matrix[i][j] += \
                        (matrix_1[i][N - 1] * matrix_2[N - 1][j])
        return result_matrix

matrix_1 = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
matrix_2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]

print(classic(matrix_1, matrix_2))
print("-" * 20)
print(vinograd(matrix_1, matrix_2))
print("-" * 20)
print(optvinograd(matrix_1, matrix_2))
print("-" * 20)
print(np.array(matrix_1).dot(np.array(matrix_2)))