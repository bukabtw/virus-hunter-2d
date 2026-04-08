import pygame
import os
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type='hdd', tile_scale=(1, 1)):
        super().__init__()
        self.platform_type = platform_type
        self.width = width
        self.height = height
        
        self.image = pygame.Surface((width, height))
        self.image.fill(COLORS['BLACK'])
        
        self.rect = pygame.Rect(x, y, width, height)

        try:
            if platform_type == 'hdd':
                sprite_path = os.path.join(SPRITES_PATH, 'hdd.png')
                orig_w, orig_h = HDD_TILE_SIZE
            elif platform_type == 'ram':
                sprite_path = os.path.join(SPRITES_PATH, 'ram.png')
                orig_w, orig_h = RAM_TILE_SIZE
            elif platform_type == 'avast':
                sprite_path = os.path.join(SPRITES_PATH, 'avast.png')
                orig_w, orig_h = AVAST_TILE_SIZE
            else:
                sprite_path = None

            if sprite_path and os.path.exists(sprite_path):
                tile = pygame.image.load(sprite_path).convert_alpha()
                
                scale_w, scale_h = tile_scale
                new_w = orig_w * scale_w
                new_h = orig_h * scale_h
                tile = pygame.transform.scale(tile, (new_w, new_h))
                
                tile_w, tile_h = new_w, new_h
                
                for px in range(0, width, tile_w):
                    for py in range(0, height, tile_h):
                        self.image.blit(tile, (px, py))
            else:
                pygame.draw.rect(self.image, COLORS['GREEN'], (0, 0, width, height), 2)
        except Exception as e:
            pygame.draw.rect(self.image, COLORS['RED'], (0, 0, width, height), 2)