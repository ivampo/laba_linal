import unittest
from math import expm1

from main import CSR, determinant


class TestMatrixMethods(unittest.TestCase):
    def test_matrix_in_csr(self):
        matrix = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        output = CSR(matrix).debug()
        expected = (3, 3, [1, 2, 3], [0, 1, 2], [1, 2, 3, 4])
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        output = CSR(matrix).debug()
        expected = (3, 3, [], [], [1, 1, 1, 1])
        # --------------####--------------
        self.assertEqual(output, expected)
        matrix = [
            [1, 2, 0, 0, 5]
        ]
        output = CSR(matrix).debug()
        expected = (1, 5, [1, 2, 5], [0, 1, 4], [1, 4])
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix = [
            [1],
            [0],
            [3]
        ]
        output = CSR(matrix).debug()
        expected = (3, 1, [1, 3], [0, 0], [1,2,2,3])
        self.assertEqual(output, expected)

    def test_sled(self):
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        output = CSR(matrix).sled()
        expected = 15
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix = [
            [42]
        ]
        output = CSR(matrix).sled()
        expected = 42
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        output = CSR(matrix).sled()
        expected = 0
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        with self.assertRaises(ValueError):
            CSR(matrix).sled()

    def test_get_elem(self):
        matrix = CSR([[42]])
        self.assertEqual(matrix.get_elem(1, 1), 42)

        matrix = CSR([
            [1, 2],
            [3, 4]
        ])
        with self.assertRaises(ValueError):
            matrix.get_elem(2, 0)
        with self.assertRaises(ValueError):
            matrix.get_elem(0, 2)

        matrix = CSR([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        self.assertEqual(matrix.get_elem(1, 1), 1)
        self.assertEqual(matrix.get_elem(2, 2), 5)
        self.assertEqual(matrix.get_elem(3, 3), 9)

    def test_add(self):
        matrix1 = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        matrix2 = [
            [0, 0, 0],
            [0, 0, 0]
        ]
        output = CSR(matrix1) + CSR(matrix2)
        output = output.debug()
        expected_result = (2, 3, [1, 2, 3, 4, 5, 6], [0, 1, 2, 0, 1, 2], [1, 4, 7])
        self.assertEqual(output, expected_result)
        # --------------####--------------
        matrix1 = [
            [1, 2, 3],
            [4, 5, 6]
        ]
        matrix2 = [
            [1, 2],
            [3, 4]
        ]
        with self.assertRaises(ValueError):
            err = CSR(matrix1) + CSR(matrix2)
        # --------------####--------------
        matrix1 = []
        matrix2 = []
        output = CSR(matrix1) + CSR(matrix2)
        expected = (0, 0, [], [], [1])
        self.assertEqual(output.debug(), expected)

    def test_mul_scalar(self):
        matrix = [
            [1, -2],
            [3, 4]
        ]
        scalar = -1
        output = (CSR(matrix) * scalar).debug()[2]
        expected = [-1, 2, -3, -4]
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix = []
        scalar = 5
        output = (CSR(matrix) * scalar).debug()
        expected = (0, 0, [], [], [1])
        self.assertEqual(output, expected)

    def test_mul_matrix(self):
        matrix1= [
            [1, 2],
            [3, 4]
        ]
        matrix2 = [
            [5, 6],
            [7, 8]
        ]
        output = CSR(matrix1) * CSR(matrix2)
        output = output.debug()
        expected = (2, 2, [19, 22, 43, 50], [0, 1, 0, 1], [1, 3, 5])
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        matrix2 = [
            [5, 6, 7]
        ]
        with self.assertRaises(ValueError):
            CSR(matrix1) * CSR(matrix2)
        # --------------####--------------
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        identity = [
            [1, 0],
            [0, 1]
        ]
        output = (CSR(matrix1) * CSR(identity)).debug()
        expected = CSR(matrix1).debug()
        self.assertEqual(output, expected)
        # --------------####--------------
        matrix1 = [
            [1, 2],
            [3, 4]
        ]
        zero_matrix = [
            [0, 0],
            [0, 0]
        ]
        output = (CSR(matrix1) * CSR(zero_matrix)).debug()
        expected = (2, 2, [], [], [1, 1, 1])
        self.assertEqual(output, expected)

    def test_determinant(self):
        matrix = [
            [6, 1, 1],
            [4, -2, 5],
            [2, 8, 7]
        ]
        expected_result = -306
        self.assertEqual(determinant(matrix), expected_result)
        # --------------####--------------
        matrix = [
            [1, 2],
            [3, 4]
        ]
        expected_result = -2
        self.assertEqual(determinant(matrix), expected_result)
        # --------------####--------------
        matrix = [[5]]
        expected_result = 5
        self.assertEqual(determinant(matrix), expected_result)
        # --------------####--------------
        matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        expected_result = 1
        self.assertEqual(determinant(matrix), expected_result)
        # --------------####--------------
        matrix = []
        with self.assertRaises(ValueError):
            determinant(matrix)