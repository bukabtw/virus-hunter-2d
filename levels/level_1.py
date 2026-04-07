import pygame
from settings import MAP_WIDTH, MAP_HEIGHT

def get_level_1():
    platforms = [
        pygame.Rect(0, MAP_HEIGHT - 50, MAP_WIDTH, 50),
        
        pygame.Rect(500, MAP_HEIGHT - 150, 300, 30),
        pygame.Rect(900, MAP_HEIGHT - 150, 300, 30),
        pygame.Rect(1300, MAP_HEIGHT - 200, 300, 30),
        pygame.Rect(1700, MAP_HEIGHT - 200, 300, 30),
        
        pygame.Rect(2200, MAP_HEIGHT - 280, 300, 30),
        pygame.Rect(2600, MAP_HEIGHT - 280, 300, 30),
        pygame.Rect(3000, MAP_HEIGHT - 350, 300, 30),
        pygame.Rect(3400, MAP_HEIGHT - 350, 300, 30),
        
        pygame.Rect(3900, MAP_HEIGHT - 450, 300, 30),
        pygame.Rect(4300, MAP_HEIGHT - 450, 300, 30),
        pygame.Rect(4700, MAP_HEIGHT - 520, 300, 30),
        pygame.Rect(5100, MAP_HEIGHT - 520, 300, 30),
        
        pygame.Rect(5600, MAP_HEIGHT - 600, 300, 30),
        pygame.Rect(6000, MAP_HEIGHT - 600, 300, 30),
        pygame.Rect(6400, MAP_HEIGHT - 680, 300, 30),
        pygame.Rect(6800, MAP_HEIGHT - 680, 300, 30),
        
        pygame.Rect(1050, MAP_HEIGHT - 300, 150, 30),
        pygame.Rect(1450, MAP_HEIGHT - 350, 150, 30),
        pygame.Rect(1950, MAP_HEIGHT - 400, 150, 30),
        pygame.Rect(2350, MAP_HEIGHT - 450, 150, 30),
        pygame.Rect(2750, MAP_HEIGHT - 500, 150, 30),
        pygame.Rect(3150, MAP_HEIGHT - 550, 150, 30),
        pygame.Rect(3550, MAP_HEIGHT - 600, 150, 30),
        pygame.Rect(3950, MAP_HEIGHT - 650, 150, 30),
        pygame.Rect(4350, MAP_HEIGHT - 700, 150, 30),
        pygame.Rect(4750, MAP_HEIGHT - 750, 150, 30),
    ]
    
    enemies = [
        (600, MAP_HEIGHT - 180), (1000, MAP_HEIGHT - 180), (1400, MAP_HEIGHT - 230),
        (1800, MAP_HEIGHT - 230), (2300, MAP_HEIGHT - 310), (2700, MAP_HEIGHT - 310),
        (3100, MAP_HEIGHT - 380), (3500, MAP_HEIGHT - 380), (4000, MAP_HEIGHT - 480),
        (4400, MAP_HEIGHT - 480), (4800, MAP_HEIGHT - 550), (5200, MAP_HEIGHT - 550),
        (5700, MAP_HEIGHT - 630), (6100, MAP_HEIGHT - 630), (6500, MAP_HEIGHT - 710),
        (6900, MAP_HEIGHT - 710),
        (1100, MAP_HEIGHT - 330), (1500, MAP_HEIGHT - 380), (2000, MAP_HEIGHT - 430),
        (2400, MAP_HEIGHT - 480), (2800, MAP_HEIGHT - 530), (3200, MAP_HEIGHT - 580),
        (3600, MAP_HEIGHT - 630), (4000, MAP_HEIGHT - 680), (4400, MAP_HEIGHT - 730),
        (4800, MAP_HEIGHT - 780),
    ]
    
    items = [
        (550, MAP_HEIGHT - 180), (950, MAP_HEIGHT - 180), (1350, MAP_HEIGHT - 230),
        (1750, MAP_HEIGHT - 230), (2250, MAP_HEIGHT - 310), (2650, MAP_HEIGHT - 310),
        (3050, MAP_HEIGHT - 380), (3450, MAP_HEIGHT - 380), (3950, MAP_HEIGHT - 480),
        (4350, MAP_HEIGHT - 480), (4750, MAP_HEIGHT - 550), (5150, MAP_HEIGHT - 550),
        (5650, MAP_HEIGHT - 630), (6050, MAP_HEIGHT - 630), (6450, MAP_HEIGHT - 710),
        (6850, MAP_HEIGHT - 710),
        (1150, MAP_HEIGHT - 330), (2050, MAP_HEIGHT - 430), (2950, MAP_HEIGHT - 530),
        (3850, MAP_HEIGHT - 630), (4650, MAP_HEIGHT - 730), (5450, MAP_HEIGHT - 630),
        (6250, MAP_HEIGHT - 710),
    ]
    
    exit_pos = (7100, MAP_HEIGHT - 730)
    
    return {
        'platforms': platforms,
        'enemies': enemies,
        'items': items,
        'exit': exit_pos,
        'boss': None
    }