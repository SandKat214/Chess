import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_n, K_y, MOUSEBUTTONDOWN, QUIT
from constants import HEIGHT, SQUARE_SIZE, UNFINISHED, WIDTH
from classes.game import Game

# Initialize pygame
pygame.init()

# Frames per second
FPS = 60

# Set game window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Var')


def get_row_col_from_mouse(position):
    """Takes mouse position as argument and returns the corresponding row & column
    position in the game grid.
    """
    x_coord, y_coord = position
    row = y_coord // SQUARE_SIZE
    col = x_coord // SQUARE_SIZE
    return row, col


def main():
    """Main game loop."""
    running = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while running:
        # Sets tempo of the loop
        clock.tick(FPS)

        for event in pygame.event.get():
            # If the red 'x' is clicked
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                # If the 'esc' key is pressed
                if event.key == K_ESCAPE:
                    running = False

                # Game Over
                if game.get_winner() != UNFINISHED:
                    # Play again?
                    if event.key == K_y:
                        game.reset()
                    elif event.key == K_n:
                        running = False

            # If mouse button clicked
            elif event.type == MOUSEBUTTONDOWN and game.get_winner() == UNFINISHED:
                position = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(position)
                game.choose(row, col)

        # Update board
        game.display()

    pygame.quit()


if __name__ == '__main__':
    main()
