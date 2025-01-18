import pygame
import numpy as np
import neat
import os
import pickle
from sprites import Board
from settings import *

class MinesweeperAI:
    def __init__(self, rows=5, cols=5, num_mines=3):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = Board(rows, cols, num_mines)

    def get_state(self):
        state = []
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.board.board_list[x][y]
                if tile.revealed:
                    if tile.type == "C":
                        state.append(self.board.check_neighbours(x, y))
                    else:
                        state.append(9)
                elif tile.flagged:
                    state.append(10)
                else:
                    state.append(-1)
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

        best_move = None
        best_score = -float('inf')
        for x, y in valid_moves:
            move_index = x * self.cols + y
            if output[move_index] > best_score:
                best_score = output[move_index]
                best_move = (x, y)

        return best_move

    def play_game(self, net):
        self.board = Board(self.rows, self.cols, self.num_mines)
        fitness = 0
        while True:
            move = self.make_move(net)
            if move is None:
                print("No valid moves left. Game over.")
                break

            x, y = move
            print(f"AI move: ({x}, {y})")
            if not self.board.dig(x, y):
                fitness -= 10
                print("AI hit a mine! Game over.")
                break
            else:
                fitness += 1
                print(f"Revealed safe tile. Fitness: {fitness}")
                if self.check_win():
                    fitness += 100
                    print("AI won the game!")
                    break
        return fitness

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        return True

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        ai = MinesweeperAI(rows=5, cols=5, num_mines=3)
        fitness = ai.play_game(net)
        genome.fitness = fitness
        print(f"Genome {genome_id} Fitness: {fitness}")

def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    with open("best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("Best genome saved to 'best_genome.pkl'.")

def play_with_best_genome(config_file, genome_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    with open(genome_file, "rb") as f:
        best_genome = pickle.load(f)

    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    ai = MinesweeperAI(rows=5, cols=5, num_mines=3)

    ai.play_game(net)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")

    mode = input("Enter 'train' to train the AI or 'play' to use the best genome: ").strip().lower()

    if mode == "train":
        run_neat(config_path)
    elif mode == "play":
        genome_file = "best_genome.pkl"
        if os.path.exists(genome_file):
            play_with_best_genome(config_path, genome_file)
        else:
            print("No saved genome found. Please train the AI first.")
    else:
        print("Invalid mode. Please enter 'train' or 'play'.")