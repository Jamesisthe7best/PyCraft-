import pygame
import sys
import json
import os
import tkinter as tk
from tkinter import filedialog

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
PINK = (255, 105, 180)
PURPLE = (128, 0, 128)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
PLAYER_COLOR = (0, 0, 255)
BACKGROUND_COLOR = WHITE  # White background

# Block types
block_colors = {
    1: BROWN,
    2: YELLOW,
    3: GREEN,
    4: BLACK,
    5: GREY,
    6: PINK,
    7: PURPLE,
    8: DARK_GREEN,
    9: ORANGE,
    10: RED,
}

selected_block = 1  # Default block type

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pycraft Test 0.0.5")

# Player
player = pygame.Rect(200, 300, TILE_SIZE, TILE_SIZE)
velocity = 5

# Camera offset
camera_x, camera_y = 0, 0

grid = {}
menu_active = False

# Font
font = pygame.font.Font(None, 36)

# Button rectangles
save_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 40, 160, 30)
load_button = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 30)

def open_file_explorer_save():
    # Open the file explorer to choose a file path for saving
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    return file_path

def open_file_explorer_load():
    # Open the file explorer to choose a file path for loading
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    return file_path

def save_world():
    world_data = {"grid": list(grid.items())}
    file_path = open_file_explorer_save()  # Let user choose where to save
    if file_path:
        with open(file_path, "w") as f:
            json.dump(world_data, f)
        print(f"World saved to {file_path}")

def load_world():
    global grid
    file_path = open_file_explorer_load()  # Let user choose a file to load
    if file_path:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                grid = {tuple(k): v for k, v in data["grid"]}
            print(f"World loaded from {file_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            print("No valid saved world found.")

def draw_grid():
    for (x, y), block_type in grid.items():
        pygame.draw.rect(screen, block_colors[block_type], (x - camera_x, y - camera_y, TILE_SIZE, TILE_SIZE))
        pygame.draw.rect(screen, WHITE, (x - camera_x, y - camera_y, TILE_SIZE, TILE_SIZE), 1)

def draw_selected_block_ui():
    pygame.draw.rect(screen, block_colors[selected_block], (SCREEN_WIDTH - 60, 20, 40, 40))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 60, 20, 40, 40), 2)  # Border

def check_collision(rect):
    for (x, y) in grid.keys():
        if rect.colliderect(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)):
            return True
    return False

def draw_menu():
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100))
    pygame.draw.rect(screen, BLACK, save_button, 2)
    pygame.draw.rect(screen, BLACK, load_button, 2)
    save_text = font.render("Save World", True, BLACK)
    load_text = font.render("Load World", True, BLACK)
    screen.blit(save_text, (save_button.x + 10, save_button.y + 5))
    screen.blit(load_text, (load_button.x + 10, load_button.y + 5))

running = True
while running:
    screen.fill(BACKGROUND_COLOR)  # Solid white background
    
    if menu_active:
        draw_menu()
    else:
        draw_grid()
        draw_selected_block_ui()
        pygame.draw.rect(screen, PLAYER_COLOR, (player.x - camera_x, player.y - camera_y, TILE_SIZE, TILE_SIZE))
    
    pygame.display.flip()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu_active = not menu_active
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                selected_block = int(event.unicode) if event.unicode.isdigit() else selected_block  # Change selected block
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if menu_active:
                if save_button.collidepoint(mouse_x, mouse_y):
                    save_world()
                elif load_button.collidepoint(mouse_x, mouse_y):
                    load_world()
            else:
                x, y = pygame.mouse.get_pos()
                x = ((x + camera_x) // TILE_SIZE) * TILE_SIZE
                y = ((y + camera_y) // TILE_SIZE) * TILE_SIZE
                
                if event.button == 1:  # Left click (break block)
                    if (x, y) in grid:
                        del grid[(x, y)]
                elif event.button == 3:  # Right click (place block)
                    if (x, y) not in grid and not player.colliderect(pygame.Rect(x - camera_x, y - camera_y, TILE_SIZE, TILE_SIZE)):
                        grid[(x, y)] = selected_block
    
    if not menu_active:
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
        
        # Update camera to follow player
        camera_x = player.x - SCREEN_WIDTH // 2
        camera_y = player.y - SCREEN_HEIGHT // 2
    
    pygame.time.delay(30)

pygame.quit()
sys.exit()

