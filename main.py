import time
from grid import Grid
from plot_results import PlotResults

def ac3(grid, var):
    """
        This is a domain-specific implementation of AC3 for Sudoku. 

        It keeps a set of arcs to be processed (arcs) which is provided as input to the method. 
        Since this is a domain-specific implementation, we don't need to maintain a graph and a set 
        of arcs in memory. We can store in arcs the cells of the grid and, when processing a cell, 
        we ensure arc consistency of all variables related to this cell by removing the value of
        cell from all variables in its column, row, and unit. 

        For example, if the method is used as a preprocessing step, then arcs is initialized with 
        all cells that start with a number on the grid. This method ensures arc consistency by
        removing from the domain of all variables in the row, column and unit the values of 
        the cells given as input. The method adds to the set of arcs all variables that have
        their values assigned during the propagation of the contrains. 
    """
    if not type(var) == list:
        arcs = [var]
    else:
        arcs = var
    checked = set()
    while len(arcs):
        cell = arcs.pop()
        checked.add(cell)

        assigned_row, failure = grid.remove_domain_row(cell[0], cell[1])
        if failure: return failure

        assigned_column, failure = grid.remove_domain_column(cell[0], cell[1])
        if failure: return failure

        assigned_unit, failure = grid.remove_domain_unit(cell[0], cell[1])
        if failure: return failure

        arcs.extend(assigned_row)
        arcs.extend(assigned_column)
        arcs.extend(assigned_unit)    
    return False

def pre_process_ac3(grid):
    """
    This method enforces arc consistency for the initial grid of the puzzle.

    The method runs AC3 for the arcs involving the variables whose values are 
    already assigned in the initial grid. 
    """
    arcs_to_make_consistent = []

    for i in range(grid.get_width()):
        for j in range(grid.get_width()):
            if len(grid.get_cells()[i][j]) == 1:
                arcs_to_make_consistent.append((i, j))

    return ac3(grid, arcs_to_make_consistent)

def select_variable_fa(grid: Grid):
    # Iterate through all grid cells until we find a 
    # cell (variable) whos domain is of size > 1
    # Returns the row/col of the first cell that is found
    # matching this condition as a tuple (row, col).
    for row in range(grid.get_width()):
        for col in range(grid.get_width()):
            if len(grid.get_cells()[row][col]) > 1:
                return row, col

def select_variable_mrv(grid: Grid):
    # Start at 10, impossible and pessimistic
    # try to find the minimum domain length in the entire grid
    smallest = 10
    for row in range(grid.get_width()):
        for col in range(grid.get_width()):
            if len(grid.get_cells()[row][col]) == 1:
                continue
            smallest = min(smallest, len(grid.get_cells()[row][col]))
    # Iterate through the grid once more to find the first cell
    # that has the minimum domain length found in the previous loop
    for row in range(grid.get_width()):
        for col in range(grid.get_width()):
            if len(grid.get_cells()[row][col]) == smallest:
                return row, col

# Function which starts the recursion and runs pre-processing
def backtracking(grid: Grid, var_selector):
    ac3_failure = pre_process_ac3(grid)
    if ac3_failure:
        return None, False
    return search(grid, var_selector)

def search(grid: Grid, var_selector):
    # Return the grid is the puzzle is solved
    if grid.is_solved():
        return grid, True 
    # var_selector here is a heuristic function (fa or mrv)
    var = var_selector(grid)
    # Iterate over the domain of the variable selected by 
    # the h-function (var_selector) and check for consistency.
    # If we find a value in the domain that is consistent with the
    # selected variable, create a copy of the grid, set the domain
    # of the variable in the copy to the selected domain value,
    # and recurse on the new grid.
    for d in grid.get_cells()[var[0]][var[1]]:
        if is_consistent(grid, var, d):
            grid_copy = grid.copy()
            grid_copy.get_cells()[var[0]][var[1]] = d
            # Run ac3 here to simplify the problem
            # If fails, backtrack immedietely
            ac3_failure = ac3(grid_copy, var)
            if ac3_failure:
                continue
            rb = search(grid_copy, var_selector)
            # If the search function returns True,
            # it means that the algorithm found a solution,
            # and we can return.
            if rb[1]:
                return rb
    # Return None, False if no solution could be found with the
    # current grid state.
    return None, False

# Helper function which if given a move and a grid position
# determines if the specified domain value is a valid move at
# that position.
def is_consistent(grid: Grid, var, domain_val):
    # Check if the row constraint is satisfied
    row = grid.get_cells()[var[0]]
    for value in row:
        if value == domain_val:
            return False
    # Check if the column constraint is satisfied
    # The following line grabs all the values in var's column
    col = [grid_row[var[1]] for grid_row in grid.get_cells()]
    for value in col:
        if value == domain_val:
            return False
    # Check if the 'unit' contraint is satisfied
    # The following lines grab all the values in var's 3x3 'unit'
    block_start_row = var[0] // 3
    block_start_col = var[1] // 3
    for i in range(3):
        for j in range(3):
            if grid.get_cells()[(block_start_row * 3) + i][(block_start_col * 3) + j] == domain_val:
                return False
    # Return True if we pass all contraints
    return True

running_time_mrv = []
running_time_first_available = []

file = open('problems.txt', 'r')
problems = file.readlines()

# Full test for MRV
for p in problems:
    g = Grid()
    g.read_file(p)
    start = time.time()
    result, success = backtracking(g, select_variable_mrv)
    if (result):
        result.print()
    end = time.time()
    running_time_mrv.append(end - start)
    print("Finished MRV!")


# Full test for FA 
for p in problems:
    g = Grid()
    g.read_file(p)
    start = time.time()
    result, success = backtracking(g, select_variable_fa)
    if (result):
        result.print()
    end = time.time()
    running_time_first_available.append(end - start)
    print("Finished FA!")

# Create the scatterplot of results
plotter = PlotResults()
plotter.plot_results(running_time_mrv, running_time_first_available,
"Running Time Backtracking (MRV)",
"Running Time Backtracking (FA)", "running_time")