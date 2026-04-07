import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, ENEMY_SPRITESHEET, ENEMY_ANIMATIONS,
    MAP_WIDTH, MAP_HEIGHT
)

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass

        def get_frames(self, *args, **kwargs): return []


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=1.5):
        super().__init__()

        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.idle_frames = []
        self.walk_right_frames = []
        self.walk_left_frames = []
        self.attack_left_frames = []
        self.attack_right_frames = []

        self.state = 'idle'

        try:
            sprite_path = f"{SPRITES_PATH}/{ENEMY_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE)


            self.idle_frames = sheet.get_row_frames(ENEMY_ANIMATIONS['idle'][0], ENEMY_ANIMATIONS['idle'][1])
            self.walk_right_frames = sheet.get_row_frames(ENEMY_ANIMATIONS['walk_right'][0], ENEMY_ANIMATIONS['walk_right'][1])
            self.walk_left_frames = sheet.get_row_frames(ENEMY_ANIMATIONS['walk_left'][0], ENEMY_ANIMATIONS['walk_left'][1])
            self.attack_left_frames = sheet.get_row_frames(ENEMY_ANIMATIONS['attack_left'][0], ENEMY_ANIMATIONS['attack_left'][1])
            self.attack_right_frames = sheet.get_row_frames(ENEMY_ANIMATIONS['attack_right'][0], ENEMY_ANIMATIONS['attack_right'][1])

            print(f"Enemy: Загружено кадров idle: {len(self.idle_frames)}, walk: {len(self.walk_right_frames)}, attack: {len(self.attack_left_frames)}")

            if self.idle_frames:
                self.image = self.idle_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            print(f"Ошибка загрузки спрайтов врага: {e}")
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = 1
        self.is_attacking = False
        self.health = 20

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE, SPRITE_HEIGHT * SPRITE_SCALE)
        surf = pygame.Surface(size)
        surf.fill(COLORS['RED'])
        return surf

    def update(self, platforms, current_time, enemies, all_sprites):
        if self.is_attacking:
            self.state = 'attack_left' if not self.facing_right else 'attack_right'
        else:
            if self.direction > 0:
                self.state = 'walk_right'
            else:
                self.state = 'walk_left'
            self.facing_right = self.direction > 0

        self.rect.x += self.speed * self.direction

        if self.rect.left <= 0 or self.rect.right >= MAP_WIDTH:
            self.direction *= -1

        if self.direction > 0:
            self.state = 'walk_right'
            self.facing_right = True
        elif self.direction < 0:
            self.state = 'walk_left'
            self.facing_right = False

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
        if self.state == 'idle':
            return self.idle_frames if self.idle_frames else [self.image]
        elif self.state == 'walk_right':
            return self.walk_right_frames if self.walk_right_frames else [self.image]
        elif self.state == 'walk_left':
            return self.walk_left_frames if self.walk_left_frames else [self.image]
        elif self.state == 'attack_left':
            return self.attack_left_frames if self.attack_left_frames else [self.image]
        elif self.state == 'attack_right':
            return self.attack_right_frames if self.attack_right_frames else [self.image]
        return [self.image]


    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()