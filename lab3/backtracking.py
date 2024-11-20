import pygame  # type: ignore
from utils import valid, update_screen


def backtrack(grid, screen, dif, font):
    def solve(grid, row, col):
        while grid[row][col] != 0:
            if row < 8:
                row += 1
            elif row == 8 and col < 8:
                row = 0
                col += 1
            elif row == 8 and col == 8:
                return True
        pygame.event.pump()
        for num in range(1, 10):
            if valid(grid, row, col, num):
                grid[row][col] = num  # Place the number
                update_screen(screen, grid, dif, font)  # Update screen

                if solve(grid, row, col):  # Recursively solve the next cell
                    return True  # Return success if the next cell solves

                grid[row][col] = 0  # Backtrack: reset the cell
                update_screen(screen, grid, dif, font)  # Update screen
        return False

    solve(grid, 0, 0)
