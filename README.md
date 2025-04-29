# Snake Game - Ultimate Edition

## Overview
This is a modern, feature-rich implementation of the classic Snake game with multiple control schemes, power-ups, and visual effects. The game is available in both web (HTML5/JavaScript) and desktop (Python/Pygame) versions.

## Features

### Core Gameplay
- Classic snake mechanics with smooth movement
- Growing snake when eating food
- Wall wrapping (snake can go through walls)
- Self-collision detection (game over if snake hits itself)

### Visual Enhancements
- Smooth color gradients for snake body
- Animated food with glow effects
- Pulsing power-ups
- Dynamic level transitions with zoom effects
- Grid background for better orientation

### Game Modes
- **Keyboard control**: Traditional arrow key controls
- **Touch control**: Swipe gestures on touch devices (web version)
- **Finger tracking**: Control the snake by pointing with your finger (desktop version using webcam)

### Power-ups
- **Speed Boost**: Increases snake speed temporarily
- **Slow Down**: Decreases snake speed temporarily
- **Score Multiplier**: Gives bonus points
- **Shield**: (Future implementation) Protects from collisions

### Progression System
- Level progression based on score
- Increasing difficulty (speed increases with level)
- Visual border color changes between levels

## Requirements

### Web Version
- Modern web browser (Chrome, Firefox, Edge, Safari)
- No additional dependencies

### Desktop Version
- Python 3.6+
- Required packages:
  ```
  pygame
  opencv-python
  mediapipe
  numpy
  ```

## Installation

### Web Version
1. Simply open the `index.html` file in your browser
2. Or host it on any web server

### Desktop Version
1. Install Python 3.6+ if not already installed
2. Install required packages:
   ```bash
   pip install pygame opencv-python mediapipe numpy
   ```
3. Run the game:
   ```bash
   python snake_game.py
   ```

## Controls

### Web Version
- **Arrow keys**: Move the snake
- **C**: Toggle between keyboard and touch control modes
- **H**: Toggle help screen
- **R**: Reset game
- **Q**: Quit game

### Desktop Version
- **Arrow keys**: Move the snake (keyboard mode)
- **Point with finger**: Move the snake (finger tracking mode)
- **C**: Toggle control mode
- **H**: Toggle help screen
- **R**: Reset game
- **Q**: Quit game

## File Structure

### Web Version
```
snake-game/
│── index.html          # Main HTML file with embedded CSS/JS
```

### Desktop Version
```
snake-game/
│── snake_game.py       # Main Python game file
```

## Future Improvements
- Add more power-up types
- Implement shield functionality
- Add sound effects and background music
- Create mobile app versions
- Add multiplayer mode

## Credits
Developed by ALBIN RAJU

