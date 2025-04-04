import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 40
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
PLAYER_COLOR = (0, 0, 255)
BACKGROUND_COLOR = WHITE  # White background

# Block types
block_colors = {
    1: BROWN,
    2: YELLOW,
    3: GREEN,
    4: BLACK,
    5: GREY,
}

selected_block = 1  # Default block type

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyCraft Test 0.0.3")

# Player
player = pygame.Rect(200, 300, TILE_SIZE, TILE_SIZE)
velocity = 5

grid = {}

def draw_grid():
    for (x, y), color in grid.items():
        pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, WHITE, (x, y, TILE_SIZE, TILE_SIZE), 1)

def draw_selected_block_ui():
    pygame.draw.rect(screen, block_colors[selected_block], (SCREEN_WIDTH - 60, 20, 40, 40))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 60, 20, 40, 40), 2)  # Border

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
                if (x, y) not in grid and not player.colliderect(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)):
                    grid[(x, y)] = block_colors[selected_block]
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                selected_block = int(event.unicode)  # Change selected block
    
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
    draw_selected_block_ui()
    pygame.draw.rect(screen, PLAYER_COLOR, player)
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
