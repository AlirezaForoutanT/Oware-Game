# Oware Game with Minimax AI

This is a Python implementation of the game Oware along with an AI player using the Minimax algorithm with alpha-beta pruning.

## Game Overview

Oware is a traditional African board game for two players. The game is played on a board with 12 small pits, called "holes", arranged in two rows. Each player controls one of the rows. At the beginning of the game, each hole is filled with a certain number of seeds.

The players take turns making moves. During a move, a player selects one of the holes from their row and redistributes its seeds in a counterclockwise direction, dropping one seed in each hole until they run out. If the last seed is dropped into an opponent's hole with 2 or 3 seeds, these seeds are captured and removed from play.

The game ends when one player has captured enough seeds to win, typically determined by a threshold of total seeds captured.

## Features

- Human vs. AI gameplay: You can play against the AI, which uses the Minimax algorithm to make decisions.
- Simple user interface: The game prompts the user for input when it's their turn and displays the current state of the board.
- Customizable parameters: You can adjust the number of holes, seeds per hole, and colors to tailor the game to your preferences.

## Requirements

- Python 3.x

## Usage

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Run the `oware.py` file using Python: `python oware.py`.
4. Follow the on-screen instructions to play the game.
5. Enjoy the game!

## Credits

This implementation was created by Alireza Foroutan.
