from constants import COLS, PLAYER_WHITE, ROWS, SQUARE_SIZE, \
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
        self._first_turn = True
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

    def not_first(self):
        """Increases turn data member by one."""
        self._first_turn = False

    def move(self, board, row, col, team, vert=0, horiz=0, rec=False, first=False):
        """Simulates a piece's potential move on the game board to determine
        the positions of all legal moves. Returns a dictionary of potential
        moves, if any. Otherwise, returns an empty dictionary.
        """
        moves_list = {}     # key is position, value is captured object

        # if piece is out of bounds, return empty dictionary
        if row < 0 or row > 7 or col < 0 or col > 7:
            return moves_list

        pos = board[row][col]

        if pos is None:     # empty square
            moves_list.update({(row, col): None})
        elif pos.get_team() != team:    # captured piece
            moves_list.update({(row, col): pos})
            return moves_list
        else:       # piece is team member
            return moves_list

        # If piece allows recursive movements or piece is Pawn on first move
        if rec or first:
            moves_list.update(self.move(board, row + vert, col + horiz, team, vert, horiz, rec))

        return moves_list


class Pawn(Piece):
    """Represents a Pawn piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the Pawn, as well as the particular and special movements
    associated with a Pawn piece.
    """
    def __init__(self, team, row, col):
        """Creates a pawn piece with the same parameters and data members as the parent
        class. Includes one additional data member, en passant boolean.
        """
        super().__init__(team, row, col)
        self._en_passant = False

    def get_type(self):
        """Takes no parameters and returns the piece type."""
        return 'PAWN'

    def en_passant(self, board):
        """Checks whether piece has positioned itself for en passant."""

        # Did pawn move two spaces on first move
        if self._first_turn and (3 <= self._row <= 4):
            left = board[self._row][self._col - 1] if self._col > 0 else None
            right = board[self._row][self._col + 1] if self._col < 7 else None

            # is there a pawn of the opposite team to the left or right
            if (left is not None and left.get_type() == 'PAWN' and left._team != self._team) \
             or (right is not None and right.get_type() == 'PAWN' and right._team != self._team):
                self._en_passant = True

    def not_en_passant(self):
        """Sets en passant data member to False."""
        self._en_passant = False

    def draw(self, window):
        """Draws the piece."""
        if self._team == PLAYER_WHITE:
            window.blit(WHITE_PAWN, (self._x_coord - WHITE_PAWN.get_width() // 2,
                                     self._y_coord - WHITE_PAWN.get_height() // 2))
        else:
            window.blit(BLACK_PAWN, (self._x_coord - BLACK_PAWN.get_width() // 2,
                                     self._y_coord - BLACK_PAWN.get_height() // 2))

    def get_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a dictionary containing
        tuples of each row and column position.
        """
        stand_moves = {}
        capture_moves = {}

        # team determines direction of movement
        if self._team == PLAYER_WHITE:
            stand_moves.update(self.move(board, self._row - 1, self._col, self._team, -1, 0, False, self._first_turn))

            # capture movement is different for pawns
            capture_moves.update(self.move(board, self._row - 1, self._col - 1, self._team))
            capture_moves.update(self.move(board, self._row - 1, self._col + 1, self._team))

        else:   # team is BLACK
            stand_moves.update(self.move(board, self._row + 1, self._col, self._team, 1, 0, False, self._first_turn))
            capture_moves.update(self.move(board, self._row + 1, self._col - 1, self._team))
            capture_moves.update(self.move(board, self._row + 1, self._col + 1, self._team))

        # standard move cannot capture a piece
        keys_to_be_removed = []
        for pos, value in stand_moves.items():
            if value is not None:
                keys_to_be_removed.append(pos)

        # capture move can only capture a piece
        for pos, value in capture_moves.items():
            if value is None:
                en_passant = board[self._row][pos[1]]
                if en_passant is not None and en_passant.get_type() == 'PAWN' and en_passant._en_passant:
                    capture_moves[pos] = en_passant
                else:
                    keys_to_be_removed.append(pos)

        stand_moves.update(capture_moves)
        for key in keys_to_be_removed:
            del stand_moves[key]

        return stand_moves


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

    def get_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a dictionary containing
        tuples of each row and column position.
        """
        valid_moves = {}

        # North, South, East, and West
        valid_moves.update(self.move(board, self._row - 1, self._col, self._team, -1, 0, True))
        valid_moves.update(self.move(board, self._row + 1, self._col, self._team, 1, 0, True))
        valid_moves.update(self.move(board, self._row, self._col - 1, self._team, 0, -1, True))
        valid_moves.update(self.move(board, self._row, self._col + 1, self._team, 0, 1, True))

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

    def get_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a dictionary containing
        tuples of each row and column position.
        """
        valid_moves = {}

        # 2up/1left, 2up/1right, 2down/1left, 2down/1right
        valid_moves.update(self.move(board, self._row - 2, self._col - 1, self._team))
        valid_moves.update(self.move(board, self._row - 2, self._col + 1, self._team))
        valid_moves.update(self.move(board, self._row + 2, self._col - 1, self._team))
        valid_moves.update(self.move(board, self._row + 2, self._col + 1, self._team))

        # 2left/1up, 2left/1down, 2right/1up, 2right/1down
        valid_moves.update(self.move(board, self._row - 1, self._col - 2, self._team))
        valid_moves.update(self.move(board, self._row + 1, self._col - 2, self._team))
        valid_moves.update(self.move(board, self._row - 1, self._col + 2, self._team))
        valid_moves.update(self.move(board, self._row + 1, self._col + 2, self._team))

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

    def get_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a dictionary containing
        tuples of each row and column position.
        """
        valid_moves = {}

        # Northwest, Northeast, Southwest, Southeast
        valid_moves.update(self.move(board, self._row - 1, self._col - 1, self._team, -1, -1, True))
        valid_moves.update(self.move(board, self._row - 1, self._col + 1, self._team, -1, 1, True))
        valid_moves.update(self.move(board, self._row + 1, self._col - 1, self._team, 1, -1, True))
        valid_moves.update(self.move(board, self._row + 1, self._col + 1, self._team, 1, 1, True))

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

    def get_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a dictionary containing
        tuples of each row and column position.
        """
        valid_moves = {}

        # North, West, South, East
        valid_moves.update(self.move(board, self._row - 1, self._col, self._team, -1, 0, True))
        valid_moves.update(self.move(board, self._row, self._col - 1, self._team, 0, -1, True))
        valid_moves.update(self.move(board, self._row + 1, self._col, self._team, 1, 0, True))
        valid_moves.update(self.move(board, self._row, self._col + 1, self._team, 0, 1, True))

        # Northwest, Southwest, Southeast, Northeast
        valid_moves.update(self.move(board, self._row - 1, self._col - 1, self._team, -1, -1, True))
        valid_moves.update(self.move(board, self._row + 1, self._col - 1, self._team, 1, -1, True))
        valid_moves.update(self.move(board, self._row + 1, self._col + 1, self._team, 1, 1, True))
        valid_moves.update(self.move(board, self._row - 1, self._col + 1, self._team, -1, 1, True))

        return valid_moves


class King(Piece):
    """Represents a King piece. This class inherits data members and methods
    from the Piece class, including init, and is responsible for the particular glyph
    representation of the King, as well as the particular movements associated
    with a King piece.
    """
    def __init__(self, team, row, col):
        """Creates a kig piece with the same parameters and data members as the parent
        class. Includes one additional data member, check boolean.
        """
        super().__init__(team, row, col)
        self._check = False

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

    def get_moves(self, board):
        """Takes the current game board as parameter. Determines the legal
        moves for the piece, and returns them in the form of a dictionary containing
        tuples of each row and column position.
        """
        valid_moves = {}

        # North, West, South, East
        valid_moves.update(self.move(board, self._row - 1, self._col, self._team))
        valid_moves.update(self.move(board, self._row, self._col - 1, self._team))
        valid_moves.update(self.move(board, self._row + 1, self._col, self._team))
        valid_moves.update(self.move(board, self._row, self._col + 1, self._team))

        # Northwest, Southwest, Southeast, Northeast
        valid_moves.update(self.move(board, self._row - 1, self._col - 1, self._team))
        valid_moves.update(self.move(board, self._row + 1, self._col - 1, self._team))
        valid_moves.update(self.move(board, self._row + 1, self._col + 1, self._team))
        valid_moves.update(self.move(board, self._row - 1, self._col + 1, self._team))

        # Castling
        valid_moves.update(self.castle(board))

        return valid_moves

    def check(self, board):
        """Examines current board to determine whether king is in check."""
        # iterate through each board position
        for row in range(ROWS):
            for col in range(COLS):
                piece = board[row][col]

                # if piece is opposite team
                if piece is not None and piece.get_team() != self._team:
                    possible_moves = piece.get_moves(board)

                    # find out if king is threatened
                    for pos, capture in possible_moves.items():
                        if capture is self:
                            self._check = True
                            break
                        self._check = False
                    else:
                        continue
                    break
            else:
                continue
            break

        print(f"{self._team} king check is {self._check}")
        return self._check

    def castle(self, board):
        """Examines current board to determine if castling is a valid move,
        and returns dictionary of valid castles if legal."""
        check_path = {}
        castles = {}
        if self._first_turn:
            # West & East
            check_path.update(self.move(board, self._row, self._col - 1, self._team, 0, -1, True))
            check_path.update(self.move(board, self._row, self._col + 1, self._team, 0, +1, True))

        for row, col in check_path:
            # Queenside
            if col == 1:
                rook = board[self._row][0]
                if self.check_rook(rook):
                    castles[(self._row, 2)] = {'rook': rook, 'pos': (self._row, 3)}

            # Kingside
            if col == 6:
                rook = board[self._row][7]
                if self.check_rook(rook):
                    castles[(self._row, col)] = {'rook': rook, 'pos': (self._row, 5)}

        return castles

    def check_rook(self, rook):
        """Works with the castle function to determine if the neighboring rook
        is valid for castling.
        """
        if rook is not None and rook.get_type() == 'ROOK' and rook.get_team() == self._team:
            return True
        return False
