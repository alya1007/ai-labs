import copy
import pygame  # type: ignore
import time
from typing import List, Optional, Set
from utils import update_screen


class ConstraintPropagator:
    def __init__(self, grid, screen, dif, font, frame_time=0.05):
        self.grid = grid
        self.screen = screen
        self.dif = dif  # Cell size
        self.font = font  # Font for rendering numbers
        self.frame_time = frame_time  # Time delay for visualization
        self.domains: List[List[Set[int]]] = [
            [set(range(1, 10)) if self.grid[i][j] ==
             0 else {self.grid[i][j]} for j in range(9)]
            for i in range(9)
        ]

    def solve(self):
        if not self.propagate_constraints():
            return False
        return self.backtrack()

    def propagate_constraints(self):
        changed = True
        while changed:
            changed = False
            for i in range(9):
                for j in range(9):
                    if len(self.domains[i][j]) == 1:
                        num = next(iter(self.domains[i][j]))
                        eliminated = self.eliminate(i, j, num)
                        if eliminated is None:
                            return False  # Failure due to empty domain
                        changed |= eliminated
        return True

    def eliminate(self, row: int, col: int, num: int) -> Optional[bool]:
        changed = False
        # Eliminate from row
        for j in range(9):
            if j != col and num in self.domains[row][j]:
                self.domains[row][j].remove(num)
                if not self.domains[row][j]:
                    return None  # Failure due to empty domain
                changed = True
        # Eliminate from column
        for i in range(9):
            if i != row and num in self.domains[i][col]:
                self.domains[i][col].remove(num)
                if not self.domains[i][col]:
                    return None
                changed = True
        # Eliminate from block
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                r, c = start_row + i, start_col + j
                if (r != row or c != col) and num in self.domains[r][c]:
                    self.domains[r][c].remove(num)
                    if not self.domains[r][c]:
                        return None
                    changed = True
        return changed

    def backtrack(self):
        # Find the unassigned cell with the smallest domain
        unassigned_cells = [
            (i, j) for i in range(9) for j in range(9) if len(self.domains[i][j]) > 1
        ]
        if not unassigned_cells:
            # All variables assigned
            for i in range(9):
                for j in range(9):
                    if not self.domains[i][j]:
                        return False  # Empty domain, failure
                    self.grid[i][j] = next(iter(self.domains[i][j]))
            return True

        row, col = unassigned_cells[0]

        for value in self.domains[row][col].copy():
            saved_domains = copy.deepcopy(self.domains)
            self.domains[row][col] = {value}
            # Update the grid for visualization
            self.grid[row][col] = value
            update_screen(self.screen, self.grid, self.dif, self.font)
            time.sleep(self.frame_time)

            if self.propagate_constraints():
                if self.backtrack():
                    return True
            # Backtrack
            self.domains = saved_domains
            self.grid[row][col] = 0
            update_screen(self.screen, self.grid, self.dif, self.font)
            time.sleep(self.frame_time)
        return False
