import pygame
from constants import HEIGHT, PLAYER_WHITE, PLAYER_BLACK, WIDTH, UNFINISHED
from .board import Board


class Game:
    """Represents a game of the chess variant. This class is responsible
    for the aspects of the game having to do with active play, such as
    making a move, keeping track of the current turn, and displaying the
    current state of the board. Works directly with the Board class to
    know what object currently occupies a board position, update the board
    when a successful move is made, and to determine the current game state.
    """
    # class constants
    FONT_SIZE = WIDTH // 20
    BACKGROUND = (0, 0, 0)
    TEXT = (255, 255, 255)

    def __init__(self, window):
        """Starts a ChessVar game. Takes the game window as parameter and
        initializes further data members via the reset function.
        """
        self._window = window
        self.reset()

    def reset(self):
        """Starts/Resets board for new game."""
        self._board = Board()
        self._turn = PLAYER_WHITE
        self._chosen = None
        self._valid_moves = []

    def get_turn(self):
        """Takes no parameters and returns the turn data member."""
        return self._turn

    def update_turn(self):
        """Takes no parameters. Signals a new turn and updates the turn data
        member to the other team.
        """
        if self._turn == PLAYER_WHITE:
            self._turn = PLAYER_BLACK
        else:
            self._turn = PLAYER_WHITE

    def display(self):
        """Takes no parameters. Displays the current state of the game."""
        self._board.draw(self._window)
        if self.get_winner() != UNFINISHED:
            winner = self.get_winner()
            if winner == PLAYER_BLACK:
                self.display_message(f'{PLAYER_BLACK} Wins! Play again: y or n?')
            else:
                self.display_message(f'{PLAYER_WHITE} Wins! Play again: y or n?')

        # Update Board
        pygame.display.update()

    def get_winner(self):
        """Takes no parameters. Checks the current state of the pieces on
        the board and, if warranted, returns the winning team.
        Otherwise, UNFINISHED.
        """
        for piece, value in self._board.get_pieces().items():
            # If a player has lost
            if value <= 0:
                if piece[0] == PLAYER_WHITE:
                    return PLAYER_BLACK
                else:
                    return PLAYER_WHITE

        # If no one has lost
        return UNFINISHED

    def choose(self, row, col):
        """Gets piece clicked by mouse and checks validity of piece moving or
        where it's moving to. Gives warning for any invalid choices.
        """
        # if moving piece is already chosen
        if self._chosen:
            return self.make_move(self._chosen, row, col)

        piece = self._board.get_piece(row, col)
        # check validity
        if piece is not None and piece.get_team() == self._turn:
            self._valid_moves = piece.get_valid_moves(self._board.get_board())

            # if piece is valid but has no valid moves
            if not self._valid_moves:
                self.warning()
                return False

            self._chosen = piece
            return True

        # invalid choice
        self.warning()
        return False

    def make_move(self, piece, row, col):
        """Simulates a move on the game board. Takes three parameters, the piece
        moving, and the row and column of the square being moved to. If the move
        is invalid, or illegal, gives warning and returns False.
        Otherwise, completes the indicated move, removes any captured piece,
        updates the turn, and returns True.
        """
        # Chosen is reset
        self._chosen = None

        if (row, col) in self._valid_moves:
            self._board.update_board(piece, row, col)
            self._valid_moves = []
            self.update_turn()
            return True

        # if move is not valid
        self.warning()
        return False

    def display_message(self, message):
        """Displays message to middle of game board."""
        font = pygame.font.SysFont('comicsans', self.FONT_SIZE)
        text = font.render(message, True, self.TEXT, self.BACKGROUND)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self._window.blit(text, text_rect)

    def warning(self):
        """Displays an invalid move warning."""
        self.display_message('Invalid Choice!')
        pygame.display.update()
        pygame.time.wait(900)  # Display message for 0.9 seconds only
