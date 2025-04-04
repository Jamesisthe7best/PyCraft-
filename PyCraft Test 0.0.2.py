import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 40
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
PLAYER_COLOR = (0, 0, 255)
BACKGROUND_COLOR = WHITE  # White background

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyCraft Test 0.0.2")

# Player
player = pygame.Rect(200, 300, TILE_SIZE, TILE_SIZE)
velocity = 5

grid = {}

def draw_grid():
    for (x, y), color in grid.items():
        pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 1)

def check_collision(rect):
    for (x, y) in grid.keys():
        if rect.colliderect(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)):
            return True
    return False

running = True
while running:
    screen.fill(BACKGROUND_COLOR)  # Solid white background
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x = (x // TILE_SIZE) * TILE_SIZE
            y = (y // TILE_SIZE) * TILE_SIZE
            
            if event.button == 1:  # Left click (break block)
                if (x, y) in grid:
                    del grid[(x, y)]
            elif event.button == 3:  # Right click (place block)
                if (x, y) not in grid:
                    grid[(x, y)] = BROWN
    
    # Player movement
    new_x, new_y = player.x, player.y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        new_x -= velocity
    if keys[pygame.K_d]:
        new_x += velocity
    if keys[pygame.K_w]:
        new_y -= velocity
    if keys[pygame.K_s]:
        new_y += velocity
    
    new_rect = pygame.Rect(new_x, new_y, TILE_SIZE, TILE_SIZE)
    if not check_collision(new_rect):
        player.x, player.y = new_x, new_y
    
    draw_grid()
    pygame.draw.rect(screen, PLAYER_COLOR, player)
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
