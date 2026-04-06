import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT

def get_level_2():
    platforms = [
        pygame.Rect(0, 650, 300, 50),
        pygame.Rect(350, 600, 200, 50),
        pygame.Rect(600, 550, 300, 50),
        pygame.Rect(950, 500, 200, 50),
        pygame.Rect(1200, 450, 300, 50),
        pygame.Rect(1550, 400, 200, 50),
        pygame.Rect(1800, 350, 300, 50),
        pygame.Rect(2100, 300, 100, 50),
        pygame.Rect(100, 400, 150, 30),
        pygame.Rect(400, 300, 150, 30),
        pygame.Rect(700, 200, 150, 30),
        pygame.Rect(1000, 100, 150, 30),
        pygame.Rect(1300, 200, 150, 30),
        pygame.Rect(1600, 300, 150, 30),
        pygame.Rect(1900, 400, 150, 30),
    ]
    
    enemies = [
        (200, 600),
        (500, 550),
        (750, 500),
        (1100, 450),
        (1400, 400),
        (1700, 350),
        (2000, 250),
    ]
    
    items = [
        (150, 350),
        (450, 250),
        (750, 150),
        (1050, 50),
        (1350, 150),
        (1650, 250),
        (1950, 350),
        (2200, 250),
    ]
    
    exit_rect = (2250, 250)
    
    boss = None
    
    return {
        'platforms': platforms,
        'enemies': enemies,
        'items': items,
        'exit': exit_rect,
        'boss': boss
    }