import random
import time
from math import trunc

DIM = 0  # Dimension of the board (n value)
board = []  # Stores the board
row_conflicts = []  # Keeps track of row conflicts
diagL_conflicts = []  # Keeps track of left diagonal conflicts
diagR_conflicts = []  # Keeps track of right diagonal conflicts


# Read in the test n dimensions of the file into a list and return
def readInFile():
    with open("nqueens_input.txt", "r") as file:
        dimensionArray = []
        for line in file:
            dimensionArray.append(int(line.rstrip("\n")))
    file.close()
    # Prep & clear contents of output file
    open("nqueens_output.txt", "w").close()
    return dimensionArray


# Append the solution array to the output file
def writeToFile():
    with open("nqueens_output.txt", "a", 64) as file:
        file.write(str(board) + "\n\n")
    file.close()


# Updates the conflict table with new conflicts from the updated queen position
# When the parameter val is 1 it will add a conflict to the global lists
# When the parameter val as -1, it will subtract a conflict to the global lists
# The values in the conflict arrays represent the number of queens in each row or diagonal
#       (i.e. a count of 1 indicates no conflict because there is only one queen in the row or diagonal)
def changeConflicts(col, row, val):
    row_conflicts[row] += val
    diagL_conflicts[col + row] += val
    diagR_conflicts[col + (DIM - row - 1)] += val


# Sets up the board using a greedy algorithm
def createBoard():
    global board
    global row_conflicts
    global diagL_conflicts
    global diagR_conflicts

    # Begin with an empty board
    board = []

    # Initialize the conflict arrays
    # The diagonal conflict lists are the size of the number of diagonals of the board
    diagL_conflicts = [0] * ((2 * DIM) - 1)
    diagR_conflicts = [0] * ((2 * DIM) - 1)
    row_conflicts = [0] * DIM

    # Create an ordered list of all possible row values
    rowList = [*range(DIM)]
    # Create a list to keep track of which queens have not been placed
    notPlaced = []

    iteration = 0
    maxIteration = DIM // 2  # Define the maximum iterations as 0.5 * size of board
    randIdx = -1  # Random index
    testRow = -1  # Possible row location
    conflicts = 0  # Number of conflicts

    for col in range(DIM):
        iteration = 0
        while iteration < maxIteration:
            randIdx = random.randrange(len(rowList))
            rowList[randIdx], rowList[-1] = rowList[-1], rowList[randIdx]
            # Pop the next possible row location to test
            testRow = rowList.pop()
            # Calculate the conflicts for potential location
            conflicts = (
                row_conflicts[testRow]
                + diagL_conflicts[col + testRow]
                + diagR_conflicts[col + (DIM - testRow - 1)]
            )
            # If there are no conflicts, place a queen in that location on the board
            if conflicts == 0:
                board.append(testRow)
                changeConflicts(col, board[col], 1)
                break
            # If a conflict is found...
            else:
                # Place the potential row to the back of the set
                rowList.append(testRow)
                iteration += 1

        if iteration == maxIteration:
            # Add a None to the board to hold the place of the potential queen
            board.append(None)
            # Keep track of which column was not placed to be handled later
            notPlaced.append(col)

    for col in notPlaced:
        # Place the remaining queen locations
        board[col] = rowList.pop()
        # Update the conflict lists
        changeConflicts(col, board[col], 1)


# Finds the column with the most conflicts
def findMaxConflictCol():
    conflicts = 0
    maxConflicts = 0
    maxConflictCols = []

    for col in range(DIM):
        # Determine the row value for the current column
        row = board[col]
        # Calculate the number of conflicts using the conflict lists
        conflicts = (
            row_conflicts[row]
            + diagL_conflicts[col + row]
            + diagR_conflicts[col + (DIM - row - 1)]
        )
        # If conflicts are greater than the current max, make that column the maximum
        if conflicts > maxConflicts:
            maxConflictCols = [col]
            maxConflicts = conflicts
        # If the conflicts equal the current max, append the index value to the maxConflictCols list
        elif conflicts == maxConflicts:
            maxConflictCols.append(col)

    # Randomly choose column from the list of tied maximums
    choice = random.choice(maxConflictCols)
    return choice, maxConflicts


# Finds the index of the best new queen position. Ties are broken randomly.
# Parameter: the current column index
def minConflictPos(col):
    minConflicts = DIM
    minConflictRows = []

    for row in range(DIM):
        # Calculate the number of conflicts using the conflict arrays
        conflicts = (
            row_conflicts[row]
            + diagL_conflicts[col + row]
            + diagR_conflicts[col + (DIM - row - 1)]
        )
        # If there are no conflicts in a row, immediately return that row value
        if conflicts == 0:
            return row
        # If the number of conflicts is less, change it to the minConflicts value
        if conflicts < minConflicts:
            minConflictRows = [row]
            minConflicts = conflicts
        # If the number of conflicts is equal, append the index instead of changing it
        elif conflicts == minConflicts:
            minConflictRows.append(row)

    # Randomly choose the index from the list of tied conflict values
    choice = random.choice(minConflictRows)
    return choice


# Sets up the board using createBoard() and then solves it with a min-conflict algorithm
def solveNQueens():
    createBoard()
    iteration = 0
    maxIteration = DIM // 2  # Define the maximum iterations as 0.5 * size of board

    while iteration < maxIteration:
        # Calculate the maximum conflicting column and the number of conflicts it contains
        col, numConflicts = findMaxConflictCol()
        # If the number of queens in the row, and diagonals is greater than 1 each (i.e. there are conflicts)
        if numConflicts > 3:
            # Use the minConflictPos() function to determine the row index with the least number of conflicts
            newLocation = minConflictPos(col)
            # If the better location is not its current location, switch the location
            if newLocation != board[col]:
                # Remove the conflicts from the position the queen is leaving
                changeConflicts(col, board[col], -1)
                board[col] = newLocation
                # Add a conflict to the position the queen is entering
                changeConflicts(col, newLocation, 1)
        # If the max number of conflicts (i.e. the number of queens in each row and diagonals) on the board
        # equals 3, then there are no conflicts since the queen is alone in it's row and both diagonals
        elif numConflicts == 3:
            # Solution is found
            return True
        iteration += 1
    # If no solution is found in under average number of iterations, return False
    return False


def main():
    global DIM
    global board
    global row_conflicts
    global diagL_conflicts
    global diagR_conflicts

    # Read in the file containing the DIM values
    dimensionArray = readInFile()

    for dimension in dimensionArray:
        # If the dimension is outside the constraints
        if dimension <= 3 or dimension > 10000000:
            # Print error and write empty array to file
            print("Cannot build board of size: " + str(dimension))
            writeToFile()
        else:
            # Set DIM equal to the current test dimension
            DIM = dimension
            # Start timer and set/reset boolean
            time0 = time.time()
            solved = False
            print("Searching for board configuration of size " + str(dimension) + "...")
            # Continues restarting solveNQueens() until a solution is found
            while not solved:
                # Solved will be True when a solution is returned
                solved = solveNQueens()

            print("Board configuration found for size " + str(dimension))

            writeToFile()

            # Calculate and print time taken to find solution
            time1 = time.time()
            tot_time = time1 - time0
            time_string = str(trunc(tot_time * 100) / 100)
            print("   Took " + time_string + " seconds\n")


if __name__ == "__main__":
    main()
