# Minesweeper AI Solver


A Python implementation of the classic Minesweeper game with an AI solver powered by the **NEAT (NeuroEvolution of Augmenting Topologies)** algorithm. The AI learns to play Minesweeper by evolving neural networks over multiple generations.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How the AI Works](#how-the-ai-works)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project is a Python implementation of Minesweeper with an AI solver that uses the **NEAT algorithm** to learn how to play the game. The AI starts with no knowledge of the game and evolves over generations to become better at detecting mines and solving the board.

The game includes:
- A fully functional Minesweeper game with customizable difficulty levels.
- An AI that uses logic and probability to solve the game.
- A NEAT-based neural network that learns to play Minesweeper through trial and error.

---

## Features

- **Classic Minesweeper Gameplay**:
  - Three difficulty levels: **Easy**, **Medium**, and **Hard**.
  - Left-click to reveal tiles, right-click to flag mines.
  - Win by revealing all safe tiles without clicking on a mine.

- **AI Solver**:
  - Uses **logic and probability** to determine safe moves.
  - Flags tiles that are certain to contain mines.
  - Falls back on a **NEAT-based neural network** for uncertain moves.

- **NEAT Algorithm**:
  - Evolves neural networks over generations to improve performance.
  - Rewards the AI for safe moves and penalizes it for clicking mines.

- **Customizable Settings**:
  - Adjust board size, number of mines, and NEAT parameters.

---

## Installation

### Prerequisites
- **Python 3.7 or higher**
- **Pygame**
- **NEAT-Python**

### Steps
1. Clone the repository:
   git clone https://github.com/your-username/minesweeper-ai.git
   cd minesweeper-ai
2.Install the required dependencies:

   Copy
   pip install -r requirements.txt

3.Run the game:

   Copy
   python main.py

---
## Usage
### Playing the Game
1.Launch the game by running main.py.

2.Select a difficulty level (Easy, Medium, or Hard).

3.Use the mouse to:

- Left-click to reveal tiles.

- Right-click to flag potential mines.

4.Win by revealing all safe tiles without clicking on a mine.

### Training the AI
1.To train the AI using the NEAT algorithm, run:

   Copy
   python main.py
2.The AI will start with random moves and gradually improve over generations.

3.Observe the AI's performance and fitness scores in the console.
---
## How the AI Works
The AI uses a combination of logic and neural networks to solve Minesweeper:

1.Logic-Based Moves:

- The AI analyzes revealed tiles to determine safe moves and flag mines.

- If a tile's number equals the number of flagged neighboring tiles, the remaining unrevealed neighbors are safe to click.

- If a tile's number minus the number of flagged neighbors equals the number of unrevealed neighbors, the unrevealed neighbors are mines and are flagged.

2.Neural Network:

- When no safe moves are available, the AI uses a NEAT-based neural network to make a guess.

- The neural network takes the current board state as input and outputs a move.

- The AI is rewarded for safe moves and penalized for clicking mines.

3.NEAT Algorithm:

- The NEAT algorithm evolves the neural network over generations.

- The fittest networks are selected for reproduction, and mutations introduce new variations.
---
## Technologies Used ##
- **Python: The core programming language.**

- **Pygame: Used for rendering the game and handling user input.**

- **NEAT-Python: Implements the NEAT algorithm for evolving neural networks.**

## Contributing 
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes and push to the branch.

Submit a pull request with a detailed description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Inspired by the classic Minesweeper game.

NEAT algorithm implementation by NEAT-Python.
