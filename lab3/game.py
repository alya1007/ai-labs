import pygame  # type: ignore
from utils import backtrack, read_grid_from_file


class Game:
    def __init__(self, screen):
        self.screen = screen  # Pygame screen
        self.dif = 500 / 9  # Size of each cell
        self.font_large = pygame.font.SysFont("comicsans", 40)
        self.font_small = pygame.font.SysFont("comicsans", 20)
        # self.default_grid = [
        #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
        #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
        #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
        #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
        #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
        #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
        #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
        #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
        #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
        # ]
        self.default_grid = read_grid_from_file("grid.txt")
        self.grid = [row[:] for row in self.default_grid]

    def draw(self):
        # Draw numbers and filled cells
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    pygame.draw.rect(self.screen, (0, 153, 153),
                                     (i * self.dif, j * self.dif, self.dif + 1, self.dif + 1))
                    text = self.font_large.render(
                        str(self.grid[i][j]), 1, (0, 0, 0))
                    self.screen.blit(
                        text, (i * self.dif + 15, j * self.dif + 15))

        # Draw grid lines
        for i in range(10):
            thickness = 7 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * self.dif), (500, i * self.dif), thickness)
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * self.dif, 0), (i * self.dif, 500), thickness)

    def display_instructions(self):
        text = self.font_small.render(
            "D - RESET TO DEFAULT / ENTER - SOLVE", 1, (0, 0, 0))
        self.screen.blit(text, (20, 520))

    def reset_to_default(self):
        self.grid = [row[:] for row in self.default_grid]

    def solve(self):
        backtrack(self.grid, self.screen, self.dif, self.font_large)
