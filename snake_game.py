import pygame
import random
import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
DARK_GREEN = (0, 180, 0)
DARK_ORANGE = (200, 100, 0)
DARK_RED = (180, 0, 0)
GRID_COLOR = (30, 30, 30)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game - Ultimate Edition')

clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 48)
font_title = pygame.font.SysFont('Arial', 64, bold=True)

class PowerUp:
    def __init__(self):
        self.type = random.choice(["speed_boost", "slow_down", "score_multiplier", "shield"])
        self.position = (0, 0)
        self.color = self.get_color()
        self.duration = 300  # frames (5 seconds at 60fps)
        self.active = False
        self.spawn_time = pygame.time.get_ticks()
        self.randomize_position()
        self.size = CELL_SIZE
        self.pulse_phase = 0
        
    def get_color(self):
        return {
            "speed_boost": CYAN,
            "slow_down": MAGENTA,
            "score_multiplier": YELLOW,
            "shield": BLUE
        }[self.type]
        
    def randomize_position(self):
        self.position = (
            random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        )
        
    def update(self):
        self.pulse_phase = (self.pulse_phase + 0.05) % (2 * math.pi)
        self.size = CELL_SIZE * (0.9 + 0.1 * math.sin(self.pulse_phase))
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, 
                         (self.position[0] + CELL_SIZE//2, 
                          self.position[1] + CELL_SIZE//2), 
                         int(self.size//2))
        
        # Draw outer ring
        pygame.draw.circle(surface, WHITE, 
                         (self.position[0] + CELL_SIZE//2, 
                          self.position[1] + CELL_SIZE//2), 
                         int(self.size//2 + 2), 2)

class LevelSystem:
    def __init__(self):
        self.level = 1
        self.target_score = 10
        self.border_color = (255, 255, 255)
        self.transition_timer = 0
        self.zooming = False
        
    def update(self, score):
        if score >= self.target_score:
            self.level += 1
            self.target_score = self.level * 15
            self.border_color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
            self.transition_timer = 30  # 0.5 seconds at 60fps
            self.zooming = True
            return True
        return False
    
    def draw_border(self, surface):
        if self.transition_timer > 0:
            self.transition_timer -= 1
            zoom_factor = 1.0 + 0.05 * math.sin(self.transition_timer * 0.2)
            
            # Create zoom effect
            zoomed = pygame.transform.scale(surface, 
                                          (int(WIDTH * zoom_factor), 
                                           int(HEIGHT * zoom_factor)))
            surface.blit(zoomed, 
                        ((WIDTH - WIDTH * zoom_factor) // 2, 
                         (HEIGHT - HEIGHT * zoom_factor) // 2))
            
            if self.transition_timer == 0:
                self.zooming = False
        
        pygame.draw.rect(surface, self.border_color, (0, 0, WIDTH, HEIGHT), 5)
        
        # Draw level indicator
        level_text = font_medium.render(f"Level: {self.level}", True, self.border_color)
        surface.blit(level_text, (WIDTH - level_text.get_width() - 20, HEIGHT - 40))



class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.positions = [(WIDTH//2, HEIGHT//2)]
        self.direction = RIGHT
        self.grow_pending = False
        self.speed = 10
        self.length = 1
        self.difficulty = "Easy"
        self.body_colors = []
        
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * CELL_SIZE) % WIDTH, 
                   (head_y + dir_y * CELL_SIZE) % HEIGHT)
        
        if self.grow_pending:
            self.positions.insert(0, new_head)
            self.length += 1
            self.update_difficulty()
            self.update_body_colors()
            self.grow_pending = False
        else:
            self.positions = [new_head] + self.positions[:-1]
    
    def update_difficulty(self):
        if self.length < 10:
            self.difficulty = "Easy"
        elif self.length < 20:
            self.difficulty = "Medium"
        else:
            self.difficulty = "Hard"
    
    def update_body_colors(self):
        # Create a smooth color transition based on length
        self.body_colors = []
        for i in range(self.length):
            if self.difficulty == "Easy":
                # Green to light green gradient
                intensity = 150 + int(105 * (i / self.length))
                self.body_colors.append((0, intensity, 0))
            elif self.difficulty == "Medium":
                # Orange to yellow gradient
                intensity_r = 200 + int(55 * (i / self.length))
                intensity_g = 100 + int(155 * (i / self.length))
                self.body_colors.append((intensity_r, intensity_g, 0))
            else:
                # Red to pink gradient
                intensity_r = 180 + int(75 * (i / self.length))
                intensity_b = int(75 * (i / self.length))
                self.body_colors.append((intensity_r, 0, intensity_b))
    
    def grow(self):
        self.grow_pending = True
    
    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def draw(self, surface):
        # Draw round head with eyes
        head = self.positions[0]
        pygame.draw.circle(surface, BLUE, 
                         (head[0] + CELL_SIZE//2, head[1] + CELL_SIZE//2), 
                         CELL_SIZE//2)
        
        # Draw eyes based on direction
        eye_size = CELL_SIZE // 5
        if self.direction == RIGHT:
            eye1_pos = (head[0] + CELL_SIZE//2 + CELL_SIZE//4, head[1] + CELL_SIZE//3)
            eye2_pos = (head[0] + CELL_SIZE//2 + CELL_SIZE//4, head[1] + 2*CELL_SIZE//3)
        elif self.direction == LEFT:
            eye1_pos = (head[0] + CELL_SIZE//2 - CELL_SIZE//4, head[1] + CELL_SIZE//3)
            eye2_pos = (head[0] + CELL_SIZE//2 - CELL_SIZE//4, head[1] + 2*CELL_SIZE//3)
        elif self.direction == UP:
            eye1_pos = (head[0] + CELL_SIZE//3, head[1] + CELL_SIZE//2 - CELL_SIZE//4)
            eye2_pos = (head[0] + 2*CELL_SIZE//3, head[1] + CELL_SIZE//2 - CELL_SIZE//4)
        else:  # DOWN
            eye1_pos = (head[0] + CELL_SIZE//3, head[1] + CELL_SIZE//2 + CELL_SIZE//4)
            eye2_pos = (head[0] + 2*CELL_SIZE//3, head[1] + CELL_SIZE//2 + CELL_SIZE//4)
        
        pygame.draw.circle(surface, WHITE, eye1_pos, eye_size)
        pygame.draw.circle(surface, WHITE, eye2_pos, eye_size)
        
        # Draw body with smooth color transition
        for i, pos in enumerate(self.positions[1:]):
            color_index = min(i, len(self.body_colors)-1)
            pygame.draw.rect(surface, self.body_colors[color_index], 
                           pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
    
    def check_collision(self):
        return self.positions[0] in self.positions[1:]

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.glow_phase = 0
        self.size_phase = 0
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        )
    
    def update(self):
        # Add pulsing glow and size effect
        self.glow_phase = (self.glow_phase + 0.05) % (2 * np.pi)
        self.size_phase = (self.size_phase + 0.1) % (2 * np.pi)
        
        glow_intensity = int((np.sin(self.glow_phase) + 1)) * 50
        self.color = (min(255, RED[0] + glow_intensity), 
                     min(255, RED[1] + glow_intensity//2), 
                     min(255, RED[2] + glow_intensity//3))
    
    def draw(self, surface):
        # Calculate pulsing size
        size_factor = 0.8 + 0.2 * math.sin(self.size_phase)
        current_size = int(CELL_SIZE * size_factor)
        offset = (CELL_SIZE - current_size) // 2
        
        # Draw food with glow effect
        pygame.draw.circle(surface, self.color, 
                         (self.position[0] + CELL_SIZE//2, 
                          self.position[1] + CELL_SIZE//2), 
                         current_size//2)
        
        # Add subtle glow
        glow_radius = int(CELL_SIZE * 1.2)
        glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        glow_intensity = int(50 * (math.sin(self.glow_phase) + 1))
        pygame.draw.circle(glow_surface, (*self.color, glow_intensity), 
                          (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surface, (self.position[0] - glow_radius + CELL_SIZE//2, 
                                  self.position[1] - glow_radius + CELL_SIZE//2))

class FoodSystem:
    def __init__(self):
        self.foods = []
        self.powerups = []
        self.special_food_timer = 0
        
    def update(self):
        # Regular food spawn
        if random.random() < 0.01 and len(self.foods) < 3:
            self.foods.append(Food())
            
        # Special food spawn
        self.special_food_timer += 1
        if self.special_food_timer > 600 and len(self.powerups) < 2:  # Every 10 seconds
            self.powerups.append(PowerUp())
            self.special_food_timer = 0
            
        # Update all foods
        for food in self.foods:
            food.update()
        for powerup in self.powerups:
            powerup.update()
            
        # Remove expired powerups
        current_time = pygame.time.get_ticks()
        self.powerups = [p for p in self.powerups 
                         if current_time - p.spawn_time < 10000]  # 10 second lifespan
    
    def draw(self, surface):
        for food in self.foods:
            food.draw(surface)
        for powerup in self.powerups:
            powerup.draw(surface)

class FingerController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # For finger control
        self.prev_finger_pos = None
        self.direction_queue = deque(maxlen=3)
        self.deadzone = 20  # Slightly larger deadzone for stability
        self.smoothing_factor = 0.2  # For smoother direction changes
        
    def get_direction(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        direction = None
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get index finger tip (landmark 8)
                finger_tip = hand_landmarks.landmark[8]
                h, w = frame.shape[:2]
                finger_x, finger_y = int(finger_tip.x * w), int(finger_tip.y * h)
                
                # Draw elegant tracking visuals
                cv2.circle(frame, (finger_x, finger_y), 10, (0, 255, 0), 2)
                cv2.circle(frame, (finger_x, finger_y), 5, (0, 255, 255), -1)
                
                if self.prev_finger_pos:
                    dx = finger_x - self.prev_finger_pos[0]
                    dy = finger_y - self.prev_finger_pos[1]
                    
                    # Only change direction if movement exceeds deadzone
                    if abs(dx) > self.deadzone or abs(dy) > self.deadzone:
                        if abs(dx) > abs(dy):
                            direction = RIGHT if dx > 0 else LEFT
                        else:
                            direction = DOWN if dy > 0 else UP
                
                self.prev_finger_pos = (finger_x, finger_y)
        
        # Show the frame with tracking
        cv2.imshow('Finger Control - Point with index finger', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass
        
        return direction
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

def draw_game_over_screen(surface, score, high_score):
    # Dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    # Game over text
    game_over_text = font_title.render("GAME OVER", True, RED)
    surface.blit(game_over_text, 
                (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//4))
    
    # Score display
    score_text = font_large.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, 
                (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 40))
    
    # High score display
    high_text = font_large.render(f"High Score: {high_score}", True, YELLOW)
    surface.blit(high_text, 
                (WIDTH//2 - high_text.get_width()//2, HEIGHT//2 + 20))
    
    # Instructions
    restart_text = font_medium.render("Press R to Restart", True, WHITE)
    quit_text = font_medium.render("Press Q to Quit", True, WHITE)
    
    surface.blit(restart_text, 
                (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))
    surface.blit(quit_text, 
                (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 140))

def draw_minimal_ui(surface, score, high_score, difficulty, control_mode):
    # Score and high score in top left
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    high_text = font_small.render(f"High: {high_score}", True, YELLOW)
    surface.blit(score_text, (10, 10))
    surface.blit(high_text, (10, 40))
    
    # Control mode indicator in top right
    mode_text = font_small.render(f"Mode: {control_mode.upper()}", True, WHITE)
    surface.blit(mode_text, (WIDTH - mode_text.get_width() - 10, 10))
    
    # Difficulty indicator (color coded) in top right
    if difficulty == "Easy":
        diff_color = GREEN
    elif difficulty == "Medium":
        diff_color = ORANGE
    else:
        diff_color = RED
        
    diff_text = font_small.render(f"Level: {difficulty}", True, diff_color)
    surface.blit(diff_text, (WIDTH - diff_text.get_width() - 10, 40))

class TouchControls:
    def __init__(self):
        self.touch_start = None
        self.deadzone = 50
        
    def handle_event(self, event):
        if event.type == pygame.FINGERDOWN:
            self.touch_start = (event.x * WIDTH, event.y * HEIGHT)
        elif event.type == pygame.FINGERUP and self.touch_start:
            end_pos = (event.x * WIDTH, event.y * HEIGHT)
            dx = end_pos[0] - self.touch_start[0]
            dy = end_pos[1] - self.touch_start[1]
            
            if abs(dx) > self.deadzone or abs(dy) > self.deadzone:
                if abs(dx) > abs(dy):
                    return RIGHT if dx > 0 else LEFT
                else:
                    return DOWN if dy > 0 else UP
        return None
def main():
    snake = Snake()
    food = Food()
    powerups = [] 
    food_system = FoodSystem()
    level_system = LevelSystem()
    controller = FingerController()
    touch_controls = TouchControls()

    score = 0
    high_score = 0
    control_mode = 'finger'
    game_state = "playing"  # Can be "playing" or "game_over"
    show_help = True
    help_timer = 0
    
    # Main game loop
    running = True
    while running:
        clock.tick(snake.speed)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            snake.move()

            # Check if snake eats food
            if snake.positions[0] == food.position:
                snake.grow()
                score += 1
                food.randomize_position()

                # Chance to spawn a new powerup
                if random.random() < 0.3:  # 30% chance
                    powerups.append(PowerUp())

                # Update the level based on score
                level_system.update(score)

            for powerup in powerups[:]:
                if snake.positions[0] == powerup.position:
                    if powerup.type == "speed_boost":
                        snake.speed += 5
                    elif powerup.type == "slow_down":
                        snake.speed = max(5, snake.speed - 3)
                    elif powerup.type == "score_multiplier":
                        score += 5
                    elif powerup.type == "shield":
                        # (optional) you can implement shield logic
                        pass
                    powerups.remove(powerup)

            for powerup in powerups:
                powerup.update()

            snake.draw(screen)

            # Draw all powerups
            for powerup in powerups:
                powerup.draw(screen)

            # Draw border and level
            level_system.draw_border(screen)

            if event.type == pygame.KEYDOWN:
                if game_state == "playing":
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                    elif event.key == pygame.K_c:
                        control_mode = 'keyboard' if control_mode == 'finger' else 'finger'
                    elif event.key == pygame.K_h:
                        show_help = not show_help
                
                # These work in both game states
                if event.key == pygame.K_r:
                    # Reset game
                    if score > high_score:
                        high_score = score
                    snake.reset()
                    food.randomize_position()
                    score = 0
                    game_state = "playing"
                    show_help = True
                    help_timer = 0
                elif event.key == pygame.K_q:
                    running = False
        
        if game_state == "playing":
            # Get direction based on control mode
            if control_mode == 'finger':
                direction = controller.get_direction()
                if direction:
                    snake.change_direction(direction)
            
            # Game logic
            snake.move()
            food.update()
            
            # Check collisions
            if snake.check_collision():
                if score > high_score:
                    high_score = score
                game_state = "game_over"
            
            # Check if snake ate food
            if snake.positions[0] == food.position:
                snake.grow()
                food.randomize_position()
                while food.position in snake.positions:
                    food.randomize_position()
                score += 1
                
        for powerup in food_system.powerups[:]:
            if snake.positions[0] == powerup.position:
                    snake.activate_powerup(powerup.type)
                    food_system.powerups.remove(powerup)
                    score += 3
            
            # Level progression
        if level_system.update(score):
            snake.speed += 1  # Increase speed each level
        # Drawing
        screen.fill(BLACK)
        
        # Draw grid (faint)
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
        
        # Draw game elements
        snake.draw(screen)
        food.draw(screen)
        
        # Draw UI elements
        draw_minimal_ui(screen, score, high_score, snake.difficulty, control_mode)
        
        # Show help temporarily at start or when requested
        if show_help and game_state == "playing":
            help_text = [
                "CONTROLS:",
                "Arrow Keys - Move (keyboard mode)",
                "Point finger - Move (finger mode)",
                "C - Toggle control mode",
                "H - Toggle this help",
                " ",
                "R - Reset game anytime",
                "Q - Quit game"
            ]
            
            # Semi-transparent background
            help_bg = pygame.Surface((300, 200), pygame.SRCALPHA)
            help_bg.fill((0, 0, 0, 180))
            screen.blit(help_bg, (WIDTH//2 - 150, HEIGHT//2 - 100))
            
            for i, text in enumerate(help_text):
                text_surface = font_small.render(text, True, WHITE)
                screen.blit(text_surface, 
                           (WIDTH//2 - text_surface.get_width()//2, 
                            HEIGHT//2 - 80 + i * 25))
            
            help_timer += 1
            if help_timer > 300:  # Hide after 5 seconds (60fps * 5)
                show_help = False
        
        # Draw game over screen if needed
        if game_state == "game_over":
            draw_game_over_screen(screen, score, high_score)
        
        pygame.display.flip()
        clock.tick(snake.speed)
    
    controller.release()
    pygame.quit()

if __name__ == "__main__":
    main()