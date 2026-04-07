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
        def get_row_frames(self, *args, **kwargs): return []


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

            if self.idle_frames:
                self.image = self.idle_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = 10
        
        self.attack_timer = 0
        self.attack_delay = 40
        self.knockback_timer = 0
        self.knockback_direction = 0

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE, SPRITE_HEIGHT * SPRITE_SCALE)
        surf = pygame.Surface(size)
        surf.fill(COLORS['RED'])
        return surf

    def update(self, platforms, current_time, enemies, all_sprites, player):
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
            self.rect.x += self.knockback_direction * 5
            return
        
        if player and player.alive():
            if self.rect.x < player.rect.x:
                self.direction = 1
                self.facing_right = True
            elif self.rect.x > player.rect.x:
                self.direction = -1
                self.facing_right = False
            
            self.rect.x += self.speed * self.direction
            
            if self.rect.colliderect(player.rect) and self.attack_timer == 0:
                self.attack_timer = self.attack_delay
                player.take_damage(1)
                self.knockback_timer = 10
                self.knockback_direction = -self.direction
        else:
            self.rect.x += self.speed * self.direction
            if self.rect.left <= 0 or self.rect.right >= MAP_WIDTH:
                self.direction *= -1
                self.facing_right = self.direction > 0

        if self.attack_timer > 0:
            self.state = 'attack_left' if not self.facing_right else 'attack_right'
        else:
            self.state = 'walk_right' if self.direction > 0 else 'walk_left'
        
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
        else:
            self.knockback_timer = 8
            self.knockback_direction = -self.direction