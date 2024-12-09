from pprint import pprint


class CSR():
    def __init__(self, matrix=None):
        self.matrix_in_csr(matrix)

    # функция для вывода матрицы в человеческом виде
    def pprint(self):
        for i in range(self.n):
            strr = []
            for j in range(self.m):
                strr.append(self.get_elem(i + 1, j + 1))
            print(*strr)
    # для тестов
    def debug(self):
        return self.n, self.m, self.data, self.ind, self.indptr

    # функция для перевода матрицы в разреженный вид
    def matrix_in_csr(self, matrix):
        # используется такой блок т.к реализована считывание не с ввода руками
        if matrix is None:
            n = int(input())
            _ = int(input())
            matrix = []
            for i in range(n):
                matrix.append(list(map(int, input().split())))
        self.n = len(matrix)
        if self.n != 0:
            self.m = len(matrix[0])
        else:
            self.m = 0
        #массивчик для хранения значений
        self.data = []
        #массивчик для хранения столбцов
        self.ind = []
        #массивчик для хранения кол-ва элементов в строках
        self.indptr = [1]
        for i in matrix:
            count = 0
            #берем стобец и значение элемента и обрабатываем их
            for ind_j, j in enumerate(i):
                if j != 0:
                    count += 1
                    self.data.append(j)
                    self.ind.append(ind_j)
            self.indptr.append(self.indptr[-1] + count)

    def sled(self):
        if self.n != self.m:
            print("След можно вычислить только для квадратных матриц.")
            raise ValueError
        sled = 0
        #проходимся по каждой строке и ищем число на главной диагонали
        for i in range(self.n):
            #индекс первого элемента в i-той строке
            elem_start = self.indptr[i] - 1
            #индекс последнего элемента в этой строке
            elem_end = self.indptr[i + 1] - 1
            #проверяем принадлежность каждого к диагонали
            for k in range(elem_start, elem_end):
                if self.ind[k] == i:
                    sled += self.data[k]
                    break
        return sled

    def get_elem(self, i, j):
        if type(i) != int or type(j) != int or i <= 0 or j <= 0 or i > self.n or j > self.n:
            raise ValueError
        try:
            #ищем индекс столбца нужного нам элемента
            c = self.ind[self.indptr[i - 1] - 1:self.indptr[i] - 1].index(j - 1)
            # получаем значение зная индекс столбца и индекс первого эл-та в строке
            return self.data[self.indptr[i -1] + c - 1]
        #ненаход -> 0
        except ValueError:
            return 0

    def mul_scalar(self, a):
        #тут вроде понятно, просто каждый элемент на число
        try:
            for i in range(len(self.data)):
                self.data[i] = self.data[i] * a
            return self
        except ValueError:
            print('умножаем только на число или матрицу')
            raise ValueError

    def __add__(self, other):
        #проверка
        if type(other) != CSR:
            print('Складываем только с матрицей')
            raise ValueError
        #и еще проверка
        if self.n != other.n or self.m != other.m:
            print('ошибка размеров')
            raise ValueError
        #задаем базу
        ans_data = []
        ans_ind = []
        ans_indptr = [1]
        for row in range(self.n):
            row_data = {}
            #получаем значения в строке
            for k in range(self.indptr[row] - 1, self.indptr[row + 1] - 1):
                col = self.ind[k]
                row_data[col] = self.data[k]
            #смотрим на полученные значения раньше и либо добавляем к ним, либо добавляем новое в словарь
            for k in range(other.indptr[row] - 1, other.indptr[row + 1] - 1):
                col = other.ind[k]
                if col in row_data:
                    row_data[col] += other.data[k]
                else:
                    row_data[col] = other.data[k]
            #сортируем наши значения(иначе порядок может сломаться) и добавляем данные
            for col, value in sorted(row_data.items()):
                if value != 0:
                    ans_data.append(value)
                    ans_ind.append(col)
            ans_indptr.append(len(ans_data) + 1)
        #создаем обьект CSR
        ans_matrix = CSR([])
        ans_matrix.n = self.n
        ans_matrix.m = self.m
        ans_matrix.data = ans_data
        ans_matrix.ind = ans_ind
        ans_matrix.indptr = ans_indptr
        return ans_matrix

    # по идее никогда не сработает, но пусть будет
    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        #проверяем матрица ли это
        if type(other) != CSR:
            return self.mul_scalar(other)
        # проверяем размерчики
        if self.m != other.n:
            print('Матрицы не подходят по размеру')
            raise ValueError
        # задаем базу
        ans_data = []
        ans_ind = []
        ans_indptr = [1]
        columns = []
        # тут получаем значения стобцов матрицы на которую умножаем
        for j in range(other.m):
            col_other_data = {}
            for row in range(other.n):
                # берем смотрим элементы строчки и ищем с нужным стобцом
                for ind_other in range(other.indptr[row] - 1, other.indptr[row + 1] - 1):
                    if other.ind[ind_other] == j:
                        col_other_data[row] = other.data[ind_other]
                        break
            columns.append(col_other_data)
        #начинаем умножение
        for i in range(self.n):
            row_data = {}
            # тут получаем значения в строке
            for k in range(self.indptr[i] - 1, self.indptr[i + 1] - 1):
                col = self.ind[k]
                row_data[col] = self.data[k]
            #умножаем на каждую колонку
            for collumn in range(self.m):
                summa = 0
                # считаем по определению умножения
                for col_row, value in row_data.items():
                    summa += value * columns[collumn].get(col_row, 0)
                # нулики не добавляем
                if summa != 0:
                    ans_data.append(summa)
                    ans_ind.append(collumn)
            ans_indptr.append(len(ans_data) + 1)
        # задаем объект CSR
        ans_matrix = CSR([])
        ans_matrix.n = self.n
        ans_matrix.m = other.m
        ans_matrix.data = ans_data
        ans_matrix.ind = ans_ind
        ans_matrix.indptr = ans_indptr
        return ans_matrix

    def __rmul__(self, other):
        # т.к умножается всегда левая на правую, перенаправляем на скаляр
        return self.mul_scalar(other)

def determinant(matrix=None):
    if matrix is None:
        n = int(input())
        _ = int(input())
        matrix = []
        for i in range(n):
            matrix.append(list(map(int, input().split())))
    try:
        if len(matrix) != len(matrix[0]):
            print('Определитель считается только для квадратных матриц')
    except Exception:
        raise ValueError
    det = 0
    # считаем определитель для матрицы 2x2
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    #функция для удаления строки и столбца для подсчета через минор
    def drop_matrix(matrix, rows, cols):
        out = []
        for i in range(len(matrix)):
            # скипаем значения в удаляемой строке
            if i == rows:
                continue
            out_row =[]
            for j in range(len(matrix[0])):
                # скипаем значения в удаляемом столбцу
                if j == cols:
                    continue
                out_row.append(matrix[i][j])
            out.append(out_row)
        return out
    for column, i in enumerate(matrix[0]):
        # пользуемся формулой для подсчета определителя
        det += (-1)**(column)*i*determinant(drop_matrix(matrix,0, column))
    return det
