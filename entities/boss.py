import pygame
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, BOSS_SPRITESHEET, BOSS_ANIMATIONS, SCREEN_WIDTH, MAP_WIDTH
)
from .enemy import Enemy

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass
        def get_row_frames(self, *args, **kwargs): return []


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, spawn_interval=3000):
        super().__init__()

        self.facing_right = True
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8

        self.idle_frames = []
        self.look_left_frames = []
        self.look_right_frames = []
        self.attack_left_frames = []
        self.attack_right_frames = []

        self.state = 'idle'
        self.health = 100

        try:
            sprite_path = f"{SPRITES_PATH}/{BOSS_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE)

            self.idle_frames = sheet.get_row_frames(BOSS_ANIMATIONS['idle'][0], BOSS_ANIMATIONS['idle'][1])
            self.look_left_frames = sheet.get_row_frames(BOSS_ANIMATIONS['look_left'][0], BOSS_ANIMATIONS['look_left'][1])
            self.look_right_frames = sheet.get_row_frames(BOSS_ANIMATIONS['look_right'][0], BOSS_ANIMATIONS['look_right'][1])
            self.attack_left_frames = sheet.get_row_frames(BOSS_ANIMATIONS['attack_left'][0], BOSS_ANIMATIONS['attack_left'][1])
            self.attack_right_frames = sheet.get_row_frames(BOSS_ANIMATIONS['attack_right'][0], BOSS_ANIMATIONS['attack_right'][1])

            if self.idle_frames:
                self.image = self.idle_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1.5
        self.direction = 1
        
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
        self.attack_timer = 0
        self.attack_delay = 60
        self.attack_cooldown = 0
        
        self.knockback_timer = 0
        self.knockback_direction = 0

    def _make_fallback(self):
        size = (SPRITE_WIDTH * SPRITE_SCALE * 3, SPRITE_HEIGHT * SPRITE_SCALE * 3)
        surf = pygame.Surface(size)
        surf.fill(COLORS['PURPLE'])
        return surf

    def update(self, platforms, current_time, enemies_group, all_sprites_group, player):
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
            self.rect.x += self.knockback_direction * 5
            return
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if player and player.alive():
            if self.rect.x < player.rect.x:
                self.direction = 1
                self.facing_right = True
            elif self.rect.x > player.rect.x:
                self.direction = -1
                self.facing_right = False
            
            self.rect.x += self.speed * self.direction
        
        if player and self.rect.colliderect(player.rect) and self.attack_cooldown == 0:
            self.attack_cooldown = self.attack_delay
            player.take_damage(2)

            self.knockback_timer = 10
            self.knockback_direction = -self.direction
        
        if current_time - self.spawn_timer > self.spawn_interval:
            self.spawn_timer = current_time
            offset = -50 if self.direction > 0 else 50
            virus = Enemy(
                self.rect.centerx + offset, 
                self.rect.bottom - 20, 
                speed=2.0
            )
            enemies_group.add(virus)
            all_sprites_group.add(virus)
        
        if self.attack_cooldown > 0:
            self.state = 'attack_left' if not self.facing_right else 'attack_right'
        else:
            self.state = 'look_left' if not self.facing_right else 'look_right'
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH
        
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
        elif self.state == 'look_left':
            return self.look_left_frames if self.look_left_frames else [self.image]
        elif self.state == 'look_right':
            return self.look_right_frames if self.look_right_frames else [self.image]
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