

# **Snake Game - Ultimate Edition** 🐍  

![Snake Game Banner](https://img.itch.zone/aW1nLzEyODQzNzgucG5n/original/BrHZ%2Fn.png)  

A **modern, feature-rich** implementation of the classic Snake game with **multiple control schemes, power-ups, and visual effects**. Available in:  
✅ **Web (HTML5/JavaScript)** – Playable on any device  
✅ **Desktop (Python/Pygame)** – With **finger-tracking** via webcam  

**Play Now:** 🌐 [HTML5 Version](https://albinraju29.github.io/snake_game/)  

---

## **📖 Table of Contents**  
1. [Features](#-features)  
2. [Pygame (Desktop) Version](#-pygame-desktop-version)  
   - [Installation](#-installation)  
   - [How to Run](#-how-to-run)  
   - [Controls](#-controls)  
3. [HTML5 (Web) Version](#-html5-web-version)  
   - [How to Play](#-how-to-play)  
4. [Game Mechanics](#-game-mechanics)  
5. [Technical Details](#-technical-details)  
6. [Screenshots](#-screenshots)  
7. [Future Improvements](#-future-improvements)  
8. [Contributing](#-contributing)  
9. [License](#-license)  

---

## **✨ Features**  

### **🎮 Core Gameplay**  
- Classic snake mechanics with **smooth movement**  
- Snake grows when eating food  
- **Wall wrapping** (snake can go through walls)  
- **Self-collision detection** (game over if snake hits itself)  

### **🎨 Visual Enhancements**  
- Smooth **color gradients** for snake body  
- **Animated food** with glow effects  
- **Pulsing power-ups**  
- Dynamic **level transitions** with zoom effects  
- **Grid background** for better orientation  

### **🕹️ Game Modes**  
- **Keyboard control**: Arrow keys (desktop & web)  
- **Touch control**: Swipe gestures (mobile web)  
- **Finger tracking**: Control snake with your finger (Pygame + webcam)  

### **⚡ Power-ups**  
- **Speed Boost** → Increases snake speed temporarily  
- **Slow Down** → Decreases snake speed temporarily  
- **Score Multiplier** → Bonus points  
- **Shield** → *(Coming soon!)* Protects from collisions  

### **📈 Progression System**  
- Level progression based on score  
- Increasing difficulty (speed increases with level)  
- Visual border color changes between levels  

---

## **🐍 Pygame (Desktop) Version**  

### **📥 Installation**  
1. **Requires Python 3.6+**  
2. Install dependencies:  
   ```bash
   pip install pygame opencv-python mediapipe numpy
   ```

### **🚀 How to Run**  
```bash
python snake_game.py
```

### **🎮 Controls**  
| **Key**       | **Action**                     |
|---------------|-------------------------------|
| **Arrow Keys** | Move the snake                |
| **C**          | Toggle keyboard/finger mode   |
| **H**          | Toggle help screen            |
| **R**          | Reset game                    |
| **Q**          | Quit game                     |

**Finger Tracking Mode:**  
👉 Point your finger at the webcam to control the snake!  

---

## **🌐 HTML5 (Web) Version**  

### **🎮 How to Play**  
- **Desktop:**  
  - **Arrow Keys** → Move the snake  
  - **R** → Reset game  
- **Mobile:**  
  - **Swipe** → Change direction  
  - **Tap Pause Button** → Reset game  

**Play Now:** 👉 [HTML5 Snake Game](https://albinraju29.github.io/snake_game/)  

---

## **🔧 Game Mechanics**  
- **Movement:** Grid-based with smooth transitions  
- **Collision:** Detects walls, self, and power-ups  
- **Scoring:**  
  - `+10` points per food  
  - `+50` for power-ups  

---

## **⚙️ Technical Details**  

### **Pygame Version**  
```python
# Core game loop
while running:
    handle_input()  # Keyboard or webcam input
    update_snake()  # Movement & collision
    spawn_food()    # Random food/power-ups
    draw_graphics() # Animated effects
```

### **HTML5 Version**  
```javascript
// Game loop using requestAnimationFrame
function gameLoop() {
    updateSnakePosition();
    checkCollisions();
    drawCanvas();
    requestAnimationFrame(gameLoop);
}
```

---

## **📸 Screenshots**  

| **Pygame Version** | **HTML5 Version** |
|--------------------|------------------|
| ![Pygame Snake](https://i.imgur.com/pygame_snake.png) | ![Web Snake](https://i.imgur.com/html5_snake.png) |  

---

## **🚀 Future Improvements**  
- [ ] **Shield power-up** (immunity to collisions)  
- [ ] **Multiplayer mode** (local/online)  
- [ ] **Sound effects & music**  
- [ ] **Mobile app** (Android/iOS)  

---

## **🤝 Contributing**  
1. **Fork** the repository  
2. Create a new branch (`git checkout -b feature`)  
3. Commit changes (`git commit -m "Add feature"`)  
4. Push (`git push origin feature`)  
5. Open a **Pull Request**  

---

## **📜 License**  
**MIT License** - See [LICENSE](LICENSE) for details.  

---

**Developed with ❤️ by [Albin Raju](https://github.com/albinraju29)**  
🐍 **Happy Gaming!** 🚀  

``` 
