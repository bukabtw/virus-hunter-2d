import pygame
from settings import *
from core.animated_entity import AnimatedEntity
from core.damageable import Damageable
from entities.enemy import Enemy

class Boss(AnimatedEntity, Damageable):
    def __init__(self, x, y, spawn_interval=3000):
        animations = {
            'idle': BOSS_ANIMATIONS['idle'],
            'look_left': BOSS_ANIMATIONS['look_left'],
            'look_right': BOSS_ANIMATIONS['look_right'],
            'attack_left': BOSS_ANIMATIONS['attack_left'],
            'attack_right': BOSS_ANIMATIONS['attack_right'],
        }
        
        sprite_path = f"{SPRITES_PATH}/{BOSS_SPRITESHEET}"
        super().__init__(x, y, sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE, animations)
        
        Damageable.__init__(self, max_health=100, invincible_duration=30)
        
        self.speed = 1.5
        self.direction = 1
        
        self.spawn_timer = 0
        self.spawn_interval = spawn_interval
        self.attack_timer = 0
        self.attack_delay = 60
        self.attack_cooldown = 0
        
        self.knockback_timer = 0
        self.knockback_direction = 0
        self.is_boss = True
        self.sound_manager = None
    
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
            
            if self.rect.colliderect(player.rect) and self.attack_cooldown == 0:
                self.attack_cooldown = self.attack_delay
                player.take_damage(1.5)
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
        
        # Границы
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH
        
        self.update_animation()
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
        else:
            self.knockback_timer = 8
            self.knockback_direction = -self.direction

    def get_damage_color(self):
        if self.is_flashing:
            return COLORS['BLACK']
        return None