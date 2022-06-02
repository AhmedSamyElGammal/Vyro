## importing essential packages
import math
import random


## the Errors
_RowLengthError = 'Length of rows must be equal'
_DivisionByZeroError = 'Division by zero'
_MatrixMustBeSquerError = 'Matrix must be square'
_DotProductError = 'The number of colmus the first matrix must be equal to the number of rows of the second matrix'
_ShapesMustBeEqualError = 'Shape of matrices must be equal'
_RowsNumberMustBeEqualError = 'The number of rows of the two matrices must be equal'
_ColumnsNumberMustBeEqualError = 'The number of columns of the two matrices must be equal'
_NotSuitableShapeError = 'the number of rows and columns must be integer'
_AreasMustBeEqualError = 'the areas of the two shapes must be equal'



## Creating a function to be sure if the input shape is suitable
def _isSuitableShape(shape):
    stats = True
    for n in shape:
        if not isinstance(n, int):
            if not n.is_integer():
                stats = False
    if stats:
        return tuple([int(n) for n in shape])
    raise ValueError(_NotSuitableShapeError)


## Creating the object Row which is base unit of the Matirx
class _Row:
    def __init__(self, arr):
        if isinstance(arr, tuple):
            self.__arr = list(arr)
        else:
            self.__arr = arr

    def getArr(self):
        return self.__arr
    
    def __getitem__(self, key):
        return self.__arr[key]

    def __setitem__(self, key, value):
        self.__arr[key] = value

    def __len__(self):
        return len(self.__arr)

    def __str__(self):
        return " ".join(str(x) for x in self.__arr)

    def __add__(self, other):
        if isinstance(other, _Row):
            if len(self) != len(other):
                raise ValueError(_RowLengthError)
            return _Row([x + y for x, y in zip(self.__arr, other.getArr())])
        else: ## if other is a number
            return _Row([x + other for x in self.__arr])

    def connect(self, other):
        return _Row(self.__arr + other.getArr())

    def __sub__(self, other):
        if isinstance(other, _Row):
            if len(self) != len(other):
                raise ValueError(_RowLengthError)
            return _Row([x - y for x, y in zip(self.__arr, other.getArr())])
        else: ## if other is a number
            return _Row([x - other for x in self.__arr])

    def __rsub__(self, other):
        if isinstance(other, _Row):
            if len(self) != len(other):
                raise ValueError(_RowLengthError)
            return _Row([y - x for x, y in zip(self.__arr, other.getArr())])
        else: ## if other is a number
            return _Row([other - x for x in self.__arr])

    def __mul__(self, num):
        return _Row([x * num for x in self.__arr])

    def __truediv__(self, num):
        if num == 0:
            raise ValueError(_DivisionByZeroError)
        return _Row([x / num for x in self.__arr])

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        return all(x == y for x, y in zip(self.__arr, other.getArr()))

    def __ne__(self, other):
        return not self.__eq__(other)



## Creating the Matrix object which is the main object to deal with
class Matrix:
    def __init__(self, rows):
        if sum([len(rows[i]) != len(rows[i +1]) for i in range(len(rows) -1)]):
            raise ValueError(_RowLengthError)

        if isinstance(rows[0], list):
            self.__rows =  [_Row(row) for row in rows]
        else:
            self.__rows = rows

        self._rowNum = len(self.__rows)
        self._colNum = len(self.__rows[0])
        self._shape = (self._rowNum, self._colNum) ## (rows_num, cols_num)
        self._area = self._rowNum * self._colNum
        self._isSquare = (self._rowNum == self._colNum)
        self._isSingleNum = (self._isSquare and self._rowNum == 1)
        self._isColumnVector = (self._colNum == 1)
        self._isRowVector = (self._rowNum == 1)
        #self._isSymmetric = (self == self.transpose()) == you cann't use this line it will cause infinty loop

    def getRows(self):
        return self.__rows

    def __getitem__(self, key):
        return self.__rows[key]

    def getItems(self):
        items = []
        for row in self.__rows:
            for item in row.getArr():
                items.append(item)
        return items

    def __setitem__(self, key, value):
        self.__rows[key] = value

    def __len__(self):
        return self._rowNum

    def shape(self): ## (rows_num, cols_num)
        return self._shape

    def area(self):
        return self._area

    def isSquare(self):
        return self._isSquare

    def isSingleNum(self):
        return self._isSingleNum

    def isColumnVector(self):
        return self._isColumnVector

    def isRowVector(self):
        return self._isRowVector

    def isSymmetric(self):
        return self == self.transpose()

    def __str__(self):
        return "\n".join(str(row) for row in self.__rows)

    def __add__(self, other):
        if isinstance(other, Matrix):
            if self.shape() != other.shape():
                raise ValueError(_ShapesMustBeEqualError)
            return Matrix([row + other[i] for i, row in enumerate(self.__rows)])
        else: ## if other is a number
            return Matrix([row + other for row in self.__rows])

    def __radd__(self, other):
        return self.__add__(other)

    def H_connect(self, other):
        if self.shape()[0] != other.shape()[0]:
            raise ValueError(_RowsNumberMustBeEqualError)
        return Matrix([row.connect(other[i]) for i, row in enumerate(self)])

    def V_connect(self, other):
        if self.shape()[1] != other.shape()[1]:
            raise ValueError(_ColumnsNumberMustBeEqualError)
        return Matrix(self.__rows + other.getRows())

    def __sub__(self, other):
        if isinstance(other, Matrix):
            if self.shape() != other.shape():
                raise ValueError(_ShapesMustBeEqualError)
            return Matrix([row - other[i] for i, row in enumerate(self.__rows)])
        else: ## if other is a number
            return Matrix([row - other for row in self.__rows])

    def __rsub__(self, other):
        if isinstance(other, Matrix):
            if self.shape() != other.shape():
                raise ValueError(_ShapesMustBeEqualError)
            return Matrix([other[i] - row for i, row in enumerate(self.__rows)])
        else: ## if other is a number
            return Matrix([other - row for row in self.__rows])

    def deleteRow(self, n):
        return Matrix([row for i, row in enumerate(self) if i != n])

    def deleteCol(self, n):
        return self.transpose().deleteRow(n).transpose()

    def fixRow(self, n, newValue = 0):
        ## replace the all numbers with the new value
        # except the n-th row numbers
        return Matrix([_Row([newValue] * self.shape()[1])
                           if i != n else row
                                for i, row in enumerate(self)])

    def fixCol(self, n, newValue = 0):
        ## replace the all numbers with the new value
        # except the n-th column numbers
        return self.transpose().fixRow(n, newValue).transpose()

    def __mul__(self, num):
        return Matrix([row * num for row in self])

    def __rmul__(self, num):
        return self.__mul__(num)

    def __truediv__(self, num):
        if num == 0:
            raise ValueError(_DivisionByZeroError)
        return Matrix([row / num for row in self])

    def __eq__(self, other):
        if self.shape() != other.shape():
            return False
        return all(row == other[i] for i, row in enumerate(self.__rows))

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def transpose(self):
        return Matrix( [_Row(row) for row in zip(*self.__rows)])

    def do(self, func):
        return Matrix( [_Row([func(x) for x in row]) for row in self])

    def dot(self, other):
        if self.shape()[1] != other.shape()[0]:
            raise ValueError(_DotProductError)
        return Matrix( [_Row([sum([n1 * n2 for n1, n2 in zip(row1, row2)])
                                 for row2 in other.transpose()])
                                 for row1 in self])

    def determin(self):
        if not self.isSquare():
            raise ValueError(_MatrixMustBeSquerError)
        if self.isSingleNum():
            return self[0][0]
        elif self.shape()[0] == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
        else:
            return sum([((-1) ** i) * self[0][i] * self.deleteRow(0).deleteCol(i).determin()
                                 for i in range(self.shape()[0])])

    def reshape(self, new_shape):
        if _isSuitableShape(new_shape):
            new_shape = _isSuitableShape(new_shape)
            if new_shape[0] * new_shape[1] != self.area():
                raise ValueError(_AreasMustBeEqualError)
            
            return Matrix([
                [self.getItems()[j + i*new_shape[1]] 
                    for j in range(new_shape[1])]
                    for i in range(new_shape[0])
            ])



## some functions to deal with the matrix more easily
def rowVector(arr):
    return Matrix([_Row(arr)])

def columnVector(arr):
    return Matrix([_Row(arr)]).transpose()

def exp(matrix):
    return matrix.Do(math.exp)

def rowSum(matrix): ## output matrix is with one column
    return Matrix([_Row([sum(col) for col in zip(*matrix.transpose())])]).transpose()

def columnSum(matrix): ## output matrix is with one row
    return rowSum(matrix.transpose()).transpose()

def ranMatrix(shap, start, end):
    return Matrix( [_Row([random.uniform(start, end)
                     for _ in range(shap[1])])
                        for _ in range(shap[0])])

def idenMatrix(n): ## identity matrix always square so its shape is (n, n)
    return Matrix( [_Row([1 if i == j else 0
                     for i in range(n)])
                        for j in range(n)])

def ZeroMatrix(shap):
    return Matrix( [_Row([0 for _ in range(shap[1])])
                        for _ in range(shap[0])])

def oneMatrix(shap):
    return Matrix( [_Row([1 for _ in range(shap[1])])
                        for _ in range(shap[0])])

def diagonalMatrix(diagnal): ## diagnal matrix always square so its shape is (len(diagnal), len(diagnal))
    return Matrix( [_Row([diagnal[i] if i == j else 0
                        for i in range(len(diagnal))])
                            for j in range(len(diagnal))])

