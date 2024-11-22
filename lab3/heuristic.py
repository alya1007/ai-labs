import copy
import pygame  # type: ignore
import time
from typing import List, Optional, Set
from utils import update_screen


class HeuristicConstraintPropagator:
    def __init__(self, grid, screen, dif, font, frame_time=0.0005):
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

        while True:
            # Find unassigned cells
            unassigned_cells = [
                (i, j) for i in range(9) for j in range(9) if len(self.domains[i][j]) > 1
            ]
            if not unassigned_cells:
                # All variables assigned
                for i in range(9):
                    for j in range(9):
                        self.grid[i][j] = next(iter(self.domains[i][j]))
                return True

            # Select cell with MRV (Minimum Remaining Values)
            unassigned_cells.sort(key=lambda cell: len(
                self.domains[cell[0]][cell[1]]))
            row, col = unassigned_cells[0]
            domain = self.domains[row][col]

            # Select value using LCV (Least Constraining Value) heuristic
            value_scores = []
            for value in domain:
                score = self.calculate_lcv_score(row, col, value)
                value_scores.append((score, value))
            # Sort values by score (least constraining first)
            value_scores.sort()
            value = value_scores[0][1]

            # Assign the value
            self.domains[row][col] = {value}
            self.grid[row][col] = value
            update_screen(self.screen, self.grid, self.dif, self.font)
            time.sleep(self.frame_time)

            # Apply constraint propagation
            if not self.propagate_constraints():
                return False  # Failure due to empty domain

    def calculate_lcv_score(self, row, col, value):
        # Calculate how constraining this value is
        # The score is the total number of possible values eliminated from neighboring cells
        score = 0
        # For each neighbor, if value is in their domain, increment score
        peers = self.get_peers(row, col)
        for r, c in peers:
            if value in self.domains[r][c]:
                score += 1
        return score

    def get_peers(self, row, col):
        peers = set()
        # Row and column peers
        for i in range(9):
            if i != col:
                peers.add((row, i))
            if i != row:
                peers.add((i, col))
        # Block peers
        start_row, start_col = 3*(row//3), 3*(col//3)
        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if (i, j) != (row, col):
                    peers.add((i, j))
        return peers

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
                        # Update grid for visualization
                        self.grid[i][j] = num
                        update_screen(self.screen, self.grid,
                                      self.dif, self.font)
                        time.sleep(self.frame_time)
        return True

    def eliminate(self, row: int, col: int, num: int) -> Optional[bool]:
        changed = False
        # Eliminate num from the domains of peers
        peers = self.get_peers(row, col)
        for r, c in peers:
            if num in self.domains[r][c]:
                self.domains[r][c].remove(num)
                if not self.domains[r][c]:
                    return None  # Failure due to empty domain
                changed = True
        return changed
