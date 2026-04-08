import pygame
from settings import *
from core.animated_entity import AnimatedEntity
from core.damageable import Damageable
from entities.projectile import Projectile

class Player(AnimatedEntity, Damageable):
    def __init__(self, x, y):
        animations = {
            'idle_right': PLAYER_ANIMATIONS['idle_right'],
            'idle_left': PLAYER_ANIMATIONS['idle_left'],
            'walk_right': PLAYER_ANIMATIONS['walk_right'],
            'walk_left': PLAYER_ANIMATIONS['walk_left'],
            'jump_right': PLAYER_ANIMATIONS['jump_right'],
            'jump_left': PLAYER_ANIMATIONS['jump_left'],
            'attack_right': PLAYER_ANIMATIONS['attack_right'],
            'attack_left': PLAYER_ANIMATIONS['attack_left'],
        }
        
        sprite_path = f"{SPRITES_PATH}/{PLAYER_SPRITESHEET}"
        super().__init__(x, y, sprite_path, SPRITE_WIDTH, SPRITE_HEIGHT, SPRITE_SCALE, animations)
        
        Damageable.__init__(self, max_health=5, invincible_duration=60)
        
        COLLIDE_W = 50
        COLLIDE_H = 95
        OFFSET_X = 38
        OFFSET_Y = 28
        
        self.collide_offset_x = OFFSET_X
        self.collide_offset_y = OFFSET_Y
        
        self.collision_rect = pygame.Rect(
            self.rect.x + OFFSET_X,
            self.rect.y + OFFSET_Y,
            COLLIDE_W,
            COLLIDE_H
        )
        
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -20
        self.gravity = 0.8
        self.on_ground = True
        
        self.collected_items = []
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = 400
        self.attack_cooldown = 0
        self.attack_cooldown_time = 500
        self.phone_in_air = False
        self.camera_x = 0
        self.camera_y = 0

        self.ram_platform = False
    
    def update(self, platforms):
        self.update_invincibility()
        
        self.vel_y += self.gravity
        self.collision_rect.y += self.vel_y
        
        self.on_ground = False
        
        for p in platforms:
            if self.collision_rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.collision_rect.bottom = p.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.ram_platform = hasattr(p, 'platform_type') and p.platform_type == 'ram'
                    break
                elif self.vel_y < 0:
                    self.collision_rect.top = p.rect.bottom
                    self.vel_y = 0
                    break
        
        self.rect.x = self.collision_rect.x - self.collide_offset_x
        self.rect.y = self.collision_rect.y - self.collide_offset_y
        
        self.collision_rect.x += self.vel_x
        
        for p in platforms:
            if self.collision_rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.collision_rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.collision_rect.left = p.rect.right
                break
        
        self.rect.x = self.collision_rect.x - self.collide_offset_x
        self.rect.y = self.collision_rect.y - self.collide_offset_y
        
        if self.ram_platform:
            self.speed = 6.5
        else:
            self.speed = 5
        
        if self.collision_rect.left < 0:
            self.collision_rect.left = 0
        if self.collision_rect.right > MAP_WIDTH:
            self.collision_rect.right = MAP_WIDTH
        if self.collision_rect.top < 0:
            self.collision_rect.top = 0
        if self.collision_rect.bottom > MAP_HEIGHT:
            self.collision_rect.bottom = MAP_HEIGHT
            self.vel_y = 0
            self.on_ground = True
        
        self.rect.x = self.collision_rect.x - self.collide_offset_x
        self.rect.y = self.collision_rect.y - self.collide_offset_y
        
        if self.is_attacking:
            self.state = 'attack_right' if self.facing_right else 'attack_left'
            if pygame.time.get_ticks() - self.attack_timer > self.attack_duration:
                self.is_attacking = False
        elif abs(self.vel_x) > 0.5:
            self.state = 'walk_right' if self.facing_right else 'walk_left'
        elif not self.on_ground:
            self.state = 'jump_right' if self.facing_right else 'jump_left'
        else:
            self.state = 'idle_right' if self.facing_right else 'idle_left'

        self.update_animation()

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

    def attack(self, target_x, target_y):
        current_time = pygame.time.get_ticks()
        if not self.is_attacking and current_time - self.attack_cooldown > self.attack_cooldown_time and not self.phone_in_air:
            self.is_attacking = True
            self.attack_timer = current_time
            self.attack_cooldown = current_time
            self.phone_in_air = True
            
            proj = Projectile(
                self.rect.centerx,
                self.rect.centery,
                target_x,
                target_y,
                self
            )
            return proj
        return None

    def take_damage(self, amount):
        super().take_damage(amount)

    def get_damage_color(self):
        if self.is_flashing:
            return COLORS['RED']
        return None