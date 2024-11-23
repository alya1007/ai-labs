import pygame  # type: ignore
import argparse
from game import Game
from backtracking import backtrack
from constraint_propagation import ConstraintPropagator
from heuristic import HeuristicConstraintPropagator
from grid_generator import SudokuGridGenerator


def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument(
        "--bt", action="store_true", help="Use the backtracking solver"
    )
    parser.add_argument(
        "--cp", action="store_true", help="Use the constraint propagation solver"
    )
    parser.add_argument(
        "--he", action="store_true", help="Use the constraint propagation solver with heuristics"
    )
    parser.add_argument(
        "--generate", action="store_true", help="Generate a new sudoku grid"
    )

    args = parser.parse_args()

    # Initialize pygame
    pygame.init()

    # Set up the game
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
    if args.generate:
        game = Game(screen, True)
    else:
        game = Game(screen, False)

    cp = ConstraintPropagator(game.grid, screen, game.dif, game.font_large)

    he = HeuristicConstraintPropagator(
        game.grid, screen, game.dif, game.font_large)

    # Main game loop
    run = True
    while run:
        screen.fill((255, 255, 255))
        game.draw()
        game.display_instructions()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    game.reset_to_default()
                elif event.key == pygame.K_RETURN:
                    if args.bt:
                        backtrack(game.grid, screen, game.dif, game.font_large)
                    elif args.cp:
                        cp.solve()
                    elif args.he:
                        he.solve()

    pygame.quit()


if __name__ == "__main__":
    main()
