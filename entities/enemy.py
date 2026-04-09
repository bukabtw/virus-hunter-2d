import pygame
import random
from settings import *
from core.animated_entity import AnimatedEntity
from core.damageable import Damageable

class Enemy(AnimatedEntity, Damageable):
    def __init__(self, x, y, speed=1.5, enemy_type='normal'):
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
        
        self.enemy_type = enemy_type
        if enemy_type == 'fast':
            self.speed = speed * 1.5
            self.max_health = 5
            self.health = 5
            self.attack_delay = 30
        elif enemy_type == 'tank':
            self.speed = speed * 0.6
            self.max_health = 25
            self.health = 25
            self.attack_delay = 60
        else:
            self.speed = speed
            self.attack_delay = 40
        
        COLLIDE_W = 80
        COLLIDE_H = 85
        OFFSET_X = 24
        OFFSET_Y = 22
        
        self.collide_offset_x = OFFSET_X
        self.collide_offset_y = OFFSET_Y
        
        self.visual_rect = self.rect.copy()
        
        self.collision_rect = pygame.Rect(
            self.visual_rect.x + OFFSET_X,
            self.visual_rect.y + OFFSET_Y,
            COLLIDE_W,
            COLLIDE_H
        )
        
        self.direction = random.choice([-1, 1])
        self.attack_timer = 0
        self.knockback_timer = 0
        self.knockback_direction = 0
        self.patrol_timer = 0
        self.patrol_direction = self.direction
        
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.8
        self.frozen = False
        self.on_ground = False
    
    def check_ground_below(self, platforms):
        """Проверяет, есть ли земля под врагом"""
        test_rect = self.collision_rect.copy()
        test_rect.y += 5
        test_rect.x += self.direction * 10
        
        for p in platforms:
            if test_rect.colliderect(p.rect):
                return True
        return False
    
    def check_wall_ahead(self, platforms):
        """Проверяет, есть ли стена впереди"""
        test_rect = self.collision_rect.copy()
        test_rect.x += self.direction * 10
        
        for p in platforms:
            if test_rect.colliderect(p.rect):
                return True
        return False
    
    def update(self, platforms, current_time, enemies, all_sprites, player):
        self.update_invincibility()
        
        if self.frozen:
            self.rect = self.visual_rect
            self.update_animation()
            return
        
        self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
        self.collision_rect.y = self.visual_rect.y + self.collide_offset_y
        
        if self.attack_timer > 0:
            self.attack_timer -= 1
        if self.knockback_timer > 0:
            self.knockback_timer -= 1
            self.visual_rect.x += self.knockback_direction * 5
            self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
            self.rect = self.visual_rect
            return
        
        self.vel_y += self.gravity
        self.collision_rect.y += self.vel_y
        
        self.on_ground = False
        for p in platforms:
            if self.collision_rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.collision_rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    break
                elif self.vel_y < 0:
                    self.collision_rect.top = p.rect.bottom
                    self.vel_y = 0
                    break
        
        self.visual_rect.x = self.collision_rect.x - self.collide_offset_x
        self.visual_rect.y = self.collision_rect.y - self.collide_offset_y
        
        if self.on_ground:
            if player and player.alive():
                dx = player.visual_rect.centerx - self.visual_rect.centerx
                
                if abs(dx) < 300:
                    if dx > 0:
                        self.direction = 1
                        self.facing_right = True
                    else:
                        self.direction = -1
                        self.facing_right = False
                    
                    if self.check_ground_below(platforms) and not self.check_wall_ahead(platforms):
                        self.collision_rect.x += self.speed * self.direction
                    else:
                        self.direction *= -1
                        self.facing_right = not self.facing_right
                else:
                    self.patrol_timer += 1
                    if self.patrol_timer > 120:
                        self.patrol_direction *= -1
                        self.patrol_timer = 0
                    self.direction = self.patrol_direction
                    self.facing_right = self.direction > 0

                    if self.check_ground_below(platforms) and not self.check_wall_ahead(platforms):
                        self.collision_rect.x += self.speed * self.direction
                    else:
                        self.direction *= -1
                        self.facing_right = not self.facing_right
            else:
                if self.check_ground_below(platforms) and not self.check_wall_ahead(platforms):
                    self.collision_rect.x += self.speed * self.direction
                else:
                    self.direction *= -1
                    self.facing_right = not self.facing_right
            
            for p in platforms:
                if self.collision_rect.colliderect(p.rect):
                    if self.direction > 0:
                        self.collision_rect.right = p.rect.left
                    else:
                        self.collision_rect.left = p.rect.right
                    self.direction *= -1
                    self.facing_right = not self.facing_right
                    break
            
            self.visual_rect.x = self.collision_rect.x - self.collide_offset_x
            self.visual_rect.y = self.collision_rect.y - self.collide_offset_y
            
            if player and player.alive():
                if self.collision_rect.colliderect(player.collision_rect) and self.attack_timer == 0:
                    self.attack_timer = self.attack_delay
                    player.take_damage(2 if self.enemy_type == 'tank' else 1)
                    self.knockback_timer = 10
                    self.knockback_direction = -self.direction
        
        if self.collision_rect.left < 0:
            self.collision_rect.left = 0
            self.direction *= -1
            self.facing_right = not self.facing_right
        if self.collision_rect.right > MAP_WIDTH:
            self.collision_rect.right = MAP_WIDTH
            self.direction *= -1
            self.facing_right = not self.facing_right
        
        self.visual_rect.x = self.collision_rect.x - self.collide_offset_x
        self.visual_rect.y = self.collision_rect.y - self.collide_offset_y
        self.rect = self.visual_rect
        self.collision_rect.x = self.visual_rect.x + self.collide_offset_x
        self.collision_rect.y = self.visual_rect.y + self.collide_offset_y
        
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

    def get_damage_color(self):
        if self.is_flashing:
            return COLORS['RED']
        return None