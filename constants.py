import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
PIECE_SIZE = 70

UNFINISHED = 'UNFINISHED'
PLAYER_WHITE = 'WHITE'
PLAYER_BLACK = 'BLACK'

BOARD_COLOR = (219, 186, 155)    # dark beige
SQUARE_COLOR = (242, 219, 183)    # light beige
FONT_SIZE = WIDTH // 20
BACKGROUND = (0, 0, 0)      # black
TEXT_COLOR = (255, 255, 255)        # white

WHITE_PAWN = pygame.transform.scale(pygame.image.load('assets/white_pawn.png'), (PIECE_SIZE, PIECE_SIZE))
WHITE_ROOK = pygame.transform.scale(pygame.image.load('assets/white_rook.png'), (PIECE_SIZE, PIECE_SIZE))
WHITE_KNIGHT = pygame.transform.scale(pygame.image.load('assets/white_knight.png'), (PIECE_SIZE, PIECE_SIZE))
WHITE_BISHOP = pygame.transform.scale(pygame.image.load('assets/white_bishop.png'), (PIECE_SIZE, PIECE_SIZE))
WHITE_QUEEN = pygame.transform.scale(pygame.image.load('assets/white_queen.png'), (PIECE_SIZE, PIECE_SIZE))
WHITE_KING = pygame.transform.scale(pygame.image.load('assets/white_king.png'), (PIECE_SIZE, PIECE_SIZE))

BLACK_PAWN = pygame.transform.scale(pygame.image.load('assets/black_pawn.png'), (PIECE_SIZE, PIECE_SIZE))
BLACK_ROOK = pygame.transform.scale(pygame.image.load('assets/black_rook.png'), (PIECE_SIZE, PIECE_SIZE))
BLACK_KNIGHT = pygame.transform.scale(pygame.image.load('assets/black_knight.png'), (PIECE_SIZE, PIECE_SIZE))
BLACK_BISHOP = pygame.transform.scale(pygame.image.load('assets/black_bishop.png'), (PIECE_SIZE, PIECE_SIZE))
BLACK_QUEEN = pygame.transform.scale(pygame.image.load('assets/black_queen.png'), (PIECE_SIZE, PIECE_SIZE))
BLACK_KING = pygame.transform.scale(pygame.image.load('assets/black_king.png'), (PIECE_SIZE, PIECE_SIZE))
