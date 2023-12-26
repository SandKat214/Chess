import pygame
from constants import COLS, BOARD_COLOR, SQUARE_COLOR, PLAYER_WHITE, PLAYER_BLACK, ROWS, SQUARE_SIZE
from .pieces import Bishop, King, Knight, Pawn, Queen, Rook


class Board:
    """Represents a chess variant game board. This class handles aspects
    of the game having to do with the game board, such as keeping track of
    all piece positions, and how many of each type of piece is left on the
    board. Works directly with the Piece class and its subclasses to determine
    where each piece can legally move.
    """

    def __init__(self):
        """Sets a ChessVar game board. Data members are initialized without
        parameters. Called methods complete initialization.
        """
        self._board = []    # will become nested list
        self._pieces = {}
        self.set_up_board()     # sets up board data member
        self.set_up_pieces()    # sets up pieces data member

    def get_board(self):
        """Takes no parameter and returns the board data member."""
        return self._board

    def get_pieces(self):
        """Takes no parameters and returns the pieces dictionary data member."""
        return self._pieces

    def set_up_board(self):
        """Takes no parameters. Sets up the game board with black and white
        team pieces in their appropriate positions. This abstract board is
        a nested list with each nested list representing a row, and its
        indexes representing the columns.
        """
        # Assign teams to variables
        team_b = PLAYER_BLACK
        team_w = PLAYER_WHITE

        for row in range(8):
            self._board.append([])
            team = team_b if row < 2 else team_w
            for col in range(8):
                # player rows besides pawns
                if row == 0 or row == 7:
                    if col == 0 or col == 7:
                        self._board[row].append(Rook(team, row, col))
                    elif col == 1 or col == 6:
                        self._board[row].append(Knight(team, row, col))
                    elif col == 2 or col == 5:
                        self._board[row].append(Bishop(team, row, col))
                    elif col == 3:
                        self._board[row].append(Queen(team, row, col))
                    else:
                        self._board[row].append(King(team, row, col))

                # pawns
                elif row == 1 or row == 6:
                    self._board[row].append(Pawn(team, row, col))

                # empty squares
                else:
                    self._board[row].append(None)

    def set_up_pieces(self):
        """Takes no parameters. Sets up the pieces dictionary with the initial
        number of each type of piece for each team. The key is a string of the
        piece team and type, and the value is how many are on the board.
        """
        self._pieces.update({
            (PLAYER_WHITE, 'PAWN'): 8,
            (PLAYER_WHITE, 'ROOK'): 2,
            (PLAYER_WHITE, 'KNIGHT'): 2,
            (PLAYER_WHITE, 'BISHOP'): 2,
            (PLAYER_WHITE, 'QUEEN'): 1,
            (PLAYER_WHITE, 'KING'): 1,
            (PLAYER_BLACK, 'PAWN'): 8,
            (PLAYER_BLACK, 'ROOK'): 2,
            (PLAYER_BLACK, 'KNIGHT'): 2,
            (PLAYER_BLACK, 'BISHOP'): 2,
            (PLAYER_BLACK, 'QUEEN'): 1,
            (PLAYER_BLACK, 'KING'): 1
        })

    def draw(self, window):
        """Draws the board."""
        window.fill(BOARD_COLOR)

        # Draw squares
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, SQUARE_COLOR, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for row in range(ROWS):
            for col in range(COLS):
                piece = self._board[row][col]
                if piece is not None:
                    piece.draw(window)

    def get_piece(self, row, col):
        """Takes a row and column corresponding to a nested list position
        as parameters and returns whatever object currently resides as that
        position on the board.
        """
        return self._board[row][col]

    def remove(self, piece):
        """Takes an object, from a certain board position, as parameter. If
        that object is a piece, removes it from the game board and updates
        its count in the pieces dictionary.
        """
        # if object is a piece
        if piece is not None:
            key = (piece.get_team(), piece.get_type())
            self._board[piece.get_row()][piece.get_col()] = None    # remove piece from board
            self._pieces[key] -= 1      # decrease quantity in pieces library

    def update_board(self, piece, row, col):
        """Takes a piece object as a parameter, as well as the row and column
        position to where it is moving to on the game board. Removes a
        captured piece (if appropriate), and moves the piece to the new position.
        """
        captured_piece = self._board[row][col]

        # remove piece if applicable
        self.remove(captured_piece)

        # swap the objects at the two locations
        self._board[piece.get_row()][piece.get_col()], self._board[row][col] =\
         self._board[row][col], self._board[piece.get_row()][piece.get_col()]

        # update piece information
        piece.change_pos(row, col)
