import pygame
from settings import MAP_WIDTH, MAP_HEIGHT

def get_level_3():
    platforms = [

        pygame.Rect(0, MAP_HEIGHT - 50, 300, 50),
        pygame.Rect(350, MAP_HEIGHT - 120, 200, 30),
        pygame.Rect(600, MAP_HEIGHT - 180, 200, 30),
        pygame.Rect(850, MAP_HEIGHT - 240, 200, 30),
        pygame.Rect(1100, MAP_HEIGHT - 300, 200, 30),
        
        pygame.Rect(1400, MAP_HEIGHT - 350, 120, 25),
        pygame.Rect(1570, MAP_HEIGHT - 400, 120, 25),
        pygame.Rect(1740, MAP_HEIGHT - 350, 120, 25),
        pygame.Rect(1910, MAP_HEIGHT - 450, 120, 25),
        pygame.Rect(2080, MAP_HEIGHT - 400, 120, 25),
        pygame.Rect(2250, MAP_HEIGHT - 500, 120, 25),
        pygame.Rect(2420, MAP_HEIGHT - 450, 120, 25),
        pygame.Rect(2590, MAP_HEIGHT - 550, 120, 25),
        
        pygame.Rect(2900, MAP_HEIGHT - 600, 150, 25),
        pygame.Rect(3100, MAP_HEIGHT - 650, 150, 25),
        pygame.Rect(3300, MAP_HEIGHT - 600, 150, 25),
        pygame.Rect(3500, MAP_HEIGHT - 700, 150, 25),
        pygame.Rect(3700, MAP_HEIGHT - 650, 150, 25),
        pygame.Rect(3900, MAP_HEIGHT - 750, 150, 25),
        
        pygame.Rect(4200, MAP_HEIGHT - 800, 250, 30),
        pygame.Rect(4500, MAP_HEIGHT - 800, 250, 30),
        pygame.Rect(4800, MAP_HEIGHT - 850, 250, 30),
        pygame.Rect(5100, MAP_HEIGHT - 850, 250, 30),
        
        pygame.Rect(5500, MAP_HEIGHT - 150, 800, 50),
        
        pygame.Rect(1450, MAP_HEIGHT - 500, 80, 20),
        pygame.Rect(1950, MAP_HEIGHT - 550, 80, 20),
        pygame.Rect(2450, MAP_HEIGHT - 650, 80, 20),
        pygame.Rect(2950, MAP_HEIGHT - 700, 80, 20),
        pygame.Rect(3450, MAP_HEIGHT - 800, 80, 20),
        pygame.Rect(3950, MAP_HEIGHT - 850, 80, 20),
        pygame.Rect(0, MAP_HEIGHT - 30, MAP_WIDTH, 30),
    ]
    
    enemies = [
        (400, MAP_HEIGHT - 150), (650, MAP_HEIGHT - 210), (900, MAP_HEIGHT - 270),
        (1150, MAP_HEIGHT - 330), (1450, MAP_HEIGHT - 380), (1620, MAP_HEIGHT - 430),
        
        (1790, MAP_HEIGHT - 380), (1960, MAP_HEIGHT - 480), (2130, MAP_HEIGHT - 430),
        (2300, MAP_HEIGHT - 530), (2470, MAP_HEIGHT - 480), (2640, MAP_HEIGHT - 580),
        
        (2950, MAP_HEIGHT - 630), (3150, MAP_HEIGHT - 680), (3350, MAP_HEIGHT - 630),
        (3550, MAP_HEIGHT - 730), (3750, MAP_HEIGHT - 680), (3950, MAP_HEIGHT - 780),
        
        (4250, MAP_HEIGHT - 830), (4550, MAP_HEIGHT - 830), (4850, MAP_HEIGHT - 880),
        (5150, MAP_HEIGHT - 880),
        
        (1490, MAP_HEIGHT - 530), (1990, MAP_HEIGHT - 580), (2990, MAP_HEIGHT - 730),
        (3490, MAP_HEIGHT - 830), (3990, MAP_HEIGHT - 880),
    ]
    
    items = [
        (450, MAP_HEIGHT - 150), (700, MAP_HEIGHT - 210), (950, MAP_HEIGHT - 270),
        (1200, MAP_HEIGHT - 330), (1500, MAP_HEIGHT - 380), (1670, MAP_HEIGHT - 430),
        (1840, MAP_HEIGHT - 380), (2010, MAP_HEIGHT - 480), (2180, MAP_HEIGHT - 430),
        (2350, MAP_HEIGHT - 530), (2520, MAP_HEIGHT - 480), (2690, MAP_HEIGHT - 580),
        
        (3000, MAP_HEIGHT - 630), (3200, MAP_HEIGHT - 680), (3400, MAP_HEIGHT - 630),
        (3600, MAP_HEIGHT - 730), (3800, MAP_HEIGHT - 680), (4000, MAP_HEIGHT - 780),
        
        (4300, MAP_HEIGHT - 830), (4600, MAP_HEIGHT - 830), (4900, MAP_HEIGHT - 880),
        (5200, MAP_HEIGHT - 880),
        
        (1550, MAP_HEIGHT - 530), (2050, MAP_HEIGHT - 580), (2550, MAP_HEIGHT - 680),
        (3050, MAP_HEIGHT - 730), (3550, MAP_HEIGHT - 830), (4050, MAP_HEIGHT - 880),
    ]
    
    boss_pos = (5900, MAP_HEIGHT - 200)
    
    return {
        'platforms': platforms,
        'enemies': enemies,
        'items': items,
        'exit': None,
        'boss': boss_pos
    }