import pygame  # type: ignore


def read_grid_from_file(filename):
    grid = []
    with open(filename, 'r') as file:
        # Read all lines and replace '*' with '0'
        lines = [line.strip() for line in file]
        # Initialize a grid with zeros (empty Sudoku grid)
        grid = [[0] * len(lines) for _ in range(len(lines[0]))]

        # Populate the grid by reading each line as a column
        for row_index, line in enumerate(lines):
            for col_index, char in enumerate(line):
                grid[col_index][row_index] = int(char) if char.isdigit() else 0
    return grid


def valid(grid, row, col, num):
    # check if num is in row or column
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    # check box
    box_row, box_col = row // 3, col // 3
    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):
            if grid[i][j] == num:
                return False
    return True


def update_screen(screen, grid, dif, font):
    screen.fill((255, 255, 255))
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, (0, 153, 153),
                                 (i * dif, j * dif, dif + 1, dif + 1))
                text = font.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text, (i * dif + 15, j * dif + 15))
    for i in range(10):
        thickness = 7 if i % 3 == 0 else 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif),
                         (500, i * dif), thickness)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0),
                         (i * dif, 500), thickness)
    pygame.display.update()
    pygame.time.delay(20)


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
