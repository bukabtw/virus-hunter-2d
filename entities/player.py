import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, PLAYER_SPRITESHEET
)

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_frames(self, *args, **kwargs): return []


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.walk_right_frames = []
        self.walk_left_frames = []
        self.idle_right_frames = []
        self.idle_left_frames = []

        try:
            sprite_path = f"{SPRITES_PATH}/{PLAYER_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE)

            ROW_WALK_RIGHT = 11
            ROW_WALK_LEFT = 9
            WALK_FRAMES = 6

            self.walk_right_frames = sheet.get_row_frames(ROW_WALK_RIGHT, WALK_FRAMES)
            self.walk_left_frames = sheet.get_row_frames(ROW_WALK_LEFT, WALK_FRAMES)

            self.idle_right_frames = [self.walk_right_frames[0]] if self.walk_right_frames else []
            self.idle_left_frames = [self.walk_left_frames[0]] if self.walk_left_frames else []

            print(f"Загружено кадров ходьбы ВПРАВО: {len(self.walk_right_frames)}")
            print(f"Загружено кадров ходьбы ВЛЕВО: {len(self.walk_left_frames)}")

            if self.walk_right_frames:
                frame_size = self.walk_right_frames[0].get_size()
                print(f"Размер кадра: {frame_size[0]}x{frame_size[1]} пикселей")
                self.image = self.walk_right_frames[0]
            else:
                self.image = self._make_fallback()

        except Exception as e:
            print(f"Ошибка загрузки спрайтов: {e}")
            self.image = self._make_fallback()
            self.walk_left_frames = [self.image]
            self.walk_right_frames = [self.image]
            self.idle_left_frames = [self.image]
            self.idle_right_frames = [self.image]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width = SPRITE_WIDTH * SPRITE_SCALE
        self.rect.height = SPRITE_HEIGHT * SPRITE_SCALE

        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = True
        self.speed = 5
        self.jump_power = -12
        self.gravity = 0.8
        self.health = 5

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE, SPRITE_HEIGHT * SPRITE_SCALE)
        surf = pygame.Surface(size)
        surf.fill(COLORS['BLACK'])
        pygame.draw.circle(surf, COLORS['WHITE'], (size[0] // 3, size[1] // 3), 5)
        pygame.draw.circle(surf, COLORS['WHITE'], (size[0] * 2 // 3, size[1] // 3), 5)
        pygame.draw.rect(surf, COLORS['BLUE'], (size[0] // 2 - 5, size[1] // 2, 10, 15))
        return surf

    def update(self, platforms):
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p) and self.vel_y >= 0:
                self.rect.bottom = p.top
                self.vel_y = 0
                self.on_ground = True

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 1200:
            self.rect.right = 1200
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 700:
            self.rect.bottom = 700
            self.vel_y = 0
            self.on_ground = True

        self._update_animation()

    def _update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            frames = self._get_current_frames()
            if frames:
                self.current_frame = (self.current_frame + 1) % len(frames)
                self.image = frames[self.current_frame]

    def _get_current_frames(self):
        if abs(self.vel_x) > 0.5:
            if self.facing_right:
                return self.walk_right_frames if self.walk_right_frames else [self.image]
            else:
                return self.walk_left_frames if self.walk_left_frames else [self.image]
        else:
            if self.facing_right:
                return self.idle_right_frames
            else:
                return self.idle_left_frames

    def move_left(self):
        self.vel_x = -self.speed
        self.facing_right = False

    def move_right(self):
        self.vel_x = self.speed
        self.facing_right = True

    def stop(self):
        self.vel_x = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False