class CSR():
    def __init__(self, matrix=None):
        self.matrix_in_csr(matrix)

    def pprint(self):
        for i in range(self.n):
            strr = []
            for j in range(self.m):
                strr.append(self.get_elem(i + 1, j + 1))
            print(*strr)

    def debug(self):
        return self.data, self.ind, self.indptr


    def matrix_in_csr(self, matrix):
        if matrix is None:
            n = int(input())
            _ = int(input())
            matrix = []
            for i in range(n):
                matrix.append(list(map(int, input().split())))
        self.n = len(matrix)
        if self.n != 0:
            self.m = len(matrix[0])
        self.data = []
        self.ind = []
        self.indptr = [1]
        for i in matrix:
            count = 0
            for ind_j, j in enumerate(i):
                if j != 0:
                    count += 1
                    self.data.append(j)
                    self.ind.append(ind_j)
            self.indptr.append(self.indptr[-1] + count)

    def sled(self):
        if self.n != self.m:
            print("След можно вычислить только для квадратных матриц.")
        sled = 0
        for i in range(self.n):
            elem_start = self.indptr[i] - 1
            elem_end = self.indptr[i + 1] - 1
            for k in range(elem_start, elem_end):
                if self.ind[k] == i:
                    sled += self.data[k]
                    break
        return sled

    def get_elem(self, i, j):
        try:
            c = self.ind[self.indptr[i - 1] - 1:self.indptr[i] - 1].index(j - 1)
            return self.data[self.indptr[i -1] + c - 1]
        except ValueError:
            return 0


    def mul_scalar(self, a):
        for i in range(len(self.data)):
            self.data[i] = self.data[i] * a

    def __add__(self, other):
        if type(other) != CSR:
            print('Складываем только с матрицей')
            return None
        if self.n != other.n or self.m != other.m:
            print('ошибка размеров')
            return None
        ans_data = []
        ans_ind = []
        ans_indptr = [1]
        for row in range(self.n):
            row_data = {}
            for k in range(self.indptr[row] - 1, self.indptr[row + 1] - 1):
                col = self.ind[k]
                row_data[col] = self.data[k]
            for k in range(other.indptr[row] - 1, other.indptr[row + 1] - 1):
                col = other.ind[k]
                if col in row_data:
                    row_data[col] += other.data[k]
                else:
                    row_data[col] = other.data[k]
            for col, value in sorted(row_data.items()):
                if value != 0:
                    ans_data.append(value)
                    ans_ind.append(col)
            ans_indptr.append(len(ans_data) + 1)
        ans_matrix = CSR([])
        ans_matrix.n = self.n
        ans_matrix.m = self.m
        ans_matrix.data = ans_data
        ans_matrix.ind = ans_ind
        ans_matrix.indptr = ans_indptr
        return ans_matrix

    def __radd__(self, other):
        self.mul_scalar(other)

    def __mul__(self, other):
        if type(other) != CSR:
            self.mul_scalar(other)
        if self.m != other.n:
            print('Матрицы не подходят по размеру')
            return None
        ans_data = []
        ans_ind = []
        ans_indptr = [1]
        columns = []
        # тут получаем значения стобцов матрицы
        for j in range(other.m):
            col_other_data = {}
            for row in range(other.n):
                for ind_other in range(other.indptr[row] - 1, self.indptr[row + 1] - 1):
                    if other.ind[ind_other] == j:
                        col_other_data[row] = self.data[ind_other]
                        break
            columns.append(col_other_data)
        for i in range(self.n):
            row_data = {}
            # тут значения строк
            for k in range(self.indptr[i] - 1, self.indptr[i + 1] - 1):
                col = self.ind[k]
                row_data[col] = self.data[k]
            for collumn in range(self.m):
                summa = 0
                for col_row, value in row_data.items():
                    summa += value * columns[collumn].get(col_row, 0)
                if summa != 0:
                    ans_data.append(summa)
                    ans_ind.append(collumn)
            ans_indptr.append(len(ans_data) + 1)
        ans_matrix = CSR([])
        ans_matrix.n = self.n
        ans_matrix.m = other.m
        ans_matrix.data = ans_data
        ans_matrix.ind = ans_ind
        ans_matrix.indptr = ans_indptr
        return ans_matrix

def determinant(matrix):
    if len(matrix) != len(matrix[0]):
        print('Определитель считается на квадратных матриц')
        return None
    det = 0
    if len(matrix) == 2 and len(matrix[0]) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    def drop_matrix(matrix, rows, cols):
        out = []
        for i in range(len(matrix)):
            if i == rows:
                continue
            out_row =[]
            for j in range(len(matrix[0])):
                if j == cols:
                    continue
                out_row.append(matrix[i][j])
            out.append(out_row)
        return out
    for column, i in enumerate(matrix[0]):
        det += (-1)**(column)*i*determinant(drop_matrix(matrix,0, column))
    return det

