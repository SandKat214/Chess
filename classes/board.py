import pygame
from constants import COLS, BOARD_COLOR, SQUARE_COLOR,\
    PLAYER_WHITE, PLAYER_BLACK, ROWS, SQUARE_SIZE
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
        self._kings = []
        self._promoted_pawn = None
        self.set_up_board()     # sets up board data member
        self.set_up_pieces()    # sets up pieces data member

    def get_board(self):
        """Takes no parameter and returns the board data member."""
        return self._board

    def get_pieces(self):
        """Takes no parameters and returns the pieces dictionary data member."""
        return self._pieces

    def get_promoted_pawn(self):
        """Takes no parameters and returns the promoted pawn data member."""
        return self._promoted_pawn

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
                        king = King(team, row, col)
                        self._kings.append(king)
                        self._board[row].append(king)

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

    def clear_en_passant(self, turn_team):
        """Falsifies en_passant status of any pawn from opposing team that
        wasn't captured on that move.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self._board[row][col]
                if piece is not None and piece.get_team() == turn_team and piece.get_type() == 'PAWN':
                    piece.not_en_passant()

    def validate_moves(self, piece, moves):
        """Takes moving piece and dictionary of moves as parameter and ensures that no moves
        will place team's king in check.
        """
        return_row = piece.get_row()
        return_col = piece.get_col()
        keys_to_be_removed = []
        captured_piece = False

        for row, col in moves:
            captured = moves[(row, col)]
            if not isinstance(captured, dict):      # king castling
                if captured is not None:
                    captured_piece = True
                    captured_row = captured.get_row()
                    captured_col = captured.get_col()
                    self._board[captured_row][captured_col] = None

                # Preliminary swap to evaluate check
                self.swap(piece, row, col)
                for king in self._kings:
                    if king.get_team() == piece.get_team():
                        if king.check(self):
                            keys_to_be_removed.append((row, col))

                # Swap everything back
                self.swap(piece, return_row, return_col)
                if captured_piece:
                    self._board[captured_row][captured_col] = captured
                    captured.change_pos(captured_row, captured_col)
                    captured_piece = False

        # remove invalidated moves from dictionary
        for key in keys_to_be_removed:
            del moves[key]

    def swap(self, piece, row, col):
        """Takes piece to be moved and row and column to be moved to and swaps them."""
        self._board[piece.get_row()][piece.get_col()], self._board[row][col] = \
            self._board[row][col], self._board[piece.get_row()][piece.get_col()]

        piece.change_pos(row, col)

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

    def update_board(self, piece, row, col, captured):
        """Takes a piece object as a parameter, as well as the row and column
        position to where it is moving to on the game board, and the object
        captured by that piece. Removes captured piece (if appropriate), and
        moves the piece to the new position.
        """
        # remove piece if applicable
        self.remove(captured)

        # swap the objects at the two locations
        self.swap(piece, row, col)

        if piece.get_type() == 'PAWN':
            # en passant?
            piece.en_passant(self._board)

            # pawn promotion
            if row == 0 or row == 7:
                self._promoted_pawn = piece

        # determine check
        for king in self._kings:
            king.check(self)

        piece.not_first()

    def promote_pawn(self, pawn, choice_col):
        """Takes pawn to be promoted and clicked choice as parameter
        and updates piece to player's choice.
        """
        team = pawn.get_team()
        pawn_row = pawn.get_row()
        pawn_col = pawn.get_col()

        # keys correspond to displayed choices
        choices = {
            2: Queen(team, pawn_row, pawn_col),
            3: Knight(team, pawn_row, pawn_col),
            4: Rook(team, pawn_row, pawn_col),
            5: Bishop(team, pawn_row, pawn_col)
        }

        # Promote pawn and update # of pieces
        self._board[pawn_row][pawn_col] = choices[choice_col]
        key = (team, self._board[pawn_row][pawn_col].get_type())
        self._pieces[key] += 1
        self._promoted_pawn = None
