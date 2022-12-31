# Intelligent Sudoku Solver

## Information
The following is a Python 3 implementation of a Constraint Satisfaction solver for Sudoku using the [AC3 (Arc consistency)](https://en.wikipedia.org/wiki/AC-3_algorithm) algorithm to reduce the state space during search.

This application uses recursive backtracking using both the FA (First Available) and MRV (Minimum Residual Value) variable selection algorithms, and after running, will generate a scatterplot of all the problems that were solved, comparing the runtime of the solver for the FA and MRV selection algorithms. 

An example scatter plot using the base `problems.txt` is included in this repo as `example-plot.png`.


## Usage Guide

### Installation
Run the following commands to set up a virtual environment and install the necessary packages for running the application
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Adding Sudoku Puzzles
The repository comes with 95 sample sudoku problems for the solver all under `problems.txt`. In this file, a problem is represented on a single line of the following format:
```
4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
``` 
Since a sudoku problem can be represented by a 9x9 grid, each set of 9 characters in the string represents a 'row' of the grid, where '.' represents an empty tile.

The application is configured to run each of the problems in this file, so feel free to edit the problems in here as necessary.

## Running the application / generating plots
You can run the application via the following command
```
python3 main.py
```
This will solve all the sudoku puzzles in the problems.txt file and print the solved puzzle out to the console. Additionally, a runtime comparison scatterplot for each of the problems (between the FA and MRV variable selection algorithms) will be generated as `running_time.png`

