#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:52:35 2020

@author: Sébastien LEJEUNE | MENIELLE IBO Alternance
"""
from ortools.sat.python import cp_model
from random import sample

base  = 3 #size of the square
side  = base*base #size of the board

def pattern(r,c):
    return (base*(r%base)+r//base+c)%side

def shuffle(s):
    '''
    It allows to return a list of k elements of the sequence seq randomly

    Parameters
    ----------
    s : tab
        tab that content the elements.

    Returns
    -------
    TYPE
        Return a k length list of unique elements chosen from the population sequence or set. Used for random sampling without replacement.

    '''
    return sample(s,len(s)) 

def generatePlate(level):
    '''
    method that generate a grid in function of the level.

    Parameters
    ----------
    level : int
        Correspond to the level of the grid.

    Returns
    -------
    board : tab
        Board with empty(0) to resolv it.

    '''
    rBase = range(base)
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))
    
    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
    
    squares = side*side
    nbOfzeros = (side*side)-DifficultyChoice(level) # get the number of 0 from the Difficulty selected
    for p in sample(range(squares),nbOfzeros+1):
        board[p//side][p%side] = 0
    return board
    
def DifficultyChoice(level):
    '''
    Method that permit to select the level of the grid

    Parameters
    ----------
    level : INT
        An int that correspond of the level (between 1 and 5).

    Returns
    -------
    nb : INT
        An int that correspond of the number that will display in the grid.

    '''
    nb = 0 #number of numbers
    if level==1 : nb=50
    elif level==2 : nb=40
    elif level==3 : nb=33
    elif level==4 : nb=26
    elif level==5 : nb=17
    return nb

def solve_sudoku(initial_grid):
    '''
    Solving the sudoku grid using CP OR TOOLS

    Parameters
    ----------
    initial_grid : tab
        Correspond of the unsolved grid  .

    Returns
    -------
    tab : tab
        The solved grid.

    '''
    model = cp_model.CpModel()

    cell_size = base
    line_size = side
    line = range(line_size) 
    cell = range(cell_size) 

    grid = {
        (i, j): model.NewIntVar(1, line_size, 'grid %i %i' % (i, j))
        for i in line for j in line
    }

    
    for i in line:
        model.AddAllDifferent([grid[(i, j)] for j in line]) # AllDifferent on rows

    
    for j in line:
        model.AddAllDifferent([grid[(i, j)] for i in line]) # AllDifferent on columns

    
    for i in cell:
        for j in cell:
            one_cell = [
                grid[(i * cell_size + di, j * cell_size + dj)] for di in cell
                for dj in cell
            ]
            model.AddAllDifferent(one_cell) # AllDifferent in case

    # Initial values.
    for i in line:
        for j in line:
            if initial_grid[i][j]:
                model.Add(grid[(i, j)] == initial_grid[i][j])

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE:
        tab = []
        for i in line:
            tab.append([int(solver.Value(grid[(i, j)])) for j in line])
    return tab #return the sudoku solved

def print_sudoku(board):
    '''
    Method used for print the board properly.

    Parameters
    ----------
    board : Tab of Int
        Correspond of the grid.

    Returns
    -------
    None.

    '''
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")

if __name__ == '__main__':
    level = eval(input('Enter a number between 1 ans 5\n'))
    assert level > 0 and level < 6
    grid=generatePlate(level)
    print('unsolved sudoku grid :')
    print_sudoku(grid)
    print('\n')
    print('solved sudoku grid :')
    sovledgrid = solve_sudoku(grid)
    print_sudoku(sovledgrid)