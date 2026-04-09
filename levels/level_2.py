import pygame
from settings import MAP_WIDTH, MAP_HEIGHT, PLATFORM_SIZES

def get_level():
    TILE_W, TILE_H = PLATFORM_SIZES['hdd']
    
    platforms = [
        pygame.Rect(0, MAP_HEIGHT - TILE_H*2, TILE_W*15, TILE_H*2),
        
        pygame.Rect(TILE_W*15, MAP_HEIGHT - TILE_H*3, TILE_W*3, TILE_H),
        
        pygame.Rect(TILE_W*16, MAP_HEIGHT - TILE_H*3, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*21, MAP_HEIGHT - TILE_H*3, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*26, MAP_HEIGHT - TILE_H*4, TILE_W*4, TILE_H),
        
        pygame.Rect(TILE_W*31, MAP_HEIGHT - TILE_H*4, TILE_W*5, TILE_H),
        pygame.Rect(TILE_W*37, MAP_HEIGHT - TILE_H*5, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*42, MAP_HEIGHT - TILE_H*5, TILE_W*6, TILE_H*2),
        
        pygame.Rect(TILE_W*48, MAP_HEIGHT - TILE_H*6, TILE_W*4, TILE_H),
        
        pygame.Rect(TILE_W*49, MAP_HEIGHT - TILE_H*5, TILE_W*8, TILE_H*2),
        pygame.Rect(TILE_W*51, MAP_HEIGHT - TILE_H*7, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*56, MAP_HEIGHT - TILE_H*7, TILE_W*4, TILE_H),
        
        pygame.Rect(TILE_W*73, MAP_HEIGHT - TILE_H*8, TILE_W*4, TILE_H),
 
        pygame.Rect(TILE_W*61, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*58, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H), 
        pygame.Rect(TILE_W*55, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*52, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H), 
        pygame.Rect(TILE_W*49, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*46, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*43, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*40, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*37, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*34, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*31, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*28, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*25, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        
        # Сплошные платформы влево от 2382 до 1435
        pygame.Rect(TILE_W*23, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*21, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*19, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*17, MAP_HEIGHT - TILE_H*2, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*15, MAP_HEIGHT - TILE_H*2, TILE_W*3, TILE_H),
        
        pygame.Rect(TILE_W*61, MAP_HEIGHT - TILE_H*8, TILE_W*5, TILE_H),
        pygame.Rect(TILE_W*67, MAP_HEIGHT - TILE_H*7, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*72, MAP_HEIGHT - TILE_H*6, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*77, MAP_HEIGHT - TILE_H*5, TILE_W*5, TILE_H*2),
        
        pygame.Rect(TILE_W*83, MAP_HEIGHT - TILE_H*6, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*88, MAP_HEIGHT - TILE_H*7, TILE_W*4, TILE_H),
        pygame.Rect(TILE_W*93, MAP_HEIGHT - TILE_H*8, TILE_W*6, TILE_H*2),
        
        pygame.Rect(TILE_W*18, MAP_HEIGHT - TILE_H*6, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*44, MAP_HEIGHT - TILE_H*8, TILE_W*2, TILE_H),
        pygame.Rect(TILE_W*69, MAP_HEIGHT - TILE_H*10, TILE_W*2, TILE_H),
    ]
    
    enemies = [
        (TILE_W*17 + TILE_W*2, MAP_HEIGHT - TILE_H*3 - 30),
        (TILE_W*27 + TILE_W*2, MAP_HEIGHT - TILE_H*4 - 30),
        (TILE_W*32 + TILE_W*2, MAP_HEIGHT - TILE_H*4 - 30),
        (TILE_W*38 + TILE_W*2, MAP_HEIGHT - TILE_H*5 - 30),
        (TILE_W*50 + TILE_W*2, MAP_HEIGHT - TILE_H*5 - 30),
        (TILE_W*54 + TILE_W*2, MAP_HEIGHT - TILE_H*5 - 30),
        (TILE_W*52 + TILE_W*2, MAP_HEIGHT - TILE_H*7 - 30),
        (TILE_W*58 + TILE_W*2, MAP_HEIGHT - TILE_H*7 - 30),
        (TILE_W*68 + TILE_W*2, MAP_HEIGHT - TILE_H*7 - 30),
        (TILE_W*73 + TILE_W*2, MAP_HEIGHT - TILE_H*6 - 30),
        (TILE_W*84 + TILE_W*2, MAP_HEIGHT - TILE_H*6 - 30),
        (TILE_W*89 + TILE_W*2, MAP_HEIGHT - TILE_H*7 - 30),
        (TILE_W*95 + TILE_W*3, MAP_HEIGHT - TILE_H*8 - 30),
    ]
    
    items = [
        (TILE_W*5 + TILE_W, MAP_HEIGHT - TILE_H*2 - 60),
        (TILE_W*17 + TILE_W*2, MAP_HEIGHT - TILE_H*3 - 60),
        (TILE_W*27 + TILE_W*2, MAP_HEIGHT - TILE_H*4 - 60),
        (TILE_W*38 + TILE_W*2, MAP_HEIGHT - TILE_H*5 - 60),
        (TILE_W*50 + TILE_W, MAP_HEIGHT - TILE_H*5 - 60),
        (TILE_W*52 + TILE_W, MAP_HEIGHT - TILE_H*7 - 60),
        (TILE_W*57 + TILE_W, MAP_HEIGHT - TILE_H*7 - 60),
        (TILE_W*68 + TILE_W*2, MAP_HEIGHT - TILE_H*7 - 60),
        (TILE_W*78 + TILE_W*2, MAP_HEIGHT - TILE_H*5 - 60),
        (TILE_W*89 + TILE_W*2, MAP_HEIGHT - TILE_H*7 - 60),
        (TILE_W*18 + TILE_W, MAP_HEIGHT - TILE_H*6 - 60),
        (TILE_W*44 + TILE_W, MAP_HEIGHT - TILE_H*8 - 60),
        (TILE_W*69 + TILE_W, MAP_HEIGHT - TILE_H*10 - 60),
    ]
    
    exit_pos = (TILE_W*99 + TILE_W*3, MAP_HEIGHT - TILE_H*8 - 40)
    
    return {
        'platforms': platforms,
        'enemies': enemies,
        'items': items,
        'exit': exit_pos,
        'boss': None
    }