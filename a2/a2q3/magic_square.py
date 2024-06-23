'''Magic Square

https://en.wikipedia.org/wiki/Magic_square

A magic square is a n * n square grid filled with distinct positive integers in
the range 1, 2, ..., n^2 such that each cell contains a different integer and
the sum of the integers in each row, column, and diagonal is equal.

'''

from z3 import Solver, sat, unsat, Sum
from z3 import *

def solve_magic_square(n, r, c, val):
    solver = Solver()
    magic_square = []
    for i in range(n):
        rows = []
        for j in range(n):
            rows.append(Int(f"magic_square_{i}_{j}"))
        magic_square.append(rows)
    
    numbers=[]
    for i in range(n):
        for j in range(n):
            numbers.append(magic_square[i][j])
    
    solver.add(Distinct(numbers))

    for i in range(n):
        for j in range(n):
            solver.add(magic_square[i][j]>= 1) 
            solver.add(magic_square[i][j]<= n**2)
    
    sum_reference = Sum(magic_square[0])
    for i in range (1, n):
        solver.add(Sum(magic_square[i]) == sum_reference)

    for j in range(n):
        col_sum = magic_square[0][j]
        for i in range(1, n):
            col_sum += magic_square[i][j]
        solver.add(col_sum == sum_reference)

    diag_sum = 0
    for i in range(n):
        for j in range(n):
            if (i==j):
                diag_sum += magic_square[i][j]
    
    solver.add(diag_sum == sum_reference)

    diag2_sum = magic_square[0][n-1]
    for i in range(1, n):
        diag2_sum += magic_square[i][n-1-i]
    solver.add(diag2_sum == sum_reference)

    solver.add(r >= 0)
    solver.add(r < n)
    solver.add(n > 0)
    solver.add(c >= 0)
    solver.add(c < n)
    solver.add(val >= 1)
    solver.add(val <= (n*n))
    solver.add([magic_square[r][c] == val])

    if solver.check() == sat:
        mod = solver.model()
        res = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(mod.evaluate(magic_square[i][j]).as_long())
            res.append(row)
        return res
    else:
        return None

def print_square(square):
    '''
    Prints a magic square as a square on the console
    '''
    n = len(square)

    assert n > 0
    for i in range(n):
        assert len(square[i]) == n

    for i in range(n):
        line = []
        for j in range(n):
            line.append(str(square[i][j]))
        print('\t'.join(line))


def puzzle(n, r, c, val):
    res = solve_magic_square(n, r, c, val)
    if res is None:
        print('No solution!')
    else:
        print('Solution:')
        print_square(res)


if __name__ == '__main__':
    n = 5
    r = 2
    c = 2
    val = 20
    puzzle(n, r, c, val)
