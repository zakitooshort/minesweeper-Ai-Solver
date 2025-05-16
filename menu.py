import pygame
import sys
import os
import main
import game
from settings import *

class MainMenu:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Set up the display
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper AI Solver - Main Menu")
        
        # Create fonts
        self.font_title = pygame.font.SysFont('Arial', 54)
        self.font_subtitle = pygame.font.SysFont('Arial', 36)
        self.font_button = pygame.font.SysFont('Arial', 28)
        self.font_small = pygame.font.SysFont('Arial', 20)
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
    def run(self):
        running = True
        
        while running:
            self.screen.fill(BGCOLOUR)
            
            # Draw title
            title_text = self.font_title.render("Minesweeper AI Solver", True, WHITE)
            subtitle_text = self.font_subtitle.render("Choose an Option", True, LIGHTGRAY)
            
            self.screen.blit(title_text, (self.width // 2 - title_text.get_width() // 2, 80))
            self.screen.blit(subtitle_text, (self.width // 2 - subtitle_text.get_width() // 2, 150))
            
            # Create buttons
            play_button = pygame.Rect(self.width // 2 - 150, 220, 300, 60)
            ai_button = pygame.Rect(self.width // 2 - 150, 300, 300, 60)
            train_button = pygame.Rect(self.width // 2 - 150, 380, 300, 60)
            exit_button = pygame.Rect(self.width // 2 - 150, 460, 300, 60)
            
            # Draw buttons with shadow effect
            button_colors = [GREEN, BLUE, YELLOW, RED]
            button_texts = ["Play Game", "AI Solver", "Train AI", "Exit"]
            buttons = [play_button, ai_button, train_button, exit_button]
            
            for button, color, text in zip(buttons, button_colors, button_texts):
                pygame.draw.rect(self.screen, DARKGRAY, button.inflate(8, 8))
                pygame.draw.rect(self.screen, color, button)
                
                text_surf = self.font_button.render(text, True, BLACK)
                self.screen.blit(text_surf, (button.centerx - text_surf.get_width() // 2, 
                                             button.centery - text_surf.get_height() // 2))
            
            # Draw version info
            version_text = self.font_small.render("v1.0", True, LIGHTGRAY)
            self.screen.blit(version_text, (self.width - version_text.get_width() - 10, 
                                           self.height - version_text.get_height() - 10))
            
            # Update display
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        # Launch manual game
                        self.launch_game()
                    elif ai_button.collidepoint(event.pos):
                        # Launch AI solver
                        self.launch_ai_solver()
                    elif train_button.collidepoint(event.pos):
                        # Launch AI training
                        self.launch_ai_training()
                    elif exit_button.collidepoint(event.pos):
                        running = False
            
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
        
    def launch_game(self):
        """Launch the manual gameplay mode"""
        pygame.quit()  # Quit pygame to reset display
        game.play_game()
        # Reinitialize pygame after game exits
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper AI Solver - Main Menu")
        
    def launch_ai_solver(self):
        """Launch the AI solver mode"""
        pygame.quit()  # Quit pygame to reset display
        
        # Get the path to the config file and best genome
        local_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(local_dir, "neat-config.txt")
        genome_file = "best_genome.pkl"
        
        if os.path.exists(genome_file):
            try:
                main.play_with_best_genome(config_path, genome_file, visualize=True)
            except Exception as e:
                print(f"AI failed: {str(e)}")
                input("Press Enter to return to main menu...")
        else:
            print("No trained AI found. Please train the AI first.")
            input("Press Enter to continue...")
            
        # Reinitialize pygame after game exits
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper AI Solver - Main Menu")
        
    def launch_ai_training(self):
        """Launch the AI training mode"""
        pygame.quit()  # Quit pygame to reset display
        
        # Show training options to the user
        print("\nMinesweeper AI Training")
        print("1. Train new AI")
        print("2. Continue training from best genome")
        print("3. Continue training from checkpoint")
        print("4. Back to menu")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        local_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(local_dir, "neat-config.txt")
        
        if choice == '1':
            main.run_neat(config_path)
        elif choice == '2':
            main.continue_training(config_path)
        elif choice == '3':
            checkpoint_files = [f for f in os.listdir('.') if f.startswith('neat-checkpoint-')]
            if checkpoint_files:
                checkpoint_files.sort()
                checkpoint = checkpoint_files[-1]  # Get the latest checkpoint
                print(f"Continuing from checkpoint: {checkpoint}")
                main.continue_training(config_path, checkpoint)
            else:
                print("No checkpoint files found. Starting fresh training...")
                main.run_neat(config_path)
        
        # Wait for user to read results
        input("\nPress Enter to return to main menu...")
        
        # Reinitialize pygame after training exits
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper AI Solver - Main Menu")

if __name__ == "__main__":
    menu = MainMenu()
    menu.run() 