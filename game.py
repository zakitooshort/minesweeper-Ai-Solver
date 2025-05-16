import pygame
import os
import time
from sprites import Board
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.default_width = 800
        self.default_height = 600
        self.screen = pygame.display.set_mode((self.default_width, self.default_height))
        pygame.display.set_caption(TITLE + " - Manual Mode")
        self.clock = pygame.time.Clock()
        self.difficulty = 'easy'
        self.win = False
        self.game_started = False
        self.start_time = 0
        self.elapsed_time = 0
        self.game_over = False
        
        # Create font objects
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.font_small = pygame.font.SysFont('Arial', 24)

    def set_screen_size(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.width = max(TILESIZE * settings['COLS'], 400)  # Ensure minimum width
        self.height = max(TILESIZE * settings['ROWS'] + 80, 400)  # Add space for UI elements
        self.board_offset_y = 60  # Offset for placing the board below the UI banner

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def home_page(self):
        self.screen.fill(BGCOLOUR)
        title_text = self.font_large.render('Minesweeper', True, (255, 255, 255))
        subtitle_text = self.font_medium.render('Choose Difficulty', True, (200, 200, 200))
        
        self.screen.blit(title_text, (self.default_width // 2 - title_text.get_width() // 2, self.default_height // 4 - 60))
        self.screen.blit(subtitle_text, (self.default_width // 2 - subtitle_text.get_width() // 2, self.default_height // 4))

        easy_button = pygame.Rect(self.default_width // 2 - 100, self.default_height // 2 - 50, 200, 50)
        medium_button = pygame.Rect(self.default_width // 2 - 100, self.default_height // 2 + 10, 200, 50)
        hard_button = pygame.Rect(self.default_width // 2 - 100, self.default_height // 2 + 70, 200, 50)

        # Draw buttons with nicer style
        for button, color, text, y_pos in [
            (easy_button, GREEN, 'Easy', self.default_height // 2 - 50),
            (medium_button, YELLOW, 'Medium', self.default_height // 2 + 10),
            (hard_button, RED, 'Hard', self.default_height // 2 + 70)
        ]:
            # Draw button with shadow effect
            pygame.draw.rect(self.screen, DARKGRAY, button.inflate(6, 6))
            pygame.draw.rect(self.screen, color, button)
            
            text_surf = self.font_medium.render(text, True, BLACK)
            self.screen.blit(text_surf, (button.centerx - text_surf.get_width() // 2, button.centery - text_surf.get_height() // 2))

        instruction_text = self.font_small.render('Left Click: Dig | Right Click: Flag', True, (180, 180, 180))
        self.screen.blit(instruction_text, (self.default_width // 2 - instruction_text.get_width() // 2, self.default_height // 2 + 140))

        pygame.display.flip()

        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        self.difficulty = 'easy'
                        choosing = False
                    elif medium_button.collidepoint(event.pos):
                        self.difficulty = 'medium'
                        choosing = False
                    elif hard_button.collidepoint(event.pos):
                        self.difficulty = 'hard'
                        choosing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return False

        self.set_screen_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        return True

    def new(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.board = Board(settings['ROWS'], settings['COLS'], settings['AMOUT_MINES'])
        self.game_started = False
        self.game_over = False
        self.win = False
        self.elapsed_time = 0
        
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            
            # Update game timer
            if self.game_started and not self.game_over:
                self.elapsed_time = int(time.time() - self.start_time)
                
            self.events()
            self.draw()
            
        return self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        
        # Draw info bar at the top
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        info_rect = pygame.Rect(0, 0, self.width, self.board_offset_y)
        pygame.draw.rect(self.screen, LIGHTGRAY, info_rect)
        
        # Draw difficulty and mines info
        difficulty_text = self.font_small.render(f"Difficulty: {self.difficulty.capitalize()}", True, BLACK)
        mines_text = self.font_small.render(f"Mines: {settings['AMOUT_MINES']}", True, BLACK)
        time_text = self.font_small.render(f"Time: {self.format_time(self.elapsed_time)}", True, BLACK)
        
        self.screen.blit(difficulty_text, (10, 10))
        self.screen.blit(mines_text, (self.width - mines_text.get_width() - 10, 10))
        self.screen.blit(time_text, (self.width // 2 - time_text.get_width() // 2, 10))
        
        # Draw board
        self.board.draw(self.screen, offset_y=self.board_offset_y)
        
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
                return
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mx, my = pygame.mouse.get_pos()
                my -= self.board_offset_y  # Adjust for the info bar
                
                # Only process clicks within the board
                if my >= 0 and mx // TILESIZE < self.board.cols and my // TILESIZE < self.board.rows:
                    mx //= TILESIZE
                    my //= TILESIZE
                    
                    # Start the timer on first click
                    if not self.game_started:
                        self.game_started = True
                        self.start_time = time.time()

                    if event.button == 1:  # Left click
                        if not self.board.board_list[mx][my].flagged:
                            if not self.board.dig(mx, my):
                                # Hit a mine, game over
                                for row in self.board.board_list:
                                    for tile in row:
                                        if tile.flagged and tile.type != "X":
                                            tile.flagged = False
                                            tile.revealed = True
                                            tile.image = tile_not_mine
                                        elif tile.type == "X":
                                            tile.revealed = True
                                self.game_over = True
                                
                    if event.button == 3:  # Right click
                        if not self.board.board_list[mx][my].revealed:
                            self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged
                    
                    # Check win condition after each move
                    if self.check_win():
                        self.win = True
                        self.game_over = True
                        # Flag all mines
                        for row in self.board.board_list:
                            for tile in row:
                                if tile.type == "X" and not tile.revealed:
                                    tile.flagged = True

    def end_screen(self):
        self.screen.fill(BGCOLOUR)
        
        if self.win:
            result_text = self.font_large.render('You Win!', True, GREEN)
        else:
            result_text = self.font_large.render('Game Over', True, RED)
            
        time_text = self.font_medium.render(f"Time: {self.format_time(self.elapsed_time)}", True, WHITE)
        
        self.screen.blit(result_text, (self.width // 2 - result_text.get_width() // 2, self.height // 4 - 30))
        self.screen.blit(time_text, (self.width // 2 - time_text.get_width() // 2, self.height // 4 + 30))

        restart_button = pygame.Rect(self.width // 2 - 200, self.height // 2, 180, 50)
        menu_button = pygame.Rect(self.width // 2 + 20, self.height // 2, 180, 50)

        # Draw buttons with shadow
        pygame.draw.rect(self.screen, DARKGRAY, restart_button.inflate(6, 6))
        pygame.draw.rect(self.screen, GREEN, restart_button)
        pygame.draw.rect(self.screen, DARKGRAY, menu_button.inflate(6, 6))
        pygame.draw.rect(self.screen, BLUE, menu_button)

        restart_text = self.font_medium.render('Play Again', True, BLACK)
        menu_text = self.font_medium.render('Main Menu', True, BLACK)
        
        self.screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2, 
                                        restart_button.centery - restart_text.get_height() // 2))
        self.screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2, 
                                     menu_button.centery - menu_text.get_height() // 2))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        waiting = False
                        self.new()  # Start new game with same difficulty
                        return True
                    elif menu_button.collidepoint(event.pos):
                        self.width = 800
                        self.height = 600
                        self.screen = pygame.display.set_mode((self.width, self.height))
                        return None  # Return to main menu

        return True  # Continue playing

def play_game():
    game = Game()
    running = True
    
    while running:
        # Show home page to select difficulty
        continue_game = game.home_page()
        if not continue_game:
            running = False
            break
            
        # Initialize new game
        game.new()
        
        # Run the game
        result = game.run()
        
        # Check if player wants to exit
        if result is False:
            running = False
        elif result is None:
            # Return to main menu
            pass
    
    pygame.quit()

if __name__ == "__main__":
    play_game() 