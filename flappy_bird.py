import pygame
import random
import sys
import os
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 1280  # 16:9 ratio
WINDOW_HEIGHT = 720
FPS = 60
PIPE_GAP = 200  # Adjusted for larger screen
PIPE_FREQUENCY = 1800  # Slightly increased for larger screen
PIPE_SPEED = 6
GRAVITY = 0.6
FLAP_POWER = -10
SCORE_INCREASE_THRESHOLD = 10
ANIMATION_SPEED = 0.15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

# Set up the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Extreme Flappy Bird')

# Create and set game icon
icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
# Draw a simple bird shape for the icon
pygame.draw.ellipse(icon_surface, (255, 200, 50), (8, 8, 20, 16))  # Body
pygame.draw.ellipse(icon_surface, (220, 180, 50), (20, 12, 8, 8))  # Head
pygame.draw.ellipse(icon_surface, WHITE, (22, 13, 4, 4))  # Eye
pygame.display.set_icon(icon_surface)

clock = pygame.time.Clock()

class Cloud:
    def __init__(self, x=None):
        self.width = random.randint(60, 120)
        self.height = random.randint(30, 50)
        self.x = x if x is not None else random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(50, WINDOW_HEIGHT // 3)
        self.speed = random.uniform(0.5, 1.5)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_cloud()

    def draw_cloud(self):
        for i in range(3):  # Draw multiple circles for fluffy appearance
            radius = self.height // 2
            center_x = self.width // 4 + (i * self.width // 4)
            center_y = self.height // 2
            pygame.draw.circle(self.surface, (255, 255, 255, 200), 
                             (center_x, center_y), radius)

    def update(self, game_speed):
        self.x -= self.speed * (game_speed / 5)
        if self.x + self.width < 0:
            self.x = WINDOW_WIDTH
            self.y = random.randint(50, WINDOW_HEIGHT // 3)

    def draw(self, surface):
        surface.blit(self.surface, (int(self.x), int(self.y)))

def create_building(width, height):
    building = pygame.Surface((width, height), pygame.SRCALPHA)
    color = (random.randint(50, 100), random.randint(50, 100), random.randint(70, 120))
    pygame.draw.rect(building, color, (0, 0, width, height))
    
    # Add windows
    window_color = (255, 255, 190)
    for y in range(10, height-10, 30):
        for x in range(5, width-5, 20):
            if random.random() > 0.3:  # 70% chance of window
                pygame.draw.rect(building, window_color, (x, y, 10, 15))
    return building

def create_background():
    # Create sky gradient
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    for y in range(WINDOW_HEIGHT):
        color = (
            max(0, min(255, 135 - y//8)),
            max(0, min(255, 206 - y//8)),
            max(0, min(255, 235 - y//8))
        )
        pygame.draw.line(background, color, (0, y), (WINDOW_WIDTH, y))
    
    # Add stars in the upper part (visible during night)
    for _ in range(40):  # More stars for larger screen
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT//3)
        pygame.draw.circle(background, (255, 255, 255), (x, y), 1)
    
    # Create buildings of different heights
    buildings = []
    x = 0
    while x < WINDOW_WIDTH * 2:
        width = random.randint(60, 100)  # Larger buildings
        height = random.randint(150, 400)  # Taller buildings
        building = create_building(width, height)
        buildings.append((x, WINDOW_HEIGHT - height, building))
        x += width - 5
    
    # Create building layer
    building_layer = pygame.Surface((WINDOW_WIDTH * 2, WINDOW_HEIGHT), pygame.SRCALPHA)
    for x, y, building in buildings:
        building_layer.blit(building, (x, y))
    
    return background.convert(), building_layer.convert_alpha()

def create_pipe_sprite():
    pipe = pygame.Surface((80, 800), pygame.SRCALPHA)  # Larger pipe for bigger screen
    
    # Main pipe body gradient
    for y in range(800):
        color = (
            max(0, min(255, 100 - y//30)),
            max(0, min(255, 200 - y//30)),
            max(0, min(255, 50 - y//30))
        )
        pygame.draw.line(pipe, color, (0, y), (80, y))
    
    # Pipe edges
    pygame.draw.rect(pipe, (60, 160, 30), (0, 0, 2, 800))
    pygame.draw.rect(pipe, (60, 160, 30), (78, 0, 2, 800))
    
    # Pipe cap
    cap_height = 60
    pygame.draw.rect(pipe, (120, 220, 70), (0, 0, 80, cap_height))
    pygame.draw.rect(pipe, (90, 190, 50), (0, cap_height-5, 80, 5))
    
    return pipe.convert_alpha()

def create_bird_sprites():
    colors = [(255, 200, 50), (255, 180, 50), (255, 220, 50)]
    sprites = []
    
    for i in range(3):
        bird = pygame.Surface((45, 45), pygame.SRCALPHA)  # Larger bird
        
        # Bird body
        pygame.draw.ellipse(bird, colors[i], (0, 7, 38, 30))
        
        # Wing (different positions for animation)
        wing_y = 15 + (i * 7 - 7)
        pygame.draw.polygon(bird, (220, 180, 50), 
                          [(7, wing_y), (30, wing_y), (18, wing_y + 12)])
        
        # Eye
        pygame.draw.circle(bird, WHITE, (30, 18), 6)
        pygame.draw.circle(bird, BLACK, (31, 18), 3)
        
        sprites.append(bird.convert_alpha())
    
    return sprites

# Create and cache all game assets
BACKGROUND, BUILDINGS = create_background()
PIPE_IMG = create_pipe_sprite()
BIRD_FRAMES = create_bird_sprites()

class Bird:
    def __init__(self):
        self.x = WINDOW_WIDTH // 4
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.frame_index = 0
        self.animation_time = 0
        self.angle = 0
        self.size = 45  # Larger bird size
        self.rect = pygame.Rect(self.x + 7, self.y + 7, self.size - 14, self.size - 14)

    def flap(self):
        self.velocity = FLAP_POWER
        self.angle = 20

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y + 7
        
        self.angle = max(-90, min(self.angle - 2, 20))
        self.animation_time += ANIMATION_SPEED
        self.frame_index = int(self.animation_time) % len(BIRD_FRAMES)
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0
            self.rect.y = 7
        elif self.y > WINDOW_HEIGHT - self.size:
            self.y = WINDOW_HEIGHT - self.size
            self.velocity = 0
            self.rect.y = WINDOW_HEIGHT - self.size + 7

    def draw(self):
        rotated_bird = pygame.transform.rotate(BIRD_FRAMES[self.frame_index], self.angle)
        bird_rect = rotated_bird.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        screen.blit(rotated_bird, bird_rect.topleft)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(200, WINDOW_HEIGHT - 200)
        self.width = 80  # Larger pipe width
        self.passed = False
        self.rect_top = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP//2)
        self.rect_bottom = pygame.Rect(self.x, self.gap_y + PIPE_GAP//2, self.width, WINDOW_HEIGHT)

    def update(self, speed):
        self.x -= speed
        self.rect_top.x = self.x
        self.rect_bottom.x = self.x

    def draw(self):
        top_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        screen.blit(top_pipe, (self.x, self.gap_y - PIPE_GAP//2 - PIPE_IMG.get_height()))
        screen.blit(PIPE_IMG, (self.x, self.gap_y + PIPE_GAP//2))

    def collides_with(self, bird):
        return bird.rect.colliderect(self.rect_top) or bird.rect.colliderect(self.rect_bottom)

class Game:
    def __init__(self):
        self.reset()
        # Create initial clouds
        self.clouds = [Cloud() for _ in range(6)]
        
    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_speed = PIPE_SPEED
        self.last_pipe = pygame.time.get_ticks()
        self.game_active = True
        self.bg_scroll = 0
        self.building_scroll = 0
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update(self.game_speed)
        
        if self.game_active:
            self.bird.update()
            
            if current_time - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(Pipe(WINDOW_WIDTH))
                self.last_pipe = current_time
            
            for pipe in self.pipes[:]:
                pipe.update(self.game_speed)
                if pipe.collides_with(self.bird):
                    self.game_active = False
                if not pipe.passed and pipe.x < self.bird.x:
                    self.score += 1
                    pipe.passed = True
                    if self.score % SCORE_INCREASE_THRESHOLD == 0:
                        self.game_speed += 0.5
                if pipe.x < -pipe.width:
                    self.pipes.remove(pipe)
            
            if self.bird.y <= 0 or self.bird.y >= WINDOW_HEIGHT - self.bird.size:
                self.game_active = False
                
        # Update scrolling
        self.bg_scroll = (self.bg_scroll - self.game_speed * 0.2) % WINDOW_WIDTH
        self.building_scroll = (self.building_scroll - self.game_speed * 0.5) % WINDOW_WIDTH
        
    def draw(self):
        # Draw background with parallax
        screen.blit(BACKGROUND, (0, 0))
        
        # Draw clouds
        for cloud in self.clouds:
            cloud.draw(screen)
        
        # Draw buildings with parallax
        screen.blit(BUILDINGS, (self.building_scroll, 0))
        screen.blit(BUILDINGS, (self.building_scroll + WINDOW_WIDTH, 0))
        
        # Draw game elements
        for pipe in self.pipes:
            pipe.draw()
        self.bird.draw()
        
        # Draw score
        font = pygame.font.Font(None, 72)  # Larger font for bigger screen
        if not self.game_active:
            # Game over score
            shadow_text = font.render(f'Score: {self.score}', True, BLACK)
            text = font.render(f'Score: {self.score}', True, WHITE)
            screen.blit(shadow_text, (WINDOW_WIDTH//2 - text.get_width()//2 + 2, WINDOW_HEIGHT//3 + 2))
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//3))
            
            # Game over message
            font = pygame.font.Font(None, 48)
            shadow_text = font.render('Game Over! Press SPACE to restart', True, BLACK)
            text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            screen.blit(shadow_text, (WINDOW_WIDTH//2 - text.get_width()//2 + 2, WINDOW_HEIGHT//2 + 2))
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
        else:
            # In-game score
            shadow_text = font.render(str(self.score), True, BLACK)
            text = font.render(str(self.score), True, WHITE)
            screen.blit(shadow_text, (WINDOW_WIDTH//2 - text.get_width()//2 + 2, 50 + 2))
            screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, 50))

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and game.game_active:
                    game.bird.flap()
                if event.key == K_SPACE and not game.game_active:
                    game.reset()
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main() 