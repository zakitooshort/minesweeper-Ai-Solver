import pygame
import numpy as np
import neat
import os
import pickle
import time
import random
from sprites import Board
from settings import *

class MinesweeperAI:
    def __init__(self, rows=5, cols=5, num_mines=3, visualize=False):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = Board(rows, cols, num_mines)
        self.visualize = visualize
        
        if visualize:
            pygame.init()
            self.screen_width = TILESIZE * cols
            self.screen_height = TILESIZE * rows
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Minesweeper AI")
            self.clock = pygame.time.Clock()

    def get_state(self):
        """Get a flattened representation of the board state for the neural network"""
        state = []
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board.board_list[x][y]
                if tile.revealed:
                    if tile.type == "C":
                        state.append(self.board.check_neighbours(x, y))
                    elif tile.type == "X":
                        state.append(9)  # Mine
                    else:
                        state.append(0)  # Empty revealed tile
                elif tile.flagged:
                    state.append(10)     # Flagged tile
                else:
                    state.append(-1)     # Unrevealed tile
        return np.array(state)

    def make_move(self, net):
        state = self.get_state()
        output = net.activate(state)

        valid_moves = []
        for x in range(self.rows):
            for y in range(self.cols):
                if not self.board.board_list[x][y].revealed and not self.board.board_list[x][y].flagged:
                    valid_moves.append((x, y))

        if not valid_moves:
            return None

        # Find the best move based on neural network output
        best_move = None
        best_score = -float('inf')
        for x, y in valid_moves:
            move_index = x * self.cols + y
            if output[move_index] > best_score:
                best_score = output[move_index]
                best_move = (x, y)

        return best_move

    def flag_obvious_mines(self):
        """Flag tiles that are obviously mines based on revealed numbers"""
        flagged = False
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board.board_list[x][y]
                if tile.revealed and tile.type == "C":
                    # Count surrounding unrevealed and flagged tiles
                    adjacent_number = self.board.check_neighbours(x, y)
                    unrevealed = []
                    flagged_count = 0
                    
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if self.board.is_inside(nx, ny):
                                neighbor = self.board.board_list[nx][ny]
                                if not neighbor.revealed:
                                    if neighbor.flagged:
                                        flagged_count += 1
                                    else:
                                        unrevealed.append((nx, ny))
                    
                    # If the number of adjacent unrevealed tiles equals the number, they must all be mines
                    if adjacent_number - flagged_count == len(unrevealed) and len(unrevealed) > 0:
                        for ux, uy in unrevealed:
                            self.board.board_list[ux][uy].flagged = True
                            flagged = True
        
        return flagged

    def dig_safe_tiles(self):
        """Dig tiles that are obviously safe based on revealed numbers and flags"""
        dug = False
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board.board_list[x][y]
                if tile.revealed and tile.type == "C":
                    # Count surrounding flags and unrevealed tiles
                    adjacent_number = self.board.check_neighbours(x, y)
                    unrevealed = []
                    flagged_count = 0
                    
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if self.board.is_inside(nx, ny):
                                neighbor = self.board.board_list[nx][ny]
                                if not neighbor.revealed:
                                    if neighbor.flagged:
                                        flagged_count += 1
                                    else:
                                        unrevealed.append((nx, ny))
                    
                    # If the number of adjacent flags equals the number, all other unrevealed are safe
                    if adjacent_number == flagged_count and len(unrevealed) > 0:
                        for ux, uy in unrevealed:
                            if self.board.dig(ux, uy) == False:
                                return False, True  # Hit a mine
                            dug = True
        
        return dug, False

    def use_logic_first(self):
        """Use deterministic logic before using the neural network"""
        # Apply deterministic strategies first
        hit_mine = False
        made_progress = True
        
        while made_progress and not hit_mine:
            # Try to flag obvious mines
            flagged = self.flag_obvious_mines()
            
            # Try to dig safe tiles
            dug, hit_mine = self.dig_safe_tiles()
            
            # If we didn't make progress with either method, break the loop
            made_progress = flagged or dug
            
            if self.visualize:
                self.draw()
                pygame.display.flip()
                time.sleep(0.5)
                self.handle_events()
        
        return not hit_mine

    def play_game(self, net):
        self.board = Board(self.rows, self.cols, self.num_mines)
        fitness = 0
        safe_tiles_revealed = 0
        total_safe_tiles = self.rows * self.cols - self.num_mines
        game_over = False
        
        try:
            # Make first move in the center (usually safer)
            center_x, center_y = self.rows // 2, self.cols // 2
            if not self.board.dig(center_x, center_y):
                fitness -= 10
                if self.visualize:
                    self.draw()
                    self.handle_events()
                    time.sleep(2)
                return fitness
            
            safe_tiles_revealed += 1
            
            while not game_over:
                if self.visualize:
                    self.draw()
                    pygame.display.flip()
                    time.sleep(0.5)
                    self.handle_events()
                
                # First try to use deterministic logic
                if not self.use_logic_first():
                    fitness -= 10
                    game_over = True
                    break
                
                # Check if we've won
                if self.check_win():
                    fitness += 100 + (safe_tiles_revealed / total_safe_tiles) * 100
                    game_over = True
                    break
                
                # If deterministic logic can't help, use neural network
                move = self.make_move(net)
                if move is None:
                    break
                
                x, y = move
                if self.visualize:
                    print(f"AI move: ({x}, {y})")
                
                if not self.board.dig(x, y):
                    fitness -= 10
                    game_over = True
                else:
                    safe_tiles_revealed += 1
                    fitness += 1 + (safe_tiles_revealed / total_safe_tiles) * 0.5
                    
                    # Extra reward for uncovering more cells at once
                    revealed_count = 0
                    for row in self.board.board_list:
                        for tile in row:
                            if tile.revealed:
                                revealed_count += 1
                    
                    if revealed_count > safe_tiles_revealed:
                        fitness += (revealed_count - safe_tiles_revealed) * 0.2
                        safe_tiles_revealed = revealed_count
                    
                    if self.check_win():
                        fitness += 100 + (safe_tiles_revealed / total_safe_tiles) * 100
                        game_over = True
            
            if self.visualize:
                # Show final state and wait for a moment
                self.draw_game_over(game_over and fitness > 0)
                pygame.display.flip()
                time.sleep(3)
            
            return fitness
            
        except Exception as e:
            print(f"Error during AI gameplay: {str(e)}")
            return -20  # Return a negative fitness for failed games

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
    
    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
    
    def draw_game_over(self, win):
        # Reveal all mines
        for row in self.board.board_list:
            for tile in row:
                if tile.type == "X":
                    tile.revealed = True
        
        self.draw()
        font = pygame.font.SysFont('Arial', 30)
        if win:
            text = font.render('AI Won!', True, GREEN)
        else:
            text = font.render('AI Lost!', True, RED)
        
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        pygame.draw.rect(self.screen, DARKGRAY, text_rect.inflate(20, 10))
        self.screen.blit(text, text_rect)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        
        # Run multiple games to get a better evaluation
        total_fitness = 0
        num_games = 3
        
        for _ in range(num_games):
            # Train on all difficulties
            difficulty = random.choice(['easy', 'medium', 'hard'])
            settings = DIFFICULTY_SETTINGS[difficulty]
            rows, cols, mines = settings['ROWS'], settings['COLS'], settings['AMOUT_MINES']
            
            ai = MinesweeperAI(rows=rows, cols=cols, num_mines=mines)
            fitness = ai.play_game(net)
            total_fitness += fitness
        
        genome.fitness = total_fitness / num_games
        print(f"Genome {genome_id} Avg Fitness: {genome.fitness:.2f}")

def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Checkpoint every 5 generations
    population.add_reporter(neat.Checkpointer(5, filename_prefix='neat-checkpoint-'))

    winner = population.run(eval_genomes, 100)  # Run for 100 generations

    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("\nBest genome saved to 'best_genome.pkl'.")
    
    return winner

def play_with_best_genome(config_file, genome_file, visualize=True):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_file)

    with open(genome_file, "rb") as f:
        best_genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    # Get difficulty settings from user
    if visualize:
        difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
        if difficulty not in ['easy', 'medium', 'hard']:
            difficulty = 'easy'
        
        settings = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS['easy'])
        rows, cols, mines = settings['ROWS'], settings['COLS'], settings['AMOUT_MINES']
    else:
        rows, cols, mines = 5, 5, 3

    ai = MinesweeperAI(rows=rows, cols=cols, num_mines=mines, visualize=visualize)
    try:
        fitness = ai.play_game(net)
        return fitness
    except (SystemExit, KeyboardInterrupt):
        # Handle ESC key or window close
        return None
    except Exception as e:
        print(f"AI failed: {str(e)}")
        return None

def continue_training(config_file, checkpoint=None):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    
    if checkpoint:
        population = neat.Checkpointer.restore_checkpoint(checkpoint)
    else:
        # Try to load the best genome and create a new population from it
        try:
            with open("best_genome.pkl", "rb") as f:
                best_genome = pickle.load(f)
            
            print("Continuing training with the best genome as starting point...")
            population = neat.Population(config)
            population.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            population.add_reporter(stats)
            
            # Add the best genome
            population.population[0] = best_genome
            # Generate new genomes based on the best one
            for i in range(1, config.pop_size):
                new_genome = neat.DefaultGenome(i)
                new_genome.configure_crossover(best_genome, best_genome, config.genome_config)
                new_genome.mutate(config.genome_config)
                population.population[i] = new_genome
        except:
            print("No existing best genome found. Starting fresh...")
            population = neat.Population(config)
    
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(neat.Checkpointer(5, filename_prefix='neat-checkpoint-'))
    
    winner = population.run(eval_genomes, 50)
    
    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("\nBest genome saved to 'best_genome.pkl'.")

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")

    if not pygame.get_init():
        pygame.init()

    # Show menu with options
    print("\nMinesweeper AI with NEAT")
    print("1. Train new AI")
    print("2. Continue training from best genome")
    print("3. Continue training from checkpoint")
    print("4. Play with best AI (visualized)")
    print("5. Test best AI performance (no visualization)")
    print("6. Exit")
    
    choice = input("\nSelect an option (1-6): ").strip()
    
    if choice == '1':
        run_neat(config_path)
    elif choice == '2':
        continue_training(config_path)
    elif choice == '3':
        checkpoint_files = [f for f in os.listdir('.') if f.startswith('neat-checkpoint-')]
        if checkpoint_files:
            checkpoint_files.sort()
            checkpoint = checkpoint_files[-1]  # Get the latest checkpoint
            print(f"Continuing from checkpoint: {checkpoint}")
            continue_training(config_path, checkpoint)
        else:
            print("No checkpoint files found. Starting fresh training...")
            run_neat(config_path)
    elif choice == '4':
        genome_file = "best_genome.pkl"
        if os.path.exists(genome_file):
            play_with_best_genome(config_path, genome_file, visualize=True)
        else:
            print("No saved genome found. Please train the AI first.")
    elif choice == '5':
        genome_file = "best_genome.pkl"
        if os.path.exists(genome_file):
            total_score = 0
            games = 10
            for i in range(games):
                score = play_with_best_genome(config_path, genome_file, visualize=False)
                total_score += score
                print(f"Game {i+1}/{games}: Score = {score}")
            
            print(f"\nAverage score over {games} games: {total_score/games:.2f}")
        else:
            print("No saved genome found. Please train the AI first.")
    elif choice == '6':
        print("Exiting...")
    else:
        print("Invalid choice. Exiting...")