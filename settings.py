import pygame
import os

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGRAY

# Game settings
TILESIZE = 32
FPS = 60
TITLE = "Minesweeper AI Solver"

# Default board size
ROWS = 5
COLS = 5

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {'AMOUT_MINES': 3, 'ROWS': 5, 'COLS': 5},     # 5x5 board with 3 mines (12% mine density)
    'medium': {'AMOUT_MINES': 10, 'ROWS': 9, 'COLS': 9},  # 9x9 board with 10 mines (12.3% mine density)
    'hard': {'AMOUT_MINES': 40, 'ROWS': 16, 'COLS': 16}   # 16x16 board with 40 mines (15.6% mine density)
}

# AI Training settings
DEFAULT_TRAINING_SIZE = 5  # Default size for AI training boards
MAX_TRAINING_SIZE = 10     # Maximum size for AI training
MIN_TRAINING_SIZE = 4      # Minimum size for AI training

# Load tile images
tile_numbers = []
try:
    for i in range(1, 9):
        tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"Tile{i}.png")), (TILESIZE, TILESIZE)))

    tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileEmpty.png")), (TILESIZE, TILESIZE))
    tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileExploded.png")), (TILESIZE, TILESIZE))
    tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileFlag.png")), (TILESIZE, TILESIZE))
    tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileMine.png")), (TILESIZE, TILESIZE))
    tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileNotMine.png")), (TILESIZE, TILESIZE))
    tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileUnknown.png")), (TILESIZE, TILESIZE))
except pygame.error:
    # If images fail to load, this will be handled when pygame is properly initialized
    pass