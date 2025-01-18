import pygame
import os


BLACK =(0, 0, 0)
DARKGRAY=(40, 40, 40)
LIGHTGRAY=(100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGRAY


TILESIZE = 32
FPS = 60
TITLE = "Minesweeper python"
ROWS= 20
COLS=20
DIFFICULTY_SETTINGS = {
    'easy': {'AMOUT_MINES': 20, 'ROWS': 15, 'COLS': 15},
    'medium': {'AMOUT_MINES': 40, 'ROWS': 25, 'COLS': 25},
    'hard': {'AMOUT_MINES': 180, 'ROWS': 35, 'COLS': 35}
}
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS
FPS = 60
TITLE= "Minesweeper python"

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", f"Tile{i}.png")),(TILESIZE, TILESIZE)))
    tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", "TileEmpty.png")),(TILESIZE, TILESIZE))
    tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", "TileExploded.png")),(TILESIZE, TILESIZE))
    tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", "TileFlag.png")),(TILESIZE, TILESIZE))
    tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", "TileMine.png")),(TILESIZE, TILESIZE))
    tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", "TileNotMine.png")),(TILESIZE, TILESIZE))
    tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper","assets", "TileUnknown.png")),(TILESIZE, TILESIZE))