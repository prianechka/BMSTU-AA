#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>

void algorythm_for_DZ(std::vector<std::vector<int>> matrix, std::vector<float>mean)
{
    int idx_1 = 0; // 1
    int idx_2 = 0; // 2
    int max_cor = 0; // 3
    for (int i = 0; i < 3; i++) //4
    {
        for (int j = i + 1; j < 3; j++) //5
        {
            double var_x = 0; // 6
            double var_y = 0; // 7
            double sum = 0; // 8
            for (int k = 0; k < 3; k++) // 9
            {
                double slag_1 = (matrix[k][i] - mean[i]); // 10
                double slag_2 = (matrix[k][j] - mean[j]); // 11
                var_x += (slag_1 * slag_1); // 12
                var_y += (slag_2 * slag_2); // 13
                sum += (slag_1 * slag_2); // 14
            }
            var_x /= n; // 15
            var_y /= n; // 16
            double cor = sum * / (n * sqrt(var_x * var_y)); // 17
            if (cor > max_cor) // 18
            {
                idx_1 = i; // 19
                idx_2 = j; // 20
                max_cor = cor; // 21
            }
        }
    }
}