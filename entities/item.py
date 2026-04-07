import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, ITEM_SPRITESHEET, ITEM_ANIMATIONS
)

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_frames(self, *args, **kwargs): return []


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type='computer'):
        super().__init__()

        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.item_type = item_type
        self.idle_frames = []

        try:
            sprite_path = f"{SPRITES_PATH}/{ITEM_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE)

            self.idle_frames = sheet.get_row_frames(ITEM_ANIMATIONS['idle'][0], ITEM_ANIMATIONS['idle'][1])

            if self.idle_frames:
                self.image = self.idle_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE // 2, SPRITE_HEIGHT * SPRITE_SCALE // 2)
        surf = pygame.Surface(size)
        surf.fill(COLORS['CYAN'])
        pygame.draw.rect(surf, COLORS['BLACK'], (4, 4, self.image.get_width()-8, self.image.get_height()-8))
        pygame.draw.rect(surf, COLORS['GRAY'], (self.image.get_width()//2-4, self.image.get_height()-6, 8, 4))
        return surf

    def update(self, *args):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.idle_frames:
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_frame]