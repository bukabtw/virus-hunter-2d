import pygame
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
                tile_image = pygame.transform.scale(tile_image, (SPRITE_WIDTH, SPRITE_HEIGHT))
                if width > SPRITE_WIDTH:
                    for i in range(0, width, SPRITE_WIDTH):
                        offset_x = i
                        offset_y = 0
                        self.image.blit(tile_image, (offset_x, offset_y))
                else:
                    tile_image = pygame.transform.scale(tile_image, (width, height))
                    self.image.blit(tile_image, (0, 0))
            else:
                # Заглушка
                self.image.fill(COLORS['GRAY'])
        except Exception as e:
            print(f"Ошибка загрузки спрайта платформы: {e}")
            self.image.fill(COLORS['GRAY'])