import pygame
import random
import numpy as np
from settings import *

class Tile:
    def __init__(self, x, y, image, type, revealed=False, flagged=False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def draw(self, board_surface, offset_y=0):
        if not self.flagged and self.revealed:
            board_surface.blit(self.image, (self.x, self.y + offset_y))
        elif self.flagged and not self.revealed:
            board_surface.blit(tile_flag, (self.x, self.y + offset_y))
        elif not self.revealed:
            board_surface.blit(tile_unknown, (self.x, self.y + offset_y))

    def __repr__(self):
        return self.type

class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board_surface = None  # Will be created when drawing
        self.board_list = [[Tile(col, row, tile_empty, ".") for row in range(self.rows)] for col in range(self.cols)]
        self.place_mines()
        self.place_clues()
        self.dug = []
        self.first_move = True
        self.mines_flagged = 0

    def place_mines(self):
        """Place mines randomly on the board"""
        for _ in range(self.mines):
            while True:
                x = random.randint(0, self.rows - 1)
                y = random.randint(0, self.cols - 1)
                if self.board_list[x][y].type == ".":
                    self.board_list[x][y].image = tile_mine
                    self.board_list[x][y].type = "X"
                    break

    def ensure_safe_first_move(self, first_x, first_y):
        """Ensures the first click is always safe"""
        # If the first click is a mine, move it elsewhere
        if self.board_list[first_x][first_y].type == "X":
            self.board_list[first_x][first_y].type = "."
            self.board_list[first_x][first_y].image = tile_empty
            
            # Find a new place for the mine
            while True:
                x = random.randint(0, self.rows - 1)
                y = random.randint(0, self.cols - 1)
                if (x != first_x or y != first_y) and self.board_list[x][y].type == ".":
                    self.board_list[x][y].image = tile_mine
                    self.board_list[x][y].type = "X"
                    break
            
            # Recalculate clues
            self.clear_clues()
            self.place_clues()
            
    def clear_clues(self):
        """Clear all clues from the board for recalculation"""
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board_list[x][y].type == "C":
                    self.board_list[x][y].type = "."
                    self.board_list[x][y].image = tile_empty

    def place_clues(self):
        """Place number clues based on mine positions"""
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board_list[x][y].type != "X":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines - 1]
                        self.board_list[x][y].type = "C"

    def is_inside(self, x, y):
        """Check if a position is inside the board"""
        return 0 <= x < self.rows and 0 <= y < self.cols

    def check_neighbours(self, x, y):
        """Count the number of adjacent mines"""
        total_mines = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].type == "X":
                    total_mines += 1
        return total_mines

    def draw(self, screen, offset_y=0):
        """Draw the board to the screen with optional vertical offset"""
        # Create the board surface if it doesn't exist or needs to be recreated
        if self.board_surface is None or self.board_surface.get_size() != (self.cols * TILESIZE, self.rows * TILESIZE):
            self.board_surface = pygame.Surface((self.cols * TILESIZE, self.rows * TILESIZE))
        
        self.board_surface.fill(BGCOLOUR)
        
        # Draw grid lines for better visual clarity
        for x in range(self.cols + 1):
            pygame.draw.line(
                self.board_surface, 
                LIGHTGRAY, 
                (x * TILESIZE, 0), 
                (x * TILESIZE, self.rows * TILESIZE)
            )
        for y in range(self.rows + 1):
            pygame.draw.line(
                self.board_surface, 
                LIGHTGRAY, 
                (0, y * TILESIZE), 
                (self.cols * TILESIZE, y * TILESIZE)
            )
            
        # Draw tiles
        for row in self.board_list:
            for tile in row:
                tile.draw(self.board_surface, offset_y=0)  # No offset within the board surface
                
        # Draw the board surface to the screen with the provided offset
        screen.blit(self.board_surface, (0, offset_y))

    def reveal_all_mines(self, exploded_x=None, exploded_y=None):
        """Reveal all mines on the board. Mark the exploded one if provided."""
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board_list[x][y]
                if tile.type == "X":
                    tile.revealed = True
                    # Mark the exploded mine differently
                    if exploded_x is not None and exploded_y is not None and x == exploded_x and y == exploded_y:
                        tile.image = tile_exploded

    def dig(self, x, y):
        """Dig at the specified position"""
        # Ensure first move is always safe
        if self.first_move:
            self.ensure_safe_first_move(x, y)
            self.first_move = False
            
        # If flagged, don't dig
        if self.board_list[x][y].flagged:
            return True
            
        # Already revealed, no need to dig again
        if self.board_list[x][y].revealed:
            return True
            
        # Keep track of dug positions for empty tile expansion
        self.dug.append((x, y))
        
        # Hit a mine
        if self.board_list[x][y].type == "X":
            self.board_list[x][y].revealed = True
            self.board_list[x][y].image = tile_exploded
            self.reveal_all_mines(x, y)
            return False
            
        # Hit a number
        elif self.board_list[x][y].type == "C":
            self.board_list[x][y].revealed = True
            return True

        # Hit an empty tile, expand to reveal adjacent tiles
        self.board_list[x][y].revealed = True

        # Expand to neighboring tiles (this is a "flood fill" algorithm)
        for row in range(max(0, x - 1), min(self.rows - 1, x + 1) + 1):
            for col in range(max(0, y - 1), min(self.cols - 1, y + 1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)
        return True

    def get_state(self):
        """
        Get the current state of the board for the AI.
        Returns a 2D numpy array where:
        -1 = Unrevealed tile
        0-8 = Revealed tile with number of adjacent mines
        9 = Revealed mine
        10 = Flagged tile
        """
        state = np.zeros((self.rows, self.cols), dtype=int)
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board_list[x][y]
                if tile.revealed:
                    if tile.type == "C":
                        state[x][y] = self.check_neighbours(x, y)
                    elif tile.type == "X":
                        state[x][y] = 9  # Revealed mine
                    else:
                        state[x][y] = 0  # Empty revealed tile
                elif tile.flagged:
                    state[x][y] = 10  # Flagged tile
                else:
                    state[x][y] = -1  # Unrevealed tile
        return state

    def get_flat_state(self):
        """Get a flattened representation of the board state for neural networks"""
        state = []
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board_list[x][y]
                if tile.revealed:
                    if tile.type == "C":
                        state.append(self.check_neighbours(x, y))
                    elif tile.type == "X":
                        state.append(9)  # Mine
                    else:
                        state.append(0)  # Empty revealed tile
                elif tile.flagged:
                    state.append(10)  # Flagged tile
                else:
                    state.append(-1)  # Unrevealed tile
        return np.array(state)

    def display_board(self):
        """Print a text representation of the board to the console (for debugging)"""
        for y in range(self.rows):
            row_str = ""
            for x in range(self.cols):
                tile = self.board_list[x][y]
                if tile.revealed:
                    if tile.type == "X":
                        row_str += "X "
                    elif tile.type == "C":
                        row_str += str(self.check_neighbours(x, y)) + " "
                    else:
                        row_str += ". "
                elif tile.flagged:
                    row_str += "F "
                else:
                    row_str += "? "
            print(row_str)