import pygame
import os

# Colours
BLACK = (0, 0, 0)
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
TITLE = "Minesweeper Python"

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {'AMOUT_MINES': 3, 'ROWS': 5, 'COLS': 5}  # 5x5 board with 3 mines
}

# Load tile images
tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"Tile{i}.png")), (TILESIZE, TILESIZE)))

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileEmpty.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileFlag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileMine.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileNotMine.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets", "TileUnknown.png")), (TILESIZE, TILESIZE))