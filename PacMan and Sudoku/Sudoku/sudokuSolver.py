#!/usr/bin/python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
# SUDOKU SOLVER

import sys
import copy
from time import time
from sudokuUtil import *
from Queue import Queue


# Please implement function solve_puzzle
# input puzzle: 2D list, for example:
# [ [0,9,5,0,3,2,0,6,4]
#   [0,0,0,0,6,0,1,0,0]
#   [6,0,0,0,0,0,0,0,0]
#   [2,0,0,9,0,3,0,0,6]
#   [0,7,6,0,0,0,0,0,3]
#   [3,0,0,0,0,0,0,0,0]
#   [9,0,0,5,0,4,7,0,1]
#   [0,5,0,0,2,1,0,9,0]
#   [0,0,8,0,0,6,3,0,5] ]
# Return a 2D list with all 0s replaced by 1 to 9.
# You can utilize argv to distinguish between algorithms
# (basic backtracking or with MRV and forward checking).
# For example: python sudokuSolver.py backtracking

class SudokuLab:

    def __init__(self, puzzle):
        '''
        Contains the various cells in sudoku
        '''

        self.domain = {}
        self.empty = []
        self.domain = {}
        self.nodes=0
        self.puzzle = copy.copy(puzzle)
        for i in range(9):
            for j in range(9):
                val = self.puzzle[i][j]
                if val == 0:
                    self.empty.append((i, j))
                    continue
    #Checks whether num value is possible in given row
    def checkRow(self, row, num):
        for col in range(9):
            currentValue = self.puzzle[row][col]
            if num == currentValue:
                return False
        return True
    #Checkes whether   num value is possible in given column
    def checkColumn(self, col, num):
        for row in range(9):
            currentValue = self.puzzle[row][col]
            if num == currentValue:
                return False
        return True
    #Checks whether goal state has been reached or not
    def isSudokuDone(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    return False
        return True
    #get unassigned cells in the sudoku
    def getUnassignedCells(self):
        cells = []
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    cells.append((row, col))
        return cells
    #Checks wheter given num is possible in given sub-square
    def checkBox(
        self,
        row,
        col,
        num,
        ):

        row = row / 3 * 3
        col = col / 3 * 3
        for r in range(3):
            for c in range(3):
                if self.puzzle[row + r][col + c] == num:
                    return False
        return True

    # Get neighboring cells in row

    def getRowBlanks(self, puzzle, row):
        cells = []
        for col in range(9):
            if puzzle[row][col] == 0:
                cells.append((row, col))
        return cells
    # Get neighboring cells in column
    def getColumnBlanks(self, puzzle, col):
        cells = []
        for row in range(9):
            if puzzle[row][col] == 0:
                cells.append((row, col))
        return cells
    # Get neighboring cells in box
    def getBoxBlanks(
        self,
        puzzle,
        row,
        col,
        ):

        cells = []
        row = row / 3 * 3
        col = col / 3 * 3
        for r in range(3):
            for c in range(3):
                if puzzle[row + r][col + c] == 0:
                    cells.append((row + r, col + c))
        return cells
    #  Get neighboring empty blanks of cell 
    def getNeighborBlanks(self, cell):
        row = cell[0]
        col = cell[1]
        neighbors = []
        associatedBlanks = self.getRowBlanks(self.puzzle, row) \
            + self.getColumnBlanks(self.puzzle, col) \
            + self.getBoxBlanks(self.puzzle, row, col)
        for blank in associatedBlanks:
            if blank not in neighbors and blank != (row, col):

           # Might be that current box collided with row / col so check here

                neighbors.append(blank)
        return neighbors

    def getPossibleValues(self, cell):
        row = cell[0]
        col = cell[1]
        allowed = []
        for i in range(1, 10):
            if self.sudokuValid(row, col, i):
                allowed.append(i)

        return allowed

    def sudokuValid(
        self,
        row,
        col,
        num,
        ):

    # Return true if row, column, and box have no violations

        valid = False
        rowValid = self.checkRow(row, num)
        colValid = self.checkColumn(col, num)
        boxValid = self.checkBox(row, col, num)
        valid = rowValid & colValid & boxValid
        return valid
    #Forward check
    def pruneIsvalidInForwardCheck(self, cell, num):

        # Get all the neighbors

        neighbors = self.getNeighborBlanks(cell)
        for neighborBlank in neighbors:
            neighborDomain = self.domain[neighborBlank]
            if num in neighborDomain:
                self.domain[neighborBlank].remove(num)
                if len(self.domain[neighborBlank]) == 0:  # Detect empty domain
                    return False
        return True

# Returns the variable with minimum Remaining Legal values

    def getMrvCell(self):

        # Build the MRV priority queue
        '''
        q = PriorityQueue()
        c

           # possible = self.getPossibleValues(emptyCell)

            possible = len(self.domain[emptyCell])
            q.put((possible, emptyCell))
        return q.get(0)[1]
        '''
        mini=float('inf')
        for emptyCell in self.empty:
           possible = len(self.domain[emptyCell])
           if(possible<mini):
              mini=possible
              cell=emptyCell
        return cell
    def puzzleSolution(self):
        return self.puzzle
    #backtrack
    def backtrack(self, index):
        if self.isSudokuDone() == True:
            return True
        self.nodes+=1
        cell = self.empty[index]
        for val in range(1, 10):
            if self.sudokuValid(cell[0], cell[1], val) == True:
                self.puzzle[cell[0]][cell[1]] = val
                #print 'index='+str(index)+ 'val='+str(val)
                if self.backtrack(index + 1) == True:
                    return True
                self.puzzle[cell[0]][cell[1]] = 0
        return False
    #arc consistency propagation.AC3 algorithm
    def propagateConstraints(self):
        
        queue = Queue()  # Build a queue of all arcs in the grid
        for probableSingleCell in self.empty:
            if len(self.domain[probableSingleCell]) == 1:

          # Get neighbours of current emptyCell

                neighbors = self.getNeighborBlanks(probableSingleCell)

          # Create a arc which would be checked from all such neighbours
          # to cells of domain length=1

                for neighbor in neighbors:
                    if len(self.domain[neighbor]) != 1:
                      queue.put((neighbor, probableSingleCell))
        while not queue.empty():
            arc = queue.get()
            src = arc[0]
            dest = arc[1]
            singleCellValue = self.domain[dest]
            srcDomain = self.domain[src]
            if singleCellValue in srcDomain:
                #We can't remove singleCellValue from srcDomain.As this would
                #cause inconsistency.backtrack
                if len(srcDomain == 1):
                    return False
                else:
                    self.domain[src].remove(singleCellValue)
                    #Insert an arc, if domain length becomes 1
                    if len(self.domain[src]) == 1:
                        neighbors = self.getNeighborBlanks(src)
                        for neighbor in neighbors:
                            if neighbor != (dest[0], dest[1]) and len(self.domain[neighbor]) != 1:
                                queue.put((neighbor, src))
        return True


    #preprocessing for our heuristic
    def processVariablesForHeuristic(self):

        # Construct the dictionary

        for emptyCell in self.empty:
            possibleValues = self.getPossibleValues(emptyCell)
            self.domain[emptyCell] = possibleValues
    #Substitute for deepcopy to achieve better times
    def copyDomain(self,domain):
        copiedDomain={}
        for dictKey in domain.keys():
          copiedDomain[dictKey]=[]
          for value in domain[dictKey]:
            copiedDomain[dictKey].append(value)
        return copiedDomain
    def heuristic(self):

  # check for goal

        if self.isSudokuDone() == True:
            return True
        self.nodes+=1
  # Select MRV variable

        mrvCell = self.getMrvCell()

  # mrvCell is of the form (0,0),(1,1),(2,2)

  # Try to assign each of the values in domain to the variable
        currentDomain=self.domain[mrvCell]
        for val in currentDomain:

            # Copy of current domain before pruning

            tempDomain = self.copyDomain(self.domain)

            # If forward checking fails, then proceed to next value in the domain

            if self.pruneIsvalidInForwardCheck( mrvCell, val) \
                == True:

          # Arc propagation begins here
          # Mark domain of current cell as val

                self.domain[mrvCell] = [val]

          # Start arc propagation

                if self.propagateConstraints() == True:
                    row = mrvCell[0]
                    col = mrvCell[1]
                    self.puzzle[row][col] = val
                    self.empty.remove(mrvCell)
                    if self.heuristic() == True:
                        return True
                    self.empty.append(mrvCell)
                    self.puzzle[row][col] = 0

            # Backtrack

            self.domain = tempDomain

    # Try Forward checking

        return False

'''
python sudokuSolver.py b :-backtrack
python sudokuSolver.py h :-heuristic

'''
def solve_puzzle(puzzle, argv):
   
    """Solve the sudoku puzzle."""
    if(len(argv)!=2):
      print "please provide arguments in the format python sudokuSolver.py b"
    arg=argv[1]
    sudoku = SudokuLab(puzzle)
    if arg == 'b':
        if sudoku.backtrack(0) == False:
            print "problem with generating solution"
    elif arg=='h':
        sudoku.processVariablesForHeuristic()
        if sudoku.heuristic() == True:
            print "problem with generating solution"
    else:
        print "Please provide which method to use in proper format"
    print 'Nodes expanded='+str(sudoku.nodes)
    solution = sudoku.puzzleSolution()
    return solution


# ===================================================#

puzzle = load_sudoku('puzzle.txt')

print 'solving ...'
t0 = time()
solution = solve_puzzle(puzzle, sys.argv)
t1 = time()
print 'completed. time usage: %f' % (t1 - t0), 'secs.'

save_sudoku('solution.txt', solution)


      