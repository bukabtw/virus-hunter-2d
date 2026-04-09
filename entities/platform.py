import pygame
import os
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type='hdd'):
        super().__init__()
        self.platform_type = platform_type
        self.width = width
        self.height = height
        
        if platform_type == 'ram':
            sprite_path = os.path.join(SPRITES_PATH, 'ram.png')
            base_w, base_h = RAM_TILE_SIZE
        elif platform_type == 'hdd':
            sprite_path = os.path.join(SPRITES_PATH, 'hdd.png')
            base_w, base_h = HDD_TILE_SIZE
        elif platform_type == 'avast':
            sprite_path = os.path.join(SPRITES_PATH, 'avast.png')
            base_w, base_h = AVAST_TILE_SIZE
        else:
            sprite_path = None
            base_w, base_h = 64, 64
        
        tile_w = base_w * PLATFORM_SCALE
        tile_h = base_h * PLATFORM_SCALE
        
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        try:
            if sprite_path and os.path.exists(sprite_path):
                tile = pygame.image.load(sprite_path).convert_alpha()
                tile = pygame.transform.scale(tile, (tile_w, tile_h))
                
                for px in range(0, width, tile_w):
                    for py in range(0, height, tile_h):
                        clip_w = min(tile_w, width - px)
                        clip_h = min(tile_h, height - py)
                        
                        if clip_w > 0 and clip_h > 0:
                            tile_part = tile.subsurface((0, 0, clip_w, clip_h))
                            self.image.blit(tile_part, (px, py))
            else:
                color = COLORS.get(platform_type.upper(), COLORS['GREEN'])
                self.image.fill(color)
                pygame.draw.rect(self.image, COLORS['BLACK'], (0, 0, width, height), 2)
                
        except Exception as e:
            print(f"Ошибка загрузки платформы {platform_type}: {e}")
            self.image.fill(COLORS['GRAY'])
            pygame.draw.rect(self.image, COLORS['BLACK'], (0, 0, width, height), 2)
        
        self.rect = pygame.Rect(x, y, width, height)