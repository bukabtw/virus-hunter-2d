# levels/level_3.py
import pygame
from settings import MAP_WIDTH, MAP_HEIGHT, PLATFORM_SIZES

def get_level():
    TILE_W, TILE_H = PLATFORM_SIZES['avast']
    OFFSET_Y = 600
    
    platforms = [
        pygame.Rect(0, 500 + OFFSET_Y, 6 * TILE_W, TILE_H),
        pygame.Rect(7 * TILE_W, 450 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(9 * TILE_W, 400 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(11 * TILE_W, 350 + OFFSET_Y, 2 * TILE_W, TILE_H),
        pygame.Rect(14 * TILE_W, 300 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(16 * TILE_W, 250 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(18 * TILE_W, 200 + OFFSET_Y, 3 * TILE_W, TILE_H),
        pygame.Rect(22 * TILE_W, 200 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(24 * TILE_W, 250 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(26 * TILE_W, 300 + OFFSET_Y, 2 * TILE_W, TILE_H),
        pygame.Rect(29 * TILE_W, 350 + OFFSET_Y, 5 * TILE_W, TILE_H*2),
        
        pygame.Rect(30 * TILE_W, 400 + OFFSET_Y, 24 * TILE_W, TILE_H*3),
        
        pygame.Rect(31 * TILE_W, 300 + OFFSET_Y, 3 * TILE_W, TILE_H),
        pygame.Rect(32 * TILE_W, 200 + OFFSET_Y, 2 * TILE_W, TILE_H),
        pygame.Rect(33 * TILE_W, 100 + OFFSET_Y, TILE_W, TILE_H),
        
        pygame.Rect(48 * TILE_W, 300 + OFFSET_Y, 3 * TILE_W, TILE_H),
        pygame.Rect(49 * TILE_W, 200 + OFFSET_Y, 2 * TILE_W, TILE_H),
        pygame.Rect(50 * TILE_W, 100 + OFFSET_Y, TILE_W, TILE_H),
        
        pygame.Rect(38 * TILE_W, 300 + OFFSET_Y, 6 * TILE_W, TILE_H),
        pygame.Rect(39 * TILE_W, 200 + OFFSET_Y, 4 * TILE_W, TILE_H),
        pygame.Rect(40 * TILE_W, 100 + OFFSET_Y, 2 * TILE_W, TILE_H),
        
        pygame.Rect(35 * TILE_W, 450 + OFFSET_Y, 2 * TILE_W, TILE_H),
        pygame.Rect(45 * TILE_W, 450 + OFFSET_Y, 2 * TILE_W, TILE_H),
        
        pygame.Rect(30 * TILE_W, 150 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(53 * TILE_W, 150 + OFFSET_Y, TILE_W, TILE_H),
        pygame.Rect(40 * TILE_W, 30 + OFFSET_Y, 2 * TILE_W, TILE_H),

        pygame.Rect(55 * TILE_W, 350 + OFFSET_Y, 3 * TILE_W, TILE_H),
        pygame.Rect(59 * TILE_W, 300 + OFFSET_Y, 2 * TILE_W, TILE_H),
        pygame.Rect(62 * TILE_W, 250 + OFFSET_Y, 3 * TILE_W, TILE_H*2),
        pygame.Rect(66 * TILE_W, 300 + OFFSET_Y, 2 * TILE_W, TILE_H),
    ]
    
    enemies = [
        (8 * TILE_W + 32, 418 + OFFSET_Y),
        (12 * TILE_W + 64, 318 + OFFSET_Y),
        (15 * TILE_W + 32, 268 + OFFSET_Y),
        (19 * TILE_W + 96, 168 + OFFSET_Y),
        (23 * TILE_W + 32, 168 + OFFSET_Y),
        (27 * TILE_W + 64, 268 + OFFSET_Y),
        (31 * TILE_W + 64, 318 + OFFSET_Y),
        (33 * TILE_W + 64, 318 + OFFSET_Y),
    ]
    
    items = [
        (6 * TILE_W + 64, 460 + OFFSET_Y),
        (10 * TILE_W + 32, 368 + OFFSET_Y),
        (13 * TILE_W + 64, 318 + OFFSET_Y),
        (17 * TILE_W + 32, 218 + OFFSET_Y),
        (20 * TILE_W + 96, 168 + OFFSET_Y),
        (25 * TILE_W + 32, 218 + OFFSET_Y),
        (28 * TILE_W + 64, 268 + OFFSET_Y),
        (30 * TILE_W + 128, 318 + OFFSET_Y),
        (31 * TILE_W + 128, 318 + OFFSET_Y),
        (32 * TILE_W + 64, 268 + OFFSET_Y),
        (41 * TILE_W + 128, 168 + OFFSET_Y),
        (48 * TILE_W + 64, 268 + OFFSET_Y),
        (40 * TILE_W + 64, 68 + OFFSET_Y),
        (30 * TILE_W + 32, 118 + OFFSET_Y),
        (53 * TILE_W + 32, 118 + OFFSET_Y),
        (40 * TILE_W + 64, -2 + OFFSET_Y),
        (56 * TILE_W + 64, 318 + OFFSET_Y),
        (60 * TILE_W + 64, 268 + OFFSET_Y),
        (63 * TILE_W + 96, 218 + OFFSET_Y),
    ]
    
    spawn_point = (100, 450 + OFFSET_Y)
    exit_point = (67 * TILE_W + 64, 250 + OFFSET_Y)
    
    boss_pos = (42 * TILE_W, 250 + OFFSET_Y)
    
    return {
        "platforms": platforms,
        "enemies": enemies,
        "items": items,
        "exit": exit_point,
        "boss": boss_pos,
        "spawn": spawn_point
    }