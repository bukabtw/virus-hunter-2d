import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT

def get_level_1():
    platforms = [
        pygame.Rect(0, MAP_HEIGHT - 50, MAP_WIDTH, 50),
        pygame.Rect(800, MAP_HEIGHT - 150, 300, 30),
        pygame.Rect(1600, MAP_HEIGHT - 250, 300, 30),
        pygame.Rect(2200, MAP_HEIGHT - 350, 300, 30),
        pygame.Rect(2800, MAP_HEIGHT - 450, 300, 30),
        pygame.Rect(3400, MAP_HEIGHT - 550, 300, 30),
        pygame.Rect(4000, MAP_HEIGHT - 650, 300, 30),
    ]
    items = [
        (850, MAP_HEIGHT - 180),
        (1650, MAP_HEIGHT - 280),
        (2250, MAP_HEIGHT - 380),
        (2850, MAP_HEIGHT - 480),
        (3450, MAP_HEIGHT - 580),
    ]
    enemies = [
        (1000, MAP_HEIGHT - 180),
        (1800, MAP_HEIGHT - 280),
        (2400, MAP_HEIGHT - 380),
        (3000, MAP_HEIGHT - 480),
        (3600, MAP_HEIGHT - 580),
    ]
    exit_pos = (4200, MAP_HEIGHT - 700)
    return platforms, items, enemies, exit_pos