#include <random>
#include <vector>
#include <iostream>
#include <queue>
#include <thread>
#include <mutex>
#include <math.h>
#include <string>

#define THREADS 3

struct array_t
{
    std::vector<double> data;
    int size;
    double avg;
    double var;
};

struct queues_t
{
    std::queue<array_t> q1;
    std::queue<array_t> q2;
    std::queue<array_t> q3;
};

void get_avg(array_t &matrix)
{
    double sum = 0;

    for (size_t i = 0; i < matrix.size; i++)
    {
        sum += matrix.data[i];
    }

    matrix.avg = sum / (matrix.size * matrix.size);
}


void get_var(array_t &matrix)
{
    double sum = 0;

    for (size_t i = 0; i < matrix.size; i++)
    {
        sum += (matrix.data[i] - matrix.avg)*(matrix.data[i] - matrix.avg);
    }

    matrix.var = sum / matrix.size / matrix.size;
}


void fill_array(array_t &matrix)
{
    for (size_t i = 0; i < matrix.size; i++)
    {
        matrix.data[i] = (matrix.data[i] - matrix.avg) / sqrt(matrix.var);
    }
}


array_t generate_array(size_t size)
{
    std::vector<double> temp;

    temp.resize(size);

    for (size_t i = 0; i < size; i++)
    {
        temp[i] = rand() % 10 + 1;
    }

    array_t result;
    result.data = temp;
    result.size = size;

    return result;
}


void print_matrix(array_t matrix)
{
    std::cout << std::endl << std::endl;

    for (size_t i = 0; i < matrix.size; i++)
    {
        printf("%-15.1f ", matrix.data[i]);
        std::cout << std::endl;
    }
}


double time_now = 0;

std::vector<double> t1;
std::vector<double> t2;
std::vector<double> t3;


void log_linear(array_t &matrix, int task_num, int stage_num, 
                void (*func)(array_t &), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double start_res_time = time_now, res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(matrix);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count()) / 1e9;

    time_now = start_res_time + res_time;

    if (is_print)
        printf("Задача: %3d, Этап: %3d, Старт: %.6f, Конец: %.6f\n", 
                    task_num, stage_num, start_res_time, start_res_time + res_time);
}



void log_conveyor(array_t &matrix, int task_num, int stage_num, 
                    void (*func)(array_t &), bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;

    time_start = std::chrono::system_clock::now();
    func(matrix);
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count()) / 1e9;

    time_now += res_time;

    double start_res_time;

    if (stage_num == 1)
    {
        start_res_time = t1[task_num - 1];

        t1[task_num] = start_res_time + res_time;
        t2[task_num - 1] = t1[task_num];
    }
    else if (stage_num == 2)
    {
        start_res_time = t2[task_num - 1];

        t2[task_num] = start_res_time + res_time;
        t3[task_num - 1] = t2[task_num];
    }
    else if (stage_num == 3)
    {
        start_res_time = t3[task_num - 1];
    }

    if (is_print)
        printf("Задача: %3d, Этап: %3d, Старт: %.6f, Конец: %.6f\n", 
                    task_num, stage_num, start_res_time, start_res_time + res_time);
}


void stage1_linear(array_t &matrix, int task_num, bool is_print)
{
    log_linear(matrix, task_num, 1, get_avg, is_print);
}



void stage2_linear(array_t &matrix, int task_num, bool is_print)
{   
    log_linear(matrix, task_num, 2, get_var, is_print);
}


void stage3_linear(array_t &matrix, int task_num, bool is_print)
{   
    log_linear(matrix, task_num, 3, fill_array, is_print);
}


void parse_linear(int count, size_t size, bool is_print)
{

    time_now = 0;

    std::queue<array_t> q1;
    std::queue<array_t> q2;
    std::queue<array_t> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    for (int i = 0; i < count; i++)
    {
        array_t res = generate_array(size);
        
        queues.q1.push(res);
    }

    for (int i = 0; i < count; i++)
    {
        array_t matrix = queues.q1.front();
        stage1_linear(matrix, i + 1, is_print);
        queues.q1.pop();
        queues.q2.push(matrix);

        matrix = queues.q2.front();
        stage2_linear(matrix, i + 1, is_print); // Stage 2
        queues.q2.pop();
        queues.q3.push(matrix);

        matrix = queues.q3.front();
        stage3_linear(matrix, i + 1, is_print); // Stage 3
        queues.q3.pop();
    }
}



void stage1_parallel(std::queue<array_t> &q1, std::queue<array_t> &q2, 
                    std::queue<array_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    while(!q1.empty())
    {      
        m.lock();
        array_t matrix = q1.front();
        m.unlock();

        log_conveyor(matrix, task_num++, 1, get_avg, is_print);

        m.lock();
        q2.push(matrix);
        q1.pop();
        m.unlock();
    }
}


void stage2_parallel(std::queue<array_t> &q1, std::queue<array_t> &q2,
                     std::queue<array_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    do
    {   
        m.lock();
        bool is_q2empty = q2.empty();
        m.unlock();

        if (!is_q2empty)
        {   
            m.lock();
            array_t matrix = q2.front();
            m.unlock();

            log_conveyor(matrix, task_num++, 2, get_var, is_print);

            m.lock();
            q3.push(matrix);
            q2.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty());
}


void stage3_parallel(std::queue<array_t> &q1, std::queue<array_t> &q2, 
                     std::queue<array_t> &q3, bool is_print)
{
    int task_num = 1;

    std::mutex m;

    do
    {
        m.lock();
        bool is_q3empty = q3.empty();
        m.unlock();

        if (!is_q3empty)
        {
            m.lock();
            array_t matrix = q3.front(); 
            m.unlock();

            log_conveyor(matrix, task_num++, 3, fill_array, is_print);

            m.lock();
            q3.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty() || !q3.empty());
}


void parse_parallel(int count, size_t size, bool is_print)
{

    time_now = 0;
    
    t1.resize(count + 1);
    t2.resize(count + 1);
    t3.resize(count + 1);

    for (int i = 0; i < count + 1; i++)
    {
        t1[i] = 0;
        t2[i] = 0;
        t3[i] = 0;
    }

    std::queue<array_t> q1;
    std::queue<array_t> q2;
    std::queue<array_t> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    
    for (int i = 0; i < count; i++)
    {
        array_t res = generate_array(size);
        
        q1.push(res);
    }

    std::thread threads[THREADS];

    threads[0] = std::thread(stage1_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[1] = std::thread(stage2_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[2] = std::thread(stage3_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);

    for (int i = 0; i < THREADS; i++)
    {
        threads[i].join();
    }

}

void print_menu()
{
    std::cout << "1. Линейная обработка \n2. Конвейерная обработка \n0. Выход\n\n" << std::endl;
}


void run()
{
    int option = -1;

    while (option != 0)
    {
        print_menu();

        std::cout << "Выбор: ";
        std::cin >> option;

        int size, count;

        if (option > 0 & option < 3)
        {
            std::cout << "\n\nРазмер массива: ";
            std::cin >> size;

            std::cout << "Количество массивов: ";
            std::cin >> count;

            if (option == 1)
                parse_linear(count, size, true);
            else
                parse_parallel(count, size, true);

        }
        else if (option < 0 || option > 2)
        {
            std::cout << "\nОшибка: Неверно введен пункт меню. Повторите\n" << std::endl;
        }
    }
}



int main(void)
{
    run();

    return 0;
}

