import random
from typing import List, Optional
from utils import valid


class SudokuGridGenerator:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Empty 9x9 grid

    def generate_complete_grid(self):
        return self._fill_grid(0, 0)  # Start filling from the top-left cell

    def _fill_grid(self, row, col):
        if row == 9:  # Reached the end of the grid
            return True
        next_row, next_col = (row + 1, 0) if col == 8 else (row, col + 1)

        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Shuffle numbers to create randomness

        for num in numbers:
            if valid(self.grid, row, col, num):
                self.grid[row][col] = num
                if self._fill_grid(next_row, next_col):
                    return True
                self.grid[row][col] = 0  # Backtrack
        return False

    def remove_numbers(self, num_holes):
        """
        Remove numbers from the grid to create a Sudoku puzzle.
        """
        positions = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(positions)

        for _ in range(num_holes):
            if not positions:
                break
            row, col = positions.pop()
            self.grid[row][col] = 0

    def generate(self, num_holes):
        """
        Generates a valid Sudoku puzzle with a specified number of empty cells.
        """
        if self.generate_complete_grid():
            self.remove_numbers(num_holes)
        return self.grid
