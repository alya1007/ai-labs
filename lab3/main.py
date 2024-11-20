import pygame  # type: ignore
from game import Game


def main():
    # Initialize pygame
    pygame.init()

    # Set up the game
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING")
    game = Game(screen)

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
                    game.solve()

    pygame.quit()


if __name__ == "__main__":
    main()
