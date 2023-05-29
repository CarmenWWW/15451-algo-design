from ortools.linear_solver import pywraplp
import math
import numpy as np


def getMatrix(a, b, size, k):
    matrix = [[0 for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            matrix[i][j] = getBig(i, j, matrix, a, b, k) / (k * (k-1))
    return matrix



def getBig(x, y, matrix, a, b, k):
    # row represents player 1's strategy
    # col represents player 2's strategy
    result = 0
    for r in range(k):
        for c in range(k):
            if (r == c): continue
            f1 = x & (1 << r)
            f2 = y & (1 << c)
            if (not f1): result += -1 * a
            elif (not f2): result += a
            elif (r > c): result += (a+b)
            else: result -= (a+b)
    return result


def lp(matrix, size, k):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    # Create the variables and let them take on any non-negative value.
    poss = [solver.NumVar(0, 1,'p{}'.format(x)) for x in range(size)]
    solver.Add(sum(poss) == 1)
    v = solver.NumVar(-1 * solver.infinity(), solver.infinity(), "v")

    for p2 in range(size): 
        solver.Add(sum([poss[p1] * matrix[p1][p2] for p1 in range(size)]) >= v)


    solver.Maximize(v)

    # Solve the system.
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # print('Solution:')
        print(solver.Objective().Value())
        # print('Objective value =', solver.Objective().Value())

    # print('\nAdvanced usage:')
    # print('Problem solved in %f milliseconds' % solver.wall_time())
    # print('Problem solved in %d iterations' % solver.iterations())



def main():
    # step 0. process read in
    k, a, b = tuple([float(x) for x in input().split()])

    size = int(pow(2, k))
    # step 1. get 1<<k * 1<<k matrix that represents all payoff
    matrix = getMatrix(a, b, size, int(k))

    # step 2. solve with solver
    lp(matrix, size, int(k))

    


main()