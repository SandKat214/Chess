import pygame
from constants import BACKGROUND, BOARD_COLOR, FONT_SIZE, HEIGHT, PLAYER_WHITE,\
    PLAYER_BLACK, SQUARE_SIZE, TEXT_COLOR, WIDTH, UNFINISHED
from .board import Board
from .pieces import Queen, Knight, Rook, Bishop


class Game:
    """Represents a game of chess. This class is responsible
    for the aspects of the game having to do with active play, such as
    making a move, keeping track of the current turn, and displaying the
    current state of the board. Works directly with the Board class to
    know what object currently occupies a board position, update the board
    when a successful move is made, and to determine the current game state.
    """
    def __init__(self, window):
        """Starts a Chess game. Takes the game window as parameter and
        initializes further data members via the reset function.
        """
        self._window = window
        self.reset()

    def reset(self):
        """Starts/Resets board for new game."""
        self._board = Board()
        self._turn = PLAYER_WHITE
        self._chosen = None
        self._valid_moves = {}      # key is position, value is captured object

    def update_turn(self):
        """Takes no parameters. Signals a new turn and updates the turn data
        member to the other team, as well as clearing any en passant status
        from any pieces not captured on that turn.
        """
        if self._turn == PLAYER_WHITE:
            self._turn = PLAYER_BLACK
        else:
            self._turn = PLAYER_WHITE

        # Clear all en passant
        self._board.clear_en_passant(self._turn)

    def display(self):
        """Takes no parameters. Displays the current state of the game."""
        self._board.draw(self._window)
        result = self.get_winner()
        if result != UNFINISHED:
            if result == PLAYER_BLACK:
                self.display_message(f'{PLAYER_BLACK} Wins. Play again: y or n?')
            else:
                self.display_message(f'{PLAYER_WHITE} Wins. Play again: y or n?')

        if self._board.get_promoted_pawn():
            self.choose_promotion()

        # Update Board
        pygame.display.update()

    def get_winner(self):
        """Takes no parameters. Checks if either team is in checkmate, and
        returns the winner. Otherwise, UNFINISHED.
        """
        if self._board.checkmate(PLAYER_BLACK):
            return PLAYER_WHITE

        if self._board.checkmate(PLAYER_WHITE):
            return PLAYER_BLACK

        # If no one has lost
        return UNFINISHED

    def choose(self, row, col):
        """Gets piece clicked by mouse and checks validity of piece moving or
        where it's moving to. Gives warning for any invalid choices.
        """
        piece = self._board.get_piece(row, col)

        # if pawn promotion available
        if self._board.get_promoted_pawn():
            if row == 3 and 2 <= col <= 5:
                return self._board.promote_pawn(self._board.get_promoted_pawn(), col)
            else:
                self.warning()
                return

        # if moving piece is already chosen
        if self._chosen:
            return self.make_move(self._chosen, row, col)

        # check validity
        if piece is not None and piece.get_team() == self._turn:
            self._valid_moves = piece.get_moves(self._board)
            self._board.validate_moves(piece, self._valid_moves)

            # if piece is valid but has no valid moves
            if not self._valid_moves:
                self.warning()
                return

            self._chosen = piece
            return

        # invalid choice
        self.warning()

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
            # Check if move is a castle
            if isinstance(self._valid_moves[(row, col)], dict):
                self._board.update_board(piece, row, col, None)
                self._board.update_board(self._valid_moves[(row, col)]['rook'],
                                         self._valid_moves[(row, col)]['pos'][0],
                                         self._valid_moves[(row, col)]['pos'][1], None)
            # Any other type of move
            else:
                self._board.update_board(piece, row, col, self._valid_moves[(row, col)])

            # Complete move
            self._valid_moves = {}
            self.update_turn()
            return True

        # if move is not valid
        self.warning()
        return False

    def display_message(self, message):
        """Displays message to middle of game board."""
        font = pygame.font.SysFont('comicsans', FONT_SIZE)
        text = font.render(message, True, TEXT_COLOR, BACKGROUND)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)
        self._window.blit(text, text_rect)

    def warning(self):
        """Displays an invalid move warning."""
        self.display_message('Invalid Choice!')
        pygame.display.update()
        pygame.time.wait(900)  # Display message for 0.9 seconds only

    def choose_promotion(self):
        """Prompts for choice of pawn promotion."""
        padding = 10

        # Prepare message
        font = pygame.font.SysFont('comicsans', SQUARE_SIZE // 4)
        text = font.render('Pawn Promotion: Click your choice!', True, TEXT_COLOR, BACKGROUND)
        text_rect = text.get_rect()

        # Create fill background
        main_rect = pygame.draw.rect(self._window, BACKGROUND, (SQUARE_SIZE * 2 - padding,
                                                                HEIGHT // 2 - SQUARE_SIZE - text_rect.height,
                                                                SQUARE_SIZE * 4 + padding * 2,
                                                                SQUARE_SIZE + text_rect.height + padding))
        # Display message
        text_rect.centerx = main_rect.centerx
        text_rect.top = main_rect.top
        pygame.display.get_surface().blit(text, text_rect)

        # Create image background
        pygame.draw.rect(self._window, BOARD_COLOR, (main_rect.x + padding, main_rect.y + text_rect.height,
                                                     SQUARE_SIZE * 4, SQUARE_SIZE))

        # Display images/choices
        choices = [
            Queen(self._board.get_promoted_pawn().get_team(), 3, 2),
            Knight(self._board.get_promoted_pawn().get_team(), 3, 3),
            Rook(self._board.get_promoted_pawn().get_team(), 3, 4),
            Bishop(self._board.get_promoted_pawn().get_team(), 3, 5)
        ]

        for choice in choices:
            choice.draw(self._window)
