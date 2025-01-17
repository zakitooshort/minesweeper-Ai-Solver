import pygame
from sprites import Board  # Import the Board class
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.default_width = 800  
        self.default_height = 600  # Set a larger default height
        self.screen = pygame.display.set_mode((self.default_width, self.default_height))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.difficulty = 'easy'  
        self.win = False  

    def set_screen_size(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.width = TILESIZE * settings['COLS']
        self.height = TILESIZE * settings['ROWS']

    def home_page(self):
        self.screen.fill(BGCOLOUR)
        font = pygame.font.Font(None, 74)
        text = font.render('Choose Difficulty', True, (255, 255, 255))
        self.screen.blit(text, (self.default_width // 2 - text.get_width() // 2, self.default_height // 4))

        easy_button = pygame.Rect(self.default_width // 2 - 100, self.default_height // 2 - 50, 200, 50)
        medium_button = pygame.Rect(self.default_width // 2 - 100, self.default_height // 2 + 10, 200, 50)
        hard_button = pygame.Rect(self.default_width // 2 - 100, self.default_height // 2 + 70, 200, 50)

        pygame.draw.rect(self.screen, (0, 255, 0), easy_button)
        pygame.draw.rect(self.screen, (255, 255, 0), medium_button)
        pygame.draw.rect(self.screen, (255, 0, 0), hard_button)

        font = pygame.font.Font(None, 36)
        text = font.render('Easy', True, (0, 0, 0))
        self.screen.blit(text, (easy_button.x + 50, easy_button.y + 10))
        text = font.render('Medium', True, (0, 0, 0))
        self.screen.blit(text, (medium_button.x + 35, medium_button.y + 10))
        text = font.render('Hard', True, (0, 0, 0))
        self.screen.blit(text, (hard_button.x + 50, hard_button.y + 10))

        pygame.display.flip()

        choosing = True
        while choosing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
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

        self.set_screen_size()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def new(self):
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.board = Board(settings['ROWS'], settings['COLS'], settings['AMOUT_MINES'])
        self.board.display_board()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
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
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
               mx, my = pygame.mouse.get_pos()
               mx //= TILESIZE
               my //= TILESIZE    

               if event.button == 1:
                   if not self.board.board_list[mx][my].flagged:
                       if not self.board.dig(mx, my):
                           for row in self.board.board_list:
                               for tile in row:
                                   if tile.flagged and tile.type !="X":
                                       tile.flagged = False
                                       tile.revealed = True
                                       tile.image = tile_not_mine
                                   elif tile.type == "X":
                                       tile.revealed = True
                           self.playing = False          
                            
               if event.button == 3:
                   if not self.board.board_list[mx][my].revealed:
                       self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged
               if self.check_win():
                   self.win = True
                   self.playing = False
                   for row in self.board.board_list:
                       for tile in row:
                           if not tile.revealed:
                               tile.flagged = True     

    def end_screen(self):
        self.screen.fill(BGCOLOUR)
        font = pygame.font.Font(None, 74)
        if self.win:
            text = font.render('You Win!', True, (0, 255, 0))
        else:
            text = font.render('Game Over', True, (255, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 4))

        restart_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 50)
        quit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 200, 50)

        pygame.draw.rect(self.screen, (0, 255, 0), restart_button)
        pygame.draw.rect(self.screen, (255, 0, 0), quit_button)

        font = pygame.font.Font(None, 36)
        text = font.render('Restart', True, (0, 0, 0))
        self.screen.blit(text, (restart_button.x + 50, restart_button.y + 10))
        text = font.render('Quit', True, (0, 0, 0))
        self.screen.blit(text, (quit_button.x + 70, quit_button.y + 10))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        waiting = False
                        self.width = 800  # Set a larger default width
                        self.height = 600 
                        self.screen = pygame.display.set_mode((self.width, self.height))
                        self.home_page()
                        self.new()
                        self.run()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        quit(0)

game = Game()
while True:
    game.home_page()
    game.new()
    game.run()