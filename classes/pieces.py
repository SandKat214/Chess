from constants import PLAYER_WHITE, SQUARE_SIZE, \
    BLACK_BISHOP, BLACK_KING, BLACK_KNIGHT, BLACK_PAWN, BLACK_QUEEN, BLACK_ROOK, \
    WHITE_BISHOP, WHITE_KING, WHITE_KNIGHT, WHITE_PAWN, WHITE_QUEEN, WHITE_ROOK


class Piece:
    """Represents a team piece on the game board. This class is responsible
    for aspects of the game that deal directly with each piece, such as what
    team it belongs to, what square it currently resides in, and how it moves
    on the board. Works directly with its child classes to simulate movement
    for each individual type of piece.
    """

    def __init__(self, team, row, col):
        """Creates a game piece. Parameters include the piece team ('BLACK' or
        'WHITE'), the row and column it starts at on the board, and its actual
        coordinates on the game window (determined by called method).
        """
        self._team = team
        self._row = row
        self._col = col
        self._x_coord = 0
        self._y_coord = 0
        self.find_position()        # sets initial x and y coord data members

    def get_team(self):
        """Takes no parameters and returns the team data member."""
        return self._team

    def get_row(self):
        """Takes no parameters and returns the row data member."""
        return self._row

    def get_col(self):
        """Takes no parameters and returns to column data member."""
        return self._col

    def find_position(self):
        """Calculates the middle of the piece's square on the game window."""
        self._x_coord = SQUARE_SIZE * self._col + SQUARE_SIZE // 2
        self._y_coord = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def change_pos(self, row, col):
        """Takes the new position row and column as parameters and updates
        the row, column, and coordinates data members.
        """
        self._row = row
        self._col = col
        self.find_position()

    def move(self, board, row, col, team, vert=0, horiz=0, rec=False, first=False):
        """Simulates a piece's potential move on the game board to determine
        the positions of all legal moves. Returns a list of potential
        moves, if any. Otherwise, returns an empty list.
        """
        moves_list = []

        # if piece is out of bounds, return empty list
        if row < 0 or row > 7 or col < 0 or col > 7:
            return moves_list

        pos = board[row][col]

        if pos is None:     # empty square
            moves_list.append((row, col))
        elif pos.get_team() != team:    # captured piece
            moves_list.append((row, col))
            return moves_list
        else:       # piece is team member
            return moves_list

        # If piece allows recursive movements or piece is Pawn on first move
        if rec or first:
            moves_list += self.move(board, row + vert, col + horiz, team, vert, horiz, rec)

        return moves_list


class Pawn(Piece):
    """Represents a Pawn piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the Pawn, as well as the particular and special movements
    associated with a Pawn piece.
    """
    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'PAWN'

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_PAWN, (self._x_coord - WHITE_PAWN.get_width() // 2,
                                     self._y_coord - WHITE_PAWN.get_height() // 2))
        else:
            window.blit(BLACK_PAWN, (self._x_coord - BLACK_PAWN.get_width() // 2,
                                     self._y_coord - BLACK_PAWN.get_height() // 2))

    def get_valid_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a list containing
        tuples of each row and column position.
        """
        stand_moves = []
        capture_moves = []

        # team determines direction of movement
        if self._team == PLAYER_WHITE:
            first = True if self._row == 6 else False
            stand_moves += self.move(board, self._row - 1, self._col, self._team, -1, 0, False, first)

            # capture movement is different for pawns
            capture_moves += self.move(board, self._row - 1, self._col - 1, self._team)
            capture_moves += self.move(board, self._row - 1, self._col + 1, self._team)

        else:   # team is BLACK
            first = True if self._row == 1 else False
            stand_moves += self.move(board, self._row + 1, self._col, self._team, 1, 0, False, first)
            capture_moves += self.move(board, self._row + 1, self._col - 1, self._team)
            capture_moves += self.move(board, self._row + 1, self._col + 1, self._team)

        # standard move cannot capture a piece
        for pos in stand_moves:
            if board[pos[0]][pos[1]] is not None:
                stand_moves.remove(pos)

        # capture move can only capture a piece
        for pos in capture_moves:
            if board[pos[0]][pos[1]] is None:
                capture_moves.remove(pos)

        return stand_moves + capture_moves


class Rook(Piece):
    """Represents a Rook piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the Rook, as well as the particular movements associated
    with a Rook piece.
    """
    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'ROOK'

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_ROOK, (self._x_coord - WHITE_ROOK.get_width() // 2,
                                     self._y_coord - WHITE_ROOK.get_height() // 2))
        else:
            window.blit(BLACK_ROOK, (self._x_coord - BLACK_ROOK.get_width() // 2,
                                     self._y_coord - BLACK_ROOK.get_height() // 2))

    def get_valid_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a list containing
        tuples of each row and column position.
        """
        valid_moves = []

        # North, South, East, and West
        valid_moves += self.move(board, self._row - 1, self._col, self._team, -1, 0, True)
        valid_moves += self.move(board, self._row + 1, self._col, self._team, 1, 0, True)
        valid_moves += self.move(board, self._row, self._col - 1, self._team, 0, -1, True)
        valid_moves += self.move(board, self._row, self._col + 1, self._team, 0, 1, True)

        return valid_moves


class Knight(Piece):
    """Represents a Knight piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the Knight, as well as the particular movements associated
    with a Knight piece.
    """
    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'KNIGHT'

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_KNIGHT, (self._x_coord - WHITE_KNIGHT.get_width() // 2,
                                       self._y_coord - WHITE_KNIGHT.get_height() // 2))
        else:
            window.blit(BLACK_KNIGHT, (self._x_coord - BLACK_KNIGHT.get_width() // 2,
                                       self._y_coord - BLACK_KNIGHT.get_height() // 2))

    def get_valid_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a list containing
        tuples of each row and column position.
        """
        valid_moves = []

        # 2up/1left, 2up/1right, 2down/1left, 2down/1right
        valid_moves += self.move(board, self._row - 2, self._col - 1, self._team)
        valid_moves += self.move(board, self._row - 2, self._col + 1, self._team)
        valid_moves += self.move(board, self._row + 2, self._col - 1, self._team)
        valid_moves += self.move(board, self._row + 2, self._col + 1, self._team)

        # 2left/1up, 2left/1down, 2right/1up, 2right/1down
        valid_moves += self.move(board, self._row - 1, self._col - 2, self._team)
        valid_moves += self.move(board, self._row + 1, self._col - 2, self._team)
        valid_moves += self.move(board, self._row - 1, self._col + 2, self._team)
        valid_moves += self.move(board, self._row + 1, self._col + 2, self._team)

        return valid_moves


class Bishop(Piece):
    """Represents a Bishop piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the Bishop, as well as the particular movements associated
    with a Bishop piece.
    """
    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'BISHOP'

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_BISHOP, (self._x_coord - WHITE_BISHOP.get_width() // 2,
                                       self._y_coord - WHITE_BISHOP.get_height() // 2))
        else:
            window.blit(BLACK_BISHOP, (self._x_coord - BLACK_BISHOP.get_width() // 2,
                                       self._y_coord - BLACK_BISHOP.get_height() // 2))

    def get_valid_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a list containing
        tuples of each row and column position.
        """
        valid_moves = []

        # Northwest, Northeast, Southwest, Southeast
        valid_moves += self.move(board, self._row - 1, self._col - 1, self._team, -1, -1, True)
        valid_moves += self.move(board, self._row - 1, self._col + 1, self._team, -1, 1, True)
        valid_moves += self.move(board, self._row + 1, self._col - 1, self._team, 1, -1, True)
        valid_moves += self.move(board, self._row + 1, self._col + 1, self._team, 1, 1, True)

        return valid_moves


class Queen(Piece):
    """Represents a Queen piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the Queen, as well as the particular movements associated
    with a Queen piece.
    """
    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'QUEEN'

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_QUEEN, (self._x_coord - WHITE_QUEEN.get_width() // 2,
                                      self._y_coord - WHITE_QUEEN.get_height() // 2))
        else:
            window.blit(BLACK_QUEEN, (self._x_coord - BLACK_QUEEN.get_width() // 2,
                                      self._y_coord - BLACK_QUEEN.get_height() // 2))

    def get_valid_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a list containing
        tuples of each row and column position.
        """
        valid_moves = []

        # North, West, South, East
        valid_moves += self.move(board, self._row - 1, self._col, self._team, -1, 0, True)
        valid_moves += self.move(board, self._row, self._col - 1, self._team, 0, -1, True)
        valid_moves += self.move(board, self._row + 1, self._col, self._team, 1, 0, True)
        valid_moves += self.move(board, self._row, self._col + 1, self._team, 0, 1, True)

        # Northwest, Southwest, Southeast, Northeast
        valid_moves += self.move(board, self._row - 1, self._col - 1, self._team, -1, -1, True)
        valid_moves += self.move(board, self._row + 1, self._col - 1, self._team, 1, -1, True)
        valid_moves += self.move(board, self._row + 1, self._col + 1, self._team, 1, 1, True)
        valid_moves += self.move(board, self._row - 1, self._col + 1, self._team, -1, 1, True)

        return valid_moves


class King(Piece):
    """Represents a King piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the King, as well as the particular movements associated
    with a King piece.
    """
    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'KING'

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_KING, (self._x_coord - WHITE_KING.get_width() // 2,
                                     self._y_coord - WHITE_KING.get_height() // 2))
        else:
            window.blit(BLACK_KING, (self._x_coord - BLACK_KING.get_width() // 2,
                                     self._y_coord - BLACK_KING.get_height() // 2))

    def get_valid_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a list containing
        tuples of each row and column position.
        """
        valid_moves = []

        # North, West, South, East
        valid_moves += self.move(board, self._row - 1, self._col, self._team)
        valid_moves += self.move(board, self._row, self._col - 1, self._team)
        valid_moves += self.move(board, self._row + 1, self._col, self._team)
        valid_moves += self.move(board, self._row, self._col + 1, self._team)

        # Northwest, Southwest, Southeast, Northeast
        valid_moves += self.move(board, self._row - 1, self._col - 1, self._team)
        valid_moves += self.move(board, self._row + 1, self._col - 1, self._team)
        valid_moves += self.move(board, self._row + 1, self._col + 1, self._team)
        valid_moves += self.move(board, self._row - 1, self._col + 1, self._team)

        return valid_moves
