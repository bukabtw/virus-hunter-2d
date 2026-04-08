import pygame
from settings import *
from core.animated_entity import AnimatedEntity
from core.damageable import Damageable

class Enemy(AnimatedEntity, Damageable):
    def __init__(self, x, y, speed=1.5):
        animations = {
            'idle': ENEMY_ANIMATIONS['idle'],
            'walk_right': ENEMY_ANIMATIONS['walk_right'],
            'walk_left': ENEMY_ANIMATIONS['walk_left'],
            'attack_left': ENEMY_ANIMATIONS['attack_left'],
            'attack_right': ENEMY_ANIMATIONS['attack_right'],
        }
        
        sprite_path = f"{SPRITES_PATH}/{ENEMY_SPRITESHEET}"
        super().__init__(x, y, sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE, animations)
        
        Damageable.__init__(self, max_health=10, invincible_duration=20)
        
        self.speed = speed
        self.direction = 1
        self.attack_timer = 0
        self.attack_delay = 40
        self.knockback_timer = 0
        self.knockback_direction = 0
    
    def update(self, platforms, current_time, enemies, all_sprites, player):
        self.update_invincibility()
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
        
        self.update_animation()
    
    def take_damage(self, amount):
        if super().take_damage(amount):
            self.knockback_timer = 8
            self.knockback_direction = -self.direction
            if self.is_dead:
                self.kill()