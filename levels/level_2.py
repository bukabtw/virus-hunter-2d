import pygame
from settings import MAP_WIDTH, MAP_HEIGHT

def get_level_2():
    platforms = [
        pygame.Rect(0, MAP_HEIGHT - 50, 400, 50),
        pygame.Rect(450, MAP_HEIGHT - 120, 250, 30),
        pygame.Rect(750, MAP_HEIGHT - 180, 250, 30),
        pygame.Rect(1050, MAP_HEIGHT - 240, 250, 30),
        pygame.Rect(1350, MAP_HEIGHT - 300, 250, 30),
        
        pygame.Rect(1700, MAP_HEIGHT - 350, 200, 30),
        pygame.Rect(1950, MAP_HEIGHT - 400, 200, 30),
        pygame.Rect(2200, MAP_HEIGHT - 350, 200, 30),
        pygame.Rect(2450, MAP_HEIGHT - 450, 200, 30),
        pygame.Rect(2700, MAP_HEIGHT - 400, 200, 30),
        pygame.Rect(2950, MAP_HEIGHT - 500, 200, 30),
        
        pygame.Rect(3300, MAP_HEIGHT - 550, 150, 30),
        pygame.Rect(3500, MAP_HEIGHT - 600, 150, 30),
        pygame.Rect(3700, MAP_HEIGHT - 550, 150, 30),
        pygame.Rect(3900, MAP_HEIGHT - 650, 150, 30),
        pygame.Rect(4100, MAP_HEIGHT - 600, 150, 30),
        pygame.Rect(4300, MAP_HEIGHT - 700, 150, 30),
        
        pygame.Rect(4600, MAP_HEIGHT - 750, 300, 30),
        pygame.Rect(4950, MAP_HEIGHT - 750, 300, 30),
        pygame.Rect(5300, MAP_HEIGHT - 800, 300, 30),
        
        pygame.Rect(1800, MAP_HEIGHT - 500, 100, 20),
        pygame.Rect(2500, MAP_HEIGHT - 550, 100, 20),
        pygame.Rect(3200, MAP_HEIGHT - 650, 100, 20),
        pygame.Rect(3800, MAP_HEIGHT - 750, 100, 20),
        pygame.Rect(4400, MAP_HEIGHT - 800, 100, 20),
        pygame.Rect(5000, MAP_HEIGHT - 850, 100, 20),
    ]
    
    enemies = [
        (500, MAP_HEIGHT - 150), (800, MAP_HEIGHT - 210), (1100, MAP_HEIGHT - 270),
        (1400, MAP_HEIGHT - 330), (1750, MAP_HEIGHT - 380), (2000, MAP_HEIGHT - 430),
        
        (2250, MAP_HEIGHT - 380), (2500, MAP_HEIGHT - 480), (2750, MAP_HEIGHT - 430),
        (3000, MAP_HEIGHT - 530), (3350, MAP_HEIGHT - 580), (3550, MAP_HEIGHT - 630),
        
        (3750, MAP_HEIGHT - 580), (3950, MAP_HEIGHT - 680), (4150, MAP_HEIGHT - 630),
        (4350, MAP_HEIGHT - 730), (4650, MAP_HEIGHT - 780), (5000, MAP_HEIGHT - 780),
        
        (1850, MAP_HEIGHT - 530), (2550, MAP_HEIGHT - 580), (3850, MAP_HEIGHT - 780),
        (4450, MAP_HEIGHT - 830), (5050, MAP_HEIGHT - 880),
    ]
    
    items = [
        (550, MAP_HEIGHT - 150), (850, MAP_HEIGHT - 210), (1150, MAP_HEIGHT - 270),
        (1450, MAP_HEIGHT - 330), (1800, MAP_HEIGHT - 380), (2050, MAP_HEIGHT - 430),
        (2300, MAP_HEIGHT - 380), (2550, MAP_HEIGHT - 480), (2800, MAP_HEIGHT - 430),
        (3050, MAP_HEIGHT - 530), (3400, MAP_HEIGHT - 580), (3600, MAP_HEIGHT - 630),
        (3800, MAP_HEIGHT - 580), (4000, MAP_HEIGHT - 680), (4200, MAP_HEIGHT - 630),
        (4400, MAP_HEIGHT - 730), (4700, MAP_HEIGHT - 780), (5050, MAP_HEIGHT - 780),
        (5400, MAP_HEIGHT - 830),

        (1900, MAP_HEIGHT - 530), (2600, MAP_HEIGHT - 580), (3300, MAP_HEIGHT - 680),
        (3900, MAP_HEIGHT - 780), (4500, MAP_HEIGHT - 830), (5100, MAP_HEIGHT - 880),
    ]
    
    exit_pos = (5600, MAP_HEIGHT - 830)
    
    return {
        'platforms': platforms,
        'enemies': enemies,
        'items': items,
        'exit': exit_pos,
        'boss': None
    }