import pygame
import os
from settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, platform_type='hdd'):
        super().__init__()
        self.platform_type = platform_type
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)

        try:
            if platform_type == 'hdd':
                sprite_path = os.path.join(SPRITES_PATH, 'hdd.png')
            elif platform_type == 'ram':
                sprite_path = os.path.join(SPRITES_PATH, 'ram.png')
            else:
                sprite_path = None

            if sprite_path:
                tile_image = pygame.image.load(sprite_path).convert_alpha()
                tile_width = tile_image.get_width()
                tile_height = tile_image.get_height()
                if width != tile_width or height != tile_height:
                    tile_image = pygame.transform.scale(tile_image, (width, height))
                self.image.blit(tile_image, (0, 0))
            else:
                # Заглушка
                self.image.fill(COLORS['GRAY'])
        except Exception as e:
            print(f"Ошибка загрузки спрайта платформы: {e}")
            self.image.fill(COLORS['GRAY'])