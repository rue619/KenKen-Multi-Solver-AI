# KenKen Multi-Solver AI

A Python desktop application that explores two approaches to solving KenKen mathematical puzzles: a Genetic Algorithm and Backtracking.

## Project Overview

This project combines algorithmic problem-solving with a graphical user interface built using Tkinter. It visualizes the puzzle grid and allows users to select different solving approaches.

## Features

- Interactive desktop interface using Tkinter
- Genetic Algorithm with fitness evaluation, crossover, and mutation
- Backtracking algorithm with constraint checking
- Visual progress while the backtracking solver searches for a solution
- Color-coded puzzle cages and mathematical targets
- Reset functionality

## Technologies Used

- Python
- Tkinter
- Genetic Algorithms
- Backtracking
- Randomized Search
- Mathematical Constraint Checking

## How to Run

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python full.py
   ```

Tkinter is included with many standard Python installations. No third-party Python packages are required for the current implementation.

## Algorithms

**Genetic Algorithm:** Generates candidate grids and evaluates them using column uniqueness and cage constraints. It applies selection, crossover, and mutation to evolve candidates.

**Backtracking:** Searches for a valid grid by assigning numbers, checking constraints, and undoing assignments when a choice fails.

## Learning Objectives

This project demonstrates algorithm design, constraint satisfaction, optimization concepts, Python programming, and desktop GUI development.

## Future Improvements

- Support puzzles of different sizes
- Improve Genetic Algorithm selection and convergence
- Add more puzzle configurations
- Display solving statistics and execution time
- Improve error handling and solution validation

## Author

Raheel Romani
