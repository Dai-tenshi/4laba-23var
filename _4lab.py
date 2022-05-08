"""Формируется матрица F следующим образом: если в Е сумма чисел, больших К в нечетных столбцах в области 3 больше,
#чем произведение чисел по периметру в области 2, то поменять в Е симметрично области 1 и 3 местами, 
иначе С и В поменять местами несимметрично. 
При этом матрица А не меняется. После чего вычисляется выражение: ((К*A)*F+ K* F T . 
Выводятся по мере формирования А, F и все матричные операции последовательно.
"""
import random
import time

def print_matrix(M, matr_name, tt):
    print("матрица " + matr_name + " промежуточное время = " + str(format(tt, '0.2f')) + " seconds.")
    for i in M:  # делаем перебор всех строк матрицы
        for j in i:  # перебираем все элементы в строке
            print("%5d" % j, end=' ')
        print()

print("\n-----Результат работы программы-------")

try:
    row_q = int(input("Введите количество строк (столбцов) квадратной матрицы в интервале от 6 до 100:"))
    while row_q < 6 or row_q > 100:
        row_q = int(input(
            "Вы ввели неверное число\nВведите количество строк (столбцов) квадратной матрицы в интервале от 6 до 100:"))
    K = int(input("Введите число К="))
    start = time.time()
    A, F, AF, FT = [], [], [], []  # задаем матрицы
    for i in range(row_q):
        A.append([0] * row_q)
        F.append([0] * row_q)
        AF.append([0] * row_q)
        FT.append([0] * row_q)
    time_next = time.time()
    print_matrix(F, "F", time_next - start)

    for i in range(row_q):  # заполняем матрицу А
        for j in range(row_q):
            # A[i][j] = random.randint(1, 5)
            if i < j and j < row_q-1-i:
                A[i][j] = 1
            elif i < j and j > row_q-1-i:
                A[i][j] = 2
            elif i > j and j > row_q-1-i:
                A[i][j] = 3
            elif i > j and j < row_q-1-i:
                A[i][j] = 4

    time_prev = time_next
    time_next = time.time()
    print_matrix(A, "A", time_next - time_prev)
    for i in range(row_q):  # F
        for j in range(row_q):
            F[i][j] = A[i][j]
    time_prev = time_next
    time_next = time.time()
    print_matrix(F, "F", time_next - time_prev)

    E = []  # задаем матрицу E
    size = row_q // 2
    for i in range(size):
        E.append([0] * size)

    for i in range(size):  # формируем подматрицу E
        for j in range(size):
            E[i][j] = F[size + i][size + row_q % 2 + j]
    time_prev = time_next
    time_next = time.time()
    print_matrix(E, "E", time_next - time_prev)
    
 
    quantity = 0
    multiplication = 1
    point = 0
    for x in range(size - 1, size // 2 - 1, -1):  # обрабатываем подматрицу E и считаем периметр снизу "треугольника"
        for y in range(size - 1, size // 2, -1):
            multiplication *= E[x][-1 - point]
            point += 1
            break
    # прошли через границу симметрии и считаем периметр сверху "треугольника"
    if size % 2 == 1:                                 #центр есть - идем по диагоналям
        point = 1
        for x in range(size // 2 - 1, 0 - 1, -1):
            for y in range(size // 2 + 1, size, 1):
                multiplication *= E[x][size // 2 + point]
                point += 1
                break
    else:                                             #центра нет - "перепрыгиваем" через него, продолжая идти по периметру
        point = 0
        for x in range(size // 2 - 1, 0 - 1, -1):
            for y in range(size // 2, size, 1):
                multiplication *= E[x][(size // 2) + point]
                point += 1
                break

    for i in range(1, size-1):  #добавляем к произведению основание периметра "треугольника"
        for j in range(size):
            point=0
            multiplication *= E[i+point][size-1]
            point+=1
            break
   
    summ = 0
    if j % 2 != 0 and i > j and j < size - 1 - i and E[i][j] > K:
        summ += E[i][j]

    if summ > multiplication:

        for i in range(1, size // 2, 1):  # меняем подматрицу E
            for j in range(0, i, 1):
                E[i][j], E[i][size - j - 1] = E[i][size - j - 1], E[i][j]
        for i in range(size // 2, size, 1):
            for j in range(0, i, 1):
                E[i][j], E[i][size - j - 1] = E[i][size - j - 1], E[i][j]
        print_matrix(E, "E", time_next - time_prev)
        for i in range(size):           # формируем матрицу F
            for j in range(size):
                F[i][size - row_q % 2 + j] = E[i][j]
    else:
        for i in range(row_q // 2):
            for j in range(0, row_q // 2):
                F[i][j], F[i][row_q // 2 + row_q % 2 + j] = F[i][row_q // 2 + row_q % 2 + j], F[i][j]

    time_prev = time_next
    time_next = time.time()
    print_matrix(F,"F",time_next-time_prev)
    print_matrix(A,"A",0)

    for i in range(row_q):      # K*A
        for j in range(row_q):
            A[i][j] = K*A[i][j]    
    time_prev = time_next
    time_next = time.time()
    print_matrix(A,"K*A",time_next-time_prev)
    
    for i in range(row_q):      # K*A*F
        for j in range(row_q):
            s = 0
            for m in range(row_q):
                s=s+ A[i][m] * F[m][j]
            AF[i][j] = s
    time_prev = time_next
    time_next = time.time()
    print_matrix(AF,"K*A*F",time_next-time_prev)
    
    for i in range(row_q):      # FT
        for j in range(i,row_q,1):
            FT[i][j],FT[j][i] = F[j][i],F[i][j]
    time_prev = time_next
    time_next = time.time()
    print_matrix(FT,"F^T",time_next-time_prev)
                
    for i in range(row_q):      # K*FT
        for j in range(row_q):
            FT[i][j] = K*FT[i][j]
    time_prev = time_next
    time_next = time.time()
    print_matrix(FT,"K*F^T",time_next-time_prev)
    
    for i in range(row_q):      # (K*A)*F+K*FT
        for j in range(row_q):
            AF[i][j] = AF[i][j]+FT[i][j]    
    time_prev = time_next
    time_next = time.time()
    print_matrix(AF,"(K*A)*F+K*F^T",time_next-time_prev)
    
    finish = time.time()
    result = finish - start
    print("Program time: " + str(result) + " seconds.")

except FileNotFoundError :
    print("\nФайл text.txt в директории проекта не обнаружен.\nДобавьте файл в директорию или переименуйте существующий *.txt файл")
