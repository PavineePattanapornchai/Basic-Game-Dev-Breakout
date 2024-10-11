# Basic-Game-Dev-Breakout

## Overview
Breakout Evolution is a reimagined take on the timeless brick-breaking game. It introduces new elements like random power-up drops, including multi-ball and extra life, and a dragon monster that appears from level 2 onward to increase the challenge. A functional pause/resume menu allows for better control during gameplay. Each level brings unpredictable dynamics thanks to randomized power-ups when breaking bricks.

## Key Features
- **Power-Ups**: Random power-ups drop as bricks are broken, featuring extra life and multi-ball options. Every level has at least two power-ups.
- **Multi-Ball**: Gain multiple balls to increase the chances of hitting bricks, with all balls behaving like the main one.
- **Dragon Monster**: Starting at level 2, a dragon appears as an additional obstacle. If hit by a ball, it costs one life.
- **Pause/Resume Menu**: Players can pause the game, resume or return to the home menu with ease.
- **Dynamic Gameplay**: With random power-up drops and varying level challenges, every playthrough is unique.

## Installation & Running Instructions
1. Clone or download the project repository:
    ```bash
    git clone <repository-url>
    ```
2. Ensure that Python 3.x and Pygame are installed on your system.
    ```bash
    pip install pygame
    ```
3. Navigate to the game directory and run the `main.py` file:
    ```bash
    python main.py
    ```
4. Use the keyboard to play:
    - `Arrow keys`: Move the paddle left or right
    - `Space`: Pause/Resume the game
    - `Enter`: Confirm selections and serve the ball

