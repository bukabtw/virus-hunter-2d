import pygame
from settings import MAP_WIDTH, MAP_HEIGHT, PLATFORM_SIZES

def get_level():
    TILE_W, TILE_H = PLATFORM_SIZES['ram']
    
    platforms = [
        pygame.Rect(0, MAP_HEIGHT - TILE_H*2, TILE_W*10, TILE_H*2),
        
        pygame.Rect(TILE_W*11, MAP_HEIGHT - TILE_H*3, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*15, MAP_HEIGHT - TILE_H*4, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*19, MAP_HEIGHT - TILE_H*3, TILE_W*4, TILE_H),
        
        pygame.Rect(TILE_W*24, MAP_HEIGHT - TILE_H*4, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*28, MAP_HEIGHT - TILE_H*5, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*32, MAP_HEIGHT - TILE_H*6, TILE_W*4, TILE_H),
        
        pygame.Rect(TILE_W*37, MAP_HEIGHT - TILE_H*6, TILE_W*6, TILE_H*2),
        
        pygame.Rect(TILE_W*44, MAP_HEIGHT - TILE_H*7, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*48, MAP_HEIGHT - TILE_H*8, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*44, MAP_HEIGHT - TILE_H*9, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*48, MAP_HEIGHT - TILE_H*10, TILE_W*4, TILE_H),
        
        pygame.Rect(TILE_W*53, MAP_HEIGHT - TILE_H*10, TILE_W*8, TILE_H*2),
        pygame.Rect(TILE_W*55, MAP_HEIGHT - TILE_H*12, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*59, MAP_HEIGHT - TILE_H*13, TILE_W*2, TILE_H),
        
        pygame.Rect(TILE_W*63, MAP_HEIGHT - TILE_H*12, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*67, MAP_HEIGHT - TILE_H*11, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*71, MAP_HEIGHT - TILE_H*10, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*75, MAP_HEIGHT - TILE_H*9, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*80, MAP_HEIGHT - TILE_H*8, TILE_W*5, TILE_H*2),
        
        pygame.Rect(TILE_W*86, MAP_HEIGHT - TILE_H*9, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*90, MAP_HEIGHT - TILE_H*10, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*94, MAP_HEIGHT - TILE_H*11, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*99, MAP_HEIGHT - TILE_H*10, TILE_W*3, TILE_H),
        pygame.Rect(TILE_W*103, MAP_HEIGHT - TILE_H*9, TILE_W*5, TILE_H*2),
        
        pygame.Rect(TILE_W*26, MAP_HEIGHT - TILE_H*7, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*50, MAP_HEIGHT - TILE_H*12, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*92, MAP_HEIGHT - TILE_H*13, TILE_W*2, TILE_H),
    ]
    
    enemies = [
        (TILE_W*25 + TILE_W, MAP_HEIGHT - TILE_H*4 - 30),
        (TILE_W*33 + TILE_W, MAP_HEIGHT - TILE_H*6 - 30),
        
        (TILE_W*45 + TILE_W, MAP_HEIGHT - TILE_H*7 - 30),
        (TILE_W*49 + TILE_W, MAP_HEIGHT - TILE_H*10 - 30),
        
        (TILE_W*54 + TILE_W, MAP_HEIGHT - TILE_H*10 - 30),
        (TILE_W*57 + TILE_W*2, MAP_HEIGHT - TILE_H*10 - 30),
        (TILE_W*60 + TILE_W, MAP_HEIGHT - TILE_H*13 - 30),
        
        (TILE_W*68 + TILE_W, MAP_HEIGHT - TILE_H*11 - 30),
        (TILE_W*76 + TILE_W, MAP_HEIGHT - TILE_H*9 - 30),
        
        (TILE_W*95 + TILE_W, MAP_HEIGHT - TILE_H*11 - 30),
        (TILE_W*100 + TILE_W, MAP_HEIGHT - TILE_H*10 - 30),
    ]
    
    items = [
        (TILE_W*12 + TILE_W, MAP_HEIGHT - TILE_H*3 - 40),
        (TILE_W*16 + TILE_W, MAP_HEIGHT - TILE_H*4 - 40),
        (TILE_W*20 + TILE_W*2, MAP_HEIGHT - TILE_H*3 - 40),
        
        (TILE_W*25 + TILE_W, MAP_HEIGHT - TILE_H*4 - 40),
        (TILE_W*29 + TILE_W, MAP_HEIGHT - TILE_H*5 - 40),
        (TILE_W*33 + TILE_W*2, MAP_HEIGHT - TILE_H*6 - 40),

        (TILE_W*38 + TILE_W, MAP_HEIGHT - TILE_H*6 - 40),
        (TILE_W*40 + TILE_W*3, MAP_HEIGHT - TILE_H*6 - 40),
        
        (TILE_W*45 + TILE_W, MAP_HEIGHT - TILE_H*7 - 40),
        (TILE_W*49 + TILE_W, MAP_HEIGHT - TILE_H*8 - 40),
        (TILE_W*45 + TILE_W, MAP_HEIGHT - TILE_H*9 - 40),
        (TILE_W*49 + TILE_W*2, MAP_HEIGHT - TILE_H*10 - 40),
        
        (TILE_W*58 + TILE_W, MAP_HEIGHT - TILE_H*10 - 40),
        (TILE_W*58 + TILE_W, MAP_HEIGHT - TILE_H*12 - 40),
        (TILE_W*60 + TILE_W, MAP_HEIGHT - TILE_H*13 - 40),
        
        (TILE_W*64 + TILE_W, MAP_HEIGHT - TILE_H*12 - 40),
        (TILE_W*68 + TILE_W, MAP_HEIGHT - TILE_H*11 - 40),
        (TILE_W*72 + TILE_W, MAP_HEIGHT - TILE_H*10 - 40),
        (TILE_W*76 + TILE_W*2, MAP_HEIGHT - TILE_H*9 - 40),
        
        (TILE_W*87 + TILE_W, MAP_HEIGHT - TILE_H*9 - 40),
        (TILE_W*91 + TILE_W, MAP_HEIGHT - TILE_H*10 - 40),
        (TILE_W*95 + TILE_W*2, MAP_HEIGHT - TILE_H*11 - 40),
        (TILE_W*104 + TILE_W*2, MAP_HEIGHT - TILE_H*9 - 40),
        
        (TILE_W*26 + TILE_W, MAP_HEIGHT - TILE_H*7 - 40),
        (TILE_W*50 + TILE_W, MAP_HEIGHT - TILE_H*12 - 40),
        (TILE_W*92 + TILE_W, MAP_HEIGHT - TILE_H*13 - 40),
    ]
    
    exit_pos = (TILE_W*108 + TILE_W*2, MAP_HEIGHT - TILE_H*9 - 40)
    
    return {
        'platforms': platforms,
        'enemies': enemies,
        'items': items,
        'exit': exit_pos,
        'boss': None
    }