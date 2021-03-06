#!/bin/env python3
# -*- coding: utf-8 -*-

"""
    This module contains the Matrix class.\n
    I abstracted this away from the HMM to clean up my code.\n
"""

__author__ = ["Amittai"]
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"


import numpy as np

class Matrix(object):
    """
        This class implements a simple matrix module,\n
        supporting operations such as matrix multiplication, addition, and subtraction,\n
        integer division, and transposition.\n
        
        The module uses numpy arrays for efficiency.\n
        NOTE: Matrices are zero-indexed.\n
    """
 
 
################# MATRIX REPRESENTATION #################   
    def __init__(self, rows, cols, source=None):
        
        """
            Creates a new Matrix of dimensions rows(downwards) x cols(sideways).\n\n
            
            `rows`: the number of rows in the Matrix. `rows` correspond to `y`.\n
            `cols`: the number of columns in the Matrix. `cols` correspond to `x`.\n
            `source`: a list of lists that will be used to populate the Matrix.\n
            NOTE: Matrices are zero-indexed.\n
            
            Format:\n
            \tFirst sub-array is first row, second sub-array is second row, etc.\n
            \tEach sub-array has cols elements.
            
            ```
            [
                [0 0 0 0]
                [0 0 0 0]
                [0 0 0 0]
            ]
            ```
            Optionally, you can pass a source array to initialize the matrix.\n
            This module expects you to pass a valid Matrix array,\n
            i.e. all subarrays have equal dimensions,\n
            and does not check for compatibility.
            
        """
        if source is not None:
            self.data = np.array(source)
            
        elif rows and cols:
            self.data = np.zeros((rows, cols))

        
        else:
            raise ValueError("Invalid Matrix dimensions.\n\
                             Please provide either a Python list to initialize with,\
                                 or specify columns and rows.")
            
        try: 
            self.rows = self.data.shape[0]
            try: 
                self.cols = self.data.shape[1]
            except IndexError: 
                self.cols = 0
        except IndexError: 
            self.rows = 0
        # print(f"rows = {rows}, cols = {cols}, data = {self.data}")
            
    def shape(self):
        
        """
            Returns a tuple of the dimensions of the Matrix.
        """
        return (self.rows, self.cols)
    
    def __getitem__(self, pos):
        
        """
            Returns the value at [x, y]\n
            
            Example usage:\n
            ```python
            print(matrix[col, row])
            ```
        """
        
        if isinstance(pos, (tuple, list)):
            (row, col) = pos
            
        elif isinstance(pos, (int, np.int64)):
            return self.data[pos]
            
        else:
            print(f"index type {type(pos)} not supported.\n")
        
        
        return self.data[row, col]
    
    def __setitem__(self, pos, value):
        
        """
            Sets the value at (x, y) to value.\n
            Example usage:\n
            ```python
            matrix[col, row] = value
            ```
        """
        (row, col) = pos
        self.data[row, col] = value
    
    def __str__(self):
        
        """
            Returns a string representation of the Matrix.
        """
        s = str(self.data)
        s = s[1:-1]
        s = f"\n {s}\n"
        return s

################## MATRIX CALCULATIONS ##################

    def __add__(self, other):
        """
            Add two matrices, or a scalar to a matrix.\n
            If two matrices, they must have the same shape.
        """
        
        if isinstance(other, (int, float, list, tuple, np.ndarray)):
            return Matrix(0, 0, np.add(self.data, other))
        
        if not isinstance(other, Matrix):
            return NotImplemented
            
        if self.shape() != other.shape():
            raise ValueError("Matrices are not compatible for addition.")
        
        return Matrix(0, 0, np.add(self.data, other.data))
    
    def __radd__(self, other):
        """
            Add two matrices, or a scalar to a matrix.\n
            If two matrices, they must have the same shape.
        """
        return self + other
    
    def __sub__(self, other):
        """
            Subtract two matrices, or a scalar to a matrix.\n
            NOTE: Order matters!\n
            If two matrices, they must have the same shape.
        """
        
        if isinstance(other, (int, float, list, tuple)):
            return Matrix(0, 0, np.subtract(self.data, other))
        
        if isinstance(other, Matrix):
            if self.shape() != other.shape():
                raise ValueError("Matrices are not compatible for subtraction.")
            
            return Matrix(0, 0, np.subtract(self.data, other.data))
            
        return NotImplemented
    
    def __rsub__(self, other):
        """
            Subtract two matrices, or a scalar to a matrix.\n
            NOTE: Order matters!\n
            If two matrices, they must have the same shape.\n
            NOTE: lists and tuples are not supported.
        """
        
        if isinstance(other, (int, float)):
            other_broadcast_to_array = np.full(np.shape(self.data), other)
            return Matrix(0, 0, np.subtract(other_broadcast_to_array, self.data))
        
        if isinstance(other, Matrix):
            if self.shape() != other.shape():
                raise ValueError("Matrices are not compatible for subtraction.")
            
            return Matrix(0, 0, np.subtract(other.data, self.data)) 
        
        return NotImplemented              # Checks if other object supports operation.
    
    def __mul__(self, other):
        
        """
            Returns the product of two matrices.\n
            Example usage:\n
            ```python
            matrix1 * matrix2
            ```
        """
        if isinstance(other, (int, float)):
            return Matrix(0, 0, np.multiply(self.data, other))
        
        
        if isinstance(other, Matrix):
            # singular-dimension matrix? broadcast.
            # print(f"mat 2 -- {other.cols}, {other.rows}")
            if other.cols == other.rows == 1:
                return Matrix(0, 0, np.dot(self.data, other.data))
            
            # otherwise... only multily if compatible.
            elif self.cols != other.rows:
                raise ValueError(f"\n\nmat1: {self}\n mat2: {other}\nMatrices are not compatible for multiplication.")
        
            return Matrix(0, 0, np.dot(self.data, other.data))
        return NotImplemented
    
    def __rmul__(self, other):
        
        """
            Returns the product of two matrices.\n
            Example usage:\n
            ```python
            matrix1 * matrix2
            ```
        """
        if isinstance(other, (int, float)):
            return Matrix(0, 0, np.multiply(self.data, other))
        
        if isinstance(other, Matrix):
            if other.cols != self.rows:
                raise ValueError("Matrices are not compatible for multiplication.")
        
            return Matrix(0, 0, np.dot(other.data, self.data))
        
        return NotImplemented
    
    def __truediv__(self, other: int):
        
        """
            Returns the quotient of a Matrix by a number.\n
            Example usage:\n
            ```python
            matrix1 / 2
            ```
        """
        if not other: raise ValueError("Cannot divide by zero.")
        
        if isinstance(other, (int, float)):
            return Matrix(0, 0, np.true_divide(self.data, other))
        
        if isinstance(other, Matrix):
            return self * (-other)
        
        if isinstance(other, (list, tuple)):
            return self / Matrix(0, 0, other)
        
        return NotImplemented
    
    def __div__(self, other):
        
        """
            Returns the quotient of a Matrix by a number.\n
            Example usage:\n
            ```python
            matrix1 / 2
            ```
        """
        if not other: raise ValueError("Cannot divide by zero.")
        
        if isinstance(other, (int, float)):
            return Matrix(0, 0, np.floor_divide(self.data, other))
        
        if isinstance(other, Matrix):
            return self * (-other)
        
        if isinstance(other, (list, tuple)):
            return self / Matrix(0, 0, other)
        
        return NotImplemented
    
    def __neg__(self):
        """
            Returns the negative of a Matrix.\n
            Example usage:\n
            ```python
            matrix1 = ....
            inv_matrix1 = -matrix1
            ```
        """
        return Matrix(0, 0, np.linalg.inv(self.data))
    
    def __pow__(self, other):
        """
            Compute the Matrix exponent.
        """
        if isinstance(other, (int, float)):
            return Matrix(0, 0, np.power(self.data, other))
        
        return NotImplemented
    
    def transpose(self):
        """
            Returns the transpose of a Matrix.\n
            Example usage:\n
            ```python
            matrix1 = ....
            transpose_matrix1 = matrix1.transpose()
            ```
        """
        return Matrix(0, 0, np.transpose(self.data))
    
    @staticmethod
    def multiply(m1, m2):
        """
            Returns the element-wise product of two matrices.\n
            Example usage:\n
            ```python
            matrix1.multiply( matrix2)
            ```
            NOTE: using the `*` operator calls __mul__ instead of this method.
        """
        if isinstance(m2, (int, float, list)):
            return Matrix(0, 0, np.multiply(m1.data, m2))
        
        if isinstance(m1, Matrix) and isinstance(m2, Matrix):
            return Matrix(0, 0, np.multiply(m1.data, m2.data))
        return NotImplemented
    
    @staticmethod
    def identity(*dims):
        """
            Get the identity matrix of given dimensions.\n
            NOTE: matrix must be square.
        """
        return Matrix(0, 0, np.identity(dims))
    
    @staticmethod
    def copy(matrix):
        """
            Returns a copy of the given Matrix.
        """
        if isinstance(matrix, Matrix):
            return Matrix(0, 0, np.copy(matrix.data))
        
        return NotImplemented
    
    @staticmethod
    def zeros(*args):
        """
            Returns a Matrix of zeros.
        """
        return Matrix(0, 0, np.zeros(args))
    
    @staticmethod
    def ones(rows, cols):
        """
            Returns a Matrix of ones.
        """
        return Matrix(0, 0, np.ones((rows, cols)))
    
    
    @staticmethod
    def full(rows, cols, value):
        """
            Returns a Matrix filled with given value.
        """
        return Matrix(0, 0, np.full((rows, cols), value))
    
    @staticmethod
    def random(rows, cols, low=0, high=1):
        """
            Returns a Matrix filled with random values in the given range.
        """
        return Matrix(0, 0, np.random.uniform(low, high, (rows, cols)))
    
    @staticmethod
    def normal(rows, cols, mean=0, std=1):
        """
            Returns a Matrix filled with normal values with given mean and standard deviation.
        """
        return Matrix(0, 0, np.random.normal(mean, std, (rows, cols)))
    
    @staticmethod
    def normalize(matrix, axis=0):
        """
            Normalize the given Matrix.
        """
        if not isinstance(matrix, Matrix):
            return NotImplemented
        
        matrix.data = matrix.data / matrix.data.sum(axis=axis, keepdims=True)
        
    @staticmethod
    def max(matrix, axis=1):
        """
            Returns the maximum values along the given axis.\n
            This method returns the values whose indices would be returned by `argmax`.\n
            Default axis is 1.
        """
        if not isinstance(matrix, Matrix):
            return NotImplemented
        
        if matrix.data.ndim == 1:
            return np.amax(matrix.data)
        
        return Matrix(0, 0, np.amax(matrix.data, axis=axis))
        
    @staticmethod
    def argmax(matrix, axis=1):
        """
            Returns the indices of the maximum values along the given axis.\n
            This method returns the indices of the values that would be returned by `max`.\n
            Default axis is 1.
        """
        if not isinstance(matrix, Matrix):
            return NotImplemented
        
        if matrix.data.ndim == 1:
            return Matrix(0, 0, np.argmax(matrix.data))
        
        return Matrix(0, 0, np.argmax(matrix.data, axis=axis))
        
    
    
def test_representation():
    # simple test case
    m = Matrix(4, 3)
    print(f"Matrix: {m}")
    print(m.shape())
    m[1, 1] = 99
    m[3, 2] = 88
    print(m[1, 1])
    print(m)
    
    # simple test case 2
    m2 = Matrix(0, 0, [[1,2,3], [4,5,6], [7,8,9], [10,11,12]])
    print(m2)
    print(m2.shape())
    
def test_add():
    print("Additions...\n_____________\n")
    m = Matrix(4,4)
    m[1, 1] = 99
    m[2, 1] = 88
    m[3, 3] = 66
    m[3, 2] = 88
    print(m)
    print(m + m)
    print(m + 2)
    print(2 + m)
    
def test_sub():
    print("Subtraction\n__________\n")
    m = Matrix(4,4)
    m[1, 1] = 99
    m[2, 1] = 88
    m[3, 3] = 66
    m[3, 2] = 88
    print(m)
    print(m - m)
    print(m - 2)
    print(2 - m)
    # print(m - None)   #! TypeError: unsupported operand type(s) for -: 'Matrix' and 'NoneType'
    
    m2 = Matrix(0, 0, [[1,0,3], [6, 6, 6], [9,8,7]])
    print(m2)
    print(-m2)
    
    
def test_mult():
    m = Matrix(4,4)
    m[1, 1] = 99
    m[3, 2] = 88
    print(m)
    print(m * m)
    print(m * 2)
    print(2 * m)
    
def test_div():
    m = Matrix(4,4)
    m[1, 1] = 99
    m[3, 2] = 88
    print(m)
    print(m / 2)
    # print(m / 0) #! breakpoint -- raises an exception.
    
    m2 = Matrix(0, 0, [[1, 2], [2, 1]])
    print(f"m2 = {m2}")
    m2_inv = -m2
    print(f"m2_inv = {m2_inv}")
    m3 = m2 ** 2
    print(f"m3 = {m3}")
    m4 = m3 / m2
    print(f"m4 = {m4}")
    
def other_tests():
    mat = Matrix(0, 0, [[1,2,3], [4,5,6], [7,8,9], [10,11,12]])
    print(mat)
    print(Matrix.normalize(mat))
    
    test = Matrix(2, 3)
    print(test)
    
    z2 = Matrix.zeros(2, 3)
    print(z2)
    
    id3 = Matrix.identity(3)
    print(id3)
    
    r4 = Matrix.random(2, 3, low=5, high = 27)
    print(r4)
    
def test_fib():
    mat = Matrix(0, 0, [[1,1], [1,0]])
    vec = Matrix(0, 0, [[1],[0]])
    
    print(mat)
    print(vec)
    print(mat * vec)
    
    for i in range(1, 21, 1):
        vec = mat * vec
        print(f"The fibonacci number {i} is {vec[1]}")
    
        
        
if __name__ == "__main__":
    test_add()
    test_sub()
    test_mult()
    test_div()
    other_tests() 
    test_fib()
        