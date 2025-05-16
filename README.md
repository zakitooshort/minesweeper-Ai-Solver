# Minesweeper AI Solver

A Minesweeper game with an AI solver using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to learn how to play the game.

## Features

- Classic Minesweeper gameplay with multiple difficulty levels
- AI solver using a trained neural network
- Training system for the AI using NEAT
- Visualization of AI gameplay
- Deterministic solving for obvious moves
- Ability to continue training from checkpoints

## Prerequisites

- Python 3.6+
- pygame
- neat-python
- numpy

## Installation

1. Clone the repository or download the source code
2. Install the required packages:

```bash
pip install pygame neat-python numpy
```

3. Run the game:

```bash
python run.py
```

## How to Play

### Manual Play

1. Select "Play Game" from the main menu
2. Choose a difficulty level (Easy, Medium, Hard)
3. Left-click to reveal a tile
4. Right-click to flag/unflag a tile
5. Try to uncover all non-mine tiles without hitting any mines!

### AI Solver

1. Select "AI Solver" from the main menu
2. Choose a difficulty level
3. Watch as the AI attempts to solve the puzzle

### Training the AI

1. Select "Train AI" from the main menu
2. Choose an option:
   - Train new AI: Start training from scratch
   - Continue training from best genome: Continue training using the best genome so far
   - Continue training from checkpoint: Resume training from a saved checkpoint

## How the AI Works

### NEAT Algorithm

The AI uses NEAT (NeuroEvolution of Augmenting Topologies), which is an evolutionary algorithm that creates artificial neural networks. 

Key aspects of the implementation:

1. **Input Representation**: The AI receives a flattened representation of the board as input, where:
   - -1 = Unrevealed tile
   - 0-8 = Revealed tile with number of adjacent mines
   - 9 = Revealed mine
   - 10 = Flagged tile

2. **Output**: The neural network outputs a value for each position on the board. The highest value for an unrevealed tile is chosen as the next move.

3. **Fitness Function**: The AI is rewarded for successfully revealing safe tiles and heavily rewarded for winning the game. It is penalized for hitting mines.

4. **Hybrid Approach**: The AI combines deterministic rules for obvious moves with neural network decisions for uncertain situations.

### Deterministic Logic

Before using the neural network, the AI attempts to make obvious moves using deterministic logic:

1. **Flag obvious mines**: If a revealed number has exactly that many unrevealed tiles around it, all those tiles must be mines and are flagged.

2. **Reveal obvious safe tiles**: If a revealed number has exactly that many flags around it, all other unrevealed tiles around it must be safe and can be revealed.

### Neural Network

When deterministic logic can't make a decision, the neural network evaluates all possible moves and chooses the one with the highest confidence score.

## Project Structure

- `run.py`: Main launcher script
- `menu.py`: Main menu interface
- `game.py`: Manual gameplay implementation
- `main.py`: AI solver implementation
- `sprites.py`: Game board and tile implementation
- `settings.py`: Game settings and constants
- `neat-config.txt`: Configuration for the NEAT algorithm
- `best_genome.pkl`: Saved best AI (if training has been done)

## Customization

You can customize the game by editing the following files:

- `settings.py`: Adjust difficulty settings, board sizes, colors, etc.
- `neat-config.txt`: Modify NEAT parameters to change how the AI evolves

## License

This project is open-source and available under the MIT License.

## Acknowledgments

- Original Minesweeper game concept by Microsoft
- NEAT algorithm by Kenneth O. Stanley
- NEAT-Python implementation by CodeReclaimers
