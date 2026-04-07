import pygame
import os
from settings import (
    COLORS, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE,
    SPRITES_PATH, PROJECTILE_SPRITESHEET, PROJECTILE_ANIMATIONS,
    MAP_WIDTH, MAP_HEIGHT
)

try:
    from core.sprite_sheet import SpriteSheet
except ImportError:
    class SpriteSheet:
        def __init__(self, *args, **kwargs): pass
        def get_row_frames(self, *args, **kwargs): return []


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, owner):
        super().__init__()

        self.owner = owner
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 10
        self.has_hit = False
        self.damage = 5
        self.state = 'fly'
        self.start_x = x
        self.start_y = y
        self.max_distance = 600
        self.fly_frames = []

        try:
            sprite_path = f"{SPRITES_PATH}/{PROJECTILE_SPRITESHEET}"
            sheet = SpriteSheet(sprite_path, 32, 32, SPRITE_SCALE)
            self.fly_frames = sheet.frames[:12]
            if self.fly_frames:
                self.image = self.fly_frames[0]
            else:
                self.image = self._make_fallback()
        except Exception as e:
            self.image = self._make_fallback()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        dx = target_x - x
        dy = target_y - y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.vx = dx / dist * 15
        self.vy = dy / dist * 15
        
        self.facing_right = self.vx > 0

    def _make_fallback(self):
        size = (32, 32)
        surf = pygame.Surface(size)
        surf.fill(COLORS['YELLOW'])
        pygame.draw.circle(surf, COLORS['ORANGE'], (16, 16), 12)
        return surf

    def update(self, player):
        if self.state == 'fly':
            self.rect.x += self.vx
            self.rect.y += self.vy
            
            if abs(self.rect.centerx - self.start_x) >= self.max_distance:
                self.state = 'return'
            
            if abs(self.rect.centery - self.start_y) >= 400:
                self.state = 'return'
            
            if (self.rect.x < -500 or self.rect.x > MAP_WIDTH + 500 or 
                self.rect.y < -500 or self.rect.y > MAP_HEIGHT + 500):
                self.kill()
                
        elif self.state == 'return':
            if self.rect.centerx < player.rect.centerx:
                self.rect.x += 8
            elif self.rect.centerx > player.rect.centerx:
                self.rect.x -= 8
                
            if self.rect.centery < player.rect.centery:
                self.rect.y += 5
            elif self.rect.centery > player.rect.centery:
                self.rect.y -= 5
            
            if (abs(self.rect.centerx - player.rect.centerx) < 40 and 
                abs(self.rect.centery - player.rect.centery) < 40):
                if hasattr(self.owner, 'phone_in_air'):
                    self.owner.phone_in_air = False
                self.kill()
        
        self._update_animation()

    def hit(self):
        if not self.has_hit:
            self.has_hit = True
            self.state = 'return'

    def _update_animation(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.fly_frames:
                self.current_frame = (self.current_frame + 1) % len(self.fly_frames)
                self.image = self.fly_frames[self.current_frame]
                if not self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self, amount):
        pass