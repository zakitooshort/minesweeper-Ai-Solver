# Minesweeper AI Solver

![Minesweeper Screenshot](screenshot.png) <!-- Add a screenshot if you have one -->

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
   ```bash
   git clone https://github.com/your-username/minesweeper-ai.git
   cd minesweeper-ai
