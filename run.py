#!/usr/bin/env python3
"""
Minesweeper AI Solver - Launcher Script

This script launches the Minesweeper AI Solver game.
"""

import sys
import os

# Ensure we're in the correct directory
if getattr(sys, 'frozen', False):
    # We're running in a bundle
    script_dir = os.path.dirname(sys.executable)
else:
    # We're running in a normal Python environment
    script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)

try:
    from menu import MainMenu
except ImportError:
    print("Error: Could not import the game modules. Make sure you're running this script from the game directory.")
    input("Press Enter to exit...")
    sys.exit(1)

if __name__ == "__main__":
    print("Starting Minesweeper AI Solver...")
    menu = MainMenu()
    menu.run() 